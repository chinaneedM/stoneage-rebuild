"""Logging content/version distinctions with explicit negative evidence guards."""
import hashlib
import json
from pathlib import Path
import unittest
from tools.stoneage_logging_probe import SOURCES, CAPTURES, report

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-LOGGING-SOURCE-CONTRACT-R1.json'


class LoggingContractTests(unittest.TestCase):
    def data(self):
        return json.loads(REPORT.read_text())

    def test_three_actual_captures_are_not_requested_dates(self):
        d = self.data()['observations']
        self.assertEqual(d['temporal_witnesses'], CAPTURES)
        self.assertEqual(CAPTURES['archived_later'], '20031205132111')
        self.assertEqual(CAPTURES['archived_index'], '20040218115426')
        self.assertEqual(CAPTURES['archived_compilation'], '20040822040357')
        self.assertFalse(self.data()['compilation_authenticated_in_2001'])

    def test_current_task_blocks_match_actual_archives(self):
        h = self.data()['observations']['selected_block_sha256']
        self.assertEqual(h['compilation'], h['archived_compilation'])
        self.assertEqual(h['later_logging'], h['archived_later'])

    def test_last_hit_and_buyback_are_different_operations(self):
        p = self.data()['observations']['profiles']
        self.assertTrue(p['compilation']['player_last_hit_gets_wood'])
        self.assertFalse(p['compilation']['pet_last_hit_gets_wood'])
        self.assertTrue(p['compilation']['permit_returned_to_merchant_on_buyback'])
        self.assertFalse(p['later_logging']['player_or_pet_last_hit_rule_explicit_here'])
        self.assertFalse(self.data()['observations']['distinctions']['per_kill_permit_consumption_proven'])

    def test_approximate_payout_does_not_create_exact_unit_price_or_capacity(self):
        p = self.data()['observations']['profiles']['compilation']
        self.assertEqual(p['payout_example']['wood_count'], 14)
        self.assertEqual(p['payout_example']['approximate_stone'], 5000)
        self.assertIsNone(p['payout_example']['exact_unit_price'])
        self.assertFalse(p['guide_bag_example']['original_inventory_capacity_proven'])

    def test_bracelet_charm_conflict_stays_separate_from_reputation(self):
        d = self.data()['observations']
        p = d['profiles']
        self.assertEqual(p['later_logging']['bracelet_stats']['charm'], -5)
        self.assertEqual(p['levelguide']['bracelet_stats']['charm'], 5)
        self.assertIsNone(p['compilation']['bracelet_charm_delta'])
        self.assertEqual(p['later_logging']['reported_reputation_header'], 2)
        self.assertFalse(p['later_logging']['reputation_is_bracelet_charm'])
        self.assertEqual(d['conflicts'][0]['resolution'], 'KEEP_SOURCE_PROFILES_NO_DEFAULT')

    def test_axe_stat_difference_is_different_errand_stages(self):
        p = self.data()['observations']['profiles']
        self.assertEqual(p['compilation']['repaired_broken_axe_stats']['attack'], 33)
        self.assertEqual(p['later_logging']['new_errand_axe_stats']['attack'], 35)
        self.assertTrue(self.data()['observations']['distinctions']['new_errand_axe_and_repaired_broken_axe_stats_are_different_stages'])

    def test_later_repeat_route_not_silently_backdated(self):
        p = self.data()['observations']['profiles']
        self.assertIsNone(p['compilation']['repeatability'])
        self.assertTrue(p['later_logging']['repeat_reported'])
        self.assertIn('GOSSIP_YOUTH', p['later_logging']['repeat_trigger'])
        self.assertFalse(p['later_logging']['suggestion_is_admission_gate'])

    def test_editorial_version_bucket_is_not_original_build_authentication(self):
        d = self.data()['observations']
        self.assertEqual(d['index_attribution']['editorial_bucket'], 'STONEAGE_1_82')
        self.assertFalse(d['index_attribution']['original_1_82_server_build_authenticated'])
        self.assertEqual(d['index_attribution']['taiwan_1_0_or_jss_1999_attribution'], 'OPEN')
        self.assertFalse(d['lineage']['independent_origins_authenticated'])
        self.assertFalse(d['lineage']['archive_is_independent_rule_author'])

    def test_missing_sources_and_redirected_archive_require_requalification(self):
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            report({})
        for key in CAPTURES:
            a = {k: (b'invented', url) for k, (url, _) in SOURCES.items()}
            a[key] = (b'invented', a[key][1].replace(CAPTURES[key], '20090101000000'))
            with self.assertRaisesRegex(ValueError, 'redirect'):
                report(a)

    def test_all_unknown_ids_and_execution_boundaries_remain_open(self):
        d = self.data()
        self.assertTrue(all(v is None for v in d['observations']['unknown'].values()))
        for key in ('original_server_executed', 'original_quest_script_recovered', 'stage_a_accepted'):
            self.assertFalse(d[key])
        self.assertEqual(d['stage_b_gate'], 'GATED')
        self.assertEqual(d['early_exact_build_membership'], 'OPEN')
        for source in d['sources'].values():
            self.assertRegex(source['sha256'], r'^[a-f0-9]{64}$')
            self.assertEqual(set(source), {'url', 'final_url', 'bytes', 'sha256', 'decoding', 'replacement_characters'})

    def test_permanent_independent_acquisition_preserves_exact_raw_json(self):
        receipt = json.loads((ROOT / 'research/recovered/STONEAGE-LOGGING-ACCEPTANCE-R1.json').read_text())
        raw = (ROOT / receipt['permanent_path']).read_bytes()
        self.assertEqual(len(raw), receipt['raw_json_bytes'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), receipt['raw_json_sha256'])
        self.assertEqual(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(), receipt['permanent_git_blob'])
        self.assertEqual(json.loads(raw), self.data())
        self.assertEqual(receipt['independent_actual_source_reads'], 6)

    def test_quest_pet_last_hit_restriction_does_not_rewrite_ordinary_loot(self):
        from tools.stoneage_battle_core_model import BattleDropItem, DropRecipientTicket, DropAllocationRoll, allocate_battle_drop_items
        binding = json.loads((ROOT / 'research/recovered/STONEAGE-LOGGING-MODEL-BINDING-R1.json').read_text())
        for pin in binding['source_pins']:
            body = (ROOT / pin['path']).read_bytes()
            self.assertEqual(len(body), pin['bytes'])
            self.assertEqual(hashlib.sha256(body).hexdigest(), pin['sha256'])
        self.assertFalse(self.data()['observations']['profiles']['compilation']['pet_last_hit_gets_wood'])
        item = BattleDropItem('synthetic:ordinary', 1)
        result = allocate_battle_drop_items((item,), (DropRecipientTicket('pet:ally', 'player:owner'),), (DropAllocationRoll(0),))
        self.assertEqual(result.pending_by_player_entry_id['player:owner'], (item,))
        self.assertFalse(binding['generic_drop_path_proven_to_implement_logging'])
        self.assertFalse(binding['runtime_code_changed'])


if __name__ == '__main__':
    unittest.main()
