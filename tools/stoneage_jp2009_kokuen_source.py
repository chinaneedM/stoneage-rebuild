"""R72: source-qualified pet, random item draw and conversion/lifetime descriptions."""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-JP2009-KOKUEN'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
URL = 'https://www.4gamer.net/games/013/G001377/20090629031/'
IMAGE_URL = URL + 'SS/001.jpg'
PROFILE = 'LATER_OFFICIAL_JP_DIGIPARK_2009_KOKUEN_EXACT_BUILD_UNKNOWN'
TYPES = ['耐久のほら貝袋(黒炎)', '気力のほら貝袋(黒炎)', '黒炎変身薬',
         '黒炎変身鎧チケット', '黒炎再抽選チケット', '黒炎交換チケット']
BOUNDARIES = {k: False for k in ('current_bytes_authenticated_as_2009_capture',
    'original_official_site_bytes_obtained', 'same_build_tw10_membership_verified',
    'original_server_runtime_verified', 'original_ids_recovered', 'screenshot_is_species_base_stats',
    'bag_guarantees_pet', 'all_items_disappear_on_logout', 'kokuen_and_hakuen_share_original_id',
    'transformation_is_pet_species_change', 'original_html_or_assets_committed', 'stage_b_started')}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(text):
    return re.sub(r'\s+', '', text)


