# Ranked Non-Photo-Centric Concept Shortlist

> These are **strategic inferences**, not official categories or commitments. Scores are directional planning aids, not predicted judge scores. Every concept still needs user/problem validation and provider-access tests.

## Ranking method

Each concept is scored 1–5 on seven dimensions: real-world utility, production-readiness potential, B2 depth, Genblaze depth, differentiation, deadline feasibility, and demo impact. Maximum: 35.

| Rank | Concept | Score | Strategic read |
|---:|---|---:|---|
| 1 | **ShipCast** — release-demo generator for agent-built software | 32/35 | Best entrant fit and fastest polished story |
| 2 | **RenderGuard** — regression and replay lab for media pipelines | 32/35 | Strongest pure Genblaze/B2 architecture fit |
| 3 | **AccessForge** — accessibility package generator | 30/35 | Clear human utility and excellent demo |
| 4 | **DubGuard** — dubbing/localization workflow with QA gates | 30/35 | Strong audio pipeline, but provider/cost complexity |
| 5 | **Provenance Gate** — generated-media release approval and verification | 30/35 | Distinctive B2 story, but trust model must be explained carefully |

The tie between ShipCast and RenderGuard is broken in favor of ShipCast because its user story and demo are easier to understand quickly, and it aligns with the entrant's interest in tools that complement coding agents without becoming an IDE or coding agent.

## 1. ShipCast — recommended first concept to validate

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

### Main risk

A fully automatic screencast is too broad for the deadline. Scope version one to supplied clips/screenshots plus generated narration, captions, composition, and evidence-linked claims.

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

Validate **ShipCast** and **RenderGuard** with two short spikes before selecting:

1. Can the core Genblaze pipeline execute with currently available providers?
2. Can B2 store and retrieve the complete run package with verifiable hashes?
3. Can a stranger understand the before/after in under 20 seconds?
4. Can one vertical slice be deployed within 48 hours?

Choose ShipCast if polished user experience and an immediately relatable demo dominate. Choose RenderGuard if the implementation team can make technical pipeline evidence visually compelling and wants the strongest developer-tool architecture.

## Concepts to avoid

- Generic prompt-to-image/video wrappers.
- A light reskin of either official sample.
- Photo-memory reels, screenplay previsualization, or field-report provenance without a materially different audience/workflow; public participant repositories already occupy those spaces.
- A Web3 token/NFT layer that is not required for the user's job. It adds scope without improving the published criteria.
- Event Notifications as a critical dependency unless Backblaze Support has enabled access.
