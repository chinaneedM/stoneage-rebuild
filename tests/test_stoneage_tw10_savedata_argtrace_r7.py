import unittest,struct
from tools.stoneage_tw10_savedata_argtrace_r7 import trace,State,step,Decoder,MAX_STATES
BASE=0x400000; RVA=0x1000; NAME=0x463634; IAT=0x403000
API=b'\xff\x15'+struct.pack('<I',IAT)
PROLOG=b'\x55\x8b\xec'
def call(rva,target): return b'\xe8'+struct.pack('<i',target-rva-5)
def run(raw,**kw): return trace(Decoder(raw,RVA,BASE),RVA,NAME,{IAT:('KERNEL32.dll','CreateFileA')},**kw)
class TestR7(unittest.TestCase):
    def test_frame_argument_load_then_push(self):
        r=run(PROLOG+b'\x8b\x45\x08\x50'+API+b'\xc3')
        self.assertTrue(r['CreateFileA_filename_slot0_candidate']); self.assertIn(0,r['api_candidates'][0]['filename_stack_slots'])
    def test_direct_wrapper_forwarding_with_return_address(self):
        code=PROLOG+b'\xff\x75\x08'; target=RVA+len(code)+6
        raw=code+call(RVA+len(code),target)+b'\xc3'+PROLOG+b'\xff\x75\x08'+API+b'\xc3'
        r=run(raw); self.assertIn(0,r['calls'][0]['filename_stack_slots']); self.assertEqual(r['api_candidates'][0]['depth'],1)
    def test_caller_continuation_not_assumed(self):
        raw=call(RVA,RVA+12)+b'\xff\x74\x24\x04'+API+b'\xc3'
        r=run(raw); self.assertFalse(r['CreateFileA_filename_slot0_candidate']); self.assertEqual(r['gaps']['call_return_summary_missing'],1)
    def test_extra_push_parameter_slot(self):
        r=run(PROLOG+b'\xff\x75\x08\x6a\x00'+API); self.assertEqual(r['api_candidates'][0]['filename_stack_slots'],[1,4])
    def test_ESP_relative_and_register_copy(self):
        r=run(b'\x8b\x44\x24\x04\x89\xc6\x56'+API); self.assertTrue(r['CreateFileA_filename_slot0_candidate'])
    def test_alias_store_stops(self):
        r=run(b'\x89\x08\xff\x74\x24\x04'+API); self.assertEqual(r['gaps'],{'alias_write':1}); self.assertEqual(r['api_candidates'],[])
    def test_known_stack_overwrite_removes_filename(self):
        r=run(b'\xc7\x44\x24\x04\x00\x00\x00\x00\xff\x74\x24\x04'+API)
        self.assertFalse(r['CreateFileA_filename_slot0_candidate'])
    def test_unaligned_stack_store_invalidates_overlap(self):
        r=run(b'\xc7\x44\x24\x05\x00\x00\x00\x00\xff\x74\x24\x04'+API)
        self.assertFalse(r['CreateFileA_filename_slot0_candidate'])
    def test_partial_register_write_kills_label(self):
        r=run(b'\x8b\x44\x24\x04\xb0\x00\x50'+API); self.assertFalse(r['CreateFileA_filename_slot0_candidate'])
    def test_branches_are_conditional_separate_states(self):
        r=run(b'\x74\x04\xff\x74\x24\x04'+API); slots=[e['filename_stack_slots'] for e in r['api_candidates']]
        self.assertIn([0,2],slots); self.assertIn([1],slots)
    def test_frame_local_store_load(self):
        r=run(PROLOG+b'\x83\xec\x04\x8b\x45\x08\x89\x45\xfc\xff\x75\xfc'+API)
        self.assertTrue(r['CreateFileA_filename_slot0_candidate'])
    def test_leave_reconstructs_parent_frame(self):
        d=Decoder(PROLOG+b'\xc9',RVA,BASE); s=State()
        for pos in (RVA,RVA+1,RVA+3): s,gap=step(d.at(pos),s,NAME); self.assertIsNone(gap)
        self.assertEqual(s.regs[__import__('capstone.x86',fromlist=['X86_REG_ESP']).X86_REG_ESP],('stack',0))
    def test_unknown_indirect_call(self):
        r=run(b'\xff\xd0\xc3'); self.assertEqual(r['gaps']['unresolved_transfer'],1)
    def test_tail_import_jump_skips_return_address(self):
        raw=b'\xff\x25'+struct.pack('<I',IAT); r=run(raw); self.assertIn(0,r['api_candidates'][0]['filename_stack_slots'])
    def test_segment_override_is_not_IAT(self):
        r=run(b'\x64'+API); self.assertEqual(r['api_candidates'],[]); self.assertEqual(r['gaps']['unresolved_transfer'],1)
    def test_depth_limit(self):
        r=run(call(RVA,RVA+6)+b'\xc3'+API,max_depth=0); self.assertEqual(r['gaps']['depth_limit'],1)
    def test_state_bound(self):
        r=run(b'\x90'*10+b'\xc3',max_states=2); self.assertTrue(r['state_limit_hit'])
        for kw in ({'max_states':True},{'max_states':MAX_STATES+1},{'max_depth':7}):
            with self.assertRaises(ValueError): run(b'\xc3',**kw)
    def test_unmodeled_ESP_change_stops(self):
        r=run(b'\x89\xc4'+API); self.assertEqual(r['gaps']['unsupported_stack'],1)
    def test_unknown_nonfile_import_stops_without_API(self):
        r=trace(Decoder(API,RVA,BASE),RVA,NAME,{IAT:('KERNEL32.dll','GetTickCount')}); self.assertEqual(r['api_candidates'],[])
if __name__=='__main__': unittest.main()
