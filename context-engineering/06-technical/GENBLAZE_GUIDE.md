# Genblaze Technical Guide

## What it is

Genblaze is Backblaze's MIT-licensed Python 3.11+ SDK for orchestrating image, video, audio, text/transcription, and supporting LLM calls. It is a library embedded in an application, not a hosted service or daemon.

## Core model

```text
Manifest → Run → Steps → Assets
```

- `Pipeline`: sync/async/streaming workflow, chaining, fan-in, concurrency, batch.
- `Step`: provider/model/prompt/params/retries/fallback/cost.
- `Asset`: URL, media type, SHA-256, size, modality metadata.
- `Manifest`: canonical hash-bound provenance document.
- `Sink`: B2/S3 object storage, Parquet, webhook.
- `AgentLoop`: generate → evaluate → refine/retry with lineage.

## Installed/inspected snapshot

- Repository commit: `293beade3e705d69b29dbf57402800f8a868313f`
- Latest release observed: `v0.6.0`, published 2026-07-22.
- Current distributions observed 2026-07-27: umbrella 0.4.4, core 0.3.7, S3 0.3.6, CLI 0.3.5. The GitHub release label is not every package's version.
- Repository scale from local Pygount scan: 590 files; 49,892 code lines; 26,700 documentation lines.
- A local zero-key quickstart was executed successfully on 2026-07-25. It built one manifest and returned `Verified: True` with canonical hash `42c451695e3aa766bf5945dffc7aa384ac4d6649b692c21589c5af101863fae8`. The run used placeholder bytes and demonstrates manifest mechanics, not live media generation.

## Install patterns

```bash
pip install genblaze
pip install "genblaze[gmicloud]"
pip install "genblaze[video]"
pip install "genblaze[all]"
```

Core packages can also be selected individually: `genblaze-core`, `genblaze-s3`, `genblaze-cli`, plus provider connectors.

Custom providers register through the `genblaze.providers` entry-point group. `BaseProvider` implements real `submit` → `poll` → `fetch_output` lifecycle plus resume/checkpoint semantics. `SyncProvider.generate()` is blocking and uses an in-memory `sync` prediction ID; async thread dispatch does not make it durable.

StageMe consequence: stock AnyAccomp Python 3.9 may use `SyncProvider` only inside its dedicated GPU worker with durable outer job state. It must never block FastAPI or the Python 3.11/3.12 Genblaze control process. Hosted/queued AnyAccomp and ACE-Step require real `BaseProvider` lifecycles.

## Provider matrix observed

- Video: GMI Cloud, NVIDIA NIM, OpenAI Sora, Google Veo, Runway, Luma, Decart.
- Image: GMI Cloud, NVIDIA NIM, OpenAI, Google Imagen, Decart, Replicate.
- Audio: GMI Cloud, NVIDIA NIM, OpenAI TTS, ElevenLabs, Stability Audio, LMNT, Hume.
- Speech-to-text: AssemblyAI.
- Standalone chat helpers: GMI Cloud, NVIDIA, OpenAI, Google.

Availability depends on provider account entitlements and exact model slugs. Registry recognition does not prove a key can execute a model.

## High-scoring features to make visible

- Chain: text/image → video → audio/transform.
- Fan-out: same input across models, then compare/select.
- Fallback models/providers for reliability.
- Streaming progress events in the UI.
- `AgentLoop` for measurable refinement.
- `ObjectStorageSink` to B2 for each intermediate and final asset.
- Manifest lineage using `parent_run_id`.
- Content-addressed storage for deduplication.
- Verification with `genblaze verify --fetch`.
- Structured logs/traces and clear failure status.

## Current version caveats

From v0.6.0 updates and live issues:

- Pin compatible ElevenLabs 2.x and LMNT >=2.6,<3.
- Unknown keyword arguments to `Step` are rejected; provider parameters belong in `params={...}` where required by the current API.
- GMI model entitlement can fail after model validation.
- Google `chat()` has an open portability issue with canonical `ImageURLContent` blocks (#194).
- Cross-provider image-to-video often needs a fetchable URL. Use a short-lived URL for transient provider input and include a stable SHA-256; never persist credential-bearing presigned URLs.
- Use `get_durable_url()` for persisted references and `get_url()` only when a provider needs temporary fetch access.
- Pin SDK/provider versions used in the demonstrated build.
- Current `ProviderComplianceTests` has 16 methods, not the 15 still stated by two documentation pages. Add StageMe-specific source-retention/task tests after the suite.

## Provenance trust boundary

`Manifest.verify()` checks canonical manifest integrity and requires output SHA-256 values; it does not automatically prove remote bytes still match unless fetched. `genblaze verify --fetch` closes that gap by downloading and re-hashing outputs. Provenance is tamper-evident in trusted storage; use Object Lock, signatures, or C2PA when a stronger adversarial trust model is required.

Writable schema is currently 1.5 while 1.6 is read-supported. Canonical hashes exclude operational data, asset transport URLs, and `parent_run_id`. StageMe must therefore bind project/version lineage in its own acceptance record and fetch/hash every locked B2 asset; a valid manifest hash alone is not a remote-byte or parent-link proof.

## Cost control

- Use local step cache while iterating.
- Register current model pricing; Genblaze does not ship fixed prices for all models.
- Use conservative retries for expensive video calls.
- Add human approval before costly fan-out.
- Test with short duration and low resolution, then run final quality settings once.
- For Wan S2V, generic `per_output_second(0.02)` does not automatically price a returned asset with no duration metadata. Estimate from input-audio duration and reconcile against `ffprobe` output duration.
