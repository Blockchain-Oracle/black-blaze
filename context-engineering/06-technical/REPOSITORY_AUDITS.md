# Repository Audits

All repositories were shallow-cloned locally under ignored `.research-clones/` directories. Commit hashes make the inspection reproducible. Third-party participant code is not vendored.

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

## Reproduction commands

```bash
git clone --depth 1 https://github.com/backblaze-labs/genblaze.git .research-clones/genblaze
git clone --depth 1 https://github.com/backblaze-labs/genblaze-gen-media-multi-provider-sample.git .research-clones/genblaze-gen-media-multi-provider-sample
git clone --depth 1 https://github.com/backblaze-labs/genblaze-gmicloud-pipeline.git .research-clones/genblaze-gmicloud-pipeline
git clone --depth 1 https://github.com/upgradedev/cinemory.git .research-clones/cinemory
git clone --depth 1 https://github.com/yaredtekile/proofrelay.git .research-clones/proofrelay
git clone --depth 1 https://github.com/woadi-vector/reel.git .research-clones/reel
```
