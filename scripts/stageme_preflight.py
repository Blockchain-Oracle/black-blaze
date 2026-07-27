#!/usr/bin/env python3
"""Zero-secret execution-readiness checks for StageMe.

The preflight never reads media bytes beyond local metadata/hash checks, never
makes provider or B2 calls, and never prints environment-variable values.
"""

from __future__ import annotations

import argparse
import array
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

PASS = "pass"
WARNING = "warning"
BLOCKER = "blocker"
NOT_YET_REQUIRED = "not-yet-required"

ANYACCOMP_CODE_COMMIT = "82604b5e3107944ad4c49fc64900b86118ae2c62"
ANYACCOMP_CHECKPOINT_REVISION = "9aa9e62427337bf1df4caa3c4f3e6ad934522e71"
ACESTEP_CODE_COMMIT = "6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0"
ACESTEP_MODEL_ID = "ACE-Step/acestep-v15-base"
ACESTEP_CHECKPOINT_REVISION = "e432212fec32b8965a14ffa57ae653438d6abd14"
MIN_ANYACCOMP_VRAM_MIB = 24 * 1024
MIN_ANYACCOMP_COMPUTE_CAPABILITY = (8, 0)
ANYACCOMP_CHECKPOINTS = {
    "flow_matching/pytorch_model.bin": (
        880_790_586,
        "e6802bd1123935a54e990cb8d3897a18190df6c53f73db021baa28c420721129",
    ),
    "vocoder/model.safetensors": (
        1_020_206_416,
        "1b7efd04c71c058cd00b4e9a91c761b31da745f878b7d7ee839e157104d3a7da",
    ),
    "vq/pytorch_model.bin": (
        177_202_134,
        "9d7f48cefea30602b2148c057faf14ecad168184e8063c8377dd57f208dc65fc",
    ),
}

PHASES = (
    "precall",
    "anyaccomp-binding",
    "anyaccomp-local",
    "anyaccomp-hosted",
    "ace-hosted",
    "b2-canary",
    "render",
    "wan",
    "all",
)

MODEL_PHASES = {"anyaccomp-local", "anyaccomp-hosted", "ace-hosted", "all"}
MODEL_BINDING_PHASES = MODEL_PHASES | {"anyaccomp-binding"}
LOCAL_GPU_PHASES = {"anyaccomp-local", "all"}
WORK_ROOT_PHASES = MODEL_PHASES | {"b2-canary", "render", "wan"}
FIXTURE_PHASES = MODEL_BINDING_PHASES
BUDGET_PLAN_PHASES = {"anyaccomp-local", "all"}

ENV_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "anyaccomp-binding": (
        "STAGEME_PROJECT_ID",
        "STAGEME_GPU_PROVIDER",
        "STAGEME_GPU_REGION",
        "STAGEME_SPEND_CAP_USD",
    ),
    "anyaccomp-local": (
        "STAGEME_PROJECT_ID",
        "STAGEME_GPU_PROVIDER",
        "STAGEME_GPU_REGION",
        "STAGEME_SPEND_CAP_USD",
    ),
    "anyaccomp-hosted": (
        "ANYACCOMP_API_URL",
        "ANYACCOMP_API_TOKEN",
        "STAGEME_PROJECT_ID",
        "STAGEME_GPU_PROVIDER",
        "STAGEME_GPU_REGION",
        "STAGEME_SPEND_CAP_USD",
    ),
    "ace-hosted": (
        "ACESTEP_API_URL",
        "ACESTEP_API_TOKEN",
        "STAGEME_PROJECT_ID",
        "STAGEME_GPU_PROVIDER",
        "STAGEME_GPU_REGION",
        "STAGEME_SPEND_CAP_USD",
    ),
    "b2-canary": (
        "B2_KEY_ID",
        "B2_APP_KEY",
        "B2_BUCKET",
        "B2_REGION",
        "B2_PREFIX",
    ),
    "wan": ("REPLICATE_API_TOKEN", "STAGEME_SPEND_CAP_USD"),
    "all": (
        "ANYACCOMP_API_URL",
        "ANYACCOMP_API_TOKEN",
        "ACESTEP_API_URL",
        "ACESTEP_API_TOKEN",
        "B2_KEY_ID",
        "B2_APP_KEY",
        "B2_BUCKET",
        "B2_REGION",
        "B2_PREFIX",
        "REPLICATE_API_TOKEN",
        "STAGEME_PROJECT_ID",
        "STAGEME_GPU_PROVIDER",
        "STAGEME_GPU_REGION",
        "STAGEME_SPEND_CAP_USD",
    ),
}

ENV_PHASE_NOTES = {
    "ANYACCOMP_API_URL": "hosted AnyAccomp lifecycle",
    "ANYACCOMP_API_TOKEN": "hosted AnyAccomp authentication",
    "ACESTEP_API_URL": "hosted ACE-Step release/query/audio lifecycle",
    "ACESTEP_API_TOKEN": "hosted ACE-Step authentication",
    "B2_KEY_ID": "real B2 canary",
    "B2_APP_KEY": "real B2 canary",
    "B2_BUCKET": "real B2 canary",
    "B2_REGION": "real B2 canary",
    "B2_PREFIX": "exact isolated B2 canary prefix",
    "REPLICATE_API_TOKEN": "optional Wan interval",
    "STAGEME_PROJECT_ID": "exact consent/project binding",
    "STAGEME_GPU_PROVIDER": "approved model-worker provider disclosure",
    "STAGEME_GPU_REGION": "approved model-worker region disclosure",
    "STAGEME_SPEND_CAP_USD": "human-approved paid-execution cap",
}

RECOMMENDED_PYTHON_PACKAGES = {
    "numpy": "2.4.6",
    "scipy": "1.17.1",
    "soundfile": "0.14.0",
    "librosa": "0.11.0",
    "pyloudnorm": "0.2.0",
}

REQUIRED_STAGE_FILES = (
    "context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md",
    "context-engineering/09-planning/STAGEME_SPIKE_PROTOCOL.md",
    "context-engineering/09-planning/STAGEME_PRECALL_READINESS_REPORT.md",
    "context-engineering/09-planning/STAGEME_FIRST_CALL_RUNBOOK.md",
    "context-engineering/09-planning/STAGEME_F1_RECORDING_CHECKLIST.md",
)


