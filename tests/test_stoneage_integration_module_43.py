"""Source-only regression for Jaruga route A6 and finish. No private bytes required."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "recovered"

def source(name):
    payload = (DATA / name).read_bytes()
    digest = hashlib.sha1(b"blob " + str(len(payload)).encode("ascii") + bytes([0]) + payload).hexdigest()
    return json.loads(payload), digest

class JarugaIntegration43Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new, _ = source("STONEAGE-INTEGRATION43-JARUGA-A6-FINISH-SOURCE-BOUNDARY-R1.json")
        cls.q, cls.qsha = source("STONEAGE-QUEST25-FOUR-ISLAND-TOUR-ROUTES-SOURCE-R1.json")
        cls.i41, cls.i41sha = source("STONEAGE-INTEGRATION41-JARUGA-ROUTE-B-CHECKPOINTS-SOURCE-R1.json")
        cls.i42, cls.i42sha = source("STONEAGE-INTEGRATION42-JARUGA-REGISTRATION-ORIGINAL-TILES-R1.json")
        cls.a = next(r for r in cls.q["routes"] if r["label"] == "A")

    def test_precise_git_inputs(self):
        self.assertEqual(self.new["source_git_blobs"], {
            "quest25":self.qsha,"integration41":self.i41sha,"integration42":self.i42sha})
        self.assertEqual(self.new["preserved_CURRENT"], {
            "bytes":2709173,"git_blob":"c89e0e33537990aa2132b47c40fef49a985a935c","modified":False})

    def test_original_four_members_and_no_new_script(self):
        manifest = self.new["private_four_source_members"]
        self.assertEqual({x["path"] for x in manifest}, {
            "jaruga/event/oev.create","jaruga/event/event.template",
            "jaruga/event/oev_6","jaruga/event/oev_ed1"})
        for row in manifest:
            self.assertIn(row, self.q["source_manifest"])
        self.assertEqual([x["members"] for x in self.new["private_archive_recheck"]],[173,413,23])
        self.assertTrue(all(x["member_CRC_all_valid"] for x in self.new["private_archive_recheck"]))
        self.assertEqual(self.new["status"]["new_original_script_discoveries"],0)

    def test_4000_identity_and_earlier_not_new_replay(self):
        m = next(x for x in self.q["source_map_metadata_reused"] if x["source_floor_id"]==4000)
        cross = next(x for x in self.i42["reuse_scan"]["matching_floors"] if x["floor"]==4000)
        current=self.new["map4000"]
        self.assertEqual(current["historical_source_sha256"],m["source_DAT_sha256"])
        self.assertEqual(current["historical_source_sha256"],cross["DAT_sha256"])
        self.assertEqual(current["prior_I42_reused_alias_occurrences"],cross["references"])
        self.assertEqual(current["prior_I42_full_map_preflight"]["high_value_references"],8603)
        self.assertEqual(current["prior_I42_full_map_preflight"]["unqualified_occurrences"],4)
        self.assertEqual(current["prior_I42_full_map_preflight"]["unqualified_aliases"],[22356,22413,22434])
        for name in ["current_original_DAT_bytes_read","current_original_RD_bytes_decoded","current_original_4000_canvas_rendered"]:
            self.assertIs(current[name],False)

    def test_A6_exact_create_script_and_item_exchange(self):
        old = next(x for x in self.a["checkpoints"] if x["number"]==6)
        new=self.new["sites"][0]
        self.assertEqual((new["name"],new["floor"],new["original_xy"],new["source_graphic_alias"]),
                         ("A6",4000,[63,66],16068))
        self.assertEqual(new["source_create"],{
            "path":old["source"]["create_path"],"ordinal":old["source"]["create_ordinal"],
            "sha256":old["source"]["block_sha256"]})
        self.assertEqual(new["original_exchange"],{
            "required_item":old["incoming_item"],"received_item":old["outgoing_item"],
            "condition":old["condition_literal"]})
        self.assertEqual((new["original_exchange"]["required_item"],new["original_exchange"]["received_item"]),(2557,2558))
        self.assertEqual(new["script"]["events"][0]["commands"],{"GetItem":["2558"],"DelItem":["2557"]})
        self.assertEqual((new["prior_window_high_refs"],new["prior_11x11_window"]),(131,[58,61,68,71]))

    def test_finish_original_reward_source(self):
        old=self.a["finish"];new=self.new["sites"][1]
        self.assertEqual((new["name"],new["floor"],new["original_xy"],new["source_graphic_alias"]),("A_finish",4000,[54,47],16027))
        self.assertEqual(new["source_create"],{
            "path":old["create_path"],"ordinal":old["create_ordinal"],"sha256":old["block_sha256"]})
        self.assertEqual(new["original_finish_proof_item"],self.a["final_proof_item"])
        self.assertEqual(new["original_finish_proof_item"],2564)
        commands=new["script"]["events"][0]["commands"]
        self.assertEqual(commands["DelItem"],["2564"])
        self.assertEqual(commands["GetPet"],["358,96,328,309,365"])
        self.assertEqual(commands["GetRandItem"],["254,351,770,1061,1062,69,59,269,2565,2566"])
        self.assertEqual((new["prior_window_high_refs"],new["prior_11x11_window"]),(139,[49,42,59,52]))

    def test_all_twelve_source_sections_are_reproducible(self):
        old_scripts={x["path"]:x for x in self.q["source_scripts"]}
        for new in self.new["sites"]:
            s=new["script"];old=old_scripts[s["path"]]
            for key in ["path","sha256","bytes","crc32"]:
                self.assertEqual(s[key],old[key])
            self.assertEqual(len(s["events"]),6)
            self.assertEqual(s["events"],[
                {key:ev[key] for key in
                 ["ordinal","type","condition_literal","condition_sha256","section_sha256","commands"]}
                for ev in old["events"]])
            self.assertEqual(new["source_functionset"],"ExChangeMan")
            self.assertEqual(new["source_template"],"jaruga/event/event.template")

    def test_cross_build_original_image_does_not_prove_same_deployment(self):
        actual=self.new["cross_source_TW1_image_for_16027"]
        original=self.i41["separate_NPC_image_candidates"]["16027"]
        for field in ["PNG_sha256","RD_sha256","width","height","physical_bitmap"]:
            self.assertEqual(actual[field],original[field])
        self.assertFalse(actual["same_official_deployment"])
        self.assertFalse(self.new["cross_source_TW1_image_for_16068"]["same_official_deployment"])
        g=self.new["negative_gates"]
        self.assertFalse(g["same_number_physical_bitmap_substitutes_logical_22413"])
        self.assertFalse(g["original_layer_palette_collision_dialogue_or_reward_execution"])
        self.assertEqual(g["A6_duplicate_LV_item_condition"],"UNKNOWN_NATIVE_BRANCH_PRIORITY")
        self.assertEqual(g["finish_overlap_ENDEV2"],"UNKNOWN_NATIVE_BRANCH_PRIORITY")

    def test_no_premature_stageB_or_progress_claim(self):
        scope=self.new["status"]
        self.assertEqual(scope["scope"],"SOURCE_BOUNDED_PARTIAL")
        self.assertEqual((scope["new_original_RD_decodes"],scope["new_4000_scene_pixels"]),(0,0))
        self.assertEqual(scope["stage_A"],{"PARTIAL":7,"OPEN":2})
        self.assertEqual(scope["stage_B"],"GATED")
        self.assertEqual(scope["wiki"],"GATED")
        self.assertEqual(scope["R79"],"PAUSED_NON_BLOCKING")
        self.assertIsNone(scope["overall_percent"])

if __name__ == "__main__":
    unittest.main()