class Entry(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0; self.active = None; self.roots = 0; self.hidden = 0
        self.parts = []; self.images = []; self.issuer = []; self.capture_issuer = False
        self.visible = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('head', 'script', 'style', 'iframe', 'noscript'):
            self.hidden += 1
        if self.hidden:
            return
        if tag == 'div':
            self.depth += 1
            if 'entry-content' in a.get('class', '').split():
                require(self.active is None, 'Nested release body')
                self.active = self.depth; self.roots += 1
        if self.active is not None:
            if tag in ('br', 'li', 'p', 'tr'):
                self.parts.append('\n')
            if tag == 'td' and a.get('class') == 'release_maker':
                self.capture_issuer = True
            if tag == 'img' and 'OVERLAY_SS_open' in a.get('onclick', ''):
                before = compact(''.join(self.parts))
                marker = '■期間限定！便利商店に新しいペット「コクエン」追加！'
                in_selected = before.count(marker) == 2 and '一発逆転!?' not in before.rsplit(marker, 1)[1]
                self.images.append({'thumbnail': a.get('src'), 'onclick': a['onclick'], 'in_selected_section': in_selected})

    def handle_endtag(self, tag):
        if tag in ('head', 'script', 'style', 'iframe', 'noscript'):
            if self.hidden: self.hidden -= 1
            return
        if self.hidden: return
        if tag == 'td': self.capture_issuer = False
        if tag == 'div':
            if self.depth == self.active: self.active = None
            self.depth -= 1

    def handle_data(self, text):
        if not self.hidden:
            self.visible.append(text)
            if self.active is not None:
                self.parts.append(text)
                if self.capture_issuer: self.issuer.append(text)


def one(pattern, text):
    found = re.findall(pattern, text)
    require(len(found) == 1, 'Missing/duplicate scoped evidence: ' + pattern)
    return found[0]


def scopes(raw):
    text = raw.decode('utf-8', errors='strict')
    p = Entry(); p.feed(text)
    require(p.roots == 1 and p.active is None, 'Release absent/duplicate/unclosed')
    require(compact(''.join(p.issuer)) == 'デジパーク', 'Operator-release issuer changed')
    visible = compact(''.join(p.visible))
    require('2009/06/2916:55' in visible and '「ストーンエイジ」の公式サイトがリニューアル。新ペットも実装' in visible,
            'Visible publication/title changed')
    full = compact(''.join(p.parts))
    require(full.count('メーカー発表文の内容をそのまま掲載しています') == 1 and '2009/06/29' in full,
            'Credited manufacturer-release boundary absent')
    marker = '■期間限定！便利商店に新しいペット「コクエン」追加！'
    require(full.count(marker) == 2, 'Topic and detailed section boundaries changed')
    section = full.rsplit(marker, 1)[1].split('一発逆転!?', 1)
    require(len(section) == 2, 'Selected pet section end absent')
    return section[0], p.images


def derive(raw):
    body, images = scopes(raw)
    require('新ペット「コクエン」や「コクエン」に変身できるアイテム' in body and
            'ステータスは一定値を基準にランダムです。必ずしも、このような数値になるとは限りません。' in body,
            'Pet or randomized-stat caveat changed')
    dates = one(r'開始：(\d+)年(\d+)月(\d+)日（火）定期メンテナンス終了から終了：(\d+)年(\d+)月(\d+)日\(火\)定期メンテナンス開始まで', body)
    price = int(one(r'黒炎の袋(\d+)Gstone', body))
    draw_count = int(one(r'ランダムでアイテムが([１-９1-9])つ手に入ります', body).translate(str.maketrans('１２３４５６７８９','123456789')))
    type_count = int(one(r'黒炎の袋出現アイテム）全(\d+)種類', body))
    table = body.split('黒炎の袋出現アイテム）全'+str(type_count)+'種類', 1)[1]
    # The first two headings are suffixed; the other four headings recur in prose.
    headings = list(re.finditer(r'耐久のほら貝袋\(黒炎\)|気力のほら貝袋\(黒炎\)|(?<!「)黒炎変身薬使用|(?<!「)黒炎変身鎧チケットCP|(?<!「)黒炎再抽選チケットCP|(?<!「)黒炎交換チケットCP', table))
    require(len(headings) == 6 and type_count == 6, 'Exactly six listed item categories required')
    rows = [table[h.start():headings[i+1].start() if i+1<len(headings) else len(table)] for i,h in enumerate(headings)]
    require(all(row.startswith(name) for row,name in zip(rows,TYPES)), 'Row order or labels changed')
    totals = [int(one(r'合計(\d+)個で「黒炎変身鎧チケット」', row)) for row in rows[:3]]
    require(len(set(totals)) == 1, 'Mixed-item total disagrees between three rows')
    mix = one(r'例）「耐久のほら貝袋」(\d+)個＋「気力のほら貝袋」(\d+)個＋「黒炎変身薬」(\d+)個で', rows[0])
    mix = [int(x) for x in mix]; require(sum(mix) == totals[0], 'Worked mixture disagrees with required total')
    require(all('「耐久のほら貝袋」「気力のほら貝袋」「黒炎変身薬」' in row for row in rows[:3]),
            'Mixed eligible item labels changed')
    restoration = []
    for row, resource in zip(rows[:2], ('耐久力', '気力')):
        require('何度でも自分の'+resource+'が回復できるアイテムが出現' in row and
                row.count('※出現するアイテムは、ログアウト/ドロップで消滅') == 1,
                'Generated recovery-item lifetime/resource changed')
        restoration.append({'bag_name': TYPES[len(restoration)], 'resource_label': resource,
            'repeated_use_of_generated_item_as_reported': True, 'logout_disappearance_scope': 'GENERATED_ITEM',
            'drop_disappearance_scope': 'GENERATED_ITEM', 'recovery_amount': None,
            'generated_item_name': None, 'outer_bag_logout_behavior': None, 'disconnect_behavior': None})
    require('使用するとペット「コクエン」に変身できる薬' in rows[2], 'Transformation medicine effect changed')
    npcs = re.findall(r'CP交換所にいるNPC「([^」]+)」', ''.join(rows[3:]))
    require(len(npcs) == 3 and len(set(npcs)) == 1, 'Three ticket rows require same named exchange NPC')
    require('ペット「コクエン」に変身できる鎧と交換。' in rows[3] and
            'ペット「コクエン」のステータス再抽選ができるチケット。' in rows[4] and
            'ペット「コクエン」と交換できるチケット。' in rows[5], 'Distinct ticket functions changed')
    next_counts = [int(one(r'(\d+)枚で「'+dest+r'」', row)) for row,dest in zip(rows[3:5], TYPES[4:6])]
    require(len(images) == 1 and images[0]['in_selected_section'], 'One pet-status image inside selected section required')
    require(images[0]['thumbnail'] == '/games/013/G001377/20090629031/TN/001.jpg' and
            "'/games/013/G001377/20090629031/SS/001.jpg','270','363'" in images[0]['onclick'], 'Original full-size image binding changed')
    date = lambda v: '-'.join(f'{int(x):0{4 if i==0 else 2}d}' for i,x in enumerate(v))
    return {'pet_name': 'コクエン', 'pet_id': None, 'exact_game_build': None,
        'announced_sale': {'start_date': date(dates[:3]), 'start_event': 'REGULAR_MAINTENANCE_END',
            'end_date': date(dates[3:]), 'end_event': 'REGULAR_MAINTENANCE_START', 'timezone': None,
            'deployment_verified': False},
        'bag': {'name': '黒炎の袋', 'price': price, 'currency_as_written': 'Gstone',
            'random_item_count': draw_count, 'declared_item_types': type_count, 'listed_item_types': TYPES,
            'outcome_probabilities': None, 'pet_guaranteed_on_open': False, 'item_id': None},
        'recovery_bags': restoration,
        'conversion': {'eligible_base_item_names_as_written': ['耐久のほら貝袋', '気力のほら貝袋', '黒炎変身薬'],
            'base_names_to_suffixed_table_names_same_id': None,
            'mixed_total_for_armor_ticket': totals[0], 'example_mixture_counts': mix,
            'example_is_exclusive_required_recipe': False, 'armor_tickets_for_reroll_ticket': next_counts[0],
            'reroll_tickets_for_pet_ticket': next_counts[1], 'item_consumption_or_atomicity_verified': False,
            'guaranteed_bag_open_count_for_pet': None, 'expected_gstone_cost_for_pet': None},
        'exchange_npc': {'name': npcs[0], 'location_label': 'CP交換所', 'npc_id': None, 'coordinates': None},
        'ticket_effects': [
            {'name': TYPES[3], 'exchange_for': 'KOKUEN_TRANSFORMATION_ARMOR', 'armor_name': None},
            {'name': TYPES[4], 'exchange_for': 'KOKUEN_STATUS_REROLL', 'retained_fields': None, 'reroll_distribution': None},
            {'name': TYPES[5], 'exchange_for': 'KOKUEN_PET', 'pet_level': None, 'tickets_per_pet_exchange': None}],
        'transformation': {'medicine': TYPES[2], 'form_label': 'コクエン', 'subject_identity': None,
            'duration': None, 'battle_stat_effects': None, 'permanent_species_change_verified': False},
        'status_warning_random_around_unspecified_reference': True, 'species_base_values': None,
        'original_image_url': IMAGE_URL, 'original_server_runtime_verified': False}


def image_metadata(raw):
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        return {'url': IMAGE_URL, 'bytes': len(raw), 'sha256': sha(raw),
                'format': im.format, 'size': list(im.size), 'mode': im.mode}


def verify_visual(raw, visual):
    actual = image_metadata(raw)
    require(actual == visual['image_metadata'], 'Exact reviewed JPEG changed')
    return actual


def catalog(ex, visual):
    rows = [('pets','documentary_named_pet_and_single_status_sample',{'pet': ex['pet_name'], 'sample': visual['sample'],
             'species_base_values': None, 'sample_is_species_base_values': False}),
            ('npcs','documentary_exchange_npc',ex['exchange_npc']),
            ('items','documentary_random_bag',ex['bag'])]
    rows += [('items','documentary_recovery_bag_generated_item_lifetime',r) for r in ex['recovery_bags']]
    rows += [('items','documentary_transformation',ex['transformation'])]
    rows += [('items','documentary_ticket_function',r) for r in ex['ticket_effects']]
    return [{'record_id': f'JP2009-KOKUEN-R72-{i:02d}', 'collection': collection, 'entity_type': kind,
        'version_profile': PROFILE, 'source_refs': ['S1','S1-IMAGE'] if i==1 else ['S1'],
        'verification_status': 'SOURCE_DESCRIPTION_NOT_RUNTIME', 'rights_status': 'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
        'record_revision': 1, 'game_ids': None, 'content': content}
        for i,(collection,kind,content) in enumerate(rows,1)]


def pin(path):
    raw=(ROOT/path).read_bytes()
    return {'path':path,'bytes':len(raw),'sha256':sha(raw),
            'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def verify_report(r):
    require(r['version_profile']==PROFILE and r['negative_boundaries']==BOUNDARIES,'Evidence boundaries changed')
    ex=r['extraction'];v=r['visual_reference']
    require(r['original_html_or_assets_in_output'] is False and r['original_game_runtime_verified'] is False,
            'Original asset/runtime status promoted')
    require(v['id']=='S1-IMAGE' and v['parent_source']=='S1' and v['image_metadata']=={
        'url':IMAGE_URL,'bytes':68476,'sha256':'2949b7719977756fe0789b25f687122ba1b9c0381979bd8bf95e606f7bca59a0',
        'format':'JPEG','size':[270,363],'mode':'RGB'}, 'Manual transcription detached from exact reviewed JPEG')
    require(r['catalog_records']==catalog(ex,v),'Catalogue detached or rights/source promoted')
    for key in ('pet_id','exact_game_build','species_base_values'):
        require(ex[key] is None,'Pet identity/base promoted')
    require(ex['original_server_runtime_verified'] is False and ex['announced_sale']['deployment_verified'] is False,
            'Original execution promoted')
    require(ex['announced_sale']['timezone'] is None and ex['exchange_npc']['npc_id'] is None and
            ex['exchange_npc']['coordinates'] is None,'Date/NPC invented')
    require(ex['bag']['outcome_probabilities'] is None and ex['bag']['pet_guaranteed_on_open'] is False and
            ex['bag']['item_id'] is None,'Random bag promoted')
    for p in ex['recovery_bags']:
        require(all(p[k] is None for k in ('recovery_amount','generated_item_name','outer_bag_logout_behavior','disconnect_behavior')) and
                p['logout_disappearance_scope']==p['drop_disappearance_scope']=='GENERATED_ITEM','Recovery lifetime scope promoted')
    c=ex['conversion']
    require(c['base_names_to_suffixed_table_names_same_id'] is None and
            c['example_is_exclusive_required_recipe'] is False and c['item_consumption_or_atomicity_verified'] is False and
            c['guaranteed_bag_open_count_for_pet'] is c['expected_gstone_cost_for_pet'] is None,'Conversion guarantee invented')
    require(all(ex['transformation'][k] is None for k in ('subject_identity','duration','battle_stat_effects')) and
            ex['transformation']['permanent_species_change_verified'] is False,'Transformation expanded')
    require(ex['ticket_effects'][0]['armor_name'] is None and
            ex['ticket_effects'][1]['retained_fields'] is ex['ticket_effects'][1]['reroll_distribution'] is None and
            ex['ticket_effects'][2]['pet_level'] is ex['ticket_effects'][2]['tickets_per_pet_exchange'] is None,
            'Ticket/reroll unknowns replaced')
    require(v['review_method']=='MANUAL_TRANSCRIPTION_BOUND_TO_EXACT_JPEG_NOT_OCR' and
            v['sample_is_species_base_values'] is False and v['sample']['element_numeric_values'] is None and
            v['sample']['original_sprite_or_model_id'] is None and v['runtime_build_authenticated'] is False,
            'Visual reference promoted')
    require(v['sample']=={'name':'コクエン','level':1,'exp_display':0,'next_display':2,'hp_display':[72,72],
        'attack_display':18,'defense_display':19,'agility_display':15,'loyalty_display':0,
        'element_numeric_values':None,'original_sprite_or_model_id':None},'Manual sample transcription changed; re-review exact pixels')
    require([p['path'] for p in r['parent_pins']]==[
        'research/recovered/STONEAGE-JP2009-GUILD-HAKUEN-SOURCE-R1.json',
        'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json'] and
        all(pin(p['path'])==p for p in r['parent_pins']),'Parent source bytes changed')
    parent=json.loads((ROOT/r['parent_pins'][0]['path']).read_text())
    require(parent['hakuen']['name']==r['parent_comparison']['parent_pet_name'] and
            parent['hakuen']['bag_declared_distinct_item_types']==r['parent_comparison']['hakuen_declared_types'] and
            parent['hakuen']['bag_visible_named_rows']==r['parent_comparison']['hakuen_named_types'],
            'Comparison not bound to real parent')
    require(r['parent_comparison']['kokuen_is_hakuen_alias_verified'] is False and
            r['parent_comparison']['hakuen_declared_types']==7 and r['parent_comparison']['hakuen_named_types']==6 and
            r['parent_comparison']['parent_seventh_item_filled_from_kokuen'] is False,'White/black version evidence merged')
    require(r['source_pages'][0]['url']==URL and r['source_pages'][0]['historical_capture'] is None and
            r['source_pages'][0]['issue_attribution']=='デジパーク','Historical source authority promoted')


MUTATIONS=(('2009/06/29 16:55','2009/06/30 16:55'),('class="release_maker">デジパーク','class="release_maker">別の会社'),
    ('一定値を基準にランダム','全員に固定'),('2009年7月21日','2009年7月22日'),
    ('定期メンテナンス 開始　まで','定期メンテナンス 終了　まで'),('400 Gstone','401 Gstone'),
    ('ランダムでアイテムが１つ','ランダムでアイテムが２つ'),('全6種類','全7種類'),
    ('合計10個','合計11個'),('」3個＋','」4個＋'),('何度でも自分の耐久力','一度だけ自分の耐久力'),
    ('何度でも自分の気力','何度でも自分の耐久力'),('※出現するアイテムは、ログアウト/ドロップで消滅','※袋は、ログアウト/ドロップで消滅'),
    ('黒炎系交換員','別の交換員'),('5枚で「黒炎再抽選チケット」','6枚で「黒炎再抽選チケット」'),
    ('5枚で「黒炎交換チケット」','6枚で「黒炎交換チケット」'),('ステータス再抽選ができる','レベルを固定できる'),
    ('SS/001.jpg','SS/002.jpg'))


def audit(raw, expected):
    text=raw.decode('utf-8')
    for old,new in MUTATIONS:
        require(old in text,'Real-source mutation missing: '+old)
        try: actual=derive(text.replace(old,new).encode())
        except ValueError: continue
        require(actual!=expected,'Semantic mutation accepted: '+old)
    require(derive(raw+b'<script>peripheral=1</script>')==expected,'Peripheral script contaminated source')
    # Adjacent event text is outside this deliberately bounded source package.
    require('掛け金が２倍' in text, 'Adjacent-event positive input absent')
    require(derive(text.replace('掛け金が２倍','掛け金が９倍').encode())==expected,'Unselected event leaked into pet scope')
    return {'semantic_mutations_rejected_without_digest_gate':len(MUTATIONS),'peripheral_script_positive':True,
            'adjacent_unselected_event_positive':True}


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True)
    args=p.parse_args();r=json.loads(REPORT.read_text());verify_report(r)
    payloads=[]
    for url,name in [(URL,'source.html'),(IMAGE_URL,'pet-panel.jpg')]:
        if args.fetch:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'StoneAge-research/1.0'}),timeout=45) as rs:
                require(rs.status==200 and rs.url==url,'HTTP identity changed');raw=rs.read(2_000_001)
        else:raw=(Path(args.input_dir)/name).read_bytes()
        require(0<len(raw)<=2_000_000,'Source size outside bound');payloads.append(raw)
    ex=derive(payloads[0]);require(ex==r['extraction'],'Selected source semantics changed')
    visual=verify_visual(payloads[1],r['visual_reference'])
    core=scopes(payloads[0])[0]
    require(len(core)==r['selected_visible_compact_core']['characters'] and
            sha(core.encode())==r['selected_visible_compact_core']['sha256'],'Selected complete core changed')
    out={'schema':'stoneage.jp2009_kokuen.replay.r1','inputs':[{'id':'S1','url':URL,'bytes':len(payloads[0]),'sha256':sha(payloads[0])},
        {'id':'S1-IMAGE',**visual}], 'extraction':ex,'visual_reference':r['visual_reference'],
        'catalog_records':catalog(ex,r['visual_reference']),'audit':audit(payloads[0],ex),
        'original_html_or_assets_in_output':False,'original_game_runtime_verified':False}
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'inputs':out['inputs'],'catalog_records':len(out['catalog_records']),'audit':out['audit']}))


if __name__=='__main__':main()
