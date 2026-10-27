import unittest
from tools.stoneage_preserved_npc_delta_r41 import arg_delta,configuration_profile,decode_fields

class SourceDeltaTests(unittest.TestCase):
 def test_exact_transcode_and_text_fingerprints(self):
  text='entype:2\nstartmsg:測試\nenemyno:1,1,2\ntime:180\n'
  r=arg_delta(text.encode('cp950'),text.encode('gb18030'))
  self.assertFalse(r['raw_bytes_equal']);self.assertEqual(r['old_bytes'],r['modern_bytes'])
  self.assertIn('cp950',r['exact_transcode_candidates']);self.assertIn('big5',r['exact_transcode_candidates'])
  self.assertEqual(r['modern_fields'][2]['numbers'],[1,1,2]);self.assertNotIn('測試',str(r))
 def test_numeric_change_not_called_transcode(self):
  old='entype:2\nstartmsg:測試\ntime:180\n'.encode('cp950')
  modern='entype:2\nstartmsg:測試\ntime:181\n'.encode('gb18030')
  self.assertNotIn('cp950',arg_delta(old,modern)['exact_transcode_candidates'])
 def test_newline_difference_not_called_exact_transcode(self):
  text='entype:2\nstartmsg:測試\n'
  r=arg_delta(text.replace('\n','\r\n').encode('cp950'),text.encode('gb18030'))
  profile=next(p for p in r['decode_candidates'] if p['codec']=='cp950')
  self.assertTrue(profile['newline_normalized_text_equal']);self.assertFalse(profile['exact_transcode_to_modern_gb18030'])
 def test_configuration_no_full_text_and_no_number_loss(self):
  raw='# comment\n{\nx = 26\nenemy = sb_kbu|file:100/sb_kbu.arg\nname = 風的守護獸\n}\n'.encode('cp950')
  r=configuration_profile(raw,'cp950');self.assertEqual(r['line_profiles'][2]['numbers'],[26])
  self.assertNotIn('風的守護獸',str(r));self.assertEqual(r['line_profiles'][3]['ascii_token'],'sb_kbu|file:100/sb_kbu.arg')
 def test_malformed_argument_is_explicit(self):self.assertIsNone(decode_fields('not an assignment'))
if __name__=='__main__':unittest.main()
