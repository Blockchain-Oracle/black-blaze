# Repository Audits

Core repositories were shallow-cloned for direct source inspection. Additional libraries and reference projects were inspected through GitHub repository metadata, README/source endpoints, or prior direct audits where a full clone was unnecessary. Exact commits and inspection methods are recorded below or in `../10-sources/repositories.json`. Third-party source is not vendored.

## Official: backblaze-labs/genblaze

- URL: https://github.com/backblaze-labs/genblaze
- Commit: `c5a57085a0ca78339eea65b91786f0edad7959e1`
- Last commit inspected: 2026-07-28 18:06:47 UTC
- License: MIT (verified in repository README/LICENSE; GitHub API metadata returned unknown)
- Purpose: core pipeline SDK, connectors, manifests, storage, CLI.
- Shape: Python monorepo with core, provider connectors, schema/TS types, CLI, docs, examples.
- Important files: `README.md`, `ARCHITECTURE.md`, `examples/quickstart.py`, `examples/quickstart_local.py`, `docs/features/`, connector READMEs.
- Finding: the product's strongest differentiators are provider portability, durable B2 sink, provenance, fallback, streaming, fan-in/concurrency, and agent loops.
- Release boundary: latest release remains `v0.6.0` at `ce651213daa6eb90cca738e5ae2c56055a2f56e1`; open PR #236 prepares but does not release v0.7.0.
- Current-main reproduction: 345 passed, 3 skipped across five zero-credential package suites. No provider call, B2 operation, or media generation was performed.

## Official: backblaze-labs/genblaze-gen-media-multi-provider-sample

- URL: https://github.com/backblaze-labs/genblaze-gen-media-multi-provider-sample
- Commit: `2e31577b7a9d5a7b0309d814f2d0282088b33fe8`
- Last commit inspected: 2026-07-07
- License: LICENSE present; official blog identifies both samples as MIT.
- Scale: 132 files; 9,116 code lines; 2,531 documentation lines.
- Stack: Next.js/React UI + FastAPI backend + ffmpeg + Genblaze + B2.
- Pipeline: one sentence → structured storyboard → image per scene → video → TTS → music → captioned MP4.
- Providers: configurable switchboard across OpenAI, Replicate, Google, NVIDIA, Decart, GMI, Runway, Luma, ElevenLabs, LMNT, Hume.
- Important pattern: provider choice per modality, live SSE progress, parent-linked manifests, all intermediates/final in B2, no direct boto3.
- Reproduction on 2026-07-27: frozen install with pnpm 10.32.1 succeeded; direct web-workspace Next.js 16.1.6 production build compiled and generated 7/7 static pages; direct `tsc --noEmit` exited 0.
- Toolchain defect: the root scripts invoke ambient `pnpm`; this resolved to pnpm 11.17.0 and failed under Node 20.20.2 despite the repository declaring Node `>=20`. Pin Corepack/`packageManager` rather than inheriting ambient pnpm.
- Strategic warning: this is a reference implementation, not a differentiated product. Forking and reskinning it is unlikely to score highly on utility.

## Official: backblaze-labs/genblaze-gmicloud-pipeline

- URL: https://github.com/backblaze-labs/genblaze-gmicloud-pipeline
- Commit: `355a539ecf99f8d6fcfc5ba40cc5f9a95523100b`
- Last commit inspected: 2026-04-27
- License: MIT.
- Scale: 153 files; 8,217 code lines; 1,246 documentation lines.
- Stack: Next.js 16/React 19 + FastAPI + Genblaze GMI connector + B2.
- Pipeline: prompt → anchor image → iterative refinement → approve → concurrent fan-out to three video models → B2 manifests/assets.
- Important pattern: under ~100 lines of Genblaze-specific integration, typed SSE events, strict layer boundary, Object Lock option.
- Risk: older model slugs or env conventions may drift; verify against current v0.6 and provider account.

## Official: backblaze-labs/nvidia-nemotron-genblaze-b2

- URL: https://github.com/backblaze-labs/nvidia-nemotron-genblaze-b2
- Commit: `71e1f12040b011340f90aba99bc07bd07a7661c7`
- Last commit inspected: 2026-05-26
- License: MIT.
- Stack: Next.js 16.1.6/React 19.2.3 + FastAPI/Python 3.11 + Genblaze + B2.
- Pipeline: uploaded image/audio/video → Nemotron structured briefing → parallel image/TTS/music and optional video → hierarchical B2 assets plus manifest.
- Finding: useful official reference for multimodal ingestion, schema-constrained planning, provider fan-out, and Genblaze isolation. Its tests deliberately make no NVIDIA/B2 calls, so they do not prove entitlement or media quality.
- Boundary: architecture reference only; do not copy its product identity or assume its older locked Genblaze packages are current API authority.

