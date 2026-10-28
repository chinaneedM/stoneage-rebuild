"""Bounded original actor/parts list replay; no client, GPU or server launch.

The actor structure, map crop/aliases, world coordinates, ADRN table and phase order are injected.
Only source spans' hashes and numeric traces may enter public Git.
"""
import argparse,hashlib,json,struct
from pathlib import Path
from tools.stoneage_private_scene_order_r6 import Native,EXE_SHA,require,display_order
from tools.stoneage_private_scene_actor_r7 import PINS

ROOT=Path(__file__).resolve().parents[1]
R8_SHA='7219c30cf99995b9feae2e6c35a35978cd4864196d076745b58ad49f4f9ec3ff'
SPANS={'actor_caller_fragment':(0x407467,0x407493),'actor_insert':(0x42aa2a,0x42aaf7),
       'part_insert':(0x42a936,0x42aa2a),'part_actor_predicate':(0x42aaf7,0x42abb9),
       'list_before_after':(0x42abb9,0x42ac03),'list_to_queue':(0x42ac03,0x42ac48),
       'physical_queue':(0x44c974,0x44ca11),'ADRN_footprint_getters':(0x411304,0x4113b2),
       'sort_dispatch':(0x44c4a3,0x44c4c0),'sort_comparator':(0x44cc14,0x44cc47),
       'original_map_sweep':(0x427c37,0x427e44)}

def sha(b):return hashlib.sha256(b).hexdigest()

def reference_list(actors,parts):
    """Independent finite 1x1/mode0 source-room model, not general occlusion."""
    nodes=[]
    for actor in actors:
        at=next((i for i,n in enumerate(nodes) if actor['screen_y']>n['screen_y']),len(nodes))
        nodes.insert(at,actor)
    for part in parts:
        require(part['footprint']==[1,1] and part['raw_attribute_word']==0,'bounded original room footprint only')
        def before(a):
            return a['kind']=='actor' and ((a['world'][0]>part['world'][0] and a['world'][1]<part['world'][1]) or part['screen_y']>a['screen_y'])
        at=next((i for i,n in enumerate(nodes) if before(n)),len(nodes));nodes.insert(at,part)
    return [n['token'] for n in nodes]

