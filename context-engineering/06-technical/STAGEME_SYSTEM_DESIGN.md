# StageMe System Design and Interface Contracts

> Historical design: decision D-014 left StageMe unselected on 2026-07-28. Read `../09-planning/STAGEME_PRODUCT_SPEC.md` only when evaluating this preserved candidate; do not treat this as the current build architecture.
>
> Pinned technical evidence: Genblaze `293beade3e705d69b29dbf57402800f8a868313f`, ACE-Step 1.5 `6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0`, AnyAccomp `82604b5e3107944ad4c49fc64900b86118ae2c62`.

## 1. Design principles

1. Prove the retained-vocal arrangement before building the full web shell.
2. Keep original, deterministic, and generated assets structurally separate.
3. Never overwrite accepted assets or project versions.
4. Make fragile generation optional behind a deterministic fallback where possible.
5. Persist enough state to resume after process or provider failure.
6. Enforce cost, duration, and retry budgets before provider submission.
7. Expose truth and progress without making infrastructure the product.
8. Use ordinary phone/browser capture; server owns the heavy compute.

## 2. Target repository shape

Create this only after the media spike passes Gate 1 and Gate 2:

```text
black-blaze/
├── apps/
│   └── web/                         # Next.js/React capture, progress, reveal, revision
├── services/
│   ├── api/                         # Python 3.11+ FastAPI application
│   ├── worker/                      # Genblaze pipeline and durable job runner
│   └── renderer/                    # deterministic audiovisual renderer
├── packages/
│   ├── contracts/                   # JSON Schema + generated Python/TypeScript types
│   ├── genblaze-anyaccomp/          # dedicated-worker adapter; SyncProvider locally, BaseProvider if hosted
│   ├── genblaze-acestep/            # polling BaseProvider adapter
│   ├── media-qc/                    # deterministic ffprobe/audio/video checks
│   └── project-manifest/            # StageMe manifest/version helpers
├── experiments/
│   └── retained-vocal-spike/        # executable spike and fixture results
├── tests/
│   ├── fixtures/                    # synthetic/licensed test fixtures only
│   ├── contract/
│   ├── integration/
│   └── e2e/
├── context-engineering/             # research and decisions
└── infra/                            # container/deployment definitions after spike
```

Do not put user recordings into Git.

## 3. Build phases

### Phase 0 — executable media spike

No frontend. A CLI or test harness takes one local authorized fixture and writes the full artifact folder.

Pass requirements:

- separate source and accompaniment assets;
- accepted mix;
- before/after preview;
- one revision branch;
- metrics and evaluation report;
- reproducible command and pinned dependencies.

### Phase 1 — local product vertical slice

- FastAPI;
- local filesystem storage through the same storage interface;
- Genblaze provider adapters;
- deterministic renderer;
- minimal web capture/reveal UI;
- one project and one user.

### Phase 2 — B2 and durable execution

- private B2 bucket;
- presigned PUT upload or API-proxied upload;
- durable run checkpoints;
- B2 sinks and fetched-byte verification;
- job recovery;
- project/version browser.

### Phase 3 — optional provider enhancement

- Replicate Wan S2V hero shot;
- strict candidate budget;
- deterministic stage retained as fallback;
- provider failure/rejection test.

### Phase 4 — polish and submission

- mobile capture quality;
- progress/recovery UI;
- deletion and consent flows;
- seeded demo plus one bounded live operation;
- judge-visible B2/Genblaze proof;
- deployment and demo runbook.

## 4. Service boundaries

### Web application

Responsibilities:

- record/upload;
- consent capture;
- creative direction;
- project creation;
- stage-level progress via SSE;
- source/arranged comparison;
- candidate acceptance;
- bounded revision request;
- project history, export, and delete.

Non-responsibilities:

- provider credentials;
- direct GPU access;
- permanent B2 credentials;
- media mixing;
- authoritative project state.

### API service

Responsibilities:

- authentication boundary if added;
- request validation;
- short-lived upload authorization;
- project/version metadata;
- consent checks;
- budget checks;
- job enqueue/resume/cancel;
- SSE event relay;
- download authorization;
- deletion workflow.

