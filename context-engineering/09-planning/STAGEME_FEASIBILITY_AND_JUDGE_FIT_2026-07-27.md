# StageMe Feasibility, Affordability, Competition, and Judge-Fit Audit

> Status: evidence-bound research as of 2026-07-27. StageMe has since been selected for a feasibility-first build. This audit remains supporting evidence, not the canonical product contract; read `STAGEME_PRODUCT_SPEC.md`. No media transformation has yet been reproduced in the StageMe environment.

## Why this audit exists

The earlier StageMe brief described an emotionally compelling product before proving that its central transformation was buildable. The user explicitly corrected that order of operations and asked for:

1. open-source or low-cost implementation paths;
2. affordability for users without expensive subscriptions or GPUs;
3. exact tool capabilities and limitations;
4. a stronger competitor scan;
5. a separate audit of judges, organizers, sponsor intent, and event fit.

This document answers those questions without converting model-card claims into demonstrated product capabilities.

## Executive finding

StageMe is **not yet approved to build**, but it is no longer technically fantastical if narrowed to:

> Record a rough, authorized vocal or musical fragment. StageMe preserves the real recording, uses an open music model to arrange backing tracks around it, and renders a shareable audiovisual stage with one bounded revision.

The feasible core is **not**:

- perfect AI singing correction;
- instant cloning of anyone's singing voice;
- a photorealistic synthetic performer;
- a complete music video generated locally on ordinary hardware;
- every interaction mode—singing, humming, tapping, acting, gesture, and camera motion—at once.

The credible open-source anchor is ACE-Step 1.5's documented `complete`, `lego`, cover, and repaint operations. The strongest visual plan is generated stage art plus deterministic animation/composition, not mandatory full video diffusion.

A real timed and qualitative spike is still required. The current audit environment has no visible NVIDIA GPU tooling, so no local model speed or quality claim has been independently reproduced.

## Corrected product statement

### Narrow promise

```text
rough human vocal or musical fragment
→ analysis and explicit creative direction
→ generated accompaniment around the original performance
→ shareable animated audiovisual stage
→ change one bounded section without losing accepted work
```

### Identity policy

The identity anchor is the person's **actual recording**, not an inferred synthetic clone.

This avoids making the MVP depend on voice-cloning quality and reduces impersonation risk. The system may clean, align, mix, or layer the authorized recording, but it must label what is original, deterministically transformed, and generated.

### Perform the Prompt

For MVP, this means only:

- record one vocal/hum/beatbox seed; and
- add one spoken or typed emotional/style direction.

Gesture, acting, camera movement, and multimodal performance control are deferred.

## Open-source audio audit

### 1. ACE-Step 1.5 — strongest candidate

Primary sources:

- <https://github.com/ace-step/ACE-Step-1.5>
- <https://huggingface.co/ACE-Step/Ace-Step1.5>
- <https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/API.md>
- <https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INFERENCE.md>

Observed evidence:

- MIT repository and model-card license.
- Public repository had 11.8K observed stars and was pushed on 2026-07-25 at audit time.
- REST API is first-party and asynchronous:
  - `POST /release_task`;
  - `POST /query_result`;
  - `GET /v1/audio`.
- Source audio can be uploaded as multipart data.
- Documented task types:
  - `text2music`;
  - `cover`;
  - `repaint`;
  - `lego`;
  - `extract`;
  - `complete`.
- `complete` is explicitly described as completing an incomplete track with specified instruments, adding backing tracks, and auto-completing musical ideas.
- `lego` generates a specific instrument track in the context of existing audio.
- `repaint` regenerates a bounded time range while preserving the rest.
- The base 2B model supports `extract`, `lego`, and `complete`; the faster turbo/SFT variants do not.
- The base model uses 50 steps and is rated lower quality than the turbo/SFT variants in the project's own model table.
- The 2B weight footprint is approximately 4.7 GB before quantization/offload according to the repository.
- The project supports CUDA, Apple Silicon/MLX, AMD/ROCm, Intel XPU, and CPU, but CPU is described as slow/testing-oriented.
- The README advertises `Vocal2BGM`, but a repository code search found that literal capability only in descriptive documentation—not as a dedicated task, test, or API operation.

