"""Offline material integration; preserve exact source report and bounded unknowns."""
import argparse
from collections import Counter
import csv
import gzip
import json
from pathlib import Path
from tools.stoneage_village_interiors_r34 import ROOT, INPUTS, TARGETS, SOURCES, annotations, pin, sha, require

RAW = 'research/recovered/STONEAGE-VILLAGE-INTERIORS-SOURCE-R34.json'
RAW_SHA = '59f1c445e3902e15d0acfd113ea97adf59ef44f3201ba8ba5bdc1de3da407a05'
OUT = 'research/recovered/STONEAGE-VILLAGE-INTERIORS-MATERIAL-R34.json'
REFS = 'research/recovered/logical-alias-catalog-r1/REFERENCES-R1.tsv.gz'
CONTENTS = 'research/recovered/logical-alias-catalog-r1/CONTENTS-R1.tsv.gz'
PINS = {REFS:'3092102e3ee83524ccbf27414ce0cf5bc5579d9a5c8638bfa073f9e62a4db1ea',
        CONTENTS:'2e4ac01f97d2e481ca1517c50a5ae6df96097dab72f4453273a761e938c35b89'}

def validate_source(d):
    require(d['schema']=='stoneage.original_village_room_material.r34','schema')
    require(d['source_scope']=='TWO_DATED_2003_THIRD_PARTY_MAP_CAPTURES_NOT_AUTHENTICATED_OFFICIAL_BUILD','source overclaim')
    require(d['source_packages']=={k:{'capture':v[0],'sha256':v[1]} for k,v in SOURCES.items()},'carrier provenance drift')
    require(d['source_pins']=={p:pin((ROOT/p).read_bytes()) for p in INPUTS},'original source pins drift')
    expected_boundaries={'original_game_executed':False,'same_build_name_or_npc_binding_proven':False,
        'rendered_scene_proven':False,'plane3_event_or_walkability_semantics_proven':False,
        'room_name_from_dat':False,'original_map_grid_published':False,'new_authenticated_tw10_entities':0,
        'stage_a':'7_PARTIAL_2_OPEN','stage_b_wiki':'GATED','r79':'PAUSED_NON_BLOCKING','overall_percent':None}
    require(d['boundaries']==expected_boundaries,'historical/runtime boundary drift')
    require([x['map_token'] for x in d['rooms']]==list(TARGETS),'four distinct source rooms required')
    notes=annotations()
    for room in d['rooms']:
        token=room['map_token'];w,h,j,z,counts=TARGETS[token]
        require(room['name_reference']==notes[token],'name-source promotion or reference drift')
        require((room['width'],room['height'])==(w,h) and room['source_path']==f'map/{token}.DAT','room source path or geometry')
        require(set(room['original_files'])=={'june','dec'},'missing original occurrence')
        for label,expected in [('june',j),('dec',z)]:
            require(room['original_files'][label]['sha256']==expected and room['original_files'][label]['bytes']==8+6*w*h,'original complete digest or extent')
        require([p['ordinal'] for p in room['planes']]==[1,2,3],'plane order')
        for i,p in enumerate(room['planes']):
            require(p['cells']==w*h and p['changed_cells']==counts[i],'cell conservation')
            if counts[i]:
                old,new=(0,2) if i==1 else (16384,49152)
                require(p['transitions']==[{'june_u16':old,'dec_u16':new,'xor_mask':old^new,'cells':counts[i]}],'actual unsigned source transition differs')
                require(p['xor_counts']==[[old^new,counts[i]]],'XOR multiplicity')
                require(p['june_sha256']!=p['dec_sha256'],'changed layer hash contradiction')
            else:
                require(p['transitions']==[] and p['xor_counts']==[] and p['june_sha256']==p['dec_sha256'],'unchanged source control')