### Worker

Responsibilities:

- Genblaze pipeline invocation;
- deterministic media analysis;
- provider lifecycle;
- artifact hashing and storage;
- quality gates;
- version creation;
- manifest verification;
- progress/checkpoint events;
- retry and fallback.

The StageMe control/QC and Genblaze environment is Python 3.11 or 3.12. The pinned stock AnyAccomp environment is Python 3.9 with a CUDA 12.1-era Torch stack. Treat them as separate processes/containers with an explicit file/job contract; do not solve the version conflict by importing the model into the API or Genblaze control process.

### Renderer

Responsibilities:

- consume a versioned `StageRenderSpec`;
- derive motion only from accepted audio/features and explicit visual inputs;
- render video deterministically for the same spec and toolchain;
- return media metadata and SHA-256;
- never invoke a paid provider implicitly.

### Metadata database

Use PostgreSQL for deployed multi-process execution. SQLite with WAL is acceptable only for the Phase 0/1 single-process spike.

The database indexes projects, jobs, versions, user decisions, and B2 object keys. B2 remains the durable media/project record; the database is not a substitute for object manifests.

### Job queue

The spike may run synchronously. The deployed build needs a durable queue or resumable worker process. Select one maintained open-source Python queue after deployment constraints are known; do not hide long GPU work inside FastAPI `BackgroundTasks`.

Required semantics:

- stable `job_id`;
- idempotency key;
- explicit retry count;
- heartbeat/lease;
- terminal failure reason;
- resume from persisted checkpoint;
- cancel before an additional paid candidate starts.

## 5. State machines

### Project state

```text
DRAFT
→ SOURCE_UPLOADED
→ READY_TO_GENERATE
→ GENERATING
→ AWAITING_ACCEPTANCE
→ STAGING
→ READY
→ REVISING
→ READY
```

Terminal/side states:

```text
FAILED_RECOVERABLE
FAILED_TERMINAL
DELETION_PENDING
DELETED
```

### Run state

```text
CREATED
→ PREFLIGHT
→ ANALYZING
→ ARRANGING
→ VALIDATING_AUDIO
→ AWAITING_SELECTION
→ GENERATING_STAGE_ART
→ RENDERING
→ VERIFYING
→ COMPLETED
```

A stage transition occurs only after its output and checkpoint are persisted.

## 6. Public API contract

Exact framework syntax may vary; endpoint semantics must not.

### Create project

```http
POST /v1/projects
```

Request:

```json
{
  "title": "Rooftop chorus",
  "retention_days": 30
}
```

Response contains `project_id`, initial version/state, and upload instructions.

### Authorize source upload

```http
POST /v1/projects/{project_id}/source-upload
```

Prefer one of:

1. backend issues a short-lived presigned S3-compatible **PUT** URL; or
2. browser uploads through the API.

Backblaze's S3-compatible API does not support browser presigned `POST` uploads. Do not design around that AWS pattern.

Never persist or log the signed query string.

### Register uploaded source and consent

```http
POST /v1/projects/{project_id}/source
```

Request references the B2 object key and includes consent fields. The API must verify ownership, object existence, size, media type, and checksum before making the project generatable.

### Start arrangement

```http
POST /v1/projects/{project_id}/runs
Idempotency-Key: <uuid>
```

```json
{
  "source_asset_id": "ast_...",
  "creative_direction": "Warm Afrobeats-pop, victorious but intimate",
  "candidate_budget": 2,
  "max_compute_usd": 0.25,
  "audio_paths": ["anyaccomp", "ace_lego", "ace_complete"]
}
```

The server may narrow paths based on enabled capabilities but must return the actual plan.

### Stream progress

```http
GET /v1/runs/{run_id}/events
Accept: text/event-stream
```

Event:

```json
{
  "event_id": "evt_...",
  "run_id": "run_...",
  "stage": "ARRANGING",
  "status": "started",
  "message": "Building accompaniment",
  "attempt": 1,
  "cost_usd_so_far": 0.0,
  "occurred_at": "..."
}
```

Do not emit invented percentages.

### Accept candidate

