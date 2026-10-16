import unittest
from tools.stoneage_tw10_savedata_r77_preflight_guard import scan,number,validate

class R77CensusTests(unittest.TestCase):
 def scan(self,x):return scan(x,['rva','va'],['entry_rva'],['operands','ops'],[321787])[321787]
 def test_retained_manifest_replay(self):self.assertEqual(validate('research/recovered/STONEAGE-TW10-SAVEDATA-R77-REFRESH-PREFLIGHT.json')['numeric_references'],[13,28])
 def test_hex_va_and_empty_operands(self):self.assertEqual(self.scan({'va':hex(4194304+321787),'mnemonic':'ret','ops':[]})['decoded'],[('$','ret')])
 def test_boolean_not_address(self):self.assertIsNone(number(True))
 def test_malformed_not_address(self):self.assertIsNone(number('not an address'))
 def test_reference_not_decoded(self):self.assertEqual(self.scan({'callee':321787})['decoded'],[])
 def test_root_not_decoded(self):
  d=self.scan({'entry_rva':321787});self.assertEqual(d['roots'],['$']);self.assertEqual(d['decoded'],[])
 def test_sibling_operands_not_same_object(self):self.assertEqual(self.scan([{'rva':321787},{'mnemonic':'mov','operands':[]}])['decoded'],[])
 def test_nested_same_object(self):self.assertEqual(self.scan({'x':[{'rva':'0x4e8fb','mnemonic':'ret','operands':[]}]})['decoded'],[('$.x[0]','ret')])
 def test_nonarray_operands_not_decoded(self):self.assertEqual(self.scan({'rva':321787,'mnemonic':'ret','operands':'[]'})['decoded'],[])
if __name__=='__main__':unittest.main()
