# StageMe F1 Recording Checklist

> **Historical, unselected procedure:** decision D-014 reopened product selection on 2026-07-28.
> Do not request, process, or upload a fixture from this checklist unless a later decision explicitly
> selects StageMe and revalidates the consent/provider boundary.

If StageMe is reselected, use this after the pre-call report names the proposed processing location. The
checklist takes under five minutes and produces the rough-singing recording that
will be bound to consent by its exact local SHA-256 before it leaves the device.
It does not authorize humming, beatboxing, voice cloning, public release, or
model training.

## Before recording

- Use your own voice and a phrase you wrote or are authorized to perform.
- Record **one voice only** with no backing track, television, radio, sampled
  beat, or another person audible.
- Choose a quiet ordinary room. Turn off fans and move away from traffic,
  hard-wall echoes, and notification sounds where practical.
- Use the phone's built-in microphone, about 15–25 cm from your mouth. Avoid
  Bluetooth microphones and speakerphone processing for the first fixture.
- If you need a pitch reference, listen first, then stop it before recording.

## Record

1. Open the phone's normal voice recorder.
2. Leave about half a second of room tone.
3. Sing one natural rough phrase for a total recording length of **8–15
   seconds**. Do not try to sound studio-perfect.
4. Keep a steady distance and avoid shouting directly into the microphone.
5. Leave about half a second of room tone, then stop.
6. Play it once. Rerecord only if it is silent, obviously clipped/distorted,
   interrupted, or contains somebody else's audio.

## Do not preprocess

Do not apply pitch correction, timing correction, denoising, reverb, stem
separation, vocal enhancement, normalization, or a backing track. Do not
convert the recording merely to make it look “professional.” StageMe must keep
the real source and record every deterministic conversion itself.

## Accepted delivery formats

WAV, FLAC, MP3, M4A/AAC, WebM, or Ogg/Opus are accepted at ingest. Keep the
phone's original file. The preflight rejects corrupt files, files outside
8–15 seconds, files over 25 MiB, and files without an audio stream before any
model call.

## Consent checkpoint

After recording—but before the file leaves the performer's device—compute its
local SHA-256, then complete
[`templates/STAGEME_CONSENT.example.json`](../../templates/STAGEME_CONSENT.example.json)
with:

- ownership/authorization attestation;
- one new private `project_id` that matches the preflight environment and every
  later manifest/version record;
- exact allowed purposes: analysis, accompaniment generation, deterministic
  mixing/QC, and review;
- named GPU host or provider and processing region when known;
- `source_original_sha256` equal to the exact phone/original file;
- exact AnyAccomp code commit and checkpoint revision;
- `training_reuse: false`;
- no third-party or celebrity voice;
- worker deletion immediately after verified download, with a 24-hour hard
  maximum for temporary worker copies;
- a provider-native hard termination deadline whose maximum compute charge plus
  storage reserve is no greater than the approved cap;
- proposed seven-day maximum for the user-controlled experiment bundle unless
  the performer chooses a shorter period;
- deletion contact/path and acceptance timestamp.

After deterministic decode/downmix/resample, StageMe creates a separate
execution record containing `source_canonical_sha256`, the FFmpeg binary hash
and version, and the exact canonicalization command. Those fields bind derived
transfer bytes; they do not expand the already accepted purpose.

Do not upload the fixture to B2, a model provider, or a GPU worker until those
fields are complete. The source and every voice-bearing derivative remain
private and must never enter Git.

## What the first fixture proves

F1 can promote AnyAccomp from **implemented** to **reproduced** only if the run
stores separate accompaniment, a deterministic mixture containing the original
source, hashes, exact configuration, null-test evidence, latency/memory/cost,
and human review. One good clip does not make the capability product-proven.
