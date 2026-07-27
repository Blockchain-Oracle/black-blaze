# Public Field Audit — 2026-07-27

> Purpose: prevent concept selection from relying on the unpublished Devpost gallery or on idea novelty assumptions.

## Evidence boundary

- Checked at 2026-07-27 01:22 UTC / 02:22 WAT.
- Devpost showed **1,096 registered participants**.
- The official project gallery said: **"The hackathon managers haven't published this gallery yet."**
- Therefore, public GitHub repositories, Devpost pages discoverable outside the event gallery, Genblaze issues, and project READMEs are competitive signals—not a complete entrant list.
- A GitHub repository search for `genblaze` returned 49 public repositories. The point-in-time result is preserved in `../10-sources/public_genblaze_repository_scan_2026-07-27.json`.
- A public repository is treated as an event entry only when its own README/description says so or it links to the event. Even then, public code does not prove final submission or judge eligibility.

## How to use competitor evidence

Competitor overlap is **not an automatic disqualifier**. Existing work can validate demand, reveal the expected quality bar, expose technical traps, and provide implementation patterns worth learning from. The strategy is not to reactively imitate or flee every overlapping project; it is to play a coherent own game with a clear user, outcome, and product thesis.

Use the field scan to ask:

1. What user demand does this validate?
2. What execution patterns should we learn from?
3. What failure modes have others already exposed?
4. What would make our product independently valuable and recognizably ours?
5. Can our implementation, positioning, and demonstration credibly outperform the visible bar?

Reject or reshape a concept only when overlap combines with a weak buyer outcome, poor sponsor fit, infeasible execution, or no credible way to distinguish the product—not merely because somebody else is building nearby.

## What the sponsor is asking for

The official event page says to help people **create, manage, verify, or publish** AI-generated media. The official Backblaze launch post adds a stronger technical signal:

- the differentiation should be in the pipeline, not just the frontend;
- stream progress;
- fan out work concurrently;
- fall back when a provider stalls;
- make providers swappable;
- keep latency tolerable;
- persist assets and provenance;
- solve a real-world use case.

The judging criteria give equal weight to:

1. real-world utility;
2. production readiness;
3. B2 storage and data orchestration;
4. meaningful Genblaze use.

A visually impressive generator with weak production and storage evidence is not automatically favored. A technically deep pipeline with no named user or useful outcome is also weak.

## Representative public projects

