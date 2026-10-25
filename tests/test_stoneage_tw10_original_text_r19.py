"""Synthetic R19 source boundary tests: no game binary needed in the repository."""
import unittest
from tools.stoneage_tw10_original_text_r19 import bounded_candidates, analyze_executables, EXPECTED

class R19Contract(unittest.TestCase):
    def test_big5_nul_label_is_candidate_not_quest(self):
        data = b"\x00" + "寵物名字".encode("cp950") + b"\x00"
        rows = bounded_candidates(data)
        self.assertGreaterEqual(rows["candidate_decode_occurrences"], 1)
        self.assertTrue(any(r["decoded_short_label"] == "寵物名字" for r in rows["candidates"]))
        self.assertTrue(all(r["entity_id"] is None and r["bitmap_id"] is None for r in rows["candidates"]))
        self.assertTrue(all(not r["npc_quest_pet_identity_qualified"] for r in rows["candidates"]))

    def test_ascii_only_is_not_han(self):
        self.assertEqual(bounded_candidates(b"\x00STONEAGE\x00")["candidate_decode_occurrences"], 0)

    def test_not_nul_terminated_is_not_evidence(self):
        self.assertEqual(bounded_candidates("寵物名字".encode("cp950"))["candidate_decode_occurrences"], 0)

    def test_bound_and_repeated_positions_preserved(self):
        data = ("寵物名字".encode("cp950") + b"\x00") * 4
        rows = bounded_candidates(data, 2)
        self.assertGreater(rows["candidate_decode_occurrences"], 2)
        self.assertEqual(rows["sampled_candidate_count"], 2)
        self.assertTrue(rows["sampling_truncated"])
        self.assertEqual(len({(r["source_file_offset"],r["source_candidate_codec"]) for r in rows["candidates"]}),2)

    def test_false_real_source_rejected(self):
        with self.assertRaises(ValueError):
            analyze_executables({"StoneAge/sa_3.exe": b"fake"})
        with self.assertRaises(ValueError):
            analyze_executables({key: b"fake" for key in EXPECTED})

    def test_sample_bound_rejected(self):
        for bound in [0, 65]:
            with self.assertRaises(ValueError):
                bounded_candidates(b"something", bound)

    def test_actual_original_digests_are_pinned(self):
        self.assertEqual(EXPECTED["StoneAge/sa_3.exe"][0], 425984)
        self.assertEqual(EXPECTED["StoneAge/StoneAge.exe"][0], 409600)
        self.assertEqual(len(EXPECTED["StoneAge/sa_3.exe"][1]), 64)
        self.assertEqual(len(EXPECTED["StoneAge/StoneAge.exe"][1]), 64)
if __name__ == "__main__":
    unittest.main()
