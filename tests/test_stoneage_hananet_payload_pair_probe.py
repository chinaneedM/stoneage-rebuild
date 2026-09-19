import unittest
from tools.stoneage_hananet_payload_pair_probe import availability,replay,safe

class HananetPayloadPairProbeTests(unittest.TestCase):
    def test_replay(self):
        self.assertEqual(replay("20010814230641","http://x/sa_demo.exe"),"https://web.archive.org/web/20010814230641id_/http://x/sa_demo.exe")
    def test_safe_pipe(self):
        self.assertEqual(safe("a|b"),"a%7Cb")

if __name__=="__main__":unittest.main()
