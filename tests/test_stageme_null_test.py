from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

try:
    import numpy as np
    import soundfile as sf
except ModuleNotFoundError:  # The repository validator does not install QC extras.
    np = None
    sf = None


@unittest.skipIf(np is None or sf is None, "StageMe QC dependencies are not installed")
class StageMeNullTestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        script = (
            Path(__file__).resolve().parents[1] / "scripts" / "stageme_null_test.py"
        )
        spec = importlib.util.spec_from_file_location("stageme_null_test", script)
        assert spec is not None and spec.loader is not None
        cls.module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.module
        spec.loader.exec_module(cls.module)

    def test_exact_float_mix_passes_and_wrong_gain_fails(self) -> None:
        assert np is not None and sf is not None
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample_rate = 48_000
            time = np.arange(sample_rate, dtype=np.float64) / sample_rate
            source = (0.05 * np.sin(2 * np.pi * 220 * time)).astype(np.float32)
            accompaniment = (0.03 * np.sin(2 * np.pi * 110 * time)).astype(np.float32)
            mixture = (source + accompaniment).astype(np.float32)
            paths = {
                "source": root / "source.wav",
                "accompaniment": root / "accompaniment.wav",
                "mixture": root / "mixture.wav",
            }
            sf.write(paths["source"], source, sample_rate, subtype="FLOAT")
            sf.write(
                paths["accompaniment"], accompaniment, sample_rate, subtype="FLOAT"
            )
            sf.write(paths["mixture"], mixture, sample_rate, subtype="FLOAT")

            passed = self.module.verify(
                paths["source"],
                paths["accompaniment"],
                paths["mixture"],
                1.0,
                1.0,
                1e-7,
                1e-8,
            )
            failed = self.module.verify(
                paths["source"],
                paths["accompaniment"],
                paths["mixture"],
                1.0,
                0.9,
                1e-7,
                1e-8,
            )

        self.assertTrue(passed["passed"])
        self.assertFalse(failed["passed"])

    def test_zero_or_tiny_source_gain_cannot_certify_absent_source(self) -> None:
        assert np is not None and sf is not None
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = np.full(100, 0.25, dtype=np.float32)
            accompaniment = np.full(100, 0.1, dtype=np.float32)
            paths = {
                "source": root / "source.wav",
                "accompaniment": root / "accompaniment.wav",
                "mixture": root / "mixture.wav",
            }
            sf.write(paths["source"], source, 24_000, subtype="FLOAT")
            sf.write(paths["accompaniment"], accompaniment, 24_000, subtype="FLOAT")
            sf.write(paths["mixture"], accompaniment, 24_000, subtype="FLOAT")

            for source_gain in (0.0, 0.01):
                with (
                    self.subTest(source_gain=source_gain),
                    self.assertRaisesRegex(ValueError, "source gain"),
                ):
                    self.module.verify(
                        paths["source"],
                        paths["accompaniment"],
                        paths["mixture"],
                        source_gain,
                        1.0,
                        1e-7,
                        1e-8,
                    )

    def test_oversized_tolerance_is_rejected(self) -> None:
        assert np is not None and sf is not None
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "audio.wav"
            sf.write(
                path, np.ones(100, dtype=np.float32) * 0.1, 24_000, subtype="FLOAT"
            )
            with self.assertRaisesRegex(ValueError, "maximum-error tolerance"):
                self.module.verify(path, path, path, 1.0, 1.0, 1.0, 1e-8)

    def test_rate_or_shape_mismatch_is_rejected(self) -> None:
        assert np is not None and sf is not None
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.wav"
            accompaniment = root / "accompaniment.wav"
            mixture = root / "mixture.wav"
            sf.write(
                source, np.ones(100, dtype=np.float32) * 0.1, 24_000, subtype="FLOAT"
            )
            sf.write(
                accompaniment,
                np.ones(100, dtype=np.float32) * 0.1,
                48_000,
                subtype="FLOAT",
            )
            sf.write(
                mixture, np.ones(100, dtype=np.float32) * 0.2, 24_000, subtype="FLOAT"
            )
            with self.assertRaisesRegex(ValueError, "sample rates differ"):
                self.module.verify(source, accompaniment, mixture, 1.0, 1.0, 1e-7, 1e-8)

    def test_exact_zero_residual_is_strict_json(self) -> None:
        assert np is not None and sf is not None
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.wav"
            accompaniment = root / "accompaniment.wav"
            mixture = root / "mixture.wav"
            signal = np.linspace(-0.1, 0.1, 100, dtype=np.float32)
            sf.write(source, signal, 24_000, subtype="FLOAT")
            sf.write(
                accompaniment, np.zeros(100, dtype=np.float32), 24_000, subtype="FLOAT"
            )
            sf.write(mixture, signal, 24_000, subtype="FLOAT")
            result = self.module.verify(
                source, accompaniment, mixture, 1.0, 1.0, 1e-7, 1e-8
            )
            rendered = json.dumps(result, allow_nan=False)
            self.assertTrue(result["passed"])
            self.assertIn('"relative_error_db": null', rendered)


if __name__ == "__main__":
    unittest.main()