## Official: backblaze-labs/ai-saas-starter-kit

- URL: https://github.com/backblaze-labs/ai-saas-starter-kit
- Commit: `79085c93b01c7ac547f9cd959b0d00fd1bb972e1`
- Last commit inspected: 2026-07-27
- License: MIT.
- Stack: Next.js 16.2.11/React 19.2.3 + FastAPI + local/hosted Supabase + optional Stripe + B2 file manager + NVIDIA/Genblaze image path.
- Finding: official reference for production-shaped auth, jobs, admin, storage, and SDK containment. Its broad SaaS shell does not supply a hackathon user's painful job or differentiated generative-media product.
- Boundary: do not inherit billing/account complexity unless the selected workflow needs it; exact dependencies trail current Genblaze packages.

## Competitive signal: upgradedev/cinemory

- URL: https://github.com/upgradedev/cinemory
- Commit: `fababdc10521f30bef2b8ba1f6ab4956173eef8c`
- Concept: photos/memories → cinematic reels with source-to-output provenance.
- Evidence: public deployment, 2:17 local demo file, extensive security/tests/readiness gates claimed in README.
- Learning: judges may see very polished entries. Match operational evidence, not concept.
- Do not copy: product identity, photo-reel workflow, code, assets, or language.

## Competitive signal: yaredtekile/proofrelay

- URL: https://github.com/yaredtekile/proofrelay
- Commit: `700cc77898677e6434bd331dbfbbbd29087ba690`
- Concept: approved field evidence → multilingual publishable media with a human approval gate.
- Learning: deterministic non-generative transformations can sit in the same Genblaze manifest and preserve factual control.
- Do not copy the incident-report/NGO product framing.

## Competitive signal: woadi-vector/reel

- URL: https://github.com/woadi-vector/reel
- Commit: `41ba8b53a2e06222ff024d57e107996eab921853`
- Concept: screenplay → shot list → stills → video clips → score → previsualized cut.
- Learning: model-slug drift, private B2 handoff, provider throttling, and chat provenance are real integration pitfalls.
- Do not copy the screenplay/previsualization concept or code.

## StageMe core/source audits — 2026-07-27

### AmphionTeam/AnyAccomp

- URL: https://github.com/AmphionTeam/AnyAccomp
- Commit: `82604b5e3107944ad4c49fc64900b86118ae2c62`
- License: MIT code; AnyAccomp model card declares checkpoints CC-BY-4.0. Preserve attribution and verify the exact downloaded artifact/model card.
- Inspection: direct shallow clone and `infer_from_folder.py` / `anyaccomp/inference_utils.py` source review.
- Finding: official inference writes separate accompaniment and a mixture computed as generated accompaniment plus the original vocal waveform. This is StageMe's strongest literal-retention candidate.
- Caveat: direct source inspection does not establish quality, latency, VRAM, or product fit.

### ace-step/ACE-Step-1.5

- URL: https://github.com/ace-step/ACE-Step-1.5
- Commit: `6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0`
- License: MIT observed; verify weights and bundled components.
- Inspection: direct shallow clone; inference/task documentation and source reviewed.
- Finding: base model supports `lego`, `complete`, and `repaint`; API uses release/query/audio job lifecycle. `lego` is the first separate-layer test; `complete` is a comparison; `repaint` is gated behind an accepted parent.
- Caveat: turbo latency claims do not apply to the required base-model edit tasks.

### StageMe support/reference repositories

The machine ledger records exact commits for the StageMe support and reference repositories, including librosa, pyloudnorm, python-audio-separator, Whisper/WhisperX, Revideo, Motion Canvas, MoviePy, PixiJS, wavesurfer.js, Meyda, ONEFIELD, Murmur, InstantBandAI, Vanta, ACE-Step Studio, AceForge, and Synesthesia.

Key license boundary:

- permissive candidates may be adopted with model/asset verification and attribution;
- ONEFIELD, Murmur, InstantBandAI, and ACE-Step UI had no recognized license metadata in the audit and are behavior-only references;
- Vanta and Remotion need exact license review before code reuse;
- Essentia/aubio introduce AGPL/GPL obligations and are not default choices.

See `../08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md` for interface-level adopt/evaluate/reject decisions.

### fspecii/ace-step-ui

