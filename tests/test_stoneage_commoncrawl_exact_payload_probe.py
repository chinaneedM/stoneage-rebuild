import unittest
from tools.stoneage_commoncrawl_exact_payload_probe import clean

class CommonCrawlExactPayloadProbeTests(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(clean("a|b\n c"),"a%7Cb c")

if __name__=="__main__":unittest.main()
