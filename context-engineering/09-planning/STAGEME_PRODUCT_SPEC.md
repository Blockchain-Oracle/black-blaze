# StageMe Product Specification — Historical Candidate Contract

> **Selection notice:** Decision D-014 superseded StageMe's active-selection status on 2026-07-28. This remains canonical only for describing the preserved StageMe candidate; it is not the repository's current product authority.
>
> **Status:** historical candidate, not selected. The load-bearing audio transformation is not product-proven. Do not implement or make paid media calls unless a later owner decision explicitly reselects StageMe and supplies the required authority.
>
> **Research date:** 2026-07-27.

## 1. Product in one sentence

> **StageMe turns your rough sung performance into an arranged 8–15 second stage moment while keeping your real voice literally present, then lets you change one generated layer or bounded section without starting over.**

## 2. The point

Many people can sing, hum, or imagine a musical moment but cannot afford studio time, production software, multiple AI subscriptions, or a high-end GPU. Existing generators often treat that human input as disposable inspiration and synthesize a replacement.

StageMe treats the authorized performance as the project's source of truth:

```text
my real performance
→ arranged around, not silently replaced
→ staged as something I am proud to play and share
→ revised without throwing away the part that already feels like me
```

The emotional test is:

> “That still feels like me—but now it feels finished.”

## 3. What is actually differentiated

StageMe does not claim to invent:

- hum-to-song;
- text-to-music;
- personalized generated vocals;
- talking portraits;
- audio-driven video;
- lyric or waveform videos.

Its specific product operation is the combination of:

1. **literal source retention:** the user's normalized source recording is an audible layer in the accepted mix;
2. **source-conditioned arrangement:** generated accompaniment responds to the performance rather than merely to a text prompt;
3. **staged reveal:** the accepted arrangement becomes one intentional audiovisual performance moment;
4. **bounded revision:** a generated layer, visual scene, or proven time interval changes while locked assets remain byte-identical;
5. **durable project memory:** sources, candidates, decisions, locks, branches, costs, and provenance survive in B2.

This is product-level differentiation, not a claim of new music-generation research.

## 4. The core feature contract

### 4.1 Canonical operation

```text
arrange_and_stage(source_performance, creative_direction, budget)
  -> staged_performance_project
```

### 4.2 Required input

- one authorized user-owned recording;
- first supported lane: **rough sung vocal**;
- duration: 8–15 seconds;
- one voice, without copyrighted backing music;
- WAV, FLAC, MP3, M4A, WebM, or Ogg/Opus at ingest;
- one style/emotional direction of at most 160 characters;
- explicit consent to process and temporarily store the recording.

Examples:

- “Warm Afrobeats-pop, victorious but intimate.”
- “Sparse drums and bass; keep the shaky honesty.”
- “Night-stage energy without making it aggressive.”

### 4.3 Evaluation-only input lanes

These are representative spike fixtures, not public promises until promoted:

- hummed melody;
- beatboxed rhythm;
- spoken lyric.

An agent must not add them to landing-page copy merely because a model accepts audio.

### 4.4 Required output

- an 8–15 second accepted arrangement;
- the canonical normalized source vocal remains a separate, audible mix layer;
- at least one generated accompaniment layer or backing track;
- one 720p H.264/AAC or H.264/Opus audiovisual artifact;
- one audio-only compressed export;
- one low-data video export;
- a manifest identifying original, deterministic, generated, accepted, rejected, and revised assets;
- a versioned B2 project that can be reloaded.

### 4.5 Required revision

```text
revise(project_version, target, instruction, lock_set)
  -> child_project_version
```

The first build must support at least one of these, in preference order:

1. change one generated instrument/accompaniment layer while preserving the source vocal and every other accepted layer;
2. insert or replace one generated musical layer only inside a selected 2–5 second interval;
3. use a reproduced ACE-Step `repaint` path that preserves audio outside the requested interval;
4. change one visual scene while keeping accepted audio byte-identical.

