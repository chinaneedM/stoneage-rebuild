import unittest
from tools.stoneage_wayi_saupdate_route_probe import decode_window, operand_metadata, raw_window, probe

BASE=0x400000

class RouteProbeTests(unittest.TestCase):
    def test_word_port_write_retains_width_and_numeric_value(self):
        row=decode_window(bytes.fromhex('66c70540584800901f'),BASE)[0]
        ops=operand_metadata(row,BASE)
        self.assertEqual(ops[0]['width_bytes'],2)
        self.assertEqual(ops[0]['absolute_rva'],0x85840)
        self.assertEqual(ops[1]['value'],8080)

    def test_indexed_stack_memory_is_not_global_slot(self):
        row=decode_window(bytes.fromhex('88440c10'),BASE)[0]
        ops=operand_metadata(row,BASE)
        self.assertNotIn('absolute_rva',ops[0])
        self.assertEqual(ops[0]['base'],'esp')
        self.assertEqual(ops[0]['index'],'ecx')

    def test_direct_branch_target_is_decoded_absolute(self):
        row=decode_window(bytes.fromhex('7450'),BASE+0x1a11)[0]
        self.assertEqual(operand_metadata(row,BASE)[0]['value'],BASE+0x1a63)

    def test_registry_call_via_register_preserved(self):
        row=decode_window(bytes.fromhex('ffd6'),BASE)[0]
        self.assertEqual(operand_metadata(row,BASE)[0]['name'],'esi')

    def test_import_thunk_absolute_slot(self):
        row=decode_window(bytes.fromhex('ff252cb54200'),BASE+0x19870)[0]
        self.assertEqual(row.mnemonic,'jmp')
        self.assertEqual(operand_metadata(row,BASE)[0]['absolute_rva'],0x2b52c)

    def test_incomplete_decode_rejected(self):
        with self.assertRaises(ValueError):decode_window(b'\xe8',BASE)

    def test_rva_window_maps_raw_offset_not_virtual_tail(self):
        layout={'sections':[{'vaddr':4096,'raw_ptr':4,'raw_size':4,'chars':0x20000000}]}
        self.assertEqual(raw_window(b'xxxxABCD',layout,4097,4099),b'BC')
        with self.assertRaises(ValueError):raw_window(b'xxxxABCD',layout,4098,4101)

    def test_backward_window_rejected(self):
        with self.assertRaises(ValueError):raw_window(b'',{'sections':[]},2,1)

    def test_data_section_never_decoded_as_code(self):
        layout={'sections':[{'vaddr':4096,'raw_ptr':0,'raw_size':4,'chars':0x40000000}]}
        with self.assertRaises(ValueError):raw_window(b'ABCD',layout,4096,4100)

    def test_unpinned_or_truncated_specimen_rejected(self):
        for payload in (b'',b'MZ',b'x'*253952):
            with self.subTest(size=len(payload)),self.assertRaises(ValueError):probe(payload)

if __name__ == '__main__':unittest.main()