```http
POST /v1/projects/{project_id}/candidates/{candidate_id}/accept
```

This freezes the candidate's asset references and starts the stage renderer. Acceptance is idempotent.

### Request revision

```http
POST /v1/projects/{project_id}/versions/{version_id}/revisions
```

```json
{
  "target": {
    "kind": "generated_layer",
    "asset_id": "ast_drums_v1",
    "start_seconds": 6.0,
    "end_seconds": 10.0
  },
  "instruction": "Make the drums softer and more spacious",
  "locked_asset_ids": [
    "ast_source_normalized",
    "ast_base_accompaniment",
    "ast_stage_art"
  ],
  "max_compute_usd": 0.15
}
```

### Read project/version

```http
GET /v1/projects/{project_id}
GET /v1/projects/{project_id}/versions
GET /v1/projects/{project_id}/versions/{version_id}
GET /v1/projects/{project_id}/versions/{version_id}/manifest
```

### Delete project

```http
DELETE /v1/projects/{project_id}
```

Deletion must be journaled, idempotent, and verified. Do not report deleted while retained provider copies or B2 objects remain silently pending. State the provider-side deletion boundary.

## 7. Core data contracts

Maintain JSON Schema as the language-neutral authority and generate Python/TypeScript models where practical.

### SourcePerformance

```json
{
  "asset_id": "ast_...",
  "project_id": "prj_...",
  "kind": "source_original",
  "object_key": "projects/prj_.../source/original.webm",
  "sha256": "...",
  "bytes": 123456,
  "media_type": "audio/webm",
  "duration_seconds": 12.4,
  "owner_attested": true,
  "consent_id": "cns_..."
}
```

### ConsentRecord

```json
{
  "consent_id": "cns_...",
  "project_id": "prj_...",
  "source_asset_sha256": "...",
  "scope": ["analysis", "arrangement", "render", "temporary_provider_processing"],
  "training_reuse": false,
  "third_party_voice": false,
  "accepted_at": "...",
  "policy_version": "1"
}
```

### CreativeDirection

```json
{
  "text": "Warm Afrobeats-pop, victorious but intimate",
  "requested_instruments": ["drums", "bass"],
  "avoid": ["aggressive distortion"],
  "visual_mood": "night rooftop, warm light"
}
```

The structured fields are derived suggestions and must retain the original text.

### AssetRecord

```json
{
  "asset_id": "ast_...",
  "role": "generated_accompaniment",
  "origin": "generated",
  "parent_asset_ids": ["ast_source_normalized"],
  "object_key": "...",
  "durable_url": null,
  "media_type": "audio/wav",
  "sha256": "...",
  "bytes": 1234567,
  "metadata": {
    "sample_rate": 24000,
    "channels": 1,
    "duration_seconds": 12.4
  },
  "provider": {
    "name": "anyaccomp",
    "model": "amphion/anyaccomp",
    "version": "82604b5e...",
    "params": {"n_timesteps": 50, "cfg": 3, "seed": 1024}
  }
}
```

### EvaluationRecord

```json
{
  "candidate_id": "cand_...",
  "deterministic": {
    "decodable": true,
    "duration_delta_seconds": 0.0,
    "clipped_samples": 0,
    "peak_dbfs": -1.2,
    "integrated_lufs": -15.1,
    "silence_ratio": 0.03
  },
  "human": {
    "source_connection": 4,
    "musical_coherence": 4,
    "shareability": 5,
    "notes": "Vocal remains clear; bass is slightly crowded"
  },
  "accepted": true
}
```

### ProjectVersion

```json
{
  "version_id": "ver_0002",
  "project_id": "prj_...",
  "parent_version_id": "ver_0001",
  "source_asset_id": "ast_source_normalized",
  "layer_asset_ids": ["ast_accomp_v1", "ast_drums_v2"],
  "stage_asset_ids": ["ast_stage_art", "ast_stage_mp4_v2"],
  "locked_asset_ids": ["ast_source_normalized", "ast_accomp_v1"],
  "revision_request_id": "rev_...",
  "manifest_asset_id": "ast_manifest_v2",
  "created_at": "..."
}
```