- URL/commit: https://github.com/fspecii/ace-step-ui at `a1fdf91829ec6f7b98844f80e323529cd155dbf2`; shallow clone inspected 2026-07-27 11:15 UTC.
- Purpose: workflow/history/editing calibration for the later ACE comparison, never a source or product-identity dependency.
- Architecture: React/Vite frontend, Express/SQLite backend, local ACE-Step Gradio API, FFmpeg/AudioMass/Demucs integrations, and library/history surfaces.
- Setup/activity: Node 18+, ACE-Step launched separately with API enabled; current head was pushed 2026-06-27. GitHub reported 47 open issues/PRs at inspection, including Gradio/CLI/VRAM failures in issue 105 and app-config fallback in issue 87.
- License boundary: the README displays an MIT badge, but the inspected tree has no LICENSE/COPYING file and GitHub license metadata is null. Treat the repository as no recognized license and do not copy code or assets.
- Finding: confirms user demand for local history, seed reuse, repaint, and region-editing workflows, while also exposing the maintenance burden and generic full-song-workstation scope StageMe must avoid.

## Reproduction commands

```bash
git clone --depth 1 https://github.com/backblaze-labs/genblaze.git .research-clones/genblaze
git clone --depth 1 https://github.com/backblaze-labs/genblaze-gen-media-multi-provider-sample.git .research-clones/genblaze-gen-media-multi-provider-sample
git clone --depth 1 https://github.com/backblaze-labs/genblaze-gmicloud-pipeline.git .research-clones/genblaze-gmicloud-pipeline
git clone --depth 1 https://github.com/backblaze-labs/nvidia-nemotron-genblaze-b2.git .research-clones/nvidia-nemotron-genblaze-b2
git clone --depth 1 https://github.com/backblaze-labs/ai-saas-starter-kit.git .research-clones/ai-saas-starter-kit
git clone --depth 1 https://github.com/upgradedev/cinemory.git .research-clones/cinemory
git clone --depth 1 https://github.com/yaredtekile/proofrelay.git .research-clones/proofrelay
git clone --depth 1 https://github.com/woadi-vector/reel.git .research-clones/reel
git clone --depth 1 --branch v2.7.2 https://github.com/runpod/runpodctl.git .research-clones/runpodctl
git -C .research-clones/runpodctl checkout --detach v2.7.2
```

## StageMe pre-call refresh — checked 2026-07-27 10:13–17:14 UTC

All repositories below were inspected from ignored shallow clones. No third-party source or weight was copied into the project. Model-output quality remains unreproduced.

### AnyAccomp refresh

- URL/commit: https://github.com/AmphionTeam/AnyAccomp at `82604b5e3107944ad4c49fc64900b86118ae2c62`; clean clone.
- Purpose: first source-conditioned accompaniment experiment.
- Code/model licenses: MIT code; checkpoint revision `9aa9e62427337bf1df4caa3c4f3e6ad934522e71` declares CC BY 4.0.
- Exact weight tree: 880,790,586-byte flow model, 1,020,206,416-byte vocoder, 177,202,134-byte VQ; 2,078,199,136 bytes total.
- Runtime: stock Python 3.9, FFmpeg 4.x, Torch/Torchaudio 2.3.1, CUDA 12.1 dependencies. A `uv pip compile` resolution for Python 3.9/Linux passed; no weights were downloaded.
- Implementation: 24 kHz mono input; 50 steps, CFG 3, seed 1024 defaults; separate accompaniment; un-gain-staged raw source-plus-accompaniment mixture.
- New installation finding: the current Hugging Face model tree already begins `pretrained/...`, so the README's `local_dir='./pretrained'` snapshot example nests it. The runbook downloads the pinned allowed tree into the repository root and verifies exact hashes.
- Hosted boundary: official Space currently reports `CONFIG_ERROR`; no Hugging Face inference-provider mapping exists. No Dockerfile or official VRAM/latency/CPU benchmark was found.

### ACE-Step 1.5 refresh