def replay(exe,adrn,mapraw,pack):
    require(len(exe)==561152 and sha(exe)==EXE_SHA,'original private program identity')
    require(len(adrn)==PINS['adrn_15.bin'][0] and sha(adrn)==PINS['adrn_15.bin'][1],'whole original ADRN identity')
    require(len(mapraw)==5408 and sha(mapraw)=='62dbef1614ede0ba032ca9c69cbfdc3d43938e45baba78701885790937b86b90','whole original map1001 identity')
    from unicorn.x86_const import UC_X86_REG_ESI,UC_X86_REG_ESP,UC_X86_REG_EIP,UC_X86_REG_EBP,UC_X86_REG_EDI
    n=Native(exe);n.u.mem_write(0xb14900,adrn)
    room=pack['room'];parts=[];ids={p['map_id'] for p in room['placements']};aliases={k:[] for k in ids}
    for off in range(0,len(adrn),80):
        key=struct.unpack_from('<I',adrn,off+76)[0]
        if key in aliases:aliases[key].append(struct.unpack_from('<I',adrn,off)[0])
    require(all(len(v)==1 for v in aliases.values()),'unique original source aliases')
    for key,values in aliases.items():n.put(0x7af6b8+key*4,values[0])
    for plane,addr in [(0,0x2ad2660),(1,0x2abaf64)]:
        crop=[struct.unpack_from('<H',mapraw,8+2*(plane*900+y*30+x))[0] for y in range(13,18) for x in range(13,18)]
        n.u.mem_write(addr,struct.pack('<25H',*crop))
    for addr,value in [(0x2ab1398,5),(0x2aba480,5),(0x2ab1f24,13),(0x2ab1f2c,13)]:n.put(addr,value)
    frame=0x400f000;n.u.reg_write(UC_X86_REG_EBP,frame);n.u.reg_write(UC_X86_REG_ESP,frame-0x100)
    n.u.reg_write(UC_X86_REG_ESI,192);n.u.reg_write(UC_X86_REG_EDI,200);n.put(frame-12,228)
    n.u.emu_start(0x427c37,0x427e44,count=200000)
    require(n.u.reg_read(UC_X86_REG_EIP)==0x427e44 and n.get(0x2abba94)==5,'actual original map sweep')
    require(n.get(0x2b40f50,'<h')==30,'whole original map queue')
    for i,p in enumerate(room['placements']):
        at=0x2b28f50+i*20
        require([n.get(at,'<i'),n.get(at+4,'<i'),n.get(at+8)]==
                [p['draw_x']+100,p['draw_y']+200,p['bitmapno']],'all thirty actual source map draw requests')
    for b in pack['actors']['bitmaps']:
        row=adrn[b['bitmapno']*80:b['bitmapno']*80+80]
        require(b['source_adrn_index']==b['bitmapno'] and sha(row)==b['record_sha256'],
                'reused source image versus actual original physical ADRN record')
    require(all(f[1:3]==[0,0] for g in pack['actors']['groups'] for a in g['animations'] for f in a['frames']),
            'bounded selected source frame displacement is zero')
    require(struct.unpack_from('<f',exe,0x632f4)[0]==64.0,'original map coordinate scale')
    for i,p in enumerate(room['placements']):
        if p['layer']!='parts':continue
        no=p['bitmapno'];row=adrn[no*80:no*80+80];values=struct.unpack_from('<7i',row)
        require(values[0]==no,'physical index is not original source position')
        at=0x2abba98+len(parts)*44
        require(n.get(at)==no and n.get(at+4,'<i')==p['draw_x']-values[3]+100 and
                n.get(at+8,'<i')==p['draw_y']-values[4]+200,'actual native map node matches source viewport')
        parts.append({'token':i,'kind':'parts','bitmapno':no,'world':[n.get(at+24,'<f'),n.get(at+28,'<f')],
            'source_grid':[p['x'],p['y']],'screen_x':n.get(at+4,'<i'),'screen_y':n.get(at+8,'<i'),
            'footprint':list(row[28:30]),'raw_attribute_word':struct.unpack_from('<H',row,30)[0],
            'original_record_sha256':sha(row)})
    require(len(parts)==5 and all(p['footprint']==[1,1] and p['raw_attribute_word']==0 for p in parts),'fixed room source attribute scope')
    same_axes=all(p['world']==[v*64 for v in p['source_grid']] for p in parts)
    swapped_axes=all(p['world']==[v*64 for v in reversed(p['source_grid'])] for p in parts)
    require(same_axes!=swapped_axes,'unambiguous native coordinate field order')
    groups=pack['actors']['groups'];cases=[]
    configs=[(x,y,100250,0) for y in range(13,18) for x in range(13,18)]
    configs += [(15,15,p,d) for p in [100250,100251,100252] for d in range(8) if (p,d)!=(100250,0)]
    for x,y,pet,direction in configs:
        n.put(0x2abba94,0);n.put(0x2ab1370,0);n.put(0x2b40f50,0,'<h')
        actors=[]
        for i,no in enumerate([100000,pet]):
            group=next(g for g in groups if g['spr_no']==no)
            a=next(a for a in group['animations'] if a['direction']==direction and a['action']==2)
            frame=a['frames'][0];require(frame[1:3]==[0,0],'bounded selected caller frame offset')
            px=(x+y-26)*32+i*32+100;py=(y-x)*24+i*24+200
            world=[x*64,(y+i)*64]
            if swapped_axes:world.reverse()
            ptr=0x4006000+i*0x400
            for off,value,fmt in [(0x98,frame[0],'<I'),(0x18,px,'<i'),(0x1c,py,'<i'),(0x110,world[0],'<f'),(0x114,world[1],'<f')]:n.put(ptr+off,value,fmt)
            n.u.reg_write(UC_X86_REG_ESI,ptr);n.u.reg_write(UC_X86_REG_ESP,n.stack)
            n.u.emu_start(0x407467,0x407493,count=200000)
            require(n.u.reg_read(UC_X86_REG_EIP)==0x407493,'original caller fragment did not finish')
            actors.append({'token':'human' if i==0 else 'pet','kind':'actor','bitmapno':frame[0],
                           'world':world,'screen_x':px,'screen_y':py})
        for p in parts:
            bits=lambda v:struct.unpack('<I',struct.pack('<f',v))[0]
            n.call(0x42a936,(p['bitmapno'],p['screen_x'],p['screen_y'],0,0,*map(bits,p['world'])))
        require(n.get(0x2abba94)==7,'two injected actors and five original parts')
        ptr=n.get(0x2ab1370);linked=[]
        for _ in range(7):
            require(ptr and (ptr-0x2abba98)%44==0,'bounded native list occurrence')
            linked.append((ptr-0x2abba98)//44);ptr=n.get(ptr+0x28)
        require(ptr==0 and sorted(linked)==list(range(7)),'no lost or repeated native list nodes')
        tokens=['human','pet']+[p['token'] for p in parts]
        actual=[tokens[i] for i in linked];require(actual==reference_list(actors,parts),'native list versus independent finite room rule')
        for p in room['placements'][:25]:
            no=p['bitmapno'];xo,yo=struct.unpack_from('<ii',adrn,no*80+12)
            n.call(0x44c974,(p['draw_x']-xo+100,p['draw_y']-yo+200,0,no,0))
        n.call(0x42ac03);require(n.get(0x2b40f50,'<h')==32,'full controlled display queue count')
        entries=[]
        ordered_tokens=list(range(25))+actual
        expected_nodes=list(room['placements'][:25])+[next(z for z in actors+parts if z['token']==t) for t in actual]
        for qi,(token,node) in enumerate(zip(ordered_tokens,expected_nodes)):
            base=0x2b28f50+qi*20;priority=n.get(0x2b3cf52+qi*4,'<B');bitmap=n.get(base+8)
            require(priority==(0 if qi<25 else 10) and bitmap==node['bitmapno'],'original queue priority and physical source frame')
            xo,yo=struct.unpack_from('<ii',adrn,bitmap*80+12)
            expected_xy=[node['draw_x']+100,node['draw_y']+200] if qi<25 else [node['screen_x']+xo,node['screen_y']+yo]
            require([n.get(base,'<i'),n.get(base+4,'<i')]==expected_xy,'actual source draw coordinate and ADRN offsets')
            entries.append({'queue_no':qi,'priority':priority,'token':token,'bitmapno':bitmap,'x':n.get(base,'<i'),'y':n.get(base+4,'<i')})
        n.call(0x44c4a3);order=[n.get(0x2b3cf50+i*4,'<h') for i in range(32)]
        require(order==[r['queue_no'] for r in display_order(entries)],'original sorter versus bounded source reference')
        cases.append({'anchor':[x,y],'pet_spr':pet,'direction':direction,'actors':actors,
                      'native_linked_tokens':actual,'native_draw_tokens':[entries[i]['token'] for i in order],
                      'native_sorted_queue_numbers':order,'queue_entries':entries})
    return {'schema':'stoneage.controlled_actor_parts_order.r9','program_sha256':EXE_SHA,
        'original_ADRN_sha256':sha(adrn),'original_map_sha256':sha(mapraw),'original_R8_html_sha256':R8_SHA,
        'original_map_sweep_executed':True,'source_coordinate_field_order':'YX' if swapped_axes else 'XY',
        'map_world_scale':{'source_va':0x4632f4,'float_value':64.0,'sha256':sha(exe[0x632f4:0x632f8])},
        'all_30_native_map_requests_match_R8':True,'all_208_source_actor_ADRN_records_match_R8':True,
        'selected_source_frame_displacements_zero':True,
        'source_spans':{k:{'start_va':a,'end_va_exclusive':b,'sha256':sha(exe[a-0x400000:b-0x400000])} for k,(a,b) in SPANS.items()},
        'original_parts':parts,'cases':cases,'case_count':len(cases),
        'native_actor_caller_fragment_executed':True,'native_linked_insert_getters_and_sorter_executed':True,
        'native_functions_stubbed':[],'source_ADRN_array_injected':True,'actor_structures_and_coordinates_injected':True,
        'actor_then_parts_phase_order_injected':True,'complete_original_frame_phase_order_proven':False,
        'native_GPU_blit_executed':False,'original_client_launched':False,'original_world_entered':False,
        'official_species_identity_authenticated':False,'same_deployed_build_proven':False,
        'scope':'CONTROLLED_TWO_ACTORS_FIVE_PARTS_1X1_MODE0_NOT_LIVE_GAME',
        'stage_a':'7_PARTIAL_2_OPEN','stage_b':'GATED','r79':'PAUSED_NON_BLOCKING','overall_completion_percent':None}

def export(exe_file,adrn_file,map_file,html_file,target):
    raw=html_file.read_bytes();require(sha(raw)==R8_SHA,'private immutable R8')
    pack=json.loads(raw.decode().split('<script id="evidence" type="application/json">')[1].split('</script>')[0])
    target=target.resolve();require(target!=ROOT and ROOT not in target.parents and not target.exists(),'new private output outside Git')
    report=replay(exe_file.read_bytes(),adrn_file.read_bytes(),map_file.read_bytes(),pack)
    target.mkdir(mode=0o700,parents=True)
    (target/'source-derived-report.json').write_text(json.dumps(report,indent=2)+'\n')
    pack['actor_order_evidence']=report
    template=(ROOT/'tools/scene-room-order-viewer-r9.html').read_text()
    (target/'stoneage-room-r9-order-observer.html').write_text(template.replace('"PRIVATE_PACK_PLACEHOLDER"',json.dumps(pack,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('exe',type=Path);p.add_argument('adrn',type=Path);p.add_argument('map',type=Path);p.add_argument('html',type=Path);p.add_argument('output',type=Path);a=p.parse_args();r=export(a.exe,a.adrn,a.map,a.html,a.output);print(json.dumps({'case_count':r['case_count'],'scope':r['scope'],'original_world_entered':False}))
