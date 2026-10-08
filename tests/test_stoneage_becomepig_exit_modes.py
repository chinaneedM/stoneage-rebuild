import unittest
from tools.stoneage_becomepig_exit_modes_audit import vectors, fs_mask, native_source, FLAG_NAMES, FS_NAMES


class ExitModesTests(unittest.TestCase):
    def test_all_safe_actor_positions_and_guards(self):
        rows = vectors()
        self.assertEqual(len(rows), len(set(rows)))
        self.assertTrue(all(len(r) == 28 for r in rows))
        for kind in (1, 2, 3):
            for mode in (1, 2, 3):
                subset = [r for r in rows if r[11] == kind and r[25] == mode]
                self.assertEqual({(r[4], r[5]) for r in subset},
                                 {(-1, 0)} | {(s,p) for s in (0,1) for p in range(5 if kind == 1 else 10)})
                self.assertEqual({r[1:4] for r in subset}, {(1,1,1), (0,1,1), (1,0,1), (1,1,0)})
        self.assertTrue(all(not r[10] for r in rows))  # invalid riders not admitted

    def test_exhaustive_flag_domain_for_each_mode(self):
        rows = vectors()
        for mode in (1, 2, 3):
            for side, pos in ((0,0), (1,4)):
                self.assertEqual({r[27] for r in rows if r[11] == 1 and r[25] == mode
                                  and r[4:6] == (side,pos)}, set(range(512)))

    def test_duel_never_emitted_and_profile_flag_scope(self):
        c = {'CHAR_FS_'+name: 1 << j for j,name in enumerate(FS_NAMES)}
        for bits in range(512):
            self.assertEqual(fs_mask('gavin', bits, c), bits & ~1)
            self.assertEqual(fs_mask('iris', bits, c), bits & ~1)
            self.assertEqual(fs_mask('bismarck', bits, c), bits & 14)
        self.assertEqual(len(FLAG_NAMES), 9)

    def test_inherited_adapter_drift_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'adapter drift'):
            native_source('int main(void){return 0;}')


if __name__ == '__main__':
    unittest.main()
