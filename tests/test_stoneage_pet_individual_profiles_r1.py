"""Original-PC pet per-profile progress: index counts and fields must be source-grounded."""
import hashlib
import json
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research" / "recovered"
P = ROOT / "research" / "pets"
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))
def git_blob(path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\x00"+b).hexdigest()

class PETIndividualProfilesR1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tw=read(R/"STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.motion=read(R/"STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json")
        cls.cross=read(R/"STONEAGE-PET126W-TW10-CN50-ALL-124-ORIGINAL-PC-NAME-VARIANTS-R1.json")
        cls.profile=read(P/"profiles/TW10-G100250-WULI.json")
        cls.progress=read(P/"PET-PROGRESS-R1.json")

    def test_source_scope_counts_no_cross_version_addition(self):
        names=self.tw["records"]; motion={x["graphic"]:x for x in self.motion["groups"]}
        self.assertEqual(len(names),124)
        self.assertEqual(len(self.cross["records"]),124)
        self.assertEqual(len(set(x["graphic_number"] for x in names)),124)
        self.assertEqual(sum(bool(x.get("portrait_rd")) for x in names),120)
        self.assertTrue(all(x["graphic_number"] in motion for x in names))
        self.assertTrue(all(motion[x["graphic_number"]]["fully_observable_sequences"]==motion[x["graphic_number"]]["source_sequences"] for x in names))
        expected=(self.progress["source_scope_counts"])
        self.assertEqual((expected["tw10_original_client_named_album_candidates"],expected["tw10_named_with_spr_source_actions"],expected["tw10_named_with_portrait_rd"],expected["tw10_named_missing_portrait_rd"]),(124,124,120,4))
        self.assertEqual(expected["cn50_preserved_compiled_named_slots_independent_nonadditive"],305)
        c=self.progress["per_pet_profile_counts"]
        self.assertEqual((c["source_indexed_candidate_rows"],c["individual_detailed_profiles"],c["individual_detailed_partial_profiles"],c["fully_historically_verified_pet_profiles"],c["individual_profiles_not_yet_created_for_candidates"]),(124,1,1,0,123))
        self.assertIsNone(self.progress["boundaries"]["all_pet_species_historical_total"])

    def test_wuli_original_client_source_and_no_official_id_promotions(self):
        p=self.profile
        w=next(x for x in self.tw["records"] if x["graphic_number"]==100250)
        m=next(x for x in self.motion["groups"] if x["graphic"]==100250)
        self.assertEqual(p["profile_id"],"TW10-G100250")
        self.assertEqual(p["names"]["original_client"],w["name_as_written"])
        self.assertEqual(p["names"]["local_name_row_sha256"],w["source_row_sha256"])
        self.assertEqual(p["appearance"]["graphic_number"],w["graphic_number"])
        self.assertEqual(p["appearance"]["spr_group_index"],w["spr_group_index"])
        self.assertEqual(p["appearance"]["full_original_spr_segment_sha256"],w["spr_original_segment_sha256"])
        self.assertEqual(p["appearance"]["portrait"]["source_rd_bitmap_number"],w["portrait_rd"]["bitmap_number"])
        self.assertEqual(p["appearance"]["portrait"]["source_rd_sha256"],w["portrait_rd"]["sha256"])
        a=p["appearance"]["action_sequences"]
        self.assertEqual((a["source_sequences"],a["source_frame_positions"],a["source_distinct_bitmap_numbers"],a["fully_observable_sequences"]), (m["source_sequences"],m["frame_positions"],m["distinct_bitmaps"],m["fully_observable_sequences"]))
        self.assertEqual(a["source_action_codes"],m["source_actions"])
        self.assertEqual(a["source_directions"],m["source_directions"])
        self.assertFalse(p["actual_official_pet_identity"]["official_living_pet_release_proven"])
        self.assertIsNone(p["actual_official_pet_identity"]["source_pet_id"])
        self.assertEqual(p["appearance"]["original_asset_type"],"2D_SPR_BITMAP_NOT_3D_MODEL")
        self.assertFalse(a["offline_preview_is_game_native_execution"])

    def test_all_requested_unknowns_are_null_not_guessed(self):
        p=self.profile
        self.assertEqual(p["combat_stats"]["status"],"OPEN_NOT_PROVEN")
        for scope in ("level_1","initial_stat_ranges"):
            self.assertEqual(p["combat_stats"][scope]["status"],"OPEN_NOT_PROVEN")
        for v in p["combat_stats"]["level_1"]["values"].values():
            self.assertIsNone(v)
        for bound in ("minimum","maximum"):
            for v in p["combat_stats"]["initial_stat_ranges"][bound].values():
                self.assertIsNone(v)
        for v in p["combat_stats"]["elements"].values():self.assertIsNone(v)
        for family in ("growth","skills","acquisition","pet_systems"):
            self.assertEqual(p[family]["status"],"OPEN_NOT_PROVEN")
        self.assertIsNone(p["skills"]["innate_at_acquisition"])
        self.assertIsNone(p["acquisition"]["original_capture"]["map_name"])
        self.assertIsNone(p["acquisition"]["original_capture"]["coordinates"])
        self.assertIsNone(p["growth"]["stat_growth_formula"])
        self.assertFalse(p["status"]["all_fields_historically_complete"])
        self.assertTrue(p["status"]["other_modules_locked"])
        self.assertIsNone(p["status"]["overall_project_completion_percent"])

    def test_source_blobs_and_browseable_index_are_consistent(self):
        p=self.profile
        for source in p["provenance"]["sources"]:
            self.assertEqual(source["git_blob"],git_blob(ROOT/source["path"]))
        self.assertEqual(p["provenance"]["source_archive_sha256"],self.tw["archive"]["sha256"])
        self.assertEqual(p["provenance"]["original_exe_sha256"],self.tw["archive"]["files"]["source/sa_3.exe"]["sha256"])
        self.assertEqual(git_blob(ROOT/"docs/CURRENT-STATE.md"),self.progress["boundaries"]["current_state_immutable_blob"])
        ix=(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8")
        rows=re.findall(r"^\| (\d+) \| (.*?) \| (.*?) \| (\d+) \| (.*?) \| 已验源 \| (.*?) \|$",ix,re.M)
        self.assertEqual(len(rows),124)
        for i,(order,name,cn,graphic,portrait,detail) in enumerate(rows):
            src=self.tw["records"][i];s=self.cross["records"][i]
            self.assertEqual((int(order),name,cn,int(graphic)),(i+1,src["name_as_written"],s["cn50_preserved_compiled_literal"],src["graphic_number"]))
            self.assertEqual(portrait,"已定位" if src["portrait_rd"] else "待补")
            self.assertEqual("查看乌力档案" in detail,src["graphic_number"]==100250)
        self.assertEqual(ix.count("| 已验源 |"),124)

if __name__=="__main__":unittest.main()
