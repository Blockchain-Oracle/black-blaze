# Open Questions

Resolve these before any implementation commitment or submission. No product is selected. StageMe is the leading hypothesis only after being narrowed to retained-vocal arrangement plus an affordable animated stage.

Primary audit: `STAGEME_FEASIBILITY_AND_JUDGE_FIT_2026-07-27.md`.

## Product proof

- [ ] Does ACE-Step 1.5 base `complete` preserve an authorized rough vocal while adding coherent backing tracks?
- [ ] Does AnyAccomp produce a more source-faithful accompaniment on the same authorized fixtures, and what are its real VRAM/latency requirements?
- [ ] Does a hummed seed materially influence the result, or does the model ignore it?
- [ ] Does a beatboxed/rhythmic seed materially influence the result?
- [ ] Can an uninformed viewer identify the source-to-output connection in under 20 seconds?
- [ ] Is the retained real vocal plus generated arrangement emotionally stronger than a generic text-to-song result?
- [ ] Is the result sufficiently distinct from ONEFIELD, Murmur, InstantBandAI, and the official multi-provider starter app?
- [ ] What exact user repeats this workflow, and what do they currently pay or struggle with?

## ACE-Step and compute

- [ ] Which GPU endpoint can run ACE-Step 1.5 base—not merely turbo—with `complete`, `lego`, and `repaint`?
- [ ] What are measured cold-start and warm-generation times for 15–30 seconds of audio?
- [ ] What are measured peak GPU memory, CPU memory, model-download size, and worker startup time?
- [ ] What is the measured cost of an accepted result including failed candidates and retries?
- [ ] Does `repaint` change only a 3–5 second interval while preserving accepted audio outside it?
- [ ] Can a lower-quality/low-compute configuration produce a useful free-tier output?
- [ ] Is a RunPod/GMI/other endpoint already available, or would the spike require paid setup?
- [ ] Are ACE-Step model weights, training-data claims, and generated-output terms acceptable for the intended use?

## Genblaze integration

- [ ] Implement only after spike approval: can a custom async ACE-Step provider pass Genblaze's provider compliance suite?
- [ ] What `ModelSpec`, capability declaration, parameter normalization, and audio metadata should the adapter expose?
- [ ] How will local or worker-produced audio become a valid `file://` or HTTPS Genblaze asset?
- [ ] Which errors are retryable, and which must fail fast?
- [ ] What second real provider/model stage makes the orchestration meaningfully multi-stage rather than decorative?
- [ ] What truthful fallback remains if ACE-Step `complete` fails?
- [ ] Can progress events and resumable job IDs survive worker/app restarts?

## Visual stage

- [ ] Which permissive renderer—Motion Canvas, Revideo, MoviePy, or another audited component—best supports the polished 15–20 second stage?
- [ ] Can one generated image plus deterministic waveform, lyric timing, lighting, and camera motion look intentional rather than templated?
- [ ] Which image provider/model is already entitled and affordable?
- [ ] What is the fallback if the image provider fails?
- [ ] Can the visual branch be revised independently while keeping accepted audio byte-identical?
- [ ] What low-data and audio-only exports should be created for constrained connectivity?
- [ ] Is full AI video omitted, precomputed, or offered only as a clearly optional renderer?
- [ ] After the deterministic stage passes, does the official Replicate Wan 2.2 S2V endpoint produce one acceptable 10–15 second audio-bound hero shot within one or two candidates at $0.02/output-second?
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

- [ ] What exact consent language authorizes processing and storage of the user's recording?
- [ ] How can a user delete/revoke the source and derived private artifacts?
- [ ] Which derived project metadata may remain after revocation, if any?
- [ ] How will the UI distinguish original, deterministically transformed, and generated audio?
- [ ] How will the MVP prevent celebrity or third-party voice uploads from becoming an imitation feature?

## B2 account and project memory

- [ ] Can the entrant create and use B2 from Nigeria without operational friction?
- [ ] What caps and payment requirements appear in the actual account dashboard?
- [ ] Will source recordings remain private and upload through signed URLs?
- [ ] What stable app endpoint will serve judge-facing accepted outputs?
- [ ] How will source, consent, analysis, candidates, accepted output, revision branches, and manifests be namespaced?
- [ ] Can the final accepted bytes be fetched and verified against the manifest?
- [ ] Event Notifications require support enablement; confirm they are not an MVP dependency.

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
- [ ] Is the eventual product repository public or private?
- [ ] Which deployment and test-account path will remain live through August 12?
- [ ] Who records, narrates, and edits the demo?
- [ ] What real artifact proves each judging criterion?
- [ ] Can the full demo be understood if judges watch only the video?
