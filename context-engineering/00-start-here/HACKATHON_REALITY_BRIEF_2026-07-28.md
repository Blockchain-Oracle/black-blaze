# Hackathon Reality Brief — 2026-07-28

> **Current authority:** product selection is reopened. No build direction is currently selected.
>
> **Purpose:** establish the competition, platform, and live-field facts before another idea pass. This document does not recommend, rank, or authorize a product.
>
> **Checked:** 2026-07-28, primarily 19:13–19:25 UTC. Mutable facts must be rechecked before implementation, paid use, deployment, or submission.

## Executive read

The organizer is asking for a working generative-media product that uses both Genblaze and Backblaze B2 in a meaningful way. It explicitly invites familiar categories—video and image tools, audio/music/voice workflows, media libraries, provenance archives, model comparison, agentic pipelines, and creator, marketing, education, entertainment, and developer tools.

**[OFFICIAL]** The published scoring model has four equally weighted criteria: real-world utility, production readiness, B2 storage/data orchestration, and Genblaze use. It does not publish a separate novelty score. The rules still require original, entrant-owned work and proper third-party rights.

**[INFERENCE]** Existing products or entrants in the same category are therefore calibration, not an automatic veto. A familiar category can remain viable when the entry serves a sharper user/job, produces a materially better first result, and uses its “add-ons” to improve a judged dimension rather than merely increasing feature count.

**[OBSERVED]** The official project gallery is still unpublished. The public participant page reports 1,146 participants but requires login to browse them; the authenticated Devpost connector exposes no participant-list endpoint, and the available browser sessions did not yield authenticated participant access. No claim about current entrant saturation can be made from that directory.

**Decision consequence:** preserve StageMe, MediaSpec, ShipCast, and the other prior concept work as research history, but do not route new agents into any of them as the chosen build. The next idea pass begins only after this reality brief and the official-source corpus are read.

## Competition contract

