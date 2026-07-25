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
| Copycat/low differentiation | Medium | High | avoid visible concepts and official-sample reskin | concept scorecard |
