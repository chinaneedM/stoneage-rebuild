import struct
import unittest
from tools.stoneage_wayi_pet_state_probe import read_rva, resolve_indexed_switch, affine_address, loop_values, probe
from tools.stoneage_wayi_saupdate_route_probe import decode_window

LAYOUT={'sections':[{'vaddr':0x1000,'raw_ptr':0,'raw_size':32,'chars':0x20000000}]}
BASE=0x400000

class PetStateProbeTests(unittest.TestCase):
    def test_rva_maps_raw_not_absolute(self):
        self.assertEqual(read_rva(bytes(range(32)),LAYOUT,0x1003,4),b'\x03\x04\x05\x06')

    def test_rva_virtual_tail_and_truncated_section_rejected(self):
        for payload,rva,size in [(bytes(32),0x101f,2),(bytes(10),0x1009,2),(bytes(32),0x1000,0)]:
            with self.subTest(rva=rva,size=size),self.assertRaises(ValueError):read_rva(payload,LAYOUT,rva,size)

    def test_switch_preserves_duplicates_and_input_order(self):
        blob=b'\x00\x01\x00\x00'+struct.pack('<II',BASE+0x1010,BASE+0x1018)+bytes(20)
        x=resolve_indexed_switch(blob,LAYOUT,ord('B'),3,0x1000,0x1004,2,BASE)
        self.assertEqual([r['input_byte'] for r in x],[66,67,68])
        self.assertEqual([r['target_rva'] for r in x],[0x1010,0x1018,0x1010])

    def test_switch_index_outside_table_rejected(self):
        with self.assertRaises(ValueError):resolve_indexed_switch(b'\x02'+bytes(31),LAYOUT,66,1,0x1000,0x1004,2,BASE)

    def test_switch_target_must_be_executable_raw(self):
        blob=b'\x00'+bytes(3)+struct.pack('<I',BASE+0x1100)+bytes(24)
        with self.assertRaises(ValueError):resolve_indexed_switch(blob,LAYOUT,66,1,0x1000,0x1004,1,BASE)

    def test_switch_counts_bounded(self):
        with self.assertRaises(ValueError):resolve_indexed_switch(bytes(32),LAYOUT,66,257,0x1000,0x1004,1,BASE)

    def test_switch_byte_range_cannot_wrap(self):
        with self.assertRaises(ValueError):resolve_indexed_switch(bytes(32),LAYOUT,255,2,0x1000,0x1004,1,BASE)

    def test_affine_indexed_lea_keeps_scale_and_displacement(self):
        x=affine_address(decode_window(bytes.fromhex('8d448108'),BASE),{'ecx':{'pet':1},'eax':{'slot':1}}, {})
        self.assertEqual(x['eax'],{'constant':8,'pet':1,'slot':4})

    def test_affine_shift_sub_and_stack_symbol_are_independent(self):
        raw=bytes.fromhex('8d04c9c1e0032bc18b4c24148d04808d2cc1')
        x=affine_address(decode_window(raw,BASE),{'ecx':{'pet':1}},{0x14:'slot_offset'})
        self.assertEqual(x['ebp'],{'slot_offset':1,'pet':2840})

    def test_affine_unknown_or_uncontracted_memory_rejected(self):
        for raw in ('8d0401','8b4c2414'):
            with self.subTest(raw=raw),self.assertRaises(ValueError):affine_address(decode_window(bytes.fromhex(raw),BASE),{}, {})

    def test_affine_partial_register_and_branch_rejected(self):
        for raw in ('668bc1','7402','c3'):
            with self.subTest(raw=raw),self.assertRaises(ValueError):affine_address(decode_window(bytes.fromhex(raw),BASE),{'ecx':{'pet':1}}, {})

    def test_loop_has_seven_values_and_no_limit_iteration(self):
        self.assertEqual(loop_values(2,14,100),[2,16,30,44,58,72,86])
        self.assertEqual(loop_values(1,2,6),[1,3,5])

    def test_nonpositive_or_unbounded_loop_rejected(self):
        for args in [(1,0,10),(2,1,2),(0,1,4097)]:
            with self.subTest(args=args),self.assertRaises(ValueError):loop_values(*args)

    def test_wrong_specimen_cannot_produce_layout(self):
        with self.assertRaises(ValueError):probe(b'MZ')

if __name__=='__main__':unittest.main()
