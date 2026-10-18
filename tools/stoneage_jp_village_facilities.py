"""Operator-described village services and explicit negative rules, not server execution."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from tools.stoneage_jp_pet_catalog import Grid, acquire, archive, require

ORIGINAL = 'http://www.hangame.co.jp/publish/sa/town2.asp'
CAPTURE = '20031215095512'
SOURCE_SHA = 'f719ff0167c32e531f3128e47b31175df6bfc641a6a83728d2fd4370a9ae58b3'
IMAGES = 'http://images.hangame.co.jp/_images/game/saj/'
FIRST_IMAGE = IMAGES + 'town2-1.gif'
REPORT = Path('research/recovered/STONEAGE-JP-OFFICIAL-VILLAGE-FACILITIES-R1.json')
NAMES = ['村長の家','病院','武器屋','道具屋','ペットショップ','肉屋','コンビニ','チャットルーム','クイズ場','トーテンポール','マンモス便','マンモスバス停','宝くじ屋']
ROLES = ['CHIEF_HOUSE','HOSPITAL','WEAPON_SHOP','TOOL_SHOP','PET_SHOP','BUTCHER','CONVENIENCE_STORE','CHAT_ROOM','QUIZ_ARENA','HOME_TOTEM','MAMMOTH_DELIVERY','MAMMOTH_BUS_STOP','LOTTERY_SHOP']
BEHAVIORS = [
 {'source_describes_initial_arrival_location':True,'source_says_one_per_village':True,'new_character_relogin_death_phase_exact_mapping':None},
 {'hp_recovery_offered':True,'medicines_sold':True,'actor_full_heal_mp_pet_targets_amount_price':None},
 {'player_can_buy_weapons':True,'village_exclusive_stock_described':True,'specific_inventory_prices_ids':None},
 {'player_can_buy_tools':True,'village_exclusive_stock_described':True,'specific_inventory_prices_ids':None},
 {'player_can_sell_pets_to_shop':True,'player_can_buy_pets_from_shop':False,'pet_technique_teaching_described':True,'technique_ids_costs_eligibility':None},
 {'pet_meat_buying_and_selling_described':True,'meat_source_slaughter_or_drop_method':None},
 {'various_items_sold':True,'synthesis_materials_and_food_ingredients_emphasized':True,'opening_hours_or_24h_operation':None},
 {'chat_room_entry_described':True,'network_ui_channel_or_persistence_details':None},
 {'quiz_and_battle_events_described':True,'clear_all_for_item_reward_described':True,'level_restriction_required':True,'entry_fee_required':True,'threshold_fee_item_ids_event_sequence':None},
 {'item_contribution_required_to_set_village_home':True,'after_setting_game_start_at_selected_village_totem_described':True,'donation_item_quantity_inventory_transaction_death_or_relogin_details':None},
 {'item_delivery_part_time_job_described':True,'money_earnings_described':True,'source_says_farther_delivery_higher_wage':True,'route_distance_metric_wage_formula_item_ids':None},
 {'automatic_travel_to_other_towns_described':True,'source_speed_category':'NORMAL_WALKING','monsters_appear_during_bus_trip':False,'money_required_to_board':True,'instant_teleport_or_faster_travel_proven':False,'fare_routes_waypoints_and_server_encounter_implementation':None},
 {'lottery_ticket_purchase_described':True,'first_prize_kind':'SPECIAL_PET_UNIDENTIFIED','other_prizes_kind':'MONEY_UNQUANTIFIED','ticket_price_odds_pet_ids_and_draw_algorithm':None},
]


class FacilityGrid(Grid):
    def __init__(self):
        super().__init__();self.facility_images=[];self.return_links=[];self.return_label=None
    def handle_starttag(self,tag,attrs):
        super().handle_starttag(tag,attrs);d=dict(attrs)
        if self.hidden:return
        if tag=='img' and re.fullmatch(re.escape(IMAGES)+r'town2-(?:[1-9]|1[0-3])\.gif',d.get('src','')):
            require(self.tables and self.tables[-1]['open'],'Facility image outside cell')
            self.facility_images.append({**self.tables[-1],**d})
        if tag=='font' and d.get('onclick')=="location.href='town.asp';":self.return_label=[]
    def handle_data(self,value):
        super().handle_data(value)
        if self.return_label is not None and not self.hidden and value.strip():self.return_label.append(value.strip())
    def handle_endtag(self,tag):
        if tag=='font' and self.return_label is not None and not self.hidden:
            self.return_links.append(''.join(self.return_label));self.return_label=None
        super().handle_endtag(tag)


def classify_page(html):
    p=FacilityGrid();p.feed(html)
    require('村の施設の紹介' in p.visible,'Actual facility topic missing')
    require(len(p.facility_images)==13 and len({im['table'] for im in p.facility_images})==1,'Wrong actual facility image references')
    entries=[]
    for i,im in enumerate(p.facility_images):
        require(im['src']==IMAGES+f'town2-{i+1}.gif','Facility image order/identity differs')
        require((im['row'],im['col'])==(i*2,0),'Facility same-row association differs')
        declared=[im.get('width'),im.get('height')]
        require(declared==([None,None] if i==0 else ['200','150']),'Source declared dimensions differ')
        texts=p.cells.get((im['table'],im['row'],2),[])
        require(len(texts)>=2 and texts[0]==NAMES[i],'Facility name/description missing or reassigned')
        entries.append({'name_as_written':texts[0],'image_original_url':im['src'],'declared_image_size':None if i==0 else [200,150],
                        'source_description_sha256':sha256(('\n'.join(texts[1:])+'\n').encode()).hexdigest(),
                        'dom_cells':{'table':im['table'],'row':im['row'],'image_column':0,'name_description_column':2}})
    require(p.return_links==['村の紹介'],'Actual return navigation differs')
    return entries


def inspect_page(raw,final):
    require(final==archive(ORIGINAL,CAPTURE),'Facility page host/path/capture mismatch')
    require(len(raw)==21792 and sha256(raw).hexdigest()==SOURCE_SHA,'Facility page byte pin mismatch')
    return classify_page(raw.decode('cp932',errors='strict'))


def validate_behavior_boundary(records):
    require(len(records)==13 and [r['source_role'] for r in records]==ROLES,'Facility role count/order changed')
    b=[r['source_described_behaviors'] for r in records]
    require(b[4]['player_can_sell_pets_to_shop'] is True and b[4]['player_can_buy_pets_from_shop'] is False,'Pet purchase prohibition lost')
    require(b[11]['source_speed_category']=='NORMAL_WALKING' and b[11]['monsters_appear_during_bus_trip'] is False and b[11]['money_required_to_board'] is True and b[11]['instant_teleport_or_faster_travel_proven'] is False,'Bus speed/encounter/payment boundary lost')
    require(b[9]['item_contribution_required_to_set_village_home'] is True and b[9]['donation_item_quantity_inventory_transaction_death_or_relogin_details'] is None,'Home donation or unknown transaction boundary lost')
    require(b[8]['level_restriction_required'] is True and b[8]['entry_fee_required'] is True and b[8]['threshold_fee_item_ids_event_sequence'] is None,'Quiz eligibility/fee unknowns lost')
    require(b[1]['actor_full_heal_mp_pet_targets_amount_price'] is None and b[6]['opening_hours_or_24h_operation'] is None,'Unsupported healing target or opening hours')
    require(b[10]['route_distance_metric_wage_formula_item_ids'] is None and b[12]['ticket_price_odds_pet_ids_and_draw_algorithm'] is None,'Invented delivery or lottery formula')
    for r in records:
        require(r['client_map_npc_item_ids_coordinates'] is None and r['cross_region_aliases'] is None,'Invented entity IDs or aliases')
        require(r['server_runtime_observed'] is False and r['rights_status']!='RELEASE_APPROVED','Runtime or asset rights promoted')
        require(all(r['image'][k] is None for k in ('sha256','actual_capture','bytes','actual_size','frames')),'Unacquired image has actual pixel claims')


def build(raw,final):
    entries=inspect_page(raw,final);records=[]
    for i,e in enumerate(entries):
        records.append({'record_id':f'jp-hangame-facility:web-position:{i+1:02d}','collection':'maps',
            'entity_type':'OPERATOR_DESCRIBED_FACILITY_AND_SERVICE_NOT_CLIENT_MAP_PAYLOAD','record_revision':1,
            'version_profile':'JAPAN_HANGAME_WEB_20031215','source_refs':[{'source':ORIGINAL,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,'evidence_role':'SAME_ROW_FACILITY_NAME_DESCRIPTION_AND_IMAGE_REFERENCE'}],
            'verification_status':'OPERATOR_SERVICE_DESCRIPTION_NOT_RUNTIME_TRANSACTION','rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
            **e,'source_role':ROLES[i],'source_described_behaviors':dict(BEHAVIORS[i]),'client_map_npc_item_ids_coordinates':None,
            'cross_region_aliases':None,'all_services_exist_in_every_named_village_proven':False,'server_runtime_observed':False,
            'image':{'original_url':e['image_original_url'],'declared_size':e['declared_image_size'],'pixels_acquired':False,
                     'sha256':None,'actual_capture':None,'bytes':None,'actual_size':None,'frames':None,
                     'status':'HTTP_404_THIS_BOUNDED_ATTEMPT' if i==0 else 'NOT_ATTEMPTED'}})
    validate_behavior_boundary(records)
    return {'schema':'stoneage.jp.official_village_facilities.r1','date':'2026-10-19','task':'JP-OFFICIAL-VILLAGE-FACILITIES-SOURCE-01',
            'source':{'original_url':ORIGINAL,'strict_replay_url':final,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,'bytes':len(raw),'encoding':'CP932_STRICT'},
            'initial_discovery':{'requested_page_url':archive(ORIGINAL,'20031214052752'),'body_failures':[]},'records':records,
            'image_source_gap':{'original_url':FIRST_IMAGE,'requested_url':archive(FIRST_IMAGE,CAPTURE),
                'initial_attempts':[{'attempt':n,'http_status':404,'error_type':'HTTPError'} for n in (1,2)],
                'historical_absence_proven':False,'pixels_or_visual_review_acquired':False,'prior_town_building_function_upgraded':False,
                'reopen_if':'A specifically captured response for this same image URL yields qualified image bytes; do not infer from filename or similar building'},
            'coverage':{'facility_descriptions':13,'image_references':13,'image_urls_attempted':1,'qualified_images':0,'unattempted_image_urls':12,'original_server_services_executed':0},
            'boundaries':{'all_13_facilities_are_in_each_four_villages_proven':False,'original_runtime_atomicity_or_price_tables_recovered':False,
                'chief_initial_arrival_equals_every_login_or_death_spawn':False,'totem_configured_start_phase_exact_client_mapping_proven':False,
                'webpage_capture_is_release_or_174a_build_date':False,'cross_region_rule_equivalence_proven':False,'original_html_or_pixels_in_git':False,
                'stage_a_families':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
            'material_review':'research/recovered/STONEAGE-OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-R7.json',
            'next':'TW-WAYI-OFFICIAL-INTRO-DETAIL-04'}


def probe_first_image_gap():
    url=archive(FIRST_IMAGE,CAPTURE)
    try:
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 StoneAgeHistoricalEvidence'}),timeout=35) as r:
            r.read(1)
        raise ValueError('Previously unavailable image now responds; require new dated image intake before claiming pixels')
    except HTTPError as exc:
        require(exc.code==404,'Image gap probe did not reproduce observed HTTP404; do not infer absence')
        print('IMAGE_REFERENCE_PROBE_HTTP=404 HISTORICAL_ABSENCE_PROVEN=False',flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--local-input-dir');ap.add_argument('--output',required=True);args=ap.parse_args()
    if args.local_input_dir:raw=(Path(args.local_input_dir)/'jp-facilities.html').read_bytes();final=archive(ORIGINAL,CAPTURE)
    else:
        raw,final=acquire(archive(ORIGINAL,CAPTURE));probe_first_image_gap()
    result=build(raw,final);payload=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('FACILITY_DESCRIPTIONS=13');print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest());print('PAGE_SHA256='+SOURCE_SHA)


if __name__=='__main__':main()
