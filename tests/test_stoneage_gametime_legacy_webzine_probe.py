import unittest

from tools.stoneage_gametime_legacy_webzine_probe import plain


class GameTimeLegacyWebzineProbeTests(unittest.TestCase):
    def test_plain_strips_markup(self):
        self.assertEqual(plain("<b>StoneAge</b>   download"), "StoneAge download")


if __name__=="__main__":
    unittest.main()
