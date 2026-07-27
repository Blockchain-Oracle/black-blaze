# Verification Report

**Latest verification date:** 2026-07-27 UTC

This is a local/read-only verification snapshot. It contains no provider credential, human audio, paid model output, or B2 write.

## Context integrity

The literal requested command returned exit 127 because this host has no `python` alias:

```text
zsh: command not found: python
```

The same validator was then executed with the available `python3` interpreter:

```bash
python3 scripts/validate_context.py
```

Result after the StageMe pre-call edits:

```text
PASS: context integrity checks succeeded
- markdown files checked: 52
- JSON files checked: 5
- repository ledger entries checked: 32
- required StageMe files checked: 21
```

`git diff --check` also exited 0.

## External links

Command:

```bash
python3 scripts/check_external_links.py --timeout 30
```

Final result:

```text
Checked 224 URLs: 224 reachable, 0 failed
```

The first pass included unrelated untracked `.agents/` examples and failed placeholder URLs; the checker now excludes local skill/cache/research directories as its docstring intended. A later pass saw transient DNS/TLS timeouts. Direct official retrieval succeeded, and the checker now retries a failed HEAD once with a bounded GET before reporting a failure.

Reachability does not prove that mutable content, pricing, entitlement, or licenses remain unchanged.

## StageMe preflight

Commands:

```bash
python3 scripts/stageme_preflight.py --phase precall
python3 scripts/stageme_preflight.py --phase precall --json
python3 scripts/stageme_preflight.py --phase anyaccomp-local --json
```

Results:

- `precall`: exit 0, overall `warning`; 13 passes, 3 warnings, and 26 `not-yet-required` checks. All required repository artifacts are present; no fixture, consent, credentials, checkpoint, work root, model worker, or hard budget plan is yet required.
- `anyaccomp-local`: exit 2, overall `blocker` as designed; 14 passes, 2 warnings, 21 blockers, and 10 `not-yet-required` checks. The current host has Python 3.14, no stock Python 3.9 worker, no NVIDIA GPU, no QC packages in system Python, no fixture/consent/checkpoints/work root, and no provider/region/project/spend approval or provider-native hard budget plan.
- Both modes state that no provider/B2 call, media upload, or secret-value print occurred.

The local machine inventory was Node 25.9.0, pnpm 10.33.0, npm 11.12.1, FFmpeg/ffprobe 8.1.1, Apple M1 Pro Metal, 16 GiB RAM, and 131.6 GiB free at final preflight. Node 25 and Python 3.14 are inventory only, not the pinned Revideo or StageMe control/model environments.

## Script tests and formatting

Commands:

```bash
python3 -m py_compile scripts/stageme_preflight.py scripts/stageme_null_test.py scripts/validate_context.py scripts/check_external_links.py
python3 -m unittest -v tests/test_stageme_preflight.py tests/test_stageme_null_test.py
.research-venv/stageme-qc/bin/python -m unittest -v tests/test_stageme_preflight.py tests/test_stageme_null_test.py
uvx --from ruff ruff check scripts/stageme_preflight.py scripts/stageme_null_test.py scripts/validate_context.py scripts/check_external_links.py tests
uvx --from ruff ruff format --check scripts/stageme_preflight.py scripts/stageme_null_test.py scripts/validate_context.py scripts/check_external_links.py tests
```

Results:

- system Python: 24 passed, 5 optional null-test cases skipped because QC dependencies are isolated;
- pinned QC environment: 29 passed;
- Ruff 0.16.0 lint/format: passed after formatting;
- the literal requested `python -m py_compile ...` command returned exit 127 because `python` is absent; the equivalent `python3 -m py_compile ...` command passed for all four scripts.

All 26 `bash` code fences and 15 embedded Python programs in the first-call runbook passed in-memory syntax checks. This checks grammar only, not a paid worker execution.

The embedded deterministic media-QC program was also executed against a generated 10-second, 24 kHz synthetic source/accompaniment/premaster set. The valid set passed and reported an accompaniment-to-source RMS ratio of `-2.49877 dB`; a silent accompaniment fixture exited nonzero with three QC failures. The provisional-manifest program populated a synthetic evidence layout successfully. The finalization fence was exercised for accepted and rejected reviews: both paths persisted a synthetic settled charge/deletion state and wrote the final evidence hash, while rejection exited nonzero. A mocked Pod-cleanup fence accepted a successful authenticated listing with the exact Pod absent and rejected a generic CLI/auth failure. These are control-flow tests only; no provider deletion was executed or verified.

## Synthetic F0 retention proof

The pinned QC environment was Python 3.12.13 with NumPy 2.4.6, SciPy 1.17.1, SoundFile 0.14.0, librosa 0.11.0, and pyloudnorm 0.2.0.

Command shape:

```bash
.research-venv/stageme-qc/bin/python scripts/stageme_null_test.py \
  --source .tmp/stageme-f0/source-synthetic.wav \
  --accompaniment .tmp/stageme-f0/accompaniment-synthetic.wav \
  --mixture .tmp/stageme-f0/mixture-synthetic.wav \
  --json
```

Observed correct-mix result:

```text
frames: 480000
sample_rate: 48000
max_abs_error: 9.313225746154785e-10
rms_error: 2.9139299742360333e-10
relative_error_db: -149.63637682235782
correlation: 0.9999999999999786
passed: true
```

An intentional `--source-gain 0.5` mismatch returned exit 2 and `passed: false` with max error `0.006248474586755037`. A zero source gain was rejected before comparison with exit 2. This reproduces null-test plumbing only; it is not AnyAccomp or human-media evidence.

## Revideo and Genblaze execution

- Revideo current source built all 10 selected projects. One bundled template rendered successfully; two immediate rerenders failed with `Navigating frame was detached`. Exact runtime/output measurements and source pins are in `../06-technical/REPOSITORY_AUDITS.md`.
- A current selected Genblaze source suite returned 210 passed, 3 skipped. A separate clean-room run returned 388 selected core tests passed and 26 selected S3 tests passed. These tests prove selected contract behavior, not StageMe provider/media execution.
- The official multi-provider sample passed its pnpm 10.32.1 frozen install, Next 16.1.6 build, and TypeScript check. It remains an architecture reference only.

## Repository-source provenance

Research clones remain ignored under `.research-clones/`; exact commits, licenses, purposes, dates, and findings are recorded in:

- `../06-technical/REPOSITORY_AUDITS.md`
- `repositories.json`

No third-party source was vendored.

## GitHub boundary

- Remote: `https://github.com/Blockchain-Oracle/black-blaze`
- Visibility observed: private
- Target branch for this explicitly authorized task: `main`
- Starting remote commit: `a8df5a9b46e2f427ae4192e6e0d2d8d9eac7399d`

The final commit/push SHA is reported after delivery; no force push or visibility change is permitted.

## Remaining limitations

- No authorized F1, AnyAccomp/ACE output, measured model latency/VRAM, or media-quality result exists.
- No real B2 canary, GPU account entitlement, payment, credentialed Replicate routing check, deployment, or Wan call exists.
- Eligibility and prize receipt remain subject to Sponsor/Administrator verification and law.
- All live pricing, provider inventory, schemas, packages, repositories, event pages, and terms require revalidation at the relevant action boundary.
