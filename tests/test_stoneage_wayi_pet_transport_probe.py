import unittest
from tools.stoneage_wayi_saupdate_route_probe import decode_window
from tools.stoneage_wayi_pet_transport_probe import summarize_window, comparison_branch_taken, probe
BASE=0x400000

class PetTransportProbeTests(unittest.TestCase):
    def summary(self,raw,imports=None):
        return summarize_window(decode_window(bytes.fromhex(raw),BASE),BASE,imports or {})

    def test_direct_call_edge_has_rva_and_instruction_end(self):
        x=self.summary('e805000000')
        self.assertEqual(x['calls'][0]['direct_target_rva'],10)

    def test_indirect_import_call_retains_identity(self):
        x=self.summary('ff15b8024a00',{0x4a02b8:('WSOCK32.dll','send')})
        self.assertEqual(x['calls'][0]['import'],['WSOCK32.dll','send'])
        self.assertNotIn('direct_target_rva',x['calls'][0])

    def test_import_thunk_kept_as_indirect_jump(self):
        x=self.summary('ff25b8024a00',{0x4a02b8:('WSOCK32.dll','send')})
        self.assertEqual(x['branches'][0]['import'],['WSOCK32.dll','send'])

    def test_adjacent_comparison_links_to_branch(self):
        x=self.summary('83f8097d03')
        self.assertEqual(x['branches'][0]['adjacent_comparison_rva'],0)
        self.assertEqual(x['branches'][0]['target_rva'],8)
        self.assertEqual(x['branches'][0]['fallthrough_rva'],5)

    def test_nonadjacent_test_is_not_guessed_as_branch_basis(self):
        x=self.summary('83f809907d03')
        self.assertNotIn('adjacent_comparison_rva',x['branches'][0])

    def test_memory_width_survives_guard_inventory(self):
        x=self.summary('66833d9061560400')
        self.assertEqual(x['comparisons'][0]['operands'][0]['width_bytes'],2)

    def test_callback_absolute_write_keeps_reg_or_constant(self):
        x=self.summary('a3e8e14b00c705e8e14b00e0e24300')
        self.assertEqual(len(x['absolute_writes']),2)
        self.assertEqual(x['absolute_writes'][0]['source']['kind'],'register')
        self.assertEqual(x['absolute_writes'][1]['source']['value'],0x43e2e0)

    def test_signed_and_unsigned_sentinel_comparisons_differ(self):
        self.assertTrue(comparison_branch_taken('jl',0xffffffff,0,4))
        self.assertFalse(comparison_branch_taken('jb',0xffffffff,0,4))

    def test_width_masks_before_equality(self):
        self.assertTrue(comparison_branch_taken('je',0x100,0,1))
        self.assertFalse(comparison_branch_taken('je',0x100,0,2))

    def test_threshold_boundary_7_and_9_not_collapsed(self):
        self.assertTrue(comparison_branch_taken('jl',6,7,4))
        self.assertFalse(comparison_branch_taken('jl',7,7,4))
        self.assertTrue(comparison_branch_taken('jl',8,9,4))
        self.assertFalse(comparison_branch_taken('jl',9,9,4))

    def test_unsupported_condition_and_width_rejected(self):
        for condition,width in [('jo',4),('jl',3)]:
            with self.subTest(condition=condition,width=width),self.assertRaises(ValueError):
                comparison_branch_taken(condition,1,2,width)

    def test_wrong_hash_cannot_produce_transport_evidence(self):
        with self.assertRaises(ValueError):probe(b'MZ')

if __name__=='__main__':unittest.main()
