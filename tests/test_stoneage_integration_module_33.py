"""INTEGRATION33: original Sainasu chains, with exact negative evidence boundaries."""
from hashlib import sha1
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/recovered/STONEAGE-INTEGRATION33-SAINASU-TWO-QUEST-CHAINS-SOURCE-R1.json"

def blob(x):
    return sha1(b"blob "+str(len(x)).encode()+bytes([0])+x).hexdigest()

class Integration33(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_text(encoding="utf-8"))
        cls.sources={}
        for k,v in cls.r["upstream"].items():
            x=(ROOT/v["path"]).read_bytes()
            assert blob(x)==v["git_blob"],k
            cls.sources[k]=json.loads(x)

    def test_full_original_current_and_custody_without_private_publication(self):
        p=self.r["preserved_CURRENT"]
        self.assertEqual((p["bytes"],p["git_blob"]),(2709173,"c89e0e33537990aa2132b47c40fef49a985a935c"))
        raw=(ROOT/"docs/CURRENT-STATE.md").read_bytes()
        self.assertGreaterEqual(len(raw),p["bytes"])
        self.assertEqual(blob(raw[:p["bytes"]]),p["git_blob"])
        z=self.r["private_source_archives"]
        self.assertEqual([(z[k]["bytes"],z[k]["members"]) for k in ("npc","item","dat1100")],
                         [(995176,2205),(5868386,838),(5759006,314)])
        self.assertTrue(all(x["member_CRC_all_pass"] for x in z.values()))

    def test_six_genuine_original_members_match_existing_quest01_index(self):
        c=self.sources["catalog"]
        files=self.r["original_raw_source_members"]
        self.assertEqual(len(files),6)
        scripts={x["path"]:x for x in c["source_scripts"]}
        for row in files:
            self.assertEqual(len(row["sha256"]),64)
            self.assertEqual(len(row["crc32"]),8)
            if not row["path"].endswith(".create"):
                old=scripts[row["path"]]
                self.assertEqual((row["bytes"],row["sha256"],row["crc32"]),
                                 (old["original_size"],old["original_sha256"],old["original_crc32"]))
        creates=self.r["original_CREATE_blocks"]
        self.assertEqual([(x["floor"],x["xy"],x["graphic_alias"]) for x in creates],
                         [(1112,[16,15],16000),(1100,[86,99],16048),
                          (11006,[11,11],16024),(11006,[11,7],16046)])
        for row in creates:
            v=next(x for x in c["source_creation_references"]
                   if x["create_source_path"]==row["create_path"]
                   and x["create_brace_ordinal"]==row["ordinal"])
            self.assertEqual((v["floorid"],v["graphic_alias_numeric"],v["original_script_path"]),
                             (row["floor"],row["graphic_alias"],row["script_path"]))
            self.assertEqual(v["create_source_sha"],next(x["sha256"] for x in files if x["path"]==row["create_path"]))
            self.assertEqual(v["original_script_sha"],next(x["sha256"] for x in files if x["path"]==row["script_path"]))

    def test_thirteen_source_sections_and_their_branch_distinctions(self):
        c=self.sources["catalog"]; sections=self.r["source_event_sections"]
        self.assertEqual(len(sections),13)
        self.assertEqual([sum(x["path"]==p for x in sections) for p in
                         ("sainasu/event/event13_1","sainasu/event/event13_2",
                          "sainasu/event/event15_1","sainasu/event/event15_2")],[4,1,7,1])
        for row in sections:
            s=next(x for x in c["source_event_blocks"]
                   if x["script_path"]==row["path"] and x["script_block_ordinal"]==row["ordinal"])
            self.assertEqual((s["source_section_decoded_cp950_normalized_UTF8_sha256"],s["event_number"],s["raw_type"]),
                             (row["utf8_section_sha256"],int(row["fields"]["EventNo"]),row["fields"]["TYPE"]))
        e13=[x for x in sections if x["path"]=="sainasu/event/event13_1"]
        self.assertEqual(e13[0]["fields"]["DelItem"],"2428,2429,2430,2431")
        self.assertEqual(e13[0]["fields"]["GetItem"],"2450")
        self.assertEqual(e13[1]["fields"]["GetItem"],"2431")
        self.assertEqual(e13[2]["fields"]["EVENT"],"LV>15")
        young=next(x for x in sections if x["path"].endswith("event13_2"))
        self.assertEqual(young["fields"]["CleanFlg"],"13")
        e15=[x for x in sections if x["path"]=="sainasu/event/event15_1"]
        self.assertEqual(e15[0]["fields"]["EVENT"],"NOWEV=15&PET>14-74")
        self.assertEqual(e15[0]["fields"]["GetRandItem"],"1350,1351,1352,1354,700,1455,1102,1122")
        self.assertEqual(e15[1]["fields"]["EVENT"],"ENDEV=15&NOWEV=16&PET>29-191")
        self.assertEqual(e15[1]["fields"]["GetPet"],"95")
        self.assertEqual(e15[1]["fields"]["DelPet"],"PET>29-191*1")
        self.assertNotEqual(e15[0]["fields"]["EVENT"],e15[1]["fields"]["EVENT"])

    def test_not_duplicate_quest08_to_31_specialized_scripts(self):
        from tools.stoneage_quest32_module_audit import SPECS, REC
        selected=set()
        for q,name,field in SPECS:
            obj=json.loads((ROOT/REC/("STONEAGE-QUEST"+q+"-"+name+"-R1.json")).read_text(encoding="utf-8"))
            for row in ([obj[field]] if field=="source_script" else obj[field]):
                selected.add(row["path"])
        own={x["path"] for x in self.r["original_raw_source_members"] if not x["path"].endswith(".create")}
        self.assertTrue(own.isdisjoint(selected))
        self.assertEqual(len(selected),235)
        self.assertTrue(own.issubset({x["path"] for x in self.sources["catalog"]["source_scripts"]}))
        self.assertTrue(self.r["prior_scope_dedupe"]["event15_1_GetPet95_previously_known_in_I05"])

    def test_three_sourced_maps_no_old_map09_repaint(self):
        m=self.sources["map09"]["maps"]
        own=self.r["three_map_qualifications"]
        for f in ("1112","11006"):
            self.assertEqual(own[f]["DAT_sha256"],m[f]["source_sha256"])
            self.assertEqual(own[f]["geometry"],m[f]["geometry"])
            self.assertEqual(own[f]["original_candidate_RGBA"],m[f]["frame_RGBA_sha256"]["combined"])
            self.assertEqual(own[f]["from"],"MAP09_PREVIOUSLY_VERIFIED_NO_NEW_PIXEL_REPLAY")
        r1100=next(x for x in self.sources["i10"]["recovered_DAT"] if x["floor"]==1100)
        self.assertEqual((own["1100"]["DAT_sha256"],own["1100"]["geometry"]),
                         (r1100["sha256"],[r1100["width"],r1100["height"]]))
        self.assertEqual(own["1100"]["three_original_u16_at_NPC"],[172,28,49152])
        self.assertIsNone(m.get("1100"))

    def test_existing_GetPet95_and_pet_template_variant_not_merged(self):
        prior=[x for x in self.sources["priorGetPet"]["rows"]
               if x["source_script_path"]=="sainasu/event/event15_1"]
        self.assertEqual(len(prior),1)
        self.assertEqual(prior[0]["original_GetPet_numeric_literals_ordered"],[95])
        own=self.r["same_community_RAR_PET10_numeric_candidate"]
        self.assertEqual(own["original_script_GetPet_literal"],"95")
        p=self.sources["pet10"]["source_rows"]
        self.assertEqual(own["PET10_primary_template_ID95"],next(x for x in p["enemybase.txt"] if x[1]==95))
        self.assertEqual(own["PET10_alternative_template_ID95"],next(x for x in p["enemybase2.txt"] if x[1]==95))
        self.assertEqual(own["community_spr_index_source_record"],
                         next(x for x in p["spradrn_5.bin"] if x[1]==100394))
        self.assertEqual((own["PET10_primary_template_ID95"][2],
                          own["PET10_alternative_template_ID95"][2]),(100394,100394))
        self.assertNotEqual(own["PET10_primary_template_ID95"][-1],
                            own["PET10_alternative_template_ID95"][-1])
        self.assertFalse(own["native_GetPet_95_lookup_or_grant_verified"])

    def test_thirteen_quest_item_source_rows_are_not_native_inventory_proof(self):
        rows=self.r["item_bridge"]["exact_original_item_ids"]
        self.assertEqual(len(rows),13)
        self.assertEqual([x["id"] for x in rows],
                         [700,1102,1122,1350,1351,1352,1354,1455,2428,2429,2430,2431,2450])
        self.assertEqual(self.r["item_bridge"]["TW1_retail_bitmap_aliases_distinct"],13)
        self.assertTrue(all(x["identical_original_94col_rows_in_two_community_tables"] for x in rows))
        self.assertTrue(all(x["TW1_retail_crosscarrier_RD_candidate_only"] for x in rows))
        self.assertTrue(all(len(x["row_sha256"])==64 for x in rows))
        self.assertTrue(self.r["item_bridge"]["not_the_same_client_server_deployment"])

    def test_original_game_and_early_version_boundaries(self):
        b=self.r["scope_boundaries"]
        for k in ("native_client_or_server_executed","original_quest_completed",
                  "native_level_predicate_parser_verified","pet_species_identity_same_deployment_verified",
                  "branch_priority_or_probability_verified","GetPet_actual_grant_verified",
                  "original_native_palette_or_animation_verified",
                  "copyrighted_original_dialogue_or_bitmap_published"):
            self.assertFalse(b[k],k)
        self.assertEqual((b["stage_A"],b["stage_B_and_wiki"],b["R79"],b["overall_percent"]),
                         ("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None))

if __name__=="__main__":
    unittest.main()
