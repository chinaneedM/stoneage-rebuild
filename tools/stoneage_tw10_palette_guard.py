"""Independent archived-instruction and actual-color-source evidence gate."""
import hashlib
import json
from pathlib import Path
import re

from tools.stoneage_original_animation_lab import ROOT
from tools import stoneage_tw10_palette as palette

DIRECTORY=ROOT/'research/recovered'
SOURCE=DIRECTORY/'STONEAGE-TW10-PALETTE-P2B-ACTUAL-COLOR-SOURCE-R1.json'
POINTER=DIRECTORY/'STONEAGE-TW10-PALETTE-P2B-POINTER-SOURCE-R1.json'
INITIAL=DIRECTORY/'STONEAGE-TW10-PALETTE-P2B-INITIAL-TRIAGE-R1.json'
SOURCE_SHA='3521274ecb0cc861623c9a8ccc43ec95c2b7c7719f2949e5e611be80a36a4977'
POINTER_SHA='9686bdd0a1ee280fcc03873c411027358b3d7a7f34f204cf7ceccfd045b2e6ce'
INITIAL_SHA='0b42d83670d0e951372c6a043066665a97ca9616b4504adbc2163ce01da002c3'


def require(ok,message):
    if not ok:raise ValueError(message)


def reserved_from_instruction_metadata(window):
    """Only the original fixed initializer's literal MOV/SUB/PUSH prefix."""
    regs=dict.fromkeys(('al','bl','cl','dl'),0);esp=0;memory={}
    for instruction in window['instructions']:
        if instruction['rva']>=0x9924:break
        op=instruction['operands'];mnemonic=instruction['mnemonic']
        if mnemonic=='sub' and op=='esp, 0x80':esp-=128
        elif mnemonic=='push':esp-=4
        elif mnemonic=='mov':
            target,value=op.rsplit(', ',1);number=regs[value] if value in regs else int(value,0)
            if target in regs:regs[target]=number
            else:
                match=re.fullmatch(r'byte ptr \[esp(?: \+ (0x[0-9a-f]+|[0-9]+))?\]',target)
                require(match is not None,'unqualified original initializer store')
                memory[esp+(int(match[1],0) if match[1] else 0)]=number
        else:raise ValueError('unqualified original initializer instruction')
    return tuple(tuple(memory[esp+8+i*4+j] for j in range(3)) for i in range(32))


