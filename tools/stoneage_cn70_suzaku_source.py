"""Replay one attributed Wayi release, two linked images, and one older portal.

Downloads are transient; output contains derived metadata only. Current HTTP
fingerprints do not authenticate 2002/2003 snapshots or original server data.
"""
import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-CN70-SUZAKU-MYTH-VISUAL-SOURCE-R1.json'
URLS = (
    'https://games.sina.com.cn/newgames/2003/12/121610098.shtml',
    'https://www.ourgame.com/news/db/32/31192.html',
    'https://image2.sina.com.cn/gm/newgames/2003/12/U163P115T9D10098F364DT20031216143816.jpg',
    'https://image2.sina.com.cn/gm/newgames/2003/12/U163P115T9D10098F167DT20031216143816.JPG',
)
NAMES = ('suzaku.html', 'ourgame.html', 'suzaku-art.jpg', 'suzaku-stats.jpg')


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.images, self.hidden = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if not self.hidden:
            self.text.append(' ')
            if tag == 'img':
                self.images.append(dict(attrs).get('src'))

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1
        if not self.hidden:
            self.text.append(' ')

    def handle_data(self, data):
        if not self.hidden:
            self.text.append(data)


def parse(html):
    p = Visible()
    p.feed(html)
    return re.sub(r'\s+', '', ''.join(p.text)), p.images


def extract_release(payload):
    html = payload.decode('gb18030')
    require(html.count('<!-- 内容 begin -->') == 1 and html.count('<!-- 内容 end -->') == 1,
            'Missing/ambiguous publisher article boundary')
    body = html.split('<!-- 内容 begin -->', 1)[1].split('<!-- 内容 end -->', 1)[0]
    text, images = parse(body)
    require(text.startswith('以下是来自华义的最新官方消息：'), 'Operator attribution missing inside article')
    require('石器时代7.0' in text and '7.0石头就业所' in text, 'Edition labels missing')
    require(len(images) == 2 and images == [u.replace('https:', 'http:') for u in URLS[2:]], 'Actual article image links changed')
    core = text[text.index('传说四大神兽，'):text.index('拍卖现场：')]
    mappings = re.findall(r'\[([^\]]+)\]封印着关于([^的]+)的技能', core)
    require(len(mappings) == 4 and len({x[0] for x in mappings}) == 4, 'Four source skill affiliations required')
    # The source separates the four temple strings with Chinese commas, so use
    # a bounded sentence rather than inferring real map IDs from their names.
    temple_sentence = core.split('被分别封印在', 1)[1].split('久久不能得到自由', 1)[0]
    temple_labels = re.findall(r'[水风地火]神殿', temple_sentence)
    require(len(temple_labels) == 4, 'Four narrative temples required')
    form = re.findall(r'朱雀——([^吧！]+)吧！', core)
    require(len(form) == 1, 'Named pet form missing or ambiguous')
    require('朱雀攻高，敏高，防低' in core, 'Qualitative combat description missing')
    return {'core_sha256': sha256(core.encode()).hexdigest(), 'core_utf8_bytes': len(core.encode()),
            'facts': {'beast_skill_affiliations': [{'beast': b, 'skill_element': e} for b, e in mappings],
                      'temples_as_ordered_text_not_map_ids': temple_labels,
                      'named_suzaku_form': form[0], 'pure_fire_reported': '纯火属性的朱雀' in core,
                      'relative_stat_description': {'attack': 'HIGH', 'agility': 'HIGH', 'defense': 'LOW'},
                      'seal_context_mentions_light_dark_king_battle': '光明精灵王与黑暗精灵王一战' in core,
                      'source_images_declared_http': images}}


def extract_older_portal(payload):
    text, _ = parse(payload.decode('gb18030'))
    require('设计公司：北京华义' in text and '发行公司：北京华义' in text, 'Company labels missing')
    require('《石器时代2.5》上市！(2002-2-5)' in text, 'Earlier portal date/title missing')
    core = text[text.index('原来除了被困漆黑深处'):text.index('天空之岛现身：')]
    return {'core_sha256': sha256(core.encode()).hexdigest(), 'core_utf8_bytes': len(core.encode()),
            'facts': {'operator_authored_release_explicitly_credited': False,
                      'company_metadata_is_authorship_proof': False,
                      'two_kings_cooperate_against_machine_civilization_reported': '两位精灵王为了拯救苍生，毅然挑战机器文明' in core,
                      'dark_king_self_seal_reported': '黑暗精灵王按照约定' in core and '自身封印了' in core,
                      'light_king_machine_seal_reported': '自身反被机器文明所封印' in core,
                      'marefia_lost_memory_and_pet_rebirth_story_reported': '失忆的精灵少女玛蕾菲雅' in core and '宠物一次重生的机会' in core}}


def jpeg_dimensions(payload):
    require(payload[:2] == b'\xff\xd8', 'Linked asset is not JPEG')
    pos = 2
    while pos + 4 <= len(payload):
        require(payload[pos] == 255, 'Invalid JPEG marker')
        while pos < len(payload) and payload[pos] == 255:
            pos += 1
        require(pos < len(payload), 'Truncated JPEG marker')
        marker = payload[pos]
        pos += 1
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            continue
        require(pos + 2 <= len(payload), 'Truncated JPEG segment')
        length = int.from_bytes(payload[pos:pos + 2], 'big')
        require(length >= 2 and pos + length <= len(payload), 'Invalid JPEG segment length')
        if marker in (0xC0, 0xC1, 0xC2):
            require(length >= 8, 'Short JPEG frame')
            height, width = struct.unpack('>HH', payload[pos + 3:pos + 7])
            return [width, height]
        pos += length
    raise ValueError('JPEG dimensions not found')