### BudgetPolicy

```json
{
  "max_audio_candidates": 2,
  "max_video_candidates": 1,
  "max_provider_retries": 1,
  "max_compute_usd": 0.5,
  "max_wall_seconds": 300,
  "require_human_approval_before_video": true
}
```

## 8. B2 object layout

```text
projects/{project_id}/
├── consent/{consent_id}.json
├── source/
│   ├── original/{sha256}.{ext}
│   └── normalized/{sha256}.wav
├── runs/{run_id}/
│   ├── plan.json
│   ├── checkpoints/{sequence}.json
│   ├── events/{sequence}.json
│   ├── analysis/media.json
│   ├── analysis/music.json
│   ├── candidates/{candidate_id}/...
│   └── manifest.json
├── versions/{version_id}/
│   ├── project.json
│   ├── mix/mix-spec.json
│   ├── audio/arrangement.wav
│   ├── visual/render-spec.json
│   ├── video/stage-720p.mp4
│   ├── exports/audio-low.mp3
│   ├── exports/video-low.mp4
│   └── manifest.json
└── tombstone.json                 # only during/after deletion workflow where legally appropriate
```

Use content-addressed keys for immutable assets where deduplication helps. Never place provider tokens, signed URLs, or raw secrets in object metadata.

## 9. Genblaze provider design

Pinned contract: `backblaze-labs/genblaze@293beade3e705d69b29dbf57402800f8a868313f`.

### `genblaze-anyaccomp`

For Phase 0/local execution, use `SyncProvider` **only inside a dedicated GPU worker** because inference is a blocking local call from Genblaze's perspective. Never execute it inline in the FastAPI request process.

Operational requirements:

- durable outer run/checkpoint exists before inference starts;
- worker concurrency is bounded to the measured per-GPU capacity, initially one job/GPU;
- timeout/cancellation and orphaned-work cleanup are explicit;
- model and checkpoints stay warm when affordable;
- the worker emits coarse progress/heartbeat events even if model internals do not;
- interrupted blocking inference resumes from the last durable stage, not from an invented provider job ID.

If AnyAccomp is deployed behind a queued/hosted service, implement Genblaze `BaseProvider` with real `submit`, `poll`, and `fetch_output` semantics instead of wrapping the network call as synchronous.

Required package:

```text
packages/genblaze-anyaccomp/
├── genblaze_anyaccomp/
│   ├── __init__.py
│   ├── provider.py
│   ├── _errors.py
│   └── py.typed
├── tests/
└── pyproject.toml
```

Entry point:

```toml
[project.entry-points."genblaze.providers"]
anyaccomp = "genblaze_anyaccomp:AnyAccompProvider"
```

`generate(step)` must:

1. validate one audio chain input;
2. resolve it to an authorized local file;
3. enforce duration/format limits;
4. invoke the pinned AnyAccomp pipeline;
5. write the separate accompaniment; retain the upstream raw mixture only as diagnostic evidence;
6. attach the accompaniment as a `file://` asset with specific MIME/audio metadata;
7. record model commit, config, steps, CFG, seed, latency, and memory metrics;
8. map errors explicitly;
9. never claim remote model discovery it cannot perform.

A following deterministic StageMe mixer—not the model provider—combines the immutable canonical source and accompaniment with recorded gains, writes a float premaster, and executes `scripts/stageme_null_test.py`. The un-gain-staged upstream mixture is never an accepted product asset.

### `genblaze-acestep`

Use `BaseProvider` for ACE-Step's HTTP job API:

- `submit(step)` → upload source and call `POST /release_task`; return task ID;
- `poll(task_id)` → call `POST /query_result`; cache terminal response;
- `fetch_output(task_id, step)` → retrieve output through `GET /v1/audio`, write/attach assets, and raise explicit errors.

Capabilities should declare audio output, audio chain input, supported task/model family, output formats, and maximum StageMe duration.

Support only the task types StageMe actually uses:

- `lego`;
- `complete`;
- `repaint` after its preservation test passes.

Do not expose the entire ACE-Step surface by default.

Current-main defensive requirements:

