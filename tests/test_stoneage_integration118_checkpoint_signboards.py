"""Source-only original checkpoint records; no private commercial text in CI."""
from __future__ import annotations
import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research/recovered"
REPORT = R / "STONEAGE-INTEGRATION118-TWO-SETS-OF-12-ORIGINAL-CHECKPOINT-SIGNBOARDS-R1.json"
CHAR07 = R / "STONEAGE-CHARACTER-NPC-MODULE-07-TOWNPEOPLE-SIGNBOARD-SOURCE-CATALOG-R1.json"
MAP04 = R / "STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json"
CURRENT = "c89e0e33537990aa2132b47c40fef49a985a935c"


def load(p): return json.loads(p.read_text(encoding="utf-8"))
def gblob(p):
    content=p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
def aggregate(values):return hashlib.sha256("\n".join(values).encode("ascii")).hexdigest()

class TestOriginalMixed25SignboardSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rep=load(REPORT)
        cls.rows=cls.rep["source_records"]
        cls.old=load(CHAR07)
        cls.maps=load(MAP04)
        cls.meta={x[0]:x for x in cls.maps["per_floor_source_rows"]}

    def test_01_old_immutable_sources_exact_git_blob(self):
        older=self.rep["prior_sources_not_newly_claimed"]
        self.assertEqual(gblob(CHAR07),"8b2fee3c121f3cd3884a6937333f2ebcf1fc3ae4")
        self.assertEqual(gblob(MAP04),"1ef8c004179128ea44ffa4fb4259748bc8c83911")
        self.assertEqual(older["CHAR07_existing_original_text_catalog_Git_blob"],gblob(CHAR07))
        self.assertEqual(older["MAP04_existing_955_DAT_index_Git_blob"],gblob(MAP04))

    def test_02_old_char07_existing_all_24_source_refs(self):
        old=sorted([r for r in self.old["records"] if r["create_path"]=="genout/oev2.create"],key=lambda r:r["create_ordinal"])
        self.assertEqual(len(old),len(self.rows))
        for x,y in zip(self.rows,old):
            self.assertEqual((x["source_ordinal"],x["original_create_block_sha256"]),
                             (y["create_ordinal"],y["create_block_sha256"]))
            self.assertEqual((x["source_signboard_path"],x["original_arg_sha256"],x["original_arg_bytes"]),
                             (y["original_arg_path"],y["original_arg_sha256"],y["original_arg_size"]))
            self.assertEqual(x["source_floor"],int(y["source_floorid_raw"]))
            self.assertEqual(x["graphic_numeric_field"],int(y["source_graphicname_raw"]))
            self.assertEqual(self.rep["source_parent_LATER_PRESERVED_MIXED25"]["original_CREATE_sha256"],y["create_source_sha256"])
            self.assertEqual(y["role"],"SignBoard")

    def test_03_original_physical_order_and_two_sets_only(self):
        self.assertEqual([x["source_ordinal"] for x in self.rows],list(range(24)))
        self.assertEqual([x["physical_sequence_group"] for x in self.rows],[1]*12+[2]*12)
        expected=list(range(1,13))*2
        self.assertEqual([x["checkpoint_label_number"] for x in self.rows],expected)
        self.assertEqual(self.rep["summary"]["physical_order_group_1_labels"],expected[:12])
        self.assertEqual(self.rep["summary"]["physical_order_group_2_labels"],expected[12:])
        self.assertEqual(set(x["graphic_numeric_field"] for x in self.rows),{10062})

    def test_04_duplicate_text_body_hashes_only_source_bound(self):
        groups={}
        for x in self.rows:groups.setdefault(x["original_question_body_sha256_UTF8"],[]).append(x["source_ordinal"])
        same=sorted(x for x in groups.values() if len(x)>1)
        self.assertEqual(same,[[6,13],[11,23]])
        self.assertEqual(len(groups),self.rep["summary"]["distinct_original_text_body_count"])
        self.assertEqual(len(groups),22)
        self.assertFalse(self.rep["historical_boundaries"]["these_24_texts_are_24_distinct_questions"])

    def test_05_map04_exact_source_identity_size_and_coordinates(self):
        present=0;missing=[];different=set()
        for x in self.rows:
            floor=x["source_floor"];different.add(floor)
            meta=self.meta.get(f"{floor}.dat")
            self.assertEqual(x["source_map_DAT_in_existing_MAP04_report"],bool(meta))
            if meta:
                self.assertEqual(x["source_map_DAT_SHA256"],meta[2])
                self.assertEqual(x["source_map_DAT_width_height"],[meta[3],meta[4]])
                px,py=x["source_point"]
                self.assertTrue(0<=px<meta[3] and 0<=py<meta[4])
                present+=1
            else:
                self.assertIsNone(x["source_map_DAT_SHA256"])
                self.assertIsNone(x["source_map_DAT_width_height"])
                missing.append(floor)
        summary=self.rep["summary"]
        self.assertEqual((present,len(missing)),(16,8))
        self.assertEqual(summary["old_MAP04_original_DAT_metadata_present"],16)
        self.assertEqual(summary["old_MAP04_coordinate_in_bounds"],16)
        self.assertEqual(summary["old_MAP04_DAT_metadata_absent"],8)
        self.assertEqual(summary["distinct_source_floor_ids"],len(different))
        self.assertEqual(sorted(missing),summary["missing_DAT_metadata_floor_occurrences"])

    def test_06_raw_source_digest_chain_and_bytes_conservation(self):
        s=self.rep["summary"]
        self.assertEqual(s["actual_original_CREATE_records"],24)
        self.assertEqual(s["original_text_files_actual_read"],24)
        self.assertEqual(s["source_original_CP950_roundtrip_verified"],24)
        self.assertEqual(s["original_arg_total_bytes"],sum(x["original_arg_bytes"] for x in self.rows))
        self.assertEqual(s["original_arg_total_bytes"],1560)
        self.assertTrue(all(x["original_CP950_roundtrip"] for x in self.rows))
        self.assertEqual(s["all_original_arg_SHA256_in_source_order_aggregate"],aggregate([x["original_arg_sha256"] for x in self.rows]))
        self.assertEqual(s["all_original_create_block_SHA256_in_source_order_aggregate"],aggregate([x["original_create_block_sha256"] for x in self.rows]))
        self.assertEqual(self.rep["source_parent_LATER_PRESERVED_MIXED25"]["original_members_CRC_verified"],2205)

    def test_07_private_provenance_without_public_original_text(self):
        p=self.rep["private_source_observation"]
        self.assertEqual((p["private_archive_bytes"],p["private_archive_member_crc_verified"]),(11440,28))
        self.assertEqual(p["private_archive_sha256"],"931cedccfbfcdd9d46a0ce467b6af3fb7e28d5f3af83eed644677bf4eb3aafb3")
        self.assertTrue(p["private_Library_roundtrip_sha256_verified"])
        self.assertFalse(p["contains_original_commercial_source_in_public_Git"])
        self.assertFalse(p["modern_viewer_is_original_native_client"])
        self.assertTrue(self.rep["prior_sources_not_newly_claimed"]["original_CHAR07_texts_recounted_as_new_source_discoveries"]==0)
        self.assertEqual(self.rep["prior_sources_not_newly_claimed"]["MAP04_original_DAT_bytes_reread_this_work_unit"],0)
        self.assertFalse(any("original_text_CP950" in x for x in self.rows))

    def test_08_open_scope_and_historical_prefix(self):
        self.assertEqual(self.rep["original_current_state_blob_preserved"],CURRENT)
        b=self.rep["historical_boundaries"]
        self.assertEqual((b["Stage_A"],b["Stage_B_Wiki"],b["R79"]),
                         ("7_PARTIAL_2_OPEN","GATED","PAUSED_NON_BLOCKING"))
        self.assertIsNone(b["overall_percent"])
        for k in ("official_JSS1999_TW1_same_deployment","original_checkpoint_route_progression_or_event_trigger_verified",
                  "answer_key_or_correct_answer_verified","original_game_client_executed","original_signboard_draw_palette_or_collision_verified",
                  "missing_DAT_here_means_original_game_did_not_have_that_floor","proprietary_original_text_or_images_published"):
            self.assertIs(b[k],False,k)

if __name__=="__main__": unittest.main()
