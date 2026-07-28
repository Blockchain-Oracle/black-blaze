# StageMe Open-Source Libraries and Reference Implementations

> Purpose: help implementation agents learn from existing tools without copying product identity, unlicensed code, mocks, or unsupported claims.
>
> **Historical, unselected candidate packet:** decision D-014 reopened product selection on 2026-07-28.
> These audits remain calibration evidence; they do not authorize StageMe implementation or establish
> its stack as the default. Recheck mutable repositories, releases, and model licenses if StageMe is
> explicitly selected again.

## 1. Clean-room rules

1. A public GitHub repository is not automatically licensed for reuse.
2. No recognized license means **inspect behavior, do not copy code or assets**.
3. A code license does not automatically cover model weights, datasets, fonts, sample media, or third-party dependencies.
4. Record commit, license, copied concept/code boundary, and attribution for every adopted dependency.
5. Prefer official APIs and upstream examples over scraping another product's implementation.
6. If StageMe is reselected, implement its product flow, visual identity, copy, and data model independently.
7. Competitors calibrate the historical execution bar; they do not select or define a current roadmap.
8. Never copy secrets, provider endpoints, copyrighted fixtures, branding, prompts, or generated demo assets from another project.

## 2. Recommended default stack

### Adopt

| Need | Library | Interface we need | License | Pin observed | Decision |
|---|---|---|---|---|---|
| Numeric arrays | [NumPy](https://github.com/numpy/numpy) 2.4.6 | deterministic QC/null-test math | BSD-3-Clause core; bundled notices apply | `25c89980fcffe59af8ac12b39cf41bd4b07d09ce` | Adopt Python 3.11-compatible release; do not float to 2.5.x on Python 3.11 |
| Signal support | [SciPy](https://github.com/scipy/scipy) 1.17.1 | librosa/scientific signal primitives | BSD-3-Clause plus bundled notices | `e0134f43e13f376a59d9aabaf7c193403131c8f9` | Adopt transitively; keep StageMe DSP narrow |
| Lossless audio I/O | [SoundFile](https://github.com/bastibe/python-soundfile) 0.14.0 | float WAV/FLAC read/write | BSD-3-Clause; libsndfile boundary | `350394191a2af890fc464d0f11a1690e7a4f4c64` | Adopt and record libsndfile build/version |
| Python audio/music analysis | [librosa](https://github.com/librosa/librosa) 0.11.0 | `load`, beat/onset, chroma/pitch, RMS, duration | ISC | `b7e7bf486353821311f68d756e487f65d09cf319` | Adopt for server/spike analysis; synthetic plumbing executed, not StageMe-reproduced |
| Loudness measurement | [pyloudnorm](https://github.com/csteinmetz1/pyloudnorm) 0.2.0 | `Meter(...).integrated_loudness(...)` | MIT | `b8d67bfd3ce5deef872f688fcfa491a0ca69fddd` | Adopt for QC, not automatic taste/mastering |
| Stem separation support | [python-audio-separator](https://github.com/nomadkaraoke/python-audio-separator) 0.44.5 | `Separator`, `load_model`, `separate`; CLI and Docker | MIT wrapper; verify chosen model | `4fe3540c249ff130bd5395c0e9377b3d16970c1a` | Defer until separation/diagnosis is necessary; not arranger |
| Speech transcription | [Whisper](https://github.com/openai/whisper) 20250625 | local transcription | MIT code; record downloaded model | `04f449b8a437f1bbd3dba5c9f826aca972e7709a` | Defer until lyric timing adds value; never assume singing accuracy |
| Word alignment | [WhisperX](https://github.com/m-bain/whisperX) 3.8.6 | word timestamps/alignment | BSD-2-Clause wrapper; alignment models separate | `2cfd7b7c5c7bba144954364db747319b50e8232b` | Defer; do not make core |
| Headless TS video rendering | [Revideo](https://github.com/midrender/revideo) 0.11.0 | `renderVideo()`, Node/headless-browser server rendering | MIT | `b5de67a009a55aa2768a1e178b0446b2479a0b4e` | Intended architecture; one smoke passed but two rerenders failed, so keep fallback active |
| Motion-graphics authoring | [Motion Canvas](https://github.com/motion-canvas/motion-canvas) | generator-based TypeScript scenes and 2D renderer | MIT | `7b91435c301d530351dcf5ebb91dd139c002e405` | Learn scene patterns; choose directly only if export/deployment is simpler than Revideo |
| Python video fallback | [MoviePy](https://github.com/Zulko/moviepy) 2.2.1 | clips, compositing, encoding | MIT | `7ffa4f00376237137a25fe1c777355c37753e9af` | Adopt for Phase-0 fallback where Revideo is unstable |
| Web/player graphics | [PixiJS](https://github.com/pixijs/pixijs) 8.19.0 | accelerated 2D WebGL scenes | MIT | `1d90a20c62433ba68dff78466e06ee372a5a5232` | Optional for interactive preview; not server render |
| Browser capture and revision selection | [wavesurfer.js](https://github.com/katspaugh/wavesurfer.js) 7.12.11 | Record, Regions, Timeline, waveform player | BSD-3-Clause | `98297a9ff4c47fc5099de85d03f6384af954a5b0` | Adopt for capture/player/region UI; it is not an editor |
| Browser feature preview | [Meyda](https://github.com/meyda/meyda) 5.6.3 | JS audio feature extraction | MIT | `ecf256616d43292c82cbf96e60a91b19ca10eb64` | Optional preview only; maintenance activity is limited and server analysis remains authoritative |
| Media encode/inspect | [FFmpeg](https://github.com/FFmpeg/FFmpeg) | ffmpeg/ffprobe; Genblaze `FFmpegCompositor` | LGPL/GPL depends on build | `a757b708ae7d43fdec89545a55cbc11ae2967b19` | Required; pin the deployed binary/config. Local 8.1.1 Homebrew build enables GPL components |

### Evaluate carefully

| Library/tool | Why attractive | Risk/decision |
|---|---|---|
| Essentia | deep audio/music descriptors and Python/C++ | AGPL-3.0 default; avoid unless isolation/compliance is intentionally accepted |
| aubio | onset, pitch, beat tools | GPL-3.0; librosa covers first needs with simpler licensing |
| madmom | strong music signal processing | repository license metadata unclear in audit; verify before reuse |
| p5.js | expressive procedural visuals | LGPL-2.1; usable with compliance but not necessary beside MIT options |
| Demucs | strong source separation | MIT but archived; prefer active audio-separator wrapper and pin chosen model |
| Remotion | mature React video ecosystem | repository uses special licensing/commercial conditions; avoid as default for the affordability/open-source thesis |

## 3. Core generative dependencies

### AnyAccomp

- Repository: <https://github.com/AmphionTeam/AnyAccomp>
- Pin: `82604b5e3107944ad4c49fc64900b86118ae2c62`
- Repository license: MIT.
- Checkpoints: <https://huggingface.co/amphion/anyaccomp>; model card declares CC-BY-4.0. Preserve attribution and recheck the exact downloaded files/model card before deployment.
- Checkpoint revision: `9aa9e62427337bf1df4caa3c4f3e6ad934522e71`; three major files total 2,078,199,136 bytes / 1.935 GiB.
- Interface: `infer_from_folder.py` and `Sing2SongInferencePipeline`.
- Stock environment: Python 3.9, FFmpeg 4.x, Torch/Torchaudio 2.3.1, CUDA 12.1 packages. Keep it outside the Python 3.11+ Genblaze/API process.
- Exact useful implementation pattern:
  - load vocal at 24 kHz mono;
  - encode vocal melody/chroma;
  - generate accompaniment;
  - length-match output;
  - write accompaniment separately;
  - create mixture as generated accompaniment plus original waveform.

Adopt:

- separate accompaniment output;
- explicit source-plus-accompaniment mix;
- deterministic seed/config capture;
- melody-conditioned framing.

Do not copy blindly:

- its direct unbounded waveform addition without StageMe gain/headroom/QC;
- repository-specific paths/config assumptions;
- any quality claim not reproduced on StageMe fixtures.

Current hosted boundary: the official Hugging Face Space is `CONFIG_ERROR` and the model has no hosted inference-provider mapping. The apparent CPU path is unproven. The upstream snapshot example also nests the current `pretrained/...` paths when used literally; the first-call runbook pins the model revision, downloads into the repository root, and verifies every file hash.

### ACE-Step 1.5

- Repository: <https://github.com/ace-step/ACE-Step-1.5>
- Pin: `6d467e4b5081ccb0abf1ec1bf4fdf9051a2d34b0`
- Code/model card observed as MIT; verify weights/third-party components at installation.
- Release `v0.1.8`; package declares 1.5.0. The five major main-plus-base tensor weights total 14,813,190,540 bytes / 13.796 GiB; the complete pinned snapshots total 14,883,895,000 bytes / 13.862 GiB including configs and auxiliary files. The 4,787,825,604-byte base checkpoint exceeds the current autonomous download boundary.
- Stock base environment: Python 3.11–3.12, Torch 2.10/CUDA 12.8 on Linux x86-64.
- Useful interfaces:
  - CLI and Python `GenerationParams`/`generate_music`;
  - HTTP `POST /release_task`, `POST /query_result`, `GET /v1/audio`;
  - `task_type="lego"` for named instrument track;
  - `task_type="complete"` for partial-track completion;
  - `task_type="repaint"` for bounded time editing.

Adopt:

- task-specific API rather than vague “Vocal2BGM” marketing;
- separate named-layer experiments through `lego`;
- asynchronous job semantics;
- explicit seed/config/model capture;
- `repaint` only after preservation is reproduced.

Avoid:

- broad UI surface;
- voice-cloning detours;
- presenting base-model 50-step behavior as turbo latency;
- claiming full source preservation from documentation alone.

Current API risks: jobs live in memory; unknown IDs look pending; there is no generation cancellation; the request timeout can leave CUDA work active; `complete` source validation/duration and `repaint` crossfade/splice behavior need StageMe enforcement. The official Space serves turbo/XL-turbo, not the required base `lego`/`complete` tasks.

### Wan 2.2 S2V on Replicate

- Official endpoint: <https://replicate.com/wan-video/wan-2.2-s2v>
- Inputs: reference image, audio, prompt.
- Current exact public version observed: `09607e6e761d2f015b0d740f938ec59199f54aa623384465a5054b230405acf4`; schema requires all three inputs and returns one URI.
- Price observed: $0.02 per output second on 2026-07-27.
- Role: optional replaceable 3–5 second hero interval after accepted audio and human approval.

Adopt:

- audio-bound reference-image shot as an optional 3–5 second reveal enhancement;
- per-output-second budget calculation;
- Genblaze Replicate lifecycle where supported.

Avoid:

- required success;
- user-selfie dependence;
- persistent avatar product shape;
- silent retries or candidate fishing;
- third-party faces.

The current generic API page exposes a different version and an `interpolate` field absent from the exact latest-version schema. Revalidate immediately before payment, record the requested and returned versions, and copy success to B2 before Replicate's short output TTL expires.

## 4. Audio support patterns

### librosa

Use for deterministic analysis, not as proof that a performance controlled a model.

Candidate functions:

```python
librosa.load(..., sr=None, mono=False)
librosa.get_duration(...)
librosa.feature.rms(...)
librosa.onset.onset_detect(...)
librosa.onset.onset_strength(...)
librosa.beat.beat_track(...)
librosa.feature.chroma_cqt(...) or chroma_stft(...)
librosa.pyin(...)  # evaluate for rough monophonic pitch; may fail on noisy singing
```

Record versions and parameters. Do not present estimated key/BPM/pitch as human truth.

### pyloudnorm

Use to measure integrated loudness:

```python
meter = pyln.Meter(sample_rate)
lufs = meter.integrated_loudness(audio)
```

Use measurement to inform QC. Do not force every short clip to a broadcast target without listening; very short clips and nonstationary music require care.

### python-audio-separator

Official interfaces observed:

```python
from audio_separator.separator import Separator
separator = Separator(...)
separator.load_model(model_filename="...")
output_files = separator.separate("audio.wav")
```

CLI:

```bash
audio-separator input.wav --model_filename <model>
audio-separator --list_models --list_format=json
```

Useful for:

- diagnosing whether a full-mix candidate contains a recoverable source;
- creating stems from licensed music when explicitly needed;
- fallback separation, not composition.

Important:

- wrapper is MIT;
- chosen UVR/Demucs model terms and attribution must be recorded separately;
- auto-downloaded models must be pinned/cached, not allowed to drift during judging.

### Whisper/WhisperX

Use only when lyric/transcript timing improves the stage. Singing transcription can be unreliable. The source recording and user-entered correction remain authoritative.

### FFmpeg/ffprobe

Use for:

- media probing;
- deterministic decoding/resampling;
- trim/fade/gain/mix;
- loudness/peak support measurements where appropriate;
- image/video/audio mux;
- codec/container validation;
- low-data exports.

Pass subprocess arguments as arrays. Never interpolate user text into a shell command. Record exact build configuration and license obligations.

## 5. Visual stack patterns

### Revideo — default deterministic renderer architecture

Observed README claims:

- TypeScript scene description;
- headless `renderVideo()` API;
- CLI-exposed render endpoint;
- Node/headless-browser deployment, including Cloud Run example;
- parallel rendering;
- media/audio components and audio export;
- MIT license.

Current measured state on 2026-07-27:

- Node requirement `>=22.12.0`; Puppeteer 25.3.0 / Chrome 150.0.7871.24;
- canonical build passed with `DISABLE_TELEMETRY=true`;
- one bundled 7.433-second 1080-square render passed in 11.42 seconds wall with about 446 MiB maximum RSS;
- two immediate rerenders failed, including on Node 22.12, with `Navigating frame was detached`, matching open issue #343;
- Cloud Run remains advertised only because the linked official example is missing.

StageMe use:

```text
StageRenderSpec
→ Revideo scene
→ audio-derived lights/shapes/type/camera
→ MP4
→ Genblaze FFmpegCompositor or ffmpeg final mux/QC
```

Pin the Revideo package, Chromium/browser build, fonts, and container digest together. A browser upgrade can alter layout or render behavior even when the scene spec is unchanged.

Before adoption, prototype:

- 15-second 720p render latency;
- custom font packaging;
- audio sync and frame determinism;
- container/headless-browser size;
- server concurrency/memory;
- telemetry opt-out/data boundary.

Require at least three consecutive cold and warm 15-second 720p renders with local 48 kHz audio/fonts, within-one-frame A/V sync, decoded frame/PCM repeat checks, one worker, measured RSS/temp disk, pinned container, and deployment cleanup. Until then, direct FFmpeg/MoviePy is the Phase-0 fallback.

### Motion Canvas

Use its generator-based scenes and 2D primitives as a design/implementation reference. It is strong for authored motion graphics; validate headless production export before choosing it over Revideo.

### wavesurfer.js

Use:

- Record plugin for microphone capture;
- waveform playback;
- Regions for bounded revision selection;
- Timeline for time context.

Do not use it for destructive audio editing. It fetches browser audio and needs correct CORS. Precomputed peaks may be preferable for large files, though StageMe clips are short.

### PixiJS/Meyda

Optional interactive reveal:

- PixiJS draws responsive stage graphics;
- Meyda can derive browser-side preview features.

The authoritative saved render and analysis remain server-side.

### MoviePy

Useful Phase 0 fallback because the media spike is Python-first. If it cannot meet visual polish/render time, keep it for tests and use Revideo for the product renderer.

## 6. Product/reference projects

### ONEFIELD

- Repository: <https://github.com/TierraLinn/onefield-by-ariyus-one>
- Pin observed: `f88d7103172824dc33d6f49c899c46fff19ed0db`
- License metadata: none recognized.
- State observed: microphone/spectrum/Web Audio/consent/receipt scaffolding; final provider pipeline described as representative without configured API. A focused audit build failed because `/src/main.tsx` was missing, so the inspected pin is not a runnable product baseline.

Learn:

- make consent visible;
- show the human signal immediately;
- store a compact receipt/provenance artifact;
- use browser audio for instant response while heavy processing runs.

Avoid:

- broad global-instrument manifesto;
- representative pipeline presented as complete;
- product copy, visual identity, or code reuse without license.

### Murmur

- Repository: <https://github.com/p-to-q/murmur>
- Pin observed: `c49882ea42cfba9c94f790c2569eefe355e40503`
- License metadata: none recognized.
- State observed: its useful musical result is local browser synthesis rather than a reproduced source-conditioned generative accompaniment pipeline.

Learn:

- consumer-simple record-to-song-card flow;
- clear artifact packaging;
- mapping unconstrained language into a small, clamped musical state;
- bounded-control and song-card interaction concepts as the competitive baseline.

Avoid:

- copying code/assets/UI;
- claiming hum-to-song itself as differentiation;
- building its wider feature list reactively.

### InstantBandAI

- Repository: <https://github.com/jeremystiffler/instantbandai>
- Pin observed: `51f4791acd1ad6b29fbd074c86cf83b20d231b22`
- License metadata: none recognized.
- State observed: closest functional calibration for rough-demo-to-band generation, but the source conditions a newly generated full mix rather than remaining literally present. Webhook authorization, persistence, and migration approaches are not StageMe-quality production references.

Learn:

- plain-language user problem;
- arrangement terminology;
- rough demo as an understandable input.
- separate project and generation records.

Avoid:

- treating roadmap providers as implementation proof;
- describing conditioning as retained performance;
- copying its webhook, authorization, persistence, or migration patterns;
- code reuse without license.

### Vanta

- Repository: <https://github.com/itsjwill/vanta>
- Pin observed: `350b053ee18fb856a87516cfbfd1ad2295c26a73`
- License metadata: no recognized SPDX license in repository metadata.
- State observed: more useful as a catalog of wrappers and design sketches than as proof of the broad integrated engine claimed by its README.

Learn:

- modular media engine boundaries;
- provider adapters;
- timeline/compositor patterns;
- local-first deployment lessons.

Avoid:

- copying code until exact license is verified;
- broad all-in-one video editor scope;
- avatar/voice-cloning product drift;
- Remotion dependency without license review.

### Backblaze Genblaze multi-provider sample

- Repository: <https://github.com/backblaze-labs/genblaze-gen-media-multi-provider-sample>
- Pin observed: `2e31577b7a9d5a7b0309d814f2d0282088b33fe8`
- License: MIT.
- Execution evidence: independently reproduced at the pinned commit on 2026-07-27. `corepack pnpm@10.32.1 install --frozen-lockfile` succeeded; direct workspace `next build` compiled Next.js 16.1.6 and generated 7/7 static pages; direct `tsc --noEmit` exited 0.
- Toolchain warning: the root `build` script shells out to ambient `pnpm`. In the audit environment that resolved to pnpm 11.17.0, which requires Node >=22.13 and failed under Node 20.20.2 on `node:sqlite`. Pin `packageManager`/Corepack or call the intended pnpm version explicitly.

Learn/adopt under license and attribution:

- real Genblaze pipeline construction;
- provider configuration;
- progress/event handling;
- B2 sink and manifest patterns;
- final media composition;
- error/fallback structure.

Avoid:

- reskinning its prompt-to-storyboard product;
- copying its broad multimodal flow as StageMe's user experience;
- leaving Genblaze sample defaults unverified against installed versions.

### Backblaze Genblaze GMI Cloud pipeline

- Repository: <https://github.com/backblaze-labs/genblaze-gmicloud-pipeline>
- Pin observed: `355a539ecf99f8d6fcfc5ba40cc5f9a95523100b`
- License: MIT.

Learn:

- provider setup and official integration conventions;
- pipeline/provenance patterns.

Do not make GMI access a core dependency without entitlement verification.

## 7. ACE ecosystem references

### ACE-Step Studio

- <https://github.com/timoncool/ACE-Step-Studio>
- Pin: `ebe16f46b51a32b25e36a62bbbe10dfaf7d5c747`
- MIT.

Learn:

- local model lifecycle;
- portable packaging;
- job/history/user-control patterns;
- current ACE setup pitfalls.

Avoid copying its full-song workstation scope.

### AceForge

- <https://github.com/audiohacking/AceForge>
- Pin: `6103f5df9d9f6e7e0a80496194c841595bfd1add`
- Apache-2.0.

Learn:

- local-first music workstation architecture;
- ACE/Demucs/audio integration boundaries;
- model management.

Avoid voice-cloning and workstation expansion.

### ACE-Step UI

- <https://github.com/fspecii/ace-step-ui>
- Pin: `a1fdf91829ec6f7b98844f80e323529cd155dbf2`
- No recognized license metadata.

Inspect setup behavior and issue patterns only. Do not copy code or assets.

### Synesthesia AI Video Director

- <https://github.com/RowanUnderwood/Synesthesia-AI-Video-Director>
- Pin: `ccf9bb843dfbfe40b15934d01c21dfa69bfdcb8a`
- MIT.

Learn:

- audio feature to storyboard boundaries;
- stems/lyrics ingestion;
- batch scene planning;
- local render orchestration.

Avoid building a generic music-video director. StageMe's stage is subordinate to the retained-performance transformation.

## 8. Adopt/evaluate/reject summary

### Adopt for the first build

- AnyAccomp direct spike;
- ACE-Step `lego`, then `complete`, then gated `repaint`;
- librosa;
- pyloudnorm;
- ffmpeg/ffprobe with exact build review;
- wavesurfer.js;
- Genblaze custom provider contract;
- B2 immutable/versioned object design;
- Revideo + pinned Chromium as the default renderer, with MoviePy fallback.

### Evaluate only if needed

- audio-separator;
- Whisper/WhisperX;
- PixiJS/Meyda interactive preview;
- Motion Canvas instead of Revideo;
- Wan S2V optional hero shot;
- ACE ecosystem packaging patterns;
- Synesthesia storyboard patterns.

### Reject/defer from MVP

- RVC/Seed-VC target-voice conversion;
- DiffSinger structured singing synthesis;
- HeartMuLa as source-conditioned arranger while reference audio remains TODO;
- AudioCraft released non-commercial weights as commercial foundation;
- full local 14B video path;
- avatar/talking-head stacks;
- Remotion as default without license decision;
- AGPL/GPL audio-analysis dependencies when permissive substitutes suffice;
- competitor code without an explicit license.

## 9. Required dependency ledger fields

Before merging a dependency, record:

```text
name
repository and exact commit/release
package and exact version
code license
model/weight license
sample/asset/font licenses
purpose in StageMe
interface used
runtime/hardware
network/data boundary
known vulnerabilities or maintenance concern
attribution location
fallback/removal plan
```

The lockfile and container digest become execution evidence; this research pin is not a substitute for a build lock.
