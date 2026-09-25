import unittest
from tools.stoneage_2000_sina_hostwide_filename_probe import HOSTROOT,TARGET,relevant

class HostwideFilenameProbeTests(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(HOSTROOT,"http://202.106.184.193/downfiles/")
        self.assertEqual(TARGET,"samap_1220.zip")

    def test_relevant(self):
        rows=[
            {"original":"http://202.106.184.193/downfiles/x/samap_1220.zip"},
            {"original":"http://202.106.184.193/downfiles/x/other.zip"},
            {"original":"http://202.106.184.193/downfiles/x/stoneage-map.zip"},
        ]
        self.assertEqual(len(relevant(rows)),2)

if __name__=="__main__":
    unittest.main()
