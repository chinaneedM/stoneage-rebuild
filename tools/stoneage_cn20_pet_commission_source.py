"""Finite two-page documentary extraction; never a spawn table or quest runtime."""
import argparse
import hashlib
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-CN20-PET-COMMISSION-HABITATS-SOURCE-R1.json'
CUSTODY = ROOT / 'research/recovered/STONEAGE-CN20-PET-COMMISSION-HABITATS-CUSTODY-R1.json'
URLS = ('https://games.sina.com.cn/newgames/0110/10236724.shtml',
        'https://games.sina.com.cn/newgames/0110/10236724_c1.shtml')
TITLE = '石器时代2之新鲜速递(三)--任务详解'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links, self.hidden = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'noscript'):
            self.hidden += 1
        if tag == 'a' and not self.hidden:
            self.links.append(dict(attrs).get('href'))

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'noscript') and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def visible(s):
    p = Visible()
    p.feed(s)
    return re.sub(r'\s+', '', ''.join(p.parts)), p.links


def between(text, first, last):
    require(text.count(first) == text.count(last) == 1, 'Ambiguous/missing section boundaries')
    require(text.index(first) < text.index(last), 'Reversed section boundaries')
    return text.split(first, 1)[1].split(last, 1)[0]


def article(raw):
    s = raw.decode('gb18030', errors='strict')
    title, _ = visible(between(s, '<!--begin title-->', '<!--end title-->'))
    require(title == TITLE, 'Wrong article title/version context')
    return visible(between(s, '<!--begin content-->', '<!--end content-->'))


def coordinates(text):
    return [[int(a), int(b)] for a, b in re.findall(r'（东(\d+),南(\d+)）', text)]


def parse_block(block, page_id):
    m = re.fullmatch(r'渔村宠物委托书([A-F])：(.+?)各(\d+)只成本：(\d+)S报酬：(\d+S|\?)宠物出没地点：(.+)', block)
    require(m is not None, 'Malformed pet commission block')
    letter, names, quantity, cost, reward, habitats = m.groups()
    pets = names.split('、')
    require(int(quantity) > 0, 'Target quantity must be positive')
    require(len(set(pets)) == len(pets) and all(pets), 'Duplicate/empty target species label')
    # Habitat order differs from target order in E; names may prefix other names.
    delimiter = '(' + '|'.join(re.escape(n) for n in sorted(pets, key=len, reverse=True)) + ')：'
    fields = re.split(delimiter, habitats)
    require(fields[0] == '' and len(fields) == 1 + 2 * len(pets), 'Habitat/target cardinality differs')
    by = {}
    for name, location in zip(fields[1::2], fields[2::2]):
        require(name not in by and location, 'Duplicate/empty habitat row')
        by[name] = {'species_label': name, 'location_text': location,
                    'coordinate_pairs_in_source_order': coordinates(location),
                    'coordinate_frame_verified': False, 'spawn_level': None,
                    'spawn_weight': None, 'map_id': None, 'species_id': None}
    require(set(by) == set(pets), 'Missing target habitat')
    return {'id': letter, 'source_page': page_id,
            'targets': [{'species_label': name, 'quantity_each': int(quantity)} for name in pets],
            'listed_cost_S': int(cost), 'listed_reward_S': None if reward == '?' else int(reward[:-1]),
            'reward_as_written': reward, 'deposit_refund': None, 'net_profit_S': None,
            'habitats_in_source_order': list(by.values()), 'actual_handover_or_payment_verified': False}


def blocks(text, page_id):
    starts = list(re.finditer(r'渔村宠物委托书[A-F]：', text))
    require(bool(starts), 'No pet commission blocks')
    return [parse_block(text[m.start(): starts[i + 1].start() if i + 1 < len(starts) else len(text)], page_id)
            for i, m in enumerate(starts)]


