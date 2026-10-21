"""One operator-hosted healing table; preserve source anomalies and no runtime formula."""
import argparse
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from tools.stoneage_cn2003_group2_manor_report import Visible
from tools.stoneage_cn20_recordpoint_source import fetch

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-CN20-HEALING-SPELLS'
REPORT = ROOT / ('research/recovered/' + STEM + '-SOURCE-R1.json')
NAV_URL = 'https://web.archive.org/web/20011204194619id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp'
BODY_URL = 'https://web.archive.org/web/20011204210425id_/http://www.waei.com.cn/ZHUANQU/stoneage2/spell/huifu.asp'
BATTLE_PARENT = 'research/recovered/STONEAGE-CN20-BATTLE-COMMANDS-DEFEAT-SOURCE-R1.json'
PROFILE = 'CN_OPERATOR_HOST_2.0_HEALING_GUIDE_CAPTURE_2001_NOT_EXACT_BUILD'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def compact(s):
    p = Visible(); p.feed(s)
    return re.sub(r'\s+', '', ''.join(p.parts))


class Table(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        elif tag == 'td' and self.row is not None:
            self.cell = {'text': [], 'rowspan': int(dict(attrs).get('rowspan', '1'))}

    def handle_data(self, data):
        if self.cell is not None:
            self.cell['text'].append(data)

    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.cell['text'] = re.sub(r'\s+', '', ''.join(self.cell['text']))
            self.row.append(self.cell); self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row); self.row = None


def section(raw):
    t = raw.decode('gb18030', errors='strict')
    require('<title>石器时代2.0</title>' in t and t.count('回 复 系 法 术') == 1, 'Actual page/title changed')
    t = t.split('回 复 系 法 术', 1)[1]
    # One content table; copyright/footer begins after its closing outer table.
    end = '<link rel="stylesheet" href="/ZHUANQU/stoneage2/Style.css"'
    require(t.count(end) == 1, 'Footer boundary changed')
    return t.split(end, 1)[0]


def extract(nav, raw):
    nt = nav.decode('gb18030', errors='strict')
    routes = re.findall(r'<a\b[^>]*href=["\'](/ZHUANQU/stoneage2/spell/huifu.asp)["\'][^>]*>(.*?)</a>', nt, re.S | re.I)
    require(len(routes) == 1 and compact(routes[0][1]) == '回复系', 'Authentic healing navigation changed')
    content = section(raw)
    tables = re.findall(r'<table\b[^>]*>(.*?)</table>', content, re.S | re.I)
    require(len(tables) == 1, 'One healing table required')
    intro = compact(content.split('<table', 1)[0])
    named = re.search(r'治愈精灵(.+?)、滋润精灵(.+?)、神恩精灵(.+?)这三种精灵', intro)
    revivals = re.search(r'复活系的精灵有(.+?)、(.+?)、(.+?)等三种', intro)
    order = re.search(r'他们回复量的顺序是(.+?)、(.+?)、(.+?)。', intro)
    require(named and revivals and order, 'Named spirits or revival order changed')
    clauses = ['哈鲁只能回复玩家', '芙蕾雅是可回复我方一人或宠物一匹的精灵', '提欧是可以对全员施展回复法术的精灵',
               '精灵主要是寄宿在衣服、铠甲等防具里', '在战斗中如果宠物昏厥了，记得要把他们救活喔',
               '忠诚度不会下降很多而且又有经验值']
    require(all(x in intro for x in clauses), 'Target, mainly-equipment or qualified pet revival advice changed')
    parser = Table(); parser.feed(tables[0])
    require([x['text'] for x in parser.rows[0]] == ['精灵名称', '等级', '效果', '消耗气力'], 'Actual headers changed')
    rows = []; remaining = 0; label = None
    for cells in parser.rows[1:]:
        if remaining == 0:
            require(len(cells) == 4 and cells[0]['rowspan'] > 0, 'New rowspan group required')
            namecell, *cells = cells; label = namecell['text']; remaining = namecell['rowspan']
        else:
            require(len(cells) == 3, 'Rowspan group overlap or missing row')
        require(all(c['rowspan'] == 1 for c in cells), 'Unexpected non-name rowspan')
        level, effect, cost = [c['text'] for c in cells]
        lm = re.fullmatch(r'LV(\d+)', level); cm = re.fullmatch(r'\d+', cost)
        heal = re.fullmatch(r'回复(自己|单体|己方全体)的耐久力\+(\d+)', effect)
        revive = re.fullmatch(r'令(单体)复活，并回复耐久力\+(\d+)', effect)
        require(lm and cm and (heal or revive), 'Actual level/effect/cost shape changed')
        m = heal or revive
        rows.append({'table_label_as_written': label, 'level_as_written': level, 'listed_level': int(lm[1]),
                     'effect_as_written': effect, 'target_as_written': m[1], 'stat_as_written': '耐久力',
                     'listed_recovery_amount': int(m[2]), 'revival_described': revive is not None,
                     'cost_column_as_written': '消耗气力', 'listed_cost': int(cost),
                     'player_level_requirement_or_original_spell_id': None, 'runtime_stat_field_formula_caps_or_timing': None})
        remaining -= 1
    require(remaining == 0 and len(rows) == 13, 'Finite thirteen rows and closed rowspans required')
    require(not re.search(r'<img\b', content, re.I), 'New article image needs explicit review')
    return {'route': {'label': '回复系', 'href': routes[0][0]},
            'core_sha256': sha((intro + compact(tables[0])).encode()), 'rows': rows,
            'intro': {'healing_roles_and_names_as_written': [{'role': role, 'name': name} for role, name in zip(['治愈精灵', '滋润精灵', '神恩精灵'], named.groups())],
                      'halu_scope_as_written': '只能回复玩家', 'freya_scope_as_written': '我方一人或宠物一匹', 'tio_scope_as_written': '全员',
                      'equipment_mainly_as_written': ['衣服', '铠甲', '等防具'], 'all_equipment_or_exclusive_rule': None,
                      'revival_names_as_written': list(revivals.groups()), 'revival_recovery_order_as_written': list(order.groups()),
                      'order_direction_and_name_to_lv_mapping': None, 'pet_faint_revive_is_advice': True,
                      'loyalty_phrase_as_written': '不会下降很多', 'experience_phrase_as_written': '又有经验值',
                      'exact_loyalty_loss_experience_amount_or_no_penalty': None},
            'content_images': 0, 'authorship': 'OPERATOR_HOSTED_UNSIGNED_GUIDE_AUTHOR_UNVERIFIED',
            'publication_date': None, 'exact_client_build': None, 'original_game_executed': False}


