"""Independent branch/input/shape tamper tests; invented controls only."""
import unittest
from tests.test_stoneage_tw10_savedata_upstream_r24 import fixture,BASE
from tools.stoneage_tw10_savedata_upstream_r24 import branch_frontier,SCALAR_ROOT,CALLS
from tools.stoneage_tw10_savedata_dataflow_r6 import Decoder
from tools.stoneage_tw10_savedata_upstream_r24_guard import validate

def branch_fixture():
    d=fixture()
    raw=bytearray(b'\x90'*(CALLS[2][2]-SCALAR_ROOT+3))
    raw[:4]=bytes.fromhex('ffd07400')
    raw[-3:]=bytes.fromhex('ffd0c3')
    d['realloc_branch_frontier']=branch_frontier(Decoder(bytes(raw),SCALAR_ROOT,BASE),[])
    return d

class R24IndependentGuard(unittest.TestCase):
    def test_branch_fixture_stays_unknown(self):self.assertTrue(validate(branch_fixture()))
    def test_branch_outcome_promotion(self):
        d=branch_fixture();d['realloc_branch_frontier']['branches'][0]['branch_outcome_known']=True
        with self.assertRaises(ValueError):validate(d)
    def test_opaque_flag_effect_promotion(self):
        d=branch_fixture();d['realloc_branch_frontier']['branches'][0]['flag_sources'][0]['semantic']={'constant':0}
        with self.assertRaises(ValueError):validate(d)
    def test_scalar_input_value_promotion(self):
        d=fixture();d['realloc_eax_definition']['input_sources']['eax']['value_known']=True
        with self.assertRaises(ValueError):validate(d)
    def test_scalar_partial_width_cannot_get_u32_model(self):
        d=fixture();d['realloc_eax_definition']['operand_shapes'][0]['width_bytes']=2
        with self.assertRaises(ValueError):validate(d)
if __name__=='__main__':unittest.main()
