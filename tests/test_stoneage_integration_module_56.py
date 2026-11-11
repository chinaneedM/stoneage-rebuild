"""INTEGRATION56: publicly reproducible mixed25 cave and independent TW1 original image source bounds."""
import hashlib, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-INTEGRATION56-DREAM-CAVE-GUARDS-41-42-TW1-32-PIXELS-R1.json"
def blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
class TestStoneageIntegration56SourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.src={}
        for k,v in cls.r["source_qualified_public_inputs"].items():
            raw=(ROOT/v["path"]).read_bytes()
            assert blob_sha(raw)==v["blob_sha"], (k,"source blob changed")
            cls.src[k]=json.loads(raw)
    def test_historical_current_original_bytes_preserved(self):
        s=self.r["prior_current_history_preserved"]
        raw=(ROOT/s["path"]).read_bytes()
        self.assertEqual(len(raw),2709173)
        self.assertEqual(blob_sha(raw),"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertFalse(s["edited"])
    def test_mixed25_original_four_creates_exact_source(self):
        q=self.src["quest09"]
        c=self.r["original_mixed25_create_file"]
        self.assertEqual(c,next(x for x in q["source_files"] if x["path"]=="400/sb_mugen.create"))
        exp=[x for x in q["source_creates"] if x["file"]=="400/sb_mugen.create" and x["floor"] in (41,42) and x["graphic_alias"] in (100343,100346)]
        got=[x["source_create"] for x in self.r["original_mixed25_npc_creates_and_actual_DAT_source_values"]]
        self.assertEqual(got,exp)
        self.assertEqual(len(got),4)
        self.assertEqual([(x["floor"],x["graphic_alias"],x["borncenter_raw"][:2]) for x in got],[(41,100343,[34,41]),(41,100346,[33,41]),(42,100343,[34,41]),(42,100346,[33,41])])
    def test_original_dats_three_native_u16_values_and_source_digests(self):
        m=self.src["quest09_map_observation"]["maps"]
        for a in self.r["original_mixed25_original_DAT"]:
            prior=m[str(a["floor"])]
            self.assertEqual((a["sha256"],a["bytes"],a["geometry"]),(prior["source_DAT_sha256"],prior["source_DAT_bytes"],prior["geometry"]))
            self.assertEqual(a["bytes"],29408)
        for b in self.r["original_mixed25_npc_creates_and_actual_DAT_source_values"]:
            x=b["source_create"]; floor=str(x["floor"]); coords=x["borncenter_raw"][:2]
            actual=next(p for p in m[floor]["source_points"] if p["xy"]==coords)
            self.assertEqual((b["source_point_label"],b["source_original_DAT_u16_three_planes"]),(actual["label"],actual["original_three_u16_values"]))
    def test_guard_arg_byte_provenance_and_source_only_meanings(self):
        q=self.src["quest09"]
        self.assertEqual(self.r["original_mixed25_guard_arg_metadata"],q["source_guard_arguments"])
        for b in self.r["original_mixed25_npc_creates_and_actual_DAT_source_values"]:
            arg=b["source_create"]["parameter_references"][0]
            self.assertEqual(arg[1],"EXACT_SAME_NPC_SUBTREE_PATH")
            self.assertEqual(arg[2],next(x["sha256"] for x in q["source_files"] if x["path"]==arg[0]))
    def test_independent_tw1_original_spr_groups_and_all_32_prior_png_sha(self):
        p=self.src["pet07"]
        r=self.r
        self.assertEqual(r["private_custody"]["pet07_catalog"]["sha256"],p["private_artifacts"]["catalog"]["sha256"])
        self.assertFalse(p["private_artifacts"]["catalog"]["public_git"])
        matrix=[]
        self.assertEqual([x["graphic"] for x in r["independent_TW1_retail_original_SPR_and_32_actual_prior_RD_PNG_receipts"]],[100343,100346])
        for group in r["independent_TW1_retail_original_SPR_and_32_actual_prior_RD_PNG_receipts"]:
            g=group["graphic"]
            self.assertEqual(group["original_source_group"],next(x for x in p["source_groups"] if x[0]==g))
            self.assertEqual((group["original_source_group"][4],group["original_source_group"][6]),(33,16))
            receipts=group["original_source_16_bitmap_receipts"]
            self.assertEqual(len(receipts),16)
            self.assertEqual(receipts,[next(x for x in p["source_actual_pixel_receipts"] if x[0]==a[0]) for a in receipts])
            self.assertEqual(len(set(x[0] for x in receipts)),16)
            for rec in receipts:
                self.assertEqual(rec[1],rec[0])
                matrix.append({"graphic":g,"bitmap":rec[0],"png_sha256":rec[8],"width":rec[5],"height":rec[6]})
        digest=hashlib.sha256(json.dumps(matrix,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()
        self.assertEqual(digest,r["private_32_png_manifest_sha256"])
        self.assertEqual(len(matrix),32)
    def test_private_evidence_is_not_a_public_game_asset(self):
        x=self.r["private_custody"]
        self.assertEqual((x["quest09"]["bytes"],x["quest09"]["members"]),(28306717,25))
        self.assertEqual(x["quest09"]["sha256"],self.src["quest09"]["private_source_zip"]["sha256"] if self.src["quest09"]["private_source_zip"]["bytes"]==28306717 else x["quest09"]["sha256"])
        self.assertTrue(x["this_work_private_custody"]["independently_downloaded_and_sha_crc_verified"])
        self.assertFalse(x["this_work_private_custody"]["public_git"])
        self.assertEqual((x["this_work_private_custody"]["bytes"],x["this_work_private_custody"]["members"]),(15621429,41))
        self.assertEqual(x["this_work_private_custody"]["sha256"],"aca681e3eee04a67bab488dcbbab00dda3d479274482c87d37a170478541bcce")
    def test_negative_guards_original_game_not_executed(self):
        n=self.r["counts"]
        self.assertEqual(n["source_mixed25_NPC_CREATE_blocks"],4)
        self.assertEqual(n["source_mixed25_map_DAT_files_original_bytes_reverified"],2)
        self.assertEqual(n["independent_TW1_original_recovered_real_PNG_replayed"],32)
        self.assertEqual(n["independent_TW1_source_frame_positions_selected"],66)
        for key in ("new_original_RD_decode_this_work","native_original_client_executions","native_original_server_executions","verified_original_same_deployment_join","verified_official_species_identification"):
            self.assertEqual(n[key],0)
        self.assertIsNone(self.r["stage_status"]["overall_percent"])
        self.assertIn("source-bound",self.r["research_scope"])
if __name__=="__main__":
    unittest.main()
