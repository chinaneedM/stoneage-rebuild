"""Four historical map files joined to qualified resource metadata, never map grids."""
import argparse
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import struct
from tools.stoneage_logical_alias_catalog import ROOT,DEST,load_catalog

TARGETS={1000:('11a6e898df8ed42a4f6efbf2bce090d13be4229d5d62277e4d593bd852eac1e3',160,160),
 2000:('d01c4194ac7e451ecbd8759aa2cf68a86eedfcfc02a4411d233696a7f063ee54',150,150),
 3000:('bca29e73c828e65d17fa95e1cd7bc90b25b2bd59c16060020a74d0ad5405f890',150,150),
 4000:('675c9ee9310ebced3c508f84dbd34a14115f5ef08d672fd5aed2bbb472c45ef9',150,150)}
SOURCE='https://web.archive.org/web/20030623234451id_/http://www.wuxitianlong.com:80/sa/map.exe'
SOURCE_SHA='372426e46765a1cf479041bdafc1d3e58fb019117d00d0b43d6a5f796620776e'
PROFILES=('TW10','CN50','PATCH129')

def need(ok,message):
    if not ok:raise ValueError(message)

def fingerprint(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
        'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

def parse(raw):
    need(len(raw)>=8,'short header');w,h=struct.unpack_from('<II',raw);n=w*h
    need(w>0 and h>0 and n<=1000000 and len(raw)==8+6*n,'exact three-plane layout required')
    planes=[]
    for i in range(3):
        b=raw[8+2*n*i:8+2*n*(i+1)];counts=Counter(v[0] for v in struct.iter_unpack('<H',b))
        planes.append({'ordinal':i+1,'sha256':hashlib.sha256(b).hexdigest(),
            'histogram':[[k,v] for k,v in sorted(counts.items())]})
    return {'width':w,'height':h,'cells':n,'planes':planes}

def resource_index(refs,blocks):
    indexed=defaultdict(list)
    for r in refs:
        c=blocks[r['content_id']]
        indexed[(r['profile'],r['logical_alias'])].append({
            'source_index':r['source_index'],'physical_bitmapno':r['physical_bitmapno'],
            'content_sha256':c['rd_sha256'],'content_bytes':c['bytes'],
            'width':r['width'],'height':r['height'],'attr_sha256':r['attr_sha256']})
    return indexed

def join_histogram(histogram,profile,index):
    rows=[]
    for alias,cells in histogram:
        # Zero is retained explicitly and never looked up as an implicit default graphic.
        refs=index.get((profile,alias),[]) if alias else []
        rows.append({'map_value':alias,'cells':cells,'zero_value':alias==0,
            'candidates':refs,'candidate_count':len(refs),
            'distinct_content_count':len({r['content_sha256'] for r in refs})})
    return {'rows':rows,'nonzero_cells':sum(r['cells'] for r in rows if not r['zero_value']),
        'unresolved_values':[r['map_value'] for r in rows if not r['zero_value'] and not r['candidates']],
        'unresolved_cells':sum(r['cells'] for r in rows if not r['zero_value'] and not r['candidates']),
        'multiple_occurrence_values':[r['map_value'] for r in rows if r['candidate_count']>1],
        'multiple_content_values':[r['map_value'] for r in rows if r['distinct_content_count']>1]}

def build(directory):
    catalog,refs,content=load_catalog(ROOT/DEST);idx=resource_index(refs,{c['content_id']:c for c in content})
    pins={p:fingerprint((ROOT/p).read_bytes()) for p in [str(DEST/'REPORT-R1.json'),str(DEST/'REFERENCES-R1.tsv.gz'),
        str(DEST/'CONTENTS-R1.tsv.gz'),'research/recovered/STONEAGE-HISTORICAL-MAPEXE-INVENTORY-R1.txt']}
    maps=[]
    for floor,(expected,w,h) in TARGETS.items():
        matches=[p for p in directory.iterdir() if p.name.casefold()==f'{floor}.dat'];need(len(matches)==1,'one exact map path required')
        raw=matches[0].read_bytes();need(hashlib.sha256(raw).hexdigest()==expected,'map source identity')
        d=parse(raw);need((d['width'],d['height'])==(w,h),'map dimensions')
        entry={'floor_token':floor,'name':None,'source_path':'map/'+matches[0].name,**fingerprint(raw),**d}
        for p in entry['planes'][:2]:p['resource_value_comparisons']={profile:join_histogram(p['histogram'],profile,idx) for profile in PROFILES}
        entry['planes'][2]['role']='ORDINAL_THIRD_PLANE_NOT_GRAPHIC_ALIAS_NOT_ENTITY_ID'
        maps.append(entry)
    return {'schema':'stoneage.map_resource_content_r21.v1','source_url':SOURCE,'source_bytes':4223728,
        'source_sha256':SOURCE_SHA,'source_scope':'2003_ARCHIVED_THIRD_PARTY_MAP_PACKAGE_NOT_AUTHENTICATED_OFFICIAL_BUILD',
        'source_pins':pins,'catalog_profile_scopes':catalog['profiles'],'comparison_namespace':'NUMERIC_MAP_VALUE_TO_LOGICAL_ALIAS_CANDIDATES',
        'maps':maps,'original_client_executed':False,'proprietary_grid_or_pixels_published':False,
        'same_build_render_selection_proven':False,'map_names_or_npcs_inferred':False,
        'new_authenticated_named_entities':0,'overall_restoration_percent':None}

def replay(report):
    need(report['schema']=='stoneage.map_resource_content_r21.v1','schema')
    need(report['source_sha256']==SOURCE_SHA and report['source_bytes']==4223728 and report['source_url']==SOURCE,'source carrier')
    need(report['source_scope']=='2003_ARCHIVED_THIRD_PARTY_MAP_PACKAGE_NOT_AUTHENTICATED_OFFICIAL_BUILD','source promotion')
    need(report['comparison_namespace']=='NUMERIC_MAP_VALUE_TO_LOGICAL_ALIAS_CANDIDATES','wrong identifier namespace')
    for k in ('original_client_executed','proprietary_grid_or_pixels_published','same_build_render_selection_proven','map_names_or_npcs_inferred'):
        need(report[k] is False,'historical/runtime overclaim')
    need(report['new_authenticated_named_entities']==0 and report['overall_restoration_percent'] is None,'no fabricated completion')
    catalog,refs,content=load_catalog(ROOT/DEST);idx=resource_index(refs,{c['content_id']:c for c in content})
    need(report['catalog_profile_scopes']==catalog['profiles'],'version provenance')
    for p,f in report['source_pins'].items():need(f==fingerprint((ROOT/p).read_bytes()),'metadata pin drift')
    need(len(report['source_pins'])==4,'missing source pins')
    need([m['floor_token'] for m in report['maps']]==list(TARGETS),'finite four maps')
    for m in report['maps']:
        digest,w,h=TARGETS[m['floor_token']]
        need(m['sha256']==digest and (m['width'],m['height'])==(w,h) and m['cells']==w*h and m['bytes']==8+6*w*h,'source map identity')
        need(m['name'] is None and [p['ordinal'] for p in m['planes']]==[1,2,3],'no guessed names or shuffled planes')
        for i,p in enumerate(m['planes']):
            histogram=p['histogram'];need(histogram==sorted(histogram) and len({r[0] for r in histogram})==len(histogram),'histogram unique order')
            need(all(type(k)is int and 0<=k<=65535 and type(n)is int and n>0 for k,n in histogram) and sum(n for k,n in histogram)==m['cells'],'cell conservation')
            if i<2:need(p['resource_value_comparisons']=={profile:join_histogram(histogram,profile,idx) for profile in PROFILES},'resource candidates differ from exact catalog')
            else:need('resource_value_comparisons' not in p and p['role']=='ORDINAL_THIRD_PLANE_NOT_GRAPHIC_ALIAS_NOT_ENTITY_ID','event bits are not graphic/entity IDs')

def main():
    a=argparse.ArgumentParser();a.add_argument('--maps',type=Path);a.add_argument('--output',type=Path);a.add_argument('--verify',type=Path);args=a.parse_args()
    if args.verify:replay(json.loads(args.verify.read_bytes()));print('R21_FOUR_MAP_RESOURCE_CONTENT_REPLAY=PASS; SAME_BUILD_AND_NAMES_OPEN')
    else:
        report=build(args.maps);replay(report);args.output.write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())

if __name__=='__main__':main()
