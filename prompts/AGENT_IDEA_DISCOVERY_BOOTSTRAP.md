# Agent Bootstrap Prompt — Backblaze Hackathon Context and Idea Discovery

Copy everything inside the prompt block into the agent that has the `context-engineering` and `hackathon` skills.

---

## Prompt

You are joining an active hackathon research and product-discovery effort for the **Backblaze Generative Media Hackathon: Build with Genblaze on B2**.

Your job is **not** to immediately generate a cute idea or start coding. Your first job is to acquire context, independently verify that context against live sources, expand the context-engineering repository, and then run a disciplined idea-discovery process that produces product-worthy directions.

### Repository

Public GitHub repository:

```text
https://github.com/Blockchain-Oracle/black-blaze
```

Public read access is sufficient for cloning; authenticated GitHub access is required only for authorized writes. Never ask for or expose the owner's GitHub token, API keys, model credentials, B2 keys, or other secrets.

### Skills

Before doing any substantive work:

1. Load your **`context-engineering`** skill.
2. Load your **`hackathon`** skill.
3. Follow both skills throughout the task.
4. If either skill conflicts with the repository's `AGENTS.md` or the official competition rules, the official rules control competition facts and `AGENTS.md` controls repository conventions.

### Operating mode

Work autonomously through the initial context and discovery pass. Do not stop immediately to ask broad questions such as “What do you want to build?” The purpose of this pass is to create enough evidence and structured alternatives for a productive conversation with the owner.

Ask the owner only when:

- access or credentials make research impossible;
- an irreversible or expensive action needs approval;
- a decision cannot be deferred without wasting substantial work.

Do not purchase anything, activate paid services, publish an app, submit to Devpost, change the repository's now-public visibility, or commit credentials.

---

## Phase 1 — Clone and orient

1. Clone the public repository; authenticated GitHub access is still required for authorized pushes:

   ```bash
   gh repo clone Blockchain-Oracle/black-blaze
   cd black-blaze
   ```

2. Create a working branch. Do not work directly on `main`:

   ```bash
   git checkout -b research/idea-discovery-YYYYMMDD
   ```

3. Read these files in order:

   1. `AGENTS.md`
   2. `README.md`
   3. `context-engineering/00-start-here/EXECUTIVE_BRIEF.md`
   4. `context-engineering/00-start-here/CONTEXT_MAP.md`
   5. `context-engineering/01-official-brief/HACKATHON_OVERVIEW.md`
   6. `context-engineering/01-official-brief/INSPIRATION.md`
   7. `context-engineering/02-rules/ELIGIBILITY_AND_RULES.md`
   8. `context-engineering/03-submission/SUBMISSION_CHECKLIST.md`
   9. `context-engineering/04-judging-and-prizes/JUDGING_AND_PRIZES.md`
   10. `context-engineering/05-schedule/SCHEDULE.md`
   11. `context-engineering/06-technical/GENBLAZE_GUIDE.md`
   12. `context-engineering/06-technical/B2_GUIDE.md`
   13. `context-engineering/06-technical/REPOSITORY_AUDITS.md`
   14. `context-engineering/07-live-signals/UPDATES.md`
   15. `context-engineering/07-live-signals/DISCUSSIONS.md`
   16. `context-engineering/07-live-signals/ISSUE_SIGNALS.md`
   17. `context-engineering/08-strategy/JUDGE_OPTIMIZATION.md`
   18. `context-engineering/08-strategy/COMPETITIVE_LANDSCAPE.md`
   19. `context-engineering/08-strategy/CONCEPT_SHORTLIST.md`
   20. `context-engineering/09-planning/RISK_REGISTER.md`
   21. `context-engineering/09-planning/OPEN_QUESTIONS.md`
   22. `context-engineering/10-sources/SOURCE_LEDGER.md`
   23. `context-engineering/10-sources/facts.json`
   24. `context-engineering/10-sources/repositories.json`

4. Run the repository checks:

   ```bash
   python scripts/validate_context.py
   python scripts/check_external_links.py
   ```

5. Summarize your understanding privately in working notes before generating ideas:

   - required technologies;
   - deadline and remaining runway;
   - submission artifacts;
   - eligibility caveats;
   - scoring criteria and tie-break order;
   - known provider, B2, Genblaze, cost, and deployment risks;
   - already-visible participant concepts;
   - assumptions that require live revalidation.

---

## Phase 2 — Independently refresh the live context

Do not assume the repository snapshot is still current. Revisit the original sources before relying on them.

### Mandatory official surfaces

Inspect all current content on:

