# StageMe Pre-Call Readiness Report

> **Current verdict:** **conditionally ready** for the first authorized call.
>
> **Checked:** 2026-07-27, primary mutable-source and policy pass completed 11:20 UTC; ACE artifact and storage-rate consistency pass completed 11:49 UTC; private F1 and RunPod CLI-contract refresh completed 17:12 UTC; fixture-scoped F1 rights affirmation and preflight refresh completed 17:28 UTC.
>
> **Repository baseline:** remote `main` at assignment start was `a8df5a9b46e2f427ae4192e6e0d2d8d9eac7399d`, newer than the supplied reference `5411be2b3d3ac2d381898edeedfb7ec08a85f198`.
>
> **Product authority:** `STAGEME_PRODUCT_SPEC.md`.

The zero-cost research, source inspection, dependency resolution, synthetic plumbing proof, consent/fixture preparation, preflight tooling, failure policy, and exact first-call procedure are ready. An owner-supplied F1 is preserved in a private local bundle, passes deterministic media QC plus a conservative pitch-bearing signal check, and has a fixture-scoped owner affirmation for authorized voice and absence of unauthorized backing media. The magical transformation is **not** ready to claim and the call still cannot start autonomously: the owner must approve a named GPU account/region and live offer, set a finite spend cap, and permit processing on that worker after the provider disclosure.

## 1. Decision-grade answer

The first real call should remain:

```text
authorized F1 rough sung phrase
→ deterministic 24 kHz mono float normalization
→ one AnyAccomp candidate at the pinned code/checkpoint revisions
→ separate accompaniment retained as its own asset
→ StageMe-owned 0.5 source + 0.5 accompaniment float premaster
→ sample-aligned null test
→ deterministic media QC
→ before/after human review
```

Proceed only if the generated accompaniment is audibly connected to F1, the source-subtraction proof passes, and the result feels meaningfully more finished. Infrastructure success is insufficient.

ACE-Step base `lego` is the next separate-layer comparison. `complete` is a full-mix comparison and does not inherit a source-retention claim. `repaint` waits for an accepted parent. Wan waits for accepted audio and a reliable deterministic stage.

The exact operator procedure is in [`STAGEME_FIRST_CALL_RUNBOOK.md`](STAGEME_FIRST_CALL_RUNBOOK.md). The under-five-minute user recording guide is in [`STAGEME_F1_RECORDING_CHECKLIST.md`](STAGEME_F1_RECORDING_CHECKLIST.md).

## 2. Evidence levels and readiness ledger

The capability-level column uses only the canonical six-level vocabulary. Execution outcome is a separate axis. Elsewhere, `[OFFICIAL]`, `[OBSERVED]`, `[INFERENCE]`, and `[OPEN]` describe source provenance—not capability maturity.

| Capability | Capability level | Execution/gate outcome | What the evidence proves | What it does not prove |
|---|---|---|---|---|
| AnyAccomp separate accompaniment | Implemented | Not run on F1 | Pinned source writes accompaniment separately | StageMe quality, latency, VRAM, reliability |
| AnyAccomp source addition | Implemented | Not run on F1 | Pinned source calculates raw mixture as accompaniment plus decoded source | Safe gain staging or a compelling mix |
| StageMe null-test plumbing | Implemented | Synthetic correct/wrong cases passed | The local verifier distinguishes retained and altered synthetic mixes | Human-source preservation through a model |
| ACE `lego` | Implemented | Not run | Base task accepts source context and writes a named instrument result | Quality or runtime on F1 |
| ACE `complete` | Implemented | Not run | Base task returns a generated complete output | Literal source passthrough |
| ACE `repaint` | Implemented | Not run; source caveats found | Time-bound source injection/splice exists for some modes | Locked-region identity without StageMe enforcement |
| Revideo package/build | Implemented | Build + one bundled smoke passed | Current source can build and render its bundled template | Repeatability, StageMe audio sync, container/deployment success |
| Revideo repeat render | Implemented | Gate failed twice | Current repeat path hits the frame-detachment failure | A production-safe renderer |
| Genblaze contracts | Implemented | Selected source tests passed | Current provider/storage/streaming contracts execute without live providers | A working StageMe provider |
| B2 path | Documented | Canary not run | Exact private-bucket, scoped-key, canary, integrity, and deletion design | Account/CORS/credentialed canary |
| Wan endpoint | Documented | Not called | Current official input schema, lifecycle, version, and price | Accepted 3–5 second result or Genblaze routing with credentials |
| F1 local fixture/QC | Reproduced | Private ingest, canonicalization, QC, pitch-bearing analysis, and fixture-scoped rights affirmation passed | The selected 14.256 s clip is technically usable, contains sustained pitched signal, and has the required owner rights attestations | Independent rights verification, subjective singing quality, provider consent, or model-output quality |
| StageMe retained-performance magic | Advertised | Not reproduced | The product promise and falsification gate are explicit | Any working or desirable transformation |

No media claim in this report is product-proven.

## 3. What was actually executed without user input

Research inspection is intentionally excluded from this execution list.

