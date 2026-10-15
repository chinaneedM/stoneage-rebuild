import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_frame_r56_guard import geometry,validate
P=Path(__file__).resolve().parents[1]/'research/recovered'
A=(P/'STONEAGE-TW10-SAVEDATA-NATIVE-IO-R54-ORIGINAL.json').read_bytes();B=(P/'STONEAGE-TW10-SAVEDATA-NATIVE-IO-R55-SPEC.json').read_bytes();D=json.loads((P/'STONEAGE-TW10-SAVEDATA-NATIVE-IO-R56-SPEC.json').read_text());R=D['complete_caller_instruction_shapes'];E=D['caller_bounded_edges']
class AlgebraTests(unittest.TestCase):
    def test_accept(self):self.assertEqual(validate(D,A,B),55)
    def test_unknown_open(self):self.assertIsNone(geometry(R,E,0x40020)[0x40090])
    def test_known_prefix(self):self.assertEqual(geometry(R,E,0x40020)[0x40069],-4172)
    def test_helper_unknown(self):self.assertIsNone(geometry(R,E,0x40020,helper_delta=None,opaque_stack_preserved=True)[0x4005a])
    def test_bad_edge(self):self.assertRaises(ValueError,geometry,R,E+[[0x40020,1]],0x40020)
    def test_exit_difference(self):
        rs=copy.deepcopy(R);next(r for r in rs if r['site_rva']==0x40070)['operands'][1]['constant']=28;self.assertEqual(geometry(rs,E,0x40020,opaque_stack_preserved=True)[0x400c1],-4)
    def test_forged_witness(self):
        d=copy.deepcopy(D);d['invented_verification']['witness_preinstruction_esp_relative_entry'][0]['esp_delta']+=4;self.assertRaises(ValueError,validate,d,A,B)
    def test_unknown_not_zero(self):self.assertIsNone(geometry(R,E,0x40020)[0x400c1])
if __name__=='__main__':unittest.main()
