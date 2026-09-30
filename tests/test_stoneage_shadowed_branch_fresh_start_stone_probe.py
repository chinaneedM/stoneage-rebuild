import tempfile
import unittest
from pathlib import Path

from tools.stoneage_shadowed_branch_fresh_start_stone_probe import (
    _setup_unique_int,
)


class FreshStartStoneProbeTests(unittest.TestCase):

    def test_setup_unique_int_reads_exact_key(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"setup.cf"
            p.write_text(
                "# comment\nOTHERGOLD=999\nGOLD=30000\n",
                encoding="utf-8",
            )
            self.assertEqual(_setup_unique_int(p,"GOLD"),30000)

    def test_setup_unique_int_rejects_duplicates(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"setup.cf"
            p.write_text("GOLD=1\nGOLD=2\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                _setup_unique_int(p,"GOLD")

    def test_setup_unique_int_rejects_noninteger(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"setup.cf"
            p.write_text("GOLD=abc\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                _setup_unique_int(p,"GOLD")


if __name__=="__main__":
    unittest.main()
