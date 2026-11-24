"""PET15 full claimed TW75 master census, source-bounded field projections only."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import html
import json
import re
from pathlib import Path

from tools import stoneage_pet_high_first_tw75_master_probe as p
from tools.stoneage_enemybase_probe import INDEX

ROOT=p.ROOT
TARGET=ROOT/'research/pets/PET-HIGH-FIRST-15-TW75-MASTER-FIELD-CATALOG-R1.json'
SOURCE_SHA='1b2e9fb0f8889dc857e80b8b8e7bdb5e2372e52b0789df336b601609e29af832'
SOURCE_BLOB='4e4da03e5d40368e9631eefb8b98ed489e789cb1'
ATLAS=ROOT/'research/pets/PET-HIGH-FIRST-TW85-NATIVE-SPR-ALBUM-R1.json'
ALBUM=ROOT/'research/pets/PET-HIGH-FIRST-TW85-ORIGINAL-PE-ALBUM-GRID-R1.json'
TW1=ROOT/'research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json'


def recover():
    raw,info=p.get(p.MEDIA+'/file/'+p.QUICK)
    if not raw: raise ValueError('public landing unavailable')
    m=re.search(r'<a\b[^>]*\bid=["\']downloadButton["\'][^>]*>',raw.decode('utf-8','replace'),re.I)
    if not m: raise ValueError('public download link unavailable')
    link=re.search(r'\bhref=["\']([^"\']+)["\']',m.group(0),re.I)
    if not link: raise ValueError('public download link missing')
    data,info=p.get(html.unescape(link.group(1)))
    if data is None or (len(data),p.sha(data),p.blob(data))!=(143465,SOURCE_SHA,SOURCE_BLOB):
        raise ValueError('claimed master bytes changed or unavailable')
    return data,info


def parse(raw,encoding):
    result=[]
    for n,line in enumerate(raw.decode(encoding).splitlines(),1):
        if not line.strip() or line.lstrip().startswith('#'): continue
        f=line.split(',')
        if len(f)!=56: raise ValueError('source column drift')
        def integer(key):
            v=f[INDEX[key]].strip()
            return int(v) if v else None
        v={'physical_line':n,'name':f[0],'template_id':integer('TEMPNO'),'initnum':integer('INITNUM'),
           'lvup_literal':f[INDEX['LVUPPOINT']],
           'base':[integer(k) for k in ('BASEVITAL','BASESTR','BASETGH','BASEDEX')],
           'elements':[integer(k) for k in ('EARTHAT','WATERAT','FIREAT','WINDAT')],
           'skill_slots':[integer('PETSKILL'+str(k)) for k in range(1,8)],
           'skill_slot_capacity':integer('SLOT'),'graphic':integer('IMGNUMBER'),'pet_flag':integer('PETFLG'),
           'row_sha256':p.sha(line.encode(encoding))}
        result.append((v,tuple(s.strip() for s in f[6:])))
    return result


def build():
    data,http=recover()
    comp,_=p.get(p.GAVIN)
    if comp is None or (p.sha(comp),p.blob(comp))!=(p.GAVIN_SHA,p.GAVIN_BLOB):
        raise ValueError('comparison source changed')
    rows=parse(data,'cp950'); comparison=parse(comp,'gb18030')
    if (len(rows),len(comparison))!=(960,1816): raise ValueError('source counts drift')
    by_id=defaultdict(list)
    for v,tail in comparison:by_id[v['template_id']].append((v,tail))
    atlas=json.loads(ATLAS.read_bytes())
    album=json.loads(ALBUM.read_bytes())
    tw1=json.loads(TW1.read_bytes())
    native={x['tw85_original_spr_number']:x['program_routes'] for x in atlas['records']}
    early=defaultdict(list)
    for row in tw1['records']:early[row['graphic_number']].append(row['name_as_written'])
    names=defaultdict(list)
    for program,info in album['programs'].items():
        for row in info['source_records']:
            names[row['original_name_cp950']].append([program,row['slot']])
    cmp_counts=Counter(); flags=Counter(); id_counts=Counter(); pets=[]; pet_names=Counter(); statuses=Counter()
    for v,tail in rows:
        id_counts[v['template_id']]+=1
        flags[str(v['pet_flag'])]+=1
        options=by_id[v['template_id']]
        exact=[x for x,t in options if t==tail]
        status='EXACT_NONNAME_50_FIELD_TAIL' if exact else ('SAME_ID_DIFFERENT_TAIL' if options else 'NO_SAME_ID')
        cmp_counts[status]+=1
        if v['pet_flag']!=1:continue
        pet_names[v['name']]+=1
        lanes=native.get(v['graphic'],{})
        qualified={k:x['original_name_cp950'] for k,x in lanes.items() if x['record_source_status']=='SOURCE_LOCAL_NAMED_ROUTE'}
        matching=sorted(k for k,n in qualified.items() if n==v['name'])
        early_names=early.get(v['graphic'],[])
        s=('TW85_NATIVE_SAME_GRAPHIC_NAME' if matching else 'TW85_NATIVE_GRAPHIC_OTHER_NAME' if qualified else
           'TW10_SAME_GRAPHIC_NAME' if v['name'] in early_names else 'TW10_GRAPHIC_OTHER_NAME' if early_names else
           'NAME_ONLY_IN_TW85_GRID' if v['name'] in names else 'NO_QUALIFIED_NAME_GRAPHIC_LINK')
        statuses[s]+=1
        pets.append({**v,'comparison_status':status,'comparison_matching_physical_lines':[x['physical_line'] for x in exact],
                     'tw85_native_graphic_names':qualified,'tw85_matching_programs':matching,
                     'tw85_exact_name_album_slots':names.get(v['name'],[]),'tw10_names_at_graphic':early_names,
                     'client_join_status':s,'official_live_pet_release_verified':False})
    summary={'source_rows':len(rows),'comparison_rows':len(comparison),'source_pet_flag_counts':dict(flags),
             'source_duplicate_template_ids':{str(k):v for k,v in id_counts.items() if v>1},
             'all_rows_comparison_status':dict(cmp_counts),'pet_flag_1_rows':len(pets),
             'pet_flag_1_distinct_exact_names':len(pet_names),'pet_flag_1_duplicate_exact_name_counts':{k:v for k,v in pet_names.items() if v>1},
             'pet_flag_1_client_join_status':dict(statuses),
             'pet_flag_1_comparison_status':dict(Counter(x['comparison_status'] for x in pets))}
    return {'scope':'PUBLIC_2012_CLAIMED_WAYI75_UNAUTHENTICATED_CLASSIC_PC_MASTER_FIELD_PROJECTION',
            'source':{'bytes':len(data),'sha256':SOURCE_SHA,'git_blob':SOURCE_BLOB,'encoding':'cp950','quick_key':p.QUICK,'download_http':http},
            'comparison_source':{'sha256':p.GAVIN_SHA,'git_blob':p.GAVIN_BLOB,'encoding':'gb18030','qualification':'LATER_COMMUNITY_NOT_OFFICIAL'},
            'input_git_blobs':{x.name:p.blob(x.read_bytes()) for x in (ATLAS,ALBUM,TW1)},
            'summary':summary,'pet_flag_1_field_projections':pets,
            'source_all_rows_preserved_privately_not_published':True,
            'official_same_deployment_verified':False,'official_species_count':None,
            'nonpet_rows_not_promoted':True,'same_name_graphic_not_official_release':True}


def verify(r):
    if r['source']['sha256']!=SOURCE_SHA or r['source']['git_blob']!=SOURCE_BLOB or r['summary']['source_rows']!=960:
        raise ValueError('source identity')
    if r['input_git_blobs']!={x.name:p.blob(x.read_bytes()) for x in (ATLAS,ALBUM,TW1)}:
        raise ValueError('client input drift')
    if r['official_same_deployment_verified'] or r['official_species_count'] is not None or not r['nonpet_rows_not_promoted']:
        raise ValueError('unsupported official promotion')
    s=r['summary'];rows=r['pet_flag_1_field_projections']
    if len(rows)!=s['pet_flag_1_rows'] or len(rows)!=s['source_pet_flag_counts'].get('1',0) or sum(s['source_pet_flag_counts'].values())!=960 or any(x['pet_flag']!=1 or x['official_live_pet_release_verified'] for x in rows):
        raise ValueError('pet flag conservation')
    if dict(Counter(x['client_join_status'] for x in rows))!=s['pet_flag_1_client_join_status']:
        raise ValueError('join coverage drift')
    if sum(s['all_rows_comparison_status'].values())!=960:
        raise ValueError('comparison census drift')
    return s


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--source',action='store_true');args=a.parse_args()
    r=build() if args.source else json.loads(TARGET.read_bytes())
    print(json.dumps(verify(r),ensure_ascii=False,sort_keys=True))
    if args.source:TARGET.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
