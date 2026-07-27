# StageMe Retained-Performance Spike Protocol

> Purpose: prove or kill StageMe's load-bearing transformation before building the broad application.
>
> Product authority: `STAGEME_PRODUCT_SPEC.md`.
>
> Current status: protocol ready; no representative media run has occurred. The present Docker environment has no visible NVIDIA GPU tooling and contains no authorized user fixture or paid-provider budget.

## 1. Decision to make

Can StageMe reliably turn an authorized rough sung performance into a coherent accompaniment and staged artifact while retaining the actual source performance, at acceptable latency and cost?

The spike is successful only if the media result is compelling and the source connection is observable. Infrastructure success is insufficient.

## 2. Claim ladder

For every tested dependency record the highest level reached:

```text
advertised
→ documented
→ reachable
→ implemented
→ reproduced
→ product-proven
```

A test report must never promote a model from implemented to reproduced without an actual artifact from the pinned configuration.

## 3. Authorization and fixture policy

### Required fixture consent

Every human fixture needs:

- performer identity or pseudonymous fixture ID;
- attestation that the performer owns the recording;
- allowed purposes: analysis, arrangement, rendering, temporary provider processing;
- provider disclosure when used;
- retention period;
- deletion request path;
- explicit `training_reuse: false` unless independently opted in.

Do not place consented recordings in Git.

### Fixture set

| ID | Input | Status | Purpose |
|---|---|---|---|
| F0 | synthetic tones/clicks generated locally | safe to create | plumbing, timing, mux, hashes; never quality proof |
| F1 | 10–12s clean rough sung vocal, one phrase | user/performer must supply | canonical product lane |
| F2 | 10–12s hum of a clear melody | user/performer must supply | evaluation-only lane |
| F3 | 8–12s beatboxed rhythm | user/performer must supply | evaluation-only lane |
| F4 | 10–12s valid but difficult phone recording with moderate room noise | user/performer must supply | robustness boundary |

Do not generate a fake human fixture and present it as evidence of performance preservation.

## 4. Environment capture

Before every run, record:

- UTC timestamp;
- operating system/container image;
- Python/Node/ffmpeg versions;
- CPU/RAM;
- accelerator model, driver, CUDA/ROCm/MPS version;
- free and peak VRAM;
- repository commit;
- ACE-Step commit/model/config;
- AnyAccomp commit/checkpoints/config;
- Genblaze and connector versions;
- random seed;
- cold versus warm status;
- provider/region and price snapshot where hosted.

Example environment commands, adapted to the actual runner:

```bash
python --version
node --version
ffmpeg -version
ffprobe -version
nvidia-smi
python -m pip freeze
```

Absence of `nvidia-smi` does not prove all accelerators are absent; record the exact detected backend.

## 5. Canonical input preparation

For each human fixture:

1. retain original bytes;
2. compute SHA-256;
3. inspect with ffprobe;
4. decode to float PCM;
5. reject corrupt, too short, too long, or effectively silent input;
6. remove DC offset if present;
7. apply only recorded deterministic trim/fade/gain operations;
8. resample to the model's required rate with a named ffmpeg/libsoxr configuration;
9. save canonical processing WAV;
10. hash every derivative.

Never silently pitch-correct, time-warp, denoise aggressively, or replace the source.

## 6. Experiment matrix

### E0 — pipeline plumbing

Input: F0 only.

Test:

- ingest and hashing;
- object layout;
- media analysis;
- deterministic mixing;
- render and mux;
- manifest generation;
- parent/child versioning;
- B2 storage when credentials are available.

Pass:

- all deterministic tests pass;
- no provider-quality claim is made.

### E1 — AnyAccomp preservation path

Pinned source: `AmphionTeam/AnyAccomp@82604b5e3107944ad4c49fc64900b86118ae2c62`.

Initial parameters from official inference script:

```text
sample_rate = 24000
n_timesteps = 50
cfg = 3
seed = 1024
device = measured runner
```

Run F1–F4 independently.

Required outputs:

- generated accompaniment;
- mixture;
- config;
- logs;
- latency/memory metrics;
- deterministic QC;
- human rubric.

Literal-retention null test before mastering:

```text
residual = mixture - generated_accompaniment
compare residual to canonical source after exact length/alignment handling
```

Pass when:

- accompaniment is a separate usable asset;
- residual matches the source within the selected float/encoding tolerance;
- no clipping or corrupt output;
- F1 accompaniment follows enough melody/rhythm to be clearly connected;
- F4 reveals a documented boundary rather than a crash or fake success.

### E2 — ACE-Step `lego` layer path

