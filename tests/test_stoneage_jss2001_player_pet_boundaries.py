"""Test false cross-context inferences in a finite offline source comparison."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from tools.stoneage_jss2001_player_pet_boundaries import INPUTS, ROOT, REPORT, build, validate_report
from tools.stoneage_early_mail_venue_crosswalk import pointer


class PlayerPetBoundariesTests(unittest.TestCase):
    def report(self):
        return json.loads(REPORT.read_text())

    def reject(self, i, key, value, message):
        o = self.report(); o['records'][i]['source_facts'][key] = value
        with self.assertRaisesRegex(ValueError, message):
            validate_report(o)

    def test_initial_stat_and_element_allocation_cannot_fill_per_level_points(self):
        self.reject(0, 'per_level_points', 20, 'Creation stat points')
        self.reject(1, 'level_up_element_allocation_proven', True, 'Creation elements')

    def test_related_charm_and_loyalty_not_same_actor_or_data_field(self):
        self.reject(2, 'charm_change_is_loyalty_same_field', True, 'Charm and loyalty')
        self.reject(2, 'pet_knockout_effect', 'CHARM_DECREASES_SLIGHTLY', 'Charm and loyalty')

    def test_knockout_repeated_in_same_manual_not_known_numeric_delta(self):
        self.reject(3, 'loyalty_decrease_numeric_delta', -1, 'numeric proof')
        o = self.report(); o['records'][3]['same_original_body_counts_as_independent_confirmation'] = True
        with self.assertRaisesRegex(ValueError, 'independent source'):
            validate_report(o)

    def test_owner_level_charm_and_loyalty_not_additive_or_recursive_growth_formula(self):
        self.reject(4, 'total_or_recursive_loyalty_increment', {'level': 1, 'charm': 1, 'total': 2}, 'pet growth formula')
        self.reject(4, 'pet_gets_player_up_allocation_ui', True, 'pet growth formula')

    def test_arena_rank_seven_seven_not_dp_balance(self):
        self.reject(5, 'dp_to_rank_conversion', {'77_dp': 'free_ticket'}, 'rank positions')
        self.reject(5, 'arena_free_cases', [{'dp': 77}], 'rank positions')

    def test_initial_capture_loyalty_bound_not_lifetime_cap_or_combat_exp_limit(self):
        self.reject(6, 'universal_loyalty_cap_or_exp_reward_formula', {'loyalty_cap': 60}, 'universal cap')
        self.reject(6, 'capture_or_pickup_blocked_gap_at_least', 5, 'universal cap')
        self.reject(6, 'pickup_blocked_gap_at_least', 7, 'universal cap')

    def test_changed_input_bytes_even_semantically_equivalent_rejected(self):
        raw = {k: (ROOT / v[0]).read_bytes() for k, v in INPUTS.items()}
        for k in raw:
            bad = dict(raw); bad[k] += b'\n'
            with self.assertRaisesRegex(ValueError, 'byte pin'):
                build(bad)
        bad = dict(raw); bad.pop('creation')
        with self.assertRaisesRegex(ValueError, 'Exact four'):
            build(bad)

    def test_per_record_provenance_json_pointers_and_actual_original_body_count(self):
        o = self.report(); validate_report(o)
        raw = {k: (ROOT / v[0]).read_bytes() for k, v in INPUTS.items()}
        self.assertEqual(build(raw), o)
        required = json.loads((ROOT / 'STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        bodies = set()
        for r in o['records']:
            self.assertLessEqual(set(required), r.keys())
            for s in r['source_refs']:
                pointer(json.loads(Path(s['derived_report']).read_bytes()), s['json_pointer'])
                bodies.add((s['original_source'], s['actual_capture'], s['original_sha256']))
        self.assertEqual(len(bodies), 2)
        for key, value in [('new_original_requests', 2), ('original_bodies_referenced', 4)]:
            bad = deepcopy(o); bad['coverage'][key] = value
            with self.assertRaisesRegex(ValueError, 'report counts'):
                validate_report(bad)


if __name__ == '__main__':
    unittest.main()
