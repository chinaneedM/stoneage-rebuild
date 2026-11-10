"""INTEGRATION46 public source relationship, hashes and negative-boundary guards.

CI holds no proprietary DAT, RD, sprite PNG, NPC original dialogue or game client.
"""
import copy
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]/"research"/"recovered"

def read(name):
    raw=(ROOT/name).read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()
    return json.loads(raw),blob

class A12OriginalSourceWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r,_=read("STONEAGE-INTEGRATION46-JARUGA-A12-ORIGINAL-DAT-AND-PIXEL-SOURCE-R1.json")
        cls.i10,cls.i10blob=read("STONEAGE-INTEGRATION10-TWELVE-RECOVERED-DAT-SEVEN-CHECKPOINT-SCENES-R1.json")
        cls.quest,cls.questblob=read("STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json")
        cls.i45,cls.i45blob=read("STONEAGE-INTEGRATION45-JARUGA-A3-A7-A11-ORIGINAL-SOURCE-SCENES-R1.json")
        cls.map04,cls.map04blob=read("STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json")
        cls.route=next(x for x in cls.quest["routes"] if x["label"]=="A")
        cls.a12=next(x for x in cls.route["checkpoints"] if x["number"]==12)

    def test_source_git_blob_provenance_and_immutable_current(self):
        self.assertEqual(self.r["source_git_blob_refs"],{
            "I10":self.i10blob,"QUEST25":self.questblob,"I45":self.i45blob,"MAP04":self.map04blob})
        self.assertEqual(self.r["historical_CURRENT_preserved"],{
            "bytes":2709173,"blob":"c89e0e33537990aa2132b47c40fef49a985a935c","modified":False})

    def test_original_DAT3400_exact_sha_dimensions_and_prior_error_kept(self):
        d=self.r["A12_DAT"]
        old=next(x for x in self.i10["recovered_DAT"] if x["floor"]==3400)
        self.assertEqual((d["floor"],d["sha256"],d["bytes"],d["width"],d["height"]),
                         (old["floor"],old["sha256"],old["bytes"],old["width"],old["height"]))
        self.assertEqual((d["bytes"],d["width"],d["height"]),(86408,120,120))
        self.assertEqual(d["sha256"],"a3c6918ba21c909e6312329c936615aa6b6d8800d7967ed85a2146d55ca263c4")
        self.assertEqual(d["original_RAR_partial_read_error_prior"],old["old_read_error"])
        self.assertTrue(d["error_not_erased"])
        self.assertEqual(self.r["actual_source_archives"][0]["sha256"],self.i10["private_archive"]["sha256"])

    def test_actual_A12_original_create_and_six_script_sections(self):
        src=self.a12["source"];n=self.r["A12_original_NPC"]
        for k,old in [
            ("create_path","create_path"),("create_ordinal","create_ordinal"),
            ("create_block_sha256","block_sha256"),("source_floor","floor"),
            ("borncorner","borncorner"),("direction","direction"),
            ("source_graphic_alias","graphic_alias"),("functionset","functionset"),
            ("template_path","template_path"),("script_path","script_path")]:
            self.assertEqual(n[k],src[old])
        self.assertEqual(n["borncorner"],[69,61,69,61])
        self.assertEqual((n["direction"],n["source_graphic_alias"]),(6,16067))
        scr=next(x for x in self.quest["source_scripts"] if x["path"]==n["script_path"])
        self.assertEqual((n["script_bytes"],n["script_sha256"]),(scr["bytes"],scr["sha256"]))
        self.assertEqual(len(n["six_original_TYPE_sections"]),6)
        self.assertEqual(n["six_original_TYPE_sections"],[
            {"ordinal":e["ordinal"],"condition_literal":e["condition_literal"],
             "section_sha256":e["section_sha256"],"commands":e["commands"]}
            for e in scr["events"]])
        self.assertEqual(n["six_original_TYPE_sections"][0]["commands"],
                         {"GetItem":["2564"],"DelItem":["2563"]})
        self.assertEqual(self.r["A12_original_NPC"]["proof_required"],2563)
        self.assertEqual(self.r["A12_original_NPC"]["proof_output_literal"],2564)
        self.assertEqual(self.r["A12_original_NPC"]["source_first_condition"],"LV>0&ITEM=2563")

    def test_exact_source_map_window_and_69_image_aliases(self):
        w=self.r["A12_window"]
        self.assertEqual((w["bounds_inclusive"],w["center"],w["original_cells"]),
                         ([64,56,74,66],[69,61],121))
        self.assertEqual(w["raw_three_u16_at_center"],[260,0,49152])
        self.assertEqual((w["high_gt99_image_occurrences"],w["distinct_source_qualified_TW1_aliases"],
                          w["low_1_to_99_occurrences"],w["unqualified_high_aliases"]),(135,69,21,0))
        self.assertEqual(w["low_numeric_histogram"],{"2":14,"27":7})
        aliases=w["qualified_aliases"]
        self.assertEqual(len(aliases),len(set(aliases)))
        self.assertEqual(len(aliases),69)
        self.assertEqual(aliases,sorted(aliases))
        map04_aliases={row[0] for row in self.map04["source_TW1_real_RD_rows"]}
        self.assertTrue(set(aliases)<=map04_aliases)
        self.assertTrue(all(i>99 for i in aliases))
        self.assertEqual((aliases[0],aliases[-1]),(147,11904))

    def test_authentic_TW1_RD16067_is_not_a_new_original_actor(self):
        actor=self.r["TW1_actor_source"]
        old=self.i45["actually_recovered_TW1_16067"]
        for new,prior in [("graphic_alias","logical_alias"),("physical_bitmap","physical_bitmap"),
                          ("ADRN_record_sha256","original_ADRN_record_sha256"),("RD_sha256","RD_sha256"),
                          ("RGBA_sha256","RGBA_sha256"),("original_REAL_offset","offset"),
                          ("RD_bytes","bytes")]:
            self.assertEqual(actor[new],old[prior])
        self.assertEqual(actor["graphic_alias"],16067)
        self.assertTrue(actor["double_decoder_pass"])
        self.assertTrue(actor["prior_INTEGRATION45_RD_bytes_identical"])
        self.assertFalse(actor["new_original_actor_RD_discovery"])

    def test_three_actual_independent_RGBA_canvases_and_real_zip_receipt(self):
        ob=self.r["actual_modern_source_images"]
        self.assertEqual((ob["canvas_size"],ob["origin"],ob["source_grid_center_canvas_xy"]),
                         ([736,769],[-3792,682],[368,490]))
        self.assertTrue(ob["Pillow_vs_NumPy_full_RGBA_identical"])
        self.assertTrue(ob["independent_second_ZIP_replay_full_RGBA_identical"])
        self.assertEqual(ob["source_compositor_RGBA_sha256"],{
            "plane0":"4ffd02f563950def8a3d9dd105db2c03b7706fd3b0a427d4fb5d9086f7ea60b9",
            "plane1":"d58097ff14ef09f8c5d2565f516ccebb71c8809f1aaf90d13c90927370f9ed8d",
            "combined":"1b8a642dc82a4c4e35d6c0bd0f52c764fba565a1f314ba80e154ff3fc459fe14"})
        self.assertTrue(ob["marker_and_actor_overlay_are_modern_only"])
        private=self.r["private_custody"]
        self.assertEqual((private["bytes"],private["members"]),(1314729,80))
        self.assertEqual(private["sha256"],"d58852205cf9fae9117d7f0dd0f721818aca5c64b8cc833f2fe4034a48a6159e")
        self.assertEqual(private["private_derived_original_cells_and_image_receipts_JSON_sha256"],
                         "39def1596a27830fd3a8a67c80d1c7f1b52e7fc797497f6b18ebc4620a3f15d6")
        self.assertTrue(private["all_member_CRC_verified"])
        self.assertTrue(private["personal_Library_upload_and_full_byte_readback_equal"])

    def test_separate_build_and_no_original_gameplay_promotion(self):
        gates=self.r["negative_evidence"]
        self.assertEqual(self.r["source_scopes"]["original_DAT_and_NPC"],
                         "PRESERVED_COMMUNITY_MIXED25_NOT_EARLY_OFFICIAL_DEPLOYMENT")
        self.assertEqual(set(gates),{
            "native_StoneAge_original_client_executed","same_official_deployed_build_proven",
            "native_palette_verified","native_layer_or_occlusion_verified",
            "native_NPC_sprite_direction_verified","native_collision_and_third_plane_semantics_verified",
            "original_NPC_dialogue_or_quest_execution_verified","official_earliest_1_82_original_behavior_proven",
            "commercial_originals_uploaded_to_public_Git","original_4000_DAT_available"})
        self.assertTrue(all(v is False for v in gates.values()))
        self.assertEqual(self.r["status"],{
            "Stage_A":{"PARTIAL":7,"OPEN":2},"Stage_B":"GATED",
            "wiki":"GATED","R79":"PAUSED_NON_BLOCKING","overall_percent":None})
        for field in gates:
            damaged=copy.deepcopy(self.r)
            damaged["negative_evidence"][field]=True
            with self.assertRaises(AssertionError):
                self.assertTrue(all(v is False for v in damaged["negative_evidence"].values()))

if __name__=="__main__":
    unittest.main()
