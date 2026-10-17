"""Bounded logging-quest content qualification, never original-server execution."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request
try:
    from tools.stoneage_early_content_probe import plain, require
    from tools.stoneage_adult_ceremony_probe import between, normalize, same_task_block, contains, news_header
except ModuleNotFoundError:
    from stoneage_early_content_probe import plain, require
    from stoneage_adult_ceremony_probe import between, normalize, same_task_block, contains, news_header

SOURCES = {
    "compilation": ("https://games.sina.com.cn/handbook/0101/01186091.shtml", "gb18030"),
    "later_logging": ("https://games.sina.com.cn/zhqu/sta/article/2003-05-20/7612.shtml", "gb18030"),
    "levelguide": ("https://news.17173.com/z/stoneage/content/2001-6-14/n654_570366.html", "utf-8"),
    "archived_compilation": ("https://web.archive.org/web/20040822040357id_/http://games.sina.com.cn:80/handbook/0101/01186091.shtml", "gb18030"),
    "archived_later": ("https://web.archive.org/web/20031205132111id_/http://games.sina.com.cn:80/zhqu/sta/article/2003-05-20/7612.shtml", "gb18030"),
    "archived_index": ("https://web.archive.org/web/20040218115426id_/http://games.sina.com.cn:80/zhqu/sta/rwgl.shtml", "gb18030"),
}
CAPTURES = {"archived_compilation": "20040822040357", "archived_later": "20031205132111", "archived_index": "20040218115426"}


def derive(documents):
    docs = {k: plain(v) for k, v in documents.items()}
    blocks = {k: between(docs[k], "先到乌鲁力村", "小猪的爱情故事") for k in ("compilation", "archived_compilation")}
    blocks.update({k: between(docs[k], "任务条件 无", "图片20 图片21") for k in ("later_logging", "archived_later")})
    blocks['levelguide'] = between(docs['levelguide'], "另外lv30~35还有一件重要的事", "lv35~40")
    blocks['archived_index'] = between(docs['archived_index'], "石器时代1.82", "转生任务")
    same_task_block(blocks['compilation'], blocks['archived_compilation'], '20040822 compilation')
    same_task_block(blocks['later_logging'], blocks['archived_later'], '20031205 detailed guide')
    early, later = blocks['compilation'], blocks['later_logging']
    contains(early, "最后攻击的人", "最后攻击的是宠物的话，是会得不到木的", "收回你的伐木许可证", "14根木的话约有5000元", "只留下一张伐木许可证", "这把断斧千万不要放在地上，会毁灭不见", "哈恩改造斧 攻+33 防-10 敏-10")
    contains(docs['compilation'], '松鼠1206')
    contains(later, "任务等级 无限制 建议等级 >20", "声望 2", "攻+35防-15敏-15", "14根木的话约有5000S", "攻+8防+5敏-5魅-5", "收回你的伐木许可证", "本任务可以重复做", "喜欢八卦的年轻人", "巴尔的斧头又坏了")
    for key in ('later_logging', 'archived_later'):
        contains(docs[key][:docs[key].find('任务条件 无')], '2003-05-20 13:14')
    contains(blocks['levelguide'], "5000左右", "衫之手环攻+8防+5敏-5魅+5")
    news_header(documents['levelguide'], '未知')
    raw_bucket = between(documents['archived_index'], '石器时代1.82', '转生任务')
    contains(raw_bucket, '/zhqu/sta/article/2003-05-20/7612.shtml', '伐木任务')
    return {
        'profiles': {
            'compilation': {'flow': ['AXE_REQUEST', 'WATER_ERRAND', 'HAND_IN_NEW_AXE', 'INTRODUCTION_AND_BROKEN_AXE', 'PERMIT', 'PLAYER_LAST_HIT_WOOD', 'WOOD_BUYBACK_AND_PERMIT_RETURN'],
                            'player_last_hit_gets_wood': True, 'pet_last_hit_gets_wood': False,
                            'guide_bag_example': {'permit_slots': 1, 'free_slots': 14, 'original_inventory_capacity_proven': False},
                            'payout_example': {'wood_count': 14, 'approximate_stone': 5000, 'exact_unit_price': None},
                            'permit_returned_to_merchant_on_buyback': True, 'bracelet_charm_delta': None,
                            'broken_axe_disappears_on_drop': True, 'repaired_broken_axe_stats': {'attack': 33, 'defense': -10, 'agility': -10},
                            'repeatability': None, 'completion_event_id': None},
            'later_logging': {'reported_level_limit': 'NONE', 'suggested_level_greater_than': 20, 'suggestion_is_admission_gate': False,
                              'reported_reputation_header': 2, 'reputation_is_bracelet_charm': False,
                              'new_errand_axe_stats': {'attack': 35, 'defense': -15, 'agility': -15},
                              'bracelet_stats': {'attack': 8, 'defense': 5, 'agility': -5, 'charm': -5},
                              'permit_returned_to_merchant_on_buyback': True, 'payout_example': {'wood_count': 14, 'approximate_stone': 5000, 'exact_unit_price': None},
                              'repeat_reported': True, 'repeat_trigger': 'TALK_TO_GOSSIP_YOUTH_AFTER_COMPLETION_BEFORE_NEW_AXE_REQUEST',
                              'player_or_pet_last_hit_rule_explicit_here': False},
            'levelguide': {'bracelet_stats': {'attack': 8, 'defense': 5, 'agility': -5, 'charm': 5}, 'approximate_stone': 5000,
                           'author': 'UNKNOWN', 'source_asserted_date': '2001-06-14', 'historical_bytes_authenticated_in_2001': False},
        },
        'temporal_witnesses': CAPTURES,
        'index_attribution': {'editorial_bucket': 'STONEAGE_1_82', 'source': 'archived_index', 'link_to_selected_detailed_guide': True,
                              'original_1_82_server_build_authenticated': False, 'taiwan_1_0_or_jss_1999_attribution': 'OPEN'},
        'conflicts': [{'field': 'bracelet.charm', 'levelguide': 5, 'later_logging': -5, 'resolution': 'KEEP_SOURCE_PROFILES_NO_DEFAULT'}],
        'distinctions': {'new_errand_axe_and_repaired_broken_axe_stats_are_different_stages': True,
                         'per_kill_permit_consumption_proven': False,
                         'approximate_total_is_not_exact_unit_price': True, 'later_repeat_route_not_backdated_into_compilation': True},
        'lineage': {'archive_is_independent_rule_author': False, 'independent_origins_authenticated': False,
                    'shared_buyback_wording_is_not_independent_corroboration': True, '17173_task_reprint_not_counted': True},
        'selected_block_sha256': {k: hashlib.sha256(normalize(v).encode()).hexdigest() for k, v in blocks.items()},
        'unknown': {'original_item_ids': None, 'original_npc_ids': None, 'original_event_id': None, 'exact_build_region': None,
                    'battle_reward_dispatch_code': None, 'durable_completion_and_repeat_reset': None, 'exact_unit_price': None},
    }


def report(acquisitions):
    require(set(acquisitions) == set(SOURCES), 'incomplete six-source acquisition')
    docs, metadata = {}, {}
    for key, (body, final_url) in acquisitions.items():
        url, encoding = SOURCES[key]
        require(final_url == url, f'redirect needs requalification: {key}')
        require(body and len(body) <= 2_000_000, f'source size {key}')
        docs[key] = body.decode(encoding, errors='replace')
        metadata[key] = {'url': url, 'final_url': final_url, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                         'decoding': encoding, 'replacement_characters': docs[key].count('\ufffd')}
    return {'schema': 'stoneage.logging.source_contract.r1', 'sources': metadata, 'observations': derive(docs),
            'compilation_authenticated_in_2001': False, 'earliest_capture_exhaustively_established': False,
            'original_server_executed': False, 'original_quest_script_recovered': False,
            'early_exact_build_membership': 'OPEN', 'stage_a_accepted': False, 'stage_b_gate': 'GATED'}


def fetch(key):
    url, _ = SOURCES[key]
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'StoneAge historical evidence research'}), timeout=40) as response:
        require(response.status == 200, f'HTTP {key}')
        return key, (response.read(2_000_001), response.url)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline-dir', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.offline_dir:
        acquisitions = {k: ((args.offline_dir / (k + '.raw')).read_bytes(), url) for k, (url, _) in SOURCES.items()}
    else:
        with ThreadPoolExecutor(max_workers=4) as pool:
            acquisitions = dict(pool.map(fetch, SOURCES))
    result = report(acquisitions)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'sources': 6, 'actual_archive_captures': 3, 'original_server_executed': False}))


if __name__ == '__main__':
    main()