| Execution | Result | Evidence |
|---|---|---|
| Context validator before edits | Passed | Existing repository integrity was sound |
| AnyAccomp dependency resolution | Passed | Stock Python 3.9/Linux requirements resolved without installing model weights |
| QC environment install | Passed | Python 3.12.13 with NumPy 2.4.6, SciPy 1.17.1, SoundFile 0.14.0, librosa 0.11.0, pyloudnorm 0.2.0 |
| Synthetic F0 pitch/loudness plumbing | Passed | 10.0 s, 48 kHz mono; pYIN median 221.274 Hz for a 220 Hz tone; LUFS −42.019 |
| Synthetic F0 null test | Passed | 480,000 frames; max error `9.313225746e-10`; RMS error `2.913929974e-10`; correlation `0.9999999999999786`; error −149.636 dB relative |
| Intentional wrong/zero-gain null tests | Failed as required | Wrong source gain returned exit 2 and max error `0.006248475`; zero source gain was rejected with exit 2; proves fail-closed behavior |
| StageMe script tests in QC environment | Passed | 32/32 tests, including project/media binding, exact ACE model revision, B2 prefix, provider-native absolute-deadline/cap math, relative/stale deadline rejection, zero-source-gain, canonical-format, and worker-source regressions |
| StageMe script tests in system environment | Passed with expected optional skips | 27 passed, 5 null-test cases skipped because QC dependencies are isolated |
| Embedded runbook media-QC gate | Passed/fail-closed on synthetic audio | Valid 24 kHz source/accompaniment/premaster passed; a silent accompaniment exited nonzero and recorded three exact failures |
| Runbook shell/Python syntax | Passed | 26 Bash fences and 15 embedded Python programs parsed successfully; syntax is not paid-worker reproduction |
| Revideo canonical build | Passed | 10 projects built with telemetry disabled |
| Revideo smoke render | Passed once | 7.433 s, 1080×1080, 30 fps H.264/AAC; 11.42 s wall; ~446 MiB max RSS |
| Revideo immediate rerenders | Failed twice | Node 25 and supported Node 22.12 both hit `Navigating frame was detached` |
| Genblaze selected source tests | Passed | 210 passed, 3 skipped; separate clean-room evidence also records 388 core + 26 S3 passes |
| Official multi-provider sample | Passed selected checks | pnpm 10.32.1 frozen install, Next 16.1.6 build, TypeScript check |
| Owner F1 local ingest and canonicalization | Passed | Immutable source copy retained outside Git; deterministic selected segment and 24 kHz mono float32 derivative are separately hashed; no gain, denoise, pitch correction, or external transfer |
| Owner F1 media and pitch-bearing checks | Passed | 14.256 s; no clipping/non-finite samples; 735/1,329 high-confidence pitched frames, 166.73 Hz median robust F0, 8.5-semitone robust span; evidence remains in the private bundle |
| RunPod CLI install/contract check | Passed locally; account gate closed | Checksum-pinned Homebrew `runpodctl` 2.7.2 installed; binary help reproduced absolute-datetime `--terminate-after`; unauthenticated inventory failed cleanly because no API key is configured |

Provider calls made: **none**. Local human-audio selection, canonicalization, media QC, and pitch-bearing analysis occurred with the owner's supplied recording. No media upload, model inference, paid API, usable credential, B2 request, public deployment, or oversized checkpoint download occurred.

## 4. Track A — AnyAccomp

### Verified identity, environment, and artifacts

