import unittest
from unittest.mock import patch
from pathlib import Path

from tools.stoneage_becomepig_hp_death_audit import (
    loyalty_penalty, native_source, vectors, verify_identity,
)


class PlayerHpDeathTests(unittest.TestCase):
    def test_hp_one_and_death_flag_are_independent(self):
        for profile in ('gavin', 'iris', 'bismarck'):
            self.assertEqual(loyalty_penalty(profile, 1, 0), 0 if profile == 'bismarck' else 10)
            for hp in (0, 1, 2, 100):
                self.assertEqual(loyalty_penalty(profile, hp, 1), 10)
            for hp in (0, 2, 100):
                self.assertEqual(loyalty_penalty(profile, hp, 0), 0)

    def test_cross_product_keeps_owned_selection_and_battle_slots_explicit(self):
        rows = list(vectors())
        self.assertEqual(len(rows), 6144)
        self.assertEqual(len(set(rows)), len(rows))
        self.assertEqual({r[-1] for r in rows}, {0, 1, 2, 150})
        self.assertEqual({r[12] for r in rows}, {0, 1})
        self.assertEqual({r[17] for r in rows}, {0, 1})
        self.assertEqual({(r[4], r[5]) for r in rows}, {(0, 0), (0, 4), (1, 0), (1, 4)})
        self.assertTrue(all(r[10] == 0 and r[11] == 1 for r in rows))

    def test_harness_adapter_rejects_changed_initialization(self):
        with self.assertRaisesRegex(ValueError, 'adapter drift'):
            native_source('int main(void){return 0;}')

    def test_identity_mutation_is_rejected(self):
        with patch.object(Path, 'read_text', return_value='{"profiles":{"gavin":{"pin":"exact"}}}'):
            verify_identity({'pin': 'exact'}, Path('pin.json'), 'gavin')
            with self.assertRaisesRegex(ValueError, 'identity drift'):
                verify_identity({'pin': 'mutated'}, Path('pin.json'), 'gavin')


if __name__ == '__main__':
    unittest.main()
