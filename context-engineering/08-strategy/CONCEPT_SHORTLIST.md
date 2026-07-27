# Ranked Non-Photo-Centric Concept Shortlist

> These are **strategic inferences**, not official categories or commitments. Scores are directional planning aids, not predicted judge scores. Every concept still needs user/problem validation and provider-access tests.

## Ranking method

Each concept is scored 1–5 on seven dimensions: real-world utility, production-readiness potential, B2 depth, Genblaze depth, differentiation, deadline feasibility, and demo impact. Maximum: 35.

| Rank | Concept | Score | Strategic read |
|---:|---|---:|---|
| 1 | **MediaSpec** — quality gates and automatic recovery for generated media | 33/35 | Best current balance of product value, Genblaze/B2 depth, and deadline feasibility |
| 2 | **RenderGuard** — regression and replay lab for media pipelines | 32/35 | Strong architecture fit, but should be narrowed to concrete checks |
| 3 | **AccessForge** — accessibility package generator | 30/35 | Clear human utility and excellent demo |
| 4 | **DubGuard** — dubbing/localization workflow with QA gates | 30/35 | Strong audio pipeline, but provider/cost complexity |
| 5 | **Provenance Gate** — generated-media release approval and verification | 30/35 | Distinctive B2 story, but trust model must be explained carefully |
| — | **ShipCast** — release-demo generator for agent-built software | Deprioritized | Exact competitors exist and the autonomous capture promise is too risky for the deadline |

The ranking changed after focused feasibility and competitor research. PageBolt already claims PR-diff + preview-deployment analysis, autonomous browser recording, narration, and PR comments. PushPlay claims merged-PR-to-video generation using extracted real UI components. RepoClip generates videos from repositories and exposes a GitHub Action. The open-source `makedemo` project also combines browser automation, AI interaction planning, narration, and MP4 output. ShipCast is therefore both crowded and difficult to differentiate within the remaining build window.

## 1. MediaSpec — recommended concept to validate

### Job

Give developers a media-output contract: generate an asset, verify that it meets concrete publishing requirements, and automatically retry or fall back when it does not.

Example requirements include duration range, aspect ratio, codec, file integrity, caption presence, transcript coverage, loudness range, maximum latency/cost, and required manifest fields. Semantic checks may be optional and must be labeled as model judgments.

### Genblaze role

- Generate one or more candidate outputs across providers.
- Stream progress and preserve every run step.
- Run cheap deterministic checks before expensive semantic evaluation.
- Retry a failed step or fall back to another provider under a fixed budget.
- Produce parent-linked manifests for rejected and accepted candidates.

### B2 role

- Store source inputs, all candidates, validation reports, manifests, and the final accepted asset.
- Preserve a reusable history by project/spec/version.
- Byte-verify the final remote object against its manifest.

### Demo

Enter a brief plus a simple media specification. Show candidate A fail a concrete requirement, automatic recovery/fallback produce candidate B, and the accepted B2 object receive a green verification report. Use a pre-seeded run so the value is visible immediately while a live small run proves the integration.

### Main risk

Do not attempt universal aesthetic scoring. Keep the MVP to deterministic and auditable checks, with at most one clearly labeled model-based evaluator.

## Deprioritized: ShipCast

### Job

Turn a pull request, changelog, screenshots, and selected product evidence into a polished, narrated, captioned release-demo package that a developer can publish immediately.

### Why it is not another coding agent

ShipCast does not write code or replace the IDE. It begins after work exists and helps developers communicate what changed.

### Genblaze role

- LLM step extracts a truthful storyboard from supplied release evidence.
- TTS creates narration.
- Optional music/audio step creates or selects a safe bed.
- Deterministic ffmpeg steps compose clips, captions, and audio.
- Evaluation checks duration, missing evidence, caption coverage, and unsupported claims.
- Failed checks trigger a constrained refinement loop.
- Manifest links source evidence, script, narration, captions, and final export.

### B2 role

- Store source evidence, intermediate narration, captions, previews, and final exports.
- Version each release package and preserve manifests.
- Serve review links and final downloadable assets.
- Keep rejected and accepted variants distinguishable.

### Demo

Provide a real PR/release bundle; show ShipCast produce a short narrated launch video, captions, platform variants, and a verification screen.

### Decisive feasibility finding

A fully automatic version is technically possible, but it requires a runnable preview deployment, credentials/test data for authenticated flows, reliable browser control, and correct inference about which user journey proves the PR. Existing products are already pursuing this exact promise. A version that asks users to provide screenshots or recordings is easier, but removes the specific value the entrant wanted. Do not pursue ShipCast for this hackathon unless it is intentionally reduced to a narrow vertical that the existing products do not cover.

