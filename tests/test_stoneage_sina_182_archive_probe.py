import unittest

from tools.stoneage_sina_182_archive_probe import (
    TARGET, BASENAME, cdx_url, nested_file_rows
)


class Sina182ArchiveProbeTests(unittest.TestCase):
    def test_target_is_pinned_without_version_promotion(self):
        self.assertEqual(TARGET,"ftp://211.90.133.5/dowload/sa/sa1.82.exe")
        self.assertEqual(BASENAME,"sa1.82.exe")

    def test_cdx_exact_and_wildcard_urls(self):
        exact=cdx_url(TARGET,False)
        wildcard=cdx_url(TARGET.rsplit("/",1)[0]+"/",True)
        self.assertIn("output=json",exact)
        self.assertIn("sa1.82.exe",exact)
        self.assertIn("%2A",wildcard)

    def test_nested_rows(self):
        sample=[{"itemid":1,"itemName":"x","fileid":"foo/sa1.82.exe","filename":"sa1.82.exe"}]
        rows=nested_file_rows(sample)
        self.assertEqual(len(rows),1)


if __name__=="__main__":
    unittest.main()
