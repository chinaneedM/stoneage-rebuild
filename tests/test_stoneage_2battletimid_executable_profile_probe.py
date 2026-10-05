import tempfile
from pathlib import Path
import unittest

from tools.stoneage_2battletimid_executable_profile_probe import (
    analyze_search_root,
    classify_2battletimid_profile,
)


class TwoBattleTimidExecutableProfileProbeTests(unittest.TestCase):
    def test_classifier_never_promotes_symbol_presence_to_profile_truth(self):
        self.assertEqual(
            classify_2battletimid_profile(
                petskill_symbol_present=True,
                attackdamage_symbol_present=True,
            ),
            "inconclusive_no_callback_local_literal_identity",
        )
        self.assertEqual(
            classify_2battletimid_profile(
                petskill_symbol_present=False,
                attackdamage_symbol_present=True,
            ),
            "inconclusive_callback_symbol_unavailable",
        )
        self.assertEqual(
            classify_2battletimid_profile(
                petskill_symbol_present=True,
                attackdamage_symbol_present=False,
            ),
            "inconclusive_attackdamage_symbol_unavailable",
        )

    def test_non_elf_files_do_not_become_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"plain").write_bytes(b"not-elf")
            rows=analyze_search_root(root)
        self.assertIn("SCAN|elf_candidates=0",rows)
        self.assertIn(
            "PROFILE_SIGNAL|literal_charset="
            "inconclusive_attackdamage_symbol_unavailable",
            rows,
        )
        self.assertIn(
            "RESOLUTION|2BATTLETIMID_EXECUTABLE_PROFILE_DISCRIMINATOR_ATTEMPTED",
            rows,
        )


if __name__=="__main__":
    unittest.main()
