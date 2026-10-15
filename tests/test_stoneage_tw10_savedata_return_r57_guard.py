import copy,unittest
from tools.stoneage_tw10_savedata_return_r57 import analyze
from tools.stoneage_tw10_savedata_return_r57_guard import audit
from tests.test_stoneage_tw10_savedata_return_r57 import row,c

def context(rows,edges):
 d=c(rows,edges);d['return_analysis']=analyze(d);return d
class ReverseTests(unittest.TestCase):
 def test_definition(self):self.assertEqual(audit(context([row(10,'mov',('eax',)),row(11,'ret')],[[10,11]])),1)
 def test_opaque(self):self.assertEqual(audit(context([row(10,'call'),row(11,'ret')],[[10,11]])),1)
 def test_entry(self):self.assertEqual(audit(context([row(10,'ret')],[])),1)
 def test_join(self):
  d=context([row(10),row(11,'mov',('eax',)),row(12,'mov',('eax',)),row(13,'ret')],[[10,11],[10,12],[11,13],[12,13]]);self.assertEqual(audit(d),1)
 def test_raw_cdq_not_overlay(self):
  d=context([row(10,'mov',('eax',)),row(11,'cdq',('eax','edx'),('eax',)),row(12,'ret')],[[10,11],[11,12]]);self.assertEqual(audit(d),2)
 def test_loop(self):
  d=context([row(10),row(11,'mov',('eax',),('eax',)),row(12,'ret')],[[10,11],[11,11],[11,12]]);self.assertEqual(audit(d),2)
 def test_promote(self):
  d=context([row(10,'ret')],[]);d['return_analysis']['actual_written_count_close_flush_or_persistence_proven']=True;self.assertRaises(ValueError,audit,d)
 def test_missing_source(self):
  d=context([row(10,'call'),row(11,'ret')],[[10,11]]);d['return_analysis']['return_contexts'][0]['eax_source_graph']['queries'][0]['source_candidates']=[];self.assertRaises(ValueError,audit,d)
if __name__=='__main__':unittest.main()
