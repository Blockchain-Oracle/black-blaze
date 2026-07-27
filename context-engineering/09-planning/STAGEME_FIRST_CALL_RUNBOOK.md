# StageMe First Authorized Call Runbook

> **Status:** prepared and mechanically validated; never executed with human media.
>
> **First-call model:** `AmphionTeam/AnyAccomp@82604b5e3107944ad4c49fc64900b86118ae2c62`, checkpoint revision `9aa9e62427337bf1df4caa3c4f3e6ad934522e71`.
>
> **One-call goal:** generate one separate accompaniment, build StageMe's own lossless premaster with the authorized canonical source audibly present, and pass literal-retention plus media-QC gates before judging quality.

This runbook begins only after the owner supplies F1 and approves the named GPU provider, disclosed region, retention terms, and a finite positive spend cap. It does not deploy, write to B2, call ACE-Step, or call Wan.

## 1. Non-negotiable gates

| Gate | Required evidence | Stop if absent |
|---|---|---|
| Fixture | One user-owned, dry, 8–15 second rough sung phrase | Yes |
| Consent | Exact project/original-byte hash, named provider/region/model/revision, terms, retention, and affirmative acceptance | Yes |
| Worker | Linux/NVIDIA; first-run risk-control gate is compute capability ≥8.0 and ≥24 GiB VRAM | Yes |
| Budget | Live rate snapshot, finite owner-approved cap, noncompute reserve, and provider-native hard termination whose maximum fits that cap | Yes |
| Privacy | Secure transfer, private worker, deletion procedure, and provider terms disclosed | Yes |
| Source/checkpoints | Exact commits, clean tracked source, filenames, byte sizes, and SHA-256 below | Yes |
| Evidence destination | Private user-controlled location outside Git | Yes |
| Preflight | Worker `anyaccomp-local` report contains no blocker | Yes |

The 24 GiB Ampere-or-newer gate is risk control, not a measured AnyAccomp minimum. Do not silently lower it or change models.

## 2. Data and shell boundary

Authorized audio may exist only on the user's device, the private local run root, the disclosed dedicated worker, and—only after a separate authorized canary—private B2. Never put media, credentials, signed URLs, or logs containing them in Git.

The code fences form **two continuous fail-closed sessions**, not independent
shells:

1. the user-controlled local/control session runs Sections 3–4, provisions the
   Pod, remains open as the independent termination control, and resumes for
   copy-out/termination/final review;
2. one worker session runs Sections 5–10 without opening a new shell.

Each session starts with:

```bash
set -euo pipefail
umask 077
```

Do not paste credentials into commands or logs. The provider account and transfer mechanism are selected by the owner; this document does not accept terms or fund an account.

Variables deliberately persist between fences inside their named session. If a
session is lost, do not guess or partially recreate state: stop/terminate the
worker, preserve the local original, and restart the affected phase with a new
empty run root. Never execute a later fence by itself.

Default proposed retention is worker deletion immediately after verified download and no later than 24 hours, plus seven days for the user-controlled bundle unless the owner changes it before acceptance. Training reuse remains false.

## 3. Local run root, QC environment, and original binding

From a clean Black Blaze checkout on the user-controlled machine:

```bash
set -euo pipefail
umask 077

STAGEME_REPO_ROOT="/absolute/path/to/black-blaze"
STAGEME_RUN_ROOT="/absolute/private/path/stageme-F1-$(date -u +%Y%m%dT%H%M%SZ)"
export STAGEME_PROJECT_ID="<new-private-project-id>"
export STAGEME_GPU_PROVIDER="RunPod Secure Cloud"
export STAGEME_GPU_REGION="<exact-approved-country-or-data-center>"
export STAGEME_SPEND_CAP_USD="<finite-positive-owner-approved-cap>"
STAGEME_GPU_RATE_USD_PER_HOUR="<exact-live-offer-rate>"
STAGEME_NONCOMPUTE_RESERVE_USD="<storage-and-rounding-reserve>"
STAGEME_HARD_TERMINATE_AFTER_HOURS="<integer-hours-1-through-24>"
STAGEME_GPU_OFFER_LABEL="<exact-gpu-offer-label>"
STAGEME_WORKER_IMAGE="<immutable-image@sha256:digest>"
STAGEME_PROVIDER_PRICE_CHECKED_AT_UTC="<ISO-8601-UTC-check-time>"
STAGEME_PROVIDER_PRICE_SOURCE_URL="https://www.runpod.io/pricing"
RUNPOD_GPU_ID="<exact-runpod-gpu-id>"
RUNPOD_COUNTRY_CODE="<exact-approved-country-code>"
test -d "$STAGEME_REPO_ROOT/.git"
test ! -e "$STAGEME_RUN_ROOT" || exit 73
mkdir -p "$STAGEME_RUN_ROOT"/{fixture,input,environment,run,output,qc,review,transfer}
chmod 700 "$STAGEME_RUN_ROOT"

command -v uv >/dev/null
uv venv --python 3.12 "$STAGEME_RUN_ROOT/environment/qc-env"
STAGEME_QC_PYTHON="$STAGEME_RUN_ROOT/environment/qc-env/bin/python"
uv pip install --python "$STAGEME_QC_PYTHON" \
  'numpy==2.4.6' 'scipy==1.17.1' 'soundfile==0.14.0' \
  'librosa==0.11.0' 'pyloudnorm==0.2.0'

"$STAGEME_QC_PYTHON" --version \
  > "$STAGEME_RUN_ROOT/environment/qc-python.txt"
uv pip freeze --python "$STAGEME_QC_PYTHON" \
  > "$STAGEME_RUN_ROOT/environment/qc-pip-freeze.txt"
git -C "$STAGEME_REPO_ROOT" rev-parse HEAD \
  > "$STAGEME_RUN_ROOT/environment/readiness-code-commit.txt"
git -C "$STAGEME_REPO_ROOT" diff --quiet HEAD --

STAGEME_BUDGET_PLAN="$STAGEME_RUN_ROOT/run/budget-plan.json"
"$STAGEME_QC_PYTHON" - \
  "$STAGEME_BUDGET_PLAN" \
  "$STAGEME_PROJECT_ID" "$STAGEME_GPU_PROVIDER" "$STAGEME_GPU_REGION" \
  "$STAGEME_GPU_OFFER_LABEL" "$STAGEME_WORKER_IMAGE" \
  "$STAGEME_PROVIDER_PRICE_SOURCE_URL" "$STAGEME_PROVIDER_PRICE_CHECKED_AT_UTC" \
  "$STAGEME_GPU_RATE_USD_PER_HOUR" "$STAGEME_NONCOMPUTE_RESERVE_USD" \
  "$STAGEME_SPEND_CAP_USD" "$STAGEME_HARD_TERMINATE_AFTER_HOURS" <<'PY'
import json
import pathlib
import sys

(
    destination,
    project_id,
    provider,
    region,
    gpu_offer,
    worker_image,
    price_url,
    price_checked_at,
    rate,
    reserve,
    cap,
    terminate_hours,
) = sys.argv[1:]
plan = {
    "schema_version": "1",
    "project_id": project_id,
    "provider": provider,
    "region": region,
    "gpu_offer_label": gpu_offer,
    "worker_image": worker_image,
    "provider_price_source_url": price_url,
    "price_checked_at_utc": price_checked_at,
    "gpu_rate_usd_per_hour": float(rate),
    "noncompute_reserve_usd": float(reserve),
    "approved_spend_cap_usd": float(cap),
    "hard_terminate_after_hours": int(terminate_hours),
    "hard_termination_control": "runpodctl pod create --terminate-after",
    "model": "AmphionTeam/AnyAccomp",
    "model_commit": "82604b5e3107944ad4c49fc64900b86118ae2c62",
    "checkpoint_revision": "9aa9e62427337bf1df4caa3c4f3e6ad934522e71",
    "owner_approved": True,
}
pathlib.Path(destination).write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
PY
```