| Project | Public proposition | Strategic implication |
|---|---|---|
| [ReproFrame AI](https://github.com/spectramaster/reproframe-ai) | Evidence-bounded scientific visual generation with deterministic checks, retry, B2 evidence, and a public Devpost submission | Generate/evaluate/retry/verify is already demonstrated in a polished domain product |
| [Waystation](https://github.com/russomon/waystation) | Broadcast-grade video delivery and QC with deterministic/AI checks, B2 Event Notifications, Object Lock, and extensive proof scripts | Generic media QC is occupied by a technically advanced entrant |
| [Genblaze Studio QC](https://github.com/reach-Harishapc/Genblaze-Studio-QC) | Self-healing multimodal generation with QC and provenance vault | Direct proposition overlap with generic MediaSpec; README says parts of QC are simulated, so execution quality still matters |
| [Crucible](https://github.com/bssilva06/crucible) | Generate-and-certify gauntlet, deterministic quality gates, optional vision judge, multi-provider fan-out | Direct overlap with candidate validation/selection MediaSpec |
| [VeriGen](https://github.com/lucylow/VeriGen-Genblaze-on-B2) | Multi-provider consensus and automated quality scoring | Model comparison and automatic selection are crowded |
| [Reprise](https://github.com/OrionArchitekton/reprise) | Search/reuse existing B2 assets before paying to regenerate; measured thresholds and immutable savings ledger | Cost control, media memory, and reuse are already occupied strongly |
| [ProofFrame](https://github.com/adjcjh777/backblaze-proofframe) | Operations desk for generated assets, approvals, hashes, manifests, and retirement | Generic review/provenance consoles are crowded |
| [SceneLedger](https://github.com/prabhakaran-jm/sceneledger) | Source-linked training media that detects which scene becomes stale when the source changes | Version-aware training media is occupied |
| [ClaimScene](https://github.com/upgradedev/claimscene) | Human-reviewed accident schematic and explicitly labeled AI illustration | Evidence-bound high-stakes domain media is occupied by a polished concept |
| [OriginShot](https://github.com/rogerjeasy/originshot) | Marketplace-ready product media cryptographically bound to the original product photo | Product-media provenance has a strong domain entrant |
| [Trueprint](https://github.com/usv240/trueprint) | Historical photo/audio restoration that exposes what AI inferred | Restoration and authenticity are occupied |
| [Cast](https://github.com/mark124/cast) | One audio recording localized into many languages with provider failover | Audio localization has a strong entrant |
| [Lumora](https://github.com/yvesdylane/Lumora) | Generative video editor where AI creates editable timeline layers | Non-destructive AI video editing is occupied |
| [Encore](https://github.com/banksythequantLab/encore) | Episodic media with persistent character/season memory and retake loop | Character continuity and series memory are occupied |
| [Cinemory](https://github.com/upgradedev/cinemory) | Personal photos/memories to cinematic reels | Personal memory reels are occupied and do not fit the user's photo preference |
| [Reel](https://github.com/woadi-vector/reel) | Screenplay to previsualized cut | Storyboard/previsualization is occupied |
| Brand/campaign generators | BrandForge, Campaign Forge, Adzenbi, AdForgeAI, GenStudio, and others | Generic marketing content factories are heavily crowded |
| Provenance/compliance tools | Prove AI, TraceFrame variants, ProofForge, ProofCast, Provenance Studio, and others | Provenance alone is a feature, not a sufficient differentiator |

## What changed for MediaSpec

### Original proposition

A user defines a media contract, Genblaze generates candidate output, deterministic and optional semantic checks decide pass/fail, failed output is repaired/retried/fallen back, and B2 stores every candidate plus evidence.

### New evidence

That proposition now overlaps directly with:

- Waystation's deterministic and AI QC lanes;
- Genblaze Studio QC's self-healing quality loop;
- Crucible's deterministic quality gates and best-of-provider selection;
- ReproFrame's constrained evaluation/retry/verify flow;
- VeriGen's multi-model consensus and scoring.

### Verdict

**Do not default to generic MediaSpec as the final product.**

This is not because competitor presence automatically kills the idea. The deeper problem is that the standalone buyer outcome remains abstract: if generation already succeeds, many users do not wake up wanting a contract or QC dashboard. The underlying contract engine remains useful and can support a recognizably different product. A generic implementation would need both to exceed the visible production evidence and to answer why a specific user needs this product independent of the infrastructure. Under the deadline, a sharply defined workflow is the stronger own-game strategy.

## Open concept spaces worth validating

### 1. ReachPack / AccessSpec — accessible publication compiler

**Outcome:** one source video becomes a reviewable accessibility and low-bandwidth delivery package: captions, descriptive transcript, draft audio description, audio-only/low-data rendition, validation report, and verified B2 bundle.

- Named users: education teams, public-information publishers, NGOs, small media teams, and course creators.
- Genblaze: transcription, visual analysis, description drafting, TTS, optional provider fallback, deterministic composition, progress events, lineage.
- B2: source master, timed text, audio tracks, renditions, reports, manifests, review state, and delivery bundle.
- MediaSpec role: validates caption timing/coverage, track presence, duration, loudness, hashes, and package completeness.
- Distinction from Waystation: remediation and accessible publishing rather than read-only broadcast QC.
- External market warning: 3Play, Subly, ViddyScribe, and other accessibility vendors exist. The product must be a complete auditable publication compiler, not merely automatic captions.
- Adjacent open-source products validate individual parts of the workflow: [descraibe](https://github.com/fhswf/descraibe) claims VAD, transcription, scene extraction, and AI audio description; [InstaScribe](https://github.com/AndriiArtemenko3/InstaScribe_Video_Description_Pipeline) claims human-reviewed, gap-aware description authoring and mixing; [Omni Describer](https://github.com/audioses/omni-describer) claims editable descriptions, TTS, and described-video export; and [ClassTranscribe](https://github.com/cs-education/classTranscribe) covers accessible, searchable captioned lectures.
- Therefore, novelty cannot rest on captions, transcription, TTS, or audio description individually. The own-game wedge must be the complete **source-to-publication bundle**: accessible derivatives, low-data delivery, explicit review state, deterministic package checks, checksums/manifests, and a versioned B2 release.
- Safety/honesty: generated captions and audio descriptions require human review; do not claim automatic WCAG certification.
- Technical red flags: descriptions must fit natural speech gaps; mixing and ducking must remain intelligible; low-data outputs must be measured rather than merely resized; and the public demo must distinguish real provider calls, cached evidence, and deterministic transformations honestly.

### 2. DemoSpec — existing browser test to truthful release video

**Outcome:** use a developer's existing Playwright test as the deterministic interaction script; Genblaze produces narration/captions/music and B2 stores versioned release media.

- Removes ShipCast's impossible arbitrary feature-discovery step.
- Requires no manual screen recording when a representative test already exists.
- Truth comes from executing the real application, not generating fake UI footage.
- External competition is real: PageBolt, PushPlay, `playwright-recast`, `playwright-demo-recorder`, and many repository-specific demo-video workflows.
- Must differentiate on reproducible demo-as-code and agent-built test reuse; otherwise this remains crowded.

### 3. AssetMemory — governed media memory for coding/creative agents

**Outcome:** an agent searches and reuses approved B2 assets and brand constraints; Genblaze generates only when nothing suitable exists.

- Strong personal fit for coding-agent users.
- B2 is naturally load-bearing as the library and provenance store.
- Genblaze is less central on reuse-heavy paths and would need a justified generation/refinement loop.
- External competition is strong: Cloudinary, ImageKit, Frontify, Aprimo, and others expose asset operations to agents/MCP.
- Event overlap: Reprise, media-vault projects, and provenance libraries cover important parts of this job.

### 4. MediaSpec as a feature, not a product

Any domain product can expose a simple contract view:

```text
caption coverage     PASS
audio description   NEEDS REVIEW
low-data rendition  PASS
remote B2 bytes      VERIFIED
```

This preserves the personally compelling part of MediaSpec without entering the event as another generic QC console.

## Provisional recommendation

**Leading direction:** validate ReachPack / AccessSpec first—not because the component market is empty, but because the integrated publication outcome provides a coherent own-game thesis.

Why it currently leads:

- immediately understandable user outcome;
- visibly multimodal pipeline;
- both Genblaze and B2 are essential;
- MediaSpec becomes differentiated quality enforcement;
- it has a coherent user outcome independent of whether nearby projects exist; the initial public `genblaze` scan did not expose the same integrated publication-bundle contract, while broader research did find established competitors for individual components;
- a short source video can demonstrate value within the three-minute judge video.

This is not yet a build authorization. The technical spike must prove one real source video can produce at least captions, one generated accessibility track or descriptive artifact, a low-data rendition, B2 storage, a manifest, and a readable pass/review report within the available time and provider budget.

## Sources

- Event: https://backblaze-generative-media.devpost.com/
- Resources/inspiration: https://backblaze-generative-media.devpost.com/resources
- Unpublished gallery: https://backblaze-generative-media.devpost.com/project-gallery
- Sponsor launch post: https://www.backblaze.com/blog/backblaze-generative-media-hackathon-build-with-b2-genblaze-and-gmi-cloud
- Genblaze issues: https://github.com/backblaze-labs/genblaze/issues
- Point-in-time public repository scan: `../10-sources/public_genblaze_repository_scan_2026-07-27.json`