A visual-only revision may be demonstrated as a recovery path, but it does not independently prove the full musical-editing thesis.

### 4.6 Locked invariants

For every accepted version:

- `source_asset_sha256` never changes;
- consent belongs to the exact source and project;
- the original uploaded bytes remain separately retrievable until the user deletes the project;
- the normalized source used in mixing has its own immutable hash;
- generated accompaniment never overwrites the source object;
- child versions never overwrite parent assets;
- unchanged locked assets are referenced, not re-generated;
- every provider/model/config/seed is recorded where available;
- every candidate and retry is charged against an explicit budget;
- failed or degraded stages are labeled rather than disguised.

## 5. Product truth boundaries

### 5.1 Evidence vocabulary

Every capability must carry one label:

1. **Advertised** — descriptive page or README.
2. **Documented** — exact operation and parameters described.
3. **Reachable** — callable CLI, SDK, or endpoint exists.
4. **Implemented** — source or test contains the operation.
5. **Reproduced** — StageMe ran a representative authorized fixture and stored the artifact.
6. **Product-proven** — representative quality, latency, cost, recovery, and repeatability pass.

Public product copy may rely only on product-proven behavior. Demo narration may discuss reproduced behavior with explicit limits.

### 5.2 Current truth ledger

| Claim | Current level | Product status |
|---|---|---|
| AnyAccomp generates a separate accompaniment from vocal input | Implemented | Pinned source contains the operation; StageMe has not reproduced it |
| AnyAccomp upstream mixture adds the decoded source waveform | Implemented | StageMe has not reproduced it and must ignore the un-gain-staged upstream mix, construct its own float premaster, and null-test it |
| ACE-Step `lego` generates a named instrument in audio context | Implemented | Secondary layer candidate; not reproduced by StageMe |
| ACE-Step `complete` completes a partial track with specified instruments | Implemented | Comparison candidate; not reproduced by StageMe |
| ACE-Step `repaint` preserves audio outside a time range in some modes | Implemented | Current-main caveats apply; StageMe must restore/hash locked parent regions independently |
| Replicate Wan 2.2 S2V accepts image + audio + prompt | Documented | Current exact-version schema is documented; optional renderer only; revalidate before payment |
| Wan S2V costs $0.02/output-second | Documented | Official endpoint price observed 2026-07-27; mutable budget input |
| StageMe produces a magical retained-vocal arrangement | Advertised | Product promise and acceptance gate exist; no working outcome is reproduced and this remains the load-bearing spike |

Outcomes such as **not reproduced** or **failed gate** are status, not evidence-level labels.

## 6. Minimum magical artifact

The first proof is not a website. It is one folder containing:

```text
fixture/
  source-original.*
  source-normalized.wav
  consent.json
  direction.json
analysis/
  media.json
  musical-features.json
candidates/
  anyaccomp-accompaniment.wav
  anyaccomp-mix.wav
  ace-lego-layer.wav
  ace-complete-mix.wav
  evaluations.json
accepted/
  arrangement.wav
  stage.mp4
revision/
  request.json
  arrangement-v2.wav
  stage-v2.mp4
manifest/
  v1.json
  v2.json
```

The before/after must be understandable without architecture narration.

## 7. User flow

### Screen 1 — Record

- one prominent record/upload action;
- duration guidance and visible 15-second cap;
- “Use only your own voice/performance” notice;
- delete and rerecord controls;
- consent must not be preselected.

### Screen 2 — Direct

- replay source;
- one short direction field;
- optional curated style chips that modify the same field rather than creating hidden magic;
- clear Generate Arrangement action with expected wait and candidate budget.

### Screen 3 — Progress

Show meaningful pipeline stages:

```text
Checking recording
Reading rhythm and melody
Building accompaniment
Checking the mix
Creating the stage
Saving the project
```

Do not expose fake percentages. Use Genblaze progress events or stage completion.

### Screen 4 — Reveal

- play the rough source first;
- immediately play the arranged stage artifact;
- identify “your retained performance” and “generated accompaniment” without cluttering the emotional reveal;
- allow accept, reject, or one bounded revision.