def build():
    raw=(ROOT/RAW).read_bytes();require(sha(raw)==RAW_SHA,'archived exact raw source report drift')
    d=json.loads(raw);validate_source(d)
    for path,digest in PINS.items():require(sha((ROOT/path).read_bytes())==digest,'original catalog source drift')
    # Only logical alias 2, never physical bitmap 2, is a numeric candidate query.
    with gzip.open(ROOT/CONTENTS,'rt') as f:
        blocks={x['content_id']:x for x in csv.DictReader(f,delimiter='\t')}
    with gzip.open(ROOT/REFS,'rt') as f:
        refs=[x for x in csv.DictReader(f,delimiter='\t') if x['logical_alias']=='2']
    profiles={}
    for profile in ('TW10','CN50','PATCH129'):
        rows=[x for x in refs if x['profile']==profile]
        profiles[profile]={'reference_count':len(rows),'distinct_rd_contents':len({(blocks[x['content_id']]['bytes'],blocks[x['content_id']]['rd_sha256']) for x in rows}),
            'references':[{'source_index':int(x['source_index']),'physical_bitmapno':int(x['physical_bitmapno']),'catalog_content_id':x['content_id']} for x in rows]}
    files=[v for room in d['rooms'] for v in room['original_files'].values()]
    unique={(v['bytes'],v['sha256']) for v in files}
    return {'schema':'stoneage.village_room_material_integration.r34',
        'source_pins':{p:pin((ROOT/p).read_bytes()) for p in (RAW,REFS,CONTENTS)},
        'full_file_conservation':{'occurrences':len(files),'unique_contents':len(unique),
            'logical_bytes':sum(v['bytes'] for v in files),'unique_content_bytes':sum(n for n,s in unique),
            'original_deleted_bytes':0},
        'actual_compared_field_pairs':sum(room['width']*room['height']*3 for room in d['rooms']),
        'first_plane_changed_cells':0,'second_plane_changed_cells':4,'third_plane_changed_cells':199,
        'part_value_transition':{'map_token':1001,'ordinal':2,'old':0,'new':2,'cells':4},
        'numeric_logical_alias_2_candidates':profiles,
        'candidate_query_is_actual_runtime_selection':False,'value_2_is_named_npc_or_pet':False,
        'third_plane_xor_0x8000_is_proven_event_or_walkability_rule':False,
        'all_four_named_rooms_certified_tw10':False,'original_map_grids_or_pixels_published':False,
        'next':'ORIGINAL_CLIENT_ACQUISITION_AND_MATERIAL_ROTATION_35'}

def verify_original(directory):
    """Independent uint16 decoder; does not call the primary DAT/delta parser."""
    raw=(ROOT/RAW).read_bytes();require(sha(raw)==RAW_SHA,'original report digest');d=json.loads(raw)
    for room in d['rooms']:
        arrays=[]
        for label in ('june','dec'):
            found=[p for p in (directory/label).rglob('*') if p.is_file() and p.parent.name.casefold()=='map' and p.name.casefold()==f"{room['map_token']}.dat"]
            require(len(found)==1,'independent original path ambiguity')
            b=found[0].read_bytes();require(pin(b)==room['original_files'][label],'independent original identity')
            require((int.from_bytes(b[:4],'little'),int.from_bytes(b[4:8],'little'))==(room['width'],room['height']),'independent dimensions')
            arrays.append(b)
        n=room['width']*room['height']
        for k,plane in enumerate(room['planes']):
            slabs=[b[8+2*n*k:8+2*n*(k+1)] for b in arrays]
            for label,b in zip(('june','dec'),slabs):require(sha(b)==plane[label+'_sha256'],'independent source plane digest')
            values=[[int.from_bytes(b[i:i+2],'little') for i in range(0,len(b),2)] for b in slabs]
            transitions=Counter((x,y) for x,y in zip(*values) if x!=y)
            require(transitions=={(v['june_u16'],v['dec_u16']):v['cells'] for v in plane['transitions']},'independent actual transition mismatch')
    print('R34_INDEPENDENT_ORIGINAL_11700_FIELD_PAIRS=PASS')

def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--original-maps',type=Path);args=a.parse_args()
    if args.original_maps:verify_original(args.original_maps)
    obj=build();raw=(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
    if args.write:(ROOT/OUT).write_bytes(raw)
    else:require((ROOT/OUT).read_bytes()==raw,'material integration no longer exactly replays')
    print('R34_FOUR_ROOM_SOURCE_AND_ALIAS_CANDIDATE_CONSERVATION=PASS')

if __name__=='__main__':main()
