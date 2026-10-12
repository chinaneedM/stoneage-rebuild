import struct,unittest
from tools.stoneage_tw10_savedata_helper_frontier_r9 import store_geometry,loop_components,structural_surface,region_for_va,inspect_verified
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
BASE=0x400000;RVA=0x1000
SECTIONS=[{'name':'.data','rva':0x3000,'raw_size':16,'vsize':256,'characteristics':0x80000000}]
def dec(raw):return Decoder(raw,RVA,BASE)
class TestR9(unittest.TestCase):
    def test_absolute_write_maps_exact_address(self):
        r=store_geometry(dec(b'\xa3'+struct.pack('<I',BASE+0x3008)),RVA,SECTIONS)
        self.assertEqual(r['absolute_effective_rva'],0x3008);self.assertTrue(r['effective_address_fully_known']);self.assertFalse(r['table_or_object_ownership_proven'])
    def test_indexed_displacement_does_not_prove_effective_address(self):
        r=store_geometry(dec(b'\x89\x04\x9d'+struct.pack('<I',BASE+0x3008)),RVA,SECTIONS)
        self.assertEqual(r['index_register'],'ebx');self.assertEqual(r['index_scale'],4);self.assertFalse(r['effective_address_fully_known']);self.assertIsNone(r['absolute_effective_rva'])
    def test_virtual_zero_region_is_not_raw_backed(self):
        r=region_for_va(SECTIONS,BASE,BASE+0x3080);self.assertFalse(r['raw_backed']);self.assertTrue(r['writable'])
    def test_unmapped_displacement(self):self.assertIsNone(region_for_va(SECTIONS,BASE,0))
    def test_segmented_write_rejected(self):
        with self.assertRaises(ValueError):store_geometry(dec(b'\x64\xa3'+struct.pack('<I',BASE+0x3008)),RVA,SECTIONS)
    def test_read_operand_is_not_store(self):
        with self.assertRaises(ValueError):store_geometry(dec(b'\xa1'+struct.pack('<I',BASE+0x3008)),RVA,SECTIONS)
    def test_scc_cycle_separate_from_dag(self):
        self.assertEqual(loop_components({1,2,3,4},{(1,2),(2,3),(3,2),(3,4)}),[{2,3}])
    def test_self_loop(self):self.assertEqual(loop_components({1},{(1,1)}),[{1}])
    def test_structural_loop_has_conditional_branch(self):
        r=structural_surface(dec(b'\x90\x75\xfd\xc3'),RVA)
        self.assertEqual(len(r['loops']),1);self.assertEqual(r['loops'][0]['conditional_branches'][0]['condition'],'jne');self.assertFalse(r['runtime_loop_conditions_proven'])
    def test_call_fallthrough_explicitly_contingent(self):
        r=structural_surface(dec(b'\xe8\x00\x00\x00\x00\xc3'),RVA)
        self.assertEqual(r['call_return_assumptions'],1);self.assertEqual(r['nodes'],2);self.assertFalse(r['caller_resumption_admitted'])
    def test_indirect_jump_stops(self):self.assertEqual(structural_surface(dec(b'\xff\xe0'),RVA)['indirect_jump_count'],1)
    def test_ret_stops_before_extra_bytes(self):self.assertEqual(structural_surface(dec(b'\xc3\x90'),RVA)['nodes'],1)
    def test_bounds(self):
        r=structural_surface(dec(b'\x90'*8+b'\xc3'),RVA,max_nodes=2);self.assertTrue(r['limit_hit'])
        for kw in ({'max_nodes':True},{'span':1025},{'max_nodes':0}):
            with self.assertRaises(ValueError):structural_surface(dec(b'\xc3'),RVA,**kw)
    def test_original_input_wrong_hash_rejected(self):
        with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):inspect_verified(b'wrong',b'')
if __name__=='__main__':unittest.main()
