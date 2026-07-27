# MediaSpec Project Brief

> Status: selected product direction. The immediate gate is a real end-to-end technical spike; implementation details remain provisional until that spike passes.

## One sentence

For developers and teams shipping generative-media workflows, **MediaSpec** turns a creative brief plus an explicit output contract into a generated, validated, recovery-ready media asset whose accepted bytes and run evidence are durably stored in Backblaze B2.

## Product promise

**Generated media should not ship merely because a model returned a file. It should ship only after it passes an auditable contract.**

MediaSpec generates candidate media, checks concrete requirements, explains failures, retries/repairs/falls back within a budget, and delivers only an accepted artifact with verification evidence.

## Primary user and problem

- **Primary user:** developer or small product team operating an automated image/audio/video pipeline.
- **Current workaround:** inspect outputs manually, write one-off ffmpeg/ffprobe scripts, rerun provider calls by hand, and keep assets/logs in unrelated systems.
- **Pain:** wrong duration, dimensions, codec, missing captions/audio, corrupt objects, incomplete metadata, silent provider failure, and expensive full reruns.
- **Immediate outcome:** a red/green validation result, exact failure reasons, automatic recovery, and a verified accepted asset.
- **Purchase signal:** the entrant stated this is a product they would personally buy; this is stronger founder-product-fit evidence than the earlier concepts.

## Core workflow

1. User enters a creative brief and selects or edits a media contract.
2. Genblaze generates one or more candidates and streams run progress.
3. MediaSpec applies cheap deterministic checks first and an optional clearly labeled semantic evaluator last.
4. Failed candidates trigger bounded repair, retry, or provider fallback.
5. Inputs, candidates, reports, manifests, and accepted output are stored in B2.
6. MediaSpec fetches the accepted remote object, verifies its bytes, and presents a green delivery report.

## Example contract

```yaml
kind: narrated-short-video
duration_seconds:
  min: 12
  max: 15
aspect_ratio: "9:16"
video_codec: h264
captions_required: true
transcript_coverage_min: 0.95
audio_required: true
loudness_lufs:
  min: -16
  max: -14
max_file_size_mb: 25
max_attempts: 2
max_estimated_cost_usd: 0.75
manifest_required: true
remote_hash_verification: true
```

## MVP checks

### Deterministic and auditable

- file exists and is non-empty;
- file is decodable;
- duration is within range;
- resolution/aspect ratio matches;
- video/audio codecs are allowed;
- audio stream exists when required;
- loudness and clipping are within limits;
- caption track/file exists;
- transcript coverage meets threshold;
- file size is within limit;
- provider/model/run metadata is complete;
- local and fetched B2 SHA-256 values match.

### Optional model judgment

At most one constrained evaluator may answer a requirement such as whether a specified visible element is present. The UI and report must label this as a model judgment, not objective truth.

## Genblaze role

- generation and transformation steps;
- concurrent candidate fan-out where affordable;
- streaming progress;
- bounded retry and provider fallback;
- repair/refinement loop;
- parent-child run lineage;
- canonical manifests for rejected and accepted attempts.

## Backblaze B2 role

Suggested key layout:

```text
projects/{project_id}/runs/{run_id}/
├── input/
│   ├── brief.json
│   └── media-spec.yaml
├── candidates/{candidate_id}/
│   ├── media.*
│   ├── validation.json
│   └── manifest.json
├── accepted/
│   ├── media.*
│   ├── validation.json
│   └── manifest.json
└── run-summary.json
```

B2 is responsible for durable source/candidate/final storage, historical run evidence, judge-facing retrieval, and remote-byte verification. It must not be used merely as a final upload destination.

## First technical spike: pass/fail gate

The concept is not considered technically validated until a real run proves:

```text
generate a small asset
→ fail one real deterministic requirement
→ repair, retry, or fall back
→ pass the second candidate
→ store all evidence in B2
→ fetch the accepted object
→ verify fetched bytes against the manifest
```

## Demo spine

1. Select a prebuilt **Vertical Launch Video** contract.
2. Submit a short brief.
3. Show candidate A fail with an immediately understandable red result.
4. Show MediaSpec recover automatically.
5. Show candidate B pass in green.
6. Play the accepted output.
7. Show the B2-backed report, lineage, and matching remote hash.

Use a pre-seeded run for instant judge comprehension and a small live run to prove the integration.

## Must ship

- one media kind only;
- one editable contract preset;
- at least five deterministic checks;
- one genuine failure and bounded recovery path;
- Genblaze run/manifest evidence;
- B2 storage for input, failed candidate, accepted candidate, and reports;
- remote-byte verification;
- polished red-to-green result UI;
- public judge-accessible deployment and sub-three-minute demo.

## Nice to have

- multiple provider fan-out;
- contract templates for common publishing destinations;
- run comparison/history;
- downloadable JSON report;
- one constrained semantic evaluator;
- GitHub/CI integration.

## Explicitly out of scope

- universal aesthetic scoring;
- full creative-suite editing;
- general-purpose AI observability;
- support for every media modality;
- autonomous product-demo recording;
- unlimited retries;
- C2PA/blockchain authenticity claims;
- production billing or enterprise access control.

## Primary risks

- provider/model access is not yet proven;
- video generation can be slow and expensive;
- subjective evaluation can weaken credibility;
- a generic dashboard would overlap existing multimodal observability tools;
- a thin B2 upload or thin Genblaze call would fail the sponsor-fit test.

## Current decision

Build no broad feature set until the pass/fail/recovery/B2-verification spike succeeds. If the spike fails quickly, use AccessForge as the fallback concept rather than weakening MediaSpec into a superficial demo.
