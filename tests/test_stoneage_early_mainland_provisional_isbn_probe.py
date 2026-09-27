import unittest
from tools.stoneage_early_mainland_provisional_isbn_probe import (
    ISBN10_HYPHEN, ISBN13_HYPHEN, isbn10_valid, isbn13_valid, exact_candidate_hit
)

class ProvisionalISBNProbeTests(unittest.TestCase):
    def test_candidate_checksums(self):
        self.assertTrue(isbn10_valid(ISBN10_HYPHEN))
        self.assertTrue(isbn13_valid(ISBN13_HYPHEN))
    def test_exact_candidate_hit(self):
        self.assertTrue(exact_candidate_hit({"title":"StoneAge","description":"ISBN 7-900323-57-0"}))
        self.assertTrue(exact_candidate_hit({"filename":"9787900323576.iso"}))
        self.assertFalse(exact_candidate_hit({"title":"广西金海湾 其他产品"}))

if __name__=="__main__":
    unittest.main()