- `https://backblaze-generative-media.devpost.com/`
- `/rules`
- `/details/dates`
- `/resources`
- `/updates`
- `/forum_topics`
- `/project-gallery`
- `/participants` if authenticated access is available
- official Backblaze hackathon and Genblaze articles
- official Backblaze B2 documentation
- all three official `backblaze-labs` repositories recorded in the source ledger
- current Genblaze releases, issues, pull requests, and relevant discussions

### Research beyond the event page

Conduct focused market and competitor research for the problem spaces being considered. Search:

- current Devpost submissions if the gallery has opened;
- public repositories linked from Genblaze issues;
- GitHub projects solving similar workflows;
- existing commercial products and open-source tools;
- current complaints, workarounds, and unmet needs on credible developer/creator communities;
- provider/API limitations that could invalidate a concept;
- whether the same idea is already common AI-product “slop.”

Use primary evidence wherever possible. Social posts and participant claims are signals, not official facts.

### Evidence discipline

Use the repository labels:

- `[OFFICIAL]`
- `[MANAGER]`
- `[OBSERVED]`
- `[INFERENCE]`
- `[OPEN]`

For every material new fact, record:

- exact source URL;
- page/repository title;
- date and time checked;
- what the source proves;
- whether it changes an existing conclusion;
- confidence and unresolved ambiguity.

Do not silently overwrite old facts. Record changes and conflicts.

### Repository expansion

Create these folders if the context-engineering skill agrees with this structure:

```text
context-engineering/11-independent-research/
context-engineering/12-idea-lab/
```

Recommended artifacts:

```text
11-independent-research/
├── RESEARCH_LOG.md
├── LIVE_CHANGES.md
├── MARKET_MAP.md
├── COMPETITOR_MATRIX.md
├── USER_PAIN_EVIDENCE.md
└── TECHNICAL_FEASIBILITY.md

12-idea-lab/
├── IDEA_INVENTORY.md
├── ANTI_SLOP_FILTER.md
├── CONCEPT_SCORECARD.md
├── TOP_CONCEPTS.md
├── REJECTED_IDEAS.md
└── CONVERSATION_BRIEF.md
```

Update the source ledger and machine-readable context when appropriate. Preserve a clear distinction between existing repository research and your new work.

For any newly relevant GitHub repository:

1. shallow-clone it under `.research-clones/`;
2. inspect its README, architecture, setup, license, recent activity, issues, and actual implementation;
3. record its exact commit SHA and purpose;
4. never vendor or copy its source into this repository;
5. never imitate a participant's unique product, wording, branding, or assets.

---

## Phase 3 — Build the idea universe before converging

Do not begin with product names. Begin with users, painful jobs, and evidence.

### Generate problem territories

Produce at least 10 materially different problem territories. Each territory must identify:

- a specific user—not “creators,” “developers,” or “businesses” generally;
- a recurring, expensive, frustrating, risky, or slow job;
- the current workaround;
- why existing products are insufficient;
- why generative media is essential rather than decorative;
- why Genblaze orchestration is load-bearing;
- why B2 storage/data orchestration is load-bearing;
- what useful result a first-time user can obtain within 30 seconds;
- what remains valuable after the hackathon demo.

The owner is not interested in photo-centric consumer apps. Give preference to developer tools, tools that complement coding agents without becoming coding agents or IDEs, voice/audio workflows, accessibility, provenance, media operations, QA, agentic pipelines, and overlooked professional workflows. These are preferences, not mandatory categories; evidence should still decide.

### The 30-second product test

A concept fails unless a new user can experience meaningful value within approximately 30 seconds of entering the usable workflow.

“Value” means receiving a useful result or insight, not merely seeing a landing page, creating an account, entering an API key, or watching a canned animation.

For each idea state:

```text
Second 0–5: what the user sees and supplies
Second 5–15: what the system does
Second 15–30: the useful result or insight returned
```

If the true workflow cannot complete that quickly because generation is slow, provide immediate partial value—such as a validated plan, preview, diagnosis, baseline comparison, or streamed first artifact—while the heavier job continues visibly.

### Product-not-demo test

Reject concepts that are primarily:

- a prompt box connected to a model;
- a provider comparison with no durable user workflow;
- a thin reskin of an official sample;
- a one-off generation stunt;
- an architecture diagram with no usable product;
- a generic “AI content studio”; 
- a dashboard whose data is mocked;
- a provenance claim that exceeds its actual trust model;
- a Web3/NFT layer that does not solve the user's job;
- dependent on unavailable GMI credits or unenabled B2 Event Notifications.