## 2. RenderGuard — strongest architecture concept

### Job

Help developers detect when a provider, model, prompt, or pipeline change silently alters generated-media quality, latency, cost, or provenance.

### Genblaze role

- Replay a benchmark prompt set across models/providers.
- Fan out generations concurrently.
- Apply deterministic or model-based evaluators.
- Retry/fallback failed runs.
- Create parent-linked manifests for baseline and candidate runs.

### B2 role

- Store immutable-ish baselines, candidate outputs, manifests, thumbnails, metrics, and comparison reports.
- Retrieve historical runs and byte-verify outputs.
- Organize by suite/provider/model/version/commit.

### Demo

Run the same benchmark against two configurations, show a visible regression or failure, compare media and metrics, then replay/verify the exact stored artifacts.

### Main risk

Quality scoring can look subjective. Use concrete checks—dimensions, duration, loudness, transcript match, perceptual similarity, latency, failure rate—and clearly label model-based judgments.

## 3. AccessForge — strongest direct human utility

### Job

Turn an existing video or audio asset into an accessible publishing package: captions, transcript, audio description, translated/dubbed tracks, chapters, and verified derivatives.

### Genblaze role

- Transcription, structured scene understanding, translation, TTS, and deterministic muxing.
- Human approval before finalization.
- Fallback provider for speech generation.
- Lineage from source asset to every derivative.

### B2 role

- Store original, transcript, caption formats, audio-description track, dubbed variants, thumbnails, final packages, and manifests.
- Version approved revisions and distribute judge-facing outputs.

### Demo

Upload a short inaccessible clip and show a captioned, audio-described, optionally translated package with a manifest.

### Main risk

Accessibility quality is sensitive. Do not claim compliance based solely on automation; describe the output as an editable first pass with human review.

## 4. DubGuard — audio localization with QA

### Job

Help small teams produce and review multilingual narration/dubbing while preserving script, voice, timing, model, and approval evidence.

### Genblaze role

- Transcribe, translate, synthesize multiple voice candidates, compare timing, retry, and compose.
- Stream progress and provide provider fallback.
- Preserve parent-child lineage for approved revisions.

### B2 role

- Store source audio/video, scripts, candidate tracks, approved tracks, timing metadata, final media, and manifests.

### Demo

Create two language versions, deliberately fail one timing or duration check, regenerate it, and approve a final version.

### Main risk

Voice providers, cloning permissions, timing alignment, and generation costs increase integration risk. Avoid impersonation and use authorized/synthetic voices.

## 5. Provenance Gate — generated-media release control

### Job

Give a team a release queue where generated assets must carry complete provider/model/asset lineage, human approval, and byte verification before publication.

### Genblaze role

- Generate or transform the asset inside the product.
- Create canonical manifests and lineage across revisions.
- Verify local and fetched remote bytes.
- Run policy/evaluation steps before approval.

### B2 role

- Store media, manifests, approvals, and final release objects.
- Optionally use Object Lock for approved records where immutability is truly required.
- Serve a verification page for published assets.

### Demo

Show an asset fail release because metadata or verification is incomplete, fix/regenerate it, approve it, and verify the final B2 bytes.

### Main risk

A SHA-256 manifest is not a complete public-trust system. Explain the trust boundary; do not claim blockchain-style or C2PA-level authenticity unless actually implemented.

## Recommendation

Validate **MediaSpec** with a short vertical-slice spike before selecting:

1. Can the core Genblaze pipeline execute with currently available providers?
2. Can B2 store and retrieve the complete run package with verifiable hashes?
3. Can a stranger understand the before/after in under 20 seconds?
4. Can one vertical slice be deployed within 48 hours?

Proceed only if one generated asset can be checked, rejected, retried/fallen back, stored in B2, fetched, and byte-verified end to end. If that spike is too costly or slow, fall back to AccessForge with a narrow caption/transcript/audio-description package.

## Concepts to avoid

- Generic prompt-to-image/video wrappers.
- A light reskin of either official sample.
- Photo-memory reels, screenplay previsualization, or field-report provenance without a materially different audience/workflow; public participant repositories already occupy those spaces.
- A Web3 token/NFT layer that is not required for the user's job. It adds scope without improving the published criteria.
- Event Notifications as a critical dependency unless Backblaze Support has enabled access.
