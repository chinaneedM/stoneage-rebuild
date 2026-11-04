"""WORLD08: archived 279 NPCEnemy refs x pinned later community C semantics.
No original commercial server/game execution or early-official attribution.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import os
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / "research" / "recovered"
MANIFEST = "STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json"
REPORT = "STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-08-NPCENEMY-APPEARANCE-OUTCOME-R1.json"
PINNED_BLOB = "45c95d9df8b1e3e9d41443ca12f6ac8f4c105fc4"


def load(name):
    return json.loads((REC / name).read_text(encoding="utf-8"))


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


class World08NPCEnemy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load(MANIFEST)
        cls.w = load(REPORT)

    def test_exhaustive_create_to_arg_join_and_distribution(self):
        d = self.d
        cols = {name: i for i, name in enumerate(d["arg_columns"])}
        cref = {name: i for i, name in enumerate(d["create_ref_columns"])}
        files = {row[cols["relative_arg_path"]]: row for row in d["argument_files"]}
        self.assertEqual((len(files), len(d["create_refs"])), (260, 279))
        vals = {k: [] for k in ["gym", "dieact", "entype", "onebattle", "newnpc"]}
        bad_warp = 0
        for ref in d["create_refs"]:
            source = files[ref[cref["arg_relative_path"]]]
            self.assertEqual(ref[cref["arg_original_sha256"]], source[cols["source_bytes_sha256"]])
            for out, field in [
                ("gym", "raw_gym_int_or_null"),
                ("dieact", "raw_dieact_int_or_null"),
                ("entype", "raw_entype_int_or_null"),
                ("onebattle", "raw_onebattle_int_or_null"),
                ("newnpc", "has_NEWNPCENEMY_token_bool_as_int"),
            ]:
                vals[out].append(source[cols[field]])
            if source[cols["raw_dieact_int_or_null"]] == 1:
                if not all(isinstance(source[cols[k]], int) for k in (
                    "raw_warpfloor_int_or_null", "raw_warpx_int_or_null", "raw_warpy_int_or_null"
                )):
                    bad_warp += 1
        w = self.w["original_create_derived_counts"]
        gym = Counter(v for v in vals["gym"] if isinstance(v, int) and v > 0)
        self.assertEqual((w["create_refs"], w["unique_arg_files"]), (279, 260))
        self.assertEqual((sum(gym.values()), len(gym), min(gym), max(gym)), (200, 100, 1, 100))
        self.assertEqual(set(gym.values()), {2})
        self.assertEqual((w["gym_positive_create_refs"], w["gym_absent_create_refs"], w["create_refs_per_positive_gym_level"]), (200, 79, 2))
        self.assertEqual((Counter(vals["dieact"])[1], Counter(vals["dieact"])[0]), (w["dieact_one_create_refs"], w["dieact_zero_create_refs"]))
        self.assertEqual((w["dieact_one_create_refs"], w["dieact_zero_create_refs"]), (250, 29))
        self.assertEqual((Counter(vals["onebattle"])[1], Counter(vals["onebattle"])[0], Counter(vals["onebattle"])[None]), (10, 13, 256))
        self.assertEqual((sum(x == 2 for x in vals["entype"]), sum(x == 1 for x in vals["newnpc"])), (279, 2))
        self.assertEqual(bad_warp, 0)
        self.assertEqual(w["dieact_one_with_missing_static_warp_triple"], bad_warp)
        self.assertEqual(w["original_enemy_SPR_number_candidates"], d["counts"]["distinct_original_source_graphic_numbers"])
        self.assertEqual(w["new_original_pixel_decodes"], 0)

    def test_newnpc_override_cases_and_historical_boundaries(self):
        w = self.w
        d = self.d
        self.assertEqual(w["archived_source"]["git_blob_sha"], "3d827b98d00c3caa6e779f34a36d28bd70945b75")
        self.assertEqual(w["archived_source"]["preserved_parent_rar_sha256"], d["original_rar_sha256"])
        a = {row[0]: row for row in d["argument_files"]}
        cols = {name: i for i, name in enumerate(d["arg_columns"])}
        witnesses = w["original_NEWNPCENEMY_marker_witnesses"]
        self.assertEqual(len(witnesses), 2)
        for x in witnesses:
            src = a[x["arg_path"]]
            self.assertEqual(x["arg_sha256"], src[cols["source_bytes_sha256"]])
            self.assertEqual(src[cols["has_NEWNPCENEMY_token_bool_as_int"]], 1)
            self.assertEqual(x["raw_warp_triple"], [src[cols[k]] for k in (
                "raw_warpfloor_int_or_null", "raw_warpx_int_or_null", "raw_warpy_int_or_null"
            )])
        self.assertEqual(w["stage_A"], "7_PARTIAL_2_OPEN")
        self.assertEqual((w["stage_B"], w["wiki"], w["R79"]), ("GATED", "GATED", "PAUSED_NON_BLOCKING"))
        self.assertIsNone(w["overall_percent"])
        self.assertEqual(w["historical_CURRENT_blob_unchanged"], "c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertTrue(all(w["bounds"].values()))

    def test_true_pinned_source_semantics_when_available(self):
        source = os.environ.get("STONEAGE_WORLD08_PINNED_NPCENEMY")
        if not source:
            self.skipTest("No pinned C bytes supplied; local archived graph only")
        raw = Path(source).read_bytes()
        self.assertEqual(git_blob(raw), PINNED_BLOB)
        self.assertEqual(self.w["pinned_code"]["git_blob_sha"], PINNED_BLOB)
        c = raw.decode("latin-1")
        for snippet in (
            'ENEMY_getEnemyArrayFromId( atoi( data))',
            'gymbody[RAND( 0, arraysizeof( gymbody ) - 1)]',
            'CHAR_setInt( meindex, CHAR_LV, gym )',
            'BATTLE_CreateVsEnemy( charaindex, 2, meindex)',
            'BATTLE_CreateVsEnemy( charaindex, 1, meindex)',
            'CHAR_WORK_ONEBATTLE',
            'BattleArray[i].createindex == meindex',
            '].WinFunc',
            'NPC_NPCEnemy_Dying',
            'CHAR_setInt( meindex, CHAR_BASEIMAGENUMBER, 0)',
            'NPCEnemyLoop',
            'CHAR_warpToSpecificPoint(',
            'MAP_IsValidCoordinate(',
        ):
            self.assertIn(snippet, c)
        self.assertEqual(len(re.findall(r'SPR_\d{3}em', c.split("static int gymbody[]")[1].split("};")[0])), 48)
        self.assertIn('if( CHAR_getWorkInt( meindex, CHAR_WORK_DIEACT) == 0 )', c)
        self.assertIn('if( tmp == -1 )', c)
        self.assertIn('NPC_ENEMY_REVIVALTIMA_DEFAULT', c)


if __name__ == "__main__":
    unittest.main()
