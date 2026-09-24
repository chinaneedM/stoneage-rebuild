import unittest
from types import SimpleNamespace

from tools.stoneage_jss_saupdate_helper_semantics_probe import (
    generation_selector_summary,
)


class JssSaUpdateHelperSemanticsProbeTests(unittest.TestCase):
    def test_generation_selector_summary_extracts_arg1_immediates(self):
        callers = [
            (0x1000, ((0x0, "imm:0x2"), (0x0, "stack:+0xc"))),
            (0x1010, ((0x0, "imm:0x8"),)),
            (0x1020, ((0x0, "register:eax"),)),
        ]
        self.assertEqual(generation_selector_summary(callers), (2, 8))


if __name__ == "__main__":
    unittest.main()
