import unittest
from tools.stoneage_2001_sina_client_topology_probe import (
    TARGET_AID,TARGET_FILENAME,TARGET_COL,extract_links,filename_path_templates
)

class Sina2001ClientTopologyTests(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(TARGET_AID,41967)
        self.assertEqual(TARGET_FILENAME,"stoneage2.0setup.exe")
        self.assertEqual(TARGET_COL,"demo")

    def test_extract_binary(self):
        b=b'<a href="http://down.example.com/client/foo.exe">download</a>'
        self.assertIn("http://down.example.com/client/foo.exe",extract_links(b,"http://x/"))

    def test_substitute(self):
        r=filename_path_templates("http://down.example.com/client/foo.exe",TARGET_FILENAME)
        self.assertIn("http://down.example.com/client/stoneage2.0setup.exe",r)

if __name__=="__main__":
    unittest.main()