Place the recording without changing its extension at `fixture/F1-original.<wav|flac|m4a|mp3|webm|ogg|opus>`. Set its exact path once:

```bash
STAGEME_ORIGINAL="$STAGEME_RUN_ROOT/fixture/F1-original.wav"
test -s "$STAGEME_ORIGINAL"

"$STAGEME_QC_PYTHON" - "$STAGEME_ORIGINAL" \
  > "$STAGEME_RUN_ROOT/input/original.sha256" <<'PY'
import hashlib
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
digest = hashlib.sha256(path.read_bytes()).hexdigest()
print(digest)
PY

ffprobe -v error \
  -show_entries format=duration,format_name,size:stream=codec_name,codec_type,sample_rate,channels \
  -of json "$STAGEME_ORIGINAL" \
  > "$STAGEME_RUN_ROOT/qc/original.ffprobe.json"
```

Now copy `templates/STAGEME_CONSENT.example.json` outside Git and fill it. `project_id` must equal `STAGEME_PROJECT_ID`, and `source_original_sha256` must equal the hash just produced. Disclose the selected provider, region, exact AnyAccomp code/checkpoint revisions, provider-native hard deadline, finite positive approved spend cap, terms URL, and retention before the performer sets `accepted: true` and a UTC `accepted_at_utc`. Leave `source_canonical_sha256` and the three runtime-specific canonicalization evidence fields null until normalization.

The sequence is deliberate: **record → hash the exact original → disclose processing/retention → accept → preflight**. Consent for a different file does not transfer.

```bash
STAGEME_CONSENT="$STAGEME_RUN_ROOT/fixture/consent.json"
test -s "$STAGEME_CONSENT"

"$STAGEME_QC_PYTHON" "$STAGEME_REPO_ROOT/scripts/stageme_preflight.py" \
  --phase precall \
  --repo-root "$STAGEME_REPO_ROOT" \
  --work-root "$STAGEME_RUN_ROOT" \
  --fixture "$STAGEME_ORIGINAL" \
  --consent "$STAGEME_CONSENT" \
  --json > "$STAGEME_RUN_ROOT/qc/precall-original.json"
```

This blocks corrupt, out-of-range, silent, repeatedly clipped, materially DC-offset, or hash-mismatched input. It does not prove the singing is suitable.

## 4. Canonical source and execution record

The F1 policy does not denoise, pitch-correct, time-warp, normalize loudness, trim, fade, or remove DC. Preflight rejects material DC offset; the accepted file is only decoded, downmixed, and resampled.

Resolve one local FFmpeg binary, record it, and never switch it during this run:

```bash
set -euo pipefail
umask 077

STAGEME_FFMPEG="$(command -v ffmpeg)"
STAGEME_FFPROBE="$(command -v ffprobe)"
test -x "$STAGEME_FFMPEG"
test -x "$STAGEME_FFPROBE"
"$STAGEME_FFMPEG" -version \
  > "$STAGEME_RUN_ROOT/environment/local-ffmpeg-version.txt"
"$STAGEME_FFMPEG" -buildconf \
  > "$STAGEME_RUN_ROOT/environment/local-ffmpeg-buildconf.txt" 2>&1
"$STAGEME_QC_PYTHON" - "$STAGEME_FFMPEG" \
  > "$STAGEME_RUN_ROOT/environment/local-ffmpeg.sha256" <<'PY'
import hashlib
import pathlib
import sys

print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())
PY

STAGEME_CANONICAL="$STAGEME_RUN_ROOT/input/F1-24k-mono-f32.wav"
"$STAGEME_FFMPEG" -nostdin -hide_banner -y \
  -i "$STAGEME_ORIGINAL" -map 0:a:0 -vn \
  -af 'aresample=resampler=soxr:precision=28,aformat=sample_fmts=flt:sample_rates=24000:channel_layouts=mono' \
  -c:a pcm_f32le "$STAGEME_CANONICAL"

"$STAGEME_QC_PYTHON" - "$STAGEME_CANONICAL" \
  > "$STAGEME_RUN_ROOT/input/canonical-source.sha256" <<'PY'
import hashlib
import pathlib
import sys

print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())
PY
"$STAGEME_FFPROBE" -v error -show_streams -show_format -of json \
  "$STAGEME_CANONICAL" > "$STAGEME_RUN_ROOT/qc/canonical-source.ffprobe.json"
```

Create an execution copy of the accepted consent. Adding the derived canonical hash and runtime evidence binds transfer bytes; it does not broaden the already accepted purpose:

```bash
STAGEME_EXECUTION_CONSENT="$STAGEME_RUN_ROOT/fixture/consent-run.json"
cp "$STAGEME_CONSENT" "$STAGEME_EXECUTION_CONSENT"
"$STAGEME_QC_PYTHON" - \
  "$STAGEME_EXECUTION_CONSENT" \
  "$STAGEME_RUN_ROOT/input/canonical-source.sha256" \
  "$STAGEME_RUN_ROOT/environment/local-ffmpeg.sha256" \
  "$STAGEME_RUN_ROOT/environment/local-ffmpeg-version.txt" <<'PY'
import json
import pathlib
import sys

consent_path, source_hash_path, binary_hash_path, version_path = map(pathlib.Path, sys.argv[1:])
record = json.loads(consent_path.read_text())
record["source_canonical_sha256"] = source_hash_path.read_text().strip()
record["canonicalization"]["ffmpeg_binary_sha256"] = binary_hash_path.read_text().strip()
record["canonicalization"]["ffmpeg_version"] = version_path.read_text().splitlines()[0]
record["canonicalization"]["command"] = "aresample=resampler=soxr:precision=28,aformat=sample_fmts=flt:sample_rates=24000:channel_layouts=mono;pcm_f32le"
consent_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
PY
```

Run the dedicated local binding phase. It requires canonical media, project,
consent, model/checkpoint identity, provider/region/cap, and the provider-native
budget plan, but deliberately does not require worker source, checkpoints, or a
GPU. This prevents an unrelated expected worker blocker from hiding a media or
consent failure:

