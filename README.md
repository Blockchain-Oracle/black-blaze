# Black Blaze

> **Context-engineering repository for the official Backblaze Generative Media Hackathon: Build with Genblaze on B2.**

The repository slug follows the requested working name, **Black Blaze**. The sponsor and product's correct name is **Backblaze**.

## Competition at a glance

| Item | Verified detail |
|---|---|
| Format | Online, public Devpost hackathon |
| Submission deadline | **August 3, 2026, 5:00 PM EDT** = **9:00 PM UTC** = **10:00 PM WAT (Nigeria)** |
| Required stack | A working generative-media application using **both Backblaze B2 and Genblaze** |
| Cash prizes | $7,000 grand prize; $2,000 second; $1,000 third |
| Bonus | 10 one-hour Backblaze architecture-mentorship awards for substantive SDK feedback |
| Core scoring | Real-world utility; production readiness; meaningful B2 orchestration; meaningful Genblaze use—equally weighted |
| Submission | Accessible working app, source repository, provider/model list, B2/Genblaze explanation, public demo video under 3 minutes |
| Nigeria | Likely eligible: adult residents of Nigeria are not named in the exclusions and Nigeria is not a country-wide OFAC program; final eligibility and prize verification remain Sponsor decisions |

**Official event:** https://backblaze-generative-media.devpost.com/

## Start here

**StageMe is the active feasibility-first build direction.**

1. [`AGENTS.md`](AGENTS.md) — operating rules for AI agents.
2. [`context-engineering/00-start-here/STAGEME_START_HERE.md`](context-engineering/00-start-here/STAGEME_START_HERE.md) — StageMe status, blockers, and required read order.
3. [`context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md`](context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md) — canonical product contract.
4. [`context-engineering/09-planning/STAGEME_SPIKE_PROTOCOL.md`](context-engineering/09-planning/STAGEME_SPIKE_PROTOCOL.md) — real-media experiments and stop conditions.
5. [`context-engineering/06-technical/STAGEME_SYSTEM_DESIGN.md`](context-engineering/06-technical/STAGEME_SYSTEM_DESIGN.md) — architecture and interfaces.
6. [`context-engineering/08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md`](context-engineering/08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md) — clean-room library/project ledger.
7. [`context-engineering/09-planning/STAGEME_AGENT_BUILD_HANDOFF.md`](context-engineering/09-planning/STAGEME_AGENT_BUILD_HANDOFF.md) — ordered implementation work.
8. [`context-engineering/00-start-here/EXECUTIVE_BRIEF.md`](context-engineering/00-start-here/EXECUTIVE_BRIEF.md) — competition orientation.
9. [`context-engineering/03-submission/SUBMISSION_CHECKLIST.md`](context-engineering/03-submission/SUBMISSION_CHECKLIST.md) — non-negotiable deliverables.
10. [`context-engineering/10-sources/SOURCE_LEDGER.md`](context-engineering/10-sources/SOURCE_LEDGER.md) — provenance and source URLs.

## Repository scope

This repository contains the competition research and StageMe's implementation-ready product/technical handoff. It does **not** yet contain the working StageMe application or reproduced media artifacts. Local source clones used for research are excluded from Git; their commit hashes and audits are recorded so another agent can reproduce the inspection.

## Validate the context

```bash
python scripts/validate_context.py
```

The validator checks required StageMe files, all repository Markdown links, all JSON, repository pins/licenses, stale active-status language, repository-escape links, and common secret patterns.

## Verification snapshot

Core competition research began on **2026-07-25**; StageMe product, model, library, and reference audits were updated on **2026-07-27**. Live surfaces such as participant count, discussions, releases, endpoint prices, licenses, and terms can change. Recheck them before paid execution, deployment, or submission.
