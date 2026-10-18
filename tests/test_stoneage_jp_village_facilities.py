"""Facility semantics/provenance negative cases use synthetic HTML and mocked HTTP."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError,URLError
from tools.stoneage_jp_village_facilities import IMAGES,NAMES,ORIGINAL,CAPTURE,REPORT,FIRST_IMAGE,archive,classify_page,inspect_page,validate_behavior_boundary,probe_first_image_gap


def specimen():
    rows=[]
    for i,name in enumerate(NAMES):
        dims='' if i==0 else ' width="200" height="150"'
        rows.append(f'<tr><td><img src="{IMAGES}town2-{i+1}.gif"{dims}></td><td></td><td>{name}<br>synthetic description {i}</td></tr>')
        if i<12:rows.append('<tr><td></td><td></td><td></td></tr>')
    return '村の施設の紹介<table>'+''.join(rows)+'</table><font onclick="location.href=\'town.asp\';">村の紹介</font>'


def records():return json.loads(REPORT.read_text())['records']


class VillageFacilityTests(unittest.TestCase):
    def test_thirteen_actual_rows_and_missing_first_declared_dimensions(self):
        e=classify_page(specimen())
        self.assertEqual([x['name_as_written'] for x in e],NAMES)
        self.assertIsNone(e[0]['declared_image_size'])
        self.assertEqual(e[-1]['dom_cells']['row'],24)
        self.assertEqual(e[1]['declared_image_size'],[200,150])
        self.assertEqual(len({x['source_description_sha256'] for x in e}),13)

    def test_swapped_name_picture_or_undocumented_dimensions_rejected(self):
        for wrong in (specimen().replace(NAMES[0],'TEMP').replace(NAMES[1],NAMES[0]).replace('TEMP',NAMES[1]),specimen().replace('town2-1.gif','TEMP').replace('town2-2.gif','town2-1.gif').replace('TEMP','town2-2.gif'),specimen().replace('town2-1.gif"','town2-1.gif" width="200" height="150"',1),specimen().replace('synthetic description 0','')):
            with self.assertRaises(ValueError):classify_page(wrong)

    def test_comment_script_and_wrong_navigation_do_not_invent_facilities(self):
        fake=f'<img src="{IMAGES}town2-1.gif">'
        self.assertEqual(len(classify_page('<!--'+fake+'--><script>'+fake+'</script>'+specimen())),13)
        with self.assertRaisesRegex(ValueError,'navigation'):classify_page(specimen().replace('town.asp','town3.asp'))

    def test_page_source_epoch_host_and_same_size_error_body_pinned(self):
        exact=archive(ORIGINAL,CAPTURE)
        for wrong in (exact.replace('hangame.co.jp','example.org'),exact.replace(CAPTURE,'20060618193306'),exact):
            with self.assertRaises(ValueError):inspect_page(b'x'*21792,wrong)

    def test_pet_shop_purchase_prohibition_is_not_silently_reversed(self):
        r=records();r[4]['source_described_behaviors']['player_can_buy_pets_from_shop']=True
        with self.assertRaisesRegex(ValueError,'Pet purchase prohibition'):validate_behavior_boundary(r)

    def test_bus_no_monsters_normal_speed_paid_not_teleport(self):
        for key,wrong in [('source_speed_category','FAST'),('monsters_appear_during_bus_trip',True),('money_required_to_board',False),('instant_teleport_or_faster_travel_proven',True)]:
            r=records();r[11]['source_described_behaviors'][key]=wrong
            with self.assertRaisesRegex(ValueError,'Bus speed/encounter/payment'):validate_behavior_boundary(r)

    def test_donation_quiz_fees_and_unknown_numerical_rules_preserved(self):
        for index,key,wrong in [(9,'item_contribution_required_to_set_village_home',False),(9,'donation_item_quantity_inventory_transaction_death_or_relogin_details',{'item':1}),(8,'entry_fee_required',False),(8,'threshold_fee_item_ids_event_sequence',{'level':20}),(10,'route_distance_metric_wage_formula_item_ids',{'pay_per_tile':1}),(12,'ticket_price_odds_pet_ids_and_draw_algorithm',{'odds':0.1})]:
            r=records();r[index]['source_described_behaviors'][key]=wrong
            with self.assertRaises(ValueError):validate_behavior_boundary(r)

    def test_healing_target_or_convenience_name_not_full_restore_or_24h(self):
        for index,key,wrong in [(1,'actor_full_heal_mp_pet_targets_amount_price','FULL_HP_MP_ALL_PETS'),(6,'opening_hours_or_24h_operation','24H')]:
            r=records();r[index]['source_described_behaviors'][key]=wrong
            with self.assertRaisesRegex(ValueError,'Unsupported healing'):validate_behavior_boundary(r)

    def test_image_404_is_temporary_observation_not_pixel_or_absence_evidence(self):
        p=json.loads(REPORT.read_text());self.assertFalse(p['image_source_gap']['historical_absence_proven'])
        self.assertFalse(p['image_source_gap']['prior_town_building_function_upgraded'])
        self.assertEqual([x['http_status'] for x in p['image_source_gap']['initial_attempts']],[404,404])
        for r in p['records']:
            for k in ('sha256','actual_capture','bytes','actual_size','frames'):self.assertIsNone(r['image'][k])
        r=records();r[0]['image']['actual_size']=[200,150]
        with self.assertRaisesRegex(ValueError,'Unacquired image'):validate_behavior_boundary(r)

    def test_independent_gap_probe_does_not_pass_network_error_or_new_success(self):
        url=archive(FIRST_IMAGE,CAPTURE)
        with patch('tools.stoneage_jp_village_facilities.urlopen',side_effect=HTTPError(url,404,'not found',None,None)):probe_first_image_gap()
        with patch('tools.stoneage_jp_village_facilities.urlopen',side_effect=HTTPError(url,503,'unavailable',None,None)):
            with self.assertRaisesRegex(ValueError,'did not reproduce'):probe_first_image_gap()
        with patch('tools.stoneage_jp_village_facilities.urlopen',side_effect=URLError('timeout')):
            with self.assertRaises(URLError):probe_first_image_gap()
        with patch('tools.stoneage_jp_village_facilities.urlopen'):
            with self.assertRaisesRegex(ValueError,'now responds'):probe_first_image_gap()

    def test_all_records_fit_archive_contract_without_runtime_ids_or_rights(self):
        p=json.loads(REPORT.read_text());contract=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        validate_behavior_boundary(p['records'])
        for r in p['records']:
            self.assertLessEqual(set(contract['record_contract']['required']),r.keys())
            self.assertIn(r['collection'],contract['required_collections'])
            self.assertEqual(r['source_refs'][0]['actual_capture'],CAPTURE)
            self.assertFalse(r['server_runtime_observed']);self.assertIsNone(r['client_map_npc_item_ids_coordinates'])
        self.assertEqual(p['coverage']['qualified_images'],0)
        self.assertEqual(p['coverage']['unattempted_image_urls'],12)


if __name__=='__main__':unittest.main()
