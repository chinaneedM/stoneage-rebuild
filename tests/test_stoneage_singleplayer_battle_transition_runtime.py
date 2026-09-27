import unittest
from unittest.mock import patch, sentinel

from tools.stoneage_singleplayer_runtime import SinglePlayerHistoricalRuntime


class SinglePlayerBattleTransitionRuntimeTests(unittest.TestCase):

    def test_runtime_exposes_resolved_round_through_typed_contract(self):
        runtime = SinglePlayerHistoricalRuntime(domain=None, topology=None)

        commands = {"player": sentinel.command}
        initiative = {"player": 0}
        profiles = {"player": sentinel.profile}
        attack_rolls = {"player": sentinel.attack_rolls}
        capture_contexts = {"player": sentinel.capture_context}
        capture_rolls = {"player": sentinel.capture_rolls}
        escape_contexts = {"player": sentinel.escape_context}
        escape_rolls = {"player": sentinel.escape_rolls}
        captured_pets = {"enemy:1": sentinel.captured_pet}
        drop_rolls = {"enemy:1": (sentinel.drop_roll,)}

        with patch.object(
            runtime,
            "resolve_persistent_battle_round",
            return_value=sentinel.round_result,
        ) as resolve_round, patch(
            "tools.stoneage_singleplayer_runtime.build_battle_round_transition",
            return_value=sentinel.transition,
        ) as build_transition:
            got = runtime.resolve_persistent_battle_transition(
                sentinel.state,
                commands=commands,
                initiative_random_subtracts=initiative,
                profiles=profiles,
                attack_rolls=attack_rolls,
                defense_profile="preserved_old",
                capture_contexts=capture_contexts,
                capture_rolls=capture_rolls,
                escape_contexts=escape_contexts,
                escape_rolls=escape_rolls,
                no_risk=True,
                captured_pets_by_target_id=captured_pets,
                drop_rolls_by_enemy_id=drop_rolls,
                field_attr="fire",
                field_power=12,
                tie_break_order=("player",),
            )

        self.assertIs(got, sentinel.transition)
        resolve_round.assert_called_once_with(
            sentinel.state,
            commands=commands,
            initiative_random_subtracts=initiative,
            profiles=profiles,
            attack_rolls=attack_rolls,
            defense_profile="preserved_old",
            capture_contexts=capture_contexts,
            capture_rolls=capture_rolls,
            escape_contexts=escape_contexts,
            escape_rolls=escape_rolls,
            no_risk=True,
            captured_pets_by_target_id=captured_pets,
            drop_rolls_by_enemy_id=drop_rolls,
            field_attr="fire",
            field_power=12,
            tie_break_order=("player",),
        )
        build_transition.assert_called_once_with(sentinel.round_result)


if __name__ == "__main__":
    unittest.main()