def validate_report(report):
    require(report['schema'] == 'stoneage.cn70_suzaku_myth_visual_source.r1', 'Unknown schema')
    require([s['http']['url'] for s in report['inputs']] == list(URLS), 'Finite source set changed')
    require(len(report['records']) == 7, 'Seven bounded research records required')
    require(report['inputs'][0]['authority'] == 'WAYI_OFFICIAL_MESSAGE_EXPLICITLY_ATTRIBUTED_BY_SINA', 'Official release attribution changed')
    require(report['inputs'][1]['authority'] == 'DATED_PORTAL_RELEASE_ARTICLE_AUTHOR_NOT_VERIFIED', 'Older portal promoted to operator author')
    require(all(s['historical_original_byte_sha256'] is None for s in report['inputs']), 'Current bytes promoted to original-era snapshot')
    required = {'record_id', 'entity_type', 'version_profile', 'source_refs', 'verification_status', 'rights_status', 'record_revision'}
    for record in report['records']:
        require(required <= record.keys(), 'Missing archive fields')
        require(record['rights_status'] == 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'Original art rights promoted')
        require(record['verification_status'] in ('SOURCE_REPORTED_NOT_RUNTIME', 'MANUAL_IMAGE_OBSERVATION_NOT_SPECIES_MASTER', 'SOURCE_RELATION_NOT_CANON_MERGE'), 'Runtime promotion')
        require(record['game_ids'] is None, 'Invented game ID')
    require(report['visual_observations']['status_image']['observed_individual_values'] == {
        'level': 1, 'experience': 0, 'next_experience_display': 2, 'hp_current': 78, 'hp_max': 78,
        'attack': 21, 'defense': 7, 'agility': 11, 'loyalty': 100}, 'Manually inspected display values changed')
    require(report['visual_observations']['status_image']['growth_rates'] is None
            and report['visual_observations']['status_image']['numeric_element_weights'] is None
            and report['visual_observations']['status_image']['name_line_transcription'] is None, 'Unclear pixel/name or growth/element values invented')
    require(report['boundaries'] == {
        'historical_2003_snapshot_authenticated': False, 'original_server_execution_verified': False,
        'original_pet_species_master_recovered': False, 'exact_client_build': None,
        'four_skill_affiliations_are_four_pet_attribute_vectors': False,
        'ordered_temple_names_are_map_or_npc_ids': False, 'single_lv1_sample_is_growth_table': False,
        'concept_art_to_sprite_or_animation_join_verified': False,
        'both_articles_share_one_canon_or_chronology': False, 'retcon_or_contradiction_proven': False,
        'auction_is_quest_reward_or_capture_rule': False, 'commercial_transaction_performed': False,
        'tw10_or_jss1999_backfill': False, 'original_html_or_images_committed': False,
        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'
    }, 'Historical boundary changed')
    require(report['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-23', 'Return to portfolio required')


def replay(report, payloads):
    validate_report(report)
    require(len(payloads) == 4, 'Exactly two HTML and two actual linked images required')
    extracted = [extract_release(payloads[0]), extract_older_portal(payloads[1])]
    for got, source in zip(extracted, report['inputs'][:2]):
        require(got['core_sha256'] == source['core_sha256'] and got['core_utf8_bytes'] == source['core_utf8_bytes'], 'Narrative core changed')
        require(got['facts'] == source['extracted_facts'], 'Source facts differ')
    images = []
    for payload, source in zip(payloads[2:], report['inputs'][2:]):
        require(sha256(payload).hexdigest() == source['http']['sha256'], 'Pinned image bytes changed')
        size = jpeg_dimensions(payload)
        require(size == source['dimensions'], 'Image dimensions changed')
        images.append({'source_id': source['id'], 'bytes': len(payload), 'sha256': sha256(payload).hexdigest(), 'dimensions': size})
    return {'schema': 'stoneage.cn70_suzaku_source.replay.r1',
            'current_http': [{'source_id': s['id'], 'bytes': len(b), 'sha256': sha256(b).hexdigest()} for s, b in zip(report['inputs'], payloads)],
            'narrative_cores': extracted, 'images': images, 'raw_html_or_image_bytes_in_output': False,
            'historical_snapshot_species_master_or_runtime_verified': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-dir', type=Path)
    p.add_argument('--fetch', action='store_true')
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    require(bool(a.source_dir) != a.fetch, 'Choose supplied transient files or four fixed URLs')
    report = json.loads(REPORT.read_text())
    payloads = []
    for url, name in zip(URLS, NAMES):
        if a.fetch:
            with urllib.request.urlopen(url, timeout=40) as response:
                require(response.status == 200 and response.url == url, 'Unexpected HTTP response/redirect')
                data = response.read(2_000_001)
                require(len(data) <= 2_000_000, 'Oversized source')
        else:
            data = (a.source_dir / name).read_bytes()
        payloads.append(data)
    result = replay(report, payloads)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('NARRATIVE_CORES_VERIFIED=2 LINKED_IMAGES_VERIFIED=2 ORIGINAL_RUNTIME_EXECUTIONS=0')


if __name__ == '__main__':
    main()
