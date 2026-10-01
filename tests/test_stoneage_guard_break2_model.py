import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_guard_break2_model import (
    GuardBreak2UndefinedSourceDomain,
    resolve_guard_break2_damage_step,
)


class GuardBreak2ModelTests(unittest.TestCase):
    def test_guard_branch_multiplies_by_1_3_before_guard_adjust(self):
        result=resolve_guard_break2_damage_step(
            101,
            defender_command_is_guard=True,
            defender_confusion_counter=0,
        )
        self.assertEqual(result.damage_after_multiplier,131)
        self.assertEqual(result.multiplier,1.3)
        self.assertTrue(result.guard_adjust_applies_after_multiplier)

    def test_non_guard_branch_reduces_to_70_percent(self):
        result=resolve_guard_break2_damage_step(
            101,
            defender_command_is_guard=False,
        )
        self.assertEqual(result.damage_after_multiplier,70)
        self.assertEqual(result.multiplier,0.7)
        self.assertFalse(result.guard_adjust_applies_after_multiplier)

    def test_confused_guard_still_gets_1_3_but_skips_guard_adjust(self):
        result=resolve_guard_break2_damage_step(
            100,
            defender_command_is_guard=True,
            defender_confusion_counter=1,
        )
        self.assertEqual(result.damage_after_multiplier,130)
        self.assertFalse(result.guard_adjust_applies_after_multiplier)

    def test_source_int_assignment_truncates_positive_fraction(self):
        self.assertEqual(
            resolve_guard_break2_damage_step(
                3,defender_command_is_guard=False
            ).damage_after_multiplier,
            2,
        )
        self.assertEqual(
            resolve_guard_break2_damage_step(
                11,defender_command_is_guard=True
            ).damage_after_multiplier,
            14,
        )

    def test_invalid_or_overflow_domain_fails_closed(self):
        with self.assertRaises(GuardBreak2UndefinedSourceDomain):
            resolve_guard_break2_damage_step(
                -1,defender_command_is_guard=False
            )
        with self.assertRaises(GuardBreak2UndefinedSourceDomain):
            resolve_guard_break2_damage_step(
                2**31-1,defender_command_is_guard=True
            )

    @unittest.skipUnless(shutil.which("cc"), "C compiler unavailable")
    def test_multiplier_matches_c_double_to_int_assignment(self):
        code=r"""
        #include <stdio.h>
        int main(void) {
          int d,g;
          while (scanf("%d%d",&d,&g)==2) {
            if (g) d=d*1.3;
            else d=d*0.7;
            printf("%d\n",d);
          }
          return 0;
        }
        """
        cases=((0,0),(1,0),(3,0),(101,0),(1,1),(11,1),(101,1))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/"oracle.c").write_text(code)
            subprocess.run(
                ["cc","-std=c99","-O0",str(root/"oracle.c"),"-o",str(root/"oracle")],
                check=True,
            )
            output=subprocess.check_output(
                [str(root/"oracle")],
                text=True,
                input="".join(f"{d} {g}\n" for d,g in cases),
            )
        actual=[
            resolve_guard_break2_damage_step(
                d,defender_command_is_guard=bool(g)
            ).damage_after_multiplier
            for d,g in cases
        ]
        self.assertEqual(actual,list(map(int,output.splitlines())))


if __name__ == "__main__":
    unittest.main()
