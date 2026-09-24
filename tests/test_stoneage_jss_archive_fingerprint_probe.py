import unittest

from tools.stoneage_jss_archive_fingerprint_probe import (
    KNOWN_MD5,
    KNOWN_SHA1,
    KNOWN_SIZE,
    QUERIES,
    candidate_files,
    strength,
)


class JssArchiveFingerprintProbeTests(unittest.TestCase):
    def test_queries_pin_first_party_traits(self):
        joined="\n".join(QUERIES)
        self.assertIn("SaUpdate.exe",joined)
        self.assertIn("update.gamersdream.ne.jp",joined)
        self.assertIn("newest.txt",joined)
        self.assertIn(KNOWN_MD5,joined)
        self.assertIn(KNOWN_SHA1,joined)

    def test_known_hash_is_strong(self):
        rows=candidate_files([{
            "name":"misc.bin","size":"1","md5":KNOWN_MD5,"sha1":"x",
        }])
        self.assertEqual(len(rows),1)
        self.assertEqual(strength(rows[0]),"HASH")

    def test_name_size_pair(self):
        rows=candidate_files([{
            "name":"StoneAge/stoneage.exe","size":str(KNOWN_SIZE),
        }])
        self.assertEqual(len(rows),1)
        self.assertEqual(strength(rows[0]),"NAME_SIZE")

    def test_manifest_and_resource_names(self):
        rows=candidate_files([
            {"name":"backup/newest.txt","size":"123"},
            {"name":"data/soundaddr_12.txt","size":"456"},
        ])
        self.assertEqual(len(rows),2)
        self.assertEqual(strength(rows[0]),"MANIFEST_NAME")
        self.assertEqual(strength(rows[1]),"JSS_RESOURCE_NAME")

    def test_irrelevant_file_is_ignored(self):
        self.assertEqual(candidate_files([{"name":"readme.txt","size":"100"}]),[])


if __name__=="__main__":
    unittest.main()