- validate source audio for `complete` even though upstream request validation currently omits it;
- pass and verify explicit matching duration;
- treat the API's in-memory job registry and unknown-ID-as-pending behavior as untrusted;
- apply an application-owned TTL/not-found policy and process-level timeout cleanup;
- for `repaint`, restore parent accompaniment samples outside the authorized interval/crossfade margins and verify them independently because upstream crossfade fields and splice behavior are mode-dependent.

### Replicate Wan S2V

Use Genblaze's existing Replicate connector where its current model family and input routing support the endpoint. Otherwise write a small StageMe-specific adapter only after verifying the installed connector contract.

Generate only a 3–5 second replaceable hero interval. Keep the deterministic Revideo render for the same interval and use it automatically when the S2V result fails, times out, drifts, or is rejected. Pin Revideo, Chromium, fonts, and the renderer container digest as one reproducibility unit.

Register mutable pricing at runtime with a StageMe-specific strategy:

```python
estimate = input_audio_duration_seconds * 0.02
# Reconcile the final amount against ffprobe(output).duration after fetch.
```

The connector's generic `per_output_second(0.02)` strategy cannot calculate this endpoint automatically when the fetched Asset lacks duration. Snapshot the pricing source/date and exact prediction version in configuration, display the estimate before submission, and reconcile after fetch.

### Provider rules

- `validate_chain_input_url()` for all chain assets;
- HTTPS and `file://` only;
- `normalize_params()` must be idempotent;
- explicit `ProviderErrorCode` mapping;
- no retry for auth, invalid input, content policy, or model errors;
- bounded retry for timeout, rate limit, and server errors;
- populate typed audio/video metadata;
- run `ProviderComplianceTests`;
- keep pricing external to model-family declarations;
- never store tokens in `provider_payload`.

## 10. Pipeline DAG

```text
ingest
  ↓
media_preflight ──────────────┐
  ↓                           │
normalize_source              │
  ↓                           │
analyze_source                │
  ├─ tempo/onsets/energy      │
  ├─ pitch/chroma             │
  └─ optional transcript      │
  ↓                           │
creative_brief                │
  ↓                           │
fan_out_audio_candidates      │
  ├─ anyaccomp                │
  ├─ ace_lego                 │
  └─ ace_complete             │
  ↓                           │
validate_candidates           │
  ↓                           │
human_acceptance checkpoint   │
  ↓                           │
mix_and_master                │
  ↓                           │
stage_art ── fallback theme   │
  ↓                           │
deterministic_stage_render    │
  ├─ optional Wan S2V after approval
  └─ deterministic result always retained
  ↓
final_media_validation
  ↓
B2 sink + manifest + fetched-byte verification
```

Do not call optional video before audio acceptance.

## 11. Deterministic quality gates

### Ingest

- decodable;
- supported codec/container;
- 8–15 seconds for canonical lane;
- file-size cap;
- one usable audio stream;
- finite sample values;
- no excessive leading/trailing silence;
- checksum recorded.

### Generated audio

- decodable;
- duration within tolerance;
- no missing/empty channel;
- no NaN/Inf;
- clipped sample count below threshold;
- peak and integrated loudness in configured range;
- source layer present in mix specification;
- output checksum recorded.

### Video

- decodable;
- expected duration, dimensions, and frame rate;
- expected audio stream;
- no black/silent output beyond threshold;
- mux duration drift within tolerance;
- H.264/AAC compatibility for primary share artifact;
- checksum recorded.

Taste, emotional connection, likeness, musical quality, and source recognizability remain human-review criteria.

## 12. Bounded revision verification

A revision test must compare parent and child manifests.

Required assertions:

```text
parent.source.sha256 == child.source.sha256
locked parent asset hashes == locked child asset hashes
child.parent_version_id == parent.version_id
requested target changed
parent remains fetchable and playable
```

For time-range audio repaint, also compare decoded audio outside the requested interval with an explicit tolerance. Do not call the edit bounded merely because it sounds similar.

## 13. Failure and recovery table

