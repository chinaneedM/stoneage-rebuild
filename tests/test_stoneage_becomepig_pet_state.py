import unittest
from tools.stoneage_becomepig_pet_state_audit import follow_result, pet_return, native_source, vectors

class PetStateTests(unittest.TestCase):
    def test_mail_and_ownership_guard_death_normalization(self):
        for hp in (-2, 0, 1, 40, 150):
            for dead in (0, 1):
                self.assertEqual(pet_return(hp, dead, 1, 4), (hp, dead))
                self.assertEqual(pet_return(hp, dead, 0, -1), (hp, dead))
                expected = (1, 0) if dead or hp <= 0 else (min(hp, 100), 0)
                for slot in range(5):
                    self.assertEqual(pet_return(hp, dead, 0, slot), expected)

    def test_follow_owner_repair_does_not_infer_roster_selection(self):
        self.assertEqual(follow_result(-1, -1), (-1, -1, ()))
        self.assertEqual(follow_result(2, -1), (-1, -1, ((40, 0, -1),)))
        self.assertEqual(follow_result(1, -1), (1, 0, ((40, 0, 1), (41, 1, 0))))
        self.assertEqual(follow_result(1, 0), (1, 0, ()))
        self.assertEqual(follow_result(0, -1), (0, -1, ()))

    def test_matrix_separates_roster_slot_battle_occupancy_and_follow(self):
        rows = list(vectors())
        self.assertEqual(len(rows), 23040)
        self.assertEqual(len(set(rows)), len(rows))
        self.assertTrue(all(len(r) == 32 for r in rows))
        self.assertEqual({r[30] for r in rows}, {-1, 0, 1, 2, 3, 4})
        self.assertEqual({(r[30], r[31]) for r in rows},
                         {(s, b) for s in (-1, 0, 1, 2, 3, 4) for b in (0, 1)})
        self.assertTrue(all(r[17] == int(r[30] >= 0) for r in rows))

    def test_changed_native_adapter_rejected(self):
        with self.assertRaisesRegex(ValueError, 'adapter drift'):
            native_source('int main(void){return 0;}')

if __name__ == '__main__':
    unittest.main()
