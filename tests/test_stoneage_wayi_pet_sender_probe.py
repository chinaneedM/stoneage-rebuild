import struct
import unittest
from tools.stoneage_wayi_pet_sender_probe import add_expression, trace_cdecl, raw_e8_refs, probe
from tools.stoneage_wayi_saupdate_route_probe import decode_window

BASE=0x400000
TARGET=BASE+0x100


def code(prefix, call=True):
    raw=bytes.fromhex(prefix)
    if call:raw+=b'\xe8'+struct.pack('<i',TARGET-(BASE+len(raw)+5))
    return decode_window(raw,BASE)


class PetSenderProbeTests(unittest.TestCase):
    def test_cdecl_arguments_reverse_push_order(self):
        result=trace_cdecl(code('6a036a026a01'),BASE,0,{TARGET:(3,None)})
        self.assertEqual(result['calls'][0]['arguments'],[1,2,3])

    def test_original_argument_read_tracks_stack_movement(self):
        # Original arg2 is still at original ESP+8 after one pushed register.
        result=trace_cdecl(code('568b44240c50'),BASE,0,{TARGET:(1,None)})
        self.assertEqual(result['calls'][0]['arguments'],[{'original_argument':2}])

    def test_same_buffer_address_survives_pushes(self):
        result=trace_cdecl(code('8d0424508d4c240451'),BASE,-32,{TARGET:(2,None)})
        self.assertEqual(result['calls'][0]['arguments'],[{'local_address':-32}]*2)

    def test_negative_destination_is_retained_as_32bit(self):
        result=trace_cdecl(code('6afe'),BASE,0,{TARGET:(1,None)})
        self.assertEqual(result['calls'][0]['arguments'],[0xfffffffe])

    def test_helper_return_contract_is_explicit_not_executed(self):
        first=code('6a096a08')
        second=code('89c656')
        result=trace_cdecl(first+second,BASE,0,{TARGET:(2,1)})
        self.assertEqual(result['calls'][1]['arguments'][0],9)
        self.assertEqual(result['interpretation'],'STATIC_WITH_EXPLICIT_HELPER_CONTRACTS')

    def test_cdecl_volatile_register_not_reused_as_known_after_call(self):
        first=code('b9030000006a01')
        second=code('51')
        result=trace_cdecl(first+second,BASE,0,{TARGET:(1,None)})
        self.assertEqual(result['calls'][1]['arguments'][0],{'clobbered_by_call':0x100})

    def test_uncontracted_or_indirect_calls_rejected(self):
        for insns in [code('6a01'),code('ffd0',call=False)]:
            with self.subTest(insns=len(insns)),self.assertRaises(ValueError):
                trace_cdecl(insns,BASE,0,{})

    def test_conditional_branch_cannot_be_treated_as_linear_proof(self):
        with self.assertRaises(ValueError):trace_cdecl(code('7402',call=False),BASE,0,{})

    def test_indexed_lea_not_guessed(self):
        with self.assertRaises(ValueError):trace_cdecl(code('8d0444',call=False),BASE,0,{})

    def test_global_and_byte_width_retained(self):
        result=trace_cdecl(code('a1244e600450'),BASE,0,{TARGET:(1,None)})
        self.assertEqual(result['calls'][0]['arguments'],[{'global_rva':0x4204e24,'width_bytes':4}])

    def test_symbolic_addition_flattens_ordered_arguments(self):
        left={'original_argument':2};right={'original_argument':3}
        self.assertEqual(add_expression(add_expression(left,right),{'original_argument':4}),
                         {'sum':[left,right,{'original_argument':4}]})

    def test_raw_e8_candidate_uses_signed_relative_displacement(self):
        raw=b'xx\xe8'+struct.pack('<i',0x100-(0x200+2+5))+b'x'
        self.assertEqual(raw_e8_refs(raw,0x200,0x100),[0x202])
        self.assertEqual(raw_e8_refs(raw[:5],0x200,0x100),[])

    def test_unpinned_client_refuses_evidence(self):
        for payload in (b'',b'MZ',b'x'*921600):
            with self.subTest(size=len(payload)),self.assertRaises(ValueError):probe(payload)

if __name__=='__main__':unittest.main()
