"""INTEGRATION35: source-only Kelke original mining, appraisal and office relation guards."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-INTEGRATION35-SAINASU-MINERAL-APPRAISAL-SOURCE-R1.json"

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

class Integration35(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.sources={}
        for k,x in cls.r["upstream"].items():
            p=ROOT/x["path"]
            raw=p.read_bytes()
            assert git_blob(raw)==x["git_blob"], (k,p)
            cls.sources[k]=json.loads(raw)

    def test_full_original_CURRENT_protected(self):
        r=self.r["remote_baseline"]
        b=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertGreaterEqual(len(b),r["CURRENT_original_bytes"])
        self.assertEqual(git_blob(b[:r["CURRENT_original_bytes"]]),r["CURRENT_original_git_blob"])
        self.assertEqual(r["CURRENT_original_bytes"],2709173)

    def test_private_source_digest_and_no_proprietary_payload(self):
        p=self.r["original_private_archives"]
        self.assertEqual([(p[k]["bytes"],p[k]["member_count"]) for k in ("char01","item01")],
                         [(995176,2205),(5868386,838)])
        for rec in p.values():
            self.assertTrue(rec["whole_sha_and_all_CRC_verified_this_unit"])
            self.assertEqual(len(rec["sha256"]),64)
        self.assertFalse(self.r["item_rows"]["original_art_bytes_or_dialogues_in_public_git"])

    def test_six_source_scripts_and_CREATE_relations(self):
        c=self.sources["quest01"]
        p={x["path"]:x for x in c["source_scripts"]}
        scripts=self.r["source_scripts"]
        self.assertEqual(len(scripts),6)
        self.assertEqual(sum(sum(x["actual_block_type_counts"].values()) for x in scripts),21)
        for x in scripts:
            src=p[x["path"]]
            for a in ("original_size","original_sha256","original_crc32","actual_block_type_counts","quest_origin"):
                self.assertEqual(x[a],src[a])
        rows=self.r["source_npcs"]
        self.assertEqual(len(rows),6)
        self.assertEqual([(x["floorid"],x["xy"]) for x in rows],
                         [(10605,[42,32]),(10605,[42,34]),(10605,[42,36]),
                          (10603,[45,23]),(1212,[17,15]),(1212,[11,4])])
        self.assertEqual([x["graphic_alias_numeric"] for x in rows],
                         [16017,16018,16025,16018,16025,16066])
        for x in rows:
            y=next(z for z in c["source_creation_references"]
                   if z["create_source_path"]==x["create_source_path"]
                   and z["create_brace_ordinal"]==x["create_brace_ordinal"])
            for k in ("create_source_sha","original_script_path","original_script_sha","floorid","graphic_alias_numeric"):
                self.assertEqual(x[k],y[k])
            self.assertEqual(x["create_source_sha"],self.r["source_CREATE_file"]["sha256"])

    def test_all_21_original_block_hashes_are_preexisting_not_new_scripts(self):
        o=self.sources["quest01"]["source_event_blocks"]
        blocks=self.r["source_event_blocks"]
        self.assertEqual(len(blocks),21)
        self.assertEqual((sum(x["raw_type"]=="ACCEPT" for x in blocks),
                          sum(x["raw_type"]=="MESSAGE" for x in blocks)),(12,9))
        for x in blocks:
            y=next(z for z in o if z["script_path"]==x["script_path"]
                   and z["script_block_ordinal"]==x["script_block_ordinal"])
            self.assertEqual(x["source_section_utf8_sha256"],
                             y["source_section_decoded_cp950_normalized_UTF8_sha256"])
            self.assertEqual(x["condition_sha256"],y["condition_expression_decoded_cp950_UTF8_sha256"])
            self.assertEqual(x["item_numeric_refs"],y["item_numeric_refs"])
            self.assertEqual(x["source_operations"],y["source_operations"])
            self.assertEqual(x["event_number"],-1)

    def test_source_conditions_not_normalized_to_real_runtime(self):
        rows=self.r["source_12_ACCEPT_literal_commands"]
        self.assertEqual(len(rows),12)
        self.assertEqual([x["GetItem"] for x in rows],
                         ["2472*4","2472*3","2472*2","2472*1",
                          "2473*4","2473*3","2473*2","2473*1",
                          "2474*4","2474*3","2474*2","2474*1"])
        self.assertEqual([x["DelItem"] for x in rows],
                         ["2469*14","2469*11","2469","2469",
                          "2470*14","2470*11","2470","2470",
                          "2471*14","2471*11","2471*8","2471*5"])
        self.assertEqual([x["EVENT"] for x in rows[0:4]],
                         ["ITEM=2469*14","ITEM=2469*11,ITEM=2469*12,ITEM=2469*13",
                          "ITEM=2469*9,ITEM=2469*8,ITEM=2469*10",
                          "ITEM=2469*7,ITEM=2469*6,ITEM=2469*5"])
        blocks=self.r["source_event_blocks"]
        for x in rows:
            y=next(z for z in blocks if z["script_path"]==x["script_path"]
                   and z["script_block_ordinal"]==x["ordinal"])
            self.assertEqual(y["raw_type"],"ACCEPT")
            self.assertEqual(y["item_numeric_refs"]["DelItem"],[int(x["DelItem"].split("*")[0])])
            self.assertEqual(y["item_numeric_refs"]["GetItem"],[int(x["GetItem"].split("*")[0])])
        self.assertTrue(self.r["original_literal_discrepancies"]["nonuniform_predicate_quantities_in_same_EVENT"])

    def test_all_nine_message_sections_and_miner_message_item(self):
        m=self.r["source_9_MESSAGE_literal_conditions"]
        self.assertEqual(len(m),9)
        self.assertEqual(sum(bool(x["GetItem"]) for x in m),1)
        miner=next(x for x in m if x["GetItem"])
        self.assertEqual((miner["script_path"],miner["EVENT"],miner["GetItem"]),
                         ("sainasu/event/nevent03_4","LV>0&ITEM!=2471","2471*1"))
        for x in m:
            y=next(z for z in self.r["source_event_blocks"]
                   if z["script_path"]==x["script_path"] and z["script_block_ordinal"]==x["ordinal"])
            self.assertEqual(y["raw_type"],"MESSAGE")
            self.assertEqual(y["item_numeric_refs"].get("GetItem",[]),
                             [int(x["GetItem"].split("*")[0])] if x["GetItem"] else [])

    def test_three_MAP09_original_candidate_floors_not_rerendered(self):
        expected={10603:"d64a87ebf4cc461c1a56ead3f268ef880a896aee1f0d85bd55096fcc5d5331f3",
                  10605:"741f997623686ce19954f59f3e4b20d15b050f70ceb54ac3559d65814ba4f5bd",
                  1212:"783821fd2ad52da3c4daed94f6fcbb8c2996b1c72ddcf189071d01710c573503"}
        self.assertEqual(set(self.r["source_map_candidates"]),set(map(str,expected)))
        for fid,sha in expected.items():
            ours=self.r["source_map_candidates"][str(fid)]
            upstream=self.sources["map09"]["maps"][str(fid)]
            self.assertEqual((ours["source_sha256"],ours["source_bytes"],ours["geometry"]),
                             (upstream["source_sha256"],upstream["source_bytes"],upstream["geometry"]))
            self.assertEqual(ours["source_sha256"],sha)
            self.assertFalse(ours["original_DAT_reread_this_unit"])

    def test_original_item_and_image_alias_boundaries(self):
        v=self.r["item_rows"]
        self.assertEqual(v["distinct_item_ids"],[2469,2470,2471,2472,2473,2474])
        rows=v["ore_to_certificate"]
        self.assertEqual([(x["ore"],x["certificate"],x["ore_alias"],x["certificate_alias"]) for x in rows],
                         [(2469,2472,14659,24222),(2470,2473,14607,24222),
                          (2471,2474,13443,24222)])
        for x in rows:
            self.assertEqual(len(x["ore_original_row_sha256"]),64)
            self.assertEqual(len(x["certificate_original_row_sha256"]),64)
        arts=v["tw1_retail_original_image_candidates"]
        self.assertEqual([x["alias"] for x in arts],[14659,14607,13443,24222])
        self.assertEqual([x["dimensions"] for x in arts],[[24,23],[24,23],[28,29],[28,39]])
        self.assertEqual([x["bytes"] for x in arts],[1112,1055,1255,1438])
        self.assertTrue(all(len(x["png_sha256"])==64 for x in arts))

    def test_no_historical_runtime_or_same_build_promotion(self):
        bounds=self.r["evidence_limits"]
        for k in ("native_original_game_running","original_server_branch_priority_observed",
                  "original_mining_quest_execution_observed","original_DelItem_quantity_semantics_verified",
                  "actual_original_item_award_or_redemption_verified",
                  "original_same_build_TW1_and_mixed25_proven","official_early_first_release_origin_proven",
                  "source_original_DIALOGUE_or_pixels_public","original_game_completion_proven"):
            self.assertFalse(bounds[k],k)
        self.assertEqual(bounds["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(bounds["stage_B"],"GATED")
        self.assertIsNone(bounds["overall_percent"])

if __name__=="__main__":
    unittest.main()
