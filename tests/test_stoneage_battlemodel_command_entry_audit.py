"""Independent guard controls and array-vs-ID/data graph counterexamples."""
import unittest

from tools.stoneage_battlemodel_command_entry_source_audit import cases, expected, native_entry
from tools.stoneage_recovered25_battlemodel_command_entry_probe import magic_census, graph_census
from tests.test_stoneage_battlemodel_admission import fixture


class CommandEntryTests(unittest.TestCase):
    def test_illegal_pet_is_blocked_before_callback_and_owner_checks(self):
        for skill in (638, 641, 649, 650):
            for illegal in (10000, 20000):
                for owner in (-1, 0, 2):
                    self.assertEqual(expected((skill, illegal, 1, 1, 1, 2, owner),
                        checktype=True, open_enemy_skills=False), (0, 0, 0))
        self.assertEqual(expected((638, 10000, 2, 1, 1, 2, -1),
            checktype=True, open_enemy_skills=False), (1, 1, 0))
        self.assertEqual(len(cases()), 864)

    def test_counterfactual_OPEN_E_does_not_remove_pet_owner_guard(self):
        for owner in (-1, 0):
            self.assertEqual(expected((638, 10000, 1, 1, 1, 2, owner),
                checktype=True, open_enemy_skills=True), (0, 0, 0))
        self.assertEqual(expected((638, 10000, 1, 1, 1, 2, 2),
            checktype=True, open_enemy_skills=True), (1, 1, 0))

    def test_native_trace_detects_illegal_guard_bypass(self):
        # Deliberately broken independent control: always calls the callback.
        source = "int PETSKILL_Use(int c,int s,int t,char*d){return trace_callback(c,t,17,d);}"
        with self.assertRaisesRegex(ValueError, "guard/argument mismatch"):
            native_entry(source)

    def test_magic_callback_uses_array_position_not_skill_ID(self):
        runtime, _ = fixture()
        fields = lambda option: [b"", b"", b"independent_magic", option]
        parsed = [(fields(b"PETSKILL_BattleModel;0;SKILL"), {"ID": 1}),
                  (fields(b"PETSKILL_BattleModel;638;SKILL"), {"ID": 2}),
                  (fields(b"PETSKILL_BattleModel;1;SKILL"), {"ID": 3})]
        result = magic_census(parsed, runtime)
        self.assertEqual(result["layout_counts"]["ordered_rows"]["resolved_ID638_rows"], 1)
        self.assertEqual(result["layout_counts"]["ordered_rows"]["resolved_other_BattleModel_rows"], 1)
        self.assertIsNone(result["callback_option_candidates"][1]["layouts"]["ordered_rows"]["resolved_skill_id"])
        self.assertEqual(result["layout_counts"]["ID_indexed_OPTIMUM"]["resolved_ID638_rows"], 1)
        self.assertNotIn("SKILL", str(result))
        for token in (b"0trailing", b"not-a-number", b" +0"):
            result = magic_census([(fields(b"PETSKILL_BattleModel;" + token), {"ID": 4})], runtime)
            self.assertEqual(result["layout_counts"]["ordered_rows"]["resolved_ID638_rows"], 1)

        # OPTIMUM publishes last row ID+1, rather than allocation max+1.
        reversed_runtime = type(runtime)(skills=dict(reversed(tuple(runtime.skills.items()))), source_file=runtime.source_file)
        truncated = magic_census([(fields(b"PETSKILL_BattleModel;641"), {"ID": 5})], reversed_runtime)
        self.assertEqual(truncated["layout_counts"]["ID_indexed_OPTIMUM"]["resolved_other_BattleModel_rows"], 0)

    def test_zero_weight_graph_counts_are_not_skill_reachability(self):
        enemies = [dict(tempno=t, id=e, tactics=1, tactics_option="at:1;1;1|wa:0;0;0;0;0;0;0", petflg=0)
                   for t, e in ((1178, 2559), (1179, 2560))]
        groups = [dict(id=1, enemyids=[2559], enemyprobs=[1]),
                  dict(id=1, enemyids=[2560], enemyprobs=[1]),
                  dict(id=2, enemyids=[2560], enemyprobs=[0])]
        areas = [dict(groupids=[1], groupprobs=[1]), dict(groupids=[1], groupprobs=[0])]
        rows = graph_census(enemies, groups, areas)
        self.assertEqual((rows[0]["positive_group_ids"], rows[0]["positive_area_rows"]), ([1], 1))
        self.assertEqual((rows[1]["positive_group_ids"], rows[1]["positive_area_rows"]), ([], 0))
        enemies[0]["tactics_option"] = "at:1;1;1|wa:0;0;1;0;0;0;0"
        with self.assertRaisesRegex(ValueError, "configuration drift"):
            graph_census(enemies, groups, areas)


if __name__ == "__main__":
    unittest.main()
