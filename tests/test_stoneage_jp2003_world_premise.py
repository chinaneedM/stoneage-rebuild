"""Bound world-premise marketing, generic facilities and tone to their source."""
import json
import unittest
from tools.stoneage_jp2003_world_premise import REPORT, URL, build, paragraphs, validate_report


class WorldPremiseTests(unittest.TestCase):
    def reject(self, i, key, value, message):
        o = json.loads(REPORT.read_text()); o['records'][i]['source_described_claims'][key] = value
        with self.assertRaisesRegex(ValueError, message): validate_report(o)

    def test_marketing_lower_bound_not_exact_species_count_or_later_catalog(self):
        self.reject(1, 'exact_species_count_or_complete_roster', 100, 'Marketing lower bound')
        self.reject(1, 'equals_later_124_entry_catalog_proven', True, 'Marketing lower bound')

    def test_album_capability_not_automatic_capture_or_full_roster(self):
        self.reject(1, 'automatic_capture_screenshot_or_all_encounters_recorded_proven', True, 'Album capability')

    def test_school_and_stone_money_not_named_npc_quest_or_currency_id(self):
        for key, value in [('school_named_or_mapped_entity', {'village': 1}),
                           ('school_curriculum_pet_trainer_or_quest_role', 'PET_TRAINER'),
                           ('currency_item_id_prices_or_trade_algorithm', {'id': 1})]:
            self.reject(2, key, value, 'Generic facility/economy')

    def test_cooperative_tone_not_no_combat_or_imported_epic_history(self):
        self.reject(4, 'combat_absent_or_disabled_proven', True, 'Tone promoted')
        self.reject(4, 'epic_history_names_or_wayi_worldline_identity', 'EDEN', 'Tone promoted')

    def test_comment_and_script_copy_not_visible_second_witness(self):
        core='<div><font>石器時代のような世界 synthetic<br><br>second</font></div>'
        self.assertEqual(paragraphs('<!--'+core+'--><script>'+core+'</script>'+core),
                         ['石器時代のような世界 synthetic', 'second'])
        with self.assertRaises(ValueError): paragraphs(core+core)
        with self.assertRaises(ValueError): paragraphs('<!--'+core+'-->')

    def test_wrong_capture_wrong_host_and_error_page_rejected(self):
        for u in [URL, URL.replace('20031214053427', '19991101000000'),
                  URL.replace('hangame.co.jp', 'example.org')]:
            with self.assertRaises(ValueError): build(b'x'*12869, u)

    def test_archive_contract_capture_build_runtime_and_rights_boundary(self):
        o=json.loads(REPORT.read_text()); validate_report(o)
        self.assertEqual(o['coverage']['named_npc_pet_species_maps_or_quests_recovered'], 0)
        self.assertFalse(o['source']['capture_is_release_or_same_build_date'])
        from pathlib import Path
        c=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        for r in o['records']:
            self.assertLessEqual(set(c['record_contract']['required']), r.keys())
            self.assertEqual(r['collection'], 'sources')
            self.assertEqual(r['source_refs'][0]['actual_capture'], '20031214053427')
        o['records'][0]['client_build_or_cross_region_identity']='TW1.0'
        with self.assertRaisesRegex(ValueError, 'same-build'): validate_report(o)


if __name__ == '__main__': unittest.main()