A product-worthy concept needs:

- a repeatable user workflow;
- stored projects/history/assets;
- clear input and output contracts;
- recovery from normal failures;
- a reason to return;
- a path beyond the hackathon;
- a judge-ready vertical slice that actually works.

### Anti-slop and uniqueness filter

For every candidate, answer:

1. What existing products already do this?
2. What public hackathon entries already resemble it?
3. What is the non-obvious insight?
4. What is the narrow wedge?
5. Why would the target user care enough to try it?
6. Why is this not just “AI for X”?
7. What would make a skeptical judge remember it the next day?
8. Could the same product exist without Genblaze or B2? If yes, the integration may be too thin.
9. Are we mistaking technical complexity for user value?
10. What evidence would falsify this concept quickly?

Maintain a rejected-ideas file with the reason for rejection so later agents do not recycle weak concepts.

---

## Phase 4 — Score, pressure-test, and converge

Score surviving concepts from 1–5 on:

- real-world utility;
- production-readiness potential;
- B2 depth;
- Genblaze depth;
- uniqueness/differentiation;
- 30-second time to value;
- demo clarity and emotional impact;
- implementation feasibility before the deadline;
- provider/account/cost risk;
- ability to remain a real product after the hackathon.

Do not manipulate scores to force a favorite. Explain each score with evidence.

For the top five concepts, write:

- one-sentence user/problem/outcome statement;
- exact 30-second experience;
- end-to-end product workflow;
- Genblaze pipeline steps;
- B2 object and metadata layout;
- required providers and exact model candidates;
- degraded/fallback mode;
- evidence for user demand;
- closest competitors;
- differentiation;
- seven-day implementation scope;
- demo story under three minutes;
- largest reasons it may fail;
- fastest falsification experiment.

Critique the repository's existing concept shortlist. Do not treat ShipCast, RenderGuard, AccessForge, DubGuard, or Provenance Gate as preselected answers. Keep, reshape, combine, or reject them based on current evidence.

---

## Phase 5 — Run lightweight feasibility spikes

Do not build five products. For the top two or three concepts, run the smallest reversible tests that resolve the biggest uncertainties.

Examples:

- credential-free Genblaze manifest construction;
- one minimum-cost live provider call if credentials are already available and use is authorized;
- one B2 upload/read/hash verification if credentials are already configured;
- exact model-entitlement preflight;
- 30-second clickable/static interaction prototype;
- sample object-key and manifest design;
- latency/cost estimate using documented pricing;
- competitor workflow test using public access;
- five-minute “stranger comprehension” test using only the proposed first screen and result.

Never fabricate tool output, model responses, users, demand evidence, costs, or test results. Clearly label unexecuted assumptions.

Do not expose secrets in logs, screenshots, commits, issues, or generated manifests. Do not spend money without owner approval.

---

## Phase 6 — Prepare the owner conversation

Your final deliverable is not just “Here are some ideas.” Produce `context-engineering/12-idea-lab/CONVERSATION_BRIEF.md` containing:

1. what changed since the existing research snapshot;
2. the strongest new market or technical evidence;
3. ideas rejected and why;
4. the top three concepts in ranked order;
5. the strongest argument for and against each;
6. the exact decision the owner needs to make;
7. 5–10 high-leverage questions for the owner;
8. your recommendation, confidence, and what would change your mind;
9. the next 24-hour experiment after selection;
10. any deadline, eligibility, provider, or cost warning requiring attention.

End your report with a proposed conversation agenda:

```text
1. Confirm the target user and painful job.
2. Compare the top three 30-second experiences.
3. Choose the concept to falsify first—not necessarily the concept to build.
4. Set a 24-hour proof target and kill criteria.
5. Decide only after the proof result whether to commit to the full build.
```

### Git discipline

- Work only on your branch.
- Run repository validators before committing.
- Commit all context changes with a descriptive message.
- Do not push or open a pull request unless the owner has authorized it or your operating environment already has explicit standing permission.
- Report the branch name, commit SHA, changed files, validation results, and any uncommitted work.

### Definition of done

This assignment is complete only when:

- the existing repository has been read and validated;
- live official sources have been refreshed;
- market and competitor evidence has been added;
- weak/common ideas have been explicitly rejected;
- the top concepts pass the 30-second and product-not-demo tests;
- scoring is evidence-backed;
- key technical uncertainties have been tested or clearly marked untested;
- the repository contains a durable conversation brief for the owner;
- no secrets or fabricated evidence were introduced.

Start now by loading the two skills, cloning the repository, reading `AGENTS.md`, and running the validators.

---
