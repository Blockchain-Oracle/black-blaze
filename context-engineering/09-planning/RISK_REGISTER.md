# Risk Register

| Risk | Probability | Impact | Mitigation | Verification |
|---|---|---|---|---|
| Deadline compression | High | Critical | vertical slice first; freeze Aug 1; submit 6h early | internal schedule |
| GMI promotional credits unavailable | High | High | choose provider with confirmed account/credits; make GMI optional | live dashboard + minimal call |
| Model slug/entitlement drift | High | High | registry inspect + real preflight; pin model/version | automated smoke test |
| Video costs/rate limits | High | High | short/low-res dev runs; cache; approval gates; conservative retry | usage dashboard |
| B2 access/cap discrepancy | Medium | High | use scoped private canary; record account caps; upload/head/fetch/hash/delete exact versions | credentialed canary + dashboard |
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
| AnyAccomp quality/VRAM/latency unknown | High | Critical | run one authorized F1 on a 24 GB+ Ampere/Ada risk-control worker; one candidate; retain metrics and human rubric | separate accompaniment + null test + review |
| AnyAccomp official hosted path unavailable | High | High | official Space is currently broken and no official maintained provider mapping was found; use an approved dedicated worker | worker preflight + direct run |
| AnyAccomp/Genblaze Python conflict | High | High | keep stock Python 3.9 CUDA worker isolated from Python 3.11/3.12 control/API | separate environment/container smoke |
| AnyAccomp raw mix clips or lacks headroom | Medium | Critical | ignore upstream mix for acceptance; StageMe-owned float premaster with recorded gains and null test | peak/QC + `stageme_null_test.py` |
| AnyAccomp model training provenance ambiguity | Medium | High | preserve CC BY attribution and paper citation; do not make an unaudited commercial-safety claim | license/NOTICE review before release |
| ACE-Step `complete` quality unknown | High | Critical | run only after AnyAccomp F1; measure source survival, coherence, latency, and failure rate; treat as full mix | real GPU output + human review |
| ACE-Step advertised capability mismatch | Medium | High | rely only on documented `complete`/`lego`/`repaint`; do not claim a dedicated Vocal2BGM API | adapter contract tests + source audit |
| ACE base download/compute burden | High | High | 14,883,895,000-byte complete pinned snapshots; base file >2 GB requires approval; do not download until AnyAccomp justifies comparison | approved download + verified hashes |
| ACE API loses or misreports jobs | Medium | High | durable StageMe state; unknown-ID TTL; process-level timeout/cleanup; no blind retry | fault-injection adapter tests |
| ACE repaint violates locked region | Medium | Critical | never repaint source; restore parent accompaniment outside bounds/margins and hash/sample-compare | decoded outside-window comparison |
| Open source requires inaccessible compute | High | High | browser-first UI, scale-to-zero GPU, short jobs, cached outputs, audio-only/low-data variants | measured cold/warm cost and latency |
| Revideo repeat-render failure | High | Critical | current smoke passed once then failed twice; keep FFmpeg/MoviePy fallback until 3× cold/warm 15s benchmark passes | pinned browser/font/container benchmark |
| Revideo audio/font/container drift | Medium | High | local assets only; pin Node 22.x, Puppeteer/Chrome, FFmpeg, fonts, lockfile, digest; telemetry off | decoded frame/PCM hashes + sync flash/click |
| Full AI video scope/cost | High | Critical | deterministic stage mandatory; Wan only one replaceable 3–5 second interval | timed render spike + candidate cap |
| Wan schema/version drift | High | High | generic and exact-version pages conflict; revalidate exact schema and record prediction-returned version | credentialed preflight immediately before payment |
| Wan latency/TTL/rejection | High | Medium | 12-minute stop; copy success before TTL; restore deterministic interval on any failure/rejection | provider lifecycle + B2 fetch/hash |
| Voice consent/impersonation | Medium | Critical | preserve user's own recording, explicit consent, no celebrity cloning, revocation path | consent fixture + manifest audit |
| Consent applies to different media/execution | Medium | Critical | bind separate original/canonical SHA-256 values, canonical derivation, exact model/checkpoint, provider/region/cap, and retention; compare at both preflight boundaries | mismatch regression tests + private execution record |
| Null test certifies inaudible source | Low | Critical | require source gain 0.1–1.0, strict tolerance ceilings, aligned lossless assets, and wrong/zero-gain regression tests | fail-closed null-test suite |
| Custom Genblaze provider defects | Medium | High | reproduce direct semantics first; 16-method compliance suite plus task/retention tests; SyncProvider only in dedicated worker | provider compliance + fault injection |
| Genblaze manifest overclaim | Medium | Critical | manifest verification does not fetch bytes and excludes transport URLs/parent ID from canonical hash; bind StageMe lineage and fetch/hash assets separately | fetched-byte/lineage audit |
| GPU account/payment unavailable in Nigeria | Medium | Critical | check RunPod/Modal account before F1; Lambda is no-go absent explicit support; keep one contingency | account and secure-inventory preflight |
| RunPod CLI/docs hard-stop drift | High | Critical | pin checksum-installed `runpodctl` 2.7.2; pass an absolute RFC 3339 UTC deadline; explicit Secure Cloud/data center; confirm deadline in authenticated console before F1 transfer | recorded CLI version/help, budget plan, console confirmation, immediate deletion |
| RunPod content-processing terms rejected | Medium | Critical | disclose current ownership/service/aggregated-anonymized-use terms and shared-security boundary before consent; use no provider if owner declines | exact terms URL/version + project-bound consent |
| GPU idle/cache cost | Medium | High | hard session cap; terminate Pod and unwanted volumes; verify billing stopped | provider dashboard/deletion evidence |
| B2 version/deletion mismatch | Medium | Critical | content-addressed keys; record VersionId/fileId; delete exact versions; avoid Object Lock on MVP bucket | post-delete head/read plus version audit |
| Presigned POST assumed available | Medium | High | B2 supports presigned PUT, not browser POST; use exact-key PUT or API proxy | real browser/CORS canary |
| Autonomous PR-to-demo scope | High | Critical | ShipCast deprioritized; do not depend on universal app discovery/capture | competitor audit + constrained spike only |
| Subjective media evaluation | High | High | deterministic audio/video checks plus explicit human taste and identity review | fixture tests + blind human review |
| Generic observability overlap | High | High | keep validation/provenance inside a user-facing transformation instead of shipping a trace viewer | compare against visible field |
