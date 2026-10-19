"""Reject materially wrong historical interpretations, without original HTML fixtures."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from tools.stoneage_jss2001_player_status import (
    ANCHORS, LABELS, PINS, REPORT, URL, build, status_rows, validate_contract,
)


def report():
    return json.loads(REPORT.read_text())


class PlayerStatusTests(unittest.TestCase):
    def reject(self, index, key, value, message):
        records = report()['records']
        records[index]['source_described_behavior'][key] = value
        with self.assertRaisesRegex(ValueError, message):
            validate_contract(records)

    def test_exp_prose_does_not_prove_last_hit_sharing_or_reward_formula(self):
        self.reject(0, 'exp_award_sharing_last_hit_formula_or_level_thresholds',
                    {'killer_share': 1}, 'EXP prose')
        self.reject(0, 'exp_eligibility_source_statement', 'ALL_GROUP_MEMBERS', 'EXP prose')

    def test_elements_are_influence_pairs_not_signed_multiplier_table(self):
        self.reject(0, 'element_advantage_direction_or_coefficients', {'earth_vs_water': 1.5}, 'Element influence')
        self.reject(0, 'element_attack_defense_influence_targets',
                    {'地属性': ['火', '風']}, 'Element influence')

    def test_primary_vitality_not_derived_durability_or_protocol_offset(self):
        self.reject(0, 'primary_equals_derived_stat_identity_proven', True, 'Primary and derived')
        self.reject(0, 'stat_conversion_formula_or_wire_offsets', {'体力': 7}, 'Primary and derived')

    def test_dp_has_two_described_triggers_but_no_known_amount(self):
        self.reject(0, 'dp_increases_described_on', ['DUEL_WIN_ONLY'], 'DP triggers')
        self.reject(0, 'dp_change_amount_or_complete_award_algorithm', 1, 'DP triggers')

    def test_revival_is_after_battle_for_character_and_pet(self):
        for key, value in [('applies_to', ['CHARACTER']), ('after_battle_revival_value_as_written', 100),
                           ('revival_timing', 'IMMEDIATE_DURING_BATTLE')]:
            self.reject(1, key, value, 'Knockout subject or timing')

    def test_damage_dependent_sp_return_not_mandatory_respawn(self):
        self.reject(1, 'return_to_savepoint_is_unconditional', True, 'Conditional SP')
        self.reject(1, 'return_to_savepoint', 'ALWAYS', 'Conditional SP')

    def test_character_charm_and_pet_loyalty_have_separate_consequences(self):
        self.reject(1, 'charm_and_loyalty_are_same_field', True, 'charm and pet loyalty')
        self.reject(1, 'player_knockout_consequence', 'LOYALTY_DECREASES', 'charm and pet loyalty')

    def test_omission_does_not_prove_no_other_knockout_losses(self):
        self.reject(1, 'exp_level_money_inventory_or_pet_loss_on_knockout', 'NO_OTHER_LOSSES', 'Knockout loss')
        self.reject(1, 'sp_return_threshold_charm_delta_loyalty_delta_or_operation_order',
                    {'charm_delta': -1}, 'Knockout loss')

    def test_bonus_choice_and_automatic_charm_dp_not_same_controls(self):
        self.reject(2, 'player_selectable_bonus_stats_as_written', ['魅力', 'DP'], 'level-up choices')
        self.reject(2, 'automatic_increases_as_written', ['体力'], 'level-up choices')

    def test_creation_points_and_pet_growth_not_levelup_bonus_values(self):
        self.reject(2, 'bonus_count_per_level_charm_delta_dp_delta_caps_or_respec', 20, 'generalized')
        self.reject(2, 'pet_growth_distribution_inferred_from_character_bonus_ui', True, 'generalized')
        self.reject(2, 'element_allocation_inferred_from_character_bonus_ui', True, 'generalized')

    def test_two_cell_row_binding_and_anchored_section_boundary(self):
        rows = ''.join('<tr><td>' + label + '</td><td>synthetic-' + str(i) + '</td></tr>'
                       for i, label in enumerate(LABELS))
        doc = '<A NAME="3040"></A><table>' + rows + '</table><A NAME="3041"></A><table>ignored</table>'
        self.assertEqual(status_rows(doc)[5], ('耐久力', 'synthetic-5'))
        for bad in [doc.replace('<td>DP</td>', '<td>DP</td><td>extra</td>'),
                    doc.replace('<td>耐久力</td>', '<td>体力</td>'),
                    doc.replace('<A NAME="3041"></A>', ''),
                    doc.replace('<td>気力</td>', '<td>魅力</td>')]:
            with self.assertRaises(ValueError):
                status_rows(bad)

    def test_authenticated_body_and_final_url_not_error_page_or_wrong_capture(self):
        for raw, url in [(b'x' * 28434, URL), (b'', URL),
                         (b'x' * 28434, URL.replace('20010418083149', '19991101000000')),
                         (b'x' * 28434, URL.replace('titan.co.jp', 'example.org'))]:
            with self.assertRaises(ValueError):
                build(raw, url)

    def test_per_record_required_fields_old_fingerprints_and_disjoint_semantics(self):
        o = report(); validate_contract(o['records'])
        contract = json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        old = json.loads(Path('research/recovered/JSS-LOGIN-MANUAL-CREATION-CONTRACT-R1.json').read_text())
        fingerprints = {x['anchor']: x['normalized_sha256'] for x in old['pages']['manual02']['relevant_section_fingerprints']}
        for a in ANCHORS:
            self.assertEqual(fingerprints[a], PINS[a][1])
        for name, key in [('STONEAGE-JSS2001-PET-MANUAL-CONTRACT-R1.json', 'section_sha256'),
                          ('STONEAGE-JSS2001-MAIL-ITEMS-SHARED-VENUES-R1.json', 'section_fingerprints')]:
            prior = json.loads(Path('research/recovered', name).read_text())
            self.assertFalse(set(ANCHORS) & set(prior[key]))
        self.assertFalse(o['source']['newly_discovered_source'])
        for record in o['records']:
            self.assertLessEqual(set(contract['record_contract']['required']), record.keys())
            self.assertEqual(record['collection'], 'tutorials')
            self.assertEqual(record['source_refs'][0]['actual_capture'], '20010418083149')
            self.assertIsNone(record['original_ids_wire_fields_and_same_build_binding'])
        for field, value in [('server_runtime_observed', True),
                             ('original_ids_wire_fields_and_same_build_binding', {'tw10': 1}),
                             ('rights_status', 'RELEASE_APPROVED')]:
            records = deepcopy(o['records']); records[0][field] = value
            with self.assertRaises(ValueError):
                validate_contract(records)


if __name__ == '__main__':
    unittest.main()
