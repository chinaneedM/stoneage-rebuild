"""One official new-pet web catalog page; positions and labels, not game IDs."""
import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from tools.stoneage_early_content_probe import plain, require
from tools.stoneage_wayi_newbie_riding_plan import fetch
from tools.stoneage_waei_cn20_newcomer_guide import URL as ENTRY_URL, SOURCE_SHA as ENTRY_SHA, ORIGINAL as ENTRY_ORIGINAL

ORIGINAL='http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet.asp'
CAPTURE='20011204194619'
URL='https://web.archive.org/web/'+CAPTURE+'id_/'+ORIGINAL
SOURCE_SHA='561950fd7bba41e7d39f4a781a671e11e175c7fe08dd1b5481fdf1fd23ba351b'
GRID_SHA='99b6274ac6ed8b03755fa940c1172371ea6a037f1c40a0cba63f4410e9fbfa67'
REPORT=Path('research/recovered/STONEAGE-WAEI-CN20-NEW-PET-CATALOG-FIRST-PAGE-R1.json')


class Images(HTMLParser):
    def __init__(self):super().__init__();self.images=[]
    def handle_starttag(self,tag,attrs):
        if tag=='img':self.images.append(dict(attrs))


def grid_digest(grid):
    return sha256(json.dumps(grid,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def parse_catalog(doc):
    require(doc.count('新 增 宠 物')==1,'One actual new-pet article heading required')
    section=doc.split('新 增 宠 物',1)[1].split('<span class="p12b">',1)[0]
    tables=re.findall(r'<table\b[^>]*>(.*?)</table>',section,re.I|re.S)
    require(len(tables)==2,'One navigation table and one actual catalog grid required')
    require(plain(tables[0])=='1-40 41-80 81-104','Actual first-page range labels differ')
    nav=[(plain(label),href) for href,label in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>',tables[0],re.I|re.S)]
    require(nav==[('41-80','new_pet1.asp'),('81-104','new_pet2.asp')],'Actual unread pagination links differ')
    grid=[]
    for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>',tables[1],re.I|re.S):
        row=[]
        for td in re.findall(r'<td\b[^>]*>(.*?)</td>',tr,re.I|re.S):
            p=Images();p.feed(td);require(len(p.images)==1,'Each source cell must bind exactly one label to one image')
            a=p.images[0];require(bool(plain(td)) and 'src' in a,'Actual cell label and image src required')
            require(('width' in a)==('height' in a),'Partial declared dimensions cannot be completed by inference')
            dims=[int(a['width']),int(a['height'])] if 'width' in a else None
            row.append([plain(td),a['src'],dims])
        require(len(row)==5,'Exactly five source positions per row required');grid.append(row)
    require(len(grid)==8,'Exactly eight actual catalog rows required')
    return grid,nav


def validate_report(o):
    records=o['records'];require(len(records)==40,'Forty source positions required')
    require([r['source_position']['ordinal'] for r in records]==list(range(1,41))
            and len({r['record_id'] for r in records})==40,'Web positions duplicated, omitted or promoted to game IDs')
    grid=[[] for _ in range(8)]
    for i,r in enumerate(records):
        p=r['source_position'];im=r['image_reference']
        require(p=={'ordinal':i+1,'row':i//5+1,'column':i%5+1},'Exact source row and column differ')
        grid[i//5].append([r['display_label_as_written'],im['relative_src_as_written'],im['html_declared_dimensions']])
        placeholder=re.fullmatch(r'\?+\d*',r['display_label_as_written']) is not None
        require(r['label_status']==('UNRESOLVED_PLACEHOLDER' if placeholder else 'NAMED_ON_WEB_PAGE')
                and r['name_as_written']==(None if placeholder else r['display_label_as_written']),
                'Placeholder silently named, transliterated or deduplicated')
        require(r['original_game_pet_id'] is None and r['stats_growth_capture_skill_or_riding_rules'] is None
                and r['cross_region_or_build_entity_identity'] is None,'Web catalog promoted to game identity or gameplay data')
        require(im['original_url']==urljoin(ORIGINAL,im['relative_src_as_written']) and im['pixels_requested'] is False
                and im['actual_capture'] is None and im['sha256'] is None and im['actual_dimensions'] is None
                and im['actual_format_or_frames'] is None,'Image reference promoted to acquired pixels, format or animation')
    require(grid_digest(grid)==GRID_SHA,'Source labels, cell associations, filename case or declared dimensions changed')
    require(sum(r['label_status']=='NAMED_ON_WEB_PAGE' for r in records)==34,'Exactly 34 named and six unresolved source labels required')
    require(o['coverage']['full_original_species_census_or_104_newly_added_pets_proven'] is False
            and o['source']['page_label_authenticates_exact_build_or_addition_date'] is False,
            'Page title or range labels promoted to full original roster or dated additions')
    require(all(not x['body_or_images_read'] for x in o['qualified_unread_pagination']), 'Unread pagination promoted to recovered bodies')


def build(entry,entry_final,body,final):
    require(entry_final==ENTRY_URL and final==URL,'Exact actual entry/catalog replay identities required')
    require(len(entry)==65653 and sha256(entry).hexdigest()==ENTRY_SHA,'Known actual entry body differs')
    require(len(body)==69317 and sha256(body).hexdigest()==SOURCE_SHA,'New-pet catalog body differs')
    ed=entry.decode('gb18030',errors='strict')
    links=[(href,plain(label)) for href,label in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',ed,re.I|re.S)
           if plain(label)=='新增宠物']
    require(links==[('/ZHUANQU/stoneage2/pet/new_pet.asp','新增宠物')],'Authentic entry label and original href differ')
    doc=body.decode('gb18030',errors='strict')
    require(re.search(r'<title>\s*石器时代2\.0\s*</title>',doc,re.I) is not None,'Actual page title differs')
    grid,nav=parse_catalog(doc);require(grid_digest(grid)==GRID_SHA,'Exact source grid fingerprint differs')
    records=[]
    for row,cells in enumerate(grid,1):
        for col,(label,src,dims) in enumerate(cells,1):
            ordinal=(row-1)*5+col;placeholder=re.fullmatch(r'\?+\d*',label) is not None
            records.append({'record_id':f'waei-cn20:new-pet-web-position:{ordinal:03d}','collection':'pets',
                            'entity_type':'OFFICIAL_WEB_CATALOG_POSITION_NOT_CLIENT_SPECIES_ID','record_revision':1,
                            'version_profile':'CN_BEIJING_WAEI_PAGE_LABEL_2_0_CAPTURE_2001_NOT_EXACT_BUILD',
                            'source_refs':[{'original_url':ORIGINAL,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,
                                            'source_grid_sha256':GRID_SHA,'row':row,'column':col}],
                            'verification_status':'WEB_NAME_AND_IMAGE_REFERENCE_ONLY_NOT_CLIENT_OR_SERVER_ENTITY',
                            'rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
                            'source_position':{'ordinal':ordinal,'row':row,'column':col},
                            'display_label_as_written':label,'name_as_written':None if placeholder else label,
                            'label_status':'UNRESOLVED_PLACEHOLDER' if placeholder else 'NAMED_ON_WEB_PAGE',
                            'image_reference':{'relative_src_as_written':src,'original_url':urljoin(ORIGINAL,src),
                                               'html_declared_dimensions':dims,'pixels_requested':False,
                                               'actual_capture':None,'sha256':None,'actual_dimensions':None,'actual_format_or_frames':None},
                            'original_game_pet_id':None,'stats_growth_capture_skill_or_riding_rules':None,
                            'cross_region_or_build_entity_identity':None})
    o={'schema':'stoneage.waei_cn20.new_pet_catalog_first_page.r1','date':'2026-10-19',
       'task':'CN20-OFFICIAL-NEW-PET-NAMED-CATALOG-SOURCE-01',
       'source':{'original_url':ORIGINAL,'strict_replay_url':URL,'actual_capture':CAPTURE,'bytes':len(body),
                 'sha256':SOURCE_SHA,'encoding':'GB18030_STRICT','page_title_as_written':'石器时代2.0',
                 'article_heading_as_written':'新 增 宠 物','visible_page_range_as_written':'1-40',
                 'page_label_authenticates_exact_build_or_addition_date':False},
       'entry_source':{'original_url':ENTRY_ORIGINAL,'strict_replay_url':ENTRY_URL,'actual_capture':'20011204212409',
                       'bytes':len(entry),'sha256':ENTRY_SHA,'label':'新增宠物','actual_href':'/ZHUANQU/stoneage2/pet/new_pet.asp',
                       'known_entry_reacquired_not_new_source':True},
       'source_grid':{'rows':8,'columns':5,'sha256':GRID_SHA},'records':records,
       'qualified_unread_pagination':[{'range_label_as_written':label,'original_url':urljoin(ORIGINAL,href),
                                      'body_or_images_read':False} for label,href in nav],
       'coverage':{'web_positions':40,'named_labels':34,'unresolved_placeholder_labels':6,
                    'unacquired_image_references':40,'new_original_bodies':1,'known_entry_reacquired':1,
                    'full_original_species_census_or_104_newly_added_pets_proven':False},
       'boundaries':{'image_filename_or_web_ordinal_is_client_pet_id':False,'new_game_asset_reuse_approved':False,
                      'original_html_images_or_programs_in_git':False,'jss1999_tw10_cn182_or_25_build_equivalence':False,
                      'stage_a':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
       'next':'CN20-NEW-PET-NAMED-VISUAL-REFERENCE-01'}
    validate_report(o);return o


def main():
    p=argparse.ArgumentParser();p.add_argument('--input-entry');p.add_argument('--input-body');p.add_argument('--output',required=True);a=p.parse_args()
    require(bool(a.input_entry)==bool(a.input_body),'Both local originals or neither required')
    entry,entry_final=(Path(a.input_entry).read_bytes(),ENTRY_URL) if a.input_entry else fetch(ENTRY_URL)
    body,final=(Path(a.input_body).read_bytes(),URL) if a.input_body else fetch(URL)
    o=build(entry,entry_final,body,final);payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('ENTRY_SHA256='+ENTRY_SHA);print('SOURCE_SHA256='+SOURCE_SHA);print('GRID_SHA256='+GRID_SHA)
    print('POSITIONS=40 NAMED_LABELS=34 UNRESOLVED_LABELS=6 ACTUAL_PIXELS=0')
    print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__=='__main__':main()