@dataclass(frozen=True)
class Check:
    """One preflight result without any credential values."""

    check_id: str
    status: str
    summary: str
    detail: str = ""


def _run(
    command: Sequence[str], timeout: float = 8.0, cwd: Path | None = None
) -> tuple[int, str]:
    """Run a read-only command and return a single bounded output string."""

    try:
        completed = subprocess.run(
            list(command),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, type(exc).__name__
    output = (completed.stdout or completed.stderr or "").strip()
    return completed.returncode, output[:2000]


def _version_tuple(raw: str) -> tuple[int, ...]:
    match = re.search(r"(\d+)(?:\.(\d+))?(?:\.(\d+))?", raw)
    if not match:
        return ()
    return tuple(int(part) for part in match.groups(default="0"))


def _command_version(command: str, args: Sequence[str] = ("--version",)) -> str | None:
    path = shutil.which(command)
    if path is None:
        return None
    code, output = _run((path, *args))
    if code != 0:
        return None
    return output.splitlines()[0] if output else "present"


def _memory_gib() -> float | None:
    if sys.platform == "darwin":
        code, output = _run(("sysctl", "-n", "hw.memsize"))
        if code == 0 and output.isdigit():
            return int(output) / 1024**3
    meminfo = Path("/proc/meminfo")
    if meminfo.is_file():
        match = re.search(
            r"^MemTotal:\s+(\d+)\s+kB$", meminfo.read_text(), re.MULTILINE
        )
        if match:
            return int(match.group(1)) * 1024 / 1024**3
    return None


def _accelerators() -> list[str]:
    found: list[str] = []
    if shutil.which("nvidia-smi"):
        code, output = _run(
            (
                "nvidia-smi",
                "--query-gpu=name,memory.total",
                "--format=csv,noheader,nounits",
            )
        )
        if code == 0 and output:
            found.extend(f"NVIDIA {line.strip()} MiB" for line in output.splitlines())
    if shutil.which("rocminfo") or shutil.which("rocm-smi"):
        found.append("AMD ROCm tooling present")
    if sys.platform == "darwin" and shutil.which("system_profiler"):
        code, output = _run(("system_profiler", "SPDisplaysDataType"))
        if code == 0 and "Metal Support" in output:
            chipset = re.search(r"Chipset Model:\s*(.+)", output)
            found.append(
                f"Apple Metal ({chipset.group(1).strip() if chipset else 'GPU'})"
            )
    return found


def environment_checks(phase: str, environ: Mapping[str, str]) -> list[Check]:
    checks: list[Check] = []
    required = set(ENV_REQUIREMENTS.get(phase, ()))
    all_names = sorted(ENV_PHASE_NOTES)
    for name in all_names:
        present = bool(environ.get(name))
        value_is_valid = present
        invalid_reason = ""
        if name == "STAGEME_SPEND_CAP_USD" and present:
            try:
                cap = float(environ[name])
                value_is_valid = math.isfinite(cap) and cap > 0.0
            except ValueError:
                value_is_valid = False
            if not value_is_valid:
                invalid_reason = "Configured spend cap is not a finite positive number"
        elif name.endswith("_API_URL") and present:
            value_is_valid = environ[name].startswith("https://")
            if not value_is_valid:
                invalid_reason = "Configured API URL is not HTTPS"
        elif name == "B2_PREFIX" and present:
            prefix = environ[name]
            value_is_valid = bool(
                re.fullmatch(r"[A-Za-z0-9._/-]{3,512}", prefix)
                and not prefix.startswith("/")
                and ".." not in prefix.split("/")
                and prefix.endswith("/")
            )
            if not value_is_valid:
                invalid_reason = "Configured B2 prefix is not an isolated relative prefix ending in /"
        if name in required:
            status = PASS if value_is_valid else BLOCKER
            summary = (
                f"{name} is configured"
                if value_is_valid
                else (invalid_reason or f"{name} is missing")
            )
        else:
            status = (
                PASS if value_is_valid else (WARNING if present else NOT_YET_REQUIRED)
            )
            summary = (
                f"{name} is configured"
                if value_is_valid
                else (invalid_reason or f"{name} is not yet required")
            )
        checks.append(
            Check(
                f"env.{name.lower()}",
                status,
                summary,
                f"Required for {ENV_PHASE_NOTES[name]}; presence and required format were checked, but the value was not printed.",
            )
        )
    return checks


def _valid_utc_timestamp(value: object) -> bool:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def budget_plan_checks(
    phase: str,
    budget_plan_path: Path | None,
    environ: Mapping[str, str] | None = None,
) -> list[Check]:
    """Validate a secret-free provider-native hard budget plan."""

    required = phase in BUDGET_PLAN_PHASES
    if budget_plan_path is None:
        return [
            Check(
                "budget.hard-plan",
                BLOCKER if required else NOT_YET_REQUIRED,
                "Hard budget plan not supplied",
                "The first local GPU call requires a provider-native termination deadline whose worst-case compute plus reserve fits the approved cap.",
            )
        ]
    if not budget_plan_path.is_file():
        return [Check("budget.hard-plan", BLOCKER, "Hard budget plan does not exist")]
    try:
        plan = json.loads(budget_plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [
            Check("budget.hard-plan", BLOCKER, "Hard budget plan is not valid JSON")
        ]

    invalid: list[str] = []
    environment = environ or {}

    def finite_number(name: str, *, positive: bool) -> float:
        try:
            number = float(plan.get(name))
        except (TypeError, ValueError):
            invalid.append(name)
            return math.nan
        if not math.isfinite(number) or (number <= 0 if positive else number < 0):
            invalid.append(name)
        return number

    for name in (
        "project_id",
        "provider",
        "region",
        "gpu_offer_label",
        "worker_image",
        "provider_price_source_url",
    ):
        value = str(plan.get(name) or "").strip()
        if not value or "<" in value or ">" in value or "example." in value:
            invalid.append(name)
    if plan.get("schema_version") != "1":
        invalid.append("schema_version=1")
    if plan.get("owner_approved") is not True:
        invalid.append("owner_approved=true")
    if plan.get("model") != "AmphionTeam/AnyAccomp":
        invalid.append("model=AmphionTeam/AnyAccomp")
    if plan.get("model_commit") != ANYACCOMP_CODE_COMMIT:
        invalid.append(f"model_commit={ANYACCOMP_CODE_COMMIT}")
    if plan.get("checkpoint_revision") != ANYACCOMP_CHECKPOINT_REVISION:
        invalid.append(f"checkpoint_revision={ANYACCOMP_CHECKPOINT_REVISION}")
    if plan.get("hard_termination_control") != "runpodctl pod create --terminate-after":
        invalid.append(
            "hard_termination_control=runpodctl pod create --terminate-after"
        )
    if "@sha256:" not in str(plan.get("worker_image") or ""):
        invalid.append("worker_image (immutable image@sha256 digest)")
    if not str(plan.get("provider_price_source_url") or "").startswith("https://"):
        invalid.append("provider_price_source_url=https URL")
    if not _valid_utc_timestamp(plan.get("price_checked_at_utc")):
        invalid.append("price_checked_at_utc (ISO-8601 UTC timestamp)")

    rate = finite_number("gpu_rate_usd_per_hour", positive=True)
    reserve = finite_number("noncompute_reserve_usd", positive=False)
    cap = finite_number("approved_spend_cap_usd", positive=True)
    hours = plan.get("hard_terminate_after_hours")
    if not isinstance(hours, int) or not 1 <= hours <= 24:
        invalid.append("hard_terminate_after_hours (integer 1..24)")
    elif all(math.isfinite(value) for value in (rate, reserve, cap)) and (
        rate * hours + reserve > cap + 1e-9
    ):
        invalid.append("rate × hard-terminate hours + reserve exceeds approved cap")

    for env_name, field in (
        ("STAGEME_PROJECT_ID", "project_id"),
        ("STAGEME_GPU_PROVIDER", "provider"),
        ("STAGEME_GPU_REGION", "region"),
    ):
        configured = environment.get(env_name)
        if configured and plan.get(field) != configured:
            invalid.append(f"{field} does not match {env_name}")
    configured_cap = environment.get("STAGEME_SPEND_CAP_USD")
    if configured_cap:
        try:
            if float(configured_cap) != cap:
                invalid.append(
                    "approved_spend_cap_usd does not match STAGEME_SPEND_CAP_USD"
                )
        except ValueError:
            invalid.append(
                "approved_spend_cap_usd does not match STAGEME_SPEND_CAP_USD"
            )

    return [
        Check(
            "budget.hard-plan",
            PASS if not invalid else BLOCKER,
            "Provider-native hard termination fits the approved cap"
            if not invalid
            else "Hard budget plan is incomplete or exceeds the approved cap",
            "Missing/invalid field names only: " + ", ".join(invalid)
            if invalid
            else "No price, cap, provider identifier, or path was printed.",
        )
    ]


def tool_checks(phase: str, require_docker: bool = False) -> list[Check]:
    checks: list[Check] = []

    current_python = platform.python_version()
    python_ok = (3, 11) <= sys.version_info[:2] <= (3, 12)
    checks.append(
        Check(
            "tool.python",
            PASS if python_ok else (BLOCKER if phase in MODEL_PHASES else WARNING),
            f"Python {current_python}",
            "Use an isolated Python 3.11 or 3.12 environment for the current Genblaze/audio stack.",
        )
    )

    node = _command_version("node")
    node_version = _version_tuple(node or "")
    node_is_pinned_line = node_version[:1] == (22,) and node_version >= (22, 12, 0)
    if node is None:
        node_status = BLOCKER if phase in {"render", "all"} else WARNING
    elif phase in {"render", "all"}:
        node_status = PASS if node_is_pinned_line else BLOCKER
    else:
        node_status = PASS if node_is_pinned_line else WARNING
    checks.append(
        Check(
            "tool.node",
            node_status,
            node or "Node.js not found",
            "Pin Node 22.x at or above 22.12.0 for the Revideo benchmark; newer majors are not the reproducibility target.",
        )
    )

    package_managers = {
        name: _command_version(name) for name in ("pnpm", "npm", "yarn")
    }
    available_managers = [
        f"{name}: {version}" for name, version in package_managers.items() if version
    ]
    checks.append(
        Check(
            "tool.package-manager",
            PASS
            if available_managers
            else (BLOCKER if phase in {"render", "all"} else WARNING),
            "; ".join(available_managers)
            if available_managers
            else "No Node package manager found",
            "Use the package-manager version pinned by the renderer/sample lockfile.",
        )
    )

    for command in ("ffmpeg", "ffprobe"):
        version = _command_version(command, ("-version",))
        checks.append(
            Check(
                f"tool.{command}",
                PASS if version else BLOCKER,
                version or f"{command} not found",
                "Required for deterministic decode, QC, mixing, and media inspection.",
            )
        )

    docker = _command_version("docker")
    docker_code, docker_server = (
        _run(("docker", "version", "--format", "{{.Server.Version}}"), timeout=5)
        if docker
        else (127, "")
    )
    docker_required = require_docker
    if docker and docker_code == 0 and docker_server:
        docker_status = PASS
        docker_summary = f"Docker client and daemon available ({docker_server})"
    elif docker:
        docker_status = BLOCKER if docker_required else WARNING
        docker_summary = "Docker client found; daemon unavailable"
    else:
        docker_status = BLOCKER if docker_required else NOT_YET_REQUIRED
        docker_summary = "Docker not available"
    checks.append(
        Check(
            "tool.docker",
            docker_status,
            docker_summary,
            "Pass --require-docker when the selected worker or renderer path is containerized.",
        )
    )

    if phase in {"anyaccomp-local", "all"}:
        for command in ("git", "sha256sum", "timeout"):
            version = _command_version(command)
            checks.append(
                Check(
                    f"tool.worker-{command}",
                    PASS if version else BLOCKER,
                    f"{command} available" if version else f"{command} not found",
                    "Required by the fail-closed worker runbook.",
                )
            )
        env_manager = next(
            (name for name in ("conda", "mamba", "micromamba") if shutil.which(name)),
            None,
        )
        checks.append(
            Check(
                "tool.worker-environment-manager",
                PASS if env_manager else BLOCKER,
                f"{env_manager} available" if env_manager else "Conda/Mamba not found",
                "Required to create separate AnyAccomp Python 3.9 and QC Python 3.12 environments.",
            )
        )
        time_path = Path("/usr/bin/time")
        code, _ = (
            _run((str(time_path), "-v", "true")) if time_path.is_file() else (127, "")
        )
        checks.append(
            Check(
                "tool.worker-time",
                PASS if code == 0 else BLOCKER,
                "GNU-compatible /usr/bin/time -v available"
                if code == 0
                else "GNU-compatible /usr/bin/time -v unavailable",
            )
        )
    return checks


def model_python_checks(phase: str, model_python: Path | None) -> list[Check]:
    """Check the stock AnyAccomp worker interpreter independently.

    Genblaze and the StageMe control/QC environment use Python 3.11 or 3.12,
    while the commit-pinned AnyAccomp environment declares Python 3.9. Keeping
    these checks separate prevents an apparently healthy control process from
    being mistaken for a reproduced model worker.
    """

    required = phase in {"anyaccomp-local", "all"}
    if model_python is None:
        return [
            Check(
                "tool.anyaccomp-python",
                BLOCKER if required else NOT_YET_REQUIRED,
                "AnyAccomp worker Python not configured",
                "The stock worker requires an isolated Python 3.9 interpreter; pass --model-python from inside the worker/container.",
            )
        ]
    if not model_python.is_file() or not os.access(model_python, os.X_OK):
        return [
            Check(
                "tool.anyaccomp-python",
                BLOCKER,
                "Configured AnyAccomp worker Python is missing or not executable",
                "The interpreter path is intentionally not printed.",
            )
        ]
    code, output = _run((str(model_python), "--version"))
    version = _version_tuple(output)
    stock_compatible = code == 0 and version[:2] == (3, 9)
    checks = [
        Check(
            "tool.anyaccomp-python",
            PASS if stock_compatible else BLOCKER,
            f"AnyAccomp worker Python {'.'.join(map(str, version[:3])) if version else 'could not be determined'}",
            "Python 3.9 is the commit-pinned upstream reproduction target; do not install this stack into the Genblaze/FastAPI process.",
        )
    ]
    if not required or not stock_compatible:
        return checks

    smoke = (
        "import json, torch, torchaudio, torchvision; "
        "p=torch.cuda.get_device_properties(0) if torch.cuda.is_available() else None; "
        "print(json.dumps({'torch':torch.__version__.split('+')[0],"
        "'torchaudio':torchaudio.__version__.split('+')[0],"
        "'torchvision':torchvision.__version__.split('+')[0],"
        "'cuda_build':torch.version.cuda,'cuda_available':torch.cuda.is_available(),"
        "'bf16':torch.cuda.is_bf16_supported() if torch.cuda.is_available() else False,"
        "'capability':list(torch.cuda.get_device_capability(0)) if p else None,"
        "'vram':p.total_memory if p else 0}))"
    )
    smoke_code, smoke_output = _run((str(model_python), "-c", smoke), timeout=30)
    try:
        inventory = json.loads(smoke_output) if smoke_code == 0 else {}
        capability = tuple(int(v) for v in (inventory.get("capability") or ()))
        vram = int(inventory.get("vram", 0))
        stack_ok = (
            inventory.get("torch") == "2.3.1"
            and inventory.get("torchaudio") == "2.3.1"
            and inventory.get("torchvision") == "0.18.1"
            and str(inventory.get("cuda_build", "")).startswith("12.1")
            and inventory.get("cuda_available") is True
            and inventory.get("bf16") is True
            and capability >= MIN_ANYACCOMP_COMPUTE_CAPABILITY
            and vram >= MIN_ANYACCOMP_VRAM_MIB * 1024**2
        )
    except (TypeError, ValueError, json.JSONDecodeError):
        stack_ok = False
    checks.append(
        Check(
            "tool.anyaccomp-cuda-smoke",
            PASS if stack_ok else BLOCKER,
            "Pinned Torch/CUDA imports and 24 GiB Ampere-or-newer gate pass"
            if stack_ok
            else "Pinned Torch/CUDA compatibility smoke failed",
            "Requires Torch/Torchaudio 2.3.1, Torchvision 0.18.1, CUDA 12.1 build, CUDA+bfloat16 availability, compute capability >=8.0, and >=24 GiB VRAM.",
        )
    )
    return checks


def capacity_checks(
    phase: str, root: Path, min_disk_gib: float, min_ram_gib: float
) -> list[Check]:
    disk_root = root
    while not disk_root.exists() and disk_root.parent != disk_root:
        disk_root = disk_root.parent
    free_gib = shutil.disk_usage(disk_root).free / 1024**3
    disk_ok = free_gib >= min_disk_gib
    disk_status = PASS if disk_ok else (BLOCKER if phase in MODEL_PHASES else WARNING)
    checks = [
        Check(
            "capacity.disk",
            disk_status,
            f"{free_gib:.1f} GiB free",
            f"Preflight threshold: {min_disk_gib:.1f} GiB; checkpoint downloads remain approval-gated.",
        )
    ]

    ram_gib = _memory_gib()
    if ram_gib is None:
        ram_status = WARNING
        ram_summary = "RAM could not be determined"
    else:
        ram_status = (
            PASS
            if ram_gib >= min_ram_gib
            else (BLOCKER if phase in MODEL_PHASES else WARNING)
        )
        ram_summary = f"{ram_gib:.1f} GiB RAM"
    checks.append(
        Check(
            "capacity.ram",
            ram_status,
            ram_summary,
            f"Preflight threshold: {min_ram_gib:.1f} GiB; real peak RAM must be measured on the worker.",
        )
    )

    accelerators = _accelerators()
    nvidia_memory_mib = [
        int(match.group(1))
        for item in accelerators
        if item.startswith("NVIDIA")
        and (match := re.search(r"(\d+) MiB$", item)) is not None
    ]
    has_suitable_nvidia = any(
        memory >= MIN_ANYACCOMP_VRAM_MIB for memory in nvidia_memory_mib
    )
    if phase in LOCAL_GPU_PHASES:
        accel_status = PASS if has_suitable_nvidia else BLOCKER
        detail = "This gate requires at least 24 GiB NVIDIA VRAM. Compute capability, bfloat16, and CUDA are separately verified through the pinned model interpreter."
    elif accelerators:
        accel_status = PASS
        detail = "Detected hardware is inventory only; it does not prove model compatibility or speed."
    else:
        accel_status = NOT_YET_REQUIRED
        detail = "GPU access becomes required at the first local model call."
    checks.append(
        Check(
            "capacity.accelerator",
            accel_status,
            "; ".join(accelerators)
            if accelerators
            else "No accelerator tooling detected",
            detail,
        )
    )
    return checks


def package_checks(phase: str) -> list[Check]:
    checks: list[Check] = []
    for package, expected in RECOMMENDED_PYTHON_PACKAGES.items():
        try:
            installed = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            installed = None
        if installed == expected:
            status = PASS
            summary = f"{package} {installed}"
        elif installed:
            status = BLOCKER if phase in MODEL_PHASES else WARNING
            summary = f"{package} {installed}; readiness pin is {expected}"
        else:
            status = BLOCKER if phase in MODEL_PHASES else NOT_YET_REQUIRED
            summary = f"{package} not installed; readiness pin is {expected}"
        checks.append(
            Check(
                f"package.{package}",
                status,
                summary,
                "Install in an isolated StageMe environment; do not mutate the system Python.",
            )
        )
    return checks


def directory_checks(
    phase: str,
    repo_root: Path,
    work_root: Path | None,
    checkpoint_root: Path | None,
    anyaccomp_root: Path | None,
) -> list[Check]:
    checks: list[Check] = []
    for rel in REQUIRED_STAGE_FILES:
        exists = (repo_root / rel).is_file()
        checks.append(
            Check(
                f"repository.{Path(rel).name.lower()}",
                PASS if exists else BLOCKER,
                f"{Path(rel).name} {'present' if exists else 'missing'}",
            )
        )

    for clone_name in ("AnyAccomp", "ACE-Step-1.5"):
        exists = (repo_root / ".research-clones" / clone_name / ".git").exists()
        checks.append(
            Check(
                f"repository.clone.{clone_name.lower()}",
                PASS if exists else WARNING,
                f"{clone_name} research clone {'present' if exists else 'missing'}",
                "Informational research clone only; executable worker source is checked separately.",
            )
        )

    source_required = phase in {"anyaccomp-local", "all"}
    if anyaccomp_root is None:
        checks.append(
            Check(
                "repository.anyaccomp-worker-source",
                BLOCKER if source_required else NOT_YET_REQUIRED,
                "AnyAccomp worker source root not configured",
                "Pass --anyaccomp-root for the actual executable clone; ignored research clones are not accepted as an implicit substitute.",
            )
        )
    else:
        required_files = (
            "infer_from_folder.py",
            "requirements.txt",
            "config/flow_matching.json",
            "config/vocoder.json",
        )
        code, commit = _run(("git", "-C", str(anyaccomp_root), "rev-parse", "HEAD"))
        diff_code, _ = _run(
            ("git", "-C", str(anyaccomp_root), "diff", "--quiet", "HEAD", "--")
        )
        files_ok = all((anyaccomp_root / rel).is_file() for rel in required_files)
        source_ok = (
            code == 0
            and commit == ANYACCOMP_CODE_COMMIT
            and diff_code == 0
            and files_ok
        )
        checks.append(
            Check(
                "repository.anyaccomp-worker-source",
                PASS if source_ok else BLOCKER,
                "AnyAccomp worker source matches the pinned commit and layout"
                if source_ok
                else "AnyAccomp worker source does not match the pinned commit/layout",
                "The source path is intentionally not printed.",
            )
        )

    if work_root is None:
        status = BLOCKER if phase in WORK_ROOT_PHASES else NOT_YET_REQUIRED
        checks.append(
            Check("directory.work-root", status, "StageMe work root not configured")
        )
    else:
        writable = work_root.is_dir() and os.access(work_root, os.W_OK)
        checks.append(
            Check(
                "directory.work-root",
                PASS if writable else BLOCKER,
                "StageMe work root is writable"
                if writable
                else "StageMe work root is missing or not writable",
                "The path is intentionally not printed; keep fixtures and outputs outside Git.",
            )
        )
        if phase in MODEL_PHASES:
            expected = (
                "src",
                "fixture",
                "input",
                "environment",
                "run",
                "output",
                "qc",
                "review",
                "transfer",
            )
            missing_dirs = [
                name for name in expected if not (work_root / name).is_dir()
            ]
            checks.append(
                Check(
                    "directory.evidence-layout",
                    PASS if not missing_dirs else BLOCKER,
                    "StageMe worker/evidence directory layout is complete"
                    if not missing_dirs
                    else "StageMe worker/evidence directory layout is incomplete",
                    "Missing directory names: " + ", ".join(missing_dirs)
                    if missing_dirs
                    else "Paths are intentionally not printed.",
                )
            )

    if checkpoint_root is None:
        status = BLOCKER if source_required else NOT_YET_REQUIRED
        checks.append(
            Check("directory.checkpoints", status, "Checkpoint root not configured")
        )
    else:
        failures: list[str] = []
        if not checkpoint_root.is_dir():
            failures.append("checkpoint root missing")
        else:
            for rel, (expected_size, expected_hash) in ANYACCOMP_CHECKPOINTS.items():
                path = checkpoint_root / rel
                if not path.is_file():
                    failures.append(f"missing {rel}")
                elif path.stat().st_size != expected_size:
                    failures.append(f"size mismatch for {rel}")
                elif _sha256(path) != expected_hash:
                    failures.append(f"hash mismatch for {rel}")
        usable = not failures
        checks.append(
            Check(
                "directory.checkpoints",
                PASS if usable else BLOCKER,
                "All three AnyAccomp checkpoints match pinned size and SHA-256"
                if usable
                else "AnyAccomp checkpoint integrity gate failed",
                "Failures: " + "; ".join(failures)
                if failures
                else f"Checkpoint revision contract: {ANYACCOMP_CHECKPOINT_REVISION}.",
            )
        )
    return checks


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _decoded_audio_qc(path: Path) -> tuple[dict[str, float | int] | None, str | None]:
    """Decode a short local fixture to mono float and calculate fail-closed QC."""

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        return None, "ffmpeg unavailable for audio QC"
    try:
        completed = subprocess.run(
            (
                ffmpeg,
                "-nostdin",
                "-v",
                "error",
                "-i",
                str(path),
                "-map",
                "0:a:0",
                "-ac",
                "1",
                "-ar",
                "24000",
                "-f",
                "f32le",
                "pipe:1",
            ),
            check=False,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, f"audio QC decode failed ({type(exc).__name__})"
    if completed.returncode != 0 or not completed.stdout:
        return None, "audio QC decode failed"
    samples = array.array("f")
    try:
        samples.frombytes(completed.stdout)
    except ValueError:
        return None, "decoded audio byte count is invalid"
    if sys.byteorder != "little":
        samples.byteswap()
    if not samples or any(not math.isfinite(value) for value in samples):
        return None, "decoded audio is empty or contains non-finite samples"
    count = len(samples)
    peak = max(abs(value) for value in samples)
    rms = math.sqrt(math.fsum(value * value for value in samples) / count)
    dc_offset = math.fsum(samples) / count
    clipped_samples = sum(1 for value in samples if abs(value) >= 0.999)
    return (
        {
            "peak": peak,
            "rms": rms,
            "dc_offset": dc_offset,
            "clipped_samples": clipped_samples,
            "sample_count": count,
        },
        None,
    )


def fixture_checks(phase: str, fixture: Path | None) -> list[Check]:
    required = phase in FIXTURE_PHASES
    if fixture is None:
        return [
            Check(
                "fixture.authorized-audio",
                BLOCKER if required else NOT_YET_REQUIRED,
                "Authorized fixture not supplied",
                "Required only at the first real audio-model call; never commit it to Git.",
            )
        ]
    if not fixture.is_file():
        return [
            Check("fixture.authorized-audio", BLOCKER, "Fixture file does not exist")
        ]
    accepted_suffixes = {
        ".wav",
        ".flac",
        ".mp3",
        ".m4a",
        ".webm",
        ".ogg",
        ".opus",
    }
    if fixture.suffix.lower() not in accepted_suffixes:
        return [
            Check("fixture.authorized-audio", BLOCKER, "Fixture format is not accepted")
        ]
    if fixture.stat().st_size > 25 * 1024 * 1024:
        return [
            Check(
                "fixture.authorized-audio",
                BLOCKER,
                "Fixture exceeds the 25 MiB preflight cap",
            )
        ]
    ffprobe = shutil.which("ffprobe")
    if ffprobe is None:
        return [
            Check(
                "fixture.authorized-audio",
                BLOCKER,
                "ffprobe unavailable for fixture validation",
            )
        ]
    code, output = _run(
        (
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,sample_fmt,channels,sample_rate",
            "-of",
            "json",
            str(fixture),
        )
    )
    if code != 0:
        return [Check("fixture.authorized-audio", BLOCKER, "Fixture is not decodable")]
    try:
        probe = json.loads(output)
        duration = float(probe.get("format", {}).get("duration", 0))
        audio_streams = [
            s for s in probe.get("streams", []) if s.get("codec_type") == "audio"
        ]
    except (ValueError, TypeError, json.JSONDecodeError):
        return [
            Check(
                "fixture.authorized-audio",
                BLOCKER,
                "Fixture metadata could not be parsed",
            )
        ]
    if not audio_streams:
        return [
            Check("fixture.authorized-audio", BLOCKER, "Fixture has no audio stream")
        ]
    if not 8.0 <= duration <= 15.0:
        return [
            Check(
                "fixture.authorized-audio",
                BLOCKER,
                f"Fixture duration {duration:.3f}s is outside 8–15s",
            )
        ]
    stream = audio_streams[0]
    canonical_required = phase in MODEL_BINDING_PHASES
    canonical_ok = (
        fixture.suffix.lower() == ".wav"
        and stream.get("codec_name") == "pcm_f32le"
        and stream.get("sample_fmt") == "flt"
        and str(stream.get("sample_rate")) == "24000"
        and str(stream.get("channels")) == "1"
    )
    if canonical_required and not canonical_ok:
        return [
            Check(
                "fixture.authorized-audio",
                BLOCKER,
                "Worker fixture is not canonical 24 kHz mono float32 WAV",
                "Normalize locally with the recorded FFmpeg/libsoxr command before any upload or model call.",
            )
        ]

    metrics, qc_error = _decoded_audio_qc(fixture)
    if qc_error or metrics is None:
        return [
            Check("fixture.authorized-audio", BLOCKER, qc_error or "Audio QC failed")
        ]
    clipped_limit = max(3, int(int(metrics["sample_count"]) * 0.0001))
    qc_failures: list[str] = []
    if float(metrics["rms"]) < 1e-4:
        qc_failures.append("effectively silent (RMS below 1e-4 full scale)")
    if int(metrics["clipped_samples"]) >= clipped_limit:
        qc_failures.append("repeated near-full-scale samples indicate clipping")
    if abs(float(metrics["dc_offset"])) > 0.005:
        qc_failures.append("absolute DC offset exceeds 0.005 full scale")
    if qc_failures:
        return [
            Check(
                "fixture.authorized-audio",
                BLOCKER,
                "Fixture fails deterministic audio QC",
                "Failures: " + "; ".join(qc_failures),
            )
        ]
    return [
        Check(
            "fixture.authorized-audio",
            PASS,
            f"Fixture passes format/duration/QC gates ({duration:.3f}s, SHA-256 {_sha256(fixture)})",
            "QC checks decodability, silence, repeated clipping, and material DC offset; musical suitability still requires human review.",
        )
    ]


def consent_checks(
    phase: str,
    consent_path: Path | None,
    fixture: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> list[Check]:
    """Bind approval to exact project, media, model, provider, and retention."""

    required = phase in FIXTURE_PHASES
    if consent_path is None:
        return [
            Check(
                "fixture.consent",
                BLOCKER if required else NOT_YET_REQUIRED,
                "Accepted consent record not supplied",
                "Use a copied StageMe consent template outside Git after exact-file hash, provider/region, and retention disclosure.",
            )
        ]
    if not consent_path.is_file():
        return [Check("fixture.consent", BLOCKER, "Consent record does not exist")]
    try:
        consent = json.loads(consent_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [Check("fixture.consent", BLOCKER, "Consent record is not valid JSON")]

    invalid: list[str] = []
    environment = environ or {}

    def require_true(path: str, value: object) -> None:
        if value is not True:
            invalid.append(path)

    def require_false(path: str, value: object) -> None:
        if value is not False:
            invalid.append(f"{path}=false")

    def valid_hash(field: str) -> str:
        value = str(consent.get(field, ""))
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            invalid.append(f"{field} (64 lowercase hexadecimal characters)")
        return value

    def require_concrete(path: str, value: object) -> str:
        rendered = str(value or "").strip()
        lowered = rendered.lower()
        if (
            not rendered
            or "<" in rendered
            or ">" in rendered
            or "example." in lowered
            or lowered in {"test", "unknown", "tbd", "todo", "placeholder", "none"}
        ):
            invalid.append(path)
        return rendered

    try:
        attestation = consent["performer_attestation"]
        purposes = consent["allowed_purposes"]
        processing = consent["processing"]
        retention = consent["retention"]
        canonicalization = consent["canonicalization"]
        if consent.get("schema_version") != "1":
            invalid.append("schema_version=1")
        if consent.get("policy_version") != "stageme-f1-2026-07-27":
            invalid.append("policy_version=stageme-f1-2026-07-27")
        for name in (
            "owns_or_is_authorized_to_use_recording",
            "recording_contains_only_authorized_voice",
            "recording_contains_no_copyrighted_backing_media",
        ):
            require_true(f"performer_attestation.{name}", attestation[name])
        require_false(
            "performer_attestation.third_party_or_celebrity_imitation_requested",
            attestation["third_party_or_celebrity_imitation_requested"],
        )
        for name in (
            "local_media_analysis",
            "accompaniment_generation",
            "deterministic_mix_and_qc",
            "private_human_review",
            "temporary_gpu_host_processing",
        ):
            require_true(f"allowed_purposes.{name}", purposes[name])
        require_false("allowed_purposes.training_reuse", purposes["training_reuse"])
        require_true("accepted", consent["accepted"])
        for name in ("fixture_id", "project_id"):
            require_concrete(name, consent.get(name))
        if not _valid_utc_timestamp(consent.get("accepted_at_utc")):
            invalid.append("accepted_at_utc (ISO-8601 UTC timestamp)")
        for name in (
            "gpu_host_or_provider",
            "model",
            "model_commit",
            "checkpoint_revision",
            "processing_region",
            "approved_spend_cap_usd",
            "provider_terms_url",
        ):
            require_concrete(f"processing.{name}", processing.get(name))
        require_true(
            "processing.provider_retention_disclosed",
            processing["provider_retention_disclosed"],
        )
        if not str(processing.get("provider_terms_url", "")).startswith("https://"):
            invalid.append("processing.provider_terms_url=https URL")
        try:
            approved_cap = float(processing.get("approved_spend_cap_usd"))
            if not math.isfinite(approved_cap) or approved_cap <= 0.0:
                invalid.append("processing.approved_spend_cap_usd (finite positive)")
        except (TypeError, ValueError):
            invalid.append("processing.approved_spend_cap_usd (finite positive)")
        worker_hours = retention["temporary_worker_max_hours"]
        bundle_days = retention["user_controlled_bundle_max_days"]
        if not isinstance(worker_hours, int) or not 1 <= worker_hours <= 24:
            invalid.append("retention.temporary_worker_max_hours (1..24)")
        if not isinstance(bundle_days, int) or not 0 <= bundle_days <= 7:
            invalid.append("retention.user_controlled_bundle_max_days (0..7)")
        require_true(
            "retention.delete_worker_copy_after_verified_download",
            retention["delete_worker_copy_after_verified_download"],
        )
        require_true(
            "retention.delete_voice_bearing_derivatives_with_source",
            retention["delete_voice_bearing_derivatives_with_source"],
        )
        require_concrete(
            "retention.deletion_contact_or_command",
            retention.get("deletion_contact_or_command"),
        )
        expected_canonicalization = {
            "operation": "decode-downmix-resample-only",
            "sample_rate_hz": 24000,
            "channels": 1,
            "sample_format": "pcm_f32le",
        }
        for name, expected in expected_canonicalization.items():
            if canonicalization.get(name) != expected:
                invalid.append(f"canonicalization.{name}={expected}")
        if phase in MODEL_BINDING_PHASES:
            for name in ("ffmpeg_version", "command"):
                if not canonicalization.get(name):
                    invalid.append(f"canonicalization.{name}")
            binary_hash = str(canonicalization.get("ffmpeg_binary_sha256", ""))
            if not re.fullmatch(r"[0-9a-f]{64}", binary_hash):
                invalid.append(
                    "canonicalization.ffmpeg_binary_sha256 (64 lowercase hexadecimal characters)"
                )
    except (KeyError, TypeError):
        return [
            Check(
                "fixture.consent",
                BLOCKER,
                "Consent record is missing required sections",
            )
        ]

    original_hash = valid_hash("source_original_sha256")
    canonical_hash = str(consent.get("source_canonical_sha256") or "")
    if phase in MODEL_BINDING_PHASES:
        canonical_hash = valid_hash("source_canonical_sha256")
    elif canonical_hash and not re.fullmatch(r"[0-9a-f]{64}", canonical_hash):
        invalid.append(
            "source_canonical_sha256 (64 lowercase hexadecimal characters when present)"
        )
    expected_hash = canonical_hash if phase in MODEL_BINDING_PHASES else original_hash
    if fixture and fixture.is_file() and expected_hash != _sha256(fixture):
        invalid.append(
            "source_canonical_sha256 does not match fixture"
            if phase in MODEL_BINDING_PHASES
            else "source_original_sha256 does not match fixture"
        )

    if phase in {
        "anyaccomp-binding",
        "anyaccomp-local",
        "anyaccomp-hosted",
        "all",
    }:
        if processing.get("model") != "AmphionTeam/AnyAccomp":
            invalid.append("processing.model=AmphionTeam/AnyAccomp")
        if processing.get("model_commit") != ANYACCOMP_CODE_COMMIT:
            invalid.append(f"processing.model_commit={ANYACCOMP_CODE_COMMIT}")
        if processing.get("checkpoint_revision") != ANYACCOMP_CHECKPOINT_REVISION:
            invalid.append(
                f"processing.checkpoint_revision={ANYACCOMP_CHECKPOINT_REVISION}"
            )
    elif phase == "ace-hosted":
        if processing.get("model") != ACESTEP_MODEL_ID:
            invalid.append(f"processing.model={ACESTEP_MODEL_ID}")
        if processing.get("model_commit") != ACESTEP_CODE_COMMIT:
            invalid.append(f"processing.model_commit={ACESTEP_CODE_COMMIT}")
        if processing.get("checkpoint_revision") != ACESTEP_CHECKPOINT_REVISION:
            invalid.append(
                f"processing.checkpoint_revision={ACESTEP_CHECKPOINT_REVISION}"
            )

    for env_name, field in (
        ("STAGEME_PROJECT_ID", "project_id"),
        ("STAGEME_GPU_PROVIDER", "gpu_host_or_provider"),
        ("STAGEME_GPU_REGION", "processing_region"),
    ):
        configured = environment.get(env_name)
        actual = consent.get(field) if field == "project_id" else processing.get(field)
        if phase in MODEL_BINDING_PHASES and configured and actual != configured:
            invalid.append(f"{field} does not match {env_name}")
    configured_cap = environment.get("STAGEME_SPEND_CAP_USD")
    if phase in MODEL_BINDING_PHASES and configured_cap:
        try:
            if float(processing.get("approved_spend_cap_usd")) != float(configured_cap):
                invalid.append(
                    "processing.approved_spend_cap_usd does not match STAGEME_SPEND_CAP_USD"
                )
        except (TypeError, ValueError):
            invalid.append(
                "processing.approved_spend_cap_usd does not match STAGEME_SPEND_CAP_USD"
            )

    status = PASS if not invalid else BLOCKER
    return [
        Check(
            "fixture.consent",
            status,
            "Consent binds exact project, media, model, provider, region, and retention"
            if status == PASS
            else "Consent binding is incomplete or inconsistent",
            "Missing/invalid field names only: " + ", ".join(invalid)
            if invalid
            else "No consent value or path was printed.",
        )
    ]


def overall_status(checks: Sequence[Check]) -> str:
    if any(check.status == BLOCKER for check in checks):
        return BLOCKER
    if any(check.status == WARNING for check in checks):
        return WARNING
    return PASS


def build_report(args: argparse.Namespace) -> dict[str, object]:
    repo_root = args.repo_root.resolve()
    work_root = args.work_root.resolve() if args.work_root else None
    checkpoint_root = args.checkpoint_root.resolve() if args.checkpoint_root else None
    anyaccomp_root = args.anyaccomp_root.resolve() if args.anyaccomp_root else None
    fixture = args.fixture.resolve() if args.fixture else None
    consent = args.consent.resolve() if args.consent else None
    budget_plan = args.budget_plan.resolve() if args.budget_plan else None
    checks = [
        *tool_checks(args.phase, args.require_docker),
        *model_python_checks(args.phase, args.model_python),
        *capacity_checks(
            args.phase,
            checkpoint_root or work_root or repo_root,
            args.min_disk_gib,
            args.min_ram_gib,
        ),
        *package_checks(args.phase),
        *directory_checks(
            args.phase, repo_root, work_root, checkpoint_root, anyaccomp_root
        ),
        *fixture_checks(args.phase, fixture),
        *consent_checks(args.phase, consent, fixture, os.environ),
        *budget_plan_checks(args.phase, budget_plan, os.environ),
        *environment_checks(args.phase, os.environ),
    ]
    return {
        "schema_version": "1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": args.phase,
        "overall": overall_status(checks),
        "checks": [asdict(check) for check in checks],
        "safety": {
            "provider_calls_made": False,
            "b2_calls_made": False,
            "secret_values_printed": False,
            "media_uploaded": False,
        },
    }


def _print_human(report: Mapping[str, object]) -> None:
    print(f"StageMe preflight: {str(report['overall']).upper()} ({report['phase']})")
    for item in report["checks"]:  # type: ignore[index]
        check = item  # type: ignore[assignment]
        print(f"[{check['status']}] {check['check_id']}: {check['summary']}")
        if check.get("detail"):
            print(f"  {check['detail']}")
    print("No provider/B2 call was made and no secret value was printed.")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    repo_default = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=PHASES, default="precall")
    parser.add_argument("--json", action="store_true", dest="json_output")
    parser.add_argument("--repo-root", type=Path, default=repo_default)
    parser.add_argument("--work-root", type=Path)
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--consent", type=Path)
    parser.add_argument(
        "--budget-plan",
        type=Path,
        help="Secret-free provider pricing and provider-native hard-termination record",
    )
    parser.add_argument("--checkpoint-root", type=Path)
    parser.add_argument(
        "--anyaccomp-root",
        type=Path,
        help="Actual executable AnyAccomp worker clone (validated against the pinned commit)",
    )
    parser.add_argument(
        "--require-docker",
        action="store_true",
        help="Promote a missing/unavailable Docker daemon to a blocker",
    )
    parser.add_argument(
        "--model-python",
        type=Path,
        help="Python executable inside the isolated stock AnyAccomp worker/container",
    )
    parser.add_argument("--min-disk-gib", type=float, default=30.0)
    parser.add_argument("--min-ram-gib", type=float, default=16.0)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(args)
    if args.json_output:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        _print_human(report)
    return 2 if report["overall"] == BLOCKER else 0


if __name__ == "__main__":
    raise SystemExit(main())
