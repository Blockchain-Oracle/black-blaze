# AGENTS.md — Black Blaze Context Protocol

This file governs any AI agent working from this repository.

## Mission

Help the entrant build and submit a polished, useful, production-shaped generative-media application for the **Backblaze Generative Media Hackathon: Build with Genblaze on B2**.

## Mandatory reading order

1. `context-engineering/00-start-here/EXECUTIVE_BRIEF.md`
2. `context-engineering/01-official-brief/HACKATHON_OVERVIEW.md`
3. `context-engineering/02-rules/ELIGIBILITY_AND_RULES.md`
4. `context-engineering/03-submission/SUBMISSION_CHECKLIST.md`
5. `context-engineering/04-judging-and-prizes/JUDGING_AND_PRIZES.md`
6. `context-engineering/06-technical/GENBLAZE_GUIDE.md`
7. `context-engineering/06-technical/B2_GUIDE.md`
8. `context-engineering/08-strategy/JUDGE_OPTIMIZATION.md`
9. `context-engineering/09-planning/OPEN_QUESTIONS.md`

## Evidence labels

Use these labels in new research:

- **[OFFICIAL]** Directly stated by the official rules, Devpost event, Backblaze docs/blog, or official repository.
- **[MANAGER]** Public clarification by a Devpost hackathon manager.
- **[OBSERVED]** Directly observed in a live page, repository, test, or executed command.
- **[INFERENCE]** Reasoned conclusion, not guaranteed by the organizer.
- **[OPEN]** Unresolved and requiring confirmation.

Never turn an inference into an official requirement.

## Source precedence

1. Official Rules
2. Official Devpost requirement/schedule pages
3. Public manager clarifications in Devpost Discussions
4. Official Backblaze documentation and repositories
5. Official Backblaze blog/update posts
6. Third-party repositories and participant reports

If sources conflict, record the conflict. The rules expressly say they control.

## Hard constraints

- Deadline: **2026-08-03 17:00 EDT / 21:00 UTC / 22:00 WAT**.
- Product must meaningfully use **both** Backblaze B2 and Genblaze.
- Build a real generative-media app, not an LLM-only chat loop or static mock.
- Provide an accessible working app and free judge access through the judging period.
- Provide source code and setup instructions. If private, grant the specified reviewer account access.
- Demo video must be public and **less than 3:00**. Target 2:30–2:45.
- List every AI provider and model used.
- Do not commit secrets, API keys, presigned URLs, personal data, or licensed assets without permission.
- Do not copy participant code or product identity. Competitive repositories are research signals only.
- Do not promise eligibility, prize receipt, model availability, or credits; verify current conditions.

## Local research clone protocol

Any GitHub repository used as material research must be shallow-cloned under `.research-clones/<repo>`, which is ignored by Git. Record:

- canonical URL;
- inspected commit SHA;
- inspection date;
- license;
- purpose;
- relevant findings.

Update `context-engineering/06-technical/REPOSITORY_AUDITS.md` and `context-engineering/10-sources/repositories.json`. Do not vendor third-party source into this repository.

## Product-development protocol

Before implementation:

1. Create a one-sentence audience/problem statement.
2. Map the concept against all four judging criteria.
3. Define a load-bearing B2 role and load-bearing Genblaze role.
4. Prove provider/model entitlement with a minimal live call.
5. Prove B2 upload/read and manifest verification.
6. Build one vertical slice before broadening scope.
7. Maintain a real evidence log: URLs, screenshots, hashes, test output, provider/model names.

## Updating this context

Live data belongs in `context-engineering/07-live-signals/`. Stable rules belong in `02-rules/`. Technical findings belong in `06-technical/`. Every fact added should carry a source URL and checked date.