- URL/commit: https://github.com/ace-step/ACE-Step-1.5 at `6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0`; clean clone.
- Release: `v0.1.8`, tag commit `dce621408bee8c31b4fcf4811682eb9359e1bc94`; package declares 1.5.0.
- Immutable Hugging Face state: model-card/main snapshot [`ACE-Step/Ace-Step1.5@19671f406d603126926c1b7e2adc169acbcade22`](https://huggingface.co/ACE-Step/Ace-Step1.5/tree/19671f406d603126926c1b7e2adc169acbcade22); base snapshot [`ACE-Step/acestep-v15-base@e432212fec32b8965a14ffa57ae653438d6abd14`](https://huggingface.co/ACE-Step/acestep-v15-base/tree/e432212fec32b8965a14ffa57ae653438d6abd14). Base `model.safetensors` is 4,787,825,604 bytes with SHA-256 `4177f600501a6d4bd81cadaa0abac557ffd15c54e5c8cb52053cdb24a0844d6b`.
- Purpose: `lego` separate-layer comparison, `complete` full-mix comparison, `repaint` only after parent acceptance.
- License: MIT code/model cards; bundled Qwen3-derived components originate under Apache 2.0.
- Download boundary: the five major tensor weights total 14,813,190,540 bytes / 13.796 GiB. The complete pinned main and base snapshots total 14,883,895,000 bytes / 13.862 GiB, including configs and auxiliary files. The base checkpoint exceeds 2 GB and was not downloaded.
- Runtime: Python 3.11–3.12; official Linux pins Torch 2.10/CUDA 12.8 and ships a CUDA 12.8.1 Dockerfile.
- Implementation risks: `complete` source validation/duration mismatch; request crossfade fields recomputed; repaint splice/truncation is mode/length-dependent; API job store is in memory, unknown IDs look pending, no generation cancel exists, and request timeout may leave CUDA work running.
- Hosted boundary: official Space exposes turbo/XL-turbo rather than base-only `lego`/`complete`; no base inference-provider mapping was found.

### Revideo refresh and reproduction

- URL/commit: https://github.com/midrender/revideo at `b5de67a009a55aa2768a1e178b0446b2479a0b4e`; npm 0.11.0; MIT.
- Runtime: Node `>=22.12.0`, Puppeteer 25.3.0, fetched Chrome/headless shell 150.0.7871.24. Telemetry opt-out is `DISABLE_TELEMETRY=true`.
- Canonical monorepo build passed for 10 projects.
- First bundled-template render passed: 7.433 seconds, 1080×1080 at 30 fps, H.264/AAC, 11.42 seconds wall, 467,517,440-byte max RSS, output SHA-256 `58ec67eab29a44a48fde7f096d3c515066b31a7b5ce0af1cdb41549463c0cda7`.
- Immediate rerenders failed on Node 25 and supported Node 22.12 with `Navigating frame was detached`, consistent with open issue #343 and the source-forced Chromium `--single-process` argument.
- Decision: intended architecture but not StageMe-reproduced. Require three consecutive cold/warm 15-second 720p local-audio/font runs, sync/repeat checks, container and deployment success. FFmpeg/MoviePy remains Phase-0 fallback.

### Genblaze refresh and reproduction

- URL/current main: https://github.com/backblaze-labs/genblaze at `c5a57085a0ca78339eea65b91786f0edad7959e1`; release `v0.6.0` tag commit `ce651213daa6eb90cca738e5ae2c56055a2f56e1`; MIT; Python ≥3.11.
- Current distributions observed independently: umbrella 0.4.4, core 0.3.7, S3 0.3.6, CLI 0.3.5.
- Previous snapshot `293beade3e705d69b29dbf57402800f8a868313f`: selected suite 210 passed, 3 skipped; separate clean-room core/S3 suites 388 and 26 passed.
- Current main on 2026-07-28: core pipeline/retry 232 passed; CLI verify-fetch 22 passed; Google chat/Gemini image 53 passed, 3 skipped; GMI entitlement 7 passed; OpenAI chat 31 passed. Total 345 passed, 3 skipped.
- A combined cross-package pytest command first failed with `ImportPathMismatchError` because connector packages expose the same top-level `tests` package. Separate package runs passed; issue #66 tracks this test-layout class.
- Runtime: CPython 3.13.13, pytest 9.1.1, macOS 26.2 arm64, using the ignored clone's `.venv/bin/python`.
- Exact passing commands from `.research-clones/genblaze`:

```bash
.venv/bin/python -m pytest -q libs/core/tests/unit/test_provider_retry.py libs/core/tests/unit/test_pipeline.py
.venv/bin/python -m pytest -q cli/tests/test_verify_fetch.py
.venv/bin/python -m pytest -q libs/connectors/google/tests/test_gemini_image_provider.py libs/connectors/google/tests/test_chat.py
.venv/bin/python -m pytest -q libs/connectors/gmicloud/tests/test_entitlement_gating.py
.venv/bin/python -m pytest -q libs/connectors/openai/tests/test_chat.py
```

- The failed combined command used those seven test files in one invocation and exited 4 while loading the GMI `conftest.py`; pytest reported `ImportPathMismatchError` against the core `tests.conftest`. This is test-layout evidence, not a product/runtime failure.
- The current compliance class has 16 methods while two docs still say 15.
- `SyncProvider` is blocking and non-durable despite async thread dispatch; local AnyAccomp belongs only in a dedicated worker with outer durable state. ACE and any queued AnyAccomp need real `BaseProvider` lifecycle semantics.
- Manifest verification does not fetch remote bytes. Canonical hashes omit asset transport URLs and `parent_run_id`; StageMe must bind lineage and fetch/hash media separately.
- Current-main changes include bounded chat retry ownership, Gemini image support, GMI/Google entitlement gates, Runway changes, and verify-fetch hardening. P1 issue #233 warns that Google examples still use delisted Imagen slugs. Open PR #236 is not a release.

### Newly cloned support/runtime repositories

| Repository | Inspected commit | License boundary | Purpose / finding |
|---|---|---|---|
| https://github.com/numpy/numpy | `25c89980fcffe59af8ac12b39cf41bd4b07d09ce` | BSD-3 core; bundled notices; GitHub metadata NOASSERTION | deterministic arrays/null metrics; released 2.4.6 selected for Python 3.11 compatibility |
| https://github.com/scipy/scipy | `e0134f43e13f376a59d9aabaf7c193403131c8f9` | BSD-3 plus bundled notices | pinned 1.17.1 signal/scientific dependency for QC environment |
| https://github.com/bastibe/python-soundfile | `350394191a2af890fc464d0f11a1690e7a4f4c64` | BSD-3 wrapper; libsndfile separate | released 0.14.0 lossless float WAV/FLAC I/O |
| https://github.com/FFmpeg/FFmpeg | `a757b708ae7d43fdec89545a55cbc11ae2967b19` | LGPL/GPL depends on build | decode/probe/resample/mix/mux/QC; local Homebrew 8.1.1 enables GPL components and is not a default redistribution build |
| https://github.com/Wan-Video/Wan2.2 | `42bf4cfaa384bc21833865abc2f9e6c0e67233dc` | Apache-2.0 code/model materials | upstream authority for optional 3–5 second Replicate S2V interval |
| https://github.com/runpod/runpodctl | `309512b4926eb7d218bbc8a8f11d380ce54f59c4` (`v2.7.2`) | GPL-3.0 | first-call GPU control plane; released deadline semantics, Secure Cloud/data-center flags, credential precedence, and operational failure calibration |

### RunPod CLI control-plane refresh

- URL/commit: https://github.com/runpod/runpodctl at detached release `v2.7.2`, commit `309512b4926eb7d218bbc8a8f11d380ce54f59c4`; ignored shallow clone inspected 2026-07-27 17:14:05 UTC.
- Purpose: verify the exact first-call Pod lifecycle rather than relying on mutable prose documentation.
- License/setup: GPL-3.0; official macOS installation uses the RunPod Homebrew tap. The checksum-pinned formula installed `runpodctl 2.7.2-309512b`; upstream source declares Go 1.26.5 for source builds.
- Architecture/implementation: Cobra CLI with REST and GraphQL clients; GPU Pod creation uses GraphQL, accepts explicit `SECURE` cloud type, one effective data-center ID, GPU/image/disk/environment controls, and passes `terminateAfter` unchanged.
- Reproduced local behavior: version/help executed; unauthenticated GPU inventory failed cleanly because no API key is configured. No Pod, media transfer, account mutation, or paid action occurred.
- Documentation conflict: the live prose page shows relative values such as `1h`, but v2.7.2 help/source define `--terminate-after` as an absolute RFC 3339 datetime. Create/get output does not return that configured deadline, so the runbook requires authenticated-console confirmation before F1 transfer.
- Activity/risks: open PR [#303](https://github.com/runpod/runpodctl/pull/303) adds missing checksum verification to self-update/install script; do not use `runpodctl update`. Open PR [#294](https://github.com/runpod/runpodctl/pull/294) reports silent template disk/volume/environment inheritance; use an immutable custom image and explicit values. Open issue [#43](https://github.com/runpod/runpodctl/issues/43) reports stalled `send`; use SSH/SCP plus SHA-256 verification.
- Credential boundary: prefer a session-local `RUNPOD_API_KEY`, which source inspection shows takes precedence over the config file. Never place it in Git, commands, screenshots, or logs.

### Official multi-provider sample refresh

- Commit remains `2e31577b7a9d5a7b0309d814f2d0282088b33fe8`.
- pnpm 10.32.1 frozen install, Next 16.1.6 build, and TypeScript check passed.
- The repository allows Node ≥20/pnpm ≥9 but does not pin `packageManager`; current pnpm 11.17 requires Node ≥22.13. Pin pnpm 10.32.1 or tighten the runtime declaration. Do not copy the sample's product identity or stale dependency pins.
