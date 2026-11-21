import unittest
from tools.stoneage_pet126r_cn50_source_catalogue import (
    album_index,instruction_exact_sites,actual_native_tail_field_bridge
)

class PET126R(unittest.TestCase):
    def test_original_field_tokens_exact_not_substring(self):
        code=[{"address":4,"instruction":"mov eax,0x482f68"},
              {"address":8,"instruction":"mov eax,0x482f680"},
              {"address":12,"instruction":"mov eax,0x482f80"}]
        got=instruction_exact_sites(code,{"base":0x482f68,"tail":0x482f80},cap=1)
        self.assertEqual(got["base"]["exact_token_occurrences"],1)
        self.assertEqual(got["tail"]["exact_token_occurrences"],1)
        self.assertEqual(got["base"]["bounded_first_contexts"][0]["va"],"0x4")
    def test_all_source_slots_preserved_while_matching_is_hypothesis(self):
        rows=[{"ordinal":i,"name":"测试"+str(i) if i%2==0 else "无",
                "raw_i32":i//2 if i%2==0 else -1,
                "raw_u32":28000+i if i%2==0 else 0,
                "raw_record":(str(i).encode()+b"x"*28)[:28]} for i in range(362)]
        # The entire same-CAB source group namespace is independent from names.
        groups=[{"spr_no":str(100250+i),"index":str(i),"segment_sha256":"a"*64} for i in range(1185)]
        tw=[{"graphic_number":100250+i,"spr_original_segment_sha256":"a"*64} for i in range(124)]
        entries=album_index(rows,groups,tw)
        self.assertEqual(len(entries),362)
        self.assertEqual(sum(x["label_as_compiled_GB18030"] is not None for x in entries),181)
        self.assertEqual(sum(x["TW10_retail_exact_same_SPR_segment_at_this_ordinal"] is True for x in entries if x["label_as_compiled_GB18030"] is not None),62)
        self.assertTrue(all(not x["CN50_name_to_SPR_native_selector_proven"] for x in entries))
        self.assertTrue(all(not x["original_official_live_pet_release_proven"] for x in entries))
        self.assertTrue(all(x["original_server_species_identifier"] is None for x in entries))
    def test_real_original_native_tail_transfer_is_adjacent_not_graphic_proof(self):
        start=0x43476e
        code=[
            {"address":start,"instruction":"mov    eax,DWORD PTR [eax+0x482f80]"},
            {"address":start+6,"instruction":"mov    DWORD PTR [edi+0x3300ccc],eax"}
        ]
        result=actual_native_tail_field_bridge(code)
        self.assertEqual(result["read_compiled_table_relative_byte_offset"],24)
        self.assertEqual(result["write_runtime_record_relative_byte_offset"],36)
        self.assertTrue(result["exact_original_static_adjacent_operand_transfer_verified"])
        self.assertTrue(result["this_is_not_SPR_selector_or_ADRN_alias_runtime_proof"])
        wrong=[code[0],dict(code[1],instruction="mov    DWORD PTR [edi+0x3300ccc],edx")]
        with self.assertRaises(ValueError):actual_native_tail_field_bridge(wrong)

    def test_invalid_group_duplicate_rejected(self):
        rows=[{"ordinal":i,"name":"无","raw_i32":-1,"raw_u32":0,"raw_record":b" "*28} for i in range(362)]
        groups=[{"spr_no":"1","index":str(i),"segment_sha256":"x"} for i in range(1185)]
        with self.assertRaises(ValueError):album_index(rows,groups,[])
if __name__=="__main__":unittest.main()
