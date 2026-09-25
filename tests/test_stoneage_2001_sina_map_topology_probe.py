import unittest
from tools.stoneage_2001_sina_map_topology_probe import extract_links,filename_path_templates
class TopologyTests(unittest.TestCase):
    def test_extract_binary_link(self):
        b=b'<a href="http://down.example.com/map/foo.exe">download</a>'
        self.assertEqual(extract_links(b,"http://x/"),("http://down.example.com/map/foo.exe",))
    def test_substitute_target(self):
        r=filename_path_templates("http://down.example.com/map/foo.exe","Estoneage2.0map_1127.exe")
        self.assertIn("http://down.example.com/map/Estoneage2.0map_1127.exe",r)
if __name__=="__main__": unittest.main()
