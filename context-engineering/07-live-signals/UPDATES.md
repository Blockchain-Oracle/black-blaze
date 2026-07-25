# Official Updates Log

Checked 2026-07-25. Recheck https://backblaze-generative-media.devpost.com/updates regularly.

## Genblaze v0.6.0 — posted around Jul 22

- ElevenLabs upgraded to SDK 2.x; fallback behavior improved.
- LMNT upgraded to SDK 2.x, requiring LMNT >=2.6.
- GMI Seedance first/last-frame routing fixed.
- Windows local file URLs fixed for B2 upload.
- B2 sink avoids a redundant `HeadObject` probe when assets are already backend-owned, reducing 403/cap failures.
- Optional dependency introspection made safer.
- Content-addressed key extension normalization prevents case-only duplicates.
- New `genblaze verify --fetch` performs byte-level remote verification.
- Dependency major versions capped to reduce surprise breakage.

**Action:** Start on v0.6-compatible packages and use `verify --fetch` as submission evidence.

## Genblaze v0.5.0 — posted around Jul 17

- Replicate community-model version resolution.
- OpenAI Sora compatibility with OpenAI SDK 2.x.
- Google Veo Vertex AI support.
- GMI typing and duration validation.
- Concurrency-safe streaming, run IDs in events, order-sensitive cache correctness.
- Stronger SSRF/ReDoS/ffmpeg/log-redaction protections.
- Stricter argument and schema validation.

**Action:** Avoid code written against old unknown-keyword behavior; pin versions.

## Multi-provider starter app — posted around Jul 7

Official sample turns one prompt into narrated/scored/captioned MP4 using selectable providers and B2 for every intermediate/final artifact. GMI credits are not required; the sample is the organizer's fallback path for participants without them.

## Genblaze v0.4.0 — posted around Jun 29

- Hume TTS and AssemblyAI transcription connectors.
- Retry resume to avoid duplicate billed generations.
- Fan-in failure propagation.
- SSRF and redirect validation.
- Stronger asset-hash requirements.
- Async and resource-lifecycle improvements.

## Release watch

The SDK changed rapidly during the event: v0.4, v0.5, and v0.6 in about one month. Freeze and record exact package versions before final validation.
