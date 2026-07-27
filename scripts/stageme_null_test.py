#!/usr/bin/env python3
"""Verify literal source retention in a lossless StageMe premaster.

This utility reads only local lossless audio, does not upload anything, and
compares `mixture - accompaniment_gain * accompaniment` with
`source_gain * source` sample for sample. Run it before mastering, limiting, or
lossy encoding.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence
from pathlib import Path

import numpy as np
import soundfile as sf

MIN_SOURCE_GAIN = 0.1
MAX_SOURCE_GAIN = 1.0
MAX_ACCOMPANIMENT_GAIN = 1.0
MAX_ALLOWED_ABS_TOLERANCE = 1e-5
MAX_ALLOWED_RMS_TOLERANCE = 1e-6


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load(path: Path) -> tuple[np.ndarray, int]:
    audio, sample_rate = sf.read(path, dtype="float64", always_2d=True)
    if audio.size == 0:
        raise ValueError("audio is empty")
    if not np.isfinite(audio).all():
        raise ValueError("audio contains a non-finite sample")
    return audio, int(sample_rate)


def verify(
    source_path: Path,
    accompaniment_path: Path,
    mixture_path: Path,
    source_gain: float,
    accompaniment_gain: float,
    max_error_tolerance: float,
    rms_error_tolerance: float,
) -> dict[str, object]:
    parameters = np.asarray(
        [
            source_gain,
            accompaniment_gain,
            max_error_tolerance,
            rms_error_tolerance,
        ],
        dtype=np.float64,
    )
    if not np.isfinite(parameters).all():
        raise ValueError("gains and tolerances must be finite")
    if not MIN_SOURCE_GAIN <= source_gain <= MAX_SOURCE_GAIN:
        raise ValueError(
            f"source gain must be between {MIN_SOURCE_GAIN} and {MAX_SOURCE_GAIN}"
        )
    if not 0.0 <= accompaniment_gain <= MAX_ACCOMPANIMENT_GAIN:
        raise ValueError(
            f"accompaniment gain must be between 0 and {MAX_ACCOMPANIMENT_GAIN}"
        )
    if not 0.0 <= max_error_tolerance <= MAX_ALLOWED_ABS_TOLERANCE:
        raise ValueError(
            f"maximum-error tolerance must be between 0 and {MAX_ALLOWED_ABS_TOLERANCE}"
        )
    if not 0.0 <= rms_error_tolerance <= MAX_ALLOWED_RMS_TOLERANCE:
        raise ValueError(
            f"RMS-error tolerance must be between 0 and {MAX_ALLOWED_RMS_TOLERANCE}"
        )

    source, source_rate = _load(source_path)
    accompaniment, accompaniment_rate = _load(accompaniment_path)
    mixture, mixture_rate = _load(mixture_path)

    rates = {source_rate, accompaniment_rate, mixture_rate}
    shapes = {source.shape, accompaniment.shape, mixture.shape}
    if len(rates) != 1:
        raise ValueError("sample rates differ; canonical alignment is not proven")
    if len(shapes) != 1:
        raise ValueError(
            "sample counts or channel counts differ; canonical alignment is not proven"
        )

    expected = source_gain * source
    residual = mixture - accompaniment_gain * accompaniment
    error = residual - expected
    max_abs_error = float(np.max(np.abs(error)))
    rms_error = float(np.sqrt(np.mean(np.square(error))))
    expected_rms = float(np.sqrt(np.mean(np.square(expected))))
    relative_error_db = (
        float(20.0 * np.log10(rms_error / expected_rms))
        if rms_error > 0.0 and expected_rms > 0.0
        else None
    )
    flat_expected = expected.reshape(-1)
    flat_residual = residual.reshape(-1)
    if np.std(flat_expected) == 0.0 or np.std(flat_residual) == 0.0:
        correlation = None
    else:
        measured_correlation = float(np.corrcoef(flat_expected, flat_residual)[0, 1])
        correlation = (
            measured_correlation if np.isfinite(measured_correlation) else None
        )
    passed = max_abs_error <= max_error_tolerance and rms_error <= rms_error_tolerance

    return {
        "schema_version": "1",
        "passed": passed,
        "sample_rate": source_rate,
        "frames": int(source.shape[0]),
        "channels": int(source.shape[1]),
        "source_gain": source_gain,
        "accompaniment_gain": accompaniment_gain,
        "max_abs_error": max_abs_error,
        "rms_error": rms_error,
        "relative_error_db": relative_error_db,
        "correlation": correlation,
        "tolerances": {
            "max_abs_error": max_error_tolerance,
            "rms_error": rms_error_tolerance,
        },
        "sha256": {
            "source": _sha256(source_path),
            "accompaniment": _sha256(accompaniment_path),
            "mixture": _sha256(mixture_path),
        },
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--accompaniment", required=True, type=Path)
    parser.add_argument("--mixture", required=True, type=Path)
    parser.add_argument("--source-gain", type=float, default=1.0)
    parser.add_argument("--accompaniment-gain", type=float, default=1.0)
    parser.add_argument("--max-error-tolerance", type=float, default=1e-7)
    parser.add_argument("--rms-error-tolerance", type=float, default=1e-8)
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = verify(
            args.source,
            args.accompaniment,
            args.mixture,
            args.source_gain,
            args.accompaniment_gain,
            args.max_error_tolerance,
            args.rms_error_tolerance,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        result = {
            "schema_version": "1",
            "passed": False,
            "error": str(exc),
        }

    if args.json_output:
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    elif result.get("passed"):
        print("PASS: the premaster literally retains the configured source layer")
        print(f"- max absolute error: {result['max_abs_error']:.12g}")
        print(f"- RMS error: {result['rms_error']:.12g}")
        print(f"- correlation: {result['correlation']}")
    else:
        print("FAIL: literal source retention was not proven")
        print(f"- {result.get('error', 'error exceeded the configured tolerance')}")
    return 0 if result.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
