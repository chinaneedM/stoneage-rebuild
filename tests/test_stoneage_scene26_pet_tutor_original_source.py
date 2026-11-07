"""SCENE26: source-bounded 4 original pet-tutor CREATEs and 3 DAT/image observations.
Public checks validate derivative metadata only; original bytes stay in private Library.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research" / "recovered"
OUT = R / "STONEAGE-SCENE26-ORIGINAL-PET-TUTOR-FOUR-CREATE-THREE-SCENE-SOURCE-R1.json"


def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def load_sources(report):
    sources = {}
    for key, pin in report["public_pins"].items():
        data = (ROOT / pin["path"]).read_bytes()
        assert git_blob_sha(data) == pin["sha"], key
        sources[key] = json.loads(data)
    return sources


def verify(report, sources):
    assert report["schema"] == "stoneage.scene26.original_four_pet_tutor_CREATE_and_three_private_real_DAT_observers.r1"
    assert report["baseline_main_head"] == "c6a8aa84b3bc459f99f94fe794c17cba2d2a507e"
    assert report["original_historical_CURRENT_blob_unchanged"] == "c89e0e33537990aa2132b47c40fef49a985a935c"
    quest, m7 = sources["quest05"], sources["map07"]
    assert report["source_parent_mixed25_RAR_sha256"] == quest["source_original_mixed25_RAR_sha256"]
    source_rows = {(r["source_CREATE_file"], r["source_CREATE_block_ordinal"]): r
        for r in quest["source_CREATE_references"] if r["source_CREATE_file"] == "sa60/newbie/newbie.create"}
    original_meta = report["private_original_replay"]
    assert len(source_rows) == 8
    assert original_meta["original_CREATE_source_bytes"] == 1548
    assert original_meta["original_petmaster_original_CP950_bytes"] == 1365
    assert original_meta["original_CREATE_SHA256"] == source_rows[("sa60/newbie/newbie.create", 4)]["source_CREATE_sha256"]
    assert original_meta["original_petmaster_SHA256"] == source_rows[("sa60/newbie/newbie.create", 4)]["source_parameter_sha256"]
    assert original_meta["private_3_original_DAT_full_sha_verified_against_Q05_and_MAP07"] is True
    assert original_meta["private_original_files_byte_sha_verified_against_public_Q05"] is True
    assert original_meta["private_3_original_MAP07_combined_RGBA_checked_against_source_report"] is True
    assert original_meta["private_source_script_literal_event_type"] == "MESSAGE"
    assert original_meta["private_source_script_literal_guard"] == "LV>0"
    assert original_meta["private_script_8_numbered_window_messages_present"] is True
    assert original_meta["private_script_contains_GetPet_GetItem_DelItem_or_DelPet_literal"] is False
    assert original_meta["original_full_script_text_or_proprietary_pixels_published"] is False
    map07 = {r["floor"]: r for r in m7["maps"]}
    expected = {
        1003: (4, [19,15], 16122, "薩姆寵物店解說員", [5000,0,49152]),
        2003: (5, [11,12], 16127, "漁村寵物店解說員", [5006,0,49152]),
        3003: (6, [16,19], 16122, "加加寵物店解說員", [5000,0,49152]),
        4003: (7, [14,17], 16122, "加魯卡寵物店解說員", None),
    }
    assert len(report["rows"]) == len(expected) == 4
    actual = {r["source_original_floorid"]: r for r in report["rows"]}
    assert len(actual) == 4
    for floor, (ordinal, coord, graphic, label, raw3) in expected.items():
        r = actual[floor]
        q = source_rows[("sa60/newbie/newbie.create", ordinal)]
        assert r["original_CREATE_block_ordinal"] == ordinal
        assert r["source_original_CREATE_file"] == q["source_CREATE_file"]
        assert r["source_original_CREATE_whole_file_sha256"] == q["source_CREATE_sha256"]
        assert r["source_original_floorid"] == q["source_floor_id"] == floor
        assert r["source_original_graphicname"] == q["source_graphic_alias"] == graphic
        assert r["source_original_script_path"] == q["source_parameter_file"] == "sa60/newbie/petmaster"
        assert r["source_original_script_sha256"] == q["source_parameter_sha256"]
        assert r["source_original_borncenter"] == coord
        assert r["source_original_CP950_comment_label"] == label
        assert r["source_original_name_literal"] == "寵物常識解說員"
        assert r["source_original_dir"] == 4
        assert r["source_original_createnum"] == 1
        assert r["original_Q05_map_status"] == q["map_status"] == "MAP09_GT99_RD_SOURCE_READY_CANDIDATE"
        assert r["original_qualified_DAT_sha256"] == q["source_DAT_sha256"]
        assert r["original_qualified_DAT_bytes"] == q["source_DAT_bytes"] == 5408
        assert r["original_DAT_raw_three_u16_words_at_borncenter"] == raw3
        assert r["native_historical_NPC_position_rendered"] is False
        assert r["original_official_same_build_identity_verified"] is False
        assert r["original_source_comment_is_not_authenticated_official_village_identity"] is True
        if floor != 4003:
            assert r["this_private_source_replay_DAT_full_sha_verified"] is True
            assert r["modern_MAP07_visual_reference_present"] is True
            assert map07[floor]["source_dat_sha256"] == r["original_qualified_DAT_sha256"]
            assert map07[floor]["source_dat_bytes"] == 5408
            assert map07[floor]["independent_RGBA_canvas_verified"] is True
            x,y = coord
            assert r["modern_isometric_observer_marker_xy"] == [16+(x+y)*32, 712+(y-x)*24]
            assert len(r["modern_MAP07_original_combined_PNG_sha256"]) == 64
        else:
            assert floor not in map07  # only this private 28-map batch; Q05 DAT is qualified.
            assert r["this_private_source_replay_DAT_full_sha_verified"] is False
            assert r["modern_MAP07_visual_reference_present"] is False
            assert r["modern_isometric_observer_marker_xy"] is None
            assert r["modern_MAP07_original_combined_PNG_sha256"] is None
    assert report["summary"]["same_script_original_CREATE_refs"] == 4
    assert report["summary"]["original_qualified_DAT_955_census"] == 4
    assert report["summary"]["private_actual_DAT_byte_rechecked"] == 3
    assert report["summary"]["private_map_source_visual_present"] == 3
    assert report["summary"]["private_archive_missing_visual_floor_id"] == 4003
    assert report["summary"]["original_selected_source_graphic_numbers"] == [16122,16127]
    assert report["summary"]["source_original_quest_ORIGIN"] == "ORIGIN_UNRESOLVED"
    assert report["private_delivery"]["ZIP_bytes"] == 3275768
    assert report["private_delivery"]["ZIP_members"] == 12
    assert report["private_delivery"]["saved_and_retrieved_full_sha_and_members_CRC_verified"] is True
    assert len(report["private_delivery"]["ZIP_sha256"]) == 64
    assert report["bounds"]["fourth_floor_4003_DAT_is_missing_from_955_manifest"] is False
    for key, value in report["bounds"].items():
        if key == "overall_stage_A":
            assert value == "7_PARTIAL_2_OPEN"
        elif key == "stage_B_wiki":
            assert value == "GATED"
        elif key == "r79":
            assert value == "PAUSED_NON_BLOCKING"
        elif key == "percent_complete":
            assert value is None
        else:
            assert value is False, key


class Scene26SourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(OUT.read_text(encoding="utf-8"))
        cls.sources = load_sources(cls.report)

    def test_full_four_NPC_source_contract(self):
        verify(self.report, self.sources)

    def check_mutation(self, fn):
        bad = deepcopy(self.report)
        fn(bad)
        with self.assertRaises(AssertionError):
            verify(bad, self.sources)

    def test_reject_wrong_original_create_ordinal(self):
        self.check_mutation(lambda x: x["rows"][0].__setitem__("original_CREATE_block_ordinal", 2))

    def test_reject_fabricated_original_NPC_position(self):
        self.check_mutation(lambda x: x["rows"][0].__setitem__("source_original_borncenter", [20,15]))

    def test_reject_4003_declared_missing_from_original_955_maps(self):
        self.check_mutation(lambda x: x["bounds"].__setitem__("fourth_floor_4003_DAT_is_missing_from_955_manifest", True))

    def test_reject_drawn_marker_claimed_original_NPC_sprite(self):
        self.check_mutation(lambda x: x["rows"][0].__setitem__("native_historical_NPC_position_rendered", True))

    def test_reject_pet_tutor_message_promoted_to_GetPet_giveaway(self):
        self.check_mutation(lambda x: x["private_original_replay"].__setitem__("private_script_contains_GetPet_GetItem_DelItem_or_DelPet_literal", True))

    def test_reject_wrong_map_DAT_SHA(self):
        self.check_mutation(lambda x: x["rows"][2].__setitem__("original_qualified_DAT_sha256", "0"*64))


if __name__ == "__main__":
    unittest.main()
