# StageMe — Historical Provisional Concept Brief

> **Historical, unselected concept:** StageMe was narrowed and selected for a feasibility-first pass,
> but decision D-014 reopened product selection on 2026-07-28. The rationale remains useful; this file
> is not current selection or implementation authority. Broad input/video language below is not an
> implementation promise.

## Feasibility correction

The original emotional concept was broader than the evidence supported. The credible MVP preserves the user's real authorized recording and generates accompaniment plus an affordable animated stage around it. It does not promise perfect singing correction, voice cloning, a photoreal synthetic performer, or full local video diffusion.

Open source is not automatically accessible: users should not need to own a GPU. The intended path is a browser capture, scale-to-zero server compute, strict duration/retry budgets, cached accepted artifacts, and low-data exports.

## Product in one sentence

StageMe turns an imperfect human performance seed—humming, rough singing, spoken lyrics, rhythm tapping, or a performed direction—into a finished short song and visual performance that still feels unmistakably connected to the person who supplied it.

## Product versus interaction

- **StageMe** is the product and promised outcome.
- **Perform the Prompt** is the input interaction.

The user should not need to write:

> Create a 96 BPM Afrobeats-pop chorus in A minor with restrained percussion, layered harmonies, and a neon rooftop performance video.

They can instead:

1. hum the melodic idea;
2. tap or beatbox the rhythm;
3. speak or sing the lyrics imperfectly;
4. say how the performance should feel;
5. optionally type a short direction.

The system interprets those human signals as the creative brief.

## The emotional promise

> **Do not prompt a performer. Become the performer.**

The reveal is not merely that AI generated a song. It is that the rough, private fragment in the user's head became something they can hear, watch, revise, and share.

## Why this ranked first in its historical snapshot

StageMe is the first broadened-search direction to combine:

- a strong founder reaction;
- an obvious before/after;
- personal identity rather than generic generation;
- audio, language, image/video, and deterministic composition in one coherent outcome;
- a finished artifact instead of a dashboard;
- a meaningful Genblaze orchestration story;
- a load-bearing B2 project-memory story;
- a demo that can be understood before the architecture is explained.

## What the inspected videos taught us

### ElevenMusic Vocals

The playable 42-second demonstration shows:

- a short recorded sample represented as a waveform;
- a simple approval/use action;
- separate `Vocals` and `Styles` concepts;
- a conventional `Studio` / `Recent work` destination.

Its accompanying thread says one-shot users can upload one voice recording, while repeat users can fine-tune toward vocal tone, texture, and style.

Implication: **“generate a song in your voice” is already a feature.** StageMe cannot be a thin ElevenMusic-style wrapper. Its differentiation must be the complete performance transformation, visual story, human reaction, and bounded revision experience.

### Multi-era wedding film

The playable 99-second video combines generated historical action-romance scenes with the real bride and groom watching below. It repeatedly places versions of the couple in different eras, then returns to the ordinary modern subway encounter where they actually met.

Its emotional structure is:

```text
impossible versions of us
→ recurring personal motif
→ ordinary real-life payoff
→ visible human reaction
```

Implication: StageMe needs a simple personal premise and payoff. Technical polish alone is insufficient. The user's reaction should be part of the demo.

### Hume TADA

The 18-second video mostly shows branding and Apple hardware, while the post text carries the utility claim: ten-second voice sample, text input, offline expressive speech.

Implication: technical usefulness can produce bookmarks, but StageMe's visual demonstration must show the input and transformation directly.

## Proposed 20-second magic moment

```text
User records 5–10 seconds:
"We made it out..." sung roughly, followed by a hummed melody and tapped rhythm.

User says:
"Make it feel victorious but intimate—night rooftop, warm city lights."

StageMe produces:
- a polished short chorus or arrangement anchored to the user's recording;
- accompaniment and harmonies where provider capability permits;
- a short visual performance or lyric-world sequence;
- one playable finished artifact.
```

Then the user requests one bounded change:

> Keep my vocal and chorus. Make the opening quieter and change only the final visual scene to sunrise.

The system should preserve the locked elements and regenerate only the affected branch.

## Honest MVP boundary

