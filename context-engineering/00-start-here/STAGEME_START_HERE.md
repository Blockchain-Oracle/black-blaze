# StageMe — Start Here

> **Current decision:** StageMe is the active product direction for a feasibility-first build. The full application is gated on proving the magical retained-performance transformation.
>
> **Canonical product file:** `../09-planning/STAGEME_PRODUCT_SPEC.md`.
>
> **Pre-call verdict:** conditionally ready; an owner-supplied F1 has passed private local ingest/QC, but no provider/model call is authorized or executed yet.
>
> **Last updated:** 2026-07-27 17:12 UTC.

## What StageMe is

> **StageMe turns your rough sung performance into an arranged 8–15 second stage moment while keeping your real voice literally present, then lets you change one generated layer or bounded section without starting over.**

```text
real authorized performance
→ separate source-conditioned accompaniment
→ mix that literally retains the source
→ intentional audiovisual stage
→ one bounded child revision
→ durable B2 project and provenance
```

## What StageMe is not

- not generic text-to-song;
- not “upload a voice and clone it”;
- not a full DAW;
- not a photo/avatar app;
- not a generic AI-media dashboard;
- not a promise to support every input modality;
- not a complete song or music-video generator in the first build;
- not two hackathon entries;
- not proven until real fixtures pass the spike.

## Required read order

1. `../09-planning/STAGEME_PRODUCT_SPEC.md` — canonical behavior, truth boundaries, and acceptance
2. `../09-planning/STAGEME_PRECALL_READINESS_REPORT.md` — current evidence, costs, blockers, and verdict
3. `../09-planning/STAGEME_FIRST_CALL_RUNBOOK.md` — exact first authorized AnyAccomp procedure
4. `../09-planning/STAGEME_F1_RECORDING_CHECKLIST.md` — under-five-minute user fixture guide
5. `../09-planning/STAGEME_SPIKE_PROTOCOL.md` — experiments and stop conditions after the first call
6. `../06-technical/STAGEME_SYSTEM_DESIGN.md` — APIs, schemas, pipeline, storage, failure recovery
7. `../08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md` — libraries and projects to learn from
8. `../09-planning/STAGEME_AGENT_BUILD_HANDOFF.md` — build order and agent constraints
9. `../09-planning/STAGEME_FEASIBILITY_AND_JUDGE_FIT_2026-07-27.md` — feasibility evidence at selection time
10. `../09-planning/DECISION_LOG.md`, `RISK_REGISTER.md`, `OPEN_QUESTIONS.md`
11. `../06-technical/GENBLAZE_GUIDE.md`, `B2_GUIDE.md`
12. `../10-sources/SOURCE_LEDGER.md`

## Ready-to-run agent prompt

Use [`STAGEME_PRECALL_AGENT_PROMPT.md`](../09-planning/STAGEME_PRECALL_AGENT_PROMPT.md) to launch the complete zero-cost pre-call research and execution-readiness pass. It authorizes research, validation, preparation artifacts, and Git delivery while stopping before paid inference, real credentials, human-audio upload, B2 writes, or deployment.

If a derivative summary conflicts with the canonical product specification, the product specification wins unless a later decision-log entry explicitly supersedes it.

## The first real deliverable

Do not begin with the complete website.

Produce one inspectable artifact bundle:

```text
source recording
+ consent
+ normalized source
+ AnyAccomp and ACE candidate layers/mixes
+ deterministic QC
+ human comparison
+ accepted arrangement
+ staged video
+ one revision branch
+ manifests and hashes
```

The first proof answers:

> Does this rough performance become something surprisingly finished while still sounding unmistakably connected to the person?

## Current strongest paths

### Primary preservation candidate

**AnyAccomp**, pinned source `82604b5e3107944ad4c49fc64900b86118ae2c62`.

Its official inference code writes:

- separate generated accompaniment;
- mixture computed from generated accompaniment plus the original vocal waveform.

This directly supports literal source retention, but quality, hardware, latency, and accepted-result cost remain unreproduced in StageMe.

