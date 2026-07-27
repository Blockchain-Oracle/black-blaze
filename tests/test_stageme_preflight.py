from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
import wave
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "stageme_preflight.py"
SPEC = importlib.util.spec_from_file_location("stageme_preflight", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
stageme_preflight = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = stageme_preflight
SPEC.loader.exec_module(stageme_preflight)


class StageMePreflightTests(unittest.TestCase):
    def test_version_parser(self) -> None:
        self.assertEqual(
            stageme_preflight._version_tuple("ffmpeg version 8.1.1"), (8, 1, 1)
        )
        self.assertEqual(stageme_preflight._version_tuple("unknown"), ())

    def test_missing_b2_environment_is_blocker(self) -> None:
        checks = stageme_preflight.environment_checks("b2-canary", {})
        b2_checks = [check for check in checks if check.check_id.startswith("env.b2_")]
        self.assertTrue(b2_checks)
        self.assertTrue(
            all(check.status == stageme_preflight.BLOCKER for check in b2_checks)
        )

    def test_b2_prefix_is_required_for_canary(self) -> None:
        checks = stageme_preflight.environment_checks(
            "b2-canary",
            {
                "B2_KEY_ID": "present",
                "B2_APP_KEY": "present",
                "B2_BUCKET": "present",
                "B2_REGION": "present",
            },
        )
        prefix = next(check for check in checks if check.check_id == "env.b2_prefix")
        self.assertEqual(prefix.status, stageme_preflight.BLOCKER)

        invalid = stageme_preflight.environment_checks(
            "b2-canary",
            {
                "B2_KEY_ID": "present",
                "B2_APP_KEY": "present",
                "B2_BUCKET": "present",
                "B2_REGION": "present",
                "B2_PREFIX": "/",
            },
        )
        invalid_prefix = next(
            check for check in invalid if check.check_id == "env.b2_prefix"
        )
        self.assertEqual(invalid_prefix.status, stageme_preflight.BLOCKER)

    def test_precall_environment_is_not_yet_required(self) -> None:
        checks = stageme_preflight.environment_checks("precall", {})
        self.assertTrue(checks)
        self.assertTrue(
            all(check.status == stageme_preflight.NOT_YET_REQUIRED for check in checks)
        )

    def test_environment_values_are_never_serialized(self) -> None:
        secret = "do-not-print-this-secret-value"
        checks = stageme_preflight.environment_checks(
            "b2-canary",
            {
                "B2_KEY_ID": secret,
                "B2_APP_KEY": secret,
                "B2_BUCKET": secret,
                "B2_REGION": secret,
            },
        )
        rendered = json.dumps([stageme_preflight.asdict(check) for check in checks])
        self.assertNotIn(secret, rendered)

    def test_spend_cap_must_be_finite_and_positive(self) -> None:
        for value in ("no", "0", "-1", "inf", "nan"):
            with self.subTest(value=value):
                checks = stageme_preflight.environment_checks(
                    "anyaccomp-local",
                    {
                        "STAGEME_GPU_PROVIDER": "provider",
                        "STAGEME_GPU_REGION": "region",
                        "STAGEME_SPEND_CAP_USD": value,
                    },
                )
                spend = next(
                    check
                    for check in checks
                    if check.check_id == "env.stageme_spend_cap_usd"
                )
                self.assertEqual(spend.status, stageme_preflight.BLOCKER)

    def test_overall_status_prioritizes_blockers(self) -> None:
        checks = [
            stageme_preflight.Check("a", stageme_preflight.WARNING, "warning"),
            stageme_preflight.Check("b", stageme_preflight.BLOCKER, "blocker"),
        ]
        self.assertEqual(
            stageme_preflight.overall_status(checks), stageme_preflight.BLOCKER
        )

    def test_fixture_absence_is_deferred_before_call(self) -> None:
        check = stageme_preflight.fixture_checks("precall", None)[0]
        self.assertEqual(check.status, stageme_preflight.NOT_YET_REQUIRED)

    def test_fixture_absence_blocks_model_phase(self) -> None:
        check = stageme_preflight.fixture_checks("anyaccomp-local", None)[0]
        self.assertEqual(check.status, stageme_preflight.BLOCKER)

    def test_consent_absence_blocks_model_phase(self) -> None:
        check = stageme_preflight.consent_checks("anyaccomp-local", None)[0]
        self.assertEqual(check.status, stageme_preflight.BLOCKER)

    def test_unaccepted_template_blocks_model_phase(self) -> None:
        consent = (
            Path(__file__).resolve().parents[1]
            / "templates"
            / "STAGEME_CONSENT.example.json"
        )
        check = stageme_preflight.consent_checks("anyaccomp-local", consent)[0]
        self.assertEqual(check.status, stageme_preflight.BLOCKER)

    def _accepted_consent(self, media_hash: str) -> dict[str, object]:
        template = (
            Path(__file__).resolve().parents[1]
            / "templates"
            / "STAGEME_CONSENT.example.json"
        )
        consent = json.loads(template.read_text(encoding="utf-8"))
        consent.update(
            {
                "fixture_id": "F1-test",
                "project_id": "stageme-project-test",
                "source_original_sha256": media_hash,
                "source_canonical_sha256": media_hash,
                "accepted": True,
                "accepted_at_utc": "2026-07-27T12:00:00Z",
            }
        )
        consent["performer_attestation"].update(  # type: ignore[index, union-attr]
            {
                "owns_or_is_authorized_to_use_recording": True,
                "recording_contains_only_authorized_voice": True,
                "recording_contains_no_copyrighted_backing_media": True,
            }
        )
        consent["allowed_purposes"].update(  # type: ignore[index, union-attr]
            {
                "local_media_analysis": True,
                "accompaniment_generation": True,
                "deterministic_mix_and_qc": True,
                "private_human_review": True,
                "temporary_gpu_host_processing": True,
            }
        )
        consent["processing"].update(  # type: ignore[index, union-attr]
            {
                "gpu_host_or_provider": "RunPod Secure Cloud",
                "model_commit": stageme_preflight.ANYACCOMP_CODE_COMMIT,
                "checkpoint_revision": stageme_preflight.ANYACCOMP_CHECKPOINT_REVISION,
                "processing_region": "US-KS-2",
                "approved_spend_cap_usd": 5.0,
                "provider_terms_url": "https://www.runpod.io/legal/terms-of-service",
                "provider_retention_disclosed": True,
            }
        )
        consent["retention"]["deletion_contact_or_command"] = "terminate worker"  # type: ignore[index]
        consent["canonicalization"].update(  # type: ignore[index, union-attr]
            {
                "ffmpeg_version": "ffmpeg version test",
                "ffmpeg_binary_sha256": "a" * 64,
                "command": "recorded deterministic command",
            }
        )
        return consent

    def test_consent_binds_exact_canonical_fixture_and_model(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture.wav"
            fixture.write_bytes(b"exact-fixture")
            media_hash = hashlib.sha256(fixture.read_bytes()).hexdigest()
            consent = self._accepted_consent(media_hash)
            consent_path = root / "consent.json"
            consent_path.write_text(json.dumps(consent), encoding="utf-8")
            environment = {
                "STAGEME_PROJECT_ID": "stageme-project-test",
                "STAGEME_GPU_PROVIDER": "RunPod Secure Cloud",
                "STAGEME_GPU_REGION": "US-KS-2",
                "STAGEME_SPEND_CAP_USD": "5",
            }

            passed = stageme_preflight.consent_checks(
                "anyaccomp-local", consent_path, fixture, environment
            )[0]
            self.assertEqual(passed.status, stageme_preflight.PASS)

            consent["source_canonical_sha256"] = "0" * 64
            consent["processing"]["model_commit"] = "1" * 40  # type: ignore[index]
            consent_path.write_text(json.dumps(consent), encoding="utf-8")
            failed = stageme_preflight.consent_checks(
                "anyaccomp-local", consent_path, fixture, environment
            )[0]
            self.assertEqual(failed.status, stageme_preflight.BLOCKER)
            self.assertIn("does not match fixture", failed.detail)
            self.assertIn("processing.model_commit", failed.detail)

    def test_consent_requires_exact_project_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture.wav"
            fixture.write_bytes(b"exact-fixture")
            media_hash = hashlib.sha256(fixture.read_bytes()).hexdigest()
            consent = self._accepted_consent(media_hash)
            consent["project_id"] = None
            consent_path = root / "consent.json"
            consent_path.write_text(json.dumps(consent), encoding="utf-8")
            failed = stageme_preflight.consent_checks(
                "anyaccomp-local",
                consent_path,
                fixture,
                {
                    "STAGEME_PROJECT_ID": "stageme-project-test",
                    "STAGEME_GPU_PROVIDER": "RunPod Secure Cloud",
                    "STAGEME_GPU_REGION": "US-KS-2",
                    "STAGEME_SPEND_CAP_USD": "5",
                },
            )[0]
            self.assertEqual(failed.status, stageme_preflight.BLOCKER)
            self.assertIn("project_id", failed.detail)

    def test_ace_consent_binds_model_and_checkpoint_revision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture.wav"
            fixture.write_bytes(b"exact-fixture")
            media_hash = hashlib.sha256(fixture.read_bytes()).hexdigest()
            consent = self._accepted_consent(media_hash)
            processing = consent["processing"]
            processing.update(  # type: ignore[union-attr]
                {
                    "model": stageme_preflight.ACESTEP_MODEL_ID,
                    "model_commit": stageme_preflight.ACESTEP_CODE_COMMIT,
                    "checkpoint_revision": stageme_preflight.ACESTEP_CHECKPOINT_REVISION,
                }
            )
            consent_path = root / "consent.json"
            consent_path.write_text(json.dumps(consent), encoding="utf-8")
            environment = {
                "STAGEME_PROJECT_ID": "stageme-project-test",
                "STAGEME_GPU_PROVIDER": "RunPod Secure Cloud",
                "STAGEME_GPU_REGION": "US-KS-2",
                "STAGEME_SPEND_CAP_USD": "5",
            }
            passed = stageme_preflight.consent_checks(
                "ace-hosted", consent_path, fixture, environment
            )[0]
            self.assertEqual(passed.status, stageme_preflight.PASS)

            processing["model"] = "AmphionTeam/AnyAccomp"  # type: ignore[index]
            processing["checkpoint_revision"] = "wrong"  # type: ignore[index]
            consent_path.write_text(json.dumps(consent), encoding="utf-8")
            failed = stageme_preflight.consent_checks(
                "ace-hosted", consent_path, fixture, environment
            )[0]
            self.assertEqual(failed.status, stageme_preflight.BLOCKER)
            self.assertIn("processing.model", failed.detail)
            self.assertIn("processing.checkpoint_revision", failed.detail)

    def test_hard_budget_plan_enforces_provider_deadline_cost(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan_path = Path(directory) / "budget-plan.json"
            hard_terminate_at = datetime.now(timezone.utc) + timedelta(hours=2)
            plan = {
                "schema_version": "1",
                "project_id": "stageme-project-test",
                "provider": "RunPod Secure Cloud",
                "region": "US-KS-2",
                "gpu_offer_label": "NVIDIA A100 80GB PCIe",
                "worker_image": "runpod/pytorch@sha256:" + "a" * 64,
                "provider_price_source_url": "https://www.runpod.io/pricing",
                "price_checked_at_utc": "2026-07-27T12:00:00Z",
                "gpu_rate_usd_per_hour": 1.39,
                "noncompute_reserve_usd": 0.5,
                "approved_spend_cap_usd": 5.0,
                "hard_terminate_after_hours": 3,
                "hard_terminate_at_utc": hard_terminate_at.isoformat(),
                "hard_termination_control": "runpodctl pod create --terminate-after",
                "hard_termination_argument_semantics": "absolute-rfc3339-utc",
                "runpodctl_version": "2.7.2",
                "model": "AmphionTeam/AnyAccomp",
                "model_commit": stageme_preflight.ANYACCOMP_CODE_COMMIT,
                "checkpoint_revision": stageme_preflight.ANYACCOMP_CHECKPOINT_REVISION,
                "owner_approved": True,
            }
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            environment = {
                "STAGEME_PROJECT_ID": "stageme-project-test",
                "STAGEME_GPU_PROVIDER": "RunPod Secure Cloud",
                "STAGEME_GPU_REGION": "US-KS-2",
                "STAGEME_SPEND_CAP_USD": "5",
            }
            passed = stageme_preflight.budget_plan_checks(
                "anyaccomp-local", plan_path, environment
            )[0]
            self.assertEqual(passed.status, stageme_preflight.PASS)

            plan["hard_terminate_after_hours"] = 4
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            failed = stageme_preflight.budget_plan_checks(
                "anyaccomp-local", plan_path, environment
            )[0]
            self.assertEqual(failed.status, stageme_preflight.BLOCKER)
            self.assertIn("approved_spend_cap_usd", failed.detail)

    def test_hard_budget_plan_rejects_relative_deadline_and_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan_path = Path(directory) / "budget-plan.json"
            plan = {
                "schema_version": "1",
                "project_id": "stageme-project-test",
                "provider": "RunPod Secure Cloud",
                "region": "US-KS-2",
                "gpu_offer_label": "NVIDIA A100 80GB PCIe",
                "worker_image": "runpod/pytorch@sha256:" + "a" * 64,
                "provider_price_source_url": "https://www.runpod.io/pricing",
                "price_checked_at_utc": "2026-07-27T12:00:00Z",
                "gpu_rate_usd_per_hour": 1.0,
                "noncompute_reserve_usd": 0.0,
                "approved_spend_cap_usd": 5.0,
                "hard_terminate_after_hours": 3,
                "hard_terminate_at_utc": "1h",
                "hard_termination_control": "runpodctl pod create --terminate-after",
                "hard_termination_argument_semantics": "relative-duration",
                "runpodctl_version": "2.7.2",
                "model": "AmphionTeam/AnyAccomp",
                "model_commit": stageme_preflight.ANYACCOMP_CODE_COMMIT,
                "checkpoint_revision": stageme_preflight.ANYACCOMP_CHECKPOINT_REVISION,
                "owner_approved": True,
            }
            plan_path.write_text(json.dumps(plan), encoding="utf-8")

            failed = stageme_preflight.budget_plan_checks(
                "anyaccomp-local", plan_path, {}
            )[0]
            binding_failed = stageme_preflight.budget_plan_checks(
                "anyaccomp-binding", plan_path, {}
            )[0]

            self.assertEqual(failed.status, stageme_preflight.BLOCKER)
            self.assertEqual(binding_failed.status, stageme_preflight.BLOCKER)
            self.assertIn("hard_terminate_at_utc", failed.detail)
            self.assertIn("hard_termination_argument_semantics", failed.detail)
            self.assertNotIn("1h", failed.detail)
            self.assertNotIn("relative-duration", failed.detail)

    def test_hard_budget_plan_rejects_stale_absolute_deadline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan_path = Path(directory) / "budget-plan.json"
            stale = datetime.now(timezone.utc) - timedelta(minutes=1)
            plan = {
                "schema_version": "1",
                "project_id": "stageme-project-test",
                "provider": "RunPod Secure Cloud",
                "region": "US-KS-2",
                "gpu_offer_label": "NVIDIA A100 80GB PCIe",
                "worker_image": "runpod/pytorch@sha256:" + "a" * 64,
                "provider_price_source_url": "https://www.runpod.io/pricing",
                "price_checked_at_utc": "2026-07-27T12:00:00Z",
                "gpu_rate_usd_per_hour": 1.0,
                "noncompute_reserve_usd": 0.0,
                "approved_spend_cap_usd": 5.0,
                "hard_terminate_after_hours": 3,
                "hard_terminate_at_utc": stale.isoformat(),
                "hard_termination_control": "runpodctl pod create --terminate-after",
                "hard_termination_argument_semantics": "absolute-rfc3339-utc",
                "runpodctl_version": "2.7.2",
                "model": "AmphionTeam/AnyAccomp",
                "model_commit": stageme_preflight.ANYACCOMP_CODE_COMMIT,
                "checkpoint_revision": stageme_preflight.ANYACCOMP_CHECKPOINT_REVISION,
                "owner_approved": True,
            }
            plan_path.write_text(json.dumps(plan), encoding="utf-8")

            failed = stageme_preflight.budget_plan_checks(
                "anyaccomp-local", plan_path, {}
            )[0]

            self.assertEqual(failed.status, stageme_preflight.BLOCKER)
            self.assertEqual(
                failed.detail,
                "Missing/invalid field names only: hard_terminate_at_utc",
            )

    def test_deadline_fields_are_optional_for_binding_but_required_locally(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan_path = Path(directory) / "budget-plan.json"
            plan = {
                "schema_version": "1",
                "project_id": "stageme-project-test",
                "provider": "RunPod Secure Cloud",
                "region": "US-KS-2",
                "gpu_offer_label": "NVIDIA A100 80GB PCIe",
                "worker_image": "runpod/pytorch@sha256:" + "a" * 64,
                "provider_price_source_url": "https://www.runpod.io/pricing",
                "price_checked_at_utc": "2026-07-27T12:00:00Z",
                "gpu_rate_usd_per_hour": 1.0,
                "noncompute_reserve_usd": 0.0,
                "approved_spend_cap_usd": 5.0,
                "hard_terminate_after_hours": 3,
                "hard_terminate_at_utc": None,
                "hard_termination_control": "runpodctl pod create --terminate-after",
                "hard_termination_argument_semantics": None,
                "runpodctl_version": None,
                "model": "AmphionTeam/AnyAccomp",
                "model_commit": stageme_preflight.ANYACCOMP_CODE_COMMIT,
                "checkpoint_revision": stageme_preflight.ANYACCOMP_CHECKPOINT_REVISION,
                "owner_approved": True,
            }
            plan_path.write_text(json.dumps(plan), encoding="utf-8")

            binding = stageme_preflight.budget_plan_checks(
                "anyaccomp-binding", plan_path, {}
            )[0]
            local = stageme_preflight.budget_plan_checks(
                "anyaccomp-local", plan_path, {}
            )[0]
            all_phase = stageme_preflight.budget_plan_checks("all", plan_path, {})[0]

            self.assertEqual(binding.status, stageme_preflight.PASS)
            self.assertEqual(local.status, stageme_preflight.BLOCKER)
            self.assertEqual(all_phase.status, stageme_preflight.BLOCKER)
            self.assertIn("hard_terminate_at_utc", local.detail)
            self.assertIn("hard_termination_argument_semantics", local.detail)
            self.assertIn("runpodctl_version", local.detail)

    def test_precall_binds_original_before_canonical_derivation_exists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "original.m4a"
            fixture.write_bytes(b"original-container-bytes")
            media_hash = hashlib.sha256(fixture.read_bytes()).hexdigest()
            consent = self._accepted_consent(media_hash)
            consent["source_canonical_sha256"] = None
            consent["canonicalization"].update(  # type: ignore[index, union-attr]
                {
                    "ffmpeg_version": None,
                    "ffmpeg_binary_sha256": None,
                    "command": None,
                }
            )
            consent_path = root / "consent.json"
            consent_path.write_text(json.dumps(consent), encoding="utf-8")
            check = stageme_preflight.consent_checks(
                "precall", consent_path, fixture, {}
            )[0]
            self.assertEqual(check.status, stageme_preflight.PASS)

    def test_model_python_is_deferred_before_call(self) -> None:
        check = stageme_preflight.model_python_checks("precall", None)[0]
        self.assertEqual(check.status, stageme_preflight.NOT_YET_REQUIRED)

    def test_stock_anyaccomp_requires_python_39(self) -> None:
        with (
            patch.object(stageme_preflight.os, "access", return_value=True),
            patch.object(stageme_preflight.Path, "is_file", return_value=True),
            patch.object(stageme_preflight, "_run", return_value=(0, "Python 3.9.21")),
        ):
            check = stageme_preflight.model_python_checks(
                "anyaccomp-local", Path("/not-disclosed/python")
            )[0]
        self.assertEqual(check.status, stageme_preflight.PASS)

    def test_stock_anyaccomp_cuda_smoke_is_fail_closed(self) -> None:
        inventory = json.dumps(
            {
                "torch": "2.3.1",
                "torchaudio": "2.3.1",
                "torchvision": "0.18.1",
                "cuda_build": "12.1",
                "cuda_available": True,
                "bf16": True,
                "capability": [8, 6],
                "vram": 24 * 1024**3,
            }
        )

        def fake_run(command: object, timeout: float = 8.0, cwd: Path | None = None):
            del timeout, cwd
            return (0, "Python 3.9.21") if "--version" in command else (0, inventory)

        with (
            patch.object(stageme_preflight.os, "access", return_value=True),
            patch.object(stageme_preflight.Path, "is_file", return_value=True),
            patch.object(stageme_preflight, "_run", side_effect=fake_run),
        ):
            checks = stageme_preflight.model_python_checks(
                "anyaccomp-local", Path("/not-disclosed/python")
            )
        self.assertTrue(all(check.status == stageme_preflight.PASS for check in checks))

    def test_worker_source_uses_explicit_root_and_pinned_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "AnyAccomp"
            for rel in (
                "infer_from_folder.py",
                "requirements.txt",
                "config/flow_matching.json",
                "config/vocoder.json",
            ):
                path = source / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            with patch.object(
                stageme_preflight,
                "_run",
                return_value=(0, stageme_preflight.ANYACCOMP_CODE_COMMIT),
            ):
                checks = stageme_preflight.directory_checks(
                    "anyaccomp-local", root, root, None, source
                )
            source_check = next(
                check
                for check in checks
                if check.check_id == "repository.anyaccomp-worker-source"
            )
            self.assertEqual(source_check.status, stageme_preflight.PASS)

            with patch.object(stageme_preflight, "_run", return_value=(0, "0" * 40)):
                checks = stageme_preflight.directory_checks(
                    "anyaccomp-local", root, root, None, source
                )
            source_check = next(
                check
                for check in checks
                if check.check_id == "repository.anyaccomp-worker-source"
            )
            self.assertEqual(source_check.status, stageme_preflight.BLOCKER)

            def dirty_run(
                command: object, timeout: float = 8.0, cwd: Path | None = None
            ):
                del timeout, cwd
                return (
                    (1, "")
                    if "diff" in command
                    else (0, stageme_preflight.ANYACCOMP_CODE_COMMIT)
                )

            with patch.object(stageme_preflight, "_run", side_effect=dirty_run):
                checks = stageme_preflight.directory_checks(
                    "anyaccomp-local", root, root, None, source
                )
            source_check = next(
                check
                for check in checks
                if check.check_id == "repository.anyaccomp-worker-source"
            )
            self.assertEqual(source_check.status, stageme_preflight.BLOCKER)

    def test_worker_fixture_requires_canonical_non_silent_audio(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "silent-stereo.wav"
            with wave.open(str(fixture), "wb") as handle:
                handle.setnchannels(2)
                handle.setsampwidth(2)
                handle.setframerate(48_000)
                handle.writeframes(b"\0" * 48_000 * 2 * 2 * 10)
            check = stageme_preflight.fixture_checks("anyaccomp-local", fixture)[0]
            self.assertEqual(check.status, stageme_preflight.BLOCKER)

    def test_build_report_cli_shape_does_not_crash(self) -> None:
        args = stageme_preflight.parse_args(["--phase", "precall"])
        report = stageme_preflight.build_report(args)
        self.assertIn(
            report["overall"], {stageme_preflight.PASS, stageme_preflight.WARNING}
        )

    def test_wrong_anyaccomp_python_blocks(self) -> None:
        with (
            patch.object(stageme_preflight.os, "access", return_value=True),
            patch.object(stageme_preflight.Path, "is_file", return_value=True),
            patch.object(stageme_preflight, "_run", return_value=(0, "Python 3.12.13")),
        ):
            check = stageme_preflight.model_python_checks(
                "anyaccomp-local", Path("/not-disclosed/python")
            )[0]
        self.assertEqual(check.status, stageme_preflight.BLOCKER)

    def test_docker_is_only_required_when_selected(self) -> None:
        with (
            patch.object(stageme_preflight, "_command_version", return_value=None),
            patch.object(stageme_preflight.shutil, "which", return_value=None),
        ):
            optional = next(
                check
                for check in stageme_preflight.tool_checks("anyaccomp-local")
                if check.check_id == "tool.docker"
            )
            required = next(
                check
                for check in stageme_preflight.tool_checks(
                    "anyaccomp-local", require_docker=True
                )
                if check.check_id == "tool.docker"
            )
        self.assertEqual(optional.status, stageme_preflight.NOT_YET_REQUIRED)
        self.assertEqual(required.status, stageme_preflight.BLOCKER)


if __name__ == "__main__":
    unittest.main()
