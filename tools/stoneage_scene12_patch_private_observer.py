"""Patch only the SHA-qualified PRIVATE R10 HTML. Never commit generated HTML."""
import argparse,hashlib
from pathlib import Path
SOURCE_LEN=1150992
SOURCE_SHA='00e7565587e009c3e44bcffa1523ab4018886d637aaef1e04749dc01637628d4'
BEFORE="""const chosen=pack.actor_order_evidence.cases.find(c=>c.anchor[0]===state.x&&c.anchor[1]===state.y&&c.pet_spr===100250&&c.direction===0);
if(!chosen)throw Error('缺少当前锚点的原片段见证');
const order=by('nativeOrder').checked?chosen.native_draw_tokens:[...room.R6_native_sorted_queue_numbers,'human','pet'];"""
AFTER="""const witness=pack.actor_order_evidence.cases.find(c=>c.anchor[0]===state.x&&c.anchor[1]===state.y&&c.pet_spr===state.petNo&&c.direction===state.direction);
const hseq=sequence(pack.actors.groups[0]),pseq=sequence(petGroup());
const humanBitmap=hseq.frames[state.frame%hseq.frames.length][0],petBitmap=pseq.frames[state.frame%pseq.frames.length][0];
const exact=!!witness&&witness.actors[0].bitmapno===humanBitmap&&witness.actors[1].bitmapno===petBitmap;
state.witnessKind=exact?'EXACT_CONTROLLED_R9_NOT_LIVE_RUNTIME':witness?'SOURCE_FRAME_DIFFERS_FROM_R9_CASE':'NO_CONTROLLED_R9_CASE';
state.drawOrderKind=by('nativeOrder').checked&&exact?'CONTROLLED_CASE_R9':'MODERN_FALLBACK_ACTORS_AFTER_MAP';
const order=state.drawOrderKind==='CONTROLLED_CASE_R9'?witness.native_draw_tokens:[...room.R6_native_sorted_queue_numbers,'human','pet'];"""

def patch(source):
    if len(source)!=SOURCE_LEN or hashlib.sha256(source).hexdigest()!=SOURCE_SHA:
        raise ValueError('private observer SHA/size mismatch')
    s=source.decode('utf-8')
    if s.count(BEFORE)!=1:raise ValueError('original one-off selector missing')
    s=s.replace(BEFORE,AFTER)
    old='原完整帧调度已认证:false,颜色:'
    if s.count(old)!=1:raise ValueError('original status boundary missing')
    s=s.replace(old,'受控R9见证范围:state.witnessKind,实际选用队列:state.drawOrderKind,原完整帧调度已认证:false,颜色:')
    s=s.replace('原片段插序候选（实验注入）','同一状态有证据才使用受控插序')
    s=s.replace('石器时代 · 帧阶段与地图取整观察 R10','石器时代 · 场景观察 R12｜严格区分受控证据与模拟')
    s=s.replace('石器时代｜帧阶段与地图取整观察 R10','石器时代｜场景观察 R12（受控证据范围修订）')
    s=s.replace('const state={scale:',"const state={witnessKind:'NOT_EVALUATED',drawOrderKind:'NOT_EVALUATED',scale:")
    note='<p class="fine" id="scopeNotice">R12：仅在锚点、宠物图号、方向、人物及宠物当前图号与R9受控案例完全一致时，使用对应的受控排序。其他状态明确回退人工顺序；不构成原游戏播放、原人物走路或真实遮挡证明。</p>'
    s=s.replace('<div class="layout"><section>',note+'<div class="layout"><section>',1)
    return s.encode('utf-8')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('private_r10',type=Path)
    ap.add_argument('private_r12',type=Path)
    a=ap.parse_args()
    result=patch(a.private_r10.read_bytes())
    a.private_r12.write_bytes(result)
    print('Private derived viewer SHA256:',hashlib.sha256(result).hexdigest(),'bytes:',len(result),'DO NOT PUSH')
if __name__=='__main__':main()