def extract(raw1, raw2):
    one, links1 = article(raw1)
    two, links2 = article(raw2)
    require(links1.count('10236724_c1.shtml') == 1, 'Real next-page link missing/ambiguous')
    # The return link is outside the continuation's article comment boundaries.
    return_links = visible(raw2.decode('gb18030', errors='strict'))[1]
    require(return_links.count('10236724.shtml') == 1, 'Continuation return link missing/ambiguous')
    require(one.count('任务分为"宠物"、"道具"、"料理"与"特别委托"') == 1,
            'Intro category scope changed')
    require('在石器时代2.0中' in one and '购买委托书（就是缴保证金啦！）' in one,
            'Version or general deposit context changed')
    first = between(one, '玛丽娜斯村任务委托店', '[下一页]')
    header, pet1 = first.split('渔村宠物委托书A：', 1)
    required = ('1.等级要求：无。', '2.特殊要求：无。', '任务委托书分为宠物和料理两种')
    require(all(x in header for x in required), 'Marinas-specific requirements/category scope changed')
    seller = re.search(r'前往北岛(.+?)的24小时便利商店（东(\d+),南(\d+)），向委托书贩售员（东(\d+),南(\d+)）购买任务委托书', header)
    require(seller is not None, 'Seller and nested location context missing')
    place, shop_x, shop_y, seller_x, seller_y = seller.groups()
    second = two.split('渔村料理委托书A：', 1)
    require(len(second) == 2, 'Pet/cooking section boundary missing')
    pet2 = second[0]
    require(pet2.startswith('渔村宠物委托书D：'), 'Continuation did not start at D')
    marinas_end = second[1].split('萨尔吉姆村任务委托店', 1)
    require(len(marinas_end) == 2, 'Next village boundary missing')
    handin = re.search(r'c\.将任务委托书上所需的物品或宠物准备好后，拿给委托管理员（东(\d+),南(\d+)）。4\.获得物品：任务委托书上所写的报酬', marinas_end[0])
    require(handin is not None, 'Marinas hand-in and reward contract missing')
    rows = blocks('渔村宠物委托书A：' + pet1, 'P1') + blocks(pet2, 'P2')
    require([r['id'] for r in rows] == list('ABCDEF'), 'Missing/duplicate/reordered commission')
    return {'title': TITLE, 'body_version_label': '石器时代2.0',
            'publication_date_verified': None, 'exact_build_verified': False,
            'intro_categories': ['宠物', '道具', '料理', '特别委托'],
            'marinas_categories': ['宠物', '料理'], 'category_scopes_equivalent': False,
            'marinas_requirements': {'level_label': '无', 'special_label': '无', 'universal_no_gate_proven': False},
            'purchase': {'place_text': place, 'outer_coordinate_pairs': coordinates(place),
                         'shop_label': '24小时便利商店', 'shop_xy_as_written': [int(shop_x), int(shop_y)],
                         'seller_role': '委托书贩售员', 'seller_xy_as_written': [int(seller_x), int(seller_y)],
                         'general_intro_payment_context': '保证金',
                         'coordinate_frames_and_npc_ids_verified': False},
            'handin': {'role': '委托管理员', 'xy_as_written': list(map(int, handin.groups())),
                       'actual_npc_id': None, 'consumed_pet_state_rules': None},
            'commissions': rows, 'species_label_count': len({t['species_label'] for r in rows for t in r['targets']}),
            'target_relation_count': sum(len(r['targets']) for r in rows),
            'next_page_link': '10236724_c1.shtml', 'further_page_retrieved': False,
            'original_server_executed': False, 'tw10_attribution_proven': False}


def verify(expected, raws):
    actual = extract(*raws)
    require(actual == expected, 'Source semantic contract changed; original uncertainty must not be promoted')
    return actual


def catalog(extracted, archive):
    """Export source relations into the existing archive vocabulary, without masters."""
    contract = archive['future_website']
    required = set(contract['record_contract']['required'])
    require({'quests', 'encounters'} <= set(contract['required_collections']), 'Archive collections changed')
    require({'source_refs', 'rights_status', 'verification_status', 'version_profile'} <= required,
            'Source/rights/version contract missing')
    records = []
    for row in extracted['commissions']:
        quest = 'cn20-sina-10236724:marinas-pet-' + row['id']
        common = {'version_profile': 'CN20_LABEL_PORTAL_UNDATED_BUILD_UNVERIFIED',
                  'source_refs': [row['source_page']], 'verification_status': 'SOURCE_DESCRIPTION_NOT_RUNTIME',
                  'rights_status': 'RESEARCH_METADATA_NOT_RELEASE_APPROVED', 'record_revision': 1, 'game_ids': None}
        records.append({**common, 'record_id': quest, 'collection': 'quests',
                        'entity_type': 'DOCUMENTARY_COMMISSION_NOT_SERVER_QUEST_MASTER',
                        'source_relation': {'commission_key': row['id'], 'target_labels': [t['species_label'] for t in row['targets']]}})
        for ordinal, habitat in enumerate(row['habitats_in_source_order'], 1):
            records.append({**common, 'record_id': quest + ':habitat-' + str(ordinal), 'collection': 'encounters',
                            'entity_type': 'DOCUMENTARY_LOCATION_RELATION_NOT_SPAWN_MASTER',
                            'source_relation': {'quest_record': quest, 'species_label': habitat['species_label'],
                                                'source_habitat_ordinal': ordinal},
                            'spawn_level': None, 'spawn_weight': None})
    require(all(required <= set(r) for r in records), 'Required archive field missing')
    return {'schema': 'stoneage.cn20_pet_commission.content_catalog.r1', 'records': records,
            'source_contract_path': str(REPORT.relative_to(ROOT)),
            'source_semantic_sha256': sha(json.dumps(extracted, ensure_ascii=False, sort_keys=True).encode()),
            'source_pages': {str('P' + str(i + 1)): url for i, url in enumerate(URLS)},
            'authenticated_game_master_count': 0, 'public_release_approved': False, 'website_built': False}


