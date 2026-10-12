import struct
import unittest
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder, first_transfer, cross_callee, MAX_NODES
BASE=0x400000; RVA=0x1000; NAME=0x463634; IAT=0x403000
PUSH=b'\x68'+struct.pack('<I',NAME)
API=b'\xff\x15'+struct.pack('<I',IAT)
def call(source,target): return b'\xe8'+struct.pack('<i',target-source-5)
def dec(raw): return Decoder(raw,RVA,BASE)
class TestR6(unittest.TestCase):
    def prefix(self,tail): return first_transfer(dec(PUSH+tail),RVA,NAME,{IAT:('KERNEL32.dll','CreateFileA')})
    def test_filename_on_top(self):
        r=self.prefix(API+b'\xc3'); self.assertEqual(r['filename_stack_slot'],0); self.assertEqual(r['import_api'],'CreateFileA')
    def test_extra_push_slot_and_pop(self):
        self.assertEqual(self.prefix(b'\x6a\x00'+API)['filename_stack_slot'],1)
        self.assertEqual(self.prefix(b'\x6a\x00\x58'+API)['filename_stack_slot'],0)
    def test_pop_filename_does_not_reappear(self):
        self.assertIsNone(self.prefix(b'\x58'+PUSH+API)['filename_stack_slot'])
    def test_alias_memory_write_invalidates(self):
        self.assertIsNone(self.prefix(b'\xc7\x04\x24\x00\x00\x00\x00'+API)['filename_stack_slot'])
    def test_esp_adjustment_invalidates(self):
        self.assertIsNone(self.prefix(b'\x83\xc4\x04'+API)['filename_stack_slot'])
    def test_16bit_push_invalidates(self):
        self.assertIsNone(self.prefix(b'\x66\x6a\x00'+API)['filename_stack_slot'])
    def test_branch_stops_without_argument_claim(self):
        r=self.prefix(b'\x74\x00'+API); self.assertEqual(r['stop'],'branch'); self.assertIsNone(r['filename_stack_slot'])
    def test_return_stops(self):
        r=self.prefix(b'\xc3'+API); self.assertEqual(r['stop'],'return'); self.assertIsNone(r['transfer_rva'])
    def test_first_call_stops_before_second_API(self):
        r=self.prefix(call(RVA+5,RVA+11)+API); self.assertEqual(r['direct_target_rva'],RVA+11); self.assertIsNone(r['import_api'])
    def test_prefix_limit(self):
        r=first_transfer(dec(PUSH+b'\x90'*10),RVA,NAME,{},max_prefix=2); self.assertEqual(r['stop'],'prefix_limit')
    def test_invalid_start(self):
        with self.assertRaises(ValueError): first_transfer(dec(b'\x90'),RVA,NAME,{})
    def test_cross_call_far_beyond_R5_radius(self):
        target=RVA+3000; raw=call(RVA,target)+b'\xc3'+b'\xcc'*2994+API+b'\xc3'
        r=cross_callee(dec(raw),RVA,{IAT:('KERNEL32.dll','ReadFile')})
        self.assertEqual(r['api_events'],[{'rva':target,'api':'ReadFile','min_call_depth':1}]); self.assertFalse(r['node_limit_hit'])
    def test_direct_thunk_tail_jmp(self):
        raw=call(RVA,RVA+6)+b'\xc3'+b'\xff\x25'+struct.pack('<I',IAT)
        r=cross_callee(dec(raw),RVA,{IAT:('KERNEL32.dll','WriteFile')}); self.assertEqual(r['api_events'][0]['rva'],RVA+6)
    def test_indirect_register_is_gap(self):
        r=cross_callee(dec(b'\xff\xd0\xc3'),RVA,{}); self.assertEqual(r['unresolved_indirect_transfers'],1)
    def test_return_blocks_API(self):
        r=cross_callee(dec(b'\xc3'+API),RVA,{IAT:('KERNEL32.dll','ReadFile')}); self.assertEqual(r['api_events'],[])
    def test_depth_limit_not_absence_proof(self):
        raw=call(RVA,RVA+6)+b'\xc3'+API+b'\xc3'
        r=cross_callee(dec(raw),RVA,{IAT:('KERNEL32.dll','ReadFile')},max_depth=0)
        self.assertEqual(r['api_events'],[]); self.assertEqual(r['depth_limit_stops'],1)
    def test_node_limit_and_bounds(self):
        r=cross_callee(dec(b'\x90'*20+b'\xc3'),RVA,{},max_nodes=2); self.assertTrue(r['node_limit_hit'])
        for kw in ({'max_nodes':0},{'max_nodes':MAX_NODES+1},{'max_depth':5},{'max_nodes':True}):
            with self.assertRaises(ValueError): cross_callee(dec(b'\xc3'),RVA,{},**kw)
    def test_nonfile_import_not_promoted(self):
        r=cross_callee(dec(API+b'\xc3'),RVA,{IAT:('KERNEL32.dll','GetTickCount')}); self.assertEqual(r['api_events'],[])
    def test_IAT_address_immediate_not_import_call(self):
        r=self.prefix(call(RVA+5,IAT-BASE)); self.assertIsNone(r['import_api'])
if __name__=='__main__': unittest.main()
