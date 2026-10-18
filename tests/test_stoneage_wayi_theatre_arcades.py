"""Venue, point-ledger, reward and promotional-context boundaries; no original HTML fixture."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from tools.stoneage_wayi_theatre_arcades import ANCHORS,FINAL,REPORT,build,sections,validate_contract
from tools.stoneage_wayi_intro_detail02_probe import Visible


def report():return json.loads(REPORT.read_text())


class TheatreArcadeTests(unittest.TestCase):
    def test_three_named_loops_keep_theatre_and_arcade_rewards_separate(self):
        o=report();validate_contract(o)
        self.assertEqual([r['name_as_written'] for r in o['records']],['伊甸劇場','魔法牌遊樂場','寵物轉轉輪遊樂場'])
        self.assertEqual(o['records'][0]['rewards_mentioned'],['SPECIAL_ITEMS_UNIDENTIFIED'])
        self.assertIn('PETS_UNIDENTIFIED',o['records'][1]['rewards_mentioned'])
        self.assertEqual(o['source']['actual_body_version_label'],'8.0')
        self.assertFalse(o['source']['site_title_is_exact_client_build'])

    def test_same_word_points_does_not_authenticate_shared_wallet(self):
        for i in (0,1,2):
            o=report();o['records'][i]['point_wallet_id_and_cross_venue_sharing']='SHARED_WALLET_1'
            with self.assertRaisesRegex(ValueError,'Shared point wallet'):validate_contract(o)

    def test_arcade_pet_prize_not_projected_onto_theatre(self):
        o=report();o['records'][0]['rewards_mentioned'].append('PETS_UNIDENTIFIED')
        with self.assertRaisesRegex(ValueError,'Theatre points/reward'):validate_contract(o)
        o=report();o['records'][0]['points_label_as_written']='積分'
        with self.assertRaises(ValueError):validate_contract(o)

    def test_unnamed_boss_and_fairytale_examples_not_named_canonical_scripts(self):
        for key in ('unnamed_boss_is_earlier_named_worldline_antagonist','theatre_fairytales_are_original_world_history_or_recovered_scripts'):
            o=report();o['boundaries'][key]=True
            with self.assertRaises(ValueError):validate_contract(o)

    def test_steps_cannot_turn_challenge_or_ticket_bet_into_guaranteed_reward(self):
        for i,loop in [(1,['REGISTER_CHALLENGE','GUARANTEED_PET']),(2,['FREE_ENTRY','GUARANTEED_PROFIT'])]:
            o=report();o['records'][i]['source_described_loop']=loop
            with self.assertRaises(ValueError):validate_contract(o)

    def test_prices_odds_ids_runtime_and_release_rights_stay_unknown(self):
        for key,value in [('prices_odds_point_rates_eligibility_and_actual_transaction',{'win_odds':0.1}),('map_npc_pet_item_skill_ids',{'pet':1}),('server_runtime_observed',True),('rights_status','RELEASE_APPROVED')]:
            o=report();o['records'][2][key]=value
            with self.assertRaises(ValueError):validate_contract(o)

    def test_section_scope_excludes_account_poll_scripts_and_footer(self):
        pieces=['unrelated poll',ANCHORS[0],'first synthetic body',ANCHORS[1],'second synthetic body',ANCHORS[2],'third synthetic body',ANCHORS[3],'footer']
        pins=[]
        for a,b in [(1,3),(3,5),(5,7)]:
            s=''.join(''.join(pieces[a:b]).split());pins.append((len(s),sha256(s.encode()).hexdigest()))
        with patch('tools.stoneage_wayi_theatre_arcades.PINS',pins):
            self.assertEqual(len(sections(pieces)),3)
            self.assertEqual(sections(['extra poll']+pieces+['extra footer']),sections(pieces))
            with self.assertRaisesRegex(ValueError,'duplicate'):sections(pieces+[ANCHORS[0]])
            with self.assertRaises(ValueError):sections(pieces[::-1])
            with self.assertRaisesRegex(ValueError,'content differs'):sections([s.replace('first synthetic','modified') for s in pieces])
        v=Visible();v.feed('<script>'+ANCHORS[0]+'</script><style>'+ANCHORS[1]+'</style>visible')
        self.assertEqual(v.pieces,['visible'])

    def test_wrong_archive_host_capture_and_same_size_error_body_rejected(self):
        for url in (FINAL.replace('wayi.com.tw','example.org'),FINAL.replace('20050614011214','20060105000000'),FINAL):
            with self.assertRaises(ValueError):build(b'x'*21308,url)

    def test_each_venue_fits_archive_contract_and_has_own_source_section(self):
        o=report();c=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        digests=[]
        for r in o['records']:
            self.assertLessEqual(set(c['record_contract']['required']),r.keys());self.assertIn(r['collection'],c['required_collections'])
            self.assertEqual(r['source_refs'][0]['actual_capture'],'20050614011214');digests.append(r['source_refs'][0]['section_fingerprint']['sha256'])
            self.assertIsNone(r['point_wallet_id_and_cross_venue_sharing']);self.assertFalse(r['server_runtime_observed'])
        self.assertEqual(len(set(digests)),3)
        self.assertEqual(o['coverage']['new_images_or_programs_acquired'],0)


if __name__=='__main__':unittest.main()