def verify_custody(receipt, root):
    require(receipt['source_scope']['original_runtime_executed'] is False, 'Custody is not game runtime evidence')
    require(len(receipt['permanent_derived_files']) >= 4, 'Incomplete permanent evidence custody')
    for pin in receipt['permanent_derived_files']:
        raw = (root / pin['path']).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()
        require(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'] and blob == pin['git_blob'],
                'Permanent derived evidence changed: ' + pin['path'])


def audit(expected, raws):
    # Real response mutations; verify uses parsed semantics, not raw/digest equality.
    changes = [(0, '各2只', '各1只', 'quantity'), (0, '成本：50S', '成本：55S', 'cost'),
               (0, '报酬：500S', '报酬：550S', 'reward'),
               (0, '东113,南661', '东114,南661', 'outer-coordinate'),
               (0, '东102,南96', '东103,南96', 'shop-coordinate'),
               (0, '东20,南12', '东21,南12', 'seller-coordinate'),
               (0, '等级要求：无', '等级要求：30级', 'scope-level'),
               (0, '在石器时代2.0中', '在石器时代1.0中', 'body-version'),
               (0, '就是缴保证金啦', '就是缴手续费啦', 'deposit-context'),
               (0, '10236724_c1.shtml', '10236724_c2.shtml', 'page-link'),
               (1, '报酬：?', '报酬：15000S', 'unknown-reward'),
               (1, '地下二楼', '地下一楼', 'habitat-floor'),
               (1, '东100,南97', '东101,南97', 'nested-village-coordinate'),
               (1, '委托管理员', '委托书贩售员', 'distinct-npc-role'),
               (1, '东18,南12', '东19,南12', 'handin-coordinate'),
               (1, '凯比：北岛科奥', '凯比：北岛异地', 'prefix-species-binding')]
    results = []
    for page, old, new, label in changes:
        a, b = old.encode('gb18030'), new.encode('gb18030')
        require(a in raws[page], 'Mutation anchor absent: ' + label)
        changed = list(raws)
        changed[page] = raws[page].replace(a, b, 1)
        try:
            verify(expected, changed)
        except (ValueError, UnicodeError):
            results.append({'case': label, 'changed_page_sha256': sha(changed[page]), 'rejected': True})
        else:
            raise ValueError('Semantic mutation accepted: ' + label)
    positive = [r + b'<script>peripheral layout only</script>' for r in raws]
    verify(expected, positive)
    return {'real_response_mutations': results, 'peripheral_script_positive': True, 'digest_gate_used': False}


def main():
    p = argparse.ArgumentParser()
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument('--fetch', action='store_true')
    source.add_argument('--html', nargs=2, type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--catalog-output', type=Path)
    args = p.parse_args()
    raws = []
    if args.fetch:
        for url in URLS:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as r:
                require(r.status == 200 and r.geturl() == url, 'HTTP status or resolved source changed')
                raw = r.read(1000001)
                require(len(raw) <= 1000000, 'Source oversized')
                raws.append(raw)
    else:
        raws = [path.read_bytes() for path in args.html]
    report = json.loads(REPORT.read_text())
    verify_custody(json.loads(CUSTODY.read_text()), ROOT)
    extracted = verify(report['extracted'], raws)
    result = {'schema': 'stoneage.cn20_pet_commission.derived_replay.r1',
              'http_inputs': [{'url': url, 'bytes': len(raw), 'sha256': sha(raw)} for url, raw in zip(URLS, raws)],
              'extracted': extracted, 'audit': audit(report['extracted'], raws),
              'original_html_assets_or_game_runtime_in_output': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    if args.catalog_output:
        archive_raw = (ROOT / report['catalog_archive_input']['path']).read_bytes()
        require(sha(archive_raw) == report['catalog_archive_input']['sha256'], 'Pinned archive contract changed')
        archive = json.loads(archive_raw)
        args.catalog_output.parent.mkdir(parents=True, exist_ok=True)
        args.catalog_output.write_text(json.dumps(catalog(extracted, archive), ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'ok': True, 'commissions': len(extracted['commissions']),
                      'species_labels': extracted['species_label_count'], 'semantic_negatives': len(result['audit']['real_response_mutations'])}))


if __name__ == '__main__':
    main()
