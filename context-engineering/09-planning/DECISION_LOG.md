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

- Historical decision: publish this research context publicly unless blocked by account policy.
- Superseded safety boundary: repository visibility, push, PR, or publication now requires task-specific owner authorization; an old publication preference is not standing permission for every agent.
- Historical task boundary: the 2026-07-27 pre-call assignment authorized readiness commits and pushes but not a visibility change.
- Current decision: on 2026-07-28, the owner explicitly authorized making `Blockchain-Oracle/black-blaze` public. A remote-history and GitHub-surface audit found no committed secrets, private media, private paths, large binaries, Actions logs, issues, pull requests, releases, or deployments. Unauthenticated GitHub API and web checks then confirmed public visibility.
- Boundary: this decision authorizes repository visibility only. It does not authorize app deployment, Devpost submission, provider processing, media publication, credential publication, or paid calls.

## D-006 — Deprioritize ShipCast after competitor/feasibility audit

- Decision: do not select ShipCast as the current hackathon build.
- Reason: PageBolt, PushPlay, RepoClip, and `makedemo` materially overlap the concept. The differentiating no-capture experience requires reliable preview deployments, authenticated test state, flow discovery, browser automation, and truthful feature verification. Requiring manual screenshots/recordings removes the value proposition the entrant cared about.

## D-007 — Validate MediaSpec before committing

- Decision: the next spike should test a narrow media quality-gate and recovery loop, not a general observability platform.
- Reason: deterministic checks are auditable and feasible; Genblaze retry/fallback and B2 artifact verification remain central rather than decorative.

## D-008 — Select MediaSpec provisionally, then reopen after field audit

- Initial decision: MediaSpec became the provisional concept because it was the first idea with explicit founder-product-fit evidence and it preserved meaningful Genblaze and B2 roles while avoiding ShipCast's autonomous-capture risk.
- Reopening evidence: the 2026-07-27 public-field audit found direct overlap with Waystation, Genblaze Studio QC, Crucible, ReproFrame, and VeriGen. More importantly, generic MediaSpec still lacked a concrete buyer outcome independent of its infrastructure. The hidden Devpost gallery had masked a technically advanced execution bar.
- Current decision: do not default to generic MediaSpec. Competitor presence is not a veto; learn from the visible builds without reactively imitating or fleeing them. Preserve the contract engine inside a coherent own-game product unless a stronger standalone buyer thesis emerges. ReachPack / AccessSpec is the leading validation candidate; DemoSpec and AssetMemory remain alternatives.
- Historical product brief: `MEDIASPEC_PROJECT_BRIEF.md`. Current field evidence: `../08-strategy/PUBLIC_FIELD_AUDIT_2026-07-27.md`.

## D-009 — Stop narrowing around MediaSpec or ReachPack

- Decision: neither MediaSpec nor ReachPack is selected. Stop treating ReachPack as the leading default and reopen discovery across video, audio, music, animation, VFX, and cross-modal experiences.
- Reason: the concepts had rational sponsor and architecture fit but did not create a strong founder reaction. The user wants the eventual direction to combine that personal recognition with evidence from what people are building, sharing, and struggling to do.
- Research implication: investigate current social behavior, visible transformations, repeated workarounds, implementation waves, and adjacent products before producing another recommendation. Competitor evidence is for calibration, not automatic rejection.
- Current signal map: `../08-strategy/GEN_MEDIA_SIGNAL_MAP_2026-07-27.md`.

## D-010 — StageMe becomes the leading candidate, with Perform the Prompt as its interaction

- Decision state: **StageMe is the current leading candidate, not yet an irreversible product selection or implementation authorization.** It must pass a narrow provider/latency/cost spike before commitment.
- Product distinction: StageMe is the outcome and product; **Perform the Prompt** is its input method. A user hums, sings imperfectly, speaks lyrics, taps a rhythm, or describes the intended performance instead of writing a technical generation prompt.
- Founder signal: this is the first broadened-search direction to produce a clear positive reaction from the user. That signal matters alongside—not instead of—technical and market evidence.
- Evidence adjustment: direct inspection of the ElevenMusic demo shows voice-sample approval and a conventional studio/recent-work interface. The feature “song in your voice” already exists; StageMe cannot differentiate as a voice-cloning wrapper.
- Demo insight: direct inspection of the multi-era wedding film shows that its emotional power comes from a recurring personal premise, a final real-life payoff, and the couple's visible reaction. StageMe's demonstration should likewise show imperfect human input, transformation, a finished audiovisual performance, the person's reaction, and one bounded revision.
- Feasibility gate: verify an authorized singing/voice-transformation path. Generic TTS is not equivalent to singing enhancement. If unavailable, preserve the user's real recorded vocal as the identity anchor and generate accompaniment, arrangement, and visual performance around it.
- Working brief: `STAGEME_CONCEPT_BRIEF.md`.

## D-011 — Narrow StageMe before any build commitment