```bash
"$STAGEME_QC_PYTHON" "$STAGEME_REPO_ROOT/scripts/stageme_preflight.py" \
  --phase anyaccomp-binding \
  --repo-root "$STAGEME_REPO_ROOT" \
  --work-root "$STAGEME_RUN_ROOT" \
  --fixture "$STAGEME_CANONICAL" \
  --consent "$STAGEME_EXECUTION_CONSENT" \
  --budget-plan "$STAGEME_BUDGET_PLAN" \
  --json > "$STAGEME_RUN_ROOT/qc/preflight-local-binding.json"

"$STAGEME_QC_PYTHON" - \
  "$STAGEME_RUN_ROOT/qc/preflight-local-binding.json" <<'PY'
import json
import pathlib
import sys

report = json.loads(pathlib.Path(sys.argv[1]).read_text())
required = {
    "fixture.authorized-audio",
    "fixture.consent",
    "budget.hard-plan",
    "env.stageme_project_id",
    "env.stageme_gpu_provider",
    "env.stageme_gpu_region",
    "env.stageme_spend_cap_usd",
}
statuses = {item["check_id"]: item["status"] for item in report["checks"]}
failed = sorted(name for name in required if statuses.get(name) != "pass")
if report["overall"] == "blocker" or failed:
    raise SystemExit("local media/consent/budget binding failed: " + ", ".join(failed))
PY
```

Package only tracked readiness code and create transfer hashes:

```bash
git -C "$STAGEME_REPO_ROOT" archive --format=tar HEAD \
  > "$STAGEME_RUN_ROOT/transfer/black-blaze-readiness.tar"
cp "$STAGEME_CANONICAL" "$STAGEME_RUN_ROOT/transfer/F1-24k-mono-f32.wav"
cp "$STAGEME_EXECUTION_CONSENT" "$STAGEME_RUN_ROOT/transfer/consent-run.json"
cp "$STAGEME_BUDGET_PLAN" "$STAGEME_RUN_ROOT/transfer/budget-plan.json"
cp "$STAGEME_RUN_ROOT/environment/readiness-code-commit.txt" \
  "$STAGEME_RUN_ROOT/transfer/readiness-code-commit.txt"
"$STAGEME_QC_PYTHON" - "$STAGEME_RUN_ROOT/transfer" \
  > "$STAGEME_RUN_ROOT/transfer/transfer.sha256" <<'PY'
import hashlib
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
for name in (
    "black-blaze-readiness.tar",
    "F1-24k-mono-f32.wav",
    "consent-run.json",
    "budget-plan.json",
    "readiness-code-commit.txt",
):
    data = (root / name).read_bytes()
    print(f"{hashlib.sha256(data).hexdigest()}  {name}")
PY
```

### First paid boundary: provision with a hard provider deadline

The local/control shell must still be open. `runpodctl` reads its API key from
`RUNPOD_API_KEY` or the user's private config; never put that value in this
repository or a command argument. The current official CLI exposes
`--terminate-after` at Pod creation. Its provider-side deadline is the failsafe;
the operator still deletes the Pod immediately after verified copy-out.

```bash
command -v runpodctl >/dev/null
test -n "${RUNPOD_API_KEY:-}" || test -s "$HOME/.runpod/config.toml"
runpodctl pod list >/dev/null

runpodctl pod create \
  --name "stageme-${STAGEME_PROJECT_ID}" \
  --gpu-id "$RUNPOD_GPU_ID" \
  --gpu-count 1 \
  --image "$STAGEME_WORKER_IMAGE" \
  --container-disk-in-gb 40 \
  --country-code "$RUNPOD_COUNTRY_CODE" \
  --terminate-after "${STAGEME_HARD_TERMINATE_AFTER_HOURS}h" \
  > "$STAGEME_RUN_ROOT/environment/runpod-create.txt"

RUNPOD_POD_ID="<pod-id-returned-by-runpodctl>"
test -n "$RUNPOD_POD_ID"
runpodctl pod get "$RUNPOD_POD_ID" \
  > "$STAGEME_RUN_ROOT/environment/runpod-provisioned.txt"
printf '%s\n' "$RUNPOD_POD_ID" \
  > "$STAGEME_RUN_ROOT/environment/runpod-pod-id.txt"
```

Do not proceed if the returned Pod does not show the selected GPU, region,
immutable image, and termination deadline. Move the six transfer files (the
five hashed payloads plus `transfer.sha256`) through the approved encrypted
channel. Do not use a public URL. Keep this local/control shell open so it can
terminate the Pod independently of the worker session.

## 5. Dedicated worker and two isolated environments

On the approved Linux/NVIDIA worker:

```bash
set -euo pipefail
umask 077

STAGEME_WORKER_ROOT="/secure/stageme-F1"
test ! -e "$STAGEME_WORKER_ROOT" || exit 73
mkdir -p "$STAGEME_WORKER_ROOT"/{src,fixture,input,environment,run,output,qc,review,transfer}
chmod 700 "$STAGEME_WORKER_ROOT"
date -u +'%Y-%m-%dT%H:%M:%SZ' \
  > "$STAGEME_WORKER_ROOT/environment/worker-session-started-at-utc.txt"
uname -a > "$STAGEME_WORKER_ROOT/environment/uname.txt"
test -r /etc/os-release
cp /etc/os-release "$STAGEME_WORKER_ROOT/environment/os-release.txt"
command -v lscpu >/dev/null
command -v free >/dev/null
lscpu > "$STAGEME_WORKER_ROOT/environment/lscpu.txt"
free -b > "$STAGEME_WORKER_ROOT/environment/memory.txt"
df -B1 "$STAGEME_WORKER_ROOT" \
  > "$STAGEME_WORKER_ROOT/environment/disk.txt"
```

Place the six transfer files in `transfer/`, then verify before extraction:

```bash
set -euo pipefail
cd "$STAGEME_WORKER_ROOT/transfer"
sha256sum -c transfer.sha256 | tee "$STAGEME_WORKER_ROOT/environment/transfer.sha256-check.txt"
mkdir -p "$STAGEME_WORKER_ROOT/src/black-blaze-readiness"
tar -xf black-blaze-readiness.tar -C "$STAGEME_WORKER_ROOT/src/black-blaze-readiness"
cp F1-24k-mono-f32.wav "$STAGEME_WORKER_ROOT/input/F1-24k-mono-f32.wav"
cp consent-run.json "$STAGEME_WORKER_ROOT/fixture/consent-run.json"
cp budget-plan.json "$STAGEME_WORKER_ROOT/run/budget-plan.json"
cp readiness-code-commit.txt \
  "$STAGEME_WORKER_ROOT/environment/readiness-code-commit.txt"
cp budget-plan.json "$STAGEME_WORKER_ROOT/environment/provider-price-and-budget.json"
```

Clone and pin the executable model source. The preflight checks the entire tracked tree for modifications, while allowing untracked checkpoints:

```bash
mkdir "$STAGEME_WORKER_ROOT/src/AnyAccomp"
git -C "$STAGEME_WORKER_ROOT/src/AnyAccomp" init
git -C "$STAGEME_WORKER_ROOT/src/AnyAccomp" remote add origin \
  https://github.com/AmphionTeam/AnyAccomp.git
git -C "$STAGEME_WORKER_ROOT/src/AnyAccomp" fetch --depth 1 origin \
  82604b5e3107944ad4c49fc64900b86118ae2c62
git -C "$STAGEME_WORKER_ROOT/src/AnyAccomp" checkout --detach FETCH_HEAD
git -C "$STAGEME_WORKER_ROOT/src/AnyAccomp" diff --quiet HEAD --
git -C "$STAGEME_WORKER_ROOT/src/AnyAccomp" rev-parse HEAD \
  > "$STAGEME_WORKER_ROOT/environment/anyaccomp-code-commit.txt"
```