Pinned source: `ace-step/ACE-Step-1.5@6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0`.

Use the base model only.

For F1, request one track at a time:

1. drums;
2. bass;
3. optional guitar or keyboard only if budget remains.

Record exact `GenerationParams`, including:

- `task_type="lego"`;
- source asset;
- instruction;
- caption;
- repaint bounds;
- inference steps;
- seed;
- model/config paths.

Pass when at least one generated instrument:

- is a separate asset;
- responds to source timing/context;
- mixes with the source without obvious destructive doubling;
- adds enough value to justify the additional model and latency.

### E3 — ACE-Step `complete` comparison

Use F1 and F4.

Record exact track request and caption.

Treat output as a full-mix candidate, not a guaranteed retained-source artifact.

Measure:

- source recognizability;
- source suppression/replacement;
- timing drift;
- generated vocal artifacts;
- quality relative to E1/E2;
- inability or ability to recover separate backing.

Pass as core only if literal source retention can be proven. Otherwise keep as a comparison/fallback candidate with honest labeling.

### E4 — accepted mix

Build at most two mix candidates from successful E1/E2 assets.

Required mix record:

- exact source hash;
- exact generated layer hashes;
- gain/pan/trim/fade per layer;
- processing chain and versions;
- peak, LUFS, clipping, duration, and silence metrics;
- resulting WAV hash.

Suggested initial mix target—not a mastered release standard:

- true/sample peak below configured ceiling;
- no clipped samples;
- integrated loudness recorded, not blindly forced;
- source intelligible on phone speaker and headphones;
- no hidden limiter damage.

Pass when human reviewers prefer one candidate and can identify the retained performance.

### E5 — bounded revision

Run the easiest honest revision first:

#### Layer revision

- parent: source + base accompaniment + generated accent layer;
- regenerate or replace only the accent layer;
- keep source and base accompaniment hashes unchanged;
- create child version and new mix.

#### Time-bounded insert

- generate a replacement/accent layer;
- insert only inside a 2–5 second region with recorded crossfades;
- keep all other assets unchanged.

#### ACE-Step repaint

Use only after E1–E4 pass.

For a 3–5 second interval:

- record parent decoded PCM;
- run `repaint`;
- exclude explicit crossfade margins when comparing outside-region audio;
- measure sample/RMS difference and correlation outside the target;
- keep parent version.

A reasonable initial strictness target is outside-region correlation >= 0.999 and difference below -60 dBFS, adjusted only with documented codec/model evidence. Perceptual similarity alone does not prove boundedness.

Pass when the requested target changes and locked asset hashes remain identical.

### E6 — deterministic stage

Input: accepted audio and analysis features.

Render:

- 720p primary artifact;
- low-data video;
- audio-only export;
- one stage world;
- waveform/shape derived from actual audio;
- timed phrases where reliable;
- beat/energy-reactive light and motion;
- deterministic camera/typography choreography.

Pass when:

- result renders without paid video;
- media QC passes;
- three reviewers do not describe it as a generic visualizer template;
- it improves preference over audio-only playback;
- same render spec/toolchain reproduces the intended sequence.

### E7 — optional Wan 2.2 S2V hero shot

Only after audio acceptance and E6.

Official endpoint observed: `wan-video/wan-2.2-s2v` on Replicate, $0.02 per output second on 2026-07-27.

Use:

- one approved generated/stylized reference image, not a third party's face;
- one 3–5 second interval from the accepted audio;
- one bounded prompt;
- one candidate initially;
- second candidate only with explicit budget approval.

Measure:

- queue and generation latency;
- output duration;
- actual billed cost;
- singing synchronization;
- identity consistency;
- visual artifacts;
- acceptance/rejection reason;
- reviewer preference against E6.

Insert the accepted shot only into that interval. If generation fails, drifts, times out, or fails automated/human QC, render the same interval through the deterministic Revideo scene. Pass as optional enhancement only if one or two candidates reliably improve the reveal. E6 remains the complete fallback.

### E8 — Genblaze/B2 production path

After media gates pass:

- invoke real custom providers through Genblaze;
- persist checkpoints after submit and each terminal stage;
- store source, candidates, accepted result, revision, and manifests in B2;
- fetch and rehash final objects;
- simulate retryable provider failure;
- simulate terminal auth/input failure;
- interrupt and resume a run;
- verify parent and child versions;
- delete a test project and verify the defined deletion boundary.

Pass when the real application path—not a parallel script—produces and reloads the same accepted artifacts.

## 7. Automated metrics

### Input/output integrity

