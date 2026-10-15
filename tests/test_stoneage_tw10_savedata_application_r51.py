import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_application_r51 import effect,stack,coordinates,analyze,same

def reg(r,width=4):return {'kind':'register','register':r,'width_bytes':width}
def imm(n):return {'kind':'immediate','constant':n,'width_bytes':4}
def row(a,m,ops=(),writes=()):return {'site_rva':a,'mnemonic':m,'operands':list(ops),'decoder_written_registers':list(writes)}
def mem(offset,base='esp',index=None,segment=None):return {'kind':'memory','width_bytes':4,'decoder_read':True,'decoder_write':False,'geometry':{'base_register':base,'index_register':index,'segment_register':segment,'relative_field_offset':offset}}
class NumericStack(unittest.TestCase):
    def test_push_pop(self):self.assertEqual([effect(row(1,m,[reg('eax')])) for m in ('push','pop')],[-4,4])
    def test_literal_cleanup(self):self.assertEqual(effect(row(1,'add',[reg('esp'),imm(24)],['esp'])),24)
    def test_sub(self):self.assertEqual(effect(row(1,'sub',[reg('esp'),imm(8)],['esp'])),-8)
    def test_pop_esp(self):self.assertIsNone(effect(row(1,'pop',[reg('esp')])))
    def test_partial_esp(self):self.assertIsNone(effect(row(1,'add',[reg('sp',2),imm(2)],['sp'])))
    def test_large_delta(self):self.assertIsNone(effect(row(1,'add',[reg('esp'),imm(4097)],['esp'])))
    def test_negative_literal(self):self.assertIsNone(effect(row(1,'add',[reg('esp'),imm(-4)],['esp'])))
    def test_bool_literal(self):self.assertIsNone(effect(row(1,'add',[reg('esp'),imm(True)],['esp'])))
    def test_opaque_call(self):
        s,cap=stack([row(1,'call'),row(2,'nop')],[[1,2]],1);self.assertIsNone(s[2]);self.assertFalse(cap)
    def test_unknown_write(self):self.assertIsNone(effect(row(1,'mov',[reg('esp'),reg('eax')],['esp'])))
    def test_merge_disagreement(self):
        s,_=stack([row(1,'jne'),row(2,'push',[reg('eax')]),row(3,'nop'),row(4,'nop')],[[1,2],[1,3],[2,4],[3,4]],1);self.assertIsNone(s[4])
    def test_merge_agreement(self):
        s,_=stack([row(1,'jne'),row(2,'nop'),row(3,'nop'),row(4,'nop')],[[1,2],[1,3],[2,4],[3,4]],1);self.assertEqual(s[4],0)
    def test_loop_state_bound(self):
        s,cap=stack([row(1,'push',[reg('eax')]),row(2,'jmp')],[[1,2],[2,1]],1);self.assertIsNone(s[1]);self.assertFalse(cap)
    def test_missing_root(self):
        with self.assertRaises(ValueError):stack([row(1,'nop')],[],2)
    def test_missing_edge(self):
        with self.assertRaises(ValueError):stack([row(1,'nop')],[[1,2]],1)
    def test_duplicate_inventory(self):
        with self.assertRaises(ValueError):stack([row(1,'nop'),row(1,'nop')],[],1)
    def test_entry_slot_return_address(self):
        pushes=[{'conditional_pre_call_esp_offset':0,'input':reg('edx')}]
        r=coordinates([row(1,'push',[reg('ebx')]),row(2,'mov',[reg('eax'),mem(8)])],[[1,2]],1,pushes)['references'][0]
        self.assertEqual(r['conditional_entry_esp_offset'],4);self.assertEqual(r['conditional_caller_pre_call_slot_offset'],0);self.assertEqual(r['matching_physical_push'],pushes[0]);self.assertFalse(r['actual_stack_value_abi_or_alias_proven'])
    def test_unknown_coordinate(self):
        r=coordinates([row(1,'call'),row(2,'mov',[reg('eax'),mem(8)])],[[1,2]],1,[])['references'][0];self.assertIsNone(r['conditional_entry_esp_offset']);self.assertIsNone(r['matching_physical_push'])
    def test_segment_override(self):self.assertEqual(coordinates([row(1,'mov',[reg('eax'),mem(8,segment='fs')])],[],1,[])['references'],[])
    def test_index_barrier(self):self.assertEqual(coordinates([row(1,'mov',[reg('eax'),mem(8,index='ecx')])],[],1,[])['references'],[])
    def test_type_sensitive_contract(self):self.assertFalse(same({'actual':False},{'actual':0}))
    def test_neutral_instruction(self):self.assertEqual(effect(row(1,'xchg',[reg('eax'),reg('edx')],['eax','edx'])),0)
if __name__=='__main__':unittest.main()