Create separate stock-model and StageMe QC environments. AnyAccomp stays on Python 3.9; Genblaze/control/QC stays on Python 3.12.

```bash
STAGEME_ENV_MANAGER="$(command -v micromamba || command -v mamba || command -v conda)"
test -x "$STAGEME_ENV_MANAGER"

"$STAGEME_ENV_MANAGER" create -y -p "$STAGEME_WORKER_ROOT/model-env" \
  -c conda-forge python=3.9 pip ffmpeg=4.4.2
"$STAGEME_ENV_MANAGER" create -y -p "$STAGEME_WORKER_ROOT/qc-env" \
  -c conda-forge python=3.12 pip

STAGEME_MODEL_PYTHON="$STAGEME_WORKER_ROOT/model-env/bin/python"
STAGEME_QC_PYTHON="$STAGEME_WORKER_ROOT/qc-env/bin/python"
STAGEME_FFMPEG="$STAGEME_WORKER_ROOT/model-env/bin/ffmpeg"
STAGEME_FFPROBE="$STAGEME_WORKER_ROOT/model-env/bin/ffprobe"

"$STAGEME_MODEL_PYTHON" -m pip install \
  -r "$STAGEME_WORKER_ROOT/src/AnyAccomp/requirements.txt"
"$STAGEME_QC_PYTHON" -m pip install \
  'numpy==2.4.6' 'scipy==1.17.1' 'soundfile==0.14.0' \
  'librosa==0.11.0' 'pyloudnorm==0.2.0'

"$STAGEME_MODEL_PYTHON" -m pip freeze \
  > "$STAGEME_WORKER_ROOT/environment/model-pip-freeze.txt"
"$STAGEME_QC_PYTHON" -m pip freeze \
  > "$STAGEME_WORKER_ROOT/environment/qc-pip-freeze.txt"
"$STAGEME_ENV_MANAGER" list -p "$STAGEME_WORKER_ROOT/model-env" --explicit \
  > "$STAGEME_WORKER_ROOT/environment/model-conda-explicit.txt"
"$STAGEME_FFMPEG" -version \
  > "$STAGEME_WORKER_ROOT/environment/ffmpeg-version.txt"
"$STAGEME_FFMPEG" -buildconf \
  > "$STAGEME_WORKER_ROOT/environment/ffmpeg-buildconf.txt" 2>&1
sha256sum "$STAGEME_FFMPEG" "$STAGEME_FFPROBE" \
  > "$STAGEME_WORKER_ROOT/environment/ffmpeg-binaries.sha256"
nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap \
  --format=csv,noheader \
  > "$STAGEME_WORKER_ROOT/environment/gpu.txt"
```

Stop on any environment, import, or binary-resolution failure. Do not patch upstream before capturing and reviewing the failure.

## 6. Exact checkpoint acquisition

This authorized step downloads 2,078,199,136 bytes total; each individual file is below 2 GB. The model card declares CC BY 4.0, so preserve author/model attribution, link the license, state modifications, and include the paper citation in eventual credits.

```bash
set -euo pipefail
cd "$STAGEME_WORKER_ROOT/src/AnyAccomp"
"$STAGEME_MODEL_PYTHON" - <<'PY'
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="amphion/anyaccomp",
    revision="9aa9e62427337bf1df4caa3c4f3e6ad934522e71",
    local_dir=".",
    allow_patterns=[
        "pretrained/flow_matching/pytorch_model.bin",
        "pretrained/vocoder/model.safetensors",
        "pretrained/vq/pytorch_model.bin",
    ],
)
PY

printf '%s  %s\n' \
  'e6802bd1123935a54e990cb8d3897a18190df6c53f73db021baa28c420721129' \
  'pretrained/flow_matching/pytorch_model.bin' \
  '1b7efd04c71c058cd00b4e9a91c761b31da745f878b7d7ee839e157104d3a7da' \
  'pretrained/vocoder/model.safetensors' \
  '9d7f48cefea30602b2148c057faf14ecad168184e8063c8377dd57f208dc65fc' \
  'pretrained/vq/pytorch_model.bin' \
  | sha256sum -c - \
  | tee "$STAGEME_WORKER_ROOT/environment/checkpoints.sha256-check.txt"

printf '%s\n' '9aa9e62427337bf1df4caa3c4f3e6ad934522e71' \
  > "$STAGEME_WORKER_ROOT/environment/checkpoint-revision.txt"
```

Expected byte sizes are 880,790,586; 1,020,206,416; and 177,202,134 respectively. The worker preflight independently rechecks all three sizes and hashes; a failed pipeline cannot be hidden by `tee` because `pipefail` is active.

## 7. Exact worker preflight

```bash
set -euo pipefail
STAGEME_BUDGET_PLAN="$STAGEME_WORKER_ROOT/run/budget-plan.json"
test -s "$STAGEME_BUDGET_PLAN"
budget_value() {
  "$STAGEME_QC_PYTHON" - "$STAGEME_BUDGET_PLAN" "$1" <<'PY'
import json
import pathlib
import sys

print(json.loads(pathlib.Path(sys.argv[1]).read_text())[sys.argv[2]])
PY
}
export STAGEME_PROJECT_ID="$(budget_value project_id)"
export STAGEME_GPU_PROVIDER="$(budget_value provider)"
export STAGEME_GPU_REGION="$(budget_value region)"
export STAGEME_SPEND_CAP_USD="$(budget_value approved_spend_cap_usd)"

PATH="$STAGEME_WORKER_ROOT/model-env/bin:$PATH" \
  "$STAGEME_QC_PYTHON" \
  "$STAGEME_WORKER_ROOT/src/black-blaze-readiness/scripts/stageme_preflight.py" \
  --phase anyaccomp-local \
  --repo-root "$STAGEME_WORKER_ROOT/src/black-blaze-readiness" \
  --work-root "$STAGEME_WORKER_ROOT" \
  --fixture "$STAGEME_WORKER_ROOT/input/F1-24k-mono-f32.wav" \
  --consent "$STAGEME_WORKER_ROOT/fixture/consent-run.json" \
  --budget-plan "$STAGEME_BUDGET_PLAN" \
  --checkpoint-root "$STAGEME_WORKER_ROOT/src/AnyAccomp/pretrained" \
  --anyaccomp-root "$STAGEME_WORKER_ROOT/src/AnyAccomp" \
  --model-python "$STAGEME_MODEL_PYTHON" \
  --json > "$STAGEME_WORKER_ROOT/qc/preflight-worker.json"
```

