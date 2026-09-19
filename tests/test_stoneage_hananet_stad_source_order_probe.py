import unittest
from tools.stoneage_hananet_stad_source_order_probe import contexts

class StadSourceOrderProbeTests(unittest.TestCase):
    def test_context_positions(self):
        text="aaa sa.exe bbb sa_demo.exe ccc"
        self.assertEqual(contexts(text,"sa.exe",3)[0][0],4)
        self.assertEqual(contexts(text,"sa_demo.exe",3)[0][0],15)

if __name__=="__main__":unittest.main()
