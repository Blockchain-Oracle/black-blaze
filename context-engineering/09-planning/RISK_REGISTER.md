# Risk Register

| Risk | Probability | Impact | Mitigation | Verification |
|---|---|---|---|---|
| Deadline compression | High | Critical | vertical slice first; freeze Aug 1; submit 6h early | internal schedule |
| GMI promotional credits unavailable | High | High | choose provider with confirmed account/credits; make GMI optional | live dashboard + minimal call |
| Model slug/entitlement drift | High | High | registry inspect + real preflight; pin model/version | automated smoke test |
| Video costs/rate limits | High | High | short/low-res dev runs; cache; approval gates; conservative retry | usage dashboard |
| B2 access/cap discrepancy | Medium | High | inspect caps, avoid polling, cache/index, load test | dashboard + scripted reads |
| Presigned URL expiry/leak | Medium | High | transient only; stable SHA; redact query strings; durable app endpoint | log/manifest scan |
| Thin B2 integration | Medium | Critical | design B2-backed library/index/version/provenance into core workflow | architecture review |
| Thin Genblaze integration | Medium | Critical | chain/fan-out/fallback/agent loop with real product need | manifest + code evidence |
| Live app fails for judges | Medium | Critical | seeded demo, health check, no fragile auth, keep live through Aug 12 | incognito external test |
| Demo exceeds/loses attention | Medium | High | 2:30–2:45 script; value in first 20s | timed rehearsal |
| Third-party media/IP issue | Low–Medium | Critical | original/synthetic/licensed media, dependency license scan | legal checklist |
| Secret exposure | Medium | Critical | `.env` ignore, secret manager, gitleaks/history scan | pre-submit scan |
| Nigeria prize payment friction | Low–Medium | Medium | verify bank details/forms if selected; account for fees/W-8BEN | winner onboarding only |
| SDK release breaks build | Medium | High | pin exact packages after final validation | clean install CI |
| Copycat/low differentiation | High | High | differentiate StageMe from ONEFIELD, Murmur, InstantBandAI, and official sample through real retained-vocal arrangement, staged reveal, and bounded revision | blind before/after test + competitor comparison |
| ACE-Step `complete` quality unknown | High | Critical | run authorized rough-vocal/hum/beatbox spike; measure source survival, coherence, latency, and failure rate | real GPU outputs + human review |
| ACE-Step advertised capability mismatch | Medium | High | rely only on documented `complete`/`lego`/`repaint`; do not claim a dedicated Vocal2BGM API | adapter contract tests + source audit |
| Open source requires inaccessible compute | High | High | browser-first UI, scale-to-zero GPU, short jobs, cached outputs, audio-only/low-data variants | measured cold/warm cost and latency |
| Full AI video scope/cost | High | Critical | generated stage art + deterministic animation for MVP; full diffusion optional | timed render spike |
| Voice consent/impersonation | Medium | Critical | preserve user's own recording, explicit consent, no celebrity cloning, revocation path | consent fixture + manifest audit |
| Custom Genblaze provider defects | Medium | High | implement compliance-tested async ACE-Step connector with explicit capability/error contracts | Genblaze provider compliance suite |
| Autonomous PR-to-demo scope | High | Critical | ShipCast deprioritized; do not depend on universal app discovery/capture | competitor audit + constrained spike only |
| Subjective media evaluation | High | High | deterministic audio/video checks plus explicit human taste and identity review | fixture tests + blind human review |
| Generic observability overlap | High | High | keep validation/provenance inside a user-facing transformation instead of shipping a trace viewer | compare against visible field |
