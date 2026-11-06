"""Read the verified PE .data capture-condition rows and two preserved item masters.

Private CLI: inputs are already extracted proprietary files. Only derived metadata
is printed. The original game program is NEVER launched. No historical server
attribution or actual inventory deletion can be inferred from this static table.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

EXE_EXPECTED_SHA = 'd5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00'
ARCHIVE_SHA = 'd71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
ENEMY_MASTER_SHA = {
    'enemybase.txt': '1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7',
    'enemybase2.txt': '8ecb23231ae1aeb21fe943c7b459f0c0d10ef3599aedfeaeccca783b077f5fd4',
}
SETUP_CF_SHA = 'b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d'
MASTER_SHA = {
    'itemset.txt': 'a415e78f9aab2e5ea5ca92ecb7430253f7be1ba7c876d6b0bb6d067b1b466688',
    'itemset0710.txt': '6d6d63fda59c6bda2f239fe18c9361b5c9da18c84f678b7cc95bde24544292fb',
}
SECTIONS = {
    '.text': '2a42c0ce1951b0963898e2a5c95be920b8eb3b42bf329b012ba03a6d4ebcd11d',
    '.data': 'f30026ba6ed6212b59cdf580fed718610c70af47f03c6d41ac65f35fc5a5ae95',
    '.rdata': 'c2740af5992a885b4d4ba14c988525ff7fa3b3329e973d87d628a28d6b5c0611',
    '.idata': '4838a3158456bd0a8eee76a8a666fa67222d5e3b432a87f50906f0b2c64ae0d4',
}
DATA_VA, RECORDS, ROW_WIDTH = 0x58cd60, 128, 64
TEXT_VA = 0x537d30
CALL_SITES = {
    'precheck_key53': (0x537d51, 0x42db90),
    'delete_key53': (0x537e6f, 0x42db90),
    'delete_inventory': (0x538099, 0x433ab0),
}


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def pe_reader(exe: bytes):
    """Require every file-backed section to match the earlier accepted source."""
    if len(exe) != 1897867 or exe[:2] != b'MZ':
        raise ValueError('PE length/header differs from recorded GMSV')
    pe = struct.unpack_from('<I', exe, 0x3c)[0]
    if exe[pe:pe+4] != b'PE\0\0':
        raise ValueError('PE signature differs')
    n = struct.unpack_from('<H', exe, pe+6)[0]
    optional_len = struct.unpack_from('<H', exe, pe+20)[0]
    base = struct.unpack_from('<I',exe,pe+24+28)[0]
    sections = {}
    for i in range(n):
        p=pe+24+optional_len+i*40
        name=exe[p:p+8].rstrip(b'\0').decode('ascii','strict')
        _,rva,size,off=struct.unpack_from('<IIII',exe,p+8)
        # size in PE header is SizeOfRawData at +16, not VirtualSize
        if name in SECTIONS:
            if size<=0 or off+size>len(exe) or sha(exe[off:off+size])!=SECTIONS[name]:
                raise ValueError(f'unverified original source section: {name}')
            sections[name]=(base+rva,off,size)
    if set(sections)!=set(SECTIONS) or base!=0x400000:
        raise ValueError('PE section topology differs')
    def take(va:int,size:int) -> bytes:
        for addr,off,cap in sections.values():
            if 0<=va-addr and va-addr+size<=cap:
                return exe[off+va-addr:off+va-addr+size]
        raise ValueError(f'VA outside verified original PE sections: {va:#x}')
    return take


def read_compiled_rows(take):
    raw=take(DATA_VA,RECORDS*ROW_WIDTH)
    entries=[]
    for i in range(RECORDS):
        row=struct.unpack_from('<16i',raw,i*ROW_WIDTH)
        key=row[0]
        if not key:
            if any(row):raise ValueError('zero-key record has nonzero trailing data')
            continue
        slots=row[1:16]
        if -1 not in slots: raise ValueError('source record missing item sentinel')
        stop=slots.index(-1)
        if stop<1 or stop>10:raise ValueError('unexpected item count')
        if slots[stop:10]!=(-1,)*(10-stop) or slots[10:]!=(0,)*5:
            raise ValueError('unexpected trailing item-slot padding')
        items=list(slots[:stop])
        if any(v<=0 for v in items): raise ValueError('invalid item ID')
        entries.append({'source_record_index':i,'char_int_key_53_value':key,'required_item_id_candidates':items,'record_sha256':sha(raw[i*64:(i+1)*64])})
    return entries,sha(raw)


def read_items(raw: bytes):
    rows={}
    for number,line in enumerate(raw.splitlines(keepends=True),1):
        columns=line.rstrip(b'\r\n').split(b',')
        if len(columns)!=94:
            raise ValueError(f'unexpected master width line {number}')
        if not columns[16].isdigit():
            continue
        key=int(columns[16])
        if key in rows: raise ValueError('duplicate original item ID')
        rows[key]={
            'line':number,'name_cp950':columns[0].decode('cp950','strict'),
            'original_row_sha256':sha(line),
            'callback_ascii':columns[10].decode('ascii','strict'),
            'item_type_ascii':columns[19].decode('ascii','strict'),
        }
    return rows


def read_enemybase(raw: bytes):
    rows={}
    for number,line in enumerate(raw.splitlines(keepends=True),1):
        if not line.strip():
            continue
        columns=line.rstrip(b'\r\n').split(b',')
        if len(columns)!=56:
            raise ValueError(f'unexpected original enemybase row width at {number}')
        if not columns[6].isdigit():
            continue
        key=int(columns[6])
        if key in rows:
            raise ValueError('duplicate enemybase original numeric key')
        rows[key]={'line':number,'name_cp950':columns[0].decode('cp950','strict'),
                   'original_row_sha256':sha(line)}
    return rows


def derive(exe_path: Path, selected: Path, alternate: Path, enemybase: Path,
           enemybase2: Path, setup_cf: Path, archive:Path|None=None):
    if archive is not None and sha(archive.read_bytes())!=ARCHIVE_SHA:
        raise ValueError('original RAR archive identity differs')
    exe=exe_path.read_bytes()
    complete_sha=sha(exe)
    take=pe_reader(exe)
    calls={}
    for label,(addr,target) in CALL_SITES.items():
        b=take(addr,5)
        if b[0]!=0xe8 or addr+5+struct.unpack_from('<i',b,1)[0]!=target:
            raise ValueError(f'original conditional capture call differs: {label}')
        calls[label]={'source_va':addr,'target_va':target,'source_sha256':sha(b)}
    entries,raw_sha=read_compiled_rows(take)
    if len(entries)!=11 or sum(len(e['required_item_id_candidates']) for e in entries)!=13:
        raise ValueError('original active capture table entries differ')
    if len({a for e in entries for a in e['required_item_id_candidates']})!=12:
        raise ValueError('original distinct item IDs differ')
    masters={}
    for fn,path in [('itemset.txt',selected),('itemset0710.txt',alternate)]:
        raw=path.read_bytes()
        if sha(raw)!=MASTER_SHA[fn]:raise ValueError('original item master SHA differs: '+fn)
        masters[fn]=read_items(raw)
    all_items=sorted({id for row in entries for id in row['required_item_id_candidates']})
    index=[]
    for item in all_items:
        a,b=(masters[n].get(item) for n in MASTER_SHA)
        if a and b and a['name_cp950']!=b['name_cp950']:
            raise ValueError('same item ID has different source names: review as conflict')
        index.append({'item_id':item,'selected':a,'alternate_0710':b,
                      'presence':'IN_BOTH' if a and b else 'ONLY_ALTERNATE' if b else 'ONLY_SELECTED' if a else 'IN_NEITHER'})
    if sorted(i['item_id'] for i in index if i['presence']=='ONLY_ALTERNATE')!=[20247,20253,20259]:
        raise ValueError('alternate-only required-item IDs differ')
    original_setup=setup_cf.read_bytes()
    if sha(original_setup)!=SETUP_CF_SHA:
        raise ValueError('original server setup.cf identity differs')
    setup_text=original_setup.decode('cp950','strict')
    if setup_text.splitlines().count('enemybasefile=./data/enemybase.txt')!=1:
        raise ValueError('original selected enemybase path differs')
    enemy_sources={}
    for fn,path in [('enemybase.txt',enemybase),('enemybase2.txt',enemybase2)]:
        raw=path.read_bytes()
        if sha(raw)!=ENEMY_MASTER_SHA[fn]:
            raise ValueError('original enemybase source SHA differs: '+fn)
        enemy_sources[fn]=read_enemybase(raw)
    enemy_crosswalk=[]
    for entry in entries:
        key=entry['char_int_key_53_value']
        a=enemy_sources['enemybase.txt'].get(key)
        b=enemy_sources['enemybase2.txt'].get(key)
        if not a or (b and a['name_cp950']!=b['name_cp950']):
            raise ValueError('same-numeric original enemybase name missing or conflicted')
        enemy_crosswalk.append({'char_int_key_53_value':key,
                               'configured_enemybase_field6_same_numeric_candidate':a,
                               'alternate_enemybase2_field6_same_numeric_candidate':b,
                               'semantic_join_runtime_verified':False})
    if len(enemy_crosswalk)!=11 or sum(bool(x['alternate_enemybase2_field6_same_numeric_candidate']) for x in enemy_crosswalk)!=7:
        raise ValueError('same-carrier enemybase numeric coverage changed')
    return {
        'schema':'stoneage.world37.r2b.compiled_capture_requirement_index.r1',
        'version_scope':'PRESERVED_LATER_COMMUNITY_MIXED25_NOT_TW1_OFFICIAL_OR_1999_JSS',
        'archive_expected_sha256':ARCHIVE_SHA,
        'archive_in_this_invocation_sha256_verified':archive is not None,
        'exe_expected_sha256':EXE_EXPECTED_SHA,
        'exe_local_full_sha256':complete_sha,
        'exe_original_full_sha256_verified':complete_sha==EXE_EXPECTED_SHA,
        'qualification':'FOUR_PE_SECTIONS_REVERIFIED_NOT_FULL_EXE' if complete_sha!=EXE_EXPECTED_SHA else 'FULL_EXE_VERIFIED',
        'original_source_file_backed_sections_sha256':SECTIONS,
        'original_condition_table':{'source_va':DATA_VA,'record_bytes':ROW_WIDTH,'capacity':RECORDS,
                                    'raw_table_sha256':raw_sha,'active_rows':len(entries),
                                    'zero_rows':RECORDS-len(entries),'item_references':13,'distinct_item_ids':12,
                                    'rows':entries},
        'compiled_call_sites':calls,
        'original_item_masters_sha256':MASTER_SHA,
        'original_item_id_crosswalk':index,
        'original_enemybase_master_sha256':ENEMY_MASTER_SHA,
        'source_setup_cf_sha256':SETUP_CF_SHA,
        'source_setup_enemybasefile':'./data/enemybase.txt',
        'enemybase_field6_numeric_join_candidates':enemy_crosswalk,
        'summary':{'selected_present':sum(bool(i['selected']) for i in index),
                   'alternate_present':sum(bool(i['alternate_0710']) for i in index),
                   'alternate_only_ids':[i['item_id'] for i in index if i['presence']=='ONLY_ALTERNATE'],
                   'selected_enemybase_matching_keys':len(enemy_crosswalk),
                   'alternate_enemybase2_matching_keys':sum(bool(x['alternate_enemybase2_field6_same_numeric_candidate']) for x in enemy_crosswalk)},
        'negative_boundaries':{
            'actual_conditional_item_consumption_executed':False,
            'original_dynamic_capture_tail_executed':False,
            'original_enemy_species_names_proven_by_key53':False,
            'same_numeric_field6_enemybase_proves_live_role_key53_identity':False,
            'configured_original_item_master_selected_is_alternate':False,
            'all_128_capture_rows_are_real_pet_species':False,
            'same_build_official_TW1_or_JSS1999_server_verified':False,
            'missing_selected_item_ids_are_invented_or_filled':False,
            'historical_STAGE_A':'7_PARTIAL_2_OPEN','Stage_B_wiki':'GATED',
            'R79':'PAUSED_NON_BLOCKING','overall_percent':None,
        },
        'next':'WORLD37_R2B_DYNAMIC_TAIL_REQUIRES_FULL_VERIFIED_EXECUTABLE_AND_X86_EMULATOR; PRIORITIZE_FURTHER_MATERIAL_CONTENT_IF_UNAVAILABLE',
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('exe',type=Path)
    ap.add_argument('selected_itemset',type=Path)
    ap.add_argument('alternate_itemset',type=Path)
    ap.add_argument('--archive',type=Path)
    ap.add_argument('--enemybase',type=Path,required=True)
    ap.add_argument('--enemybase2',type=Path,required=True)
    ap.add_argument('--setup',type=Path,required=True)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    report=derive(args.exe,args.selected_itemset,args.alternate_itemset,args.enemybase,args.enemybase2,args.setup,args.archive)
    payload=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(payload,encoding='utf-8')
    else:print(payload,end='')

if __name__=='__main__':main()
