"""Four historical room DATs: original plane/value deltas, not rendered gameplay."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    1001: (30, 30, '62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90', '4665e4621be1d36a9dfb82c87d69d9ba5d9eaa3088599648a54f2655db105568', [0,4,80]),
    1003: (30, 30, 'fc3037a1850c8baf06ad5874a4cb49ca5e13e9315c020f64c019417c33b694e6', 'fc3037a1850c8baf06ad5874a4cb49ca5e13e9315c020f64c019417c33b694e6', [0,0,0]),
    1005: (30, 30, 'a6c9d1e43223a8afc515e37367d58cfcc6c301909e9e060d4c80d35fcb87c7c9', '71bb2a4a72991b8420128dbaf1cb8885eee71bd8c0302579fee7eb5afbfddd76', [0,0,52]),
    1006: (30, 40, 'aa2e7d2bdb138545a3efa30f9482d563b1781810a856b4a91c12ce83eb08ab4a', 'caee33ec3b20630949725900f217a2868c05984fe2f7e8f13fdd94250be6e3a7', [0,0,67]),
}
SOURCES = {
    'june': ('20030623234451', '372426e46765a1cf479041bdafc1d3e58fb019117d00d0b43d6a5f796620776e'),
    'dec': ('20031210092426', '5f7f58e0d26d596e926a7d551d7c24e8a9a27824d5bdc53be3955b19b0e13abc'),
}
INPUTS = (
    'research/recovered/STONEAGE-2003-MAP-TIMELINE-R1.txt',
    'research/recovered/STONEAGE-HISTORICAL-MAPEXE-SA25-LINEAGE-R1.txt',
    'research/recovered/STONEAGE-25-STABLE-MAP-NAMES-R1.txt',
    'research/recovered/STONEAGE-25-STABLE-WORLD-CONTENT-COVERAGE-R1.txt',
)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pin(raw):
    return {'bytes': len(raw), 'sha256': sha(raw), 'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

def require(ok, message):
    if not ok: raise ValueError(message)

def fields(text, prefix):
    rows = [s for s in text.splitlines() if s.startswith(prefix)]
    require(len(rows) == 1, 'one unambiguous prior source row required: '+prefix)
    return dict(s.split('=', 1) for s in rows[0].split('|')[1:])

def parse(raw):
    require(len(raw) >= 8, 'short original map header')
    w,h = struct.unpack_from('<II', raw)
    n = w*h
    require(w > 0 and h > 0 and n <= 1000000 and len(raw) == 8+6*n, 'exact bounded three-plane DAT required')
    return w,h,[raw[8+2*n*i:8+2*n*(i+1)] for i in range(3)]

def plane_delta(old, new):
    require(len(old) == len(new) and len(old)%2 == 0, 'same uint16 extents required')
    a = [v[0] for v in struct.iter_unpack('<H',old)]
    b = [v[0] for v in struct.iter_unpack('<H',new)]
    transitions = Counter((x,y) for x,y in zip(a,b) if x != y)
    return {'june_sha256': sha(old), 'dec_sha256': sha(new), 'cells': len(a),
            'changed_cells': sum(transitions.values()),
            'transitions': [{'june_u16': x, 'dec_u16': y, 'xor_mask': x^y, 'cells': count}
                            for (x,y),count in sorted(transitions.items())],
            'xor_counts': [[x,sum(c for (a,b),c in transitions.items() if a^b==x)]
                          for x in sorted({a^b for a,b in transitions})]}

def annotations():
    texts = [(ROOT/p).read_text(encoding='utf-8') for p in INPUTS]
    result = {}
    for token,(w,h,j,d,counts) in TARGETS.items():
        name = fields(texts[2],f'MAP_NAME|floor={token}|')
        coverage = fields(texts[3],f'FLOOR|id={token}|')
        require(name['status']=='RESOLVED_BIG5_CP950_CONSENSUS' and name['raw_variants']=='1','name ambiguity')
        require((int(coverage['width']),int(coverage['height']))==(w,h) and coverage['map_sha256']==j,'name/geometry reference identity')
        if token != 1003:
            timeline = fields(texts[0],f'MAP_TIMELINE|id={token}|')
            require(timeline['j_sha256']==j and timeline['d_sha256']==d and timeline['p_sha256']==j,'old exact source witness drift')
            require([int(timeline[k]) for k in ('jd_tile_diff','jd_parts_diff','jd_event_diff')]==counts,'old changed-count witness drift')
        else:
            exact = fields(texts[1],f'EXACT_SAMPLE|name={token}.DAT|')
            require(exact['sha256']==j and exact['dims']==f'{w}x{h}','unchanged control prior witness')
        result[token] = {
            'recovered25_name_escaped': name['name'], 'raw_name_sha256': name['raw_sha256'],
            'name_scope': 'LATER_RECOVERED_SERVER_FLOOR_AND_DIMENSION_CONSENSUS_NOT_SAME_GRID_OR_TW10',
            'reference_client_sha256': coverage['map_sha256'],
            'reference_npc_create_count': int(coverage['npc_create']),
            'npc_count_scope': 'PRIOR_MIXED25_CONFIGURATION_NOT_OBSERVED_POPULATION',
        }
    return result

def compare_pair(june,dec):
    w,h,a = parse(june); wd,hd,b = parse(dec)
    require((w,h)==(wd,hd),'map dimensions differ')
    return {'width':w,'height':h,'planes':[{'ordinal':i+1,**plane_delta(x,y)} for i,(x,y) in enumerate(zip(a,b))]}

def build(folder):
    notes=annotations(); rooms=[]
    for token,(w,h,j,d,counts) in TARGETS.items():
        payload=[]
        for label,expected in [('june',j),('dec',d)]:
            matches=[p for p in (folder/label).rglob('*') if p.is_file() and p.parent.name.casefold()=='map' and p.name.casefold()==f'{token}.dat']
            require(len(matches)==1,'missing or ambiguous source room')
            raw=matches[0].read_bytes(); require(sha(raw)==expected,'original DAT full SHA mismatch')
            payload.append(raw)
        delta=compare_pair(*payload)
        require((delta['width'],delta['height'])==(w,h) and [p['changed_cells'] for p in delta['planes']]==counts,'original historical count mismatch')
        rooms.append({'map_token':token,'source_path':f'map/{token}.DAT','original_files':{'june':pin(payload[0]),'dec':pin(payload[1])},'name_reference':notes[token],**delta})
    return {'schema':'stoneage.original_village_room_material.r34',
            'source_scope':'TWO_DATED_2003_THIRD_PARTY_MAP_CAPTURES_NOT_AUTHENTICATED_OFFICIAL_BUILD',
            'source_packages':{k:{'capture':v[0],'sha256':v[1]} for k,v in SOURCES.items()},
            'source_pins':{p:pin((ROOT/p).read_bytes()) for p in INPUTS}, 'rooms':rooms,
            'boundaries':{'original_game_executed':False,'same_build_name_or_npc_binding_proven':False,
                'rendered_scene_proven':False,'plane3_event_or_walkability_semantics_proven':False,
                'room_name_from_dat':False,'original_map_grid_published':False,
                'new_authenticated_tw10_entities':0,'stage_a':'7_PARTIAL_2_OPEN','stage_b_wiki':'GATED',
                'r79':'PAUSED_NON_BLOCKING','overall_percent':None}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--maps',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(); obj=build(args.maps)
    raw=(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
    args.output.write_bytes(raw)
    print('R34_JSON_BEGIN'); print(raw.decode(),end='');print('R34_JSON_END')
    print('R34_REPORT_SHA256='+sha(raw))

if __name__=='__main__':main()
