# Open Questions

StageMe is the selected feasibility-first direction. Resolve the load-bearing items below before broad application implementation or submission. Questions answered by the 2026-07-27 pre-call pass are checked; a checked infrastructure question does not promote the media transformation above its evidence level.

Current primary audit: `STAGEME_PRECALL_READINESS_REPORT.md`. Historical selection audit: `STAGEME_FEASIBILITY_AND_JUDGE_FIT_2026-07-27.md`.

## Product proof

- [x] Has an owner-supplied rough-vocal F1 passed local technical readiness? Yes: the private 14.256-second selection passed deterministic canonicalization/media QC and contains sustained pitch-bearing signal; fixture-scoped rights attestations are complete, while model quality remains a separate gate.
- [ ] Does one pinned AnyAccomp run on authorized F1 produce a coherent, source-connected accompaniment, and what are measured cold/warm latency, VRAM, RAM, and cost?
- [ ] Does the StageMe premaster pass the sample-aligned null test while keeping F1 audible and emotionally stronger?
- [ ] Does ACE-Step 1.5 base `lego` produce a useful separate instrument layer on the same F1?
- [ ] How does ACE-Step base `complete` compare as a full mix, without assuming source preservation?
- [ ] Does a hummed seed materially influence the result, or does the model ignore it?
- [ ] Does a beatboxed/rhythmic seed materially influence the result?
- [ ] Can an uninformed viewer identify the source-to-output connection in under 20 seconds?
- [ ] Is the retained real vocal plus generated arrangement emotionally stronger than a generic text-to-song result?
- [ ] Is the result sufficiently distinct from ONEFIELD, Murmur, InstantBandAI, and the official multi-provider starter app?
- [ ] What exact user repeats this workflow, and what do they currently pay or struggle with?

## Models and compute

- [x] What is the first worker strategy? Use an approved RunPod Secure Cloud Pod for the interactive experiment; Modal is the serverless follow-on. Lambda is unavailable to a Nigeria-billed account unless explicitly confirmed.
- [x] What exact RunPod hard-stop contract applies? Checksum-pinned `runpodctl` 2.7.2 requires an absolute RFC 3339 UTC `--terminate-after` value; prose duration examples conflict, and v2.7.2 output does not return the configured deadline, so the authenticated console must confirm it before media transfer.
- [ ] Does the actual RunPod/Modal account accept the user's payment method and expose a secure 24 GB+ Ampere/Ada worker in an acceptable region?
- [ ] What are measured cold-start and warm-generation times for 8–15 seconds of AnyAccomp audio?
- [ ] What are measured peak GPU memory, CPU memory, checkpoint-download time, and worker startup time?
- [ ] What is the measured cost of an accepted result including failed candidates and retries?
- [ ] Does `repaint` change only a 3–5 second interval while preserving accepted audio outside it?
- [ ] Can a lower-quality/low-compute configuration produce a useful free-tier output?
- [x] Are exact model download sizes known? AnyAccomp is 2,078,199,136 bytes total. ACE's five major main+base tensor weights total 14,813,190,540 bytes; the complete pinned snapshots total 14,883,895,000 bytes, and the base file exceeds 2 GB.
- [ ] Are AnyAccomp/ACE model training-data claims and output terms acceptable for production after legal/product review?

## Genblaze integration

- [ ] Implement only after direct semantics are reproduced: can the AnyAccomp and ACE providers pass the current 16-method compliance suite plus StageMe retention/task tests?
- [x] What provider shape is required? Dedicated-worker `SyncProvider` for local AnyAccomp; real `BaseProvider` for queued AnyAccomp and ACE; exact package layout is in the system design.
- [x] How will local or worker audio become a Genblaze asset? Canonical allowlisted `file://` inside the worker or absolute validated HTTPS from a queued provider.
- [x] Which errors retry? Only bounded timeout/rate/server failures by default; auth, invalid input, content policy, and model errors fail fast.
- [ ] What second real provider/model stage makes the orchestration meaningfully multi-stage rather than decorative?
- [ ] What truthful fallback remains if ACE-Step `complete` fails?
- [ ] Can progress events and resumable job IDs survive worker/app restarts?

## Visual stage

