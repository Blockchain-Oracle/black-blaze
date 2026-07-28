# Devpost Discussions and Manager Clarifications

Checked 2026-07-28 19:22 UTC. Forum: https://backblaze-generative-media.devpost.com/forum_topics

## 1. B2 2,500/day cap report

A participant reported that a daily 2,500-access limit blocked an AI-agent workflow. No manager response was present. Current official pricing language and older account/help behavior are not perfectly aligned; test the entrant's actual account, data caps, and read pattern.

**Design response:** cache aggressively, avoid polling/listing loops, trust storage-owned URLs where Genblaze supports it, and set account alerts/caps intentionally.

## 2. GMI Cloud promotional credits

Multiple participants reported missing, rejected, or exhausted GMI credits. Manager J D stated credits were only for the first 270 GMI signups who completed the request form and directed others to:

https://github.com/backblaze-labs/genblaze-gen-media-multi-provider-sample

Support requests were directed to the GMI Discord: https://discord.com/invite/Rjb2wSKXW

**Decision:** treat promotional GMI credits as unavailable unless already visible in the account. GMI itself is optional.

## 3. Private/proprietary client source

A participant asked whether a private backend repository plus a non-compilable proprietary macOS frontend and working build/video could comply. Manager J D said yes: a reviewer GitHub account would be provided for backend review, and a video was required.

**Caution:** this clarification addressed that specific arrangement. The written rules still require the repository to contain necessary source/assets/setup instructions. For maximum safety, provide complete judge-reviewable code unless there is a strong proprietary reason not to.

## 4. Starter repository

Manager confirmed the multi-provider sample as the starter showing Genblaze + B2 across providers.

## 5. New private-repository question

On 2026-07-28, a participant asked which collaborator to invite for a private repository. The topic had zero replies when checked:

https://backblaze-generative-media.devpost.com/forum_topics/44607-can-i-keep-my-github-repo-private-if-yes-who-should-i-invite-as-a-collaborator

The written rules already identify `b2genblaze`. Recheck the rules and topic immediately before submission rather than treating the unanswered post as new guidance.

## 6. Gallery and participant access

The project gallery remained unpublished. The public participant page displayed 1,146 but required login to browse names. The official Devpost connector exposes no participant-list endpoint, and the available browser sessions did not produce authenticated participant access. No participant concept was inferred from the count.

## All observed topic URLs

- https://backblaze-generative-media.devpost.com/forum_topics/44557-2500-max-day-rate-limits-for-free-buckets-on-b2-blaze
- https://backblaze-generative-media.devpost.com/forum_topics/44329-did-not-receive-gmi-cloud-credits
- https://backblaze-generative-media.devpost.com/forum_topics/44322-do-the-repos-need-to-be-full-repo
- https://backblaze-generative-media.devpost.com/forum_topics/44259-genblaze-gmi-credits
- https://backblaze-generative-media.devpost.com/forum_topics/44248-did-not-receive-gmi-cloud-credits
- https://backblaze-generative-media.devpost.com/forum_topics/44231-gmi-cloud-key-not-working
- https://backblaze-generative-media.devpost.com/forum_topics/44229-the-credits-request-form-this-promotion-has-reached-its-redemption-limit
- https://backblaze-generative-media.devpost.com/forum_topics/44224-starter-repo-for-genblaze-b2
- https://backblaze-generative-media.devpost.com/forum_topics/44607-can-i-keep-my-github-repo-private-if-yes-who-should-i-invite-as-a-collaborator

## Monitoring rule

Before implementation milestones and submission, check for new discussions and manager answers. Record participant reports separately from authoritative manager clarification.
