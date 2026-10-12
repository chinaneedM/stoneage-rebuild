import struct,unittest
from tools.stoneage_tw10_savedata_helper_effects_r8 import summarize
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
BASE=0x400000;RVA=0x1000

def run(raw,**kw):return summarize(Decoder(raw,RVA,BASE),RVA,**kw)
class TestHelperEffects(unittest.TestCase):
    def test_leaf_return_keeps_registers_and_return_word(self):
        r=run(b'\xc3');self.assertTrue(r['qualifies_modeled_return_effect_summary']);self.assertEqual(len(r['common_preserved_registers']),7)
    def test_frame_round_trip(self):
        r=run(b'\x55\x8b\xec\x83\xec\x08\xc9\xc3');self.assertTrue(r['qualifies_modeled_return_effect_summary']);self.assertIn('ebp',r['common_preserved_registers'])
    def test_register_clobber_excluded(self):
        r=run(b'\x31\xc0\xc3');self.assertTrue(r['qualifies_modeled_return_effect_summary']);self.assertNotIn('eax',r['common_preserved_registers'])
    def test_saved_register_restore(self):
        r=run(b'\x53\x31\xdb\x5b\xc3');self.assertIn('ebx',r['common_preserved_registers'])
    def test_partial_clobber_excluded(self):
        r=run(b'\xb0\x01\xc3');self.assertNotIn('eax',r['common_preserved_registers'])
    def test_return_word_corruption_rejects_summary(self):
        r=run(b'\xc7\x04\x24\x00\x00\x00\x00\xc3');self.assertFalse(r['qualifies_modeled_return_effect_summary']);self.assertFalse(r['return_paths'][0]['return_word_preserved'])
    def test_displaced_return_stack_rejects(self):
        r=run(b'\x50\xc3');self.assertFalse(r['qualifies_modeled_return_effect_summary']);self.assertEqual(r['return_paths'][0]['pre_ret_stack_delta'],-4)
    def test_caller_argument_write_blocks_summary(self):
        r=run(b'\x89\x44\x24\x04\xc3');self.assertEqual(r['gaps'],{'caller_memory_write':1});self.assertFalse(r['qualifies_modeled_return_effect_summary'])
    def test_push_into_caller_region_blocks_summary(self):
        r=run(b'\x83\xc4\x0c\x50\x83\xec\x08\xc3');self.assertEqual(r['gaps'],{'caller_memory_write':1})
    def test_caller_argument_read_is_unknown_register_value(self):
        r=run(b'\x8b\x44\x24\x04\xc3');self.assertTrue(r['qualifies_modeled_return_effect_summary']);self.assertNotIn('eax',r['common_preserved_registers'])
    def test_stdcall_cleanup_reported(self):
        r=run(b'\xc2\x08\x00');self.assertTrue(r['qualifies_modeled_return_effect_summary']);self.assertEqual(r['uniform_ret_cleanup_bytes'],8)
    def test_nonuniform_cleanup_rejects(self):
        r=run(b'\x74\x03\xc2\x04\x00\xc2\x08\x00');self.assertFalse(r['qualifies_modeled_return_effect_summary']);self.assertIsNone(r['uniform_ret_cleanup_bytes'])
    def test_all_branch_register_preservation_intersection(self):
        r=run(b'\x74\x02\x31\xc0\xc3');self.assertTrue(r['qualifies_modeled_return_effect_summary']);self.assertNotIn('eax',r['common_preserved_registers'])
    def test_unsummarized_call_stops(self):
        r=run(b'\xe8\x00\x00\x00\x00\xc3');self.assertFalse(r['qualifies_modeled_return_effect_summary']);self.assertEqual(r['gaps'],{'unsummarized_call':1})
    def test_gap_site_has_exact_call_target_and_count(self):
        r=run(b'\xe8\x00\x00\x00\x00\xc3');self.assertEqual(r['gap_sites'],[{'rva':RVA,'reason':'unsummarized_call','direct_target_rva':RVA+5,'occurrences':1}])
    def test_gap_sites_reconcile_with_counts(self):
        r=run(b'\x74\x02\xff\xe0\xff\xe0')
        self.assertEqual(sum(e['occurrences'] for e in r['gap_sites']),sum(r['gaps'].values()))
    def test_original_probe_rejects_wrong_source_before_parsing(self):
        from tools.stoneage_tw10_savedata_helper_original_r8 import inspect_verified
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'not original',b'')
    def test_indirect_tail_jump_stops(self):
        r=run(b'\xff\xe0');self.assertEqual(r['gaps'],{'indirect_jump':1});self.assertFalse(r['qualifies_modeled_return_effect_summary'])
    def test_global_alias_store_stops(self):
        r=run(b'\x89\x08\xc3');self.assertEqual(r['gaps'],{'alias_write':1})
    def test_x87_store_stops(self):
        r=run(b'\xd9\x1c\x24\xc3');self.assertEqual(r['gaps'],{'unsupported_memory':1})
    def test_loop_cap_prevents_summary(self):
        r=run(b'\x50\xeb\xfd',max_states=8);self.assertTrue(r['state_limit_hit']);self.assertFalse(r['qualifies_modeled_return_effect_summary'])
    def test_cycle_with_possible_return_still_rejects_total_summary(self):
        r=run(b'\x74\x02\xeb\xfc\xc3');self.assertTrue(r['control_flow_cycle']);self.assertFalse(r['qualifies_modeled_return_effect_summary'])
    def test_system_transfer_is_not_pure_leaf(self):
        r=run(b'\x0f\x34\xc3');self.assertEqual(r['gaps'],{'terminal':1});self.assertFalse(r['qualifies_modeled_return_effect_summary'])
    def test_far_ret_not_ordinary_return(self):
        r=run(b'\xcb');self.assertEqual(r['gaps'],{'unsupported_return':1})
    def test_bounds_and_no_native_promotion(self):
        for bound in (0,2049,True):
            with self.assertRaises(ValueError):run(b'\xc3',max_states=bound)
        r=run(b'\xc3');self.assertFalse(r['original_helper_accepted']);self.assertFalse(r['native_io_executed'])
if __name__=='__main__':unittest.main()
