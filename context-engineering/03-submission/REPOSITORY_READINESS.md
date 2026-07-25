# Product Repository Readiness Standard

The eventual product repository should make judge evaluation effortless.

## Recommended root files

```text
README.md                 problem, solution, live demo, architecture, quickstart
AGENTS.md                 agent constraints and project conventions
.env.example              names only; no secrets
ARCHITECTURE.md           data flow and B2/Genblaze load-bearing roles
SUBMISSION.md             final Devpost copy and provider/model list
DEMO_SCRIPT.md            shot-by-shot <3-minute script
EVIDENCE.md               executed tests, hashes, URLs, screenshots, limitations
LICENSE                   only after owner chooses a license
```

## README first screen

Within the first screen, show:

1. one-sentence user problem;
2. one-sentence product result;
3. live app link;
4. demo video link;
5. architecture image or compact pipeline line;
6. explicit "Built with Genblaze + Backblaze B2" statement.

## Reproducibility

- One setup path that works from a clean machine.
- Pin versions and document Python >=3.11 plus ffmpeg if needed.
- Include a credential-free local/demo mode, but clearly label mock outputs.
- Keep a separate live integration test gated by secrets.
- Health endpoint should reveal component readiness without exposing secret values.

## Judge experience

- Seed a sample project.
- Put a direct "Try demo" action on the landing page.
- Avoid mandatory account creation if possible.
- If an account is unavoidable, provide working credentials in the private Devpost field, not public source.
- Ensure media playback works cross-browser and private B2 links do not expire mid-judging.