- SHA-256;
- byte size;
- codec/container;
- sample rate/channels;
- duration;
- decodability;
- NaN/Inf count;
- clipped sample count;
- peak/RMS/integrated loudness;
- silence ratio;
- audio/video stream and mux integrity.

### Source preservation

- source asset hash unchanged;
- normalized source hash unchanged across versions;
- null test for AnyAccomp mixture;
- explicit source layer in mix spec;
- source-layer gain above the configured audibility floor;
- accompaniment PCM outside an authorized edit interval plus declared crossfade margin remains identical when temporal boundedness is claimed;
- optional source-estimate correlation, labeled as analysis rather than proof.

### Revision

- parent and child IDs;
- locked hash equality;
- requested target hash inequality;
- outside-region sample/correlation metrics where temporal editing is claimed;
- parent fetch/playability after child creation.

### Performance and economics

- cold load time;
- warm generation time;
- end-to-end wall time;
- peak CPU RAM;
- peak VRAM;
- accelerator utilization where available;
- candidate and retry counts;
- pure compute cost;
- provider charge;
- storage/egress estimate;
- cost per accepted result.

## 8. Human evaluation rubric

Use at least three reviewers unfamiliar with the implementation where possible. Randomize candidate order.

Score 1–5:

| Dimension | 1 | 5 |
|---|---|---|
| Source connection | result feels unrelated | unmistakably grows from source |
| Source recognizability | performer disappears | real performance remains clear |
| Musical coherence | clashes/unstable | arrangement feels intentional |
| Emotional lift | no meaningful improvement | strong before/after payoff |
| Shareability | would not replay/share | proud to play/share |
| Artifact quality | obvious broken model output | polished enough for demo |

Also ask:

1. What remained human?
2. What did the system add?
3. Could you explain the difference from ordinary hum-to-song?
4. Which result would you keep?
5. What failed or felt fake?

Do not average away a catastrophic identity or source-retention failure.

## 9. Initial budgets and gates

These are decision thresholds, not advertised guarantees.

### Audio

- target warm candidate latency: <= 60 seconds;
- provisional ceiling: <= 180 seconds;
- target accepted-result compute/provider cost: <= $0.10;
- provisional ceiling: <= $0.25;
- maximum initial candidates: 2 per path/fixture only where budget permits.

If the only good path routinely exceeds the ceiling, redesign hosting or reject live use.

### Deterministic rendering

- target render latency for 15 seconds at 720p: <= 30 seconds on selected deployment hardware;
- hard demo ceiling: <= 60 seconds;
- no paid dependency.

### Optional S2V

- maximum 15 output seconds;
- official observed candidate cost: <= $0.30 at the 2026-07-27 price;
- maximum two candidates/accepted shot: <= $0.60 before image/provider overhead;
- provisional end-to-end ceiling: <= 180 seconds;
- human approval required before call.

## 10. Pass decision

StageMe proceeds to the full vertical slice only when:

1. E1 or E2 produces a source-conditioned separate backing/layer;
2. literal source retention is proven structurally;
3. at least one F1 result has median human scores >= 4 for source connection, musical coherence, and emotional lift;
4. the hard valid fixture exposes a tolerable boundary;
5. one bounded revision preserves locked assets;
6. deterministic stage output is submission-worthy;
7. latency and cost remain within provisional ceilings;
8. the before/after is understandable without infrastructure explanation.

## 11. Stop or reframe conditions

Stop the current StageMe promise if:

- generated backing ignores the source;
- the source must be regenerated or replaced to sound acceptable;
- the result is generic without explanatory prose;
- only unrelated text-to-music works;
- revision changes locked assets;
- quality needs unbounded candidate fishing;
- compute/provider access is too brittle for the judge path;
- deterministic visual output is too weak and S2V is unreliable;
- consent or licensing cannot support the demonstrated use.

Do not respond to failure by quietly broadening the app.

## 12. Artifact report template

Every run folder must include `REPORT.md` with:

```markdown
# Run <ID>

## Decision
pass | fail | inconclusive

## Fixture and consent
fixture ID, source hash, consent record reference

## Environment
hardware, runtime, commits, model/checkpoint versions

## Exact command/config
reproducible invocation with secrets redacted

## Outputs
asset paths/keys, hashes, durations, sizes

## Measurements
latency, RAM/VRAM, QC, cost, retries

## Human review
scores, reviewers, blinded order, notes

## Failures
classification and recovery

## Claim promotion
which claim moved from what level to what level

## Next decision
proceed, repeat, reframe, reject
```

A run without artifacts, hashes, and exact configuration is not evidence.
