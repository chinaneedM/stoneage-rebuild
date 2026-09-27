import unittest
from tools.stoneage_sa40_direct_archive_probe import TARGETS,arq_cdx

class SA40DirectArchiveTests(unittest.TestCase):
    def test_target_variants(self):
        self.assertEqual(len(TARGETS),2)
        self.assertTrue(all("updatex_1024/shiqi4updatex_02_11_08.zip" in u for u in TARGETS))
        self.assertTrue(any(":80/" in u for u in TARGETS))

    def test_arquivo_url(self):
        self.assertIn("arquivo.pt/wayback/cdx",arq_cdx(TARGETS[0]))

if __name__=="__main__":
    unittest.main()
