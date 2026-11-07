"""Private source observation of all motions of the twelve CHAR02 body candidates."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
from tools import stoneage_pet15_tw10_full_motion as motion

ROOT=motion.ROOT
PRIOR=motion.RECOVERED/'STONEAGE-CHARACTER-NPC-MODULE-02-TW1-12-ACTOR-ACTION2-RECEIPT-R1.json'
PRIOR_BLOB='ea65572a4bb9cd826f5b5b7c7289ce9b0878783e'
REPORT=motion.RECOVERED/'STONEAGE-CHAR10-TW10-TWELVE-BODY-ALL-MOTION-R1.json'


def selected():
    raw=PRIOR.read_bytes()
    motion.need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==PRIOR_BLOB,'CHAR02 source receipt drift')
    old=json.loads(raw)['original_source_groups']
    groups=motion.selected_motion([x[0] for x in old])
    expected={x[0]:(x[1],x[2]) for x in old}
    motion.need(len(groups)==len(expected)==12,'CHAR02 original selection changed')
    for g in groups:
        motion.need((g['group_index'],g['segment_sha256'])==expected[g['graphic']],'CHAR02 original SPR segment changed')
        g.pop('mixed25_same_number_rows')
        g.pop('prior_pet07')
    return groups


def observer(groups,receipts):
    model={'groups':groups,'bitmaps':receipts}
    encoded=json.dumps(model,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c')
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' file:; script-src 'unsafe-inline'; style-src 'unsafe-inline'">
<title>CHAR10 台湾1.0原人物候选：全部源动作</title><style>
body{max-width:1000px;margin:28px auto;padding:0 20px;background:#182125;color:#e2e7e5;font:16px system-ui}
select,button,input{font:inherit;margin:8px;padding:5px}img{image-rendering:pixelated;max-width:100%;min-height:80px}
.stage{min-height:260px;display:grid;place-items:center;background:repeating-conic-gradient(#263439 0 25%,#304147 0 50%) 0/24px 24px}
pre{white-space:pre-wrap}label{display:inline-block}</style><h1>台湾1.0原人物候选 · 全动作查阅</h1>
<p>十二个源SPR数字候选。不是已认证的官方人物名单。动作码、方向和duration保留原数字；配色、倒行、透明处理是观察候选，没有原游戏运行证明。完整解压后打开。</p>
<label>图号<select id="graphic"></select></label><label>源动作<select id="action"></select></label><label>源方向<select id="direction"></select></label>
<div><button id="prev">上一帧</button><input type="range" id="frame" min="0" value="0"><button id="next">下一帧</button><button id="play">播放 / 暂停</button></div>
<p>播放使用现代查阅间隔180毫秒，不是源duration单位或原生速度。原偏移和声音word只显示数值，不播放声音。</p>
<div class="stage"><img id="picture" alt="源位图候选"></div><pre id="info"></pre><script id="source" type="application/json">'''+encoded+'''</script><script>
const D=JSON.parse(document.getElementById('source').textContent),$=id=>document.getElementById(id);let timer=null;
function group(){return D.groups.find(g=>g.graphic===Number($('graphic').value))}
function sequence(){return group().sequences.find(s=>s.action===Number($('action').value)&&s.direction===Number($('direction').value))}
function options(id,values){$(id).replaceChildren(...values.map(v=>new Option(v,v)))}
function render(){const g=group(),s=sequence(),i=Number($('frame').value),f=s.frames[i],b=D.bitmaps[String(f[0])];$('picture').hidden=!b.candidate_png_sha256;if(b.candidate_png_sha256)$('picture').src='images/'+f[0]+'.png';else $('picture').removeAttribute('src');$('info').textContent=JSON.stringify({graphic:g.graphic,source_animation_index:s.index,direction:s.direction,action:s.action,frame:i+1,frames:s.frame_count,duration_raw:s.duration,bitmap:f[0],offset_x_raw:f[1],offset_y_raw:f[2],sound_word_raw:f[3],pixel_status:b.status},null,2)}
function choose(){const s=sequence();$('frame').max=s.frames.length-1;$('frame').value=0;render()}
function selectGroup(){options('action',[...new Set(group().sequences.map(s=>s.action))].sort((a,b)=>a-b));options('direction',[...new Set(group().sequences.map(s=>s.direction))].sort((a,b)=>a-b));choose()}
function step(n){$('frame').value=(Number($('frame').value)+n+sequence().frames.length)%sequence().frames.length;render()}
options('graphic',D.groups.map(g=>g.graphic));$('graphic').onchange=selectGroup;$('action').onchange=choose;$('direction').onchange=choose;$('frame').oninput=render;$('prev').onclick=()=>step(-1);$('next').onclick=()=>step(1);$('play').onclick=()=>{if(timer){clearInterval(timer);timer=null}else timer=setInterval(()=>step(1),180)};selectGroup();</script></html>'''


def export(source_zip,target):
    target=target.resolve()
    motion.need(ROOT not in target.parents and not target.exists(),'private output must be new and outside Git')
    groups=selected();wanted={n for g in groups for n in motion.frames_of(g)}
    with tempfile.TemporaryDirectory() as tmp,zipfile.ZipFile(target,'x') as out:
        work=Path(tmp);motion.extract_spr(source_zip,work)
        receipts=motion.write_bitmaps(work,wanted,out)
        out.writestr('CHAR10.html',observer(groups,receipts),compress_type=zipfile.ZIP_DEFLATED)
        out.writestr('private-pixel-receipts.json',json.dumps(receipts,sort_keys=True),compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(target) as z:motion.need(z.testzip() is None,'private output CRC')
    prior_action2={f[0] for g in groups for s in g['sequences'] if s['action']==2 for f in s['frames']}
    motion.need(len(prior_action2)==576,'CHAR02 source action2 bitmap scope changed')
    missing={n:r['status'] for n,r in receipts.items() if 'indices_sha256' not in r}
    return {'schema':'stoneage.char10.tw10_twelve_body_all_motion.r1',
      'source_scope':'TW10_RETAIL_CHAR02_TWELVE_NUMERIC_BODY_CANDIDATES_NOT_OFFICIAL_ROSTER',
      'source_archive_bytes':motion.ZIP_BYTES,'source_archive_sha256':motion.ZIP_SHA,
      'source_members':motion.SOURCE_MEMBERS,
      'selection_prior_git_blob':PRIOR_BLOB,
      'groups':motion.motion_summary(groups,missing),
      'source_sequences':sum(len(g['sequences']) for g in groups),
      'source_frame_positions':sum(len(motion.frames_of(g)) for g in groups),
      'distinct_original_bitmaps':len(wanted),'prior_char02_action2_bitmap_scope':len(prior_action2),
      'additional_bitmap_scope_beyond_char02':len(wanted-prior_action2),
      'source_bitmap_statuses':dict(Counter(r['status'] for r in receipts.values())),
      'unrendered_bitmaps':missing,
      'bounded_bitmaps':[n for n,r in receipts.items() if r['status']==motion.BOUNDED],
      'actual_pixel_receipts_sha256':motion.sha(json.dumps(receipts,sort_keys=True).encode()),
      'private_zip_bytes':target.stat().st_size,'private_zip_sha256':hashlib.file_digest(target.open('rb'),'sha256').hexdigest(),
      'boundaries':{k:False for k in ['official_twelve_character_roster_verified','source_action_names_inferred','source_duration_unit_verified',
        'native_palette_verified','original_game_executed','proprietary_images_in_git','all_historical_actors_restored']}}


def main():
    p=argparse.ArgumentParser();p.add_argument('source_zip',type=Path);p.add_argument('private_zip',type=Path);args=p.parse_args()
    report=export(args.source_zip,args.private_zip);REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['groups','source_members']},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