MUTATIONS = (
    (0, 'nav-label', '>回复系</font></a>', '>恢复系</font></a>'),
    (0, 'nav-path', '/spell/huifu.asp', '/spell/missing.asp'),
    (1, 'named-healer', '治愈精灵哈鲁', '治愈精灵卡鲁'),
    (1, 'halu-player-only', '哈鲁只能回复玩家', '哈鲁可以回复玩家和宠物'),
    (1, 'freya-target', '我方一人或宠物一匹', '我方所有人物和宠物'),
    (1, 'tio-scope', '可以对全员施展', '可以对敌人全员施展'),
    (1, 'mainly-not-only', '精灵主要是寄宿', '精灵只能寄宿'),
    (1, 'revival-name-order', '顺序是希鲁菲尔、雅鲁、哈恩', '顺序是哈恩、雅鲁、希鲁菲尔'),
    (1, 'qualified-loyalty', '忠诚度不会下降很多', '忠诚度完全不会下降'),
    (1, 'experience-advice', '而且又有经验值', '而且保证恢复全部经验值'),
    (1, 'source-plus-ten', '回复单体的耐久力+10</td>', '回复单体的耐久力+100</td>'),
    (1, 'source-self-target', '回复自己的耐久力+50', '回复单体的耐久力+50'),
    (1, 'allied-all-target', '回复己方全体的耐久力+50', '回复敌方全体的耐久力+50'),
    (1, 'revive-amount', '令单体复活，并回复耐久力+100', '令单体复活，并回复耐久力+300'),
    (1, 'table-name-not-intro-name', '恩惠的精灵</td>', '神恩的精灵</td>'),
    (1, 'rowspan', 'rowspan="4"', 'rowspan="5"'),
    (1, 'level-not-player-requirement', '>LV1</td>', '>人物LV1</td>'),
    (1, 'cost-number', 'align="center">5</td>', 'align="center">6</td>'),
)


def audit(raws, expected):
    out = []
    for i, label, old, new in MUTATIONS:
        t = raws[i].decode('gb18030'); require(old in t, 'Mutation anchor missing: ' + label)
        changed = list(raws); changed[i] = t.replace(old, new).encode('gb18030')
        try:
            x = extract(*changed)
            rejected = {k: v for k, v in x.items() if k != 'core_sha256'} != {k: v for k, v in expected.items() if k != 'core_sha256'}
        except ValueError:
            rejected = True
        require(rejected, 'Semantic mutation accepted: ' + label)
        out.append({'case': label, 'source_index': i, 'input_sha256': sha(changed[i]), 'rejected_without_digest_gate': True})
    require(extract(*[b + b'<script>outer only</script>' for b in raws]) == expected, 'Outer script positive failed')
    return {'real_source_mutations': out, 'outer_script_positive': True}


