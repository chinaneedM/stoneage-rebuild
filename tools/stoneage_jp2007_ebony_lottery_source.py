"""R78: source-scoped named pet acquisition; lottery rates are not wild encounters."""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

from PIL import Image
from tools.stoneage_jp2005_treasure_source import VisibleMarkup, one, plain, require, sha

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-JP2007-EBONY-LOTTERY'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
URL = 'https://www.4gamer.net/news/history/2007.07/20070730194730detail.html'
PROFILE = 'JP_PC_2007_UTD_RELEASE_REPUBLISHED_BY_4GAMER_EXACT_BUILD_UNKNOWN'
PARENTS = ['research/recovered/STONEAGE-JP2008-FUKUURI-CAPTURE-SOURCE-R1.json',
           'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
PARSER = 'tools/stoneage_jp2005_treasure_source.py'
BOUNDARIES = {k: False for k in (
    'direct_official_page_acquired', 'current_bytes_authenticated_as_2007_original',
    'original_server_runtime_verified', 'tw10_membership_verified',
    'lottery_rate_is_wild_encounter_or_capture_rate', 'absolute_probabilities_recovered',
    'four_other_pets_named', 'image_left_right_species_identity_verified',
    'images_are_client_sprites_or_animation', 'gstone_is_stone_or_gash',
    'promised_change_proves_deployment', 'original_html_or_assets_committed', 'stage_b_started')}


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.images = []; self.anchors = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'img': self.images.append(a.get('src'))
        if tag == 'a': self.anchors.append(a.get('href'))


def article(raw):
    p = VisibleMarkup(); p.feed(raw.decode('cp932', errors='strict')); text = ''.join(p.parts)
    require(re.search(r'charset=shift_jis', text, re.I), 'Declared encoding changed')
    heading = one(r'<!--↓大見出し-->(.*?)<!--↑大見出し-->', text, re.S)
    require(plain(one(r'<h5>(.*?)</h5>', heading, re.S)) == '【リリース】「ストーンエイジ」，レアペットの出現確率が2倍に', 'Title changed')
    require(plain(one(r'<div class="news_txt1">(.*?)</div>', text, re.S)) == '2007/07/3019:47', 'Publication changed')
    require(plain(one(r'<td class="release_maker">(.*?)</td>', text, re.S)) == 'UTDエンターテインメント', 'Issuer changed')
    require(plain(one(r'<td class="release_date">(.*?)</td>', text, re.S)) == '2007/07/30', 'Release date changed')
    require(plain(one(r'<p class="release_caution txt3">(.*?)</p>', text, re.S)) == '＜以下，メーカー発表文の内容をそのまま掲載しています＞', 'Quotation authority changed')
    body = one(r'<div class="release_box">(.*?)</div>', text, re.S)
    p = Links(); p.feed(body)
    links = [urljoin(URL, u) for u in p.images]
    require(links == [f'https://www.4gamer.net/news/image/2007.07/20070730194730_{n}.jpg' for n in (0, 3)], 'Attached image references changed')
    require(p.anchors == ['http://stoneage.to/'] * 2, 'Official exit links changed')
    return plain(body), links


def derive(raw):
    body, images = article(raw)
    require('7月27日より販売を開始している「黒檀のくじ」' in body, 'Prior sale statement changed')
    require('この「黒檀のくじ」でのレアペット出現確率を2倍に引き上げます' in body, 'Lottery context/announcement changed')
    sy, sm, sd, sh, smin, em, ed, eh, emin = 2007, *map(int, one(r'▼確率変更日時(\d+)月(\d+)日（月）(\d+):(\d+)より(\d+)月(\d+)日（火）(\d+):(\d+)まで', body))
    require('（「黒檀のくじ」販売終了）▼販売価格' in body, 'End is no longer sale end')
    price = int(one(r'▼販売価格(\d+)GStone', body))
    shop = one(r'※GStoneはストーンエイジのショッピングサイト「([^」]+)」でご利用いただける仮想通貨です', body)
    rates = one(r'▼確率の変更内容(.*?)※ほか', body)
    pairs = re.findall(r'([^→倍]+)→出現確率(\d+)倍', rates)
    require(len(pairs) == 2 and ''.join(n+'→出現確率'+v+'倍' for n,v in pairs) == rates, 'Exactly two named relative rates required')
    others = int(one(r'※ほか(\d+)種類はこれに伴い、出現確率が若干低くなります', body))
    detail_hour = int(one(r'詳細な情報と出現確率は本日(\d+)時以降にストーンエイジ公式サイトにてご確認ください', body))
    require('▼『マンモストア』へはストーンエイジ公式サイトよりお入りください' in body, 'Shop entry statement changed')
    return {'lottery_name': '黒檀のくじ', 'acquisition_context': 'PAID_SHOP_LOTTERY_NOT_WILD_ENCOUNTER',
            'issuer_as_written': 'UTDエンターテインメント', 'publication_as_written': '2007/07/30 19:47',
            'sale_start_month_day_as_reported': [7, 27],
            'rate_window_using_publication_year': [[sy, sm, sd, sh, smin], [sy, em, ed, eh, emin]],
            'year_in_window_body_explicit': False, 'timezone_explicit': None,
            'window_end_also_sale_end_as_reported': True,
            'price_as_reported': {'amount': price, 'currency': 'GStone', 'shop': shop, 'purchase_unit_or_bundle_count': None},
            'named_pet_relative_rates': [{'name': n, 'relative_multiplier_as_reported': int(v), 'base_probability': None, 'changed_probability': None, 'original_species_id': None} for n,v in pairs],
            'other_pet_types_count': others, 'other_rate_direction': 'SLIGHT_DECREASE_AS_REPORTED', 'other_pet_names': None,
            'official_probability_details_promised_after_hour': detail_hour,
            'absolute_rates_or_normalization_formula': None, 'guarantee_or_pity': None,
            'pet_stats_growth_skills_habitat': None, 'exact_build': None,
            'image_references': images,
            'core_fingerprint': {'characters': len(body), 'utf8_bytes': len(body.encode()), 'sha256': sha(body.encode())}}


def pin(path):
    b = (ROOT/path).read_bytes()
    return {'path': path, 'bytes': len(b), 'sha256': sha(b), 'git_blob': hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def catalog(ex):
    rows = [('LOTTERY', 'items', {'name': ex['lottery_name'], 'context': ex['acquisition_context'], 'price': ex['price_as_reported']})]
    rows += [('PET'+str(i), 'pets', v) for i,v in enumerate(ex['named_pet_relative_rates'],1)]
    rows += [('WINDOW', 'tutorials', {'window': ex['rate_window_using_publication_year'], 'sale_end': True, 'other_types': ex['other_pet_types_count'], 'other_direction': ex['other_rate_direction']})]
    return [{'record_id': 'JP2007-R78-'+ident, 'collection': coll, 'content': c, 'version_profile': PROFILE,
             'source_refs': ['S1'], 'verification_status': 'SOURCE_REPORTED_NOT_RUNTIME',
             'rights_status': 'RESEARCH_METADATA_NOT_RELEASE_APPROVED', 'game_ids': None, 'record_revision': 1} for ident,coll,c in rows]


def validate(r):
    require(r['schema'] == 'stoneage.jp2007_ebony_lottery.source.r1' and r['version_profile'] == PROFILE, 'Version/schema changed')
    require(r['negative_boundaries'] == BOUNDARIES, 'Authority boundary promoted')
    require(r['source']['url'] == URL and r['source']['authority'] == 'UTD_RELEASE_EXPLICITLY_REPUBLISHED_BY_4GAMER', 'Source authority changed')
    require(r['parent_pins'] == [pin(p) for p in PARENTS] and r['parser_pin'] == pin(PARSER), 'Parent/parser original bytes changed')
    ex = r['extraction']
    require(ex['acquisition_context'] == 'PAID_SHOP_LOTTERY_NOT_WILD_ENCOUNTER', 'Lottery became wild ecology')
    require(all(ex[k] is None for k in ('timezone_explicit', 'other_pet_names', 'absolute_rates_or_normalization_formula', 'guarantee_or_pity', 'pet_stats_growth_skills_habitat', 'exact_build')), 'Unknown values invented')
    require(ex['year_in_window_body_explicit'] is False and ex['price_as_reported']['purchase_unit_or_bundle_count'] is None, 'Year/unit promoted')
    require(ex['price_as_reported'] == {'amount':1000,'currency':'GStone','shop':'マンモストア','purchase_unit_or_bundle_count':None}, 'Shop price/currency changed')
    require(all(all(v[k] is None for k in ('base_probability','changed_probability','original_species_id')) for v in ex['named_pet_relative_rates']), 'Relative rate promoted')
    require(r['catalog_records'] == catalog(ex), 'Catalog changed or detached')
    require(r['comparison'] == {'gash_capture_campaign_is_separate_acquisition_and_currency': True,
                              'same_pet_ids_or_build_proven': False, 'modern_adoption_decided': False}, 'Cross-version merge')
    require(r['archive_discovery']['requested_timestamp'] == '20070730' and r['archive_discovery']['closest_timestamp'] == '20070805235420' and r['archive_discovery']['capture_fetched'] is False, 'Availability became acquired original page')
    require(r['visual_observations'] == [
        {'id': 'I1', 'kind': 'SHOP_PROMOTIONAL_BANNER', 'manual_visual_review': True, 'description': 'Red-brown horned creature, flame and limited-sale wording; no species label or stats.', 'original_sprite_or_animation_proven': False},
        {'id': 'I2', 'kind': 'TWO_CREATURE_PROMOTIONAL_ILLUSTRATION', 'manual_visual_review': True, 'description': 'Grey and brown horned creatures face one another against a red burst; no individual name labels.', 'left_right_named_species_join': None, 'original_sprite_or_animation_proven': False}], 'Image observations promoted')
    require([(v['bytes'],v['sha256'],v['size']) for v in r['images']] == [
        (26401,'b511b1091843075a2f8e08915fa2b7fc1fda4fbb83197e89a4d71b56bdd2b516',[140,240]),
        (44950,'194a88bf354674e896bbfb871858d26f15aa3ddc34010665d98dee73c4b62fac',[306,189])], 'Observations detached from reviewed images')


MUTATIONS = [('7月27日より販売','7月26日より販売'), ('くじ」でのレアペット出現確率','野外でのレアペット出現確率'),
             ('18:00より','17:00より'), ('13:00まで','12:00まで'), ('販売終了）','確率変更終了）'),
             ('1000 GStone','2000 GStone'), ('仮想通貨です','ゲーム内Stoneです'),
             ('ギガドラン','別のペット'), ('ドルーザス','別の恐竜'), ('出現確率2倍','出現確率3倍'),
             ('ほか4種類','ほか5種類'), ('若干低く','若干高く'), ('本日18時以降','本日19時以降')]


def audit(raw, expected):
    text = raw.decode('cp932'); target = {k:v for k,v in expected.items() if k != 'core_fingerprint'}
    for old,new in MUTATIONS:
        require(old in text, 'Mutation absent: '+old)
        try: got = derive(text.replace(old,new).encode('cp932'))
        except (ValueError,IndexError): continue
        got.pop('core_fingerprint'); require(got != target, 'Semantic change masked by fingerprint: '+old)
    require(derive(raw+b'<script>peripheral=1</script>') == expected, 'Peripheral script changed meaning')
    # Hidden body evidence and same words outside the quotation cannot repair a missing claim.
    old = '※ほか4種類はこれに伴い、出現確率が若干低くなります'
    for replacement in ('<script>'+old+'</script>', ''):
        changed = text.replace(old,replacement) + '<div>'+old+'</div>'
        try: derive(changed.encode('cp932'))
        except ValueError: pass
        else: raise ValueError('Outside/hidden text repaired missing quotation evidence')
    return {'semantic_mutations_without_fingerprint_gate': len(MUTATIONS), 'hidden_and_outside_quote_counterexamples': 2, 'peripheral_script_positive': True}


def inspect_images(inputs, r):
    for idx,p in enumerate(r['images']):
        b = inputs[p['id']]
        with Image.open(io.BytesIO(b)) as im:
            im.load(); actual = {'bytes':len(b),'sha256':sha(b),'format':im.format,'mode':im.mode,'size':list(im.size)}
        require(all(p[k] == v for k,v in actual.items()) and p['url'] == r['extraction']['image_references'][idx], 'Image changed or detached')


def replay(inputs, r):
    validate(r); ex = derive(inputs['S1']); require(ex == r['extraction'], 'Source content changed')
    inspect_images(inputs, r)
    return {'schema': 'stoneage.jp2007_ebony_lottery.replay.r1',
            'inputs': [{'id':k, 'bytes':len(v), 'sha256':sha(v)} for k,v in inputs.items()],
            'extraction': ex, 'images': r['images'], 'visual_observations': r['visual_observations'],
            'catalog_records': catalog(ex), 'comparison': r['comparison'], 'audit': audit(inputs['S1'],ex),
            'original_html_or_assets_in_output': False, 'original_server_runtime_verified': False}


def read_inputs(directory=None):
    urls = {'S1': URL, 'I1': URL.replace('history/2007.07/20070730194730detail.html','image/2007.07/20070730194730_0.jpg'),
            'I2': URL.replace('history/2007.07/20070730194730detail.html','image/2007.07/20070730194730_3.jpg')}
    result = {}
    for key,url in urls.items():
        if directory:
            result[key] = (Path(directory)/(key+('.html' if key=='S1' else '.jpg'))).read_bytes()
        else:
            with urllib.request.urlopen(url,timeout=45) as response:
                require(response.status == 200 and response.url == url, 'HTTP status or redirect changed')
                result[key] = response.read()
    return result


def main():
    p = argparse.ArgumentParser(); p.add_argument('--input-dir'); p.add_argument('--fetch',action='store_true'); p.add_argument('--output',required=True); a = p.parse_args()
    require(bool(a.input_dir) != a.fetch, 'Choose input directory or live fetch')
    result = replay(read_inputs(a.input_dir),json.loads(REPORT.read_text()))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('R78 bounded source replay passed; original server execution remains unproven.')


if __name__ == '__main__': main()
