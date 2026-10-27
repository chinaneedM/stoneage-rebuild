"""Adversarial checks keep original gameplay separate from synthetic locale."""
import copy
import unittest
from tools.stoneage_p3f_manifest_probe import (
    LAYERS, STATUS_GO, STATUS_BLOCKED, candidate, validate,
)


def fixture(acp=950, depth=8):
    def exe(codepage, bpp):
        return {
            "original_executed": False, "pointer_bytes": 4,
            "desktop_mode_changed": False, "cp950_installed": True,
            "cp950_sample_fallback": False,
            "cp950_sample_bytes": list("石器".encode("cp950")),
            "acp_before": codepage, "acp_after_console950": codepage,
            "display_bpp": bpp, "ddraw_create": 0,
            "ddraw_current_result": 0, "ddraw_current": [640, 480, bpp],
        }
    report = {
        "schema": "stoneage.p3f.synthetic_process_acp_manifest.v1",
        "case_order": list(LAYERS),
        "cases": [{
            "layer": layer, "plain_x86": exe(1252, 32 if i == 0 else 8),
            "embedded_zh_tw_manifest": exe(acp, 32 if i == 0 else depth),
        } for i, layer in enumerate(LAYERS)],
        "original_client_downloaded": False, "original_client_executed": False,
        "world_entered": False, "original_server_contacted": False,
        "palette_pixels_same_process_qualified": False,
        "mouse_input_same_process_qualified": False,
        "original_process_isolation_qualified": False,
    }
    report["synthetic_acp950_8bpp_candidate"] = candidate(report)
    report["status"] = STATUS_GO if candidate(report) else STATUS_BLOCKED
    return report


class P3FManifestBoundaries(unittest.TestCase):
    def test_positive_only_synthetic_candidate(self):
        self.assertTrue(validate(fixture()))

    def test_1252_is_a_real_blocker(self):
        self.assertFalse(validate(fixture(acp=1252)))

    def test_32bpp_not_8bpp(self):
        self.assertFalse(validate(fixture(depth=32)))

    def test_codepage_after_console_must_not_be_forged(self):
        report = fixture(acp=1252)
        report["cases"][1]["embedded_zh_tw_manifest"]["acp_after_console950"] = 950
        with self.assertRaises(AssertionError): validate(report)

    def test_process_observed_not_promoted_to_game_world(self):
        for field in ("original_client_executed", "world_entered", "original_server_contacted"):
            report = fixture()
            report[field] = True
            with self.assertRaises(AssertionError): validate(report)

    def test_reject_unsupported_palette_or_input_claim(self):
        for field in ("palette_pixels_same_process_qualified",
                      "mouse_input_same_process_qualified",
                      "original_process_isolation_qualified"):
            report = fixture()
            report[field] = True
            with self.assertRaises(AssertionError): validate(report)

    def test_missing_layer(self):
        report = fixture()
        report["cases"].pop()
        with self.assertRaises(AssertionError): validate(report)

    def test_ddraw_32bpp_even_when_gdi_says_8bpp(self):
        report = fixture()
        for row in report["cases"][1:]:
            row["embedded_zh_tw_manifest"]["ddraw_current"][2] = 32
        with self.assertRaises(AssertionError): validate(report)

    def test_forged_candidate_flag(self):
        report = fixture(acp=1252)
        report["synthetic_acp950_8bpp_candidate"] = True
        report["status"] = STATUS_GO
        with self.assertRaises(AssertionError): validate(report)

    def test_source_gdi_same_process_pair(self):
        report = fixture()
        report["cases"][1]["embedded_zh_tw_manifest"]["display_bpp"] = 32
        with self.assertRaises(AssertionError): validate(report)

    def test_both_paired_process_architecture(self):
        report = fixture()
        report["cases"][0]["embedded_zh_tw_manifest"]["pointer_bytes"] = 8
        with self.assertRaises(AssertionError): validate(report)


if __name__ == "__main__":
    unittest.main()