| Fact | Evidence | Current conclusion |
|---|---|---|
| What to build | **[OFFICIAL]** [Overview](https://backblaze-generative-media.devpost.com/) and [rules](https://backblaze-generative-media.devpost.com/rules) | A working generative-AI media software application using both B2 and Genblaze, solving a real user problem and showing a path to production. |
| Required technologies | **[OFFICIAL]** Rules | Backblaze B2 and Genblaze are mandatory. GMI Cloud is optional. |
| Deadline | **[OFFICIAL]** Rules | 2026-08-03 17:00 EDT / 21:00 UTC / 22:00 WAT. At 2026-07-28 19:25 UTC, approximately 6 days 1 hour 34 minutes remained. |
| Judging | **[OFFICIAL]** Rules and [criteria](https://backblaze-generative-media.devpost.com/#judging-criteria) | Four equally weighted criteria. Tie-break order: utility, production readiness, B2, Genblaze, then judge vote. |
| Working access | **[OFFICIAL]** Rules | A functioning app URL, free and easy judge access through judging, plus test credentials/instructions if authentication is used. |
| Repository | **[OFFICIAL]** Rules | Public or private repository containing necessary source, assets, and setup. Private repositories must grant the named reviewer account access. |
| Demo | **[OFFICIAL]** Rules | Public functioning demo video, less than 3:00. “About three minutes” elsewhere does not override the rule. |
| Provider disclosure | **[OFFICIAL]** Rules | List every AI provider and model used and explain both B2 and Genblaze usage. |
| Existing projects | **[OFFICIAL]** Rules | Permitted if B2 and Genblaze were added after the event began and the significant update is explained. |
| Multiple entries | **[OFFICIAL]** Rules | Permitted only when each entry is unique and substantially different. |

### Exact current submission schema

The Devpost connector returned a complete submission schema at `2026-07-28T19:14:26Z`:

| Field ID | Required field |
|---:|---|
| `27756` | App URL |
| `27757` | GitHub Repo URL |
| `27760` | Providers and models |
| `27761` | B2 and Genblaze usage |

The global schema reports `website_required=false`, but the custom App URL field is required. A demo video is required; a ZIP file is not.

## What the sponsor explicitly invites

**[OFFICIAL]** The [resources page](https://backblaze-generative-media.devpost.com/resources) and overview name:

- AI video generation or editing;
- image generation, remixing, transformation, and brand libraries;
- audio, music, podcast, voiceover, and voice workflows;
- multimodal campaign or media workflows;
- generated-media search, tagging, libraries, and archives;
- provenance-aware workflows;
- agentic pipelines that generate, evaluate, retry, and store outputs;
- model comparison;
- workflows that create media, metadata, thumbnails, and final assets;
- creator, marketing, education, entertainment, and developer tools.

These are examples, not separate prize tracks. **[OBSERVED]** The current Devpost schema reports no
judging tracks.

### What follows—and what does not

- **[OFFICIAL]** A product may live in a familiar category.
- **[OFFICIAL]** It must still be original work, rights-compliant, functional, and meaningfully use both required technologies.
- **[INFERENCE]** “Someone already made one” is weak rejection evidence by itself.
- **[INFERENCE]** “We added more features” is also weak differentiation unless those features improve the target user's outcome or one of the four judging criteria.
- **[OPEN]** The unpublished gallery prevents a complete entrant-by-entrant overlap audit today.

## Live Devpost state

### Updates

The Devpost connector returned four announcements, complete, at `2026-07-28T19:20:37Z`:

1. **[OFFICIAL]** [Genblaze v0.6.0](https://backblaze-generative-media.devpost.com/updates/45436-genblaze-v0-6-0), sent `2026-07-22T15:43:16Z`: provider SDK compatibility, Windows/B2 reliability, content-addressed deduplication, pricing fixes, security hardening, and `genblaze verify --fetch` for byte-level output verification.
2. **[OFFICIAL]** [Genblaze v0.5.0](https://backblaze-generative-media.devpost.com/updates/45363-genblaze-v0-5-0), sent `2026-07-17T16:38:50Z`: stronger Replicate/OpenAI/Google/GMI connectors, concurrency-safe streams, ordered caching, stricter schemas, and security improvements.
3. **[OFFICIAL]** [Multi-provider starter](https://backblaze-generative-media.devpost.com/updates/45182-genblaze-multi-provider-starter-app), sent `2026-07-07T19:49:37Z`: prompt to storyboard/images/video/TTS/music/captions/composed MP4, with selectable providers and every intermediate/final artifact stored in B2 through Genblaze.
4. **[OFFICIAL]** [Genblaze v0.4.0](https://backblaze-generative-media.devpost.com/updates/45048-genblaze-v0-4-0), sent `2026-06-29T14:46:24Z`: Hume TTS, AssemblyAI STT, in-flight retry resume, fan-in failure propagation, SSRF hardening, and stronger hash requirements.

### Discussions and account risks

- **[MANAGER]** GMI credits were limited to the first 270 eligible GMI signups who completed the request form. Managers repeatedly direct non-recipients to the official multi-provider sample. Do not make GMI credits a dependency.
- **[OBSERVED]** A participant reported a 2,500-operation daily B2 limitation; no manager answered. This is a risk signal, not an official account limit. Inspect the actual account caps and run a canary.
- **[MANAGER]** A narrow proprietary-client/private-backend arrangement was accepted in one reply, but the higher-precedence written rules still require the necessary source, assets, and setup. Do not generalize the reply beyond its facts.
- **[OBSERVED]** A new [private-repository question](https://backblaze-generative-media.devpost.com/forum_topics/44607-can-i-keep-my-github-repo-private-if-yes-who-should-i-invite-as-a-collaborator) had no reply when checked. The rules already name `b2genblaze` for private review access.

## Genblaze reality

### Released SDK versus moving source

- **[OFFICIAL]** Latest announced release: `v0.6.0` on 2026-07-22.
- **[OBSERVED]** The release name is not the version of every distribution. The announcement lists umbrella `genblaze` 0.4.4, core 0.3.7, and CLI 0.3.5; the inspected S3 distribution is 0.3.6.
- **[OBSERVED]** Official `main` advanced on 2026-07-28 to commit [`c5a57085a0ca78339eea65b91786f0edad7959e1`](https://github.com/backblaze-labs/genblaze/commit/c5a57085a0ca78339eea65b91786f0edad7959e1), ahead of the published release. Five zero-credential current-main suites produced 345 passed and 3 skipped; this reproduces selected contracts, not provider reachability, B2 access, or media quality.
- **[OBSERVED]** Latest published release: [`v0.6.0`](https://github.com/backblaze-labs/genblaze/releases/tag/v0.6.0) at tag commit `ce651213daa6eb90cca738e5ae2c56055a2f56e1`. Open PR #236 prepares a v0.7.0 wave; v0.7.0 was not released when checked.
- **[OFFICIAL]** The [Backblaze Labs organization](https://github.com/backblaze-labs) describes its projects as experimental, exploratory, and not production-supported.

### Load-bearing capabilities available to a product

**[OBSERVED]** Current Genblaze source and documentation provide pipeline steps, chaining, fan-in/fan-out, sync/async/streaming execution, provider fallback, retries and resume semantics, structured assets, cost strategies, SHA-256-bound manifests, B2/S3 sinks, an agent loop, and provider compliance contracts.

**[INFERENCE]** Merely importing Genblaze or wrapping one model call is weaker evidence than showing a workflow where its orchestration changes reliability, cost, progress, fallback, evaluation, or lineage. The official starter demonstrates architecture—not a product identity to reskin.

Two newly relevant official references were also shallow-cloned and pinned: [`nvidia-nemotron-genblaze-b2@71e1f120...`](https://github.com/backblaze-labs/nvidia-nemotron-genblaze-b2/commit/71e1f12040b011340f90aba99bc07bd07a7661c7) for multimodal ingestion/fan-out, and [`ai-saas-starter-kit@79085c93...`](https://github.com/backblaze-labs/ai-saas-starter-kit/commit/79085c93b01c7ac547f9cd959b0d00fd1bb972e1) for a production-shaped application shell. Both are MIT architecture references with older pinned Genblaze packages; neither supplies a product direction or proof of live provider/media behavior.

## B2 reality

- **[OFFICIAL]** The S3-compatible API is the preferred path for most new integrations. Use a scoped standard application key; the master key is unsupported by S3.
- **[OFFICIAL]** Private/public access is bucket-level. Per-object ACLs, IAM roles, and object tagging are unsupported.
- **[OFFICIAL]** Direct browser upload should use a short-lived presigned `PUT` or an application proxy. Browser presigned `POST` uploads are unsupported; CORS is not authorization.
- **[OFFICIAL]** B2 buckets are always versioned. Reusing an object key creates another version, and name-only deletion can leave older bytes.
- **[OFFICIAL]** Filename plus metadata is generally limited to 7,000 bytes, reduced to 2,048 bytes with server-side encryption or Object Lock. Full provenance belongs in separate manifest objects.
- **[OFFICIAL]** Do not equate ETag, VersionId, or native SHA-1 with the application's SHA-256 proof. Store the digest in a manifest and verify fetched bytes.
- **[OFFICIAL]** Current pricing: first 10 GB free; `$6.95/TB/30-day` beyond that; pay-as-you-go Class A/B/C transactions free; Class D event calls have 2,500/day free then `$0.004/10,000`; free egress up to 3× average monthly storage, then `$0.01/GB`, subject to documented partner exceptions.
- **[OFFICIAL]** New accounts default to 500 upload/download requests per second. Native API throttling returns `429`; S3 returns `503 SlowDown`, potentially with `Retry-After`.
- **[OFFICIAL]** Current S3 lifecycle APIs exist, despite an older official page saying lifecycle was Web/Native-only. Processing is approximately daily, not an immediate-deletion guarantee.
- **[OFFICIAL]** Event Notifications require Backblaze Support enablement and deliver at least once. They cannot be a mandatory MVP dependency until entitlement is confirmed.
- **[OFFICIAL]** Object Lock enablement is irreversible at bucket level. Do not use it casually or on a transient canary bucket.

Primary references: [B2 documentation](https://www.backblaze.com/docs/), [integration guide](https://www.backblaze.com/docs/en/cloud-storage-get-started-with-a-backblaze-integration), [S3-compatible API](https://www.backblaze.com/docs/cloud-storage-s3-compatible-api), [pricing](https://www.backblaze.com/cloud-storage/pricing), and [rate limits](https://www.backblaze.com/docs/cloud-storage-rate-limits).

## Live field and saturation boundary

| Surface | 2026-07-28 result | What may be concluded |
|---|---|---|
| [Participants](https://backblaze-generative-media.devpost.com/participants) | **[OBSERVED]** 1,146 displayed; names require login | **[INFERENCE]** Competition interest is high. Product overlap is unknown. |
| [Project gallery](https://backblaze-generative-media.devpost.com/project-gallery) | **[OBSERVED]** Not published | Absence of a visible gallery entry proves nothing. |
| Public repositories linked from Genblaze issues | **[OBSERVED]** Existing repository audits capture multiple participant/project signals | They calibrate execution and overlap, but are not a complete or organizer-certified entrant list. |
| Official starter | **[OFFICIAL]** Full multi-provider media pipeline | It establishes the expected architecture floor, not a mandatory product category. |

## Changes from the prior active snapshot

1. **Product authority changed.** StageMe's active-selection status is superseded by owner direction on 2026-07-28; its evidence is retained, not erased.
2. **Participant count changed.** 1,069 on 2026-07-25 became 1,146 on 2026-07-28; the value is explicitly volatile.
3. **Gallery status did not change.** It remains unpublished.
4. **Genblaze source changed.** `main` moved from the reproduced `293beade...` snapshot to unreleased `c5a57085...`; v0.6.0 remains the latest published release.
5. **The official announcements are now captured with exact timestamps and URLs.**
6. **A new unanswered private-repository forum topic appeared.**
7. **B2 documentation now clearly supports S3 lifecycle APIs and documents a 500-request/second default, despite older conflicting pages.**

## Conflicts and unresolved facts

- **[OFFICIAL] Conflict:** Rules say registration opened June 22 at 10:00 ET; the schedule surface says 12:30 PM EDT. Rules control. The closing deadline agrees.
- **[OFFICIAL] Conflict:** The main pricing page says `$6.95/TB/30-day`; stale official representations still expose `$0.005/GB-month`. Use the main pricing page for budgeting.
- **[OFFICIAL] Conflict:** Older lifecycle documentation says Web/Native only; current S3 lifecycle API documentation shows support. Use the current API docs.
- **[OPEN]** Complete participant concepts remain inaccessible while the gallery is closed and authenticated participant browsing is unavailable.
- **[OPEN]** Actual B2 account caps, region, payment state, key capabilities, and Event Notification entitlement require authenticated inspection and a harmless canary.
- **[OPEN]** Actual provider/model entitlements and budgets remain account-specific.
- **[OPEN]** No product is selected. No product-specific provider call, deployment, or paid experiment is authorized by this brief.

## Guardrails for the next idea pass

These are evidence-handling rules, not product recommendations:

1. Start from a specific user and repeated painful job.
2. Treat official example categories as allowed territory, not as ideas that must be avoided.
3. Treat competitor or category overlap as a prompt to sharpen the wedge, not an automatic kill signal.
4. Reject copying of product identity, wording, assets, or unique implementation.
5. Require a useful result or diagnostic within roughly 30 seconds of the usable workflow.
6. Require B2 and Genblaze to change the product's behavior, reliability, history, or trust—not merely appear in the architecture diagram.
7. Judge every add-on by the user outcome and the four official criteria.
8. Do not select a direction until the owner and agent compare evidence-backed alternatives.

## Primary links for the next agent

- [Hackathon overview](https://backblaze-generative-media.devpost.com/)
- [Official rules](https://backblaze-generative-media.devpost.com/rules)
- [Dates](https://backblaze-generative-media.devpost.com/details/dates)
- [Resources](https://backblaze-generative-media.devpost.com/resources)
- [Updates](https://backblaze-generative-media.devpost.com/updates)
- [Discussions](https://backblaze-generative-media.devpost.com/forum_topics)
- [Project gallery](https://backblaze-generative-media.devpost.com/project-gallery)
- [Participants](https://backblaze-generative-media.devpost.com/participants)
- [Backblaze documentation](https://www.backblaze.com/docs/)
- [Genblaze developer guide](https://www.backblaze.com/docs/en/cloud-storage-genblaze-developer-guide)
- [Backblaze Labs](https://github.com/backblaze-labs)
- [Genblaze](https://github.com/backblaze-labs/genblaze)
- [Official multi-provider sample](https://github.com/backblaze-labs/genblaze-gen-media-multi-provider-sample)
