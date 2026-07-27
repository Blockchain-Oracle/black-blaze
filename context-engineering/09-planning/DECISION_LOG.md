# Decision Log

## D-001 — Official name vs repository name

- Decision: repository working name is `black-blaze`; all documentation uses the sponsor's correct name, Backblaze.
- Reason: preserve the user's requested repo label without propagating an incorrect product name.

## D-002 — Local clones are not vendored

- Decision: clone research repositories under ignored `.research-clones/`; commit audits and SHAs only.
- Reason: preserves reproducibility and understanding without redistributing or nesting third-party source.

## D-003 — GMI Cloud is optional

- Decision: no strategy may depend on promotional GMI credits unless already present.
- Evidence: rules only require B2 + Genblaze; manager says first-270 allocation was exhausted.

## D-004 — Official rules control

- Decision: where schedule/overview/forum language differs, record both and follow rules.
- Example: submission start time conflict; deadline is consistent.

## D-005 — Public repository default for context

- Decision: publish this research context publicly unless blocked by account policy.
- Reason: all contents summarize public sources and the user wants other agents to pull it. The eventual product repository can be separately public or private.

## D-006 — Deprioritize ShipCast after competitor/feasibility audit

- Decision: do not select ShipCast as the current hackathon build.
- Reason: PageBolt, PushPlay, RepoClip, and `makedemo` materially overlap the concept. The differentiating no-capture experience requires reliable preview deployments, authenticated test state, flow discovery, browser automation, and truthful feature verification. Requiring manual screenshots/recordings removes the value proposition the entrant cared about.

## D-007 — Validate MediaSpec before committing

- Decision: the next spike should test a narrow media quality-gate and recovery loop, not a general observability platform.
- Reason: deterministic checks are auditable and feasible; Genblaze retry/fallback and B2 artifact verification remain central rather than decorative.

## D-008 — Select MediaSpec as the product direction

- Decision: MediaSpec is the selected concept; implementation commitment is gated on its end-to-end technical spike.
- Reason: it is the first shortlisted concept with explicit founder-product-fit evidence—the entrant stated they would personally buy it—and it preserves meaningful Genblaze and B2 roles while avoiding ShipCast's autonomous-capture risk.
- Product brief: `MEDIASPEC_PROJECT_BRIEF.md`.

## Pending decisions

- First media kind, team structure, provider stack, deployment platform, B2 access model, and product-repository visibility remain open. MediaSpec remains subject to the end-to-end spike gate.