- [x] Which renderer architecture leads? Revideo 0.11.0 with pinned Node/Chromium/fonts/container; direct FFmpeg/MoviePy remains Phase-0 fallback because repeat-render stability failed.
- [ ] Can Revideo complete three consecutive cold and warm 15-second 720p local-audio/font renders with one-frame sync and repeatable decoded output?
- [ ] Can one generated image plus deterministic waveform, lyric timing, lighting, and camera motion look intentional rather than templated?
- [ ] Which image provider/model is already entitled and affordable?
- [ ] What is the fallback if the image provider fails?
- [ ] Can the visual branch be revised independently while keeping accepted audio byte-identical?
- [ ] What low-data and audio-only exports should be created for constrained connectivity?
- [ ] Is full AI video omitted, precomputed, or offered only as a clearly optional renderer?
- [ ] After the deterministic stage passes, does the exact-version Replicate Wan 2.2 S2V endpoint produce one acceptable replaceable 3–5 second interval within one or two candidates at $0.02/output-second?
- [ ] Which Wan codec/duration constraints and exact prediction version apply immediately before payment, given the current official schema conflict?
- [ ] Does the S2V hero shot improve blind preference enough to justify its latency, consent, and failure risk?

## Affordability and access

- [ ] What free-tier generation budget can be sustained after measuring cold starts, retries, and rejected candidates?
- [ ] Can scale-to-zero avoid idle GPU cost without unacceptable startup time?
- [ ] What hard limits apply to source duration, output duration, candidates, and revisions?
- [ ] Can users complete the workflow from an ordinary phone browser without installing a model?
- [ ] What project-size budget keeps B2 storage and egress predictable?
- [ ] Can the app provide phone-friendly Opus/audio and low-bitrate MP4 exports?
- [ ] Is BYOK or self-hosting useful later without making the default product inaccessible?

## Voice consent and rights

- [x] Is a pre-call consent/recording template prepared? Yes: the checklist and consent template bind original/canonical hashes, deterministic derivation evidence, exact model/checkpoint, provider/region/spend cap, retention, deletion, and `training_reuse=false`.
- [x] Has the owner affirmed the exact F1 contains only authorized voice and no unauthorized backing media? Yes: recorded privately against fixture `F1-beb7138cae96` on 2026-07-27; this does not authorize provider processing or payment.
- [ ] Does the owner approve the final provider/region-specific consent and seven-day user-bundle retention wording?
- [ ] How can a user delete/revoke the source and derived private artifacts?
- [ ] Which derived project metadata may remain after revocation, if any?
- [ ] How will the UI distinguish original, deterministically transformed, and generated audio?
- [ ] How will the MVP prevent celebrity or third-party voice uploads from becoming an imitation feature?

## B2 account and project memory

- [ ] Can the entrant create and use B2 from Nigeria without operational friction?
- [ ] What caps and payment requirements appear in the actual account dashboard?
- [x] What is the upload boundary? Private bucket; short-lived presigned PUT or API proxy; browser presigned POST is unsupported; signed URLs never persist.
- [ ] What stable app endpoint will serve judge-facing accepted outputs?
- [x] How are objects namespaced? Immutable source/candidate/run/version/manifest keys are defined in the system design and readiness report; record exact B2 version IDs.
- [ ] Can the final accepted bytes be fetched and verified against the manifest?
- [x] Event Notifications require Support enablement and are not an MVP dependency.

## Rules, organizers, and judging

- [x] Is StageMe inside the official scope? Yes: Music/Art and Voice skills are explicit categories, and media transformation is encouraged.
- [x] Are individual judges publicly fixed? No: rules permit undisclosed and changing employees or third parties.
- [x] What should replace speculative judge profiling? The four equally weighted official criteria plus Backblaze's public Genblaze product thesis.
- [ ] Recheck overview, rules, updates, and discussions immediately before submission.
- [ ] Confirm the private-repository reviewer account immediately before submission (`b2genblaze` was previously named).
- [ ] Confirm no new live/finalist obligation was announced.

## Competition

- [ ] Recheck ONEFIELD for live provider/B2 worker integration before product commitment.
- [ ] Run and inspect Murmur's current hum-to-song flow if its setup is reproducible.
- [ ] Check whether another public entrant has shipped retained-vocal arrangement plus revision.
- [ ] Do not infer absence from the unpublished Devpost gallery.
- [ ] Conduct a blind comparison: can viewers describe why StageMe is not Murmur or ONEFIELD without architecture explanation?

## Multiple submissions

- [x] Do the rules permit multiple submissions? Yes, if they are unique and substantially different.
- [ ] Did the user's speech-to-text phrase “two entries” mean two hackathon submissions?
- [ ] If yes, can a second entry be independently narrow and production-ready without weakening StageMe?
- [ ] Default decision remains one polished entry unless the user explicitly chooses otherwise.

## Submission

- [ ] Who is the entrant/representative?
- [x] Is the product repository public or private? Public as of 2026-07-28, after a clean remote-history and GitHub-surface audit; this does not publish the private F1 media bundle.
- [ ] Which deployment and test-account path will remain live through August 12?
- [ ] Who records, narrates, and edits the demo?
- [ ] What real artifact proves each judging criterion?
- [ ] Can the full demo be understood if judges watch only the video?
