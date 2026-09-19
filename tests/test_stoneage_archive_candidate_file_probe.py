import unittest
from tools.stoneage_archive_candidate_file_probe import candidate_files,LOW,HIGH

class ArchiveCandidateFileProbeTests(unittest.TestCase):
    def test_exact_name(self):
        rows=candidate_files([{"name":"client/sa_demo.exe","size":"123"}])
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["exact"])
    def test_gametime_trial_exact_name(self):
        rows=candidate_files([{"name":"mirror/stone_demo.exe","size":"245366784"}])
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["exact"])
    def test_size_window(self):
        rows=candidate_files([{"name":"mystery.bin","size":str(250*1024*1024)}])
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["size_match"])
    def test_irrelevant(self):
        self.assertEqual(candidate_files([{"name":"foo.txt","size":"100"}]),[])

if __name__=="__main__":unittest.main()