The official Hugging Face Space is currently unavailable and no official maintained hosted inference mapping was found. The first call therefore uses a dedicated approved GPU worker. StageMe keeps only the separate accompaniment from upstream, constructs its own gain-staged float premaster, and runs the repository null-test utility.

The first-call control path is pinned to `runpodctl` 2.7.2. Its released binary/source require an absolute RFC 3339 datetime for `--terminate-after`, despite a conflicting prose-doc duration example. The runbook computes and records that deadline immediately before an explicitly Secure Cloud, single-data-center provision and requires authenticated-console confirmation before F1 transfer because the CLI response omits the configured deadline.

### Secondary arrangement/editing candidate

**ACE-Step 1.5**, pinned source `6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0`.

Relevant base-model tasks:

- `lego` — generate a named instrument in context;
- `complete` — complete a partial track with specified instruments;
- `repaint` — regenerate a bounded interval.

Test `lego` first for separate layers, `complete` as a comparison, and `repaint` only after an accepted parent exists.

### Required visual path

A deterministic audio-reactive stage that works without paid video generation.

### Optional visual enhancement

Official Replicate `wan-video/wan-2.2-s2v`, observed at $0.02/output-second on 2026-07-27. It may replace only a 3–5 second interval; the complete deterministic stage remains available underneath it. It is optional until quality, latency, cost per accepted shot, safety, and preference are measured.

## Evidence labels

Every capability must be labeled:

```text
advertised
→ documented
→ reachable
→ implemented
→ reproduced
→ product-proven
```

Current StageMe core status: **implemented upstream, not reproduced in the StageMe environment**.

## Known blockers

- an owner-supplied 14.256-second F1 is technically ready outside Git and its fixture-scoped voice/backing-media rights attestations are complete; provider-processing consent remains unset;
- no selected/approved NVIDIA GPU account, region, or live secure inventory;
- no measured AnyAccomp or ACE quality/latency/VRAM;
- no approved hosted-inference budget;
- no real B2 credentials/canary in the build environment;
- Revideo built and rendered once, but two immediate rerenders failed; its 15-second StageMe sync/font/container/deployment benchmark remains red;
- provider/region-specific processing consent and final retention wording need owner approval;
- no application implementation exists yet.

These are explicit work items, not permission to use mocks as proof.

## What can proceed without those blockers

- synthetic F0 plumbing fixture;
- schemas and contracts;
- deterministic media inspection/QC;
- local artifact/version store;
- lock-set verification;
- provider adapter scaffolding and compliance tests using fakes;
- deterministic renderer prototype using synthetic or properly licensed audio;
- deployment planning;
- consent and deletion-flow implementation;
- B2 adapter tests without claiming the real account path.

These zero-cost preparation items now have a concrete readiness report, runbook, recording checklist, consent template, preflight, null-test utility, and tests. Their existence does not promote the media transformation above implemented.

## Hackathon fit

Stage 1 requires legitimate generative-media, Genblaze, and B2 use.

Stage 2 equally scores:

1. real-world utility;
2. production readiness;
3. meaningful B2 integration;
4. meaningful Genblaze orchestration.

Tie-break order starts with utility. The demo therefore begins with the rough source and finished result, not architecture.

## Core judge proof

```text
0:00 rough source
0:10 arranged/staged reveal
0:35 one bounded revision
1:00 locked assets and versions
1:30 real Genblaze progress/fallback
2:00 B2 source/candidates/manifests
2:30 fetched-byte verification and close
```

The exact demo script is written only after real generation timings are measured.

## Copyable continuation prompt

```text
Continue StageMe from /workspace/black-blaze.

Read the required files listed in context-engineering/00-start-here/STAGEME_START_HERE.md. Treat STAGEME_PRODUCT_SPEC.md as canonical. The first goal is the retained-performance artifact bundle, not a broad UI.

Preserve the user's real source recording as an immutable audible layer. Use AnyAccomp/ACE only according to their verified evidence levels. Do not make paid calls, use secrets, deploy, commit, push, or broaden scope without authorization. Run real tests, retain artifacts/hashes/configs, and report blockers honestly.
```
