# StageMe Agent Build Handoff

> **Historical handoff:** decision D-014 superseded StageMe's active-selection status on 2026-07-28. Do not execute this handoff unless a later owner decision explicitly reselects StageMe. It authorizes no paid call, secret use, deployment, commit, or push by itself.

## 1. Required read order

1. `../00-start-here/STAGEME_START_HERE.md`
2. `STAGEME_PRODUCT_SPEC.md` — canonical product authority
3. `STAGEME_PRECALL_READINESS_REPORT.md` — current evidence, blockers, and costs
4. `STAGEME_FIRST_CALL_RUNBOOK.md` — exact authorized F1/AnyAccomp procedure
5. `STAGEME_F1_RECORDING_CHECKLIST.md` — fixture instructions
6. `STAGEME_SPIKE_PROTOCOL.md` — evidence gates
7. `../06-technical/STAGEME_SYSTEM_DESIGN.md` — interfaces and architecture
8. `../08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md` — inspiration and library ledger
9. `STAGEME_FEASIBILITY_AND_JUDGE_FIT_2026-07-27.md` — research depth at selection time
10. `RISK_REGISTER.md`, `OPEN_QUESTIONS.md`, `DECISION_LOG.md`
11. `../06-technical/GENBLAZE_GUIDE.md`, `../06-technical/B2_GUIDE.md`
12. `../10-sources/SOURCE_LEDGER.md`

For the StageMe candidate contract, `STAGEME_PRODUCT_SPEC.md` wins. Repository-level selection and routing are controlled by later decision-log entries; D-014 currently leaves StageMe unselected.

## 2. Current mission

Prove this one transformation:

```text
authorized 8–15 second rough sung performance
→ separate source-conditioned accompaniment or instrument layer
→ mix that literally retains the original source
→ one polished 8–15 second audiovisual stage moment
→ one child revision that preserves locked assets
```

The first deliverable is the artifact bundle described in `STAGEME_SPIKE_PROTOCOL.md`, not a landing page.

## 3. Non-negotiable boundaries

Do not:

- claim humming, beatboxing, spoken lyrics, voice cloning, full songs, or photoreal performers as supported before their gates pass;
- substitute unrelated text-to-music and call it source-conditioned;
- regenerate the user's singing voice and describe it as retained;
- use copyrighted or third-party vocal fixtures without permission;
- store user media in Git;
- commit secrets, signed URLs, raw credentials, or historical tokens;
- make paid calls without a stated budget and explicit authorization;
- make Wan S2V mandatory;
- build a generic dashboard or full DAW;
- copy competitor branding, copy, UI, or proprietary assets;
- report a model run as successful without inspectable media, exact config, hashes, and metrics;
- overwrite parent versions or locked assets;
- build two submissions by default;
- treat MediaSpec as the selected user-facing product.

MediaSpec-style QC, validation, manifests, and recovery remain useful internal components.

## 4. Evidence discipline

Label claims:

```text
advertised | documented | reachable | implemented | reproduced | product-proven
```

A coding agent may promote a claim only when the produced artifact and report support the next level.

Examples:

- finding `task_type="lego"` in ACE-Step source → implemented;
- executing it on F1 and storing output → reproduced;
- meeting quality/latency/cost/recovery gates repeatedly → product-proven.

## 5. Work sequencing

### Track A — Core media proof (critical path)

#### A0. Fixture and environment readiness

Deliver:

- fixture directory outside Git;
- consent records;
- environment capture;
- F0 synthetic plumbing fixture;
- F1 user-owned sung fixture before qualitative execution.

Zero-cost readiness tooling already exists:

- `scripts/stageme_preflight.py` for phase-aware, zero-secret environment checks;
- `scripts/stageme_null_test.py` for literal-retention verification;
- `.env.example` for names-only configuration;
- `templates/STAGEME_CONSENT.example.json` for a copied, user-specific consent record.

Blockers:

- no authorized F1;
- no GPU/endpoint;
- no approved paid budget when using a hosted endpoint.

Do not ask for F1 until the selected worker provider/region, retention, deletion, and spend cap can be disclosed.

#### A1. Deterministic ingest and QC

Implement:

- ffprobe inspection;
- SHA-256;
- decode, downmix, and resample F1 to the canonical processing format with the
  exact commands recorded;
- do not trim, fade, or gain-adjust F1 unless a later explicit, versioned
  experiment authorizes and records that transformation; apply such operations
  only to generated layers or downstream mixes otherwise;
- duration/silence/clipping/format validation;
- immutable original and canonical normalized asset records.

Acceptance:

