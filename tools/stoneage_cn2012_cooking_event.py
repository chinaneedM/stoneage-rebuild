"""A bounded operator promotion: cooking event chain, not a server recipe table."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from tools.stoneage_cn2011_stall_source import Article, jpeg_dimensions
from tools.stoneage_cn2003_group2_manor_report import fetch

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN2012-COOKING-EVENT'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
URL = 'https://games.sina.com.cn/o/n/2012-02-10/1551581681.shtml'
PROFILE = 'LATER_OFFICIAL:CN_CINS_2012_PROMOTION_SERVER_SCOPE_UNRESOLVED'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class SourceArticle(Article):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if self.article_depth and not self.block and tag == 'a':
            self.links.append(dict(attrs).get('href'))


def parse(raw):
    t = raw.decode('gb18030', errors='strict')
    require('2012年02月10日 15:51' in t, 'Publication stamp changed')
    p = SourceArticle()
    p.feed(t)
    require(p.roots == 1 and len(p.images) == 3, 'Article/image scope changed')
    require(len(p.paragraphs) >= 16, 'Incomplete article')
    require(p.paragraphs[0].startswith('经典Q版回合制网游《石器时代》“高厨料理”'), 'Article start changed')
    require(p.paragraphs[-1].startswith('声明：新浪网游戏频道'), 'Disclaimer boundary changed')
    require(p.links.count('http://sa.cins.cn') == 2, 'Actual official links changed')
    return p.paragraphs[:-1], p.images


def extract(raw):
    paragraphs, images = parse(raw)
    t = ''.join(paragraphs)
    schedule = re.search(r'从(周一)到(周日)、每晚(\d\d:\d\d)~(\d\d:\d\d)点“(高厨料理)”准时开启', t)
    require(schedule, 'Named event/schedule missing')
    require('先准备一只懂调制料理的宠物' in t and '村庄宠物店学习料理技能' in t, 'Pet prerequisite/training changed')
    trade = re.search(r'在活动时间内，.*?NPC(扑满乌力)和NPC(黑乌力)”[，,]就能(购买)到各种珍贵食材.*?“(扑满乌力的蔬菜色拉)”(或者)“(黑乌力的蔬菜色拉)”，然后.*?到(加加村24店)里的NPC(大厨)处(换取奖励)', t)
    require(trade, 'Vendor/cooking/delivery sequence changed')
    require('这些珍贵食材、加上你的料理宠物的精心调制' in t, 'Cooking actor/material relation changed')
    require('原始人可以获得珍贵的荣誉值' in t and '在荣誉商城换购' in t, 'Reward/currency changed')
    require('珍稀宠物、给力道具以及超强的装备' in t, 'Redemption categories changed')
    require('更多精彩，敬请继续锁定胜思网络' in t and '广东胜思网络科技有限公司全权负责' in t, 'Promoter attribution changed')
    versions = re.search(r'(8\.5)(魔域大冒险)版本.*?《石器时代》(2\.5)“(精灵王传说)”版本服务器', t)
    require(versions, 'Two advertised server labels missing')
    return {
        'core_sha256': sha('\n'.join(paragraphs).encode()),
        'issuer_evidence': 'SINA_HOSTED_CINS_NAMED_PROMOTIONAL_COPY_NOT_AUTHENTICATED_ORIGINAL_ISSUER_FILE',
        'official_link_as_written': 'http://sa.cins.cn',
        'event': schedule[5],
        'schedule': {'weekday_start': schedule[1], 'weekday_end': schedule[2], 'start_clock': schedule[3], 'end_clock': schedule[4],
                     'timezone': None, 'endpoint_inclusivity': None, 'launch_date': None, 'daily_limit': None, 'live_execution_verified': False},
        'pet': {'prerequisite': 'PET_WITH_COOKING_SKILL', 'training_location': '村庄宠物店', 'skill_id_price_or_species_limits': None},
        'flow': {'vendors_as_written': [trade[1], trade[2]], 'acquisition': trade[3],
                 'products_as_written': [trade[4], trade[6]], 'product_connector_as_written': trade[5],
                 'delivery_location_as_written': trade[7], 'recipient_as_written': trade[8], 'delivery_action': trade[9],
                 'ingredients_recipes_prices_coordinates_ids': None, 'both_products_required': None,
                 'vendor_to_product_exact_recipe_mapping': None, 'consumption_and_transaction_rules': None},
        'reward': {'currency_as_written': '荣誉值', 'redemption_place_as_written': '荣誉商城',
                   'reported_categories': ['宠物', '道具', '装备'], 'amount_rate_daily_cap_or_stock': None,
                   'cash_equivalence_or_tradeability': None},
        'server_context': {'advertised_labels': [versions[1] + versions[2], versions[3] + versions[4]],
                           'event_applicable_groups': None, 'exact_client_build': None, 'belongs_to_original_2002_25': False,
                           'belongs_to_tw10_or_jss1999': False},
        'images': images, 'historical_server_executed': False,
    }


MUTATIONS = (
    ('weekday', '从周一到周日', '从周一到周五'),
    ('start-clock', '19:00~21:00', '18:00~21:00'),
    ('end-clock', '19:00~21:00', '19:00~22:00'),
    ('cooking-pet', '先准备一只懂调制料理的宠物', '先准备一只不懂调制料理的宠物'),
    ('training', '村庄宠物店学习料理技能', '村庄医院学习料理技能'),
    ('vendor', 'NPC扑满乌力和NPC黑乌力', 'NPC扑满乌力和NPC白乌力'),
    ('purchase', '就能购买到各种珍贵食材', '就能免费领到各种珍贵食材'),
    ('first-dish', '“扑满乌力的蔬菜色拉”', '“扑满乌力的水果色拉”'),
    ('second-dish', '“黑乌力的蔬菜色拉”', '“白乌力的蔬菜色拉”'),
    ('or-vs-and', '色拉”或者“黑乌力', '色拉”以及“黑乌力'),
    ('handover-place', '加加村24店', '萨姆吉尔24店'),
    ('recipient', 'NPC大厨处换取奖励', 'NPC护士处换取奖励'),
    ('reward-action', 'NPC大厨处换取奖励', 'NPC大厨处购买奖励'),
    ('currency', '原始人可以获得珍贵的荣誉值', '原始人可以获得珍贵的石币'),
    ('redemption', '在荣誉商城换购', '在现金商城换购'),
    ('version-context', '8.5魔域大冒险版本', '8.0魔域大冒险版本'),
    ('second-context', '2.5“精灵王传说”版本服务器', '1.82“精灵王传说”版本服务器'),
    ('official-link', 'href="http://sa.cins.cn"', 'href="http://example.invalid"'),
    ('actual-image-link', 'DT20120210155002.jpg', 'DT20120210155003.jpg'),
)


def audit(raw, expected):
    t = raw.decode('gb18030')
    checks = []
    for label, old, new in MUTATIONS:
        # Link change deliberately changes both in-article references.
        require(t.count(old) == (2 if label == 'official-link' else 1), 'Ambiguous mutation: ' + label)
        changed = t.replace(old, new).encode('gb18030')
        try:
            actual = extract(changed)
            rejected = {k: v for k, v in actual.items() if k != 'core_sha256'} != {k: v for k, v in expected.items() if k != 'core_sha256'}
        except ValueError:
            rejected = True
        require(rejected, 'Semantic mutation accepted: ' + label)
        checks.append({'case': label, 'input_sha256': sha(changed), 'rejected_without_digest_gate': True})
    require(extract(raw + b'<script>outside only</script>') == expected, 'Outer positive rejected')
    return {'real_source_mutations': checks, 'outer_script_positive': True}


def validate(r):
    local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
    require(r['extracted'] == local['extracted'], 'Source semantics changed')
    require(r['source']['url'] == URL and r['source']['encoding'] == 'GB18030_STRICT', 'Source URL/encoding changed')
    require(r['source']['published'] == '2012-02-10 15:51' and r['source']['authenticated_2012_original_bytes'] is False, 'Source date promotion')
    require(r['source']['authority'] == local['extracted']['issuer_evidence'], 'Source authority promotion')
    require(r['source']['current_observed_bytes'] == local['http_bytes'] and r['source']['current_observed_sha256'] == local['http_sha256'], 'Observed source pins changed')
    keys = ['schedule', 'pet', 'flow', 'reward', 'server_context']
    require(len(r['records']) == len(keys), 'Bounded five record scope')
    for key, row in zip(keys, r['records']):
        require(row['record_id'] == 'CN2012-COOKING-' + key.upper() and row['evidence'] == r['extracted'][key], 'Record/evidence alignment')
        require(row['version_profile'] == PROFILE and row['game_ids'] is None, 'Version or IDs invented')
        require(row['evidence_status'] == 'SOURCE_REPORTED_NOT_RUNTIME_VERIFIED', 'Evidence promotion')
    require(r['images'] == local['images'] and len(r['images']) == 2, 'Image pins/observation changed')
    require([x['url_as_written'] for x in r['images']] == [x['src'] for x in r['extracted']['images'][:2]], 'Not actual source-linked images')
    for im in r['images']:
        require(im['requested_url'] == im['url_as_written'].replace('http:', 'https:'), 'URL rewrite changed')
        require(im['cooking_event_or_recipe_proven'] is False and im['capture_date'] is None, 'Crowd screenshot promoted')
    require(all(v is False for v in r['unproven'].values()), 'Unsupported conclusion promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'}, 'Stage changed')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-49', 'Queue changed')


def replay(r, raw, pictures):
    validate(r)
    x = extract(raw)
    require(x == r['extracted'], 'Source body changed')
    require(len(pictures) == len(r['images']), 'Image payload count')
    for pin, b in zip(r['images'], pictures):
        require(len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'Current image bytes changed')
        require(jpeg_dimensions(b) == (pin['width'], pin['height']), 'Image dimensions changed')
    return {'schema': 'stoneage.cn2012_cooking_event.derived_replay.r1', 'http_bytes': len(raw), 'http_sha256': sha(raw),
            'extracted': x, 'images': r['images'], 'audit': audit(raw, x),
            'raw_html_or_assets_in_output': False, 'historical_server_executed': False}


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch', action='store_true')
    g.add_argument('--html', type=Path)
    p.add_argument('--images', type=Path, nargs=2)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r = json.loads(REPORT.read_text())
    if a.fetch:
        raw = fetch(URL, 1000000)
        pictures = [fetch(x['requested_url'], 2000000) for x in r['images']]
    else:
        if not a.images:
            p.error('--images is required with --html')
        raw, pictures = a.html.read_bytes(), [x.read_bytes() for x in a.images]
    out = replay(r, raw, pictures)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'http_bytes': len(raw), 'images': len(pictures), 'semantic_mutations': len(out['audit']['real_source_mutations'])}))


if __name__ == '__main__':
    main()