Conclusion:

- `complete` is the honest StageMe spike path.
- `Vocal2BGM` must not be claimed as independently verified.
- The first spike must test whether `complete` preserves a rough vocal while generating coherent backing tracks.
- The second spike must test `repaint` as the bounded revision.

### AnyAccomp — secondary spike candidate

Primary sources:

- <https://github.com/AmphionTeam/AnyAccomp>
- <https://huggingface.co/amphion/anyaccomp>

Observed evidence:

- MIT repository;
- explicitly targets accompaniment generation for vocals and solo instruments;
- extracts core melodic features through a quantized melodic bottleneck before flow-matching accompaniment generation;
- publishes pretrained VQ, flow-matching, and vocoder checkpoints;
- public repository had 39 observed stars and was last pushed on 2025-12-22 during the audit;
- README does not publish a clear minimum-VRAM or latency table.

Conclusion:

AnyAccomp is more purpose-specific than ACE-Step and should be tested on the same authorized input fixtures. Its smaller ecosystem, older last push, and missing performance envelope make it a secondary candidate rather than the default.

### HeartMuLa — permissive but not source-conditioned yet

Source: <https://github.com/HeartMuLa/heartlib>

Observed evidence:

- Apache-2.0 code and weights according to the repository;
- 3B text/lyrics-controlled music generation and released checkpoints;
- current inference speed reported around real-time factor 1.0;
- repository recommends two RTX 4090 GPUs for convenient model/codec separation, with a lazy-load single-GPU path;
- reference-audio conditioning remains explicitly listed as TODO.

Conclusion:

HeartMuLa can be a text/lyrics generation fallback or comparison baseline. It cannot currently anchor StageMe's source-performance-preservation claim.

### 2. Seed-VC

Source: <https://github.com/Plachtaa/seed-vc>

Observed evidence:

- GPL-3.0.
- Repository is archived.
- Supports zero-shot voice and singing voice conversion from a short reference.
- README reports testing on an RTX 3060 laptop.

Why it is not the MVP anchor:

- archived dependency;
- copyleft integration implications;
- voice conversion solves a different problem from accompaniment;
- stronger impersonation and consent risks;
- no need if the product preserves the real vocal.

### 3. RVC

Source: <https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI>

Observed evidence:

- MIT;
- active and widely used;
- can perform voice conversion and supports training/inference workflows.

Why it is not the MVP anchor:

- normally requires obtaining or training a target voice model;
- adds setup friction;
- encourages the product toward “sound like someone else” rather than “finish my idea”;
- creates consent, impersonation, and rights risks without improving the core arrangement story.

### 4. DiffSinger

Source: <https://github.com/MoonInTheRiver/DiffSinger>

Observed evidence:

- MIT;
- active singing synthesis system;
- expects structured inputs such as lyrics, MIDI, pitch/F0, and acoustic models.

Why it is not the MVP anchor:

It is useful synthesis infrastructure, but not a frictionless rough-vocal-to-finished-performance path.

### 5. AudioCraft / MusicGen

Source: <https://github.com/facebookresearch/audiocraft>

Observed evidence:

- code is MIT;
- released model weights are CC-BY-NC 4.0 according to the repository.

Decision:

Do not use those weights as the commercial-path foundation.

### 6. Deterministic support tools

- Demucs: MIT stem separation.
- `python-audio-separator`: MIT wrapper/integration surface.
- Whisper: MIT code and weights for transcription.
- WhisperX: BSD-2-Clause, word-level alignment, CPU path available.
- ffmpeg/ffprobe: media inspection, normalization, muxing, and validation subject to the selected build's licensing configuration.

