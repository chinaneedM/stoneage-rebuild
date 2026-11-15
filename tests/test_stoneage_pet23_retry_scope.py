"""PET23 finite retry/source immutability and private custody safety gates."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import stoneage_pet23_low_rate_retry as pet23
import stoneage_pet23_verify_private_gif as private


class Pet23Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.old = pet23.load_pinned_inputs()

    def test_12_spread_sources_are_all_previously_unobserved_and_unambiguous(self):
        targets = pet23.source_ready_targets(self.catalog, self.old)
        self.assertEqual([t["web_ordinal"] for t in targets],
                         [11, 22, 33, 43, 49, 60, 71, 84, 103, 110, 114, 124])
        self.assertEqual([sum(1 for t in targets if 1 <= t["web_ordinal"] <= 45),
                          sum(1 for t in targets if 46 <= t["web_ordinal"] <= 90),
                          sum(1 for t in targets if 91 <= t["web_ordinal"] <= 124)],
                         [4, 4, 4])
        self.assertTrue(all(t["actual_client_species_id"] is None for t in targets))
        self.assertTrue(all(t["public_use_permission_verified"] is False for t in targets))

    def test_no_prior_verified_images_get_recounted(self):
        existing = [r for r in self.old["records"]
                    if r["best_archival_observation_sha256_or_null"]]
        self.assertEqual(len(existing), 28)
        self.assertEqual(len(self.old["records"]), 124)
        tampered = copy.deepcopy(self.old)
        tampered["records"][10]["best_archival_observation_sha256_or_null"] = "0" * 64
        with self.assertRaises(ValueError):
            pet23.source_ready_targets(self.catalog, tampered)

    def test_changing_original_image_url_fails_closed(self):
        altered = copy.deepcopy(self.old)
        altered["records"][21]["original_image_url"] += "123"
        with self.assertRaises(ValueError):
            pet23.source_ready_targets(self.catalog, altered)

    def test_private_verifier_blocks_unknown_sha_and_non_image(self):
        with tempfile.TemporaryDirectory() as d:
            file = Path(d) / "private.gif"
            file.write_bytes(b"not an original archived GIF")
            with self.assertRaises(ValueError):
                private.verify_private_file(100, file, self.old)
            with self.assertRaises(ValueError):
                private.verify_private_file(1, file, self.old)

    def test_private_verifier_refuses_fake_gif_hash(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "fake.gif"
            f.write_bytes(b"GIF89a" + (60).to_bytes(2, "little") +
                          (65).to_bytes(2, "little") + b"fake")
            with self.assertRaises(ValueError):
                private.verify_private_file(1, f, self.old)


if __name__ == "__main__":
    unittest.main()
