"""Close two qualified web pages; preserve mixed captures and literal cell bindings."""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urljoin

from tools.stoneage_early_content_probe import plain, require
from tools.stoneage_wayi_newbie_riding_plan import fetch
from tools.stoneage_waei_cn20_new_pet_catalog import Images, grid_digest, validate_report as validate_parent

PARENT = Path('research/recovered/STONEAGE-WAEI-CN20-NEW-PET-CATALOG-FIRST-PAGE-R1.json')
PARENT_SHA = '9a460c23968a714717b375d823308bb5e56848116aaf44880091b75808024df6'
VISUAL = Path('research/recovered/STONEAGE-WAEI-CN20-AMIDUO-VISUAL-REFERENCE-R1.json')
VISUAL_SHA = '5ef2cfc5cd7f24229ece5f0fa01c924e932b40716af32417aa0bf4358eeb9cb0'
REPORT = Path('research/recovered/STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json')
BASE = 'http://www.waei.com.cn/ZHUANQU/stoneage2/pet/'
PAGES = [
    {'original_url': BASE+'new_pet1.asp', 'actual_capture': '20011023173210',
     'bytes': 66451, 'sha256': 'dfc191c476dc5c968e1957e58070297d048475e3f3f8d8d5e897ccae56ea0c65',
     'range_label_as_written': '41-80', 'first_ordinal': 41,
     'row_lengths': [5]*8, 'final_row_explicitly_closed': True,
     'grid_sha256': '4f194a8b3bec04b36a37f629751841509bfaa26bbfb9fccee1b230941f01d182'},
    {'original_url': BASE+'new_pet2.asp', 'actual_capture': '20011023181629',
     'bytes': 64382, 'sha256': '2c7aea8d0319c2070d5c7590a95bfc892c2463deb76c5b95fca8c281549c76f0',
     'range_label_as_written': '81-104', 'first_ordinal': 81,
     'row_lengths': [5,5,5,5,4], 'final_row_explicitly_closed': False,
     'grid_sha256': 'a52bc5cf3b5b8660b29bbcfd5162463d69c986e546733026e55bbe8b97e72818'},
]
for page in PAGES:
    page['strict_replay_url'] = 'https://web.archive.org/web/'+page['actual_capture']+'id_/'+page['original_url']


