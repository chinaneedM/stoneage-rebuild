import unittest
from tools.stoneage_preserved_genkou_third_r42 import finite_diff,fingerprint
class R42SourceTests(unittest.TestCase):
 def test_distinct_numbers_repeated_positions_and_message_privacy(self):
  a='entype:2\nstartmsg:測試\nenemyno:1,1,2\ntime:180\n'.encode('cp950')
  b='entype:2\nstartmsg:另一段\nenemyno:2,2,5\ntime:180\n'.encode('cp950')
  d=finite_diff(a,b)
  self.assertEqual(d['numeric_differences'],[{'field':'enemyno','kbu':[1,1,2],'kgi':[2,2,5]}])
  self.assertEqual(d['changed_fields'],['startmsg','enemyno'])
  self.assertEqual(d['unchanged_fields'],['entype','time'])
  self.assertNotIn('測試',str(d));self.assertNotIn('另一段',str(d))
  self.assertFalse(d['full_text_or_payload_published'])
 def test_add_and_drop_distinct_keys(self):
  a='entype:2\ntime:180\n'.encode()
  b='entype:2\nother:3\n'.encode()
  d=finite_diff(a,b)
  self.assertEqual(d['kbu_only_keys'],['time'])
  self.assertEqual(d['kgi_only_keys'],['other'])
 def test_duplicate_key_rejected(self):
  with self.assertRaises(Exception):fingerprint(b'time:1\ntime:2\n')
 def test_unknown_format_rejected(self):
  with self.assertRaises(Exception):fingerprint(b'not an assignment\n')
 def test_source_full_hash_constraints(self):
  from tools.stoneage_preserved_genkou_third_r42 import ORIGINAL_KGI
  self.assertEqual(ORIGINAL_KGI[1],281)
  self.assertEqual(len(ORIGINAL_KGI[2]),64)
if __name__=='__main__':unittest.main()
