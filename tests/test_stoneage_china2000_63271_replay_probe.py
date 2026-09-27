import unittest
from tools.stoneage_china2000_63271_replay_probe import (
    PageParser,
    classify,
    decode_score,
    replay_url,
)

class China200063271ReplayProbeTests(unittest.TestCase):
    def test_replay_url(self):
        u=replay_url("20010309223137","id_")
        self.assertIn("20010309223137id_",u)
        self.assertIn("63271.html",u)

    def test_parser_scrubs_queries_and_external(self):
        p=PageParser()
        p.feed('<html><head><title>测试名单</title></head><body><a href="/x/y.html?a=secret">x</a><a href="mailto:a@b.com">m</a><a href="https://example.com/z">e</a></body></html>')
        self.assertEqual("".join(p.title_parts),"测试名单")
        self.assertIn("/x/y.html",p.paths)
        self.assertEqual(len(p.paths),1)

    def test_classify_recipient_page_without_emitting_people(self):
        role,arch,privacy=classify("石器时代 赠送 名单 姓名 地址 邮编")
        self.assertEqual(role,"GIVEAWAY_RESULTS_OR_RECIPIENT_LIST")
        self.assertGreater(arch.get("名单",0),0)
        self.assertGreater(privacy.get("地址",0),0)

    def test_chinese_decode_score(self):
        self.assertGreater(decode_score("石器时代 测试光盘 名单 地址"),decode_score("garbled text"))

if __name__=="__main__":
    unittest.main()