def parse_page(doc, page_index):
    page = PAGES[page_index]
    require(re.search(r'<title>\s*石器时代2\.0\s*</title>', doc, re.I) is not None,
            'Actual page title differs')
    require(doc.count('新 增 宠 物') == 1, 'One actual article heading required')
    section = doc.split('新 增 宠 物', 1)[1].split('<span class="p12b">', 1)[0]
    tables = re.findall(r'<table\b[^>]*>(.*?)</table>', section, re.I|re.S)
    require(len(tables) == 2, 'Exactly one navigation and one catalog grid required')
    require(plain(tables[0]) == '1-40 41-80 81-104', 'Actual range navigation differs')
    nav = [(plain(label), href) for href, label in re.findall(
        r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', tables[0], re.I|re.S)]
    expected_nav = [[('1-40','new_pet.asp'),('81-104','new_pet2.asp')],
                    [('1-40','new_pet.asp'),('41-80','new_pet1.asp')]][page_index]
    require(nav == expected_nav, 'Actual page links differ')
    # The source's last row on 81-104 ends at </table> without </tr>.
    # Split at opening rows so those four real cells are not silently discarded.
    chunks = re.split(r'<tr\b[^>]*>', tables[1], flags=re.I)
    require(not plain(chunks[0]), 'Unexpected content before first grid row')
    grid = []
    closures = []
    for chunk in chunks[1:]:
        closures.append(bool(re.search(r'</tr>', chunk, re.I)))
        row = []
        cells = re.findall(r'<td\b[^>]*>(.*?)</td>', chunk, re.I|re.S)
        require(len(cells) == len(re.findall(r'<td\b', chunk, re.I)), 'Unclosed source cell')
        for cell in cells:
            parser = Images(); parser.feed(cell)
            require(len(parser.images) == 1 and bool(plain(cell)), 'One actual name/image binding per cell required')
            attrs = parser.images[0]
            require('src' in attrs and ('width' in attrs) == ('height' in attrs), 'Incomplete image reference')
            dims = [int(attrs['width']), int(attrs['height'])] if 'width' in attrs else None
            row.append([plain(cell), attrs['src'], dims])
        grid.append(row)
    require([len(row) for row in grid] == page['row_lengths'], 'Real source row lengths differ; no empty or invented cell')
    require(closures == [True]*(len(grid)-1)+[page['final_row_explicitly_closed']], 'Source row closure differs')
    require(grid_digest(grid) == page['grid_sha256'], 'Literal labels, src case, cell association or declared dimensions changed')
    return grid


def pinned_metadata(parent_bytes, visual_bytes):
    require(sha256(parent_bytes).hexdigest() == PARENT_SHA, 'Immutable first-page Git metadata differs')
    require(sha256(visual_bytes).hexdigest() == VISUAL_SHA, 'Known one-image supplement differs')
    parent = json.loads(parent_bytes); validate_parent(parent)
    visual = json.loads(visual_bytes)
    require(visual['records'][0]['existing_catalog_record_id'] == parent['records'][6]['record_id'],
            'Known visual must retain its existing position binding')
    return parent


def validate_report(o, parent_bytes=None, visual_bytes=None):
    parent = pinned_metadata(PARENT.read_bytes() if parent_bytes is None else parent_bytes,
                             VISUAL.read_bytes() if visual_bytes is None else visual_bytes)
    require(o['immutable_first_page'] == {'path':str(PARENT),'sha256':PARENT_SHA,'records_copied_without_change':40},
            'Immutable parent custody differs')
    records = o['records']
    require(len(records) == 104 and records[:40] == parent['records'], '104 actual web positions and unchanged first 40 required')
    require(o['new_page_sources'] == PAGES, 'Source-specific actual captures/pins/row closures must remain separate')
    for index, page in enumerate(PAGES):
        start = page['first_ordinal']-1
        count = sum(page['row_lengths'])
        grid = [[] for _ in page['row_lengths']]
        for offset, r in enumerate(records[start:start+count]):
            ordinal = start+offset+1; row = offset//5+1; col = offset%5+1
            require(r['source_position'] == {'ordinal': ordinal,'row': row,'column': col}
                    and r['record_id'] == f'waei-cn20:new-pet-web-position:{ordinal:03d}', 'Web ordinal/local row/column or ID differs')
            require(r['source_refs'] == [{'original_url':page['original_url'], 'actual_capture':page['actual_capture'],
                     'sha256':page['sha256'], 'source_grid_sha256':page['grid_sha256'],'row':row,'column':col}],
                    'Cell provenance detached from actual page capture')
            im = r['image_reference']
            grid[row-1].append([r['display_label_as_written'],im['relative_src_as_written'],im['html_declared_dimensions']])
            require(r['name_as_written'] == r['display_label_as_written'] and r['label_status'] == 'NAMED_ON_WEB_PAGE',
                    'New page names must remain literal')
            require(im['original_url'] == urljoin(page['original_url'], im['relative_src_as_written'])
                    and im['pixels_requested'] is False and all(im[k] is None for k in
                    ['actual_capture','sha256','actual_dimensions','actual_format_or_frames']), 'Unrequested pixels promoted to acquired metadata')
            require(all(r[k] is None for k in ['original_game_pet_id','stats_growth_capture_skill_or_riding_rules',
                                              'cross_region_or_build_entity_identity']), 'Web position promoted to game entity or gameplay')
            require(all(r[k] == parent['records'][6][k] for k in ['collection','entity_type','record_revision',
                    'version_profile','verification_status','rights_status']), 'Required research record boundary differs')
        require(grid_digest(grid) == page['grid_sha256'], 'Exact source grid bindings differ')
    require(o['coverage'] == {'finite_web_positions':104, 'named_labels':98, 'unresolved_placeholders':6,
                'new_named_positions':64,'new_original_bodies':2,'new_image_requests':0,
                'previously_acquired_image_supplements':1,'image_references_without_acquired_pixels':103,
                'remaining_qualified_pagination_bodies':0,'full_original_game_species_census_proven':False}, 'Finite coverage accounting differs')
    require(o['known_visual_supplement'] == {'path':str(VISUAL),'sha256':VISUAL_SHA,
                'existing_record_id':'waei-cn20:new-pet-web-position:007','newly_reacquired':False,
                'parent_historical_image_state_rewritten':False}, 'Prior visual custody or historical state altered')
    require(o['source_compilation']['same_capture_day_or_exact_build_proven'] is False
            and o['source_compilation']['first_page_actual_capture'] == '20011204194619'
            and o['source_compilation']['pagination_actual_captures'] == [p['actual_capture'] for p in PAGES],
            'October/December captures flattened into same build or patch sequence')
    require(o['source_compilation']['capture_order_is_release_or_patch_order'] is False
            and o['boundaries'] == {'original_html_images_programs_in_git':False,'new_game_asset_reuse_approved':False,
                '104_newly_added_species_or_exact_build_proven':False,'stage_a':'7_PARTIAL_2_OPEN',
                'stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'}, 'Research scope or capture chronology promoted')
    require(o['finite_outcome'] == 'CLOSED_QUALIFIED_THREE_PAGE_WEB_CATALOG_NOT_GAME_ROSTER'
            and o['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-15', 'Finite stop/whole-project return differs')


def build(parent_bytes, visual_bytes, bodies_and_urls):
    parent = pinned_metadata(parent_bytes, visual_bytes)
    require(len(bodies_and_urls) == 2, 'Only the two qualified pagination bodies required')
    records = deepcopy(parent['records'])
    for index, (body, final) in enumerate(bodies_and_urls):
        page = PAGES[index]
        require(final == page['strict_replay_url'], 'Exact actual final URL/capture required')
        require(len(body) == page['bytes'] and sha256(body).hexdigest() == page['sha256'], 'Exact source byte pin differs')
        grid = parse_page(body.decode('gb18030', errors='strict'), index)
        for row, cells in enumerate(grid, 1):
            for col, (label, src, dims) in enumerate(cells, 1):
                ordinal = page['first_ordinal']+(row-1)*5+col-1
                r = deepcopy(parent['records'][6])
                r.update(record_id=f'waei-cn20:new-pet-web-position:{ordinal:03d}',
                         source_position={'ordinal':ordinal,'row':row,'column':col},
                         display_label_as_written=label,name_as_written=label,label_status='NAMED_ON_WEB_PAGE',
                         source_refs=[{'original_url':page['original_url'],'actual_capture':page['actual_capture'],
                                       'sha256':page['sha256'],'source_grid_sha256':page['grid_sha256'],'row':row,'column':col}])
                r['image_reference'].update(relative_src_as_written=src,original_url=urljoin(page['original_url'],src),
                                            html_declared_dimensions=dims)
                records.append(r)
    o = {'schema':'stoneage.waei_cn20.new_pet_finite_catalog.r1','date':'2026-10-19',
         'task':'CN20-NEW-PET-CATALOG-FINITE-PAGINATION-01',
         'immutable_first_page':{'path':str(PARENT),'sha256':PARENT_SHA,'records_copied_without_change':40},
         'new_page_sources':deepcopy(PAGES),'records':records,
         'source_compilation':{'first_page_actual_capture':'20011204194619',
                               'pagination_actual_captures':[p['actual_capture'] for p in PAGES],
                               'same_capture_day_or_exact_build_proven':False,
                               'capture_order_is_release_or_patch_order':False},
         'known_visual_supplement':{'path':str(VISUAL),'sha256':VISUAL_SHA,
                                    'existing_record_id':'waei-cn20:new-pet-web-position:007',
                                    'newly_reacquired':False,'parent_historical_image_state_rewritten':False},
         'coverage':{'finite_web_positions':104,'named_labels':98,'unresolved_placeholders':6,
                     'new_named_positions':64,'new_original_bodies':2,'new_image_requests':0,
                     'previously_acquired_image_supplements':1,'image_references_without_acquired_pixels':103,
                     'remaining_qualified_pagination_bodies':0,'full_original_game_species_census_proven':False},
         'acquisition':{'initial_requested_capture':'20011204194619',
                        'reader_open_initially_unavailable':True,
                        'direct_http_actual_october_captures_acquired':True,
                        'independent_runner_repeats_initial_reader_failure':False,
                        'other_links_images_clients_or_programs_requested':False},
         'finite_outcome':'CLOSED_QUALIFIED_THREE_PAGE_WEB_CATALOG_NOT_GAME_ROSTER',
         'boundaries':{'original_html_images_programs_in_git':False,'new_game_asset_reuse_approved':False,
                       '104_newly_added_species_or_exact_build_proven':False,
                       'stage_a':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
         'next':'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-15'}
    validate_report(o, parent_bytes, visual_bytes)
    return o


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-page1'); parser.add_argument('--input-page2'); parser.add_argument('--output',required=True)
    args = parser.parse_args()
    require(bool(args.input_page1) == bool(args.input_page2), 'Both local originals or neither required')
    sources = [(Path(path).read_bytes(), page['strict_replay_url']) if path else fetch(page['strict_replay_url'])
               for path, page in zip([args.input_page1,args.input_page2],PAGES)]
    o = build(PARENT.read_bytes(), VISUAL.read_bytes(), sources)
    payload = json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2)+'\n'
    out = Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(payload,encoding='utf-8')
    for page in PAGES:
        print('SOURCE_SHA256='+page['sha256']+' GRID_SHA256='+page['grid_sha256'])
    print('WEB_POSITIONS=104 NAMED=98 PLACEHOLDERS=6 NEW_IMAGES=0 NEW_ORIGINAL_BODIES=2')
    print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__ == '__main__':
    main()