| Failure | Classification | Recovery |
|---|---|---|
| invalid/corrupt source | terminal input error | ask for rerecord; no provider call |
| source too long | terminal input error | deterministic trim UI; new consented source asset |
| GPU OOM | model error or capacity failure | lower supported config or alternate worker; do not infinite-retry |
| AnyAccomp Python/Genblaze environment conflict | terminal packaging error | keep the stock Python 3.9 model worker separate from the Python 3.11/3.12 control process |
| provider timeout/5xx | retryable | one bounded retry with checkpoint |
| auth/entitlement failure | terminal configuration | disable branch and surface operator action |
| accompaniment fails QC | candidate rejection | one alternate seed/path within budget |
| all source-conditioned candidates weak | product stop condition | do not disguise unrelated text-to-music |
| generated art fails | degraded branch | deterministic stage theme |
| Wan S2V fails/rejected | optional branch failure | retain deterministic stage |
| Revideo repeat render detaches/crashes | renderer failure | use pinned FFmpeg/MoviePy Phase-0 renderer; do not claim Revideo reproduced |
| B2 upload interrupted | recoverable | idempotent multipart/reupload then checksum verify |
| worker restart | recoverable | resume from last persisted checkpoint |
| manifest fetch mismatch | terminal integrity failure | quarantine output; do not publish |

## 14. Observability

Record per stage:

- run/project/version IDs;
- provider/model/version;
- started/finished timestamps;
- cold versus warm signal where measurable;
- input/output asset IDs, not signed URLs;
- latency;
- memory/accelerator metrics where available;
- candidate/retry count;
- estimated and actual cost;
- error code;
- fallback/degraded status;
- user acceptance decision.

Redact:

- credentials;
- signed URL query strings;
- raw consented audio;
- transcript/lyrics from general logs;
- provider payload fields containing private data.

## 15. Security and data handling

- private B2 bucket by default;
- bucket-scoped least-privilege key;
- provider credentials only in server secrets;
- short-lived upload/download URLs;
- SSRF validation for fetched assets;
- MIME verification from bytes, not filename alone;
- strict subprocess argument arrays for ffmpeg; never interpolate shell strings from user input;
- project authorization on every object lookup;
- rate, duration, candidate, and cost limits;
- deletion journal and verification;
- no model training reuse without separate opt-in;
- no third-party or celebrity voice path.

## 16. Test plan

### Unit

- schemas and state transitions;
- budget calculations;
- B2 key construction;
- lock-set comparison;
- error mapping;
- media metadata parsing;
- signed-URL redaction;
- parameter normalization idempotency.

### Provider compliance

Subclass Genblaze `ProviderComplianceTests` for both adapters. Verify lifecycle, assets, capabilities, chain validation, audio metadata, pricing behavior, and retries.

### Contract

- JSON Schema validates in Python and TypeScript;
- API response/event examples remain valid;
- manifest round-trip retains unknown forward-compatible fields.

### Integration without GPU

- fake AnyAccomp/ACE job servers;
- fixed local WAV fixtures;
- actual ffmpeg/ffprobe validation;
- B2-compatible local emulator only where semantics match; run real B2 canary before claiming production path.

### GPU/provider integration

- representative authorized fixtures;
- exact pinned model/config;
- artifacts retained outside Git;
- no mocked success in the evidence report.

### End-to-end

```text
create project
→ upload
→ consent
→ generate
→ receive progress
→ accept
→ render
→ revise
→ reload parent and child
→ verify manifest
→ delete
```

## 17. Deployment blockers to resolve

- GPU/endpoint for AnyAccomp and ACE-Step base model;
- measured model load size, cold start, VRAM, and warm latency;
- installed Genblaze package versions and custom-provider packaging;
- B2 credentials and actual account/API limits;
- Revideo 15-second StageMe benchmark: three consecutive cold/warm renders, pinned Chromium/fonts, A/V sync, memory, cleanup, container, and deployment (one smoke passed but two immediate rerenders failed on 2026-07-27);
- durable queue/database hosting;
- public functional-app URL;
- provider data-retention terms;
- representative user-owned fixtures;
- explicit paid-call budget.

No agent should resolve these by silently swapping in unrelated generation.
