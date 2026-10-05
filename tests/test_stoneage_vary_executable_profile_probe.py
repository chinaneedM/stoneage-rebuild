import unittest

from tools.stoneage_vary_executable_profile_probe import (
    _little_u32_count,
    _strstr_calls,
    classify_vary_profile,
)


class VaryExecutableProfileProbeTests(unittest.TestCase):
    def test_profile_classification_is_deliberately_narrow(self):
        self.assertEqual(
            classify_vary_profile(symbol_present=True, strstr_calls=2),
            "gavin_iris_attack_quick",
        )
        self.assertEqual(
            classify_vary_profile(symbol_present=True, strstr_calls=3),
            "bismarck_attack_defense_quick",
        )
        self.assertEqual(
            classify_vary_profile(symbol_present=False, strstr_calls=3),
            "inconclusive_symbol_unavailable",
        )
        self.assertEqual(
            classify_vary_profile(symbol_present=True, strstr_calls=4),
            "inconclusive_call_shape",
        )

    def test_strstr_call_counter_ignores_non_calls(self):
        disassembly = """
0000 <PETSKILL_Vary>:
  10: call 20 <strstr@plt>
  20: mov eax,0
  30: call 40 <strstr>
  40: lea eax,[strstr@GOT]
"""
        self.assertEqual(_strstr_calls(disassembly), 2)

    def test_u32_scan_is_exact_little_endian(self):
        data = b"x" + (600).to_bytes(4, "little") * 2 + b"y"
        self.assertEqual(_little_u32_count(data, 600), 2)
        self.assertEqual(_little_u32_count(data, 601), 0)


if __name__ == "__main__":
    unittest.main()
