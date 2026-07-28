# Official Updates Log

Checked 2026-07-28 19:20:37 UTC through the official Devpost connector. Four announcements were returned, complete. Recheck https://backblaze-generative-media.devpost.com/updates regularly.

## Genblaze v0.6.0 — sent 2026-07-22 15:43:16 UTC

Source: https://backblaze-generative-media.devpost.com/updates/45436-genblaze-v0-6-0

- ElevenLabs upgraded to SDK 2.x; fallback behavior improved.
- LMNT upgraded to SDK 2.x, requiring LMNT >=2.6.
- GMI Seedance first/last-frame routing fixed.
- Windows local file URLs fixed for B2 upload.
- B2 sink avoids a redundant `HeadObject` probe when assets are already backend-owned, reducing 403/cap failures.
- Optional dependency introspection made safer.
- Content-addressed key extension normalization prevents case-only duplicates.
- New `genblaze verify --fetch` performs byte-level remote verification.
- Dependency major versions capped to reduce surprise breakage.

**Release boundary:** the announcement title is v0.6.0, while its install section names umbrella `genblaze` 0.4.4, core 0.3.7, and CLI 0.3.5; the inspected S3 distribution is 0.3.6. Do not apply the release label to every package.

## Genblaze v0.5.0 — sent 2026-07-17 16:38:50 UTC

Source: https://backblaze-generative-media.devpost.com/updates/45363-genblaze-v0-5-0

- Replicate community-model version resolution.
- OpenAI Sora compatibility with OpenAI SDK 2.x.
- Google Veo Vertex AI support.
- GMI typing and duration validation.
- Concurrency-safe streaming, run IDs in events, order-sensitive cache correctness.
- Stronger SSRF/ReDoS/ffmpeg/log-redaction protections.
- Stricter argument and schema validation.

**Action:** Avoid code written against old unknown-keyword behavior; pin versions.

## Multi-provider starter app — sent 2026-07-07 19:49:37 UTC

Source: https://backblaze-generative-media.devpost.com/updates/45182-genblaze-multi-provider-starter-app

Official sample turns one prompt into narrated/scored/captioned MP4 using selectable providers and B2 for every intermediate/final artifact. GMI credits are not required; the sample is the organizer's fallback path for participants without them.

## Genblaze v0.4.0 — sent 2026-06-29 14:46:24 UTC

Source: https://backblaze-generative-media.devpost.com/updates/45048-genblaze-v0-4-0

- Hume TTS and AssemblyAI transcription connectors.
- Retry resume to avoid duplicate billed generations.
- Fan-in failure propagation.
- SSRF and redirect validation.
- Stronger asset-hash requirements.
- Async and resource-lifecycle improvements.

## Release watch

The SDK changed rapidly during the event: v0.4, v0.5, and v0.6 in about one month. On 2026-07-28, official `main` had advanced to `c5a57085a0ca78339eea65b91786f0edad7959e1`, while open PR #236 prepared—but had not released—a v0.7.0 wave. Freeze exact package versions and do not treat `main` as released.