### Screen 5 — Revise

- choose one generated layer or visual scene;
- optionally select a 2–5 second interval when the audio path supports it;
- show locked items explicitly;
- state the maximum retry/candidate cost before execution;
- create a child version rather than mutate the parent.

### Screen 6 — Project history

- source;
- accepted versions;
- revision relationship;
- downloadable audio/video;
- compact provenance and verification view;
- deletion control.

## 8. Audio behavior

### 8.1 Canonical source handling

1. Keep the original uploaded bytes immutable.
2. Decode to a canonical processing WAV.
3. Measure DC offset. For F1, reject/re-record when absolute decoded mean exceeds `0.005` full scale; otherwise do not alter it. Any later correction must be explicit, versioned, and hashed.
4. Do not pitch-correct, time-warp, denoise aggressively, or synthesize a replacement in the first build.
5. Hash the normalized source and record every transformation.

Recommended processing target pending spike confirmation:

- mono source layer;
- 24 kHz for AnyAccomp inference;
- retain a 48 kHz working copy for final render if resampling quality is validated;
- 32-bit float internal mixing;
- final audio export at 48 kHz.

### 8.2 Candidate paths

#### Candidate A — AnyAccomp

Pinned source inspected: `AmphionTeam/AnyAccomp@82604b5e3107944ad4c49fc64900b86118ae2c62`.

The inference script:

- loads vocal audio at 24 kHz mono;
- encodes melodic features;
- generates accompaniment;
- length-matches accompaniment to the source;
- writes `accompaniment/<file>`;
- writes `mixture/<file>` as generated accompaniment plus the original vocal waveform.

This is the primary candidate for literal vocal retention. The upstream addition has no explicit gain/headroom policy. StageMe accepts only the separate accompaniment, creates its own lossless premaster with recorded gains, and verifies `premaster - accompaniment == retained source` within the declared sample tolerance.

The stock worker declares Python 3.9 while current Genblaze requires Python 3.11 or newer. Keep the model in a dedicated worker/container and never import it into the FastAPI process.

#### Candidate B — ACE-Step `lego`

Pinned source inspected: `ace-step/ACE-Step-1.5@6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0`.

Use the base model to generate one named instrument track from source context. Test drums, bass, or guitar separately. Keep each generated output as its own asset and mix it with the immutable source.

#### Candidate C — ACE-Step `complete`

Use the base model with explicit tracks and caption. Treat its output as a candidate full mix. It does not satisfy literal-retention policy until a real run proves the source survives or a separate source layer can be mixed without destructive doubling.

### 8.3 Mixing policy

- never normalize each stem independently without recording gain changes;
- prevent clipping with headroom before limiting;
- preserve the source at an intelligible level;
- record per-layer gain, pan, trim, fade, and processing chain;
- reject silent, clipped, corrupt, duration-mismatched, or unintelligible candidates automatically;
- keep taste and source connection as human judgments.

## 9. Visual behavior

### 9.1 Core renderer

The core renderer must work without full generative video:

- one generated or deterministic stage world;
- audio-driven light, particles, typography, waveform, and camera movement;
- no generic dashboard aesthetic;
- no dependence on a user selfie;
- no false synthetic performer identity;
- final video derived from accepted audio timing and analysis.

### 9.2 Optional hero shot

Wan 2.2 S2V may replace one **3–5 second** audio-bound interval after audio acceptance. The complete deterministic stage, including the same interval, must already exist and remain the immediate fallback.

It remains optional until StageMe measures:

- singing synchronization;
- visual consistency;
- accepted-candidate rate;
- latency variance;
- full cost per accepted shot;
- consent and deletion behavior;
- preference over the deterministic stage.

If unavailable, timed out, drifted, rejected, or disliked, the deterministic interval remains the valid output. Pin and record the exact Replicate prediction version because the current generic and version-specific API pages expose conflicting schemas.

## 10. Accessibility and affordability

