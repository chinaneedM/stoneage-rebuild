import unittest
from tools.stoneage_waei_fileid133_header_probe import URL
class HeaderProbeTests(unittest.TestCase):
    def test_url(self):
        self.assertIn("20010605174213id_",URL)
        self.assertIn("fileid=133",URL)
if __name__=="__main__":unittest.main()
