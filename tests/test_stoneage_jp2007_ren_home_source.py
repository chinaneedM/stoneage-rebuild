import copy
import datetime
import json
import unittest
from tools.stoneage_jp2007_ren_home_source import REPORT, ROOT, STEM, validate


class RenHome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r)
        node = r
        for key in keys[:-1]:
            node = node[key]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            validate(r)

    def test_versioned_unique_records_and_source_roles(self):
        validate(self.r)
        self.reject(['records', 0, 'version_profile'], 'TW10')
        self.reject(['records', 0, 'game_ids'], [1])
        self.reject(['records', 0, 'source'], 'june')

    def test_january_unnamed_crush_not_backfilled_by_june(self):
        self.reject(['extracted', 'january', 'crush_named_in_january'], 'ワイト')
        self.reject(['extracted', 'narrative_links', 1, 'relation'], 'INDEPENDENT_WHITE_DAY_SOURCE')
        self.reject(['extracted', 'june', 'named_roles', 'レン'], 'VILLAGE_CHIEFS_DAUGHTER')

    def test_chocolate_approximate_whole_party_not_exact_or_single(self):
        self.reject(['extracted', 'january', 'effect', 'amount_approximate'], 601)
        self.reject(['extracted', 'january', 'effect', 'target'], 'ONE_PLAYER')
        self.reject(['extracted', 'january', 'ingredients_and_quantities'], {'cocoa': 1})

    def test_defeat_drops_not_capture_or_invented_prizes(self):
        self.reject(['extracted', 'june', 'flow', 0], 'CAPTURE_DINOSAURS')
        self.reject(['extracted', 'june', 'dinosaurs_materials_ranks_prizes_thresholds'], {'threshold': 100})
        self.reject(['extracted', 'june', 'counter_scope'], 'SERVER_WIDE')

    def test_calendar_discrepancy_retained_without_guessing_end(self):
        self.assertEqual(datetime.date(2007, 6, 12).weekday(), 1)
        self.assertEqual(datetime.date(2007, 6, 27).weekday(), 2)
        self.reject(['extracted', 'june', 'end_weekday_conflict', 'body_weekday'], '水')
        self.reject(['extracted', 'june', 'end_weekday_conflict', 'actual_intended_end_date'], '2007-06-26')
        self.reject(['extracted', 'june', 'time_of_day_or_timezone'], 'JST')

    def test_world_change_not_actual_marriage_or_permanent_house(self):
        self.reject(['extracted', 'june', 'final_house_or_marriage_observed'], True)
        self.reject(['extracted', 'june', 'house_persistence'], 'PERMANENT')
        self.reject(['unproven', 'actual_wedding_or_player_marriage_system_proven'], True)

    def test_player_charm_not_pet_loyalty_or_guaranteed_obedience(self):
        self.reject(['extracted', 'perfume', 'target'], 'PET_LOYALTY')
        self.reject(['extracted', 'perfume', 'changes_pet_loyalty_directly'], True)
        self.reject(['extracted', 'perfume', 'guarantees_obedience'], True)
        self.reject(['extracted', 'perfume', 'exact_recovery_prices_type_names_cap_formula'], {'price': 100})

    def test_real_source_mutations_and_outer_positive_receipts(self):
        r = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
        cases = r['audit']['real_body_mutations']
        self.assertEqual(len(cases), 17)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 17)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertEqual(r['audit']['outer_script_positives'], {'june': True, 'january': True})
        self.assertEqual(r['extracted'], self.r['extracted'])

    def test_current_source_authority_and_stage_boundaries(self):
        self.reject(['sources', 'june', 'current_bytes_are_authenticated_2007_original'], True)
        self.reject(['sources', 'january', 'authority'], 'ORIGINAL_OFFICIAL_HTML')
        for key in self.r['unproven']:
            with self.subTest(key=key):
                self.reject(['unproven', key], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'EXPAND_HOUSE_HELPERS')


if __name__ == '__main__':
    unittest.main()