These are production support components, not the magical transformation.

## Genblaze integration audit

Primary sources:

- <https://github.com/backblaze-labs/genblaze>
- `docs/guides/new-provider.md` at audited commit `293beade3e705d69b29dbf57402800f8a868313f`
- `docs/features/provider-system.md` at that commit

Observed evidence:

- Genblaze supports custom providers through Python entry points.
- A polling provider implements:
  - `submit()`;
  - `poll()`;
  - `fetch_output()`.
- ACE-Step's REST job model maps directly to that lifecycle.
- Genblaze accepts `file://` assets for local outputs and HTTPS assets for remote ones.
- A custom provider can declare input/output capabilities, normalize parameters, attach audio metadata, classify errors, expose retries, and participate in B2 sinks/manifests.
- Provider compliance tests are supplied by Genblaze.
- Cost is not automatically known; a pricing strategy must be registered.

Conclusion:

ACE-Step not being a built-in connector is additional engineering, not an architectural blocker. A real `genblaze-acestep` adapter must be written and tested if the spike passes. Manual UI automation is not acceptable.

## Visual-performance audit

### Full local video generation

#### FramePack

Source: <https://github.com/lllyasviel/FramePack>

- Apache-2.0;
- minimum stated GPU memory: 6 GB;
- official README reports 1.5–2.5 seconds per frame on RTX 4090 and four to eight times slower on cited laptops.

Low VRAM does not mean low latency.

#### Wan 2.1 / 2.2

Sources:

- <https://github.com/Wan-Video/Wan2.1>
- <https://github.com/Wan-Video/Wan2.2>

- Apache-2.0 repositories;
- serious character/audio-driven models are large;
- Wan 2.1's 1.3B path reports roughly four minutes for five seconds of 480p on an RTX 4090;
- Wan 2.2's 14B official paths can require 80 GB VRAM;
- the 5B consumer path targets a 4090-class machine.

#### MuseTalk

Source: <https://github.com/TMElyralab/MuseTalk>

- MIT repository;
- can run in low VRAM;
- its README example reports roughly five minutes for eight seconds on an RTX 3050 Ti.

#### LatentSync / InfiniteTalk / LivePortrait

These can animate or lip-sync people but add:

- more models and preprocessing;
- identity-consistency and safety risks;
- larger hardware requirements;
- a photo/talking-head product shape the user does not want;
- latency inconsistent with the narrow demo budget.

Decision:

Full AI video is not a required MVP stage.

### Optional hosted audio-bound hero shot

Official endpoint: <https://replicate.com/wan-video/wan-2.2-s2v>

Observed evidence on 2026-07-27:

- official warm Replicate model with 127.9K displayed runs;
- accepts a reference image, audio file, and prompt;
- price displayed as $0.02 per second of output video;
- the loaded example used approximately 14.848 seconds of audio and displayed a generation time of 1 minute 52 seconds;
- the underlying model is Wan 2.2 S2V 14B.

Cost envelope before retries:

- 10-second shot: $0.20;
- 15-second shot: $0.30;
- three 15-second candidates: $0.90.

Conclusion:

A single S2V hero shot is financially plausible and could dramatically improve the reveal. It is not yet reliable enough to make mandatory because singing behavior, likeness consistency, safety, latency variance, and accepted-candidate rate remain unmeasured. Test it only after the audio arrangement passes. Deterministic stage animation remains the fallback and must be good enough to submit independently.

### Affordable visual renderer

Recommended composition layer:

- one or more generated stage/background images through a confirmed image provider;
- the real user's waveform or silhouette, not a synthetic cloned face;
- lyrics or key phrases with word/phrase timing;
- beat-reactive lighting and motion;
- deterministic pan, zoom, transitions, and final MP4 mux.

Permissive candidates observed:

