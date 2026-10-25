import copy
import json
import unittest
from tools import stoneage_npc_carrier_qualification as m


class CarrierQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.static = (m.ROOT / m.STATIC).read_text()
        cls.game = (m.ROOT / m.GAME).read_text()
        cls.modern = json.loads((m.ROOT / m.MODERN).read_bytes())

    def run_case(self, static=None, game=None, modern=None):
        return m.qualify(self.static if static is None else static,
                         self.game if game is None else game,
                         self.modern if modern is None else modern)

    def test_real_manifests_and_archived_result(self):
        self.assertEqual(m.build(), json.loads((m.ROOT / m.REPORT).read_bytes()))
        r = self.run_case()
        self.assertEqual(len(r['members']), 3)
        self.assertFalse(r['modern_arg_comparison']['sha256_equal'])
        self.assertFalse(r['preserved_script_bodies_read_this_turn'])

    def test_parent_size(self):
        with self.assertRaises(ValueError):
            self.run_case(static=self.static.replace('stoneage25-combined.rar|361255180', 'stoneage25-combined.rar|361255181'))

    def test_parent_hash(self):
        with self.assertRaises(ValueError):
            self.run_case(static=self.static.replace(m.BUNDLE, '0' * 64))

    def test_each_member_hash_in_each_independent_manifest(self):
        for path, (_, sha) in m.TARGETS.items():
            for which in ['static', 'game']:
                with self.subTest(path=path, which=which), self.assertRaises(ValueError):
                    self.run_case(**{which: getattr(self, which).replace(sha, '0' * 64)})

    def test_duplicate_member_rejected(self):
        line = next(x for x in self.game.splitlines() if x.startswith('CANDIDATE|server|character_npc_enemy|npc/100/sb_kbu.arg|'))
        with self.assertRaises(ValueError):
            self.run_case(game=self.game + '\n' + line)

    def test_static_member_size(self):
        with self.assertRaises(ValueError):
            self.run_case(static=self.static.replace(m.PREFIX + 'npc/100/sb_kbu.arg|258', m.PREFIX + 'npc/100/sb_kbu.arg|259'))

    def test_no_same_size_hash_substitution(self):
        changed = copy.deepcopy(self.modern)
        changed['embedded_sha256'] = m.TARGETS['npc/100/sb_kbu.arg'][1]
        with self.assertRaises(ValueError):
            self.run_case(modern=changed)

    def test_no_official_promotion(self):
        changed = copy.deepcopy(self.modern)
        changed['certified_same_official_build'] = True
        with self.assertRaises(ValueError):
            self.run_case(modern=changed)


if __name__ == '__main__':
    unittest.main()