def validate(pointer,source,old):
    require(pointer['original_exe']['sha256']==palette.EXE_SHA and
            pointer['original_palette']['sha256']==palette.PAL_SHA,'original file identities')
    literals={s['rva']:s['text'] for s in pointer['palette_literals']}
    slots=sorted(pointer['static_literal_pointer_slots'],key=lambda x:x['slot_rva'])
    require([x['slot_rva'] for x in slots]==list(range(0x56178,0x561b8,4)),'original pointer table geometry')
    require([literals[x['literal_rva']] for x in slots]==
            ['data\\pal\\Palet_'+str(i)+'.sap' for i in list(range(1,16))+[0]],'original pointer table path order')
    window=next(w for w in pointer['windows'] if w['start_rva']==0x96c0)
    require(reserved_from_instruction_metadata(window)==palette.FIXED_RGB,'32 compiled reserved RGB constants')
    ins={i['rva']:(i['mnemonic'],i['operands']) for i in window['instructions']}
    pivots={0x99d3:('mov','eax, dword ptr [0x4561b4]'),0x99e9:('mov','esi, 0x49f611'),
            0x99ef:('call','0x4485c2'),0x99f5:('mov','byte ptr [esi + 1], al'),
            0x99fe:('mov','byte ptr [esi], al'),0x9a05:('mov','byte ptr [esi - 1], al'),
            0x9a0b:('add','esi, 4'),0x9a11:('cmp','esi, 0x49f991'),
            0x9a29:('mov','byte ptr [0x49f872], 0'),0x9a30:('mov','byte ptr [0x49f871], 0'),
            0x9a37:('mov','byte ptr [0x49f870], 0'),0x9a4c:('push','0x49f5d0'),
            0x9a54:('call','dword ptr [edx + 0x14]')}
    require(all(ins.get(rva)==expected for rva,expected in pivots.items()),'original BGR/index/black-entry/API pivots')
    require(source['schema']=='stoneage.tw10.palette_initial_native.p2b_v1','actual color source schema')
    require(source['original_exe_sha256']==palette.EXE_SHA and source['original_palette_sha256']==palette.PAL_SHA,'native source identity')
    require(source['fixed_32_rgb_sha256']==palette.digest(bytes(v for c in palette.FIXED_RGB for v in c)),'native fixed constants digest')
    require(source['read_file_bytes']==672 and source['preserved_unread_suffix_bytes']==36,'SAP byte budget')
    for key,count,cache in [('original_actual_palette',672,0),('synthetic_palette_with_original_code',672,0),
                            ('synthetic_cached_state_with_original_code',0,1)]:
        state=source[key]
        require(state['reads']==count and state['cache_guard']==cache,'native read/cache behavior')
        require(state['closes']==int(cache==0),'native close behavior')
        require(state['opens']==([] if cache else [{'path':'data\\pal\\Palet_0.sap','mode':'rb'}]),'native open behavior')
        for flag in ('original_client_executed','original_com_palette_creation_executed','real_file_io_executed'):
            require(state[flag] is False,'unproved native execution effect')
    for flag in ('actual_scene_palette_selection_proven','historical_color_screenshot_observed','original_client_executed','original_assets_published'):
        require(source[flag] is False,'unproved whole-game/display/publication claim')
    require(source['source_palette_rgb_mapping_verified'] is True,'missing bounded RGB proof')
    require(source['original_actual_palette']['rgb_sha256']=='e02d929c63d9edce15891c28748758ef8da90d28fed5f525fd86ec73d34364e3','actual native Palet_0 RGB digest')
    synthetic=bytes((i*17+3)%256 for i in range(708))
    require(source['synthetic_palette_with_original_code']['rgb_sha256']==palette.digest(palette.initial_rgb(synthetic)),'native synthetic RGB reference')
    require(len(source['color_animation_previews'])==len(old['cases'])==3,'finite preview count')
    for actual,prior in zip(source['color_animation_previews'],old['cases']):
        require(actual['selectors']==prior['selectors'] and actual['frames']==prior['frames'],'same-source animation selection')
        require(actual['preview_mode']==palette.MODE and actual['source_palette_rgb_mapping_verified'] is True,'color preview scope')
        for flag in ('actual_scene_palette_selection_proven','original_client_executed','assistant_viewed_or_heard_original'):
            require(actual[flag] is False,'unproved preview observation claim')
        require(len(actual['bitmap_witnesses'])==len(prior['bitmap_witnesses']),'original bitmap coverage')
        for a,b in zip(actual['bitmap_witnesses'],prior['bitmap_witnesses']):
            for field in ('bitmapno','adrn_record_sha256','rd_block_sha256','palette_index_sha256'):
                require(a[field]==b[field],'color export changed original indexed pixels/source')
            require(re.fullmatch('[0-9a-f]{64}',a['private_indexed_color_png_sha256']) is not None,'missing color PNG digest')
    return True


def main():
    for path,pin in [(SOURCE,SOURCE_SHA),(POINTER,POINTER_SHA),(INITIAL,INITIAL_SHA)]:
        require(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'archived original derivative changed: '+path.name)
    validate(json.loads(POINTER.read_bytes()),json.loads(SOURCE.read_bytes()),
             json.loads((DIRECTORY/'STONEAGE-TW10-ANIMATION-OBSERVATION-P2A-ACTUAL-SOURCE-R1.json').read_bytes()))
    print('P2B_ORIGINAL_BGR_INITIALIZATION_NATIVE_AND_COLOR_PIXEL_SOURCE=PASS; ACTUAL_SCENE_CLIENT_BOOT=OPEN')


if __name__=='__main__':main()
