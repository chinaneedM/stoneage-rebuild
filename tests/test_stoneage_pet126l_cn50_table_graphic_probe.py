"""PET126L synthetic same-CAB numeric crosswalk; no native semantic promotion."""
import struct
import unittest

from tools.stoneage_pet126l_cn50_table_graphic_probe import (
    TABLE_OFFSET, ROWS, STRIDE, crosswalk, exact_pointer_literals, source_rows,
)

class Pet126LSourceQualification(unittest.TestCase):
    def test_numeric_matches_are_candidate_only(self):
        rows = [{"ordinal":i, "name":"候选", "raw_i32":101 if i % 2 else 102,
                 "raw_u32":28001} for i in range(305)]
        groups = {101:{"index":1},102:{"index":2}}
        frames = [{"group_index":1,"bmp_no":42},{"group_index":2,"bmp_no":43},
                  {"group_index":1,"bmp_no":0xffffffff}]
        got = crosswalk(rows,groups,frames,{42,43,28001})
        self.assertEqual(got["numeric_source_key_overlaps"]["raw_i32"]["spr_key_rows"],305)
        self.assertEqual(got["numeric_source_key_overlaps"]["raw_u32"]["bitmap_key_rows"],305)
        self.assertEqual(got["spr_groups_selected_by_either_numeric_field"],2)
        self.assertEqual(got["selected_spr_distinct_frame_bitmap_numbers"],2)
        self.assertEqual(got["selected_spr_frame_bitmaps_missing_same_cab_adrn"],0)
        self.assertFalse(got["native_pet_graphic_selector_proven"])
        self.assertFalse(got["official_live_pet_issuance_proven"])
        self.assertFalse(got["species_count_inferable"])

    def test_unqualified_population_rejected(self):
        with self.assertRaisesRegex(ValueError,"unexpected-name-population"):
            crosswalk([{"ordinal":0,"name":"候选","raw_i32":1,"raw_u32":2}],{},[],set())

    def test_raw_pe32_literal_hit_is_not_selector_proof(self):
        data = bytearray(1024)
        data[0x3c:0x40] = struct.pack("<I",128)
        data[128:132] = b"PE\x00\x00"
        struct.pack_into("<H",data,134,1) # section count
        struct.pack_into("<H",data,148,224) # optional header size
        struct.pack_into("<H",data,152,0x10b) # PE32
        struct.pack_into("<I",data,180,0x400000) # image base
        sec = 152 + 224
        data[sec:sec+8] = b".text\x00\x00\x00"
        struct.pack_into("<IIII",data,sec+8,256,0x1000,256,512)
        data[520:524] = struct.pack("<I",0x401008)
        got = exact_pointer_literals(bytes(data),520)
        self.assertEqual(got["table_rva"],0x1008)
        self.assertEqual(got["literal_va_hits"],1)
        self.assertFalse(got["proves_selector"])
        self.assertEqual(got["literal_va_locations"],[{"file_offset":520,"rva":0x1008}])


if __name__=="__main__":
    unittest.main()