def validate(r):
    local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())
    require(r['schema'] == 'stoneage.cn20_healing_spells.source.r1' and r['extracted'] == local['extracted'], 'Source semantics changed')
    require([x['url'] for x in r['sources']] == [NAV_URL, BODY_URL], 'Exact two captures required')
    require([x['capture_timestamp'] for x in r['sources']] == ['20011204194619', '20011204210425'], 'Capture conflation')
    for s, observed in zip(r['sources'], local['http']):
        require(s['bytes'] == observed['bytes'] and s['sha256'] == observed['sha256'] and s['encoding'] == 'GB18030_STRICT', 'HTTP pin/encoding changed')
        require(s['publication_date'] is None and s['exact_client_build'] is None, 'Capture promoted to publication/build')
    require([s['role'] for s in r['sources']] == ['KNOWN_NAVIGATION_REACQUIRED', 'OPERATOR_HOSTED_UNSIGNED_HEALING_GUIDE'], 'Source role promoted')
    pin = r['prior_battle_context']['parent']; b = (ROOT / BATTLE_PARENT).read_bytes()
    require(pin['path'] == BATTLE_PARENT and len(b) == pin['bytes'] and sha(b) == pin['sha256'] and blob(b) == pin['git_blob'], 'Prior source identity changed')
    old = json.loads(b)
    require(old['records'][1]['record_id'] == 'CN20-BATTLE-02' and old['records'][1]['source_reported']['meaning'] == 'SPIRIT_MAGIC_ATTACHED_TO_EQUIPMENT', 'Prior qualitative spell context differs')
    require(r['prior_battle_context']['qualitative_equipment_context_only'] is True and r['prior_battle_context']['same_client_build_or_runtime_formula_proven'] is False, 'Cross-source promotion')
    require(r['prior_battle_context']['existing_record_id'] == 'CN20-BATTLE-02' and r['prior_battle_context']['old_battle_html_or_image_reacquired_by_this_job'] is False, 'Prior-source acquisition promoted')
    require(len(r['records']) == 14 and len({x['record_id'] for x in r['records']}) == 14, 'One intro and thirteen skill rows required')
    evidence = [r['extracted']['intro']] + r['extracted']['rows']
    for i, (row, ev) in enumerate(zip(r['records'], evidence)):
        require(row['source_reported'] == ev and row['source_refs'] == ['S1'] and row['version_profile'] == PROFILE and row['game_ids'] is None, 'Record/source identity changed')
        require(row['collection'] == ('tutorials' if i == 0 else 'skills') and row['entity_type'] == ('HEALING_INTRO_CONTEXT' if i == 0 else 'DOCUMENTARY_SPELL_LEVEL_ROW'), 'Record collection changed')
        require(row['record_revision'] == 1 and row['verification_status'] == 'SOURCE_TABLE_OR_PROSE_NOT_ORIGINAL_RUNTIME' and row['rights_status'] == 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'Export attribution promoted')
    require(all(x is False for x in r['unproven'].values()), 'Unsupported conclusion promoted')
    require(r['status'] == {'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'} and r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-54', 'Stage/queue changed')


def replay(r, raws):
    validate(r); require(len(raws) == 2, 'Two HTML inputs required')
    x = extract(*raws); require(x == r['extracted'], 'Actual healing source changed')
    http = [{'bytes': len(b), 'sha256': sha(b)} for b in raws]
    require(http == [{'bytes': s['bytes'], 'sha256': s['sha256']} for s in r['sources']], 'Actual HTML byte pin changed')
    return {'schema': 'stoneage.cn20_healing_spells.derived_replay.r1', 'http': http, 'extracted': x, 'audit': audit(raws, x),
            'content_images_fetched': 0, 'raw_html_or_assets_in_output': False, 'original_game_executed': False}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--fetch', action='store_true', required=True); p.add_argument('--output', type=Path, required=True); a = p.parse_args()
    r = json.loads(REPORT.read_text())
    with ThreadPoolExecutor(max_workers=2) as pool:
        raws = list(pool.map(fetch, [NAV_URL, BODY_URL]))
    out = replay(r, raws); a.output.parent.mkdir(parents=True, exist_ok=True); a.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'success': True, 'html_bytes': [len(b) for b in raws], 'spell_level_rows': 13, 'source_mutations': 18, 'images': 0}))


if __name__ == '__main__':
    main()