Exit must be zero. This checks Python/QC pins; fail-closed worker tools; exact clean source; checkpoint hashes; canonical 24 kHz mono float32 WAV; audio QC; project/media/consent binding; provider/region/model/retention binding; provider-native deadline math; positive cap; GPU VRAM; and Torch 2.3.1/Torchaudio 2.3.1/Torchvision 0.18.1/CUDA 12.1/bfloat16/compute-capability imports.

## 8. Generate exactly one candidate

```bash
set -euo pipefail
MODEL_INPUT="$STAGEME_WORKER_ROOT/run/model-input"
RAW_OUTPUT="$STAGEME_WORKER_ROOT/run/anyaccomp-raw"
mkdir -p "$MODEL_INPUT" "$RAW_OUTPUT"
cp "$STAGEME_WORKER_ROOT/input/F1-24k-mono-f32.wav" "$MODEL_INPUT/F1.wav"
test "$(find "$MODEL_INPUT" -maxdepth 1 -type f | wc -l | tr -d ' ')" -eq 1

cd "$STAGEME_WORKER_ROOT/src/AnyAccomp"
START_EPOCH="$(date +%s)"
date -u +'%Y-%m-%dT%H:%M:%SZ' \
  > "$STAGEME_WORKER_ROOT/run/inference-started-at-utc.txt"
nvidia-smi \
  --query-gpu=timestamp,index,memory.used,utilization.gpu \
  --format=csv,noheader,nounits -l 1 \
  > "$STAGEME_WORKER_ROOT/run/gpu-samples.csv" 2>&1 &
GPU_SAMPLER_PID=$!
set +e
/usr/bin/time -v timeout --signal=TERM --kill-after=60s 30m \
  "$STAGEME_MODEL_PYTHON" infer_from_folder.py \
  --input_folder "$MODEL_INPUT" \
  --infer_dst "$RAW_OUTPUT" \
  --cfg_path ./config/flow_matching.json \
  --checkpoint_path ./pretrained/flow_matching \
  --vocoder_checkpoint_path ./pretrained/vocoder \
  --vocoder_cfg_path ./config/vocoder.json \
  --n_timesteps 50 --cfg 3 --device cuda --seed 1024 \
  > "$STAGEME_WORKER_ROOT/run/stdout.txt" \
  2> "$STAGEME_WORKER_ROOT/run/stderr-and-time.txt"
INFERENCE_EXIT=$?
kill "$GPU_SAMPLER_PID" 2>/dev/null
wait "$GPU_SAMPLER_PID" 2>/dev/null
END_EPOCH="$(date +%s)"
set -e
date -u +'%Y-%m-%dT%H:%M:%SZ' \
  > "$STAGEME_WORKER_ROOT/run/inference-ended-at-utc.txt"
STAGEME_RUNTIME_SECONDS="$((END_EPOCH - START_EPOCH))"
printf '%s\n' "$INFERENCE_EXIT" > "$STAGEME_WORKER_ROOT/run/exit-code.txt"
printf '%s\n' "$STAGEME_RUNTIME_SECONDS" > "$STAGEME_WORKER_ROOT/run/runtime-seconds.txt"
"$STAGEME_QC_PYTHON" - \
  "$STAGEME_WORKER_ROOT/run/gpu-samples.csv" \
  "$STAGEME_WORKER_ROOT/run/gpu-peak.json" <<'PY'
import csv
import json
import pathlib
import sys

source, destination = map(pathlib.Path, sys.argv[1:])
memory_mib = []
utilization_percent = []
with source.open(newline="") as handle:
    for row in csv.reader(handle):
        if len(row) < 4:
            continue
        try:
            memory_mib.append(int(row[2].strip()))
            utilization_percent.append(int(row[3].strip()))
        except ValueError:
            continue
if not memory_mib:
    raise SystemExit("no parseable GPU samples")
destination.write_text(
    json.dumps(
        {
            "schema_version": "1",
            "samples": len(memory_mib),
            "peak_gpu_memory_mib": max(memory_mib),
            "peak_gpu_utilization_percent": max(utilization_percent),
        },
        indent=2,
        sort_keys=True,
    )
    + "\n"
)
PY
test "$INFERENCE_EXIT" -eq 0
if grep -q 'Error processing' "$STAGEME_WORKER_ROOT/run/stdout.txt" \
  "$STAGEME_WORKER_ROOT/run/stderr-and-time.txt"; then
  exit 74
fi

RAW_ACCOMP="$RAW_OUTPUT/accompaniment/F1.wav"
RAW_MIXTURE="$RAW_OUTPUT/mixture/F1.wav"
test -s "$RAW_ACCOMP"
test -s "$RAW_MIXTURE"
test "$(find "$RAW_OUTPUT" -type f -name '*.wav' | wc -l | tr -d ' ')" -eq 2
cp "$RAW_OUTPUT/config.json" "$STAGEME_WORKER_ROOT/run/config.json"
cp "$RAW_MIXTURE" "$STAGEME_WORKER_ROOT/output/upstream-raw-mixture.wav"

STAGEME_ACCOMP="$STAGEME_WORKER_ROOT/output/accompaniment-f32.wav"
"$STAGEME_FFMPEG" -nostdin -hide_banner -y -i "$RAW_ACCOMP" \
  -map 0:a:0 -ar 24000 -ac 1 -c:a pcm_f32le "$STAGEME_ACCOMP"
```

Verify exact frame alignment and deterministic accompaniment QC:

```bash
"$STAGEME_QC_PYTHON" - \
  "$STAGEME_WORKER_ROOT/input/F1-24k-mono-f32.wav" \
  "$STAGEME_ACCOMP" <<'PY'
import soundfile as sf
import sys

source, source_rate = sf.read(sys.argv[1], always_2d=True)
accomp, accomp_rate = sf.read(sys.argv[2], always_2d=True)
if source_rate != 24000 or accomp_rate != 24000 or source.shape != accomp.shape:
    raise SystemExit("source/accompaniment sample alignment mismatch")
PY

PATH="$STAGEME_WORKER_ROOT/model-env/bin:$PATH" \
  "$STAGEME_QC_PYTHON" \
  "$STAGEME_WORKER_ROOT/src/black-blaze-readiness/scripts/stageme_preflight.py" \
  --phase precall \
  --repo-root "$STAGEME_WORKER_ROOT/src/black-blaze-readiness" \
  --work-root "$STAGEME_WORKER_ROOT" \
  --fixture "$STAGEME_ACCOMP" \
  --json > "$STAGEME_WORKER_ROOT/qc/accompaniment-preflight.json"
```

Stop without retry on timeout, CUDA/OOM/NaN, caught per-file error, missing/extra output, silence, clipping, DC failure, alignment mismatch, or spend-cap approach. One seed and one candidate is the initial search boundary.

## 9. StageMe premaster and literal-retention test

The upstream mixture is evidence about upstream semantics only. StageMe uses the separate accompaniment and canonical source with recorded gains of 0.5/0.5 to preserve summation headroom.

