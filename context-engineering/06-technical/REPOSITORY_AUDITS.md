# Repository Audits

Core repositories were shallow-cloned for direct source inspection. Additional StageMe libraries and reference projects were inspected through GitHub repository metadata, README/source endpoints, or prior direct audits where a full clone was unnecessary. Exact commits and inspection methods are recorded below or in `../10-sources/repositories.json`. Third-party source is not vendored.

## Official: backblaze-labs/genblaze

- URL: https://github.com/backblaze-labs/genblaze
- Commit: `293beade3e705d69b29dbf57402800f8a868313f`
- Last commit inspected: 2026-07-23
- License: MIT (verified in repository README/LICENSE; GitHub API metadata returned unknown)
- Purpose: core pipeline SDK, connectors, manifests, storage, CLI.
- Shape: Python monorepo with core, provider connectors, schema/TS types, CLI, docs, examples.
- Important files: `README.md`, `ARCHITECTURE.md`, `examples/quickstart.py`, `examples/quickstart_local.py`, `docs/features/`, connector READMEs.
- Finding: the product's strongest differentiators are provider portability, durable B2 sink, provenance, fallback, streaming, fan-in/concurrency, and agent loops.

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

The machine ledger records exact commits for 20 additional repositories, including librosa, pyloudnorm, python-audio-separator, Whisper/WhisperX, Revideo, Motion Canvas, MoviePy, PixiJS, wavesurfer.js, Meyda, ONEFIELD, Murmur, InstantBandAI, Vanta, ACE-Step Studio, AceForge, and Synesthesia.

Key license boundary:

- permissive candidates may be adopted with model/asset verification and attribution;
- ONEFIELD, Murmur, InstantBandAI, and ACE-Step UI had no recognized license metadata in the audit and are behavior-only references;
- Vanta and Remotion need exact license review before code reuse;
- Essentia/aubio introduce AGPL/GPL obligations and are not default choices.

See `../08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md` for interface-level adopt/evaluate/reject decisions.

## Reproduction commands

```bash
git clone --depth 1 https://github.com/backblaze-labs/genblaze.git .research-clones/genblaze
git clone --depth 1 https://github.com/backblaze-labs/genblaze-gen-media-multi-provider-sample.git .research-clones/genblaze-gen-media-multi-provider-sample
git clone --depth 1 https://github.com/backblaze-labs/genblaze-gmicloud-pipeline.git .research-clones/genblaze-gmicloud-pipeline
git clone --depth 1 https://github.com/upgradedev/cinemory.git .research-clones/cinemory
git clone --depth 1 https://github.com/yaredtekile/proofrelay.git .research-clones/proofrelay
git clone --depth 1 https://github.com/woadi-vector/reel.git .research-clones/reel
```
