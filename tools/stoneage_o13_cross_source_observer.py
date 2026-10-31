"""O13 private offline source-separated pet-animation observer.

No proprietary assets in the program. Original images are taken only from a
privately furnished O11 archive; public crosswalk cites separately preserved
community server text and original Taiwanese retail client animation metadata.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
import re
from zipfile import ZipFile, ZIP_DEFLATED


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_source_animation(o11: ZipFile):
    old_html = o11.read('O11-private-self-contained.html').decode('utf-8')
    match = re.search(r'const S=(\{.*?\});let seq=', old_html, re.S)
    if not match:
        raise ValueError('old observer sequence source missing')
    return json.loads(match.group(1))


def build(o11_zip: Path, report: dict, dest: Path, p3h_zip: Path|None=None):
    assert report['schema'] == 'stoneage.o13.cross_source_original_sprite_named_observer.r1'
    if report['official_tw1_species_join_proven'] or report['historical_game_runtime_executed']:
        raise ValueError('forbidden evidence promotion')
    if p3h_zip is not None:
        if sha(p3h_zip.read_bytes()) != report['tw1_original_archive_sha256']:
            raise ValueError('TW1 private original archive digest mismatch')
        with ZipFile(p3h_zip) as original:
            if len(original.namelist()) != 379:
                raise ValueError('unexpected P3H inventory')
            for member, digest in report['original_tw1_member_sha256'].items():
                if sha(original.read(member)) != digest:
                    raise ValueError(f'original source SHA mismatch: {member}')
    if sha(o11_zip.read_bytes()) != report['o11_private_archive_sha256']:
        raise ValueError('O11 private archive identity mismatch')

    with ZipFile(o11_zip) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP CRC failed')
        witness = json.loads(z.read('O11-PRIVATE-SOURCE-REPLAY.json'))
        seqs = load_source_animation(z)
        raw = seqs['groups']
        expected = witness['cross_sample_action0']['all_24_source_animation_records']
        digest_by_anim = {(x['spr_no'],x['direction']):x['source_animation_span_sha256'] for x in expected}
        by_num = {(x['spr_no'],x['direction']):x for x in raw}
        if len(raw)!=24 or len(digest_by_anim)!=24 or len(by_num)!=24:
            raise ValueError('exactly 24 original source sequences required')
        if set(by_num) != set(digest_by_anim):
            raise ValueError('animation direction mismatch')
        original_positions = sum(len(x['frames']) for x in raw)
        if original_positions != 352:
            raise ValueError('original ordered frame occurrences must remain 352')
        pngs = witness['private_preserved_png_sha256']
        referenced = {str(f[0]) for seq in raw for f in seq['frames']}
        if len(referenced)!=208 or set(pngs)!=referenced:
            raise ValueError('208 distinct original PNG identity mismatch')
        for s in raw:
            if s['source_animation_span_sha256']!=digest_by_anim[(s['spr_no'],s['direction'])]:
                raise ValueError('source animation digest mismatch')
            recorded=[{'frame_index':i,'source_word':f[3]} for i,f in enumerate(s['frames']) if f[3]]
            exp=next(x for x in expected if x['spr_no']==s['spr_no'] and x['direction']==s['direction'])
            if recorded!=exp['nonzero_frame_source_words']:
                raise ValueError('nonzero source words mismatch')
        image_urls={}
        for n in sorted(referenced,key=int):
            raw_png=z.read(f'original-private-png/{n}.png')
            if sha(raw_png)!=pngs[n]:
                raise ValueError(f'original PNG mutated: {n}')
            image_urls[n]='data:image/png;base64,'+base64.b64encode(raw_png).decode('ascii')
        rows=report['server_occurrences']
        if [r['original_server_line'] for r in rows] != [1,2,3,6,407,479,858]:
            raise ValueError('seven original server occurrence positions must remain intact')
        expected_groups={100250,100251,100252}
        if {r['graphic_column_37'] for r in rows}!=expected_groups:
            raise ValueError('wrong source graphic namespace')
        if any('original_server_line' not in r or 'original_row_sha256' not in r for r in rows):
            raise ValueError('original row custody missing')
        if any(r['graphic_column_37'] not in {s['spr_no'] for s in raw} for r in rows):
            raise ValueError('server graphic cannot be matched to original group')
        occ_by_group={str(i):[] for i in sorted(expected_groups)}
        for r in rows:
            occ_by_group[str(r['graphic_column_37'])].append({'line':r['original_server_line'], 'template':r['template_column_7'], 'flag':r['flag_column_38']})
        if [x['flag'] for x in occ_by_group['100252']] != [1,1,1,0]:
            raise ValueError('do not flatten source flag conflict')
        vis={str(x): {'name': next(r['name_zh_Hant'] for r in rows if r['graphic_column_37']==x), 'occurrences': occ_by_group[str(x)]} for x in sorted(expected_groups)}
        view_model={'sprites':raw,'images':image_urls,'named_later_community':vis}
        script_data=json.dumps(view_model,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
        source_hash=sha(z.read('O11-PRIVATE-SOURCE-REPLAY.json'))

    markup='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>O13 · 原客户端动画 / 后期保存版名称并列观察</title>
<style>body{background:#111723;color:#edf3fd;font:16px system-ui, sans-serif;max-width:1030px;margin:24px auto;padding:0 18px}h1{font-size:24px}p,li{line-height:1.65;color:#c2cdde}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}article{background:#202b3b;border:1px solid #40506a;border-radius:10px;padding:16px}.stage{height:245px;display:grid;place-items:center;border-radius:8px;background:#303b4c;margin:12px 0}.stage img{image-rendering:pixelated;max-width:90%;max-height:220px;object-fit:contain}button,select,input{background:#263c53;border:1px solid #62728d;border-radius:6px;color:#fff;padding:7px;font:inherit}button{cursor:pointer}label{display:inline-flex;gap:8px;align-items:center;margin:7px 0}code{color:#f5d39f}small{color:#afbed0}.alert{border-left:4px solid #e8ac60;padding:8px 14px;background:#322b29}.detail{font-size:13px;line-height:1.7;white-space:pre-wrap;color:#cbd6e7}button:focus-visible,select:focus-visible{outline:2px solid #b1e0fc}</style>
<h1>O13｜原始像素与跨版本具名候选观察</h1><p class="alert">左侧图像、动画帧与动作字段来自已认证台湾 1.0 客户端原资源；繁体宠物名称与模板行来自另一个社区混合 2.5 保存版。两者只通过数字图形键及此前源片段比对联系。<strong>这里不是台湾 1.0 官方宠物命名表，也不是原游戏画面或实际宠物行为执行。</strong></p>
<p>所有图片均从私下保存的原客户端已验原像素生成，直接内嵌、无需联网。每张卡可以查看8个方向及有序帧；不会自动播放声音，不把帧末字段73当作叫声。原程序编译期编号73、声音地址表第73项属于不同命名空间（O12）；具体触发仍未知。</p>
<main id="cards"></main><p><small>证据：台湾 1.0 原 O11 SPR/RD；R39 社区模板第7/37/38列原数字；R40 同保存包三组 SPR 原动画及同内容 TW1 字节对照。源字体颜色/帧率/动作语义并未认证。离线私人研究资料，不是可再发行的原商业美术授权。</small></p>
<script>const D=__DATA__;const cards=document.getElementById('cards');
for(const group of [100250,100251,100252]){let id=String(group),c=D.named_later_community[id],art=document.createElement('article');let name=document.createElement('h2');name.textContent=c.name+' · 图形组 '+id;art.append(name);let origin=document.createElement('p');origin.textContent='名称仅据后期社区模板；台湾1.0原始物种身份未知';art.append(origin);
let dirLabel=document.createElement('label');dirLabel.textContent='原方向序号 ';let sel=document.createElement('select');for(let d=0;d<8;d++){let opt=document.createElement('option');opt.value=d;opt.textContent=String(d);sel.append(opt)}dirLabel.append(sel);art.append(dirLabel);
let stage=document.createElement('div');stage.className='stage';let img=document.createElement('img');img.alt='原 TW1 数字组 '+id+' 的已认证原像素';stage.append(img);art.append(stage);
let bprev=document.createElement('button'),bnext=document.createElement('button');bprev.textContent='上一帧';bnext.textContent='下一帧';art.append(bprev,' ',bnext);let slider=document.createElement('input');slider.type='range';slider.min='0';slider.value='0';slider.setAttribute('aria-label','原有序帧位置');art.append(slider);let info=document.createElement('div');info.className='detail';art.append(info);
let rowInfo=document.createElement('details');let summ=document.createElement('summary');summ.textContent='后期社区版本所有原模板位置（保留重复）';rowInfo.append(summ);let pre=document.createElement('pre');pre.textContent=c.occurrences.map(r=>'行 '+r.line+' / 模板 '+r.template+' / 第38列原标志 '+r.flag).join('\\n');rowInfo.append(pre);art.append(rowInfo);
let idx=0;const current=()=>D.sprites.find(x=>x.spr_no===group&&x.direction===Number(sel.value));function render(){let seq=current();slider.max=String(seq.frames.length-1);slider.value=String(idx);let f=seq.frames[idx];img.src=D.images[String(f[0])];info.textContent='原动作码 '+seq.action+'，方向 '+seq.direction+'\\n原动画序号 '+seq.source_animation_index+'，帧位置 '+idx+'/'+(seq.frames.length-1)+'\\nbitmap '+f[0]+'，偏移 '+f[1]+','+f[2]+'\\n帧末原字段 '+f[3]+'；duration '+seq.duration_word+'（单位未知）';}sel.addEventListener('change',()=>{idx=0;render()});slider.addEventListener('input',()=>{idx=Number(slider.value);render()});bprev.addEventListener('click',()=>{idx=(idx+current().frames.length-1)%current().frames.length;render()});bnext.addEventListener('click',()=>{idx=(idx+1)%current().frames.length;render()});cards.append(art);render();}
</script></html>'''.replace('__DATA__',script_data)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(markup.encode('utf-8'))
    acceptance={
        'schema':'stoneage.o13.private_original_pixel_named_cross_source_acceptance.r1',
        'generated_html_sha256':sha(dest.read_bytes()),
        'generated_html_bytes':dest.stat().st_size,
        'o11_private_source_replay_sha256':source_hash,
        'original_ordered_frame_positions':352,
        'original_source_sequences':24,
        'original_distinct_png':208,
        'server_template_rows':7,
        'community_named_groups':3,
        'new_original_species_claims':0,
        'historical_game_runtime_executed':False,
        'actual_sound_event_selected':False,
        'source_scope':'TW1_PIXEL_AND_ANIMATION__COMMUNITY_MIXED25_NAME_METADATA_NOT_SAME_DEPLOYED_BUILD',
    }
    return acceptance

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--o11-private',required=True,type=Path)
    p.add_argument('--report',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--original-p3h',type=Path)
    a=p.parse_args()
    print(json.dumps(build(a.o11_private,json.loads(a.report.read_text(encoding='utf-8')),a.output,a.original_p3h),ensure_ascii=False,indent=2))
