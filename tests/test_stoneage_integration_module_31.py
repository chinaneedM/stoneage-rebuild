"""Original conditional WarpMan entrance is distinct from ordinary mapwarp."""
import hashlib,json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-INTEGRATION31-DUNGEON-WARPMAN-ENTRY-SOURCE-R1.json"

def blob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()

class DungeonWarpMan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.src={}
        for k,v in cls.r["upstream"].items():
            raw=(ROOT/v["path"]).read_bytes()
            assert blob(raw)==v["git_blob"],k
            cls.src[k]=json.loads(raw)

    def test_unmodified_full_continuity(self):
        p=self.r["historical_CURRENT"]
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertGreaterEqual(len(raw),p["bytes"])
        self.assertEqual(blob(raw[:p["bytes"]]),p["git_blob"])
        self.assertEqual(p["git_blob"],"c89e0e33537990aa2132b47c40fef49a985a935c")

    def test_private_source_sha_and_original_definition(self):
        p=self.r["raw_private_original_sources"]
        self.assertEqual(p["CHAR01_zip"]["sha256"],
            "c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f")
        self.assertEqual((p["CHAR01_zip"]["members"],p["I30_zip"]["members"]),(2205,28))
        self.assertEqual(p["I30_zip"]["sha256"],self.src["i30"]["private_archive"]["sha256"])
        self.assertEqual(p["npc_create"]["sha256"],self.src["i30"]["original_files"]["npc20600_create_sha256"])
        self.assertEqual(p["mapwarp"]["sha256"],self.src["i30"]["original_files"]["mapwarp_sha256"])
        self.assertEqual((p["npc_create"]["record_start_offset"],p["npc_create"]["record_end_offset_exclusive"]),(974,1137))
        self.assertEqual(p["wpm_parameter"]["sha256"],"6936519676f71b1478d4208241cd20b3437d61af7ac1c0d7ad4780e60b2e51de")

    def test_conditional_warpman_source_and_not_a_plain_row(self):
        p=self.r["entry"]
        n=p["original_create"]
        self.assertEqual((n["floor"],n["xy"],n["alias"],n["direction"],n["function"]),
                         (20606,[9,23],100439,6,"npcgen_warpman"))
        self.assertEqual(p["original_parameter_literals"]["WARP"],[20607,7,5])
        self.assertEqual(p["original_parameter_literals"]["FREE"],"LV>0")
        self.assertEqual(self.r["raw_private_original_sources"]["mapwarp"]["total_source_lines"],2981)
        self.assertEqual(self.r["raw_private_original_sources"]["mapwarp"]["exact_plain_mapwarp_rows_with_start_floor_20606_target_floor_20607"],0)
        self.assertEqual(p["mechanism_source"],"NPCGEN_WARPMAN_PARAMETER_NOT_MAPWARP_DIRECTION")
        self.assertFalse(p["native_conditional_evaluation_or_transfer_verified"])

    def test_dat_cells_from_actual_20606_and_20607(self):
        p=self.r["entry"]; m=self.src["map09"]["maps"]
        self.assertEqual(m["20606"]["geometry"],[70,50])
        self.assertEqual((p["original_DAT_before"]["xy"],p["original_DAT_before"]["u16"]),([9,23],[4074,0,49152]))
        self.assertEqual((p["original_DAT_after"]["xy"],p["original_DAT_after"]["u16"]),([7,5],[4084,0,49155]))
        for key in ("before","after"):
            rec=p["original_DAT_"+key]
            self.assertEqual(rec["source_sha256"],m[str(rec["floor"])]["source_sha256"])
            self.assertEqual(rec["source_sha256"],self.src["i30"]["original_files"]["DAT_sha256"][str(rec["floor"])])

    def test_outbound_is_a_different_original_mechanism(self):
        out=self.r["outbound"]
        prior=next(x for x in self.src["i30"]["other_directed_warps"] if x["line"]==2307)
        self.assertEqual((out["start"],out["target"],out["start_u16"],out["target_u16"]),
                         (prior["start"],prior["target"],prior["start_u16"],prior["target_u16"]))
        self.assertEqual(out["original_full_line_SHA256_including_LF"],prior["sha256"])
        self.assertEqual(out["target"],[20606,8,23])
        self.assertNotEqual(out["target"][1:],self.r["entry"]["original_create"]["xy"])
        self.assertFalse(out["explicit_ordinary_reverse_row_in_entire_mapwarp"])
        self.assertTrue(out["different_target_from_warpman_location"])

    def test_native_evidence_not_inferred_from_static_strings(self):
        limits=self.r["scope_limits"]
        for k in ("original_client_running","original_server_running","private_originals_published"):
            self.assertFalse(limits[k])
        self.assertTrue(limits["flat_mapwarp_absence_does_not_rule_out_warpman"])
        self.assertTrue(limits["npc_dialogue_not_password_runtime_proof"])
        self.assertEqual((limits["stage_A"],limits["stage_B_wiki"],limits["R79"],limits["overall_percent"]),
                         ("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))

if __name__=="__main__":
    unittest.main()
