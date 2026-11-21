import unittest
from tools.stoneage_pet126s_cn50_runtime_u32_consumer import (
    TAIL_VA, BASE_VA, NAME_TAIL_VA, classify_direct_field_instruction,
    exact_hex_tokens, occurrences, bounded_native_reader_following_call
)
class PET126SStaticConsumer(unittest.TestCase):
    def test_absolute_operand_token_exact_not_substring(self):
        self.assertIn(TAIL_VA,exact_hex_tokens("mov    eax,DWORD PTR [edi+0x3300ccc]"))
        self.assertNotIn(TAIL_VA,exact_hex_tokens("mov    eax,DWORD PTR [edi+0x3300ccc0]"))
        self.assertNotIn(TAIL_VA,exact_hex_tokens("mov    eax,DWORD PTR [edi+0x3300cc]"))
    def test_read_write_address_only_separate(self):
        self.assertEqual(classify_direct_field_instruction(
            "mov    DWORD PTR [edi+0x3300ccc],eax",TAIL_VA),"EXPLICIT_MEMORY_WRITE")
        self.assertEqual(classify_direct_field_instruction(
            "mov    eax,DWORD PTR [edi+0x3300ccc]",TAIL_VA),"EXPLICIT_MEMORY_READ")
        self.assertEqual(classify_direct_field_instruction(
            "lea    eax,[edi+0x3300ccc]",TAIL_VA),"ADDRESS_ONLY_LEA_NOT_DEREFERENCE")
        self.assertEqual(classify_direct_field_instruction(
            "cmp    DWORD PTR [edi+0x3300ccc],0x1",TAIL_VA),"EXPLICIT_MEMORY_TEST_OR_PUSH_READ")
    def test_scope_is_original_exact_absolute_address(self):
        self.assertNotEqual(BASE_VA,TAIL_VA)
        self.assertNotEqual(NAME_TAIL_VA,TAIL_VA)
        self.assertIsNone(classify_direct_field_instruction(
            "mov    eax,DWORD PTR [edi+0x482f80]",TAIL_VA))
        self.assertIsNone(classify_direct_field_instruction(
            "mov    eax,DWORD PTR [edi+0x3300ccc0]",TAIL_VA))
    def test_bounded_occurrence_preserves_all_hit_addresses(self):
        code=[
            {"address":0x43476e,"instruction":"mov    eax,DWORD PTR [eax+0x482f80]"},
            {"address":0x434774,"instruction":"mov    DWORD PTR [edi+0x3300ccc],eax"},
            {"address":0x43477a,"instruction":"mov    ecx,DWORD PTR [esi+0x3300ccc]"},
            {"address":0x434780,"instruction":"lea    edx,[edi+0x3300ccc]"}
        ]
        found=occurrences(code,TAIL_VA,context=1)
        self.assertEqual(found["exact_instruction_hits"],3)
        self.assertEqual(found["all_hit_instruction_addresses"],["0x434774","0x43477a","0x434780"])
        self.assertEqual(found["by_access_class"]["EXPLICIT_MEMORY_WRITE"],1)
        self.assertEqual(found["by_access_class"]["EXPLICIT_MEMORY_READ"],1)
        self.assertEqual(found["by_access_class"]["ADDRESS_ONLY_LEA_NOT_DEREFERENCE"],1)

    def test_bounded_original_reader_call_does_not_imply_renderer(self):
        b=0x439f0e
        code=[
            {"address":b,"instruction":"push   DWORD PTR [eax+0x3300ccc]"},
            {"address":b+6,"instruction":"push   ebx"},
            {"address":b+7,"instruction":"call   0x500000"},
            {"address":0x500000,"instruction":"mov    eax,ebx"},
            {"address":0x500002,"instruction":"ret"}
        ]
        x=bounded_native_reader_following_call(code)
        self.assertEqual(x["native_plus36_consumer_va"],"0x439f0e")
        self.assertEqual(x["first_direct_call_target_va"],"0x500000")
        self.assertEqual(len(x["first_target_first_12_decoded_instructions"]),2)
        self.assertFalse(x["call_target_is_original_SPR_or_ADRN_bitmap_renderer_proven"])
        self.assertFalse(x["first_call_is_always_reached_or_push_still_on_stack_proven"])
        with self.assertRaises(ValueError):
            bounded_native_reader_following_call(code[1:])

if __name__=="__main__":
    unittest.main()
