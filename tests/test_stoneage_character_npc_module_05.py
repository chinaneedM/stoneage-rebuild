"""CHAR05: verify source-derived numeric joins, not protected original game image content."""
import json
import copy
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]/"research"/"recovered"
def get(name):return json.loads((R/name).read_text(encoding="utf-8"))
def replay(d,s,o,p,r):
    assert d["schema"]=="stoneage.character_npc_module_05_30_verified_source_config_to_existing_original_SPR_pixels.r1"
    assert d["original_RAR_sha256"]==s["original_rar_sha256"]==p["preserved_original_rar"]["sha256"]
    assert len(s["source_files"])==d["count"]["original_NPC_subtree_files_sha_verified_locally"]==2205
    assert len(s["create_rows"])==4985
    assert len(p["source_rows"]["spradrn_5.bin"])==847
    expected=o["indexed_graphic_source_summary"]
    found=d["graphic_material_status"]
    assert len(found)==len(expected)==108
    assert [(x["graphicname"],x["original_SPR_index_positions"],x["config_occurrences"]) for x in found]==expected
    assert sum(x["config_occurrences"] for x in found)==617
    groups={g["spr_no"]:g for g in r["full_segment_comparisons"]}
    assert set(groups)=={100250,100251,100252}
    assert sum(x["original_full_SPR_material_qualification"]=="R40_AND_SCENE13_ACTUAL_ORIGINAL_ACTION0_RD" for x in found)==3
    for row in found:
        if row["graphicname"] in groups:
            assert row["verified_full_SPR_segment_sha256"]==groups[row["graphicname"]]["segment_sha256"]
        else:
            assert row["original_full_SPR_material_qualification"]=="INDEX_ONLY_UNQUALIFIED_FULL_SPR_OR_RD"
            assert row["verified_full_SPR_segment_sha256"] is None
    prior=o["prior_R40_full_SPR_segment_source_create_refs"]
    rows=d["config_with_existing_real_art"]
    assert len(rows)==len(prior)==30
    smap={(x[0],x[1]):x for x in s["create_rows"]}
    counts={g:0 for g in groups}
    for actual,ref in zip(rows,prior):
        path,ord,role,g=ref
        v=smap[(path,ord)]
        assert (actual["source_create_path"],actual["source_create_ordinal"],actual["source_template_function"],actual["source_graphicname"])==(path,ord,role,g)
        assert actual["source_block_sha256"]==v[4]
        assert actual["source_floorid"]==v[5]
        assert actual["source_original_SPR_segment_sha256"]==groups[g]["segment_sha256"]
        assert actual["source_SPR_group_index"]==groups[g]["client_group_index"]
        assert actual["runtime_render_binding_not_proven"] is True
        counts[g]+=1
    assert counts=={100250:13,100251:3,100252:14}
    c=d["count"]
    assert c["original_graphicname_source_index_only_without_full_SPR_or_RD_qualification"]==105
    assert c["source_create_rows_source_index_only_without_full_SPR_or_RD_qualification"]==587
    assert c["earlier_R13_original_RD_blocks_SHA_reverified_locally"]==208
    assert c["new_original_RD_images_discovered_this_turn"]==0
    assert all(x is False for x in d["unproven"].values() if x is not None)
    assert d["unproven"]["overall_restoration_percent"] is None
    assert not d["private_material_receipt"]["original_RD_or_PNG_in_public_git"]
class TestCHAR05(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=(get("STONEAGE-CHARACTER-NPC-MODULE-05-30-ORIGINAL-MOTION-SOURCE-BRIDGE-R1.json"),get("STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json"),get("STONEAGE-CHARACTER-NPC-MODULE-04-SAME-CARRIER-GRAPHIC-FUNCTION-JOIN-R1.json"),get("STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json"),get("STONEAGE-PRESERVED-PET-SPR-MATERIAL-R40.json"))
    def validate(self,d):replay(d,*self.data[1:])
    def test_exact_full_replay(self):self.validate(self.data[0])
    def test_reject_missing_row(self):
        d=copy.deepcopy(self.data[0]);d["config_with_existing_real_art"].pop()
        with self.assertRaises(AssertionError):self.validate(d)
    def test_reject_changed_original_frame_sha(self):
        d=copy.deepcopy(self.data[0]);d["config_with_existing_real_art"][0]["source_original_SPR_segment_sha256"]="0"*64
        with self.assertRaises(AssertionError):self.validate(d)
    def test_reject_spurious_pixels(self):
        d=copy.deepcopy(self.data[0]);next(x for x in d["graphic_material_status"] if x["verified_full_SPR_segment_sha256"] is None)["original_full_SPR_material_qualification"]="R40_AND_SCENE13_ACTUAL_ORIGINAL_ACTION0_RD"
        with self.assertRaises(AssertionError):self.validate(d)
    def test_reject_original_identity_claim(self):
        d=copy.deepcopy(self.data[0]);d["unproven"]["original_official_30_NPC_person_identities"]=True
        with self.assertRaises(AssertionError):self.validate(d)
    def test_reject_wrong_original_role(self):
        d=copy.deepcopy(self.data[0]);d["config_with_existing_real_art"][0]["source_template_function"]="UNSUPPORTED_ROLE"
        with self.assertRaises(AssertionError):self.validate(d)
if __name__=="__main__":unittest.main()
