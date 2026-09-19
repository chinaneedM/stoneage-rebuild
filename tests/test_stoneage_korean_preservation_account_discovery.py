import unittest

from tools.stoneage_korean_preservation_account_discovery import (
    ITEM_RE,
    parse_identifiers,
)


class KoreanPreservationAccountDiscoveryTests(unittest.TestCase):
    def test_item_regex_only_accepts_corpus_item_rows(self):
        self.assertIsNotNone(ITEM_RE.match("ITEM|identifier=abc|title=x|date=2001"))
        self.assertIsNone(ITEM_RE.match("CARRIER|identifier=abc|name=disc.iso"))

    def test_parse_identifiers_deduplicates_in_order(self):
        text = "\n".join(
            [
                "ITEM|identifier=a|title=A",
                "CARRIER|identifier=a|name=disc.iso",
                "ITEM|identifier=b|title=B",
                "ITEM|identifier=a|title=A again",
            ]
        )
        self.assertEqual(parse_identifiers(text), ["a", "b"])


if __name__ == "__main__":
    unittest.main()
