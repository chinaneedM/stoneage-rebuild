"""SCENE26-R2: source-limited fourth original tutor room, no private bytes in CI."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"research/recovered/STONEAGE-SCENE26-R2-FOUR-ORIGINAL-PET-TUTOR-ROOMS-SOURCE-R1.json"

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()

def verify(j,up):
    assert j["schema"]=="stoneage.scene26.r2.four_tutor_original_DAT_source_bounded_visual_observer.r1"
    assert j["baseline_main_head"]=="38f489e57d4e460803f5d9e4d03f9001e4d4eea9"
    assert j["original_historical_CURRENT_blob_preserved"]=="c89e0e33537990aa2132b47c40fef49a985a935c"
    a,b,c=up["scene26"],up["map09"],up["quest05"]
    old={x["source_original_floorid"]:x for x in a["rows"]}
    cross={(x["source_floor_id"],x["source_CREATE_block_ordinal"]):x for x in c["source_CREATE_references"] if x["source_CREATE_file"]=="sa60/newbie/newbie.create"}
    rows=j["source_tutor_four_CREATE_rows"]
    assert len(rows)==4 and {x["source_floor_id"] for x in rows}=={1003,2003,3003,4003}
    for row in rows:
        floor=row["source_floor_id"];src=old[floor];q=cross[(floor,row["source_CREATE_ordinal"])]
        assert row["source_CREATE_ordinal"]==src["original_CREATE_block_ordinal"]
        assert row["original_borncenter"]==src["source_original_borncenter"]
        assert row["original_source_graphicname"]==src["source_original_graphicname"]==q["source_graphic_alias"]
        assert row["original_DAT_whole_sha256"]==src["original_qualified_DAT_sha256"]==q["source_DAT_sha256"]
        assert row["original_DAT_bytes"]==src["original_qualified_DAT_bytes"]==q["source_DAT_bytes"]==5408
        assert row["original_script_sha256"]==src["source_original_script_sha256"]==q["source_parameter_sha256"]
        assert row["original_source_label"]==src["source_original_CP950_comment_label"]
        assert row["original_directions"]==src["source_original_dir"]==4
        assert row["native_NPC_sprite_of_source_graphicname_rendered"] is False
        assert row["original_official_same_deployment_proven"] is False
        assert row["private_qualified_visual_present"] is True
        assert row["newly_replayed_in_SCENE26_R2"]==(floor==4003)
        assert row["original_DAT_three_u16_words_at_original_borncenter"]==([5002,12802,49152] if floor==4003 else src["original_DAT_raw_three_u16_words_at_borncenter"])
        assert row["modern_marker_xy"]==([1008,784] if floor==4003 else src["modern_isometric_observer_marker_xy"])
    floor4003=old[4003];v=j["newly_source_replayed_fourth_room"];m=b["maps"]["4003"]
    assert v["source_floor"]==4003
    assert v["original_DAT_sha256"]==m["source_sha256"]==floor4003["original_qualified_DAT_sha256"]==cross[(4003,7)]["source_DAT_sha256"]
    assert v["original_DAT_bytes"]==m["source_bytes"]==5408
    assert v["original_DAT_geometry"]==m["geometry"]==[30,30]
    assert v["original_DAT_three_u16_words_at_borncenter"]==[5002,12802,49152]
    assert v["source_original_borncenter"]==[14,17]
    assert v["source_graphic_alias"]==16122
    assert v["actual_original_RD_candidate_aliases_used"]==m["unique_draw_aliases"]==45
    assert v["original_source_canvas_draw_positions"]==m["draw_positions"]==143
    assert v["source_qualified_MAP09_frame_RGBA_sha256"]==m["frame_RGBA_sha256"]
    assert v["private_numpy_Pillow_independent_composite_full_RGBA_SHA256"]==m["frame_RGBA_sha256"]["combined"]
    assert v["modern_candidate_canvas_pixels"]==m["canvas_size"]==[1889,1425]
    assert v["candidate_origin_xy"]==m["origin"]==[16,712]
    x,y=v["source_original_borncenter"]
    assert v["modern_coordinate_marker_xy"]==[16+(x+y)*32,712+(y-x)*24]==[1008,784]
    assert v["source_pixel_ref_is_original_TW10_retail_under_cross_carrier_qualification"] is True
    assert v["actual_original_same_deployment_TW10_MAP09_NPC_scripts_proven"] is False
    carrier=j["original_carrier_context"]
    assert carrier["source_era"]=="LATER_COMMUNITY_MIXED25_NPC_AND_DAT_SEPARATE_TW10_ORIGINAL_CLIENT_RD"
    assert carrier["map09_private_source_archive_sha256"]=="d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a"
    assert carrier["map09_original_955_DAT_zip_sha256"]==b["original_DAT_archive"]["sha256"]
    assert carrier["map09_original_955_DAT_zip_bytes"]==b["original_DAT_archive"]["bytes"]
    assert carrier["map09_original_955_DAT_members"]==b["original_DAT_archive"]["members"]==955
    assert carrier["private_prior_scene26_zip_sha256"]==a["private_delivery"]["ZIP_sha256"]
    assert carrier["original_CREATE_sha256"]==floor4003["source_original_CREATE_whole_file_sha256"]
    assert carrier["original_petmaster_sha256"]==floor4003["source_original_script_sha256"]
    private=j["private_four_room_delivery"]
    assert private["zip_bytes"]==2532646 and private["zip_members"]==11
    assert private["zip_sha256"]=="cf7d0d6dbb34fc77e64740f2d4990a0012a15a347bfb683e3cd1dc97eb02ca4c"
    assert private["preview_bytes"]==222802 and private["preview_sha256"]=="c149529a610e08fb044b648926fd7a3076cb9c5202196d4ca051b2b3366013ad"
    assert all(private[k] for k in ("zip_all_CRC_passed","read_back_whole_ZIP_and_JPG_sha256_verified","source_NPC_original_scripts_and_4003_original_DAT_only_private","source_4003_tiles_derivative_and_4_room_previews_only_private"))
    s=j["summary"]
    assert (s["four_original_source_NPC_CREATE_refs"],s["prior_privately_completed_rooms"],s["newly_replayed_original_DAT_rooms"],s["privately_observable_original_room_candidates_now"])==(4,3,1,4)
    assert (s["newly_original_DATA_downloaded_this_work"],s["newly_original_RD_decompressions"])==(0,0)
    assert s["new_standalone_source_data_interpretation_at_4003_coordinate"] is True
    for k in ("original_NPC_16122_16127_actual_pixels_rendered","original_client_or_server_NPC_interaction_observed","first_JSS1999_or_Chinese_182_early_official_version_proven","native_in_game_render_order_collision_palette_or_pixel_drawer_verified","proprietary_source_files_in_Git"):
        assert s[k] is False,k
    assert (s["stage_A"],s["stage_B_wiki"],s["R79"],s["overall_percent"])==("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING",None)

class Scene26R2FourRooms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(TARGET.read_text(encoding="utf-8"))
        cls.up={}
        for name,pin in cls.report["public_immutable_upstream"].items():
            blob=(ROOT/pin["path"]).read_bytes()
            assert git_blob(blob)==pin["git_blob_sha"],name
            cls.up[name]=json.loads(blob)
    def test_original_four_source_join(self):
        verify(self.report,self.up)
    def mutate(self,fn):
        j=deepcopy(self.report);fn(j)
        with self.assertRaises((AssertionError,KeyError,TypeError)):
            verify(j,self.up)
    def test_reject_imaginary_fourth_DAT(self):
        self.mutate(lambda j:j["newly_source_replayed_fourth_room"].__setitem__("original_DAT_sha256","0"*64))
    def test_reject_wrong_original_coordinate(self):
        self.mutate(lambda j:j["newly_source_replayed_fourth_room"]["source_original_borncenter"].__setitem__(0,19))
    def test_reject_wrong_original_4003_cell_words(self):
        self.mutate(lambda j:j["newly_source_replayed_fourth_room"]["original_DAT_three_u16_words_at_borncenter"].__setitem__(1,0))
    def test_reject_fake_pixel_digest(self):
        self.mutate(lambda j:j["newly_source_replayed_fourth_room"].__setitem__("private_numpy_Pillow_independent_composite_full_RGBA_SHA256","f"*64))
    def test_reject_wrong_NPC_graphic_alias(self):
        self.mutate(lambda j:j["source_tutor_four_CREATE_rows"][3].__setitem__("original_source_graphicname",16127))
    def test_reject_claimed_old_official_same_build(self):
        self.mutate(lambda j:j["summary"].__setitem__("first_JSS1999_or_Chinese_182_early_official_version_proven",True))
    def test_reject_claimed_native_NPC_sprite(self):
        self.mutate(lambda j:j["summary"].__setitem__("original_NPC_16122_16127_actual_pixels_rendered",True))
    def test_reject_unearned_original_gameplay(self):
        self.mutate(lambda j:j["summary"].__setitem__("original_client_or_server_NPC_interaction_observed",True))
if __name__=="__main__":
    unittest.main()