- unit tests cover corrupt, silent, too-long, and valid audio;
- processing is reproducible;
- no shell interpolation from user input;
- F0 artifact report exists.

#### A2. AnyAccomp direct spike

Start from pinned upstream `82604b5e3107944ad4c49fc64900b86118ae2c62` in an isolated environment/container.

Use stock Python 3.9 separately from the Python 3.11/3.12 StageMe control/Genblaze environment. The official hosted Space is currently unavailable; follow `STAGEME_FIRST_CALL_RUNBOOK.md` on an approved dedicated worker.

Do not modify upstream code before reproducing its stock inference on a safe fixture unless setup demands a documented patch.

Deliver:

- exact environment/build script;
- checkpoint/license record;
- direct inference command;
- accompaniment, StageMe-owned float premaster, and upstream mixture only as diagnostic evidence;
- null-test utility;
- measurements and report.

Acceptance:

- separate accompaniment exists;
- mixture minus accompaniment reconstructs canonical source within declared tolerance;
- no unsupported quality claim.

#### A3. ACE-Step direct spike

Start from pinned upstream `6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0`.

Run in this order:

1. `lego` one instrument;
2. `complete` comparison;
3. `repaint` only after an accepted parent exists.

Deliver the same evidence shape as A2.

#### A4. Candidate comparison and magic gate

- build at most two accepted-budget mix candidates;
- blind human evaluation;
- before/after preview;
- decide pass, reframe, or stop.

Do not proceed to broad app implementation if source connection and emotional lift fail.

### Track B — Deterministic platform (may proceed alongside A)

#### B0. Contracts

Implement JSON Schemas and generated/parallel Python and TypeScript types for:

- SourcePerformance;
- ConsentRecord;
- CreativeDirection;
- AssetRecord;
- EvaluationRecord;
- BudgetPolicy;
- ProjectVersion;
- RevisionRequest;
- RunEvent.

Acceptance:

- examples in system design validate;
- unknown forward-compatible fields are handled deliberately;
- cross-language contract tests pass.

#### B1. Artifact store abstraction

Implement local filesystem backend first, with B2 backend conforming to the same interface.

Required operations:

- put immutable asset;
- fetch/stream;
- head/metadata;
- verify hash;
- list project/version assets;
- delete with journal;
- create durable reference without persisting signed URL.

#### B2. Version and lock verification

Implement parent/child version creation and hash-lock assertions before generative revision.

Acceptance:

- child cannot overwrite parent;
- unchanged locked assets are reused;
- parent remains restorable;
- tests detect lock violations.

### Track C — Renderer (may prototype alongside A using F0/licensed audio)

#### C0. Validate the default renderer

Use Revideo with a pinned Chromium/browser build as the intended deterministic renderer. Its 2026-07-27 canonical build and first smoke render passed, but two immediate rerenders failed with the current frame-detachment issue. Keep MoviePy/direct FFmpeg as the Phase-0 fallback until the full repeatability benchmark passes. Motion Canvas remains a pattern/alternative reference rather than a second default implementation.

The renderer must implement:

```text
render(StageRenderSpec) -> video AssetRecord
```

#### C1. Deterministic stage prototype

Required visual vocabulary:

- stage world, not dashboard;
- audio-driven lights/shapes;
- intentional typography;
- waveform or energy trace derived from accepted audio;
- deterministic motion/camera;
- 720p, low-data, and audio-only outputs.

Acceptance:

- renders from F0/licensed audio;
- media QC passes;
- repeatable spec;
- no paid video dependency;
- reviewer response is not “generic visualizer template.”

#### C2. Optional Wan branch

Only after A4 and C1 pass and budget is authorized.

Generate only a 3–5 second replaceable hero interval. Use a stylized silhouette, stage sculpture, instrument, or abstract living artwork rather than turning StageMe into a portrait/avatar product. Use human approval before submission and retain the deterministic C1 interval/output regardless.

### Track D — Genblaze adapters (after direct inference semantics are known)

#### D1. AnyAccomp provider adapter

For direct local inference, implement a Genblaze `SyncProvider` only inside the dedicated GPU worker; it must never block the API process. Keep outer job state durable, initially cap concurrency at one job/GPU, and make timeout/orphan cleanup explicit. If AnyAccomp runs behind a queued hosted service, use `BaseProvider` with real submit/poll/fetch semantics instead. Return the separate accompaniment; a following deterministic StageMe mixer creates and null-tests the accepted premaster. Run the current 16-method `ProviderComplianceTests` plus StageMe retention tests.

#### D2. ACE-Step polling BaseProvider

Map release/query/audio endpoints. Support only StageMe's permitted task types. Persist submit checkpoint before polling.

