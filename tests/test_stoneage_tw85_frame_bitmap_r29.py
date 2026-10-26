"""R29 adversarial material evidence gates, including all repeated raw record choices."""
from pathlib import Path
import tempfile
import unittest
from tools import stoneage_tw85_frame_bitmap_r29 as r29


class R29SourceContractTests(unittest.TestCase):
    def test_duplicate_original_id_is_not_silently_last_wins(self):
        original=[
          {"index":1,"size":112,"rd_sha256":"a"*64},
          {"index":2,"size":112,"rd_sha256":"a"*64}
        ]
        self.assertEqual(r29.classification(original),"MULTIPLE_SAME_COMPLETE_RD")
        changed=[original[0],{"index":2,"size":113,"rd_sha256":"b"*64}]
        self.assertEqual(r29.classification(changed),"MULTIPLE_DIFFERENT_COMPLETE_RD")
        self.assertEqual(len(original),2)

    def test_absent_not_normalized_and_single_qualified(self):
        self.assertEqual(r29.classification([]),"MISSING_SAME_SAMPLE_ADRN_ID")
        self.assertEqual(r29.classification([{"size":1,"rd_sha256":"a"*64}]),
                         "SINGLE_ORIGINAL_RD_RECORD")

    def test_raw_flag_zero_authoritative_size_can_pass_only_bounded_exception(self):
        row={"adder":"0","size":"116","width":"10","height":"10","rd_width":"10",
             "rd_height":"10","rd_status":"HEADER_MISMATCH","rd_size":"8621960",
             "rd_flag":"0"}
        self.assertEqual(r29.rd_status(row,1000),"VALID_FLAG0_ADRN_SIZE")
        row["rd_flag"]="1"
        self.assertEqual(r29.rd_status(row,1000),"INVALID")
        row["rd_flag"]="0";row["width"]="9"
        self.assertEqual(r29.rd_status(row,1000),"INVALID")
        row["width"]="10";row["adder"]="999"
        self.assertEqual(r29.rd_status(row,1000),"INVALID")

    def test_matching_header_requires_real_span_and_dimensions(self):
        row={"adder":"12","size":"200","width":"12","height":"14","rd_width":"12",
             "rd_height":"14","rd_status":"HEADER_MATCH","rd_size":"200","rd_flag":"1"}
        self.assertEqual(r29.rd_status(row,212),"VALID_HEADER")
        self.assertEqual(r29.rd_status(row,211),"INVALID")
        row["rd_height"]="15"
        self.assertEqual(r29.rd_status(row,212),"INVALID")

    def test_all_source_material_pins_present_and_strict(self):
        self.assertEqual(len(r29.INPUTS),6)
        self.assertEqual(r29.INPUTS["R28_FRAME"][1],
                         "d5e026801e743fed481847fe69da4a235c14d8019d3824d64182bc2821645142")
        self.assertEqual(r29.INPUTS["R06_NATIVE"][1],
                         "495928a0a44d7c81bf1d6ef7b06d26decfc5096803fbd60b9e8e0aa9752a45ce")
        self.assertIn("UNVERIFIED",r29.PROVENANCE)

    def test_status_is_index_binding_not_visible_render_or_pet_species(self):
        self.assertNotIn("visible",r29.classification([{"size":100,"rd_sha256":"a"*64}]).lower())
        self.assertTrue(r29.ROOT.is_dir())
        self.assertTrue((r29.R28/"R28-INDEPENDENT-CUSTODY.json").exists())


if __name__=="__main__":unittest.main()
