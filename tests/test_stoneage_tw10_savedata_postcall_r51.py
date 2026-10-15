import unittest,copy,json,hashlib
from pathlib import Path
from tools.stoneage_tw10_savedata_postcall_r51 import return_candidates,derive,validate
from tests.test_stoneage_tw10_savedata_application_r51 import row,reg,imm
class NormalReturnGeometry(unittest.TestCase):
    def test_plain_ret(self):self.assertEqual(return_candidates([row(1,'ret')],[],1)[0]['conditional_net_near_call_esp_delta'],0)
    def test_callee_cleanup(self):self.assertEqual(return_candidates([row(1,'ret',[imm(8)])],[],1)[0]['conditional_net_near_call_esp_delta'],8)
    def test_balanced_push_pop(self):
        r=return_candidates([row(1,'push',[reg('ebx')]),row(2,'pop',[reg('ebx')]),row(3,'ret')],[[1,2],[2,3]],1);self.assertEqual(r[0]['conditional_net_near_call_esp_delta'],0)
    def test_unbalanced_push(self):
        r=return_candidates([row(1,'push',[reg('ebx')]),row(2,'ret')],[[1,2]],1);self.assertEqual(r[0]['conditional_net_near_call_esp_delta'],-4)
    def test_unknown_call(self):
        r=return_candidates([row(1,'call'),row(2,'ret')],[[1,2]],1);self.assertIsNone(r[0]['conditional_net_near_call_esp_delta'])
    def test_far_return(self):self.assertIsNone(return_candidates([row(1,'retf')],[],1)[0]['conditional_net_near_call_esp_delta'])
    def test_trap_exit(self):self.assertIsNone(return_candidates([row(1,'ud2')],[],1)[0]['conditional_net_near_call_esp_delta'])
    def test_distinct_cleanup_paths(self):
        r=return_candidates([row(1,'je'),row(2,'ret'),row(3,'ret',[imm(4)])],[[1,2],[1,3]],1);self.assertEqual([x['conditional_net_near_call_esp_delta'] for x in r],[0,4])
class PinnedPostcall(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=Path('research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R51-ORIGINAL.json').read_bytes();cls.contract=derive(cls.raw)
    def test_valid(self):self.assertTrue(validate(self.contract,self.raw))
    def test_digest(self):
        with self.assertRaises(ValueError):derive(self.raw+b' ')
    def test_contract_type(self):
        c=copy.deepcopy(self.contract);c['actual_stack_alias_processor_output_length_schema_or_execution_proven']=0
        with self.assertRaises(ValueError):validate(c,self.raw)
    def test_schema(self):
        d=json.loads(self.raw);d['schema']='other';raw=json.dumps(d).encode()
        with self.assertRaises(ValueError):derive(raw,hashlib.sha256(raw).hexdigest())
    def test_missing_inventory(self):
        d=json.loads(self.raw);d['processor_instruction_shapes'].pop();raw=json.dumps(d).encode()
        with self.assertRaises(ValueError):derive(raw,hashlib.sha256(raw).hexdigest())
    def test_cleanup_changes_coordinate(self):
        d=json.loads(self.raw);r=next(r for r in d['processor_instruction_shapes'] if r['mnemonic']=='ret');r['operands']=[imm(4)];raw=json.dumps(d).encode()
        c=derive(raw,hashlib.sha256(raw).hexdigest());self.assertEqual(c['conditional_normal_return_net_esp_delta_candidates'],[4]);self.assertEqual(c['candidate_matching_caller_lea_coordinates'][0]['destination_register'],'edx')
if __name__=='__main__':unittest.main()