#### D3. Real pipeline

Replace direct spike calls with provider invocations through Genblaze. Compare resulting bytes/config against direct path where deterministic equivalence is expected.

Acceptance:

- provider compliance passes;
- progress events flow;
- retry/error classes are explicit;
- cost remains bounded;
- artifacts/manifests persist.

### Track E — Product vertical slice (only after A4 passes)

#### E0. API

Implement project/source/run/events/accept/revise/version/delete endpoints from system design.

#### E1. Minimal web flow

Build only:

```text
Record → Direct → Progress → Reveal → Revise → History
```

No feed, collaboration, marketplace, full editor, avatar builder, or settings sprawl.

#### E2. B2 production path

- private bucket;
- short-lived presigned PUT or proxied upload;
- source/candidate/version layout;
- fetched-byte verification;
- deletion boundary.

#### E3. Recovery and demo

- retryable failure;
- terminal failure;
- worker interruption/resume;
- deterministic visual fallback;
- seeded complete project;
- one live bounded operation.

## 6. Parallelization rules

Safe parallel work before A4:

- Agent A: media spike;
- Agent B: schemas, QC, local artifact/version store;
- Agent C: deterministic renderer prototype;
- Agent R: reference/library verification.

Do not start independent agents on:

- competing product definitions;
- broad frontend feature work;
- alternate voice-cloning products;
- a second submission;
- full deployment before media gates.

Shared contracts must be merged before dependent tracks diverge.

## 7. Definition of done by milestone

### M0 — Documentation ready

- canonical spec;
- system design;
- spike protocol;
- reference ledger;
- source ledger;
- agent handoff;
- readiness report, first-call runbook, recording checklist, consent/environment templates, preflight, null-test utility, and tests;
- navigation and validation.

### M1 — Core media reproduced

- F1 authorized fixture;
- one separate source-conditioned accompaniment/layer;
- accepted retained-vocal mix;
- report with metrics and hashes.

### M2 — Magic and revision proven

- blind preference gate passes;
- before/after is legible;
- one bounded child revision preserves lock set.

### M3 — Reliable audiovisual artifact

- deterministic stage is polished;
- media exports pass;
- optional S2V evaluated but nonessential.

### M4 — Real production path

- Genblaze executes real providers;
- B2 stores full lifecycle;
- progress/recovery/cost controls work;
- manifests verify against fetched bytes.

### M5 — Submission ready

- public functional app;
- code access;
- <=3-minute truthful demo;
- official requirements checked;
- no hidden mocks or rehearsed-only critical path.

## 8. Required pull-request or change report

Every implementation change must report:

- product contract affected;
- evidence claim changed;
- files and interfaces changed;
- exact commands/tests executed;
- real outputs and paths;
- known failures;
- cost/provider side effects;
- security/license implications;
- next gate.

A green unit test is not a substitute for a real media artifact when the claim concerns generated media.

## 9. Copyable agent kickoff prompt

```text
You are implementing StageMe in /workspace/black-blaze.

Read, in order:
1. context-engineering/00-start-here/STAGEME_START_HERE.md
2. context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md
3. context-engineering/09-planning/STAGEME_PRECALL_READINESS_REPORT.md
4. context-engineering/09-planning/STAGEME_FIRST_CALL_RUNBOOK.md
5. context-engineering/09-planning/STAGEME_F1_RECORDING_CHECKLIST.md
6. context-engineering/09-planning/STAGEME_SPIKE_PROTOCOL.md
7. context-engineering/06-technical/STAGEME_SYSTEM_DESIGN.md
8. context-engineering/08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md
9. context-engineering/09-planning/STAGEME_AGENT_BUILD_HANDOFF.md

The canonical product promise is retained real performance + source-conditioned accompaniment + staged reveal + bounded revision. Do not broaden scope or replace the source with synthetic vocals.

Before editing, inspect git status and preserve existing uncommitted research. Work only on the assigned track. Do not make paid calls, use credentials, deploy, commit, push, or modify another track's contract without authorization. Execute and verify every requested artifact. Label model claims by evidence level and return exact paths, hashes, commands, tests, blockers, and real outputs.
```

## 10. Immediate blockers requiring a human or configured environment

- one authorized F1 sung fixture;
- approved secure GPU account/region/live inventory capable of pinned AnyAccomp; ACE comes after the first result;
- explicit first-session spend cap and provider funding approval;
- B2 bucket and scoped key for real storage canary;
- deployment target selection;
- final data-retention policy;
- consent copy approval.

Agents must surface these blockers; they must not fabricate replacements.
