import copy,json,unittest
from pathlib import Path
from tools.stoneage_tw10_savedata_writer_r54_contract import derive,validate,physical_pushes
P=Path(__file__).resolve().parents[1]/'research/recovered/STONEAGE-TW10-SAVEDATA-NATIVE-IO-R54-ORIGINAL.json'
class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw=P.read_bytes();cls.d=derive(cls.raw)
    def test_custody(self):self.assertRaises(ValueError,derive,self.raw+b' ')
    def test_missing_source(self):self.assertRaises(ValueError,derive,b'{}')
    def test_replay(self):self.assertTrue(validate(self.d,self.raw))
    def test_bool_type_confusion(self):
        d=copy.deepcopy(self.d);d['local_straight_line_verified']=1;self.assertRaises(ValueError,validate,d,self.raw)
    def test_promotion(self):
        d=copy.deepcopy(self.d);d['actual_bytes_copy_size_inverse_schema_migration_or_persistence_proven']=True;self.assertRaises(ValueError,validate,d,self.raw)
    def test_slot_constants(self):
        ps=self.d['physical_pushes'];self.assertEqual([p['input'].get('constant') for p in ps],[None,127,0,None,None,4000])
    def test_local_addresses(self):self.assertEqual([x['conditional_pre_call_esp_relative_address'] for x in self.d['conditional_caller_lea_coordinates']],[36,32,164,36])
    def test_slot_mutation_retained(self):
        refs=self.d['processor_entry_coordinates']['references'];self.assertTrue(any(x['site_rva']==0x470f5 and x['decoder_write'] for x in refs))
    def test_no_actual_inverse(self):self.assertFalse(self.d['historical_writer_equals_invented_inverse_for_arbitrary_key_proven'])
    def test_repeat_boundary(self):
        d=copy.deepcopy(self.d);d['copy_syntax']['conditional_total_if_rep_count_direction_segments_and_addresses_valid']=128;self.assertRaises(ValueError,validate,d,self.raw)
    def test_push_width(self):
        r={'site_rva':1,'mnemonic':'push','operands':[{'kind':'immediate','width_bytes':2,'constant':0}],'decoder_written_registers':['esp']};self.assertRaises(ValueError,physical_pushes,[r],2)
    def test_opaque_call_stops(self):
        rs=[{'site_rva':1,'mnemonic':'call','operands':[],'decoder_written_registers':[]},{'site_rva':2,'mnemonic':'push','operands':[{'kind':'immediate','width_bytes':4,'constant':0}],'decoder_written_registers':['esp']}];self.assertEqual(len(physical_pushes(rs,3)),1)
if __name__=='__main__':unittest.main()
