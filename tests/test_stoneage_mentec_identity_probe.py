import unittest

from tools.stoneage_mentec_identity_probe import DOMAINS, TERMS, snippets


class MentecIdentityProbeTests(unittest.TestCase):
    def test_candidate_domains_are_bounded(self):
        self.assertEqual(
            DOMAINS,
            ["mentec.co.kr","mentech.co.kr","mantech.co.kr","man-tech.co.kr"],
        )

    def test_identity_terms_require_period_context(self):
        rows=snippets("삼성전자 PC교육센터 운영 업체 멘테크")
        self.assertTrue(rows)
        self.assertTrue(TERMS.search("PC 교육센터"))
        self.assertFalse(TERMS.search("unrelated pressure sensor company"))


if __name__=="__main__":
    unittest.main()