```bash
set -euo pipefail
STAGEME_SOURCE="$STAGEME_WORKER_ROOT/input/F1-24k-mono-f32.wav"
STAGEME_PREMASTER="$STAGEME_WORKER_ROOT/output/premaster-f32.wav"

"$STAGEME_FFMPEG" -nostdin -hide_banner -y \
  -i "$STAGEME_SOURCE" -i "$STAGEME_ACCOMP" \
  -filter_complex \
  '[0:a]volume=0.5[s];[1:a]volume=0.5[a];[s][a]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[m]' \
  -map '[m]' -ar 24000 -ac 1 -c:a pcm_f32le "$STAGEME_PREMASTER"

"$STAGEME_QC_PYTHON" \
  "$STAGEME_WORKER_ROOT/src/black-blaze-readiness/scripts/stageme_null_test.py" \
  --source "$STAGEME_SOURCE" \
  --accompaniment "$STAGEME_ACCOMP" \
  --mixture "$STAGEME_PREMASTER" \
  --source-gain 0.5 --accompaniment-gain 0.5 \
  --max-error-tolerance 1e-7 --rms-error-tolerance 1e-8 \
  --json > "$STAGEME_WORKER_ROOT/qc/null-test.json"
```

The null utility rejects source gains below 0.1, non-finite gains, and loose tolerances. Pass requires identical rate/channels/frames plus numeric residual bounds. Correlation alone is insufficient. A failure is a stop: never call the source retained.

## 10. QC, evidence bundle, and human review

```bash
set -euo pipefail
for NAME in accompaniment premaster; do
  case "$NAME" in
    accompaniment) ASSET="$STAGEME_ACCOMP" ;;
    premaster) ASSET="$STAGEME_PREMASTER" ;;
  esac
  "$STAGEME_FFPROBE" -v error -show_streams -show_format -of json "$ASSET" \
    > "$STAGEME_WORKER_ROOT/qc/$NAME.ffprobe.json"
  "$STAGEME_FFMPEG" -nostdin -hide_banner -i "$ASSET" \
    -af 'astats=metadata=1:reset=0' -f null - \
    2> "$STAGEME_WORKER_ROOT/qc/$NAME.astats.txt"
done

PATH="$STAGEME_WORKER_ROOT/model-env/bin:$PATH" \
  "$STAGEME_QC_PYTHON" \
  "$STAGEME_WORKER_ROOT/src/black-blaze-readiness/scripts/stageme_preflight.py" \
  --phase precall \
  --repo-root "$STAGEME_WORKER_ROOT/src/black-blaze-readiness" \
  --work-root "$STAGEME_WORKER_ROOT" \
  --fixture "$STAGEME_PREMASTER" \
  --json > "$STAGEME_WORKER_ROOT/qc/premaster-preflight.json"

"$STAGEME_QC_PYTHON" - \
  "$STAGEME_SOURCE" "$STAGEME_ACCOMP" "$STAGEME_PREMASTER" \
  "$STAGEME_WORKER_ROOT/qc/media-qc.json" <<'PY'
import json
import math
import pathlib
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

paths = {
    "source": pathlib.Path(sys.argv[1]),
    "accompaniment": pathlib.Path(sys.argv[2]),
    "premaster": pathlib.Path(sys.argv[3]),
}
destination = pathlib.Path(sys.argv[4])
metrics = {}
signals = {}
failures = []
reference_shape = None
for name, path in paths.items():
    data, rate = sf.read(path, dtype="float64", always_2d=True)
    signals[name] = data
    finite = np.isfinite(data)
    finite_count = int(finite.sum())
    nonfinite_count = int(data.size - finite_count)
    safe = np.where(finite, data, 0.0)
    peak = float(np.max(np.abs(safe))) if safe.size else 0.0
    rms = float(np.sqrt(np.mean(np.square(safe)))) if safe.size else 0.0
    dc = float(np.mean(safe)) if safe.size else 0.0
    non_silent_fraction = float(np.mean(np.abs(safe) >= 1e-4)) if safe.size else 0.0
    lufs = float(pyln.Meter(rate).integrated_loudness(safe[:, 0])) if safe.size else -math.inf
    metrics[name] = {
        "sample_rate": rate,
        "channels": int(data.shape[1]) if data.ndim == 2 else 0,
        "frames": int(data.shape[0]) if data.ndim == 2 else 0,
        "duration_seconds": float(data.shape[0] / rate) if rate and data.ndim == 2 else 0.0,
        "nonfinite_samples": nonfinite_count,
        "peak": peak,
        "rms": rms,
        "dc_offset": dc,
        "non_silent_fraction": non_silent_fraction,
        "integrated_lufs": lufs,
    }
    shape = (rate, data.shape)
    if reference_shape is None:
        reference_shape = shape
    elif shape != reference_shape:
        failures.append(f"{name}: sample alignment differs from source")
    if rate != 24000 or data.ndim != 2 or data.shape[1] != 1:
        failures.append(f"{name}: not canonical 24 kHz mono")
    if nonfinite_count:
        failures.append(f"{name}: contains non-finite samples")
    if rms < 1e-4 or non_silent_fraction < 0.01:
        failures.append(f"{name}: silent or nearly silent")
    if not math.isfinite(lufs):
        failures.append(f"{name}: LUFS is non-finite")
    if abs(dc) > 0.005:
        failures.append(f"{name}: absolute DC offset exceeds 0.005")
    if name != "source" and peak >= 0.999:
        failures.append(f"{name}: peak reaches the clipping guard")

source_rms = metrics["source"]["rms"]
accompaniment_rms = metrics["accompaniment"]["rms"]
ratio_db = (
    20.0 * math.log10(accompaniment_rms / source_rms)
    if source_rms > 0.0 and accompaniment_rms > 0.0
    else -math.inf
)
metrics["accompaniment_to_source_rms_db"] = ratio_db
if not -24.0 <= ratio_db <= 12.0:
    failures.append("accompaniment/source RMS ratio is outside -24..+12 dB")

result = {
    "schema_version": "1",
    "thresholds": {
        "minimum_rms": 1e-4,
        "minimum_non_silent_fraction": 0.01,
        "maximum_absolute_dc_offset": 0.005,
        "generated_peak_must_be_below": 0.999,
        "accompaniment_to_source_rms_db": [-24.0, 12.0],
    },
    "metrics": metrics,
    "failures": failures,
    "passed": not failures,
}
destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
if failures:
    raise SystemExit("deterministic media QC failed; inspect media-qc.json")
PY

sha256sum "$STAGEME_SOURCE" "$STAGEME_ACCOMP" "$STAGEME_PREMASTER" \
  "$STAGEME_WORKER_ROOT/output/upstream-raw-mixture.wav" \
  > "$STAGEME_WORKER_ROOT/qc/assets.sha256"

"$STAGEME_QC_PYTHON" - "$STAGEME_WORKER_ROOT/review/human-review.json" <<'PY'
import json
import pathlib
import sys

review = {
    "reviewed_at_utc": None,
    "reviewer": None,
    "source_unmistakably_present": None,
    "accompaniment_follows_performance": None,
    "emotional_lift": None,
    "no_destructive_doubling_suppression_or_drift": None,
    "before_after_understood_within_20_seconds": None,
    "accepted": False,
    "notes": None,
}
pathlib.Path(sys.argv[1]).write_text(json.dumps(review, indent=2) + "\n")
PY
```

