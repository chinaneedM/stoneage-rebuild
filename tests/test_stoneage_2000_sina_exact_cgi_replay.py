import unittest
from tools.stoneage_2000_sina_exact_cgi_replay import candidates, relevant_lines, TARGET, TS

class ExactCGIReplayTests(unittest.TestCase):
    def test_target(self):
        self.assertEqual(TARGET,"samap_1220.zip")
        self.assertEqual(TS,"20010126074600")

    def test_candidate_link(self):
        b=b'<a href="http://down.example.com/maps/samap_1220.zip">download</a>'
        self.assertEqual(candidates(b),("http://down.example.com/maps/samap_1220.zip",))

    def test_script_location(self):
        b=b'<script>window.location="http://down.example.com/file.zip";</script>'
        self.assertIn("http://down.example.com/file.zip",candidates(b))

    def test_relevant_lines(self):
        self.assertTrue(relevant_lines(b'download map'))

if __name__=="__main__":
    unittest.main()