- Motion Canvas: MIT — <https://github.com/motion-canvas/motion-canvas>
- Revideo: MIT — <https://github.com/midrender/revideo>
- MoviePy: MIT — <https://github.com/Zulko/moviepy>
- PixiJS: MIT — <https://github.com/pixijs/pixijs>

Remotion is technically capable but its repository warns that a company license is required in some cases. Prefer a clearly permissive path for this project's affordability/open-source story.

Optional full-video rendering can be a later provider branch, not the core promise.

## Affordability audit

### Open source is not automatically accessible

A free model that requires a 24 GB GPU, multi-gigabyte downloads, and complex setup is not accessible to a low-income user.

The user-facing product should therefore be browser-first and server-executed:

- record in a browser;
- short Opus upload;
- no local model installation;
- scale-to-zero GPU worker;
- hard duration and retry budget;
- accepted-result caching;
- audio-only and low-data exports;
- project portability and optional self-hosting/BYOK later.

### Current observed GPU pricing

Official RunPod pricing, updated 2026-07-17, showed:

Secure pods:

- RTX A5000 24 GB: $0.27/hour;
- L4 24 GB: $0.39/hour;
- RTX 3090 24 GB: $0.50/hour;
- RTX 4090 24 GB: $0.69/hour.

Serverless:

- 24 GB L4/A5000/3090 class: $0.69/hour;
- 24 GB RTX 4090: $1.10/hour.

Source: <https://www.runpod.io/pricing>

Pure GPU-time examples, excluding cold starts, model loading, storage volumes, CPU, retries, and provider margin:

| Rate | 30 seconds | 120 seconds | 300 seconds |
|---|---:|---:|---:|
| $0.69/hour | $0.00575 | $0.02300 | $0.05750 |
| $1.10/hour | $0.00917 | $0.03667 | $0.09167 |

These numbers show a possible free-tier envelope, not measured ACE-Step economics.

### B2 storage economics

The current official B2 pricing page displays:

- $6.95/TB-month;
- free egress up to 3× average monthly data stored, then $0.01/GB;
- free API calls within documented allowances;
- no minimum file-size fees;
- no minimum storage-duration fees.

Source: <https://www.backblaze.com/cloud-storage/pricing>

Explicit assumption example:

- 1,000 projects;
- 50 MB of durable source/intermediate/output data each;
- 50 GB total.

At the displayed storage rate, that is approximately $0.35/month and an included-egress envelope of roughly 150 GB/month. Generation compute is the dominant cost.

The current rendered pricing page did not expose the older “first 10 GB free” claim, so this audit does not rely on it.

## Competitor and entrant audit

Competitors are evidence and calibration, not an automatic veto.

### ONEFIELD — direct event overlap

Source: <https://github.com/TierraLinn/onefield-by-ariyus-one>

Description:

> turns a real human voice into generative music, visual fields, and a consent-first global instrument using Genblaze and Backblaze B2.

Observed state:

- created 2026-07-21;
- browser microphone capture, spectrum analysis, Web Audio layering, receipts, consent UI, and backend scaffolding are described as real;
- README explicitly states that without the media API URL, the final generative pipeline is representative;
- real provider worker integration and end-to-end deployment remain TODO.

Implication:

StageMe cannot rely on “voice becomes music and visuals” as its novelty. It must beat ONEFIELD through a narrower, real end-to-end transformation and revision—not a broader manifesto.

### Murmur — strongest external product overlap

Source: <https://github.com/p-to-q/murmur>

Observed promise:

- consumer hum-to-song studio;
- melody correction and arrangement pipeline;
- shareable audio, poster, and audio-backed video;
- substantial documented architecture.

Implication:

Hum-to-song is not a new category. StageMe's differentiation must be the retained real vocal, stage/reveal experience, constrained revision, Genblaze reliability, and B2 project memory.

### InstantBandAI

Source: <https://github.com/jeremystiffler/instantbandai>

Promise:

> rough vocal, piano, guitar, or phone demo into a fuller band arrangement.

Observed state:

