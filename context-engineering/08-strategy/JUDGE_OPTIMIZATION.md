# Judge Optimization Strategy

## Core thesis

Do not build "a Genblaze demo." Build a real product whose hard part is a resilient, inspectable generative-media pipeline. Then make both required technologies visibly essential.

## Scorecard design before code

Every concept must produce explicit answers:

| Criterion | Required product answer |
|---|---|
| Utility | Who has this problem, what do they do now, and what measurable outcome improves? |
| Production | What makes the workflow reliable, testable, secure, and usable after the demo? |
| B2 | Why does the product need durable object storage, organization, retrieval, policy, or provenance? |
| Genblaze | Why does the workflow need orchestration rather than one direct provider API call? |

If any answer is weak, reshape the concept before coding.

## Recommended architecture shape

```text
user job
  → validate/plan
  → Genblaze generation step(s)
  → automated evaluation/moderation
  → retry/fallback/fan-out when needed
  → deterministic transform/composition
  → B2 intermediate + final assets
  → manifest/index/verification
  → clear user outcome
```

## Make Genblaze meaningful

Use at least two of the following, but only where product-justified:

- chain/fan-in between modalities;
- provider/model fallback;
- concurrent fan-out and selection;
- agent-loop refinement against a quality score;
- progress streaming;
- parent-linked iterations;
- deterministic transformation in the same manifest;
- byte-level verification.

Meaningful depth beats a long provider list.

## Make B2 meaningful

Use at least three product-relevant roles:

- permanent inputs/intermediates/finals;
- structured project/run/version paths;
- generated metadata and provenance manifests;
- private delivery or public publishing;
- media search/index/catalog;
- lifecycle cleanup;
- immutable approval/audit record where justified;
- retrieval for replay, comparison, or downstream transforms.

## Production-readiness evidence

- clean deployed path and health check;
- provider entitlement preflight;
- timeout/retry/fallback behavior;
- exact error status in UI;
- input bounds and type validation;
- secrets management and least-privileged B2 key;
- offline tests plus a recorded live integration run;
- monitoring/logs and reproducible setup;
- a transparent degraded mode rather than fake success.

## Utility evidence

- one named persona, not "creators" in general;
- one high-friction job completed end to end;
- a before/after comparison;
- output that can be used immediately;
- no mandatory tour before first value.

## Demo structure — target 2:35

1. **0:00–0:20 — problem and outcome:** one user, one pain, one result.
2. **0:20–1:15 — real workflow:** user input → generation → visible progress → useful output.
3. **1:15–1:45 — Genblaze depth:** pipeline map, fan-out/fallback/evaluation/lineage.
4. **1:45–2:10 — B2 depth:** asset organization, durable media, manifest/index.
5. **2:10–2:25 — production proof:** failure recovery, tests, verification, security.
6. **2:25–2:35 — concise value/close.**

Do not spend the demo installing dependencies or narrating every framework.

## Feedback-prize strategy

A high-quality issue should emerge from actual implementation, not speculative feature requests. Include environment, versions, minimal reproduction, expected/actual behavior, business impact, workaround, and a scoped proposal. This may earn mentorship and also signals technical seriousness, but it is optional and should not distract from the product.
