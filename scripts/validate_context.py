#!/usr/bin/env python3
"""Validate Black Blaze context integrity without network access."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    ".git",
    ".research-clones",
    ".research-venv",
    ".tmp",
    ".cache",
    ".agents",
    ".claude",
    "node_modules",
}

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[opsu]_[A-Za-z0-9]{30,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Replicate token": re.compile(r"\br8_[A-Za-z0-9]{20,}\b"),
    "Hugging Face token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "AWS-style access key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
}

REQUIRED = [
    "AGENTS.md",
    "README.md",
    "context-engineering/00-start-here/STAGEME_START_HERE.md",
    "context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md",
    "context-engineering/09-planning/STAGEME_SPIKE_PROTOCOL.md",
    "context-engineering/09-planning/STAGEME_PRECALL_READINESS_REPORT.md",
    "context-engineering/09-planning/STAGEME_FIRST_CALL_RUNBOOK.md",
    "context-engineering/09-planning/STAGEME_F1_RECORDING_CHECKLIST.md",
    "context-engineering/06-technical/STAGEME_SYSTEM_DESIGN.md",
    "context-engineering/08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md",
    "context-engineering/09-planning/STAGEME_AGENT_BUILD_HANDOFF.md",
    "context-engineering/09-planning/DECISION_LOG.md",
    "context-engineering/10-sources/SOURCE_LEDGER.md",
    "context-engineering/10-sources/VERIFICATION.md",
    "context-engineering/10-sources/repositories.json",
    "scripts/stageme_preflight.py",
    "scripts/stageme_null_test.py",
    "tests/test_stageme_preflight.py",
    "tests/test_stageme_null_test.py",
    ".env.example",
    "templates/STAGEME_CONSENT.example.json",
]

ACTIVE_STATUS_FILES = [
    "README.md",
    "AGENTS.md",
    "context-engineering/00-start-here/EXECUTIVE_BRIEF.md",
    "context-engineering/00-start-here/CONTEXT_MAP.md",
    "context-engineering/00-start-here/STAGEME_START_HERE.md",
    "context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md",
    "context-engineering/09-planning/STAGEME_SPIKE_PROTOCOL.md",
    "context-engineering/06-technical/STAGEME_SYSTEM_DESIGN.md",
    "context-engineering/08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md",
    "context-engineering/09-planning/STAGEME_AGENT_BUILD_HANDOFF.md",
    "context-engineering/09-planning/STAGEME_PRECALL_READINESS_REPORT.md",
    "context-engineering/09-planning/OPEN_QUESTIONS.md",
]

STALE_PATTERNS = [
    re.compile(r"StageMe remains a hypothesis", re.IGNORECASE),
    re.compile(r"No build is selected", re.IGNORECASE),
    re.compile(r"StageMe[^\n]{0,80}not (?:yet )?selected", re.IGNORECASE),
    re.compile(r"ReachPack\s*/\s*AccessSpec is the leading", re.IGNORECASE),
    re.compile(r"No product is selected", re.IGNORECASE),
    re.compile(r"StageMe is the leading hypothesis", re.IGNORECASE),
]

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


def is_excluded(path: Path) -> bool:
    """Return whether a repository-relative path sits under an ignored audit directory."""
    return bool(EXCLUDED_DIRS.intersection(path.relative_to(ROOT).parts))


def validate_required(errors: list[str]) -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")


def validate_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if is_excluded(path):
            continue
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(
                    f"local link escapes repository: {path.relative_to(ROOT)} -> {raw}"
                )
                continue
            if not resolved.exists():
                errors.append(f"broken local link: {path.relative_to(ROOT)} -> {raw}")


def validate_json(errors: list[str]) -> None:
    for path in ROOT.rglob("*.json"):
        if is_excluded(path):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - validator should report all parse errors
            errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")

    ledger_path = ROOT / "context-engineering/10-sources/repositories.json"
    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError):
        return
    if not isinstance(ledger, list):
        errors.append("repositories.json must contain a JSON array")
        return

    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(ledger):
        label = f"repositories.json[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} is not an object")
            continue
        owner = item.get("owner")
        repo = item.get("repo")
        commit = item.get("commit")
        key = (str(owner).lower(), str(repo).lower())
        if key in seen:
            errors.append(f"duplicate repository entry: {owner}/{repo}")
        seen.add(key)
        if not owner or not repo:
            errors.append(f"{label} missing owner/repo")
        if not isinstance(commit, str) or not HEX40_RE.fullmatch(commit):
            errors.append(f"{label} has malformed commit: {commit!r}")
        for field in ("artifact_revision", "model_card_revision"):
            revision = item.get(field)
            if revision is not None and (
                not isinstance(revision, str) or not HEX40_RE.fullmatch(revision)
            ):
                errors.append(f"{label} has malformed {field}: {revision!r}")
        artifact_sha256 = item.get("artifact_sha256")
        if artifact_sha256 is not None and (
            not isinstance(artifact_sha256, str)
            or not HEX64_RE.fullmatch(artifact_sha256)
        ):
            errors.append(f"{label} has malformed artifact_sha256: {artifact_sha256!r}")
        if not item.get("license"):
            errors.append(f"{label} missing explicit license status")
        if not item.get("purpose"):
            errors.append(f"{label} missing research purpose")
        if not item.get("inspected_at"):
            errors.append(f"{label} missing inspected_at")

    ledger_by_repo = {
        (str(item.get("owner", "")).lower(), str(item.get("repo", "")).lower()): item
        for item in ledger
        if isinstance(item, dict)
    }
    references_path = (
        ROOT / "context-engineering/08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md"
    )
    if references_path.is_file():
        for block in re.split(
            r"(?m)^### ", references_path.read_text(encoding="utf-8")
        ):
            pin = re.search(r"(?m)^- Pin: `([0-9a-f]{40})`", block)
            repo = re.search(r"https://github\.com/([^/\s)]+)/([^/\s)#]+)", block)
            if not pin or not repo:
                continue
            key = (repo.group(1).lower(), repo.group(2).rstrip(".,>").lower())
            entry = ledger_by_repo.get(key)
            if entry is None:
                errors.append(
                    f"pinned StageMe reference missing from repositories.json: {key[0]}/{key[1]}"
                )
            elif entry.get("commit") != pin.group(1):
                errors.append(
                    f"pinned StageMe reference commit mismatch: {key[0]}/{key[1]}"
                )

    facts_path = ROOT / "context-engineering/10-sources/facts.json"
    try:
        facts = json.loads(facts_path.read_text(encoding="utf-8"))
        stageme = facts["stageme_pre_call"]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError):
        return
    if not isinstance(stageme, dict):
        errors.append("facts.json stageme_pre_call must be an object")
        return

    def compare_model_contract(
        fact_section: str,
        repo_key: tuple[str, str],
        field_map: dict[str, str],
    ) -> None:
        model = stageme.get(fact_section)
        entry = ledger_by_repo.get(repo_key)
        if not isinstance(model, dict):
            errors.append(
                f"facts.json stageme_pre_call.{fact_section} must be an object"
            )
            return
        if entry is None:
            errors.append(
                "StageMe model missing from repositories.json: "
                f"{repo_key[0]}/{repo_key[1]}"
            )
            return
        expected_repository = f"{entry.get('owner')}/{entry.get('repo')}"
        if model.get("repository") != expected_repository:
            errors.append(
                f"StageMe {fact_section}.repository does not match repositories.json"
            )
        for fact_field, ledger_field in field_map.items():
            if model.get(fact_field) != entry.get(ledger_field):
                errors.append(
                    "StageMe source pin mismatch: "
                    f"{fact_section}.{fact_field} != repositories.json {ledger_field}"
                )

    compare_model_contract(
        "first_model",
        ("amphionteam", "anyaccomp"),
        {
            "code_commit": "commit",
            "checkpoint_revision": "artifact_revision",
        },
    )
    compare_model_contract(
        "second_model",
        ("ace-step", "ace-step-1.5"),
        {
            "code_commit": "commit",
            "model_card_repository": "model_card_repository",
            "model_card_revision": "model_card_revision",
            "base_model_repository": "artifact_repository",
            "base_model_revision": "artifact_revision",
            "base_model_sha256": "artifact_sha256",
            "base_model_weight_bytes": "base_model_weight_bytes",
            "main_snapshot_bytes": "main_snapshot_bytes",
            "base_snapshot_bytes": "base_snapshot_bytes",
            "major_weight_bytes": "major_weight_bytes",
            "full_snapshot_download_bytes": "full_snapshot_download_bytes",
        },
    )
    compare_model_contract(
        "renderer",
        ("midrender", "revideo"),
        {"code_commit": "commit"},
    )

    ace_entry = ledger_by_repo.get(("ace-step", "ace-step-1.5"))
    if ace_entry is not None:
        required_ace_fields = (
            "model_card_repository",
            "model_card_revision",
            "artifact_repository",
            "artifact_revision",
            "artifact_sha256",
            "base_model_weight_bytes",
            "main_snapshot_bytes",
            "base_snapshot_bytes",
            "major_weight_bytes",
            "full_snapshot_download_bytes",
            "artifact_inspected_at",
        )
        for field in required_ace_fields:
            if ace_entry.get(field) in (None, ""):
                errors.append(f"ACE-Step ledger entry missing {field}")
        for field in (
            "base_model_weight_bytes",
            "main_snapshot_bytes",
            "base_snapshot_bytes",
            "major_weight_bytes",
            "full_snapshot_download_bytes",
        ):
            value = ace_entry.get(field)
            if not isinstance(value, int) or value <= 0:
                errors.append(f"ACE-Step ledger entry has invalid {field}: {value!r}")

        doc_values = {
            "main snapshot revision": ace_entry.get("model_card_revision"),
            "base snapshot revision": ace_entry.get("artifact_revision"),
            "base artifact SHA-256": ace_entry.get("artifact_sha256"),
            "major-weight byte total": (
                f"{ace_entry['major_weight_bytes']:,}"
                if isinstance(ace_entry.get("major_weight_bytes"), int)
                else None
            ),
            "full-snapshot byte total": (
                f"{ace_entry['full_snapshot_download_bytes']:,}"
                if isinstance(ace_entry.get("full_snapshot_download_bytes"), int)
                else None
            ),
        }
        for rel in (
            "context-engineering/10-sources/SOURCE_LEDGER.md",
            "context-engineering/06-technical/REPOSITORY_AUDITS.md",
            "context-engineering/09-planning/STAGEME_PRECALL_READINESS_REPORT.md",
        ):
            path = ROOT / rel
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for description, value in doc_values.items():
                if value and str(value) not in text:
                    errors.append(f"{rel} missing ACE-Step {description}: {value}")


def validate_evidence_labels(errors: list[str]) -> None:
    """Prevent third-party provider and registry pages from becoming event-official facts."""

    third_party_markers = (
        "replicate.com",
        "runpod.io",
        "modal.com",
        "vast.ai",
        "lambda.ai",
        "pypi.org",
        "pypi distributions",
    )
    for rel in (
        "context-engineering/10-sources/SOURCE_LEDGER.md",
        "context-engineering/09-planning/STAGEME_PRECALL_READINESS_REPORT.md",
    ):
        path = ROOT / rel
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            lowered = line.lower()
            if "[official]" in lowered and any(
                marker in lowered for marker in third_party_markers
            ):
                errors.append(
                    f"{rel}:{number} labels a third-party provider/PyPI source [OFFICIAL]"
                )


def validate_secrets(errors: list[str]) -> None:
    """Catch common credential forms across source, docs, and configuration."""
    patterns = ("*.md", "*.json", "*.py", "*.sh", "*.toml", "*.yaml", "*.yml")
    candidates = [path for pattern in patterns for path in ROOT.rglob(pattern)]
    candidates.append(ROOT / ".env.example")
    for path in candidates:
        if not path.is_file() or is_excluded(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {name} in {path.relative_to(ROOT)}")


def validate_active_status(errors: list[str]) -> None:
    for rel in ACTIVE_STATUS_FILES:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in STALE_PATTERNS:
            if match := pattern.search(text):
                excerpt = match.group(0).replace("\n", " ")
                errors.append(f"stale active status in {rel}: {excerpt!r}")


def validate_core_phrase(errors: list[str]) -> None:
    product = (
        ROOT / "context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md"
    ).read_text(encoding="utf-8")
    required_terms = [
        "rough sung performance",
        "original",
        "bounded",
        "non-goals",
        "source-conditioned",
    ]
    for term in required_terms:
        if term.lower() not in product.lower():
            errors.append(f"canonical product spec missing required term: {term}")

    if not re.search(r"Wan[^\n]{0,120}3[–-]5 second", product, re.IGNORECASE):
        errors.append(
            "canonical product spec missing the fixed 3–5 second Wan interval"
        )
    if re.search(r"Wan[^\n]{0,100}10[–-]15 second", product, re.IGNORECASE):
        errors.append("canonical product spec still claims a 10–15 second Wan interval")


def validate_stageme_readiness(errors: list[str]) -> None:
    """Check the pre-call safety contract and names-only configuration."""

    report_path = (
        ROOT / "context-engineering/09-planning/STAGEME_PRECALL_READINESS_REPORT.md"
    )
    runbook_path = (
        ROOT / "context-engineering/09-planning/STAGEME_FIRST_CALL_RUNBOOK.md"
    )
    if report_path.is_file():
        report = report_path.read_text(encoding="utf-8").lower()
        for term in (
            "conditionally ready",
            "authorized f1",
            "evidence level",
            "provider calls",
            "failure and fallback",
        ):
            if term not in report:
                errors.append(
                    f"pre-call readiness report missing required term: {term}"
                )
    if runbook_path.is_file():
        runbook = runbook_path.read_text(encoding="utf-8").lower()
        for term in (
            "anyaccomp",
            "null test",
            "stop",
            "clean up",
            "roll back",
            "sha-256",
        ):
            if term not in runbook:
                errors.append(f"first-call runbook missing required term: {term}")

    env_path = ROOT / ".env.example"
    if env_path.is_file():
        for number, raw in enumerate(
            env_path.read_text(encoding="utf-8").splitlines(), 1
        ):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                errors.append(f".env.example:{number} is not a NAME= placeholder")
                continue
            name, value = line.split("=", 1)
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
                errors.append(f".env.example:{number} has malformed variable name")
            if value:
                errors.append(f".env.example:{number} must not contain a value")

    consent_path = ROOT / "templates/STAGEME_CONSENT.example.json"
    if consent_path.is_file():
        try:
            consent = json.loads(consent_path.read_text(encoding="utf-8"))
            training_reuse = consent["allowed_purposes"]["training_reuse"]
            accepted = consent["accepted"]
            original_hash = consent["source_original_sha256"]
            canonical_hash = consent["source_canonical_sha256"]
            canonicalization = consent["canonicalization"]
            processing = consent["processing"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid StageMe consent template contract: {exc}")
        else:
            if training_reuse is not False:
                errors.append(
                    "StageMe consent template must default training_reuse to false"
                )
            if accepted is not False:
                errors.append("StageMe consent template must default accepted to false")
            if original_hash is not None or canonical_hash is not None:
                errors.append("StageMe consent template hashes must default to null")
            if canonicalization.get("operation") != "decode-downmix-resample-only":
                errors.append(
                    "StageMe consent template has stale canonicalization policy"
                )
            if processing.get("checkpoint_revision") is not None:
                errors.append(
                    "StageMe consent template checkpoint revision must be user-filled"
                )
            if processing.get("approved_spend_cap_usd") is not None:
                errors.append("StageMe consent template spend cap must be user-filled")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_markdown_links(errors)
    validate_json(errors)
    validate_evidence_labels(errors)
    validate_secrets(errors)
    validate_active_status(errors)
    validate_core_phrase(errors)
    validate_stageme_readiness(errors)

    if errors:
        print(f"FAIL: {len(errors)} context error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    markdown_count = sum(1 for path in ROOT.rglob("*.md") if not is_excluded(path))
    json_count = sum(1 for path in ROOT.rglob("*.json") if not is_excluded(path))
    ledger_count = len(
        json.loads(
            (ROOT / "context-engineering/10-sources/repositories.json").read_text(
                encoding="utf-8"
            )
        )
    )
    print("PASS: context integrity checks succeeded")
    print(f"- markdown files checked: {markdown_count}")
    print(f"- JSON files checked: {json_count}")
    print(f"- repository ledger entries checked: {ledger_count}")
    print(f"- required StageMe files checked: {len(REQUIRED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