- **[OBSERVED]** Code: [`AmphionTeam/AnyAccomp@82604b5`](https://github.com/AmphionTeam/AnyAccomp/commit/82604b5e3107944ad4c49fc64900b86118ae2c62), MIT, no releases.
- **[OBSERVED]** Checkpoints: [`amphion/anyaccomp@9aa9e62`](https://huggingface.co/amphion/anyaccomp/tree/9aa9e62427337bf1df4caa3c4f3e6ad934522e71), CC BY 4.0.
- **[OBSERVED] Capability level: documented.** Environment: Python 3.9, FFmpeg 4.x, Torch/Torchaudio 2.3.1, Torchvision 0.18.1, CUDA 12.1 packages. Linux/NVIDIA is the safest unmodified target.
- **[OBSERVED] Capability level: implemented.** Inputs are WAV, MP3, or FLAC; Gradio accepts 3–30 seconds; source is decoded/resampled to 24 kHz mono without explicit peak/loudness normalization.
- **[OBSERVED] Capability level: implemented.** Defaults are 50 steps, CFG 3, seed 1024, CUDA.
- **[OPEN]** No official VRAM, RAM, latency, or CPU benchmark exists. CUDA-specific operations make the apparent CPU flag untrusted.
- **[OBSERVED]** No Dockerfile exists.
- **[OBSERVED] Reachability check.** The official Hugging Face Space is currently `CONFIG_ERROR` because its Torch version is unsupported by ZeroGPU. No official maintained hosted inference mapping was found.

| Checkpoint | Bytes | SHA-256 |
|---|---:|---|
| `pretrained/flow_matching/pytorch_model.bin` | 880,790,586 | `e6802bd1123935a54e990cb8d3897a18190df6c53f73db021baa28c420721129` |
| `pretrained/vocoder/model.safetensors` | 1,020,206,416 | `1b7efd04c71c058cd00b4e9a91c761b31da745f878b7d7ee839e157104d3a7da` |
| `pretrained/vq/pytorch_model.bin` | 177,202,134 | `9d7f48cefea30602b2148c057faf14ecad168184e8063c8377dd57f208dc65fc` |

Total: 2,078,199,136 bytes / 1.935 GiB. No individual file exceeds the assignment's 2 GB approval boundary, but they were deliberately not downloaded to a non-GPU Mac merely to claim acquisition.

### Important installation and trust boundaries

- The current model repository stores weights under `pretrained/...`; the upstream README's `local_dir='./pretrained'` snapshot command would create `pretrained/pretrained/...`. The runbook corrects this by downloading the pinned `pretrained/*` tree into the repository root and then verifying every hash.
- The code adds source and accompaniment directly without a headroom or mastering policy. StageMe ignores that raw mixture for acceptance and performs its own recorded float mix.
- Python 3.9 for AnyAccomp conflicts with Genblaze's Python 3.11+ requirement. The model must run in a dedicated environment/container, never imported into FastAPI.
- Attribution must name AnyAccomp/authors, link the model and CC BY 4.0, preserve notices, state modifications, and include the paper citation. The reported in-the-wild/source-separated training corpus is not documented well enough for an independent commercial-risk conclusion.

Recommendation: one direct worker run first, 24 GB Ampere/Ada or larger as risk control, one seed, one candidate, 30-minute inference stop, no silent retry.

## 5. Track B — ACE-Step 1.5

- **[OBSERVED]** Current main: [`6d467e4`](https://github.com/ace-step/ACE-Step-1.5/commit/6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0).
- **[OBSERVED]** Latest release: [`v0.1.8`](https://github.com/ace-step/ACE-Step-1.5/releases/tag/v0.1.8), tag commit `dce621408bee8c31b4fcf4811682eb9359e1bc94`; package declares 1.5.0.
- **[OBSERVED]** Immutable model state checked 2026-07-27 11:49:07 UTC: model-card/main snapshot [`ACE-Step/Ace-Step1.5@19671f406d603126926c1b7e2adc169acbcade22`](https://huggingface.co/ACE-Step/Ace-Step1.5/tree/19671f406d603126926c1b7e2adc169acbcade22); base snapshot [`ACE-Step/acestep-v15-base@e432212fec32b8965a14ffa57ae653438d6abd14`](https://huggingface.co/ACE-Step/acestep-v15-base/tree/e432212fec32b8965a14ffa57ae653438d6abd14). Base `model.safetensors` is 4,787,825,604 bytes with SHA-256 `4177f600501a6d4bd81cadaa0abac557ffd15c54e5c8cb52053cdb24a0844d6b`.
- **[OBSERVED] Capability level: documented.** ACE code/model cards declare MIT; Qwen3-derived components originate under Apache 2.0. Preserve both notices. Commercial-use/training-data statements remain author claims, not a legal audit.
- **[OBSERVED] Capability level: documented.** Python 3.11–3.12; Linux x86-64 pins Torch 2.10/CUDA 12.8; official Docker uses Ubuntu 22.04/CUDA 12.8.1.
- **[OBSERVED]** The five major tensor weights total 14,813,190,540 bytes / 13.796 GiB. The complete pinned main and base snapshots total 14,883,895,000 bytes / 13.862 GiB, including configs and auxiliary files. The base DiT alone is 4,787,825,604 bytes and therefore was not downloaded without approval.
- **[OBSERVED] Capability level: implemented.** Base supports `lego`, `complete`, and `repaint`. Turbo does not support `lego` or `complete`; turbo latency must not be applied to them.
- **[OBSERVED] Reachability check.** Official Space is running turbo/XL-turbo only; no official maintained hosted base-task endpoint or Hugging Face provider mapping was found.
- **[INFERENCE]** A 24 GB Ampere/Ada worker is a conservative first-experiment risk control, not a measured minimum.

### Task semantics and hazards

| Task | Output meaning | StageMe decision |
|---|---|---|
| `lego` | One requested instrument track conditioned on source | First ACE comparison; mix with immutable performer stem |
| `complete` | One generated complete output | Full-mix comparison only |
| `repaint` | Time-bounded generation/source injection | Only after parent acceptance; never repaint performer stem |

Current-main caveats:

- documentation says `complete` requires source audio, while current source validation omits it;
- `complete` does not lock duration to the source;
- explicit crossfade request fields are accepted but recomputed from mode/strength;
- repaint can truncate to the shorter length and retain a generated tail;
- outside-region source splice applies only in non-aggressive modes.

StageMe must independently replace locked accompaniment regions with parent bytes/samples and then hash/null-test them.

The official REST lifecycle is `POST /release_task` → `POST /query_result` with `task_id_list` → `GET /v1/audio?path=...`. Status values are 0 pending, 1 success, 2 failure. Job state is in memory, unknown IDs appear pending, no cancellation endpoint exists, and the 600-second request timeout may leave CUDA work running. The Genblaze adapter therefore needs its own durable state, missing/TTL policy, origin allowlist, bounded polling, process-level termination, and guarded retries.

### Pinned later-call request contracts

These are **implemented-source contracts, not executed requests**. Use multipart upload so the service creates its own temporary source path; set `batch_size=1`, a fixed seed, base model, and `wav32`. The first ACE comparison is `lego`:

```text
POST /release_task multipart/form-data
src_audio=@F1-24k-mono-f32.wav
task_type=lego
model=acestep-v15-base
instruction=Generate the instrumental accompaniment track based on the source audio context:
track_name=instrumental accompaniment
repainting_start=0
repainting_end=-1
thinking=false
inference_steps=50
guidance_scale=7
use_random_seed=false
seed=<recorded integer>
batch_size=1
audio_format=wav32
```

The separate `complete` comparison changes `task_type=complete` and uses `instruction=Complete the input with drums, bass, harmony, and accompaniment:`. It returns a generated complete output; do not represent it as source passthrough. Current source does not reliably lock `complete` duration to the source, so measure and reject a mismatch.

Only after an accepted accompaniment parent, a bounded `repaint` request uses that accompaniment—not the immutable performer stem—with `task_type=repaint`, `model=acestep-v15-base`, `chunk_mask_mode=explicit`, explicit `repainting_start`/`repainting_end`, `repaint_mode=conservative`, recorded crossfade fields, a fixed seed, and `batch_size=1`. Current comments disagree about the direction of `repaint_strength`; conservative mode avoids relying on that ambiguous field until a credentialed source test resolves it. StageMe then restores parent samples outside the authorized interval plus explicit crossfade margins and verifies them byte/sample-wise.

Poll with `POST /query_result` and JSON `{"task_id_list":["<id>"]}`. Parse the successful `result` JSON string, allowlist the returned relative `/v1/audio?path=...` URL, fetch it once, hash it, and reject unknown IDs/TTL expiry instead of polling forever. There is no reliable cancellation endpoint; terminate the isolated worker process on timeout and resolve any billable orphan before retrying.

## 6. Track C — audio/QC support stack

The reproducible StageMe control/QC target is Python 3.11 or 3.12. The following Python 3.11-compatible pins resolved and installed together in an isolated environment.

| Dependency | Pin | License boundary | Purpose | Decision / risk |
|---|---:|---|---|---|
| FFmpeg/ffprobe | deploy build TBD; local 8.1.1 | LGPL/GPL depends on build/options | decode, resample, mix, inspect, encode | Adopt; pin binary/config. Local Homebrew build enables GPL codecs and is not an automatic redistribution choice |
| NumPy | 2.4.6 | BSD-3-Clause core; bundled notices apply | arrays, hashes/QC math, null testing | Adopt. PyPI 2.5.1 requires Python ≥3.12, so do not float latest on 3.11 |
| SciPy | 1.17.1 | BSD-3-Clause plus bundled notices | signal utilities where librosa requires them | Adopt transitively; avoid unnecessary DSP |
| SoundFile | 0.14.0 | BSD-3-Clause; libsndfile boundary | lossless float WAV/FLAC I/O | Adopt; record libsndfile build/version |
| librosa | 0.11.0 | ISC | RMS, onset, beat, chroma/pYIN | Adopt for analysis; output is an estimate, not musical truth |
| pyloudnorm | 0.2.0 | MIT | integrated loudness measurement | Adopt for QC; do not force short clips to a broadcast target |
| python-audio-separator | 0.44.5 | MIT wrapper; each model separate | diagnose/recover stems if genuinely needed | Defer; not an arranger and adds weights/licenses |
| OpenAI Whisper | 20250625 | MIT code; model artifact must be recorded | optional transcript hint | Defer until lyric timing proves useful; singing accuracy unproven |
| WhisperX | 3.8.6 | BSD-2-Clause wrapper; alignment models separate | optional word alignment | Defer; model/access/runtime overhead |
| `hashlib` | Python standard library | PSF | SHA-256 | Adopt |

Current relevant repository pins and purposes are recorded in `repositories.json`. Newly inspected heads include NumPy `25c89980fcffe59af8ac12b39cf41bd4b07d09ce`, SciPy `e0134f43e13f376a59d9aabaf7c193403131c8f9`, SoundFile `350394191a2af890fc464d0f11a1690e7a4f4c64`, and FFmpeg `a757b708ae7d43fdec89545a55cbc11ae2967b19`.

The synthetic pitch test produced 261 onset detections on a steady tone, a useful warning that feature plumbing can pass while musical interpretation is wrong.

## 7. Track D — deterministic renderer

### Revideo current result

- **[OBSERVED]** Current main `b5de67a009a55aa2768a1e178b0446b2479a0b4e`; npm `@revideo/*` 0.11.0; tag peeled commit `73479d620d151792edfee45cca32395fd1b60b94`; MIT.
- **[OBSERVED] Capability level: implemented.** `renderVideo({projectFile, variables, settings})` is the headless entrypoint.
- **[OBSERVED] Capability level: implemented.** Node requirement is `>=22.12.0`; repository `.nvmrc` is 22; Puppeteer 25.3.0 fetched Chrome/headless shell 150.0.7871.24.
- **[OBSERVED] Capability level: implemented.** Telemetry goes to PostHog EU; disable with `DISABLE_TELEMETRY=true`.
- **[OBSERVED] Smoke outcome.** The canonical build and one bundled-template render passed; this is not a StageMe representative-fixture reproduction.
- **[OBSERVED] Gate outcome: failed.** Two immediate rerenders failed with `Navigating frame was detached`, matching [open issue #343](https://github.com/midrender/revideo/issues/343) and the current source's forced Chromium `--single-process` flag.
- **[INFERENCE] Capability level: advertised.** Cloud Run is described, but the official linked example is missing; deployment is not reproduced.

Revideo remains the intended architecture, not the immediate reliable fallback. Before promotion it must render a local-font/local-audio 15-second 1280×720, 30 fps StageRenderSpec three consecutive cold and warm times, within one-frame A/V sync, with frame/PCM repeat checks, pinned browser/fonts/FFmpeg/container, measured RSS/temp disk, telemetry disabled, and successful container/deployment cleanup.

Inject precomputed beat, onset, RMS/energy, phrase, palette, camera, lighting, and seed values through `variables`; do no live music analysis inside Chromium. Use MoviePy 2.2.1 or direct FFmpeg as the Phase-0 fallback. Motion Canvas is a design alternative, PixiJS/Meyda are preview-only, and wavesurfer.js 7.12.11 is for capture/playback/region selection.

## 8. Track E — optional Wan S2V

- **[OBSERVED]** Endpoint: [`wan-video/wan-2.2-s2v`](https://replicate.com/wan-video/wan-2.2-s2v).
- **[OBSERVED]** Public current version: `09607e6e761d2f015b0d740f938ec59199f54aa623384465a5054b230405acf4`.
- **[OBSERVED] Capability level: documented.** Exact current schema requires `prompt`, `image`, and `audio`; optional `seed`; `num_frames_per_chunk` defaults 81 and allows 1–121; output is one URI.
- **[OPEN]** Exhaustive codec/container list and maximum accepted audio duration are not published.
- **[OBSERVED]** Generic `/api` currently hydrates a different `3e660c83…` schema with `interpolate`; the exact latest-version page does not. Revalidate and record the returned version immediately before payment.
- **[OBSERVED]** Price is $0.02 per output-video second.
- **[OBSERVED] Capability level: documented.** Statuses are `starting`, `processing`, `succeeded`, `canceled`, `failed`; async polling is preferred; `Cancel-After` accepts 5 seconds through 24 hours.
- **[OBSERVED]** Public examples show 112–531 second prediction times, not an SLA.
- **[OBSERVED] Data handling.** API-created prediction inputs, outputs, files, values, and logs are removed after one hour by default; web-created prediction data is retained indefinitely. Use only the API and explicitly delete/copy according to consent.
- **[OBSERVED]** Upstream Wan2.2 commit `42bf4cfaa384bc21833865abc2f9e6c0e67233dc`, Apache 2.0.

Genblaze's Replicate connector implements submit/poll/fetch and URL validation, but a credentialed preflight must confirm which versioned submission route it selects. Its generic output-second pricing helper cannot calculate this endpoint automatically because the returned asset lacks duration; use input-audio duration as a pre-call estimate and reconcile with `ffprobe` output duration.

Fixed StageMe boundary: one replaceable 3–5 second silhouette, sculpture, instrument, or abstract interval. Failure/timeout/drift/rejection restores the deterministic interval.

The endpoint/model license makes the caller responsible for avoiding unlawful/harmful uses, harmful personal-information disclosure, misinformation, and targeting vulnerable people. Replicate's published retention page does not prove that customer inputs are excluded from every training/resultant-data use; re-read the then-current terms and obtain specific performer approval before sending voice-bearing audio. StageMe's default remains `training_reuse=false`, and Wan stays optional if that boundary is unacceptable.

Calculated with Node using `candidates × seconds × 0.02`:

| Output duration | One candidate | Two candidates |
|---:|---:|---:|
| 3 s | $0.06 | $0.12 |
| 4 s | $0.08 | $0.16 |
| 5 s | $0.10 | $0.20 |

## 9. Track F — Genblaze

- **[OFFICIAL]** Current repository: [`backblaze-labs/genblaze@293bead`](https://github.com/backblaze-labs/genblaze/tree/293beade3e705d69b29dbf57402800f8a868313f), MIT; release v0.6.0 published 2026-07-22.
- **[OBSERVED]** Current independent packages are `genblaze==0.4.4`, `genblaze-core==0.3.7`, `genblaze-s3==0.3.6`, `genblaze-cli==0.3.5`; Python ≥3.11. Do not call every distribution “0.6.0.”
- **[OBSERVED] Capability level: implemented.** Provider discovery uses Python entry points in group `genblaze.providers`.
- **[OBSERVED] Capability level: implemented.** `BaseProvider` owns `submit`, `poll`, `fetch_output`, `invoke/ainvoke`, and `resume/aresume`; it checkpoints an external prediction ID after submit.
- **[OBSERVED] Capability level: implemented.** `SyncProvider.generate()` uses an in-memory `sync` ID. `asyncio.to_thread` prevents event-loop blocking but does not create durability.
- **[OBSERVED] Capability level: implemented.** Capabilities declare modality/input/chain/duration/resolution/format/model support. Provider outputs require absolute HTTPS URLs; `file://` inputs require canonical allowlisted roots.
- **[OBSERVED] Capability level: implemented.** Typed errors include timeout, rate limit, auth, invalid input, model, server, content policy, unknown. Defaults retry only timeout/rate/server.
- **[OBSERVED] Capability level: implemented.** Pricing is model/family strategy-based; prices must be refreshed.
- **[OBSERVED] Capability level: implemented.** Pipeline emits typed progress events; the app, not Genblaze, serializes them as SSE. Breaking sync iteration does not cancel the worker.
- **[OBSERVED]** Current `ProviderComplianceTests` has 16 methods although some docs say 15.

`FFmpegCompositorProvider` stream-copies one video plus one audio. It does not mix stems, render StageMe, or prove retention.

`ObjectStorageSink` downloads assets, computes hashes/metadata, uploads to B2/S3, rewrites durable credential-free URLs, and writes a manifest. Writable manifest schema is 1.5; 1.6 is read-supported. `Manifest.verify()` does not fetch remote bytes, and canonical hashes exclude transport URLs plus `parent_run_id`; StageMe must still bind lineage and perform fetched-byte verification.

Exact adapter boundary:

```text
packages/genblaze-anyaccomp/
  pyproject.toml
  genblaze_anyaccomp/{__init__.py,provider.py,_errors.py,py.typed}
  tests/{test_compliance.py,test_provider.py}

packages/genblaze-acestep/
  pyproject.toml
  genblaze_acestep/{__init__.py,provider.py,_errors.py,py.typed}
  tests/{test_compliance.py,test_provider.py}
```

AnyAccomp may be a `SyncProvider` only inside the dedicated GPU worker with durable outer job state. A queued/hosted AnyAccomp is a real `BaseProvider`. ACE is always a real `BaseProvider` over its release/query/audio lifecycle. Direct inference semantics must be reproduced before either adapter is promoted.

The official multi-provider sample is an architecture reference only. Pin pnpm 10.32.1: the repository allows Node ≥20 and pnpm ≥9 but has no `packageManager`; current pnpm 11.17 requires Node ≥22.13 and can break valid Node 20 installations.

## 10. Track G — Backblaze B2

### Configuration and least privilege

Recommended production path is `boto3==1.43.56` (Apache 2.0, Python ≥3.10) against the TLS endpoint pattern `s3.REGION.backblazeb2.com`; optional native SDK is `b2sdk==2.12.0` (MIT, Python ≥3.10).

Use a standard application key—not the master key—restricted to one private bucket and the exact StageMe prefix. The canary needs `readFiles`, `writeFiles`, `deleteFiles`, and `listAllBucketNames`; add `listFiles` only for a list-based test.

- Presigned GET and PUT are supported; browser presigned POST is not.
- Allow only the production origin and required PUT/GET/HEAD methods/headers in CORS. CORS is not authorization.
- Single S3 upload maximum is 5 GB; StageMe objects should use one PUT. A 64 MiB app multipart threshold is a recommendation.
- Filename plus metadata limit is 7,000 bytes, or 2,048 with SSE/Object Lock. Keep only IDs, SHA-256, media type, and lineage pointer in metadata; full details live in JSON manifests.
- Do not treat ETag as SHA-256. Fetch all bytes and recompute.
- Buckets are always versioned. Record `VersionId`/native `fileId`; name-only deletion can leave older versions.
- Do not enable Object Lock on the MVP/test bucket; it can make the user's deletion promise impossible.
- Lifecycle processing is approximately daily with a one-day boundary. Current S3 lifecycle API docs conflict with an older official page; use the newer API and one management surface.
- Event Notifications require Support enablement, are at-least-once, and are not an MVP dependency.

Prepared credentialed canary:

```text
PutObject synthetic artifact                 Class A
HeadObject                                  Class B
GetObject + SHA-256                         Class B
PutObject manifest                          Class A
GetObject manifest + SHA-256                Class B
DeleteObject artifact exact version         Class A
DeleteObject manifest exact version         Class A
optional HeadObject ×2 for confirmed 404     Class B ×2
```

Base requests: A=4, B=3; with delete verification: A=4, B=5. It remains unexecuted because no credential use or B2 write was authorized.

Current pricing source says $6.95/TB/30-day (about $0.00695/GB-month), first 10 GB stored free, up to 3× average monthly storage egress free, then $0.01/GB. Classes A/B/C are free; Class D first 2,500/day free then $0.004/10,000. The transaction page still shows stale $0.005/GB-month; the current main pricing page controls the budget.

```text
storage = max(0, average_stored_GB - 10) × 0.00695
egress  = max(0, downloaded_GB - 3 × average_stored_GB) × 0.01
```

## 11. Track H — GPU/hosting comparison

| Option | Current published price | Scale/cache/data facts | Account/access conclusion |
|---|---|---|---|
| RunPod Pod | A40 48 GB $0.44/h; A6000 48 GB $0.53/h; L40S 48 GB $0.99/h; A100 80 GB $1.39/h; H100 80 GB $2.89/h | Per-second; custom Docker/secrets; no auto scale-to-zero for Pods; B2 documented; terminate to stop compute/storage | Best first interactive experiment. Requires balance covering one hour; credits begin at $10 and are non-refundable. Nigeria/card acceptance unresolved |
| Modal | L40S $1.9512/h; A100 40 GB $2.0988/h; A100 80 GB $2.4984/h; H100 $3.9492/h, plus CPU/RAM | Per-second, no minimum; zero containers by default; images/secrets/volumes; public outbound B2 path | Best serverless follow-on. Payment method and Nigeria acceptance unresolved; do not count advertised credits yet |
| Vast.ai | Live marketplace price unavailable without authenticated search | Per-second; custom Docker; serverless scale; storage/bandwidth host-specific; data risk at zero credits | Contingency only; capture a verified/secure offer first; $5 minimum deposit |
| Lambda Cloud | A6000 48 GB $1.09/h; A100 40 GB $1.99/h; H100 80 GB $3.29–$4.29/h | One-minute billing; no suspend/scale-to-zero; terminate to stop; local data destroyed | No-go for a Nigeria-billed account unless Lambda confirms support; Nigeria absent from official purchase-region list |

For Modal L40S + four physical cores + 32 GiB RAM:

```text
cost/second = GPU + 4×0.0000131 + 32×0.00000222
            = $0.00066544
cost/hour   = $2.395584
```

Live secure inventory, exact region, cold start, cache behavior, outbound B2 canary, secrets/deletion, and Nigeria payment acceptance remain first-use checks.

**[OBSERVED] RunPod cache-rate source:** the [RunPod Storage options page](https://docs.runpod.io/pods/storage/types), checked 2026-07-27 11:49:07 UTC, lists volume disk at $0.10/GB-month while a Pod is running and $0.20/GB-month while stopped. Therefore the expected cache row is `50 GB × $0.10 × 1/30 = $0.1667`, and the high row is `100 GB × $0.20 × 1/30 = $0.6667`. These are storage-only estimates; provider billing remains mutable.

**[OBSERVED] Hard-cap control and documentation conflict:** the [RunPod prose CLI reference](https://docs.runpod.io/runpodctl/reference/runpodctl-pod) describes relative duration examples such as `1h`, but the checksum-pinned [`runpodctl` v2.7.2 release](https://github.com/runpod/runpodctl/releases/tag/v2.7.2), installed and checked at 17:12 UTC, reports `--terminate-after` as an absolute datetime and its pinned [source at commit `309512b`](https://github.com/runpod/runpodctl/blob/309512b4926eb7d218bbc8a8f11d380ce54f59c4/cmd/pod/create.go) passes that string unchanged to the API. The runbook now forbids `${hours}h`, calculates a fresh RFC 3339 UTC deadline immediately before creation, records CLI version and semantics, and explicitly requests Secure Cloud plus one approved data-center ID. Because v2.7.2 `pod create`/`pod get` output does not return the configured deadline, the operator must confirm the exact timestamp in the authenticated console before F1 transfer. The budget still uses `rate × declared maximum hours + noncompute reserve ≤ owner-approved cap`, followed by immediate deletion after verified copy-out.

**[OBSERVED] Provider-processing disclosure:** the [RunPod Terms of Service](https://www.runpod.io/legal/terms-of-service), last updated 2026-03-24 and checked 2026-07-27 17:12 UTC, say the customer retains ownership but grants RunPod access/use needed to provide the service and permits aggregated/anonymized use for improvement; the customer is responsible for content permissions and application/data security. The [security page](https://docs.runpod.io/references/security-and-compliance) describes container isolation and enhanced Secure Cloud controls. These terms are not silently accepted by this research pass and must be disclosed with the exact region and deletion plan before performer consent.

## 12. Cost and time envelope

No model runtime is measured. These are hard-planning envelopes, not predictions:

```text
GPU = hourly_rate × billed_seconds / 3600
cache = GB × monthly_rate × retained_days / 30
Wan = candidates × output_seconds × 0.02
B2 = storage formula + egress formula + applicable Class D requests
```

| Item | Low: RunPod A40 | Expected: RunPod A100 80 GB | High: RunPod H100 80 GB |
|---|---:|---:|---:|
| Setup/download | 20m / $0.1467 | 45m / $1.0425 | 90m / $4.3350 |
| AnyAccomp F1 | 10m / $0.0733 | 20m / $0.4633 | 30m / $1.4450 |
| ACE `lego` | 8m / $0.0587 | 15m / $0.3475 | 30m / $1.4450 |
| ACE `complete` | 8m / $0.0587 | 15m / $0.3475 | 30m / $1.4450 |
| Bounded revision | 8m / $0.0587 | 15m / $0.3475 | 30m / $1.4450 |
| Deterministic render | 6m / $0.0440 | 10m / $0.2317 | 15m / $0.7225 |
| Retry reserve | 0m / $0 | 30m / $0.6950 | 75m / $3.6125 |
| GPU subtotal | **$0.44** | **$3.475** | **$14.45** |
| Cache | $0 | 50 GB running 1d / $0.1667 | 100 GB stopped 1d / $0.6667 |
| Optional Wan | one 3s / $0.06 | two 4s / $0.16 | two 5s / $0.20 |
| B2 nominal in free pools | $0 | $0 | $0 |
| Calculated total | **$0.50** | **$3.8017** | **$15.3167** |

The low case assumes compatible cached images and that both models fit 48 GB. RunPod still requires an initial account credit purchase even when actual compute is lower. Replace every time range with measured cold/warm data after the first session.

## 13. F1 fixture, consent, and handling

**Current local status, 2026-07-27:** an owner-supplied M4A was copied into an owner-only private bundle before the temporary macOS share path expired. A deterministic 14.256-second selection and 24 kHz mono float32 derivative passed byte/hash, decode, duration, clipping, silence, non-finite, DC, loudness, and reproducibility checks. Conservative pYIN analysis found two phrase-like pitched regions and supports only the statement “pitch-bearing rough-vocal candidate.” [OBSERVED] At 17:26:55 UTC, the owner affirmatively answered the exact fixture-scoped statement that F1 contains only authorized voice and no copyrighted or otherwise unauthorized backing audio; the private record expressly does not authorize provider upload, payment, B2, publication, or training reuse. Waveform analysis still cannot independently prove rights, absence of backing audio, singing quality, or expected AnyAccomp quality. No media, private path, or media hash is committed to Git.

Required fixture:

- one 8–15 second rough sung phrase, one user-owned voice;
- dry voice only, no instrumental, copyrighted backing, second person, speaker playback, or synthetic/celebrity voice;
- ordinary phone mic 15–25 cm away, quiet soft-furnished room, notifications off, no clipping;
- WAV/FLAC preferred; M4A/MP3/WebM/OGG/Opus accepted for ingest;
- no denoise, autotune, pitch correction, time stretch, reverb, normalization, or manual trimming before ingest;
- consent binds the exact project, original-byte hash, canonical derivative hash/command/FFmpeg evidence, model/checkpoint, provider/region, spend cap, purpose, retention, deletion, and `training_reuse=false`;
- a separate budget plan binds the live rate snapshot, immutable worker image, provider-native hard termination deadline, and noncompute reserve; worst-case compute plus reserve must fit the approved cap.

The first RunPod path would process F1 on the named secure GPU Pod, copy the verified result to a user-controlled local destination, and delete/terminate the worker. Private B2 is added only after its canary passes and storage is authorized.

## 14. Concrete failure and fallback table

| Failure | Detection/evidence | Retry policy | Fallback and user wording | Decision |
|---|---|---|---|---|
| Dependency install | nonzero install/import/CUDA smoke; freeze/log | 1 clean rebuild | “The model worker could not be prepared.” Preserve log | Stop |
| Checkpoint download/hash | missing size or SHA mismatch | 1 fresh verified download | no alternate/mirror without recording source | Stop |
| Insufficient VRAM | CUDA OOM + GPU telemetry | 0 on same shape | move once to larger approved Ampere/Ada worker | Stop until approved |
| CUDA mismatch | import/kernel/driver error | 1 pinned image rebuild | use recorded compatible image | Stop |
| Malformed input | ffprobe/decode/duration failure | 0 | “This file cannot be read; please record again.” | Stop |
| Silent input | RMS/peak/voicing gate | 0 | “We could not hear a usable sung phrase.” | Stop |
| Clipped input | repeated near-full-scale samples/astats | 0 | “The recording is distorted; move back and retry.” | Stop |
| Melody-following failure | blinded F1 connection review | 0 initial; one model comparison later | ACE `lego`; do not hide with visuals | Kill/reframe if repeated |
| Generic accompaniment | human rubric + pitch/rhythm features | 0 initial | ACE `lego` comparison | Kill/reframe if repeated |
| Source suppression/replacement | null test or source audibility fails | 0 | reject candidate; immutable source remains | Stop claim |
| Destructive doubling | listening/correlation/phase inspection | 0 | separate-layer remix; otherwise reject | Stop candidate |
| Timing drift | duration/alignment/onset comparison | 0 | deterministic trim only if causally justified | Stop candidate |
| Repaint changes locks | outside-window byte/sample/hash diff | 0 | overwrite from parent and reverify; reject if seam bad | Stop revision |
| Candidate fishing | requested count > budget | none | one candidate, explicit later approval | Stop |
| Provider timeout | durable state + wall-clock stop | max 1 only if no billable orphan | source-only rollback | Stop until orphan cleared |
| Auth/entitlement | 401/403/account UI | 0 | owner fixes account or choose approved provider | Human blocker |
| B2 presign/CORS | browser/API error + server logs | 1 configuration correction | API proxy/local evidence; no fake storage claim | Stop B2 promotion |
| B2 hash mismatch | fetched SHA differs | 1 new immutable key | quarantine/delete exact failed version | Stop |
| B2 deletion failure | version still heads/reads | 0 blind retries | surface retention incident; exact-version cleanup | Stop/privacy incident |
| Revideo drift/crash | repeat benchmark/frame/PCM hashes | 0 production retry until fixed | FFmpeg/MoviePy deterministic stage | Reframe renderer |
| Chromium/font mismatch | browser/font hashes or screenshot drift | rebuild once from pin | bundled fallback fonts/renderer | Stop Revideo |
| Wan rejection/drift | status/QC/human reject | max candidates in approved budget | deterministic interval restored | Continue core |
| Cost overrun | preflight rejects `rate × hard deadline + reserve > cap`; provider-native expiry; final settled charge comparison | none | immediate Pod deletion, source-only rollback, record violation | Stop |
| Consent gap | missing/contradictory consent field | none | do not upload/process | Stop |
| Provenance gap | asset/config/hash missing | none | artifact remains experimental, not accepted | Stop acceptance |
| Demo network failure | pre-demo fetch/play check | no generation retry | cached accepted local/B2 asset and deterministic video | Continue demo |

## 15. Go/no-go decision

### Go to the first authorized call when

- F1 and project-bound signed/affirmed consent are present outside Git;
- RunPod confirms account, region, secure inventory, an immutable worker image, live rate, owner cap, and provider-side `--terminate-after` whose worst-case charge plus reserve fits that cap;
- the local media/consent/budget binding phase and worker preflight pass with stock Python 3.9, CUDA, disk/RAM, exact code/checkpoints, and no secrets printed;
- the owner accepts the processing and deletion boundary.

### No-go or reframe after the call when

- the separate accompaniment does not follow the rough performance enough to be perceptible;
- source retention cannot be proven mechanically and heard clearly;
- acceptable output requires replacing the performer's source;
- one bounded candidate cannot show emotional lift;
- runtime/cost or privacy is outside the approved envelope.

Do not build the broad app or use polished visuals to defer this decision.

## 16. Remaining human/credential blockers

| Blocker | Why autonomous work stops | Exact human action |
|---|---|---|
| Consent | Provider processing and retention require the performer's decision | Complete the project/file-bound consent record after provider/region is selected |
| GPU account/entitlement | Registration, payment, region, and secure inventory are external | Confirm RunPod account/payment works and select a secure Ampere/Ada 24 GB+ offer |
| Budget | Any GPU run spends money and RunPod credits are non-refundable | Approve a live rate, hard provider deadline, noncompute reserve, and first-session cap; recommended expected cap is $5 after funding terms are understood |
| B2 canary credentials | A real write/delete needs scoped private credentials | Later provide presence of a scoped canary key/bucket through a secret store, never chat/Git |
| ACE base weights | Required checkpoint is individually >2 GB | Approve download only after AnyAccomp result justifies comparison |
| Wan | Paid, optional, schema mutable | No action until accepted audio and deterministic stage exist |

Only the first three are required to press the first AnyAccomp button. B2, ACE, and Wan are later gates.

## 17. Recommendation and what would change it

**Recommendation:** approve one capped RunPod Secure Cloud session using the first-call runbook, not a product build. Use AnyAccomp first; evaluate the actual transformation before Genblaze adapter work, ACE downloads, B2 human-media storage, or Wan.

**Confidence:** high that the experiment is operationally prepared; low-to-moderate that AnyAccomp will create a magical result because no representative output, VRAM, latency, or repeatability has been measured.

Change the recommendation if:

- live secure inventory or Nigeria payment access fails;
- AnyAccomp checkpoint/license terms become unacceptable;
- a maintained authorized hosted AnyAccomp endpoint appears with a clearer privacy/cost boundary;
- a zero-cost authorized direct artifact already proves/falsifies the same F1 operation;
- the owner declines processing F1 on a third-party GPU.

## 18. Primary mutable sources

Every source below was rechecked on 2026-07-27; exact detailed pins also live in `../10-sources/SOURCE_LEDGER.md` and `repositories.json`.

- [AnyAccomp repository](https://github.com/AmphionTeam/AnyAccomp) and [checkpoint model](https://huggingface.co/amphion/anyaccomp)
- [ACE-Step 1.5 repository](https://github.com/ace-step/ACE-Step-1.5), [inference tasks](https://github.com/ace-step/ACE-Step-1.5/blob/6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0/docs/en/INFERENCE.md), [API](https://github.com/ace-step/ACE-Step-1.5/blob/6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0/docs/en/API.md), [pinned main snapshot](https://huggingface.co/ACE-Step/Ace-Step1.5/tree/19671f406d603126926c1b7e2adc169acbcade22), and [pinned base snapshot](https://huggingface.co/ACE-Step/acestep-v15-base/tree/e432212fec32b8965a14ffa57ae653438d6abd14)
- [Revideo repository](https://github.com/midrender/revideo) and [issue #343](https://github.com/midrender/revideo/issues/343)
- [Genblaze repository](https://github.com/backblaze-labs/genblaze) and [v0.6.0](https://github.com/backblaze-labs/genblaze/releases/tag/v0.6.0)
- [Wan S2V endpoint](https://replicate.com/wan-video/wan-2.2-s2v), [exact current API schema](https://replicate.com/wan-video/wan-2.2-s2v/versions/09607e6e761d2f015b0d740f938ec59199f54aa623384465a5054b230405acf4/api), [prediction lifecycle](https://replicate.com/docs/topics/predictions/create-a-prediction), [data retention](https://replicate.com/docs/topics/predictions/data-retention), and [terms](https://replicate.com/terms)
- [B2 S3-compatible API](https://www.backblaze.com/docs/cloud-storage-s3-compatible-api), [application-key capabilities](https://www.backblaze.com/docs/cloud-storage-application-key-capabilities), [file versions](https://www.backblaze.com/docs/cloud-storage-file-versions), and [pricing](https://www.backblaze.com/cloud-storage/pricing)
- [RunPod pricing](https://www.runpod.io/pricing), [RunPod Storage options](https://docs.runpod.io/pods/storage/types), [Modal pricing](https://modal.com/pricing), [Vast.ai pricing guide](https://docs.vast.ai/guides/instances/pricing), and [Lambda Cloud instances](https://lambda.ai/instances)

## 19. Readiness verdict

**Conditionally ready.** Everything that can be truthfully completed without human media, account authority, a GPU, or spend has been prepared or explicitly tested. The next evidence-producing action is one authorized AnyAccomp F1 run. Until it passes both human magic and literal-retention gates, StageMe remains an implemented upstream thesis—not a proven product.
