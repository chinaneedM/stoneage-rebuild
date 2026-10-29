import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("scene26", ROOT / "tools/stoneage_scene26_pet_action1.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class TestSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = mod.load_pinned(mod.SRC, mod.SRC_BLOB)
        cls.cross = mod.load_pinned(mod.XREF, mod.XREF_BLOB)

    def test_git_blob_integrity(self):
        for name, sha in ((mod.SRC, mod.SRC_BLOB), (mod.XREF, mod.XREF_BLOB)):
            self.assertEqual(mod.git_blob_sha((ROOT / name).read_bytes()), sha)

    def test_complete_machine_report(self):
        actual = mod.derive(self.source, self.cross)
        published = __import__("json").loads((ROOT / mod.OUT).read_text(encoding="utf-8"))
        self.assertEqual(actual, published)
        self.assertEqual(actual["summary"], {
            "group_count": 3, "direction_sequences": 24,
            "frame_occurrences": 80, "distinct_bitmap_numbers": 48,
            "zero_sound_field_occurrences": 80
        })
        self.assertIsNone(actual["interpretation"]["overall_restoration_percentage"])
        self.assertFalse(actual["interpretation"]["original_game_executed"])

    def test_action_identity_not_promoted(self):
        for g in mod.derive(self.source, self.cross)["groups"]:
            self.assertEqual(g["action_code"], 1)
            self.assertEqual([a["direction"] for a in g["directions"]], list(range(8)))
            self.assertTrue(all(a["duration_word"] == 100 for a in g["directions"]))

    def test_missing_direction_rejected(self):
        s = copy.deepcopy(self.source)
        g = s["material"]["selected_groups"][0]
        g["animations"] = [a for a in g["animations"] if not (a["anim_no"] == 1 and a["direction"] == 7)]
        with self.assertRaisesRegex(ValueError, "direction"):
            mod.derive(s, self.cross)

    def test_wrong_crossversion_segment_rejected(self):
        x = copy.deepcopy(self.cross)
        x["full_segment_comparisons"][0]["reference_occurrences"]["TW10"][0]["segment_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "equality"):
            mod.derive(self.source, x)

    def test_source_scope_conflict_rejected(self):
        x = copy.deepcopy(self.cross)
        x["source_scope"] = "OFFICIAL_SAME_DEPLOYMENT"
        with self.assertRaisesRegex(ValueError, "scope"):
            mod.derive(self.source, x)

    def test_frame_changed_rejected(self):
        s = copy.deepcopy(self.source)
        g = s["material"]["selected_groups"][1]
        a = next(x for x in g["animations"] if x["anim_no"] == 1 and x["direction"] == 0)
        a["frames"][1][0] += 1
        with self.assertRaisesRegex(ValueError, "repeated-frame"):
            mod.derive(s, self.cross)

    def test_sound_added_rejected(self):
        s = copy.deepcopy(self.source)
        a = next(x for x in s["material"]["selected_groups"][2]["animations"] if x["anim_no"] == 1)
        a["frames"][0][3] = 73
        with self.assertRaisesRegex(ValueError, "sound pattern"):
            mod.derive(s, self.cross)

    def test_no_dedup_of_duplicate_frame_occurrences(self):
        g0 = mod.derive(self.source, self.cross)["groups"][0]
        self.assertEqual(g0["directions"][0]["frames"][0][0], g0["directions"][0]["frames"][1][0])
        self.assertEqual(g0["directions"][0]["frames"][1][0], g0["directions"][0]["frames"][2][0])
        self.assertNotEqual(g0["directions"][0]["frames"][2][0], g0["directions"][0]["frames"][3][0])


if __name__ == "__main__":
    unittest.main()
