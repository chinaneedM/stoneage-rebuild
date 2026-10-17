import unittest
from tools.stoneage_tw10_login_avatar_probe import select_calls,inspect_runtime
class ScopeTests(unittest.TestCase):
 def test_wrong_version_rejected_before_decoding(self):
  with self.assertRaisesRegex(ValueError,'SHA256'):inspect_runtime(b'later client')
 def test_candidate_bounds_not_nearest_function_claim(self):
  rows=[{'target_rva':v} for v in [99,100,131,132,133]]
  self.assertEqual(select_calls(rows,132),rows[1:4])
 def test_empty_does_not_invent_entry(self):self.assertEqual(select_calls([],100),[])
if __name__=='__main__':unittest.main()