Generate a **provisional worker manifest** before copy-out. It records measured
runtime/resources and the price plan, but deliberately leaves the final bill,
termination result, and human decision pending. Do not keep a billable Pod alive
while waiting for review or a settled charge:

```bash
export STAGEME_RUNTIME_SECONDS
"$STAGEME_QC_PYTHON" - "$STAGEME_WORKER_ROOT" <<'PY'
import hashlib
import json
import os
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
consent = json.loads((root / "fixture/consent-run.json").read_text())
budget = json.loads((root / "run/budget-plan.json").read_text())
gpu_peak = json.loads((root / "run/gpu-peak.json").read_text())
time_log = (root / "run/stderr-and-time.txt").read_text(errors="replace")
rss_match = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", time_log)
if rss_match is None:
    raise SystemExit("peak CPU RSS was not captured")

assets = {}
for relative in (
    "input/F1-24k-mono-f32.wav",
    "output/accompaniment-f32.wav",
    "output/premaster-f32.wav",
    "output/upstream-raw-mixture.wav",
):
    path = root / relative
    assets[relative] = {
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }

manifest = {
    "schema_version": "1",
    "project_id": consent["project_id"],
    "fixture_id": consent["fixture_id"],
    "readiness_commit": (root / "environment/readiness-code-commit.txt").read_text().strip(),
    "model": "AmphionTeam/AnyAccomp",
    "code_commit": "82604b5e3107944ad4c49fc64900b86118ae2c62",
    "checkpoint_revision": "9aa9e62427337bf1df4caa3c4f3e6ad934522e71",
    "parameters": {"steps": 50, "cfg": 3, "seed": 1024, "device": "cuda"},
    "mix": {"source_gain": 0.5, "accompaniment_gain": 0.5},
    "worker": {
        "provider": budget["provider"],
        "region": budget["region"],
        "gpu_offer_label": budget["gpu_offer_label"],
        "image": budget["worker_image"],
        "cold_start": True,
    },
    "timing": {
        "inference_started_at_utc": (root / "run/inference-started-at-utc.txt").read_text().strip(),
        "inference_ended_at_utc": (root / "run/inference-ended-at-utc.txt").read_text().strip(),
        "inference_wall_seconds": int(os.environ["STAGEME_RUNTIME_SECONDS"]),
    },
    "resources": {
        "peak_cpu_rss_kib": int(rss_match.group(1)),
        **gpu_peak,
    },
    "budget": {
        "price_snapshot": "environment/provider-price-and-budget.json",
        "approved_cap_usd": budget["approved_spend_cap_usd"],
        "hard_terminate_after_hours": budget["hard_terminate_after_hours"],
        "estimated_inference_compute_usd": budget["gpu_rate_usd_per_hour"]
        * int(os.environ["STAGEME_RUNTIME_SECONDS"])
        / 3600.0,
        "actual_billed_usd": None,
        "final_charge_status": "pending provider termination and settlement",
    },
    "candidate_count": 1,
    "retry_count": 0,
    "assets": assets,
    "literal_retention_evidence": "qc/null-test.json",
    "media_qc_evidence": "qc/media-qc.json",
    "human_review": "review/human-review.json",
    "deletion": {
        "worker": "pending verified copy-out and Pod termination",
        "worker_deleted_at_utc": None,
        "provider_termination_verified": False,
        "b2": "not used",
    },
}
(root / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
PY
```

The completed pre-copy bundle is now:

```text
fixture/consent-run.json
input/F1-24k-mono-f32.wav
environment/{readiness-code-commit,provider-price-and-budget,worker-session-started-at-utc,os-release,uname,lscpu,memory,disk,anyaccomp-code-commit,checkpoint-revision,checkpoints.sha256-check,model-pip-freeze,qc-pip-freeze,model-conda-explicit,gpu,ffmpeg-*}
run/{budget-plan,config,stdout,stderr-and-time,exit-code,runtime-seconds,inference-*-at-utc,gpu-samples,gpu-peak}.txt-csv-or-json
output/{accompaniment-f32,premaster-f32,upstream-raw-mixture}.wav
qc/{preflight-worker,accompaniment-preflight,premaster-preflight,null-test,media-qc,assets,*.ffprobe,*.astats}.json-or-txt
review/human-review.json
manifest.json
```

## 11. Verified copy-out, clean up, and roll back

Create and hash the bundle on the worker:

```bash
set -euo pipefail
cd "$STAGEME_WORKER_ROOT"
tar -czf transfer/stageme-F1-evidence.tar.gz \
  fixture input environment run output qc review manifest.json
sha256sum transfer/stageme-F1-evidence.tar.gz \
  > transfer/stageme-F1-evidence.tar.gz.sha256
```

Copy the archive plus hash over the approved encrypted channel. Back in the
still-open local/control shell, verify it before opening:

```bash
STAGEME_TRANSFER_OUT="$STAGEME_RUN_ROOT/transfer-out"
STAGEME_LOCAL_BUNDLE="$STAGEME_RUN_ROOT/result/stageme-F1"
mkdir -p "$STAGEME_TRANSFER_OUT" "$STAGEME_LOCAL_BUNDLE"
# Place stageme-F1-evidence.tar.gz and its .sha256 file in STAGEME_TRANSFER_OUT.
cd "$STAGEME_TRANSFER_OUT"
sha256sum -c stageme-F1-evidence.tar.gz.sha256
tar -xzf stageme-F1-evidence.tar.gz -C "$STAGEME_LOCAL_BUNDLE"
test -s "$STAGEME_LOCAL_BUNDLE/output/premaster-f32.wav"
test -s "$STAGEME_LOCAL_BUNDLE/qc/null-test.json"
test -s "$STAGEME_LOCAL_BUNDLE/qc/media-qc.json"
```

If verification fails, retransfer once without rerunning inference and without
deleting the worker copy.

Only after verified copy-out, delete every file beneath the exact worker run
root. This includes `transfer/`, its copy of F1/consent, the evidence archive,
raw outputs, checkpoints, and logs. Run this in the continuous worker shell:

```bash
set -euo pipefail
test "$STAGEME_WORKER_ROOT" = "/secure/stageme-F1"
find "$STAGEME_WORKER_ROOT" \( -type f -o -type l \) -delete
if find "$STAGEME_WORKER_ROOT" \( -type f -o -type l \) -print -quit \
  | grep -q .; then
  exit 75
fi
```

Immediately return to the local/control shell and terminate—not merely stop—the
Pod. The create-time deadline remains a fallback if this command or the worker
session fails. A failed `pod get` is not absence evidence: authenticate an
entire `pod list --all` request successfully, then require the exact Pod ID to
be absent from that response.

