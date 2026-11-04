"""Source-bounded doctored-input checks for the 3021/3022 offline content atlas.

The public CI verifies preserved derived numeric evidence only; it does not run
the original commercial client or privately preserved source files.
"""
from collections import Counter
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1] / "research" / "recovered"


def source(name):
    return json.loads((ROOT / name).read_bytes())


class OfflineDojoSourceAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = source("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-01-DOJO-SOURCE-ATLAS-R1.json")
        cls.previous = source("STONEAGE-STAGE-A-3021-3022-ORIGINAL-STATIC-ROUTE-CONTENT-R1.json")
        cls.verified = source("STONEAGE-STAGE-A-INDEPENDENT-RAR-MAP-PIXEL-RECOVERY-R1.json")

    def test_authentic_source_files_and_prior_evidence(self):
        r, old = self.r, self.previous
        self.assertEqual(r["private_original_rar_sha256"], old["source_original_RAR"]["sha256"])
        self.assertEqual(r["npc_create"]["sha256"],
                         old["floor3021_original_NPCCREATE"]["sha256"])
        self.assertEqual(r["npc_create"]["source_npc_blocks"], 300)
        self.assertEqual(r["npc_create"]["disciple_create_blocks"], 100)
        self.assertEqual(r["npc_create"]["independent_warp_create_blocks"], 200)
        for key, previous in [
            ("3021_map", old["floor3021_client_MAP"]),
            ("3022_map", old["floor3022_original_client_MAP"]),
            ("3022_dat", old["floor3022_original_client_DAT"]),
        ]:
            new = r["source_files"][key]
            self.assertEqual((new["bytes"], new["crc32"], new["sha256"]),
                             (previous["size_bytes"], previous["crc32"], previous["sha256"]))
        self.assertRegex(r["private_source_zip_sha256"], r"^[a-f0-9]{64}$")

    def test_all_real_create_and_arg_targets_reconciled(self):
        r = self.r
        old = self.verified["floor3021"]["original_NPCEnemy_ARG_route"]
        original = old["rows"]
        rows = r["disciples"]
        self.assertEqual(len(rows), len(original))
        self.assertEqual([x["ordinal"] for x in rows], list(range(1, 101)))
        self.assertEqual(sum(row["arg_bytes"] for row in rows), old["source_ARG_total_bytes"])
        self.assertEqual(len({x["original_arg_sha256"] for x in rows}), 100)
        self.assertEqual(len({tuple(x["coordinate"]) for x in rows}), 100)
        for new, prior in zip(rows, original):
            with self.subTest(ordinal=new["ordinal"]):
                self.assertEqual(new["ordinal"], prior[0])
                self.assertEqual(new["coordinate"], prior[2])
                self.assertEqual(new["configured_arg_target"], prior[3])
                self.assertEqual(new["arg_bytes"], prior[4])
                self.assertEqual(new["original_arg_sha256"], prior[6])
                x, y = new["coordinate"]
                self.assertGreaterEqual(x, 0)
                self.assertLess(x, 407)
                self.assertGreaterEqual(y, 0)
                self.assertLess(y, 144)
                self.assertEqual(new["warp_positions"], [[x + 6, y + 2], [x + 6, y + 3]])
                self.assertEqual(len(new["warp_map_raw_codes"]), 2)
                self.assertRegex(new["original_arg_sha256"], r"^[a-f0-9]{64}$")
        self.assertEqual(sum(x["configured_arg_target"][0] == 3021 for x in rows), 99)
        self.assertEqual(rows[-1]["configured_arg_target"], [3008, 20, 20])
        self.assertEqual(old["independent_CREATE_exit_target"], [3022, 1, 7])

    def test_original_raw_map_codes_and_two_routes_remain_distinct(self):
        r = self.r
        nums = r["numeric_crosschecks"]
        self.assertEqual(nums["floor_3021_dimensions"], [407, 144])
        self.assertEqual(nums["npc_center_map_codes"],
                         {"0": 25, "257": 26, "42405": 49})
        self.assertEqual(nums["warp_center_map_codes"], {
            "0": 58, "257": 58, "41637": 13, "41674": 8,
            "41677": 21, "41893": 17, "41930": 4, "41932": 21})
        self.assertEqual(sum(nums["npc_center_map_codes"].values()), 100)
        self.assertEqual(sum(nums["warp_center_map_codes"].values()), 200)
        self.assertEqual(Counter(str(x["map_raw_code"]) for x in r["disciples"]),
                         nums["npc_center_map_codes"])
        self.assertEqual(Counter(str(v) for x in r["disciples"] for v in x["warp_map_raw_codes"]),
                         nums["warp_center_map_codes"])
        previous = self.previous["floor3021_original_NPCCREATE"]
        self.assertEqual(sorted((int(k),v) for k,v in nums["npc_center_map_codes"].items()),
                         previous["raw_3021_MAP_values_at_disciple_centers"])
        self.assertEqual(sorted((int(k),v) for k,v in nums["warp_center_map_codes"].items()),
                         previous["raw_3021_MAP_values_at_warp_centers"])
        self.assertEqual(nums["routed_within_3021"], 99)
        self.assertEqual(nums["last_target_3008"], [3008, 20, 20])
        self.assertEqual(nums["independent_warp_create_count"], 200)
        self.assertEqual(nums["independent_warp_target"], [3022, 1, 7])
        self.assertEqual(nums["3022_target_raw"], {
            "MAP": 46003, "DAT_tile": 4085,
            "DAT_object": 0, "DAT_event": 49152,
        })

    def test_source_truth_must_not_become_native_game_claim(self):
        r = self.r
        self.assertEqual(r["evidence"], "SOURCE_FILES_READ_AND_HASH_VERIFIED_STATIC_NOT_NATIVE_PLAY")
        self.assertIn("COMMUNITY_MIXED25", r["archive_scope"])
        self.assertTrue(all(x is False for x in r["evidence_limits"].values()))
        self.assertEqual(r["stage_a"], "7_PARTIAL_2_OPEN")
        self.assertEqual(r["stage_b"], "GATED")
        self.assertEqual(r["R79"], "PAUSED_NON_BLOCKING")
        self.assertIsNone(r["overall_percent"])
        self.assertNotIn("script_message", r["disciples"][0])
        self.assertNotIn("raw_image", r)
        self.assertEqual({int(i) for x in r["disciples"] for i in x["coordinate"] if isinstance(i, int)}.issubset(set(range(407))), True)


if __name__ == "__main__":
    unittest.main()