Do **not** promise a complete three-minute song, flawless singing conversion, perfect lip-sync, a persistent synthetic celebrity, or a full nonlinear editor.

The first defensible artifact is:

- one authorized user;
- one 5–10 second performance seed;
- one 15–30 second finished excerpt;
- one musical direction;
- one visual premise;
- two or three short visual segments at most;
- one bounded revision;
- one versioned project in B2.

## Genblaze role

Subject to provider verification, Genblaze should coordinate:

1. transcription and analysis of the performance seed;
2. language reasoning that extracts lyrics, emotion, rhythm, and a bounded creative brief;
3. music/audio generation or arrangement;
4. authorized voice processing if an available provider genuinely supports it;
5. visual storyboard generation;
6. short video generation, potentially concurrent across shots;
7. retries or fallback within a fixed budget;
8. progress events and provenance;
9. final B2 sinks and manifest creation.

Genblaze is the production coordinator, not the underlying singing, music, or video model.

## B2 role

B2 is the durable project memory for:

- original recordings;
- extracted transcript and creative brief;
- waveform/rhythm metadata;
- lyrics and arrangement decisions;
- generated stems or mixes;
- storyboard frames;
- video candidates;
- accepted and rejected versions;
- locked-element state;
- final output;
- checksums, manifest, and provider provenance.

Without B2, StageMe would be a disposable provider call. With B2, it is a revisable performance project.

## Critical feasibility gates

### 1. Singing and voice transformation

Generic TTS is not singing enhancement. Verify one of these paths:

- an authorized singing-voice provider available through or usable alongside Genblaze;
- a provider that can preserve a user's vocal identity safely;
- a music model that can condition on a real vocal or melodic seed;
- a fallback composition path that keeps the user's original recording and generates accompaniment around it.

Fail the concept if the demo requires falsely claiming that TTS transformed rough singing.

### 2. Rights and consent

- Use only the participant's own voice or clearly licensed voices.
- Record explicit consent for voice processing.
- Do not support celebrity imitation in the MVP.
- Clearly label generated and transformed components.
- Preserve provider terms and model provenance in the project manifest.

### 3. Video feasibility

Verify:

- provider access and credentials;
- image-to-video or text-to-video path;
- generation time for two or three short segments;
- identity/visual consistency adequate for the demo;
- maximum retry budget;
- whether the live demonstration uses a small generation while a pre-seeded run proves the complete path.

### 4. Audio finishing

Generated songs can lose loudness and mix consistency. Apply deterministic checks for:

- duration;
- clipping;
- peak and integrated loudness;
- silence or missing audio;
- sample rate/channel expectations;
- final mux integrity.

Taste remains a human judgment.

## Three-minute demo shape

### 0:00–0:20 — Human seed

Record an intentionally rough vocal, hum, rhythm, or spoken lyric.

### 0:20–0:45 — Perform the Prompt

Add one natural performance direction. Show StageMe understanding the seed without requiring technical prompting.

### 0:45–1:20 — Reveal

Play the finished 15–30 second song and visual performance. Keep the person's reaction in frame.

### 1:20–1:45 — Control

Lock the vocal/chorus and revise one musical section or visual scene.

### 1:45–2:20 — Production proof

Show the source, intermediate assets, rejected/accepted candidates, lineage, and versions in the project—not a generic infrastructure dashboard.

### 2:20–2:45 — B2 proof

Fetch the accepted artifact and verify it against its manifest.

### 2:45–3:00 — Close

> StageMe: don't prompt a performer. Become the performer.

## Spike decision rule

Proceed only if a narrow spike proves all of the following:

1. a real human performance seed materially controls the result;
2. the audio transformation is honest and perceptibly connected to the source;
3. a 15–30 second output can finish inside the cost and time budget;
4. at least one visual segment can be produced reliably;
5. one bounded revision preserves a locked element;
6. source, intermediates, accepted output, and manifest can be stored and fetched from B2;
7. an uninformed viewer understands the before/after in under 20 seconds.

If voice transformation fails but accompaniment around the user's real recording succeeds, retain StageMe with a narrower promise. If neither path creates a striking result, stop rather than disguising a generic song generator as the product.