- small repository/README;
- provider integrations listed as roadmap.

Implication:

The problem is legible and independently discovered, but execution remains the opportunity.

### Vanta

Source: <https://github.com/itsjwill/vanta>

- broad open-source media/video engine;
- combines local voice, avatar, captions, video generation, ACE-Step music, and timeline composition;
- demonstrates component availability;
- not a focused consumer transformation product.

### Official starter app

Backblaze's official multi-provider sample already turns one prompt into a narrated, scored, captioned MP4 using storyboard, image, video, TTS, music, and final composition.

Implication:

A generic multimodal creator is indistinguishable from the sample. StageMe must show human input, identity preservation, constrained revision, and project continuity.

### Visibility limitation

The live Devpost gallery remains unpublished. It showed 1,102 participants during the audit. Public GitHub sampling cannot establish competitor absence or represent the full field.

## Hackathon scope and judge-fit audit

Official event: <https://backblaze-generative-media.devpost.com/>

### Scope

StageMe is squarely within the published scope:

- Music/Art is an explicit category.
- Voice skills are an explicit category.
- The overview includes music, voice, audio, transformation, video, and multimodal examples.
- B2 and Genblaze are required; GMI Cloud is optional.

### Judging process and criteria

Stage 1 is a pass/fail screen for clear generative-media fit and legitimate use of both required technologies. A beautiful app that treats Genblaze or B2 as decorative risks failing before comparative scoring.

Stage 2 uses four equally weighted criteria:

1. real-world utility;
2. production readiness;
3. meaningful Backblaze B2 integration;
4. meaningful Genblaze orchestration.

The published tie-break order begins with real-world utility. Lead the pitch with the recurring user problem and transformation, not infrastructure.

The rules allow judges to evaluate from the video alone, making an immediate before/after essential.

### Named judges

The official rules say judges are selected by the sponsor and may be employees or third parties. Individual judges may not be listed and may change.

No fixed public judge panel was found. Do not present employees or maintainers as confirmed judges.

### Public sponsor-side sources

- Jeronimo De Leon authored Backblaze's official Genblaze article; his GitHub bio says he is building at Backblaze.
- Gonzalo Peña-Castellanos (`goanpeca`) identifies as a Backblaze senior software engineer focused on open-source AI.

These are useful sources of sponsor/SDK intent, not confirmed judges.

### Sponsor product thesis

Official article: <https://www.backblaze.com/blog/introducing-genblaze-a-python-sdk-for-generative-media-pipelines/>

Key thesis:

> The pipeline is becoming the moat.

The article emphasizes:

- multiple providers rather than one hard-coded model;
- model-specific routing and fallback;
- retries and output guards;
- progress events;
- concurrency and backpressure;
- durable object storage;
- SHA-256-verified provenance;
- a pipeline that survives model churn.

### What StageMe must show to fit that thesis

- an ACE-Step custom provider plus at least one other meaningful model/provider stage;
- a fallback path that produces a truthful degraded output rather than failing silently;
- progress state and resumable jobs;
- accepted and rejected candidates in B2;
- a bounded repaint/revision that reuses previous artifacts;
- deterministic audio/video validation;
- final manifest verification;
- explicit cost/retry budget.

Simply running ACE-Step and uploading the MP3 to B2 would be a weak Genblaze submission.

## Multiple submissions

The official rules permit multiple submissions by the same entrant, but each must be unique and substantially different.

This does **not** make two entries strategically wise. Production readiness is equally weighted, and the deadline is compressed. Do not split into two products unless both become narrow, independent, and fully polishable. No second entry is currently selected.

## Proposed MVP architecture