```bash
set +e
runpodctl pod delete "$RUNPOD_POD_ID" \
  > "$STAGEME_RUN_ROOT/environment/runpod-delete.txt" 2>&1
RUNPOD_DELETE_EXIT=$?
set -e
RUNPOD_ABSENCE_VERIFIED=false
for attempt in $(seq 1 10); do
  if runpodctl pod list --all \
    > "$STAGEME_RUN_ROOT/environment/runpod-post-delete-list.txt" 2>&1; then
    if ! awk -v id="$RUNPOD_POD_ID" '
      {
        for (field = 1; field <= NF; field++) {
          if ($field == id) {
            found = 1
          }
        }
      }
      END { exit found ? 0 : 1 }
    ' "$STAGEME_RUN_ROOT/environment/runpod-post-delete-list.txt"; then
      RUNPOD_ABSENCE_VERIFIED=true
      break
    fi
  fi
  sleep 5
done
test "$RUNPOD_ABSENCE_VERIFIED" = true
date -u +'%Y-%m-%dT%H:%M:%SZ' \
  > "$STAGEME_RUN_ROOT/environment/worker-deleted-at-utc.txt"
printf '%s\n' "$RUNPOD_DELETE_EXIT" \
  > "$STAGEME_RUN_ROOT/environment/runpod-delete-exit.txt"
```

A nonzero delete exit is acceptable only when a successful authenticated
`pod list --all` response proves the exact Pod ID is absent, which can happen if
the provider-side deadline removed it first. Authentication, network, rate-limit,
or CLI failures never count as absence. No separate volume is created by this
runbook; if the operator changed that, its deletion and absence are an additional
stop gate.

After termination—not before—wait for the session charge to settle in the
provider billing view. Record that exact charge, fill the local review file, and
finalize the local manifest:

```bash
STAGEME_ACTUAL_BILLED_USD="<final-settled-session-charge>"
export STAGEME_ACTUAL_BILLED_USD
# Privately fill every null review field, set accepted deliberately, and save:
STAGEME_HUMAN_REVIEW="$STAGEME_LOCAL_BUNDLE/review/human-review.json"

set +e
"$STAGEME_QC_PYTHON" - \
  "$STAGEME_LOCAL_BUNDLE" \
  "$STAGEME_HUMAN_REVIEW" \
  "$STAGEME_RUN_ROOT/environment/worker-deleted-at-utc.txt" <<'PY'
from datetime import datetime, timedelta, timezone
import json
import math
import os
import pathlib
import sys

root, review_path, deleted_path = map(pathlib.Path, sys.argv[1:])
manifest_path = root / "manifest.json"
manifest = json.loads(manifest_path.read_text())
review = json.loads(review_path.read_text())
required_true = (
    "source_unmistakably_present",
    "accompaniment_follows_performance",
    "emotional_lift",
    "no_destructive_doubling_suppression_or_drift",
    "before_after_understood_within_20_seconds",
)
review_fields_are_boolean = isinstance(review.get("accepted"), bool) and all(
    isinstance(review.get(name), bool) for name in required_true
)
review_complete = bool(
    review.get("reviewed_at_utc")
    and review.get("reviewer")
    and review_fields_are_boolean
)
review_accepted = review_complete and review.get("accepted") is True and all(
    review.get(name) is True for name in required_true
)

billed = float(os.environ["STAGEME_ACTUAL_BILLED_USD"])
cap = float(manifest["budget"]["approved_cap_usd"])
if not math.isfinite(billed) or billed < 0:
    raise SystemExit("final provider charge is invalid")
budget_passed = billed <= cap
manifest["budget"].update(
    {
        "actual_billed_usd": billed,
        "final_charge_status": "settled",
        "within_approved_cap": budget_passed,
    }
)
deleted_at = deleted_path.read_text().strip()
manifest["deletion"].update(
    {
        "worker": "all run-root files deleted; Pod absent",
        "worker_deleted_at_utc": deleted_at,
        "provider_termination_verified": True,
    }
)
consent = json.loads((root / "fixture/consent-run.json").read_text())
days = int(consent["retention"]["user_controlled_bundle_max_days"])
manifest["deletion"]["local_bundle_delete_by_utc"] = (
    datetime.now(timezone.utc) + timedelta(days=days)
).isoformat()
manifest["human_review_outcome"] = {
    "complete": review_complete,
    "accepted": review_accepted,
    "reviewed_at_utc": review.get("reviewed_at_utc"),
    "reviewer": review.get("reviewer"),
}
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
if not budget_passed:
    raise SystemExit("final charge exceeded the approved cap; stop progression")
if not review_complete:
    raise SystemExit("human review identity/time is incomplete")
if not review_accepted:
    raise SystemExit("human review did not accept every product gate")
PY
STAGEME_FINALIZER_EXIT=$?
set -e
printf '%s\n' "$STAGEME_FINALIZER_EXIT" \
  > "$STAGEME_LOCAL_BUNDLE/environment/finalizer-exit.txt"

(
  cd "$STAGEME_LOCAL_BUNDLE"
  find . -type f -print0 \
    | sort -z \
    | xargs -0 sha256sum \
    > "$STAGEME_RUN_ROOT/final-evidence.sha256"
)
test "$STAGEME_FINALIZER_EXIT" -eq 0 || exit "$STAGEME_FINALIZER_EXIT"
```

Listen privately in this order: original F1, canonical source, accompaniment,
then StageMe premaster. Proceed only if the source is unmistakable, the
accompaniment feels caused by its pitch/rhythm/phrasing, emotional lift is
material, destructive doubling/suppression/drift is absent, and the before/after
reads in under 20 seconds. One accepted artifact is still not product-proven.

At the recorded local deletion deadline—or earlier on request—delete the exact
private `STAGEME_RUN_ROOT`, including the original and every voice-bearing
derivative, then verify the target contains no files. B2 remains `not used`; no
signed URL is persisted.

```bash
STAGEME_DELETE_TARGET="$STAGEME_RUN_ROOT"
test -n "$STAGEME_DELETE_TARGET"
test -s "$STAGEME_DELETE_TARGET/fixture/consent.json"
find "$STAGEME_DELETE_TARGET" \( -type f -o -type l \) -delete
if find "$STAGEME_DELETE_TARGET" \( -type f -o -type l \) -print -quit \
  | grep -q .; then
  exit 76
fi
```

Rollback is always the immutable local original plus canonical source with no accepted child. Never overwrite/delete the original to undo a model result. A failed model, null test, review, transfer, deletion, or billing gate stops ACE, Revideo, B2, and Wan progression.

## 12. Decision and next experiments

Proceed to ACE-Step base `lego` only when the separate accompaniment is usable, null/QC pass, human connection and emotional lift pass, measured cost/runtime fit the continuation envelope, and deletion is verified.

Stop or reframe if the accompaniment is generic/unrelated, the source must be replaced to sound good, one bounded candidate cannot show meaningful lift, or handling/deletion cannot be proven. Do not rescue a failed audio thesis with a renderer or Wan.

If F1 passes, the order is:

1. ACE-Step 1.5 base `lego` as a separate instrument-layer comparison.
2. ACE `complete` only as a full-mix comparison; it does not inherit literal retention.
3. Revideo 15-second 720p repeatability/audio-sync/container benchmark, with FFmpeg/MoviePy fallback.
4. Private B2 upload/read/fetched-byte-hash/manifest/delete canary.
5. ACE `repaint` only after an accepted parent and locked-region replacement/hash verification.
6. Optional Wan 3–5 second replaceable interval after deterministic-stage success.

No step inherits an earlier evidence level.