The default user owns the phone, not the GPU.

Required principles:

- browser capture;
- no model installation;
- short compressed uploads;
- server-side scale-to-zero GPU execution;
- explicit candidate and retry budgets;
- cached accepted assets;
- audio-only and low-data exports;
- resumable projects;
- optional self-host/BYOK later, not required.

Avoid patronizing language. The product is for creators constrained by money, hardware, bandwidth, time, or production skill.

## 11. Safety, consent, and rights

Required:

- user-owned or explicitly licensed performance;
- active consent before processing;
- no celebrity imitation;
- no target-voice cloning in the first build;
- private B2 storage by default;
- configurable retention and user deletion;
- provider/model/license metadata in the manifest;
- no credential-bearing presigned URL in logs or manifests;
- no training reuse implied without a separate explicit opt-in.

## 12. Explicit non-goals

Do not build these before the core is product-proven:

- full three-minute songs;
- a DAW or nonlinear editor;
- arbitrary multimodal performance inputs;
- perfect pitch correction;
- synthetic replacement of the user's singing identity;
- celebrity or third-party voice cloning;
- persistent photorealistic avatar;
- multi-person collaboration;
- social feed or global chorus;
- marketplace;
- mobile native app;
- mandatory local inference;
- two separate hackathon entries.

## 13. Acceptance criteria

The product survives only when all are true:

### Human-result criteria

- an uninformed viewer connects source and result in under 20 seconds;
- the user can hear their real performance in the mix;
- at least two of three evaluators prefer the accepted arrangement to the raw source for sharing;
- the result feels intentional rather than like a model demo;
- the user can explain what changed and what stayed theirs.

### Technical criteria

- input is validated and hashed;
- source is stored separately and never overwritten;
- one source-conditioned accompaniment path passes;
- final audio and video pass media validation;
- one revision preserves the lock set;
- interrupted/retried runs do not duplicate accepted assets;
- project reload reconstructs every accepted version;
- final manifest verifies against fetched B2 bytes;
- secrets and expiring URLs are absent from persisted metadata.

### Operational criteria

- latency, GPU memory, candidate count, and accepted-result cost are measured;
- a deterministic renderer completes when optional S2V fails;
- failure states are visible and recoverable;
- a bounded retry never silently exceeds budget;
- the live judge path does not depend on an unverified provider entitlement.

## 14. Judge-visible proof

| Official criterion | Visible StageMe proof |
|---|---|
| Real-world utility | ordinary phone recording becomes something shareable without studio tools |
| Production readiness | progress, validation, explicit budgets, retry/fallback, recovery, deletion |
| Meaningful B2 | full source/candidate/version/manifest lifecycle, not final-file dumping |
| Meaningful Genblaze | custom/open provider orchestration, optional hosted provider, progress, fallback, provenance |

Stage 1 requires legitimate generative-media, Genblaze, and B2 use. Tie-break order starts with utility, so the demonstration leads with the human transformation.

## 15. Decision gates

### Gate 1 — literal source retention

Pass when AnyAccomp or a separate ACE-generated layer produces a coherent accompaniment that can be mixed with the immutable source.

### Gate 2 — magic

Pass when the side-by-side result creates an obvious “that came from this” reaction.

### Gate 3 — revision

Pass when a child version changes the requested generated region/layer and locked asset hashes remain unchanged.

### Gate 4 — stage

Pass when the deterministic renderer is submission-quality without optional S2V.

### Gate 5 — production path

Pass when Genblaze and B2 execute the real workflow with verified manifests, recovery, and bounded cost.

Failure at Gate 1 or Gate 2 stops the full app. A failed spike is a successful decision artifact.

## 16. Change control

Any proposal that changes the following requires a decision-log entry and evidence:

- primary input lane;
- literal source-retention guarantee;
- core output duration;
- required revision behavior;
- mandatory model/provider;
- default data retention;
- identity/voice policy;
- core versus optional video boundary;
- public product claim.

Do not broaden scope because a library exposes additional features.