```text
Browser
  ├─ record 5–10s authorized vocal/hum/beatbox seed
  ├─ capture one style/emotion direction
  └─ upload source directly to private B2 path

Genblaze pipeline
  1. inspect + deterministic media validation
  2. transcribe/analyze lyrics, tempo, pitch contour, and energy
  3. language step creates bounded arrangement + stage brief
  4. ACE-Step custom provider:
       primary: complete source with selected backing instruments
       optional: lego one additional track
  5. audio validation + human candidate selection
  6. image provider creates one stage world, with fallback
  7. Motion Canvas/Revideo/MoviePy deterministic audiovisual render
  8. bounded revision:
       ACE-Step repaint a selected audio interval OR
       regenerate one visual layer while preserving audio
  9. final mux + validation
  10. B2 sink + manifest verification

B2 project
  ├─ source recording + consent
  ├─ analysis and creative brief
  ├─ model/config/version data
  ├─ candidates and validation reports
  ├─ accepted arrangement
  ├─ generated stage art and render ingredients
  ├─ revision branches and locked elements
  ├─ low-data/audio-only exports
  └─ final manifest and checksums
```

## Bounded fallback design

If ACE-Step `complete` fails quality or latency:

1. analyze the source for tempo/key/style;
2. generate a short instrumental independently;
3. mix the real vocal over it;
4. clearly label this as a fallback because the instrumental is not tightly conditioned on the vocal;
5. retain the source and allow the user to reject it.

If generated visual art fails:

- use a deterministic audio-reactive stage theme derived from selected colors and energy;
- still produce the audiovisual result;
- label the degraded branch in the manifest.

If neither audio path produces a perceptibly connected result, stop StageMe rather than disguising text-to-music as performance transformation.

## Required spike before selection

### Spike A — source-conditioned arrangement

Use three authorized inputs:

1. spoken/sung lyric with approximate pitch;
2. hummed melody;
3. beatboxed/rhythmic fragment.

For each, run ACE-Step base `complete` with the same bounded instrument request.

Measure:

- cold-start time;
- warm generation time;
- GPU and CPU memory;
- output duration;
- source-vocal survival and intelligibility;
- timing drift;
- musical coherence;
- failure rate;
- deterministic validation;
- human preference.

Pass only if at least two input types materially control the output.

### Spike B — bounded revision

Use `repaint` on a 3–5 second interval.

Pass only if:

- the unchanged region remains perceptibly stable;
- the requested interval changes;
- the new branch is stored separately;
- the accepted parent can be restored.

### Spike C — affordable stage renderer

Generate one stage image and render a 15–20 second video with waveform, timed words, beat-reactive light, and deterministic camera motion.

Pass only if:

- output finishes inside the demo budget;
- it looks intentional rather than like a music visualizer template;
- it has an audio-only or low-data export;
- all ingredients and the final MP4 persist in B2.

### Spike D — optional Wan S2V hero shot

Only after Spikes A–C pass, submit one approved stage/performer reference image and a 10–15 second accepted audio excerpt to the official Replicate Wan 2.2 S2V endpoint.

Measure:

- generation latency and variance;
- cost per candidate and per accepted shot;
- singing/audio synchronization;
- identity and visual consistency;
- safety and consent behavior;
- whether the hero shot materially improves preference over the deterministic stage.

Keep S2V only if one or two candidates reliably produce an acceptable result. The submission must remain functional without it.

### Stop conditions

Reject or radically reframe StageMe if:

- `complete` suppresses or mangles the source vocal;
- generation routinely exceeds the demo window;
- bounded repaint cannot preserve accepted material;
- the result is indistinguishable from Murmur/ONEFIELD without explanatory text;
- the only reliable path is unrelated text-to-music;
- provider access or compute cannot be secured without a brittle paid dependency.

## Current recommendation

### Do not build the full original StageMe brief.

### Do authorize only a narrow feasibility spike if the user wants to continue.

The best current formulation is:

> **StageMe: your rough performance, arranged and staged—not replaced.**

Its affordability promise should be:

> Works from a phone and does not require the user to own a GPU or subscribe to a stack of creative tools.

That promise is plausible but unproven until the timed ACE-Step and render spikes run on real compute.
