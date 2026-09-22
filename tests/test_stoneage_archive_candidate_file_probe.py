import unittest
from tools.stoneage_archive_candidate_file_probe import (
    HIGH,
    LOW,
    QUERIES,
    candidate_files,
)

class ArchiveCandidateFileProbeTests(unittest.TestCase):
    def test_japan_174a_launch_metadata_queries_are_pinned(self):
        self.assertIn('"sa174hg.exe"',QUERIES)
        self.assertIn(
            '"hangame.gamania.co.jp/stoneage/sa174hg.exe"',
            QUERIES,
        )
        self.assertIn('"StoneAge" AND "1.74a"',QUERIES)
        self.assertIn('"STONE AGE" AND "248MB"',QUERIES)
        self.assertIn('"4988609011565"',QUERIES)
        self.assertIn('"WR-04156"',QUERIES)
        self.assertIn('"item-city.com" AND "product_id=423"',QUERIES)

    def test_korea_174_launch_metadata_queries_are_pinned(self):
        self.assertIn('"스톤에이지" AND "1.74"',QUERIES)
        self.assertIn('"StoneAge" AND "1.74"',QUERIES)
        self.assertIn('"넷마블" AND "스톤에이지"',QUERIES)
        self.assertIn('"Netmarble" AND "StoneAge"',QUERIES)
        self.assertIn('"game3.netmarble.net/stoneage"',QUERIES)
        self.assertIn('"game3.netmarble.net" AND "stoneage"',QUERIES)
        self.assertIn('"20030728" AND "StoneAge"',QUERIES)

    def test_exact_name(self):
        rows=candidate_files([{"name":"client/sa_demo.exe","size":"123"}])
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["exact"])
    def test_gametime_trial_exact_name(self):
        rows=candidate_files([{"name":"mirror/stone_demo.exe","size":"245366784"}])
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["exact"])
    def test_gametime_record9_exact_name(self):
        rows=candidate_files([{"name":"mirror/ONLSTONEAGE.ZIP","size":"123"}])
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["exact"])
    def test_size_window(self):
        rows=candidate_files([{"name":"mystery.bin","size":str(250*1024*1024)}])
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["size_match"])
    def test_irrelevant(self):
        self.assertEqual(candidate_files([{"name":"foo.txt","size":"100"}]),[])

    def test_japan_174a_exact_name(self):
        rows=candidate_files([{"name":"mirror/sa174hg.exe","size":"123"}])
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["exact"])

if __name__=="__main__":unittest.main()
