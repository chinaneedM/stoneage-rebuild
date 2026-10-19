"""Official CN2.0 source table transcription, without fitted XP/runtime rules."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from tools.stoneage_early_content_probe import plain, require
from tools.stoneage_wayi_newbie_riding_plan import fetch

ORIGINAL = 'http://www.waei.com.cn:80/ZHUANQU/stoneage2/tyro/upgrade.asp'
CAPTURE = '20011204165711'
URL = 'https://web.archive.org/web/' + CAPTURE + 'id_/' + ORIGINAL
SOURCE_SHA = '73fde66ffb3c92261d66715f873fa9b9f54166e4443d5d29924fe137cdcb8d35'
GRID_SHA = '72d9161343f1ec017fa6aedead769bdc28cc004215e7ae9d0ebe5bc2300caa45'
REPORT = Path('research/recovered/STONEAGE-WAEI-CN20-LEVEL-EXP-TABLE-R1.json')
INTRO = '以下是每个等级所需要的经验值列表：'
HEADERS = ['等级', '所需经验值'] * 3


def grid_digest(grid):
    return sha256(json.dumps(grid, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def extract_grid(doc):
    require(doc.count(INTRO) == 1, 'Exactly one actual experience-table introduction required')
    section = doc.split(INTRO, 1)[1].split('</table>', 1)[0]
    grid = [[plain(c) for c in re.findall(r'<td\b[^>]*>(.*?)</td>', row, re.I | re.S)]
            for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>', section, re.I | re.S)]
    require(len(grid) == 29 and grid[0] == HEADERS and all(len(row) == 6 for row in grid),
            'Exact repeated two-column headers and 28 six-cell data rows required')
    return grid


def observations(grid):
    result, blank = [], []
    for row_index, cells in enumerate(grid[1:], 1):
        for group in range(3):
            level, xp = cells[2*group:2*group+2]
            if not level and not xp:
                blank.append({'source_data_row': row_index, 'source_pair_group': group+1})
                continue
            require(re.fullmatch(r'[1-9][0-9]*', level) is not None and re.fullmatch(r'[0-9]+', xp) is not None,
                    'Unpaired, malformed or interpolated source numeric cells')
            result.append({'level_label_as_written': level, 'required_exp_as_written': xp,
                           'source_data_row': row_index, 'source_pair_group': group+1})
    require(sorted(int(r['level_label_as_written']) for r in result) == list(range(1,83)),
            'Exactly one observed source pair for each visible level 1 through 82 required')
    require(blank == [{'source_data_row': 27, 'source_pair_group': 3}, {'source_data_row': 28, 'source_pair_group': 3}],
            'Final two blank pairs must remain blanks, not inferred levels')
    return sorted(result, key=lambda r: int(r['level_label_as_written'])), blank


def validate_report(o):
    require(len(o['records']) == 1, 'One documentary table record, not 82 restored entities')
    r = o['records'][0]; data = r['source_table_observations']
    require(len(data) == 82 and [x['level_label_as_written'] for x in data] == [str(i) for i in range(1,83)],
            'Source levels reordered, duplicated, omitted or extrapolated')
    grid = [HEADERS] + [['']*6 for _ in range(28)]
    seen = set()
    for x in data:
        row, group = x['source_data_row'], x['source_pair_group']
        require(1 <= row <= 28 and 1 <= group <= 3 and (row,group) not in seen,
                'Source pair coordinates duplicated or outside actual table')
        seen.add((row,group)); grid[row][2*(group-1):2*group] = [x['level_label_as_written'], x['required_exp_as_written']]
    require(grid_digest(grid) == GRID_SHA, 'Original cell values or positions silently corrected or changed')
    require(o['table_shape']['blank_pairs'] == [{'source_data_row':27,'source_pair_group':3},
                                               {'source_data_row':28,'source_pair_group':3}], 'Blank source slots extrapolated')
    b = r['semantic_boundaries']
    require(b['incremental_versus_cumulative'] == 'UNSPECIFIED_BY_SOURCE_TABLE'
            and b['current_versus_destination_level'] == 'UNSPECIFIED_BY_SOURCE_TABLE'
            and b['player_versus_pet_applicability'] == 'UNSPECIFIED_BY_SOURCE_TABLE'
            and b['reincarnation_scaling_or_carryover'] is None,
            'Ambiguous XP semantics promoted to a runtime rule')
    require(b['formula_or_extrapolated_levels'] is None and b['last_visible_level_is_game_cap_proven'] is False
            and b['source_values_have_been_corrected_or_smoothed'] is False,
            'Visible table promoted to cap, fitted formula or smoothed progression')
    require(r['actual_server_rule_or_execution_verified'] is False
            and r['original_game_ids_or_same_build_binding'] is None,
            'Table promoted to original server execution')
    require(o['source']['page_title_as_written'] == '石器时代2.0'
            and o['source']['actual_capture'] == CAPTURE
            and o['boundaries']['cn25_jss1999_tw10_cn182_same_rule_proven'] is False
            and o['boundaries']['upgrade_path_is_software_download_target'] is False,
            'CN2.0 table misattributed to another build or software updater')


def build(body, final):
    require(final == URL, 'Exact original URL and actual capture required')
    require(len(body) == 75141 and sha256(body).hexdigest() == SOURCE_SHA, 'Known official source byte pin differs')
    doc = body.decode('gb18030', errors='strict')
    require(re.search(r'<title>\s*石器时代2\.0\s*</title>', doc, re.I) is not None, 'Actual official page title differs')
    newcomer = [(href, plain(label)) for href, label in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', doc, re.I | re.S)
                if plain(label) == '新入石器']
    require(newcomer == [('/ZHUANQU/stoneage2/sw/adventure.asp', '新入石器')], 'Real unread newcomer entry differs')
    grid = extract_grid(doc); require(grid_digest(grid) == GRID_SHA, 'Exact six-cell grid fingerprint differs')
    data, blank = observations(grid)
    r = {'record_id':'waei-cn20:2001-level-exp-table', 'collection':'tutorials',
         'entity_type':'OFFICIAL_DOCUMENTARY_LEVEL_EXPERIENCE_TABLE', 'record_revision':1,
         'version_profile':'CN_BEIJING_WAEI_PAGE_LABEL_2_0_CAPTURE_2001_NOT_EXACT_BUILD',
         'source_refs':[{'original_url':ORIGINAL,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,
                         'table_locator':'ONE_TABLE_AFTER_EXACT_INTRO','normalized_grid_sha256':GRID_SHA}],
         'verification_status':'SOURCE_TABLE_TRANSCRIPTION_NOT_ORIGINAL_SERVER_RULE',
         'rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
         'source_table_observations':data,
         'semantic_boundaries':{'incremental_versus_cumulative':'UNSPECIFIED_BY_SOURCE_TABLE',
                                'current_versus_destination_level':'UNSPECIFIED_BY_SOURCE_TABLE',
                                'player_versus_pet_applicability':'UNSPECIFIED_BY_SOURCE_TABLE',
                                'reincarnation_scaling_or_carryover':None, 'formula_or_extrapolated_levels':None,
                                'last_visible_level_is_game_cap_proven':False,
                                'source_values_have_been_corrected_or_smoothed':False},
         'actual_server_rule_or_execution_verified':False,'original_game_ids_or_same_build_binding':None}
    o = {'schema':'stoneage.waei_cn20.level_exp_table.r1','date':'2026-10-19',
         'task':'CN20-OFFICIAL-LEVEL-EXP-CONTENT-TABLE-01',
         'source':{'original_url':ORIGINAL,'strict_replay_url':URL,'actual_capture':CAPTURE,
                   'bytes':len(body),'sha256':SOURCE_SHA,'encoding':'GB18030_STRICT',
                   'page_title_as_written':'石器时代2.0','table_intro_as_written':INTRO,
                   'capture_is_release_or_unchanged_launch_body_proven':False,
                   'known_original_reacquired_not_new_webpage':True},
         'table_shape':{'header_as_written':HEADERS,'data_rows':28,'cells_per_row':6,
                        'pair_group_observation_counts':[28,28,26],'blank_pairs':blank,
                        'normalized_grid_sha256':GRID_SHA},
         'records':[r],
         'qualified_unread_entry':{'label':'新入石器',
                                   'original_url':'http://www.waei.com.cn:80/ZHUANQU/stoneage2/sw/adventure.asp',
                                   'body_or_images_read':False},
         'coverage':{'documentary_table_records':1,'observed_numeric_pairs':82,
                      'new_original_pages':0,'known_original_pages_reacquired':1,
                      'original_server_tables_or_new_game_entities_restored':0,
                      'images_binaries_or_other_pages_acquired':0},
         'boundaries':{'cn25_jss1999_tw10_cn182_same_rule_proven':False,
                        'upgrade_path_is_software_download_target':False,
                        'automatic_new_game_design_adoption':False,'raw_original_html_or_assets_in_git':False,
                        'stage_a':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
         'next':'CN20-OFFICIAL-NAMED-NEWCOMER-CONTENT-SOURCE-01'}
    validate_report(o);return o


def main():
    p=argparse.ArgumentParser();p.add_argument('--input');p.add_argument('--output',required=True);a=p.parse_args()
    body, final=(Path(a.input).read_bytes(),URL) if a.input else fetch(URL)
    o=build(body,final);payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('SOURCE_SHA256='+SOURCE_SHA);print('GRID_SHA256='+GRID_SHA)
    print('DOCUMENTARY_TABLES=1 OBSERVED_PAIRS=82 BLANK_PAIRS=2 SERVER_RULES=0')
    print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__=='__main__':main()