- Decision state: StageMe remains a hypothesis, not the selected build. The earlier concept was too broad and assumed unverified singing/video capabilities.
- Credible audio path: preserve the user's real authorized recording and spike ACE-Step 1.5 base-model `complete` for backing-track arrangement plus `repaint` for bounded revision. The advertised `Vocal2BGM` label was found only in descriptive documentation, not as a dedicated API task or source implementation.
- Credible visual path: generated stage art plus deterministic animation/composition. An official Replicate Wan 2.2 S2V endpoint priced at $0.02/output-second makes one audio-bound hero shot a plausible optional spike after audio succeeds; full local video diffusion and synthetic performers remain nonessential.
- Affordability principle: open-source weights do not make a product accessible if users need expensive GPUs. Use browser capture, scale-to-zero compute, hard duration/retry budgets, B2 caching, and low-data exports.
- Competition adjustment: ONEFIELD directly overlaps inside the event, while Murmur already offers a substantial hum-to-song workflow. StageMe must prove a narrower real end-to-end transformation, retained vocal identity, staged reveal, and bounded revision.
- Judge-fit adjustment: individual judges are undisclosed. Optimize for the four official criteria and Backblaze's public thesis that the pipeline—not one model—is the moat.
- Evidence: `STAGEME_FEASIBILITY_AND_JUDGE_FIT_2026-07-27.md`.

## D-012 — Select StageMe for a feasibility-first build

- Decision: the user authorized StageMe documentation, research, and build preparation. StageMe is now the active direction, not merely a candidate. The full application and final submission remain conditional on the retained-performance media gate.
- Canonical core: one authorized 8–15 second rough sung performance → separate source-conditioned accompaniment/layer → literal original-source retention in the accepted mix → staged audiovisual artifact → one bounded child revision.
- New primary candidate: AnyAccomp, whose pinned implementation writes accompaniment separately and computes its mixture from accompaniment plus the original vocal waveform. ACE-Step `lego`, `complete`, and gated `repaint` remain required comparison/layer/edit experiments.
- Build order: magical artifact bundle first; deterministic contracts/QC/renderer may proceed in parallel; broad product UI follows only after source connection and emotional lift pass.
- Optional video: official Replicate Wan 2.2 S2V may produce one budgeted hero shot after audio acceptance; deterministic stage output remains mandatory.
- Canonical file: `STAGEME_PRODUCT_SPEC.md`. Start/handoff: `../00-start-here/STAGEME_START_HERE.md` and `STAGEME_AGENT_BUILD_HANDOFF.md`.
- Authorization boundary: this decision does not authorize unbudgeted paid calls, credential use, deployment, commit, push, or unsupported public claims.

## D-013 — StageMe is conditionally ready for one authorized AnyAccomp call

- Decision: the zero-cost pre-call pass is complete enough to run one capped F1 experiment, but media execution remains blocked until the owner supplies an authorized rough-sung fixture, approves the named GPU provider/region and processing disclosure, and approves a spend cap.
- First call: pinned AnyAccomp direct worker inference → separate accompaniment → StageMe-owned lossless source/accompaniment premaster → sample-aligned null test → deterministic QC → before/after human review.
- Environment boundary: stock AnyAccomp Python 3.9 remains isolated from the Python 3.11/3.12 Genblaze/control process. No maintained hosted AnyAccomp endpoint is currently available.
- Renderer boundary: Revideo remains the intended architecture, but one successful smoke followed by two failed rerenders keeps direct FFmpeg/MoviePy as the Phase-0 fallback.
- Follow-on order: ACE base `lego`; `complete` comparison; Revideo/B2 proof; `repaint` after an accepted parent; optional Wan only after deterministic-stage success.
- Decision evidence: `STAGEME_PRECALL_READINESS_REPORT.md` and `STAGEME_FIRST_CALL_RUNBOOK.md`.

## D-014 — Reopen product selection and return to official context

- Decision date: 2026-07-28.
- Owner direction: stop treating the current StageMe work as the build, refresh the full hackathon context from Devpost, Backblaze documentation, and official repositories, and do not choose another idea yet.
- Current decision: **no product is selected.** This entry supersedes only the active-selection status in D-012/D-013; it does not erase the StageMe research, fixture evidence, feasibility findings, or safety boundaries.
- Research rule: official example categories are permitted territory. A competitor or participant in the same broad category is calibration, not an automatic rejection. Original work, rights compliance, a sharper user/job, and materially better judged outcomes remain required.
- Add-on rule: an add-on matters when it improves real-world utility, production readiness, B2 orchestration, or Genblaze orchestration. Feature count is not differentiation by itself.
- Routing authority: `../00-start-here/HACKATHON_REALITY_BRIEF_2026-07-28.md` is the current facts-only orientation. Another concept decision requires a later decision-log entry.
- Authorization boundary: this decision does not authorize implementation, provider calls, B2 writes, spending, deployment, Devpost submission, or use/publication of private media.

## Pending decisions

- The target user, painful job, product direction, first falsification test, provider/model entitlement, B2 canary, deployment platform, budget, and team structure remain open. StageMe-specific execution questions remain preserved but dormant unless StageMe is explicitly selected again.
