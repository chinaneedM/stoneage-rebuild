import unittest

from tools.stoneage_sa25_pcpc_source_replay_probe import (
    TARGETS, interesting_hrefs, normalized_visible, replay_url, token_context
)


class SA25PcpcSourceReplayProbeTests(unittest.TestCase):
    def test_capture_dates_are_pinned(self):
        self.assertEqual(TARGETS[0][1],"20030605104851")
        self.assertEqual(TARGETS[1][1],"20031203042412")

    def test_raw_replay_url(self):
        u=replay_url("20030605104851","http://pcpc.idv.tw:80/soft/soft.htm")
        self.assertIn("20030605104851id_",u)
        self.assertTrue(u.endswith("http://pcpc.idv.tw:80/soft/soft.htm"))

    def test_interesting_href(self):
        html='<a href="http://202.104.32.168/file/game/maoxian/sa25up.zip">x</a><a href="x.exe">y</a>'
        self.assertEqual(
            interesting_hrefs(html),
            ("http://202.104.32.168/file/game/maoxian/sa25up.zip",),
        )

    def test_visible_context(self):
        html='<b>[下載]</b> 石器時代2.5 <a href="x">sa25up.zip</a>'
        visible=normalized_visible(html)
        self.assertIn("石器時代2.5",visible)
        self.assertIn("sa25up.zip",visible)
        self.assertIn("sa25up.zip",token_context(visible,"sa25up.zip"))


if __name__=="__main__":
    unittest.main()
