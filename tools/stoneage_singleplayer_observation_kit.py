"""Single-command PRIVATE offline TW1 original-resource animation and scene-observer kit.

Uses existing fully pinned TW1 original-frame decoders; no client executable or
server is started. Outputs copyrighted reconstructed frames ONLY outside public Git.
The optional modern scene observer is an archaeology overlay, not native gameplay.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from tools.stoneage_original_animation_lab import ROOT, ORIGINALS, timeline, preview, write_private
from tools.stoneage_private_sprite_frame_export_r1 import unpack, export_private

SOURCE_VIEWER=ROOT/"tools/modern-observation-viewer.html"
SCHEMA="stoneage.private_offline_asset_first_observation_kit.r1"
MAX_FRAMES=512

def require(condition,message):
    if not condition: raise ValueError(message)

def sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def safe_directories(original:Path,output:Path):
    repo=ROOT.resolve()
    src=original.expanduser().resolve()
    dest=output.expanduser().resolve()
    require(src.is_dir(),"original TW1 data directory missing")
    require(dest.is_dir() and not dest.is_symlink(),"private output must be an existing real directory")
    require(src!=dest and dest!=repo and repo not in dest.parents and src not in dest.parents,
            "private output overlaps source or public repository")
    require(not any(dest.iterdir()),"private output must be empty: never overwrite evidence")
    require(SOURCE_VIEWER.is_file(),"existing modern offline observer missing")
    return src,dest

def landing_html(sprite_no:int,direction:int,action:int,count:int,scene21:bool=False)->str:
    require(0<count<=MAX_FRAMES and 0<=sprite_no<=10000000 and 0<=direction<=32 and 0<=action<=256,
            "invalid finite original sprite source selection")
    html = ("""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>石器时代｜本机原客户端资源观察</title>
<style>body{background:#152126;color:#e6eff1;font:16px/1.75 system-ui,"Microsoft YaHei",sans-serif;
max-width:820px;margin:48px auto;padding:0 20px}a{color:#a4dcff}section{padding:16px;border:1px solid #536e79;
border-radius:10px;margin:14px 0}small{color:#bacbd1}</style></head><body>
<h1>石器时代 · 原客户端资源单机观察</h1>
<p>本目录由本地已验证的客户端数据导出。无需登录、服务器或旧版游戏联网。</p>
<section><h2>1. 原资源动画</h2>
<p>原 SPR 数字组号 """+str(sprite_no)+"""，方向 """+str(direction)+"""，动作码 """+str(action)+"""，
导出帧位置 """+str(count)+"""。数字码不等于已确认人物或宠物身份。</p>
<a href="animation-original.html">打开真实原资源逐帧动画</a>
</section><section><h2>2. 单机场景观察</h2>
<p>已有本机导出帧：<code>frames/frame-*.png</code>。在场景观察台中手动选择这些PNG，
并加载相邻的 <code>frames/source-manifest.json</code> 校验；
若没有真实地图PNG，仍显示明确标记的人工背景网格。</p>
<a href="modern-observation-viewer.html">打开简体中文离线场景观察台</a>
</section><section><h2>3. 证据清单</h2>
<p><code>kit-receipt.json</code> 和 <code>animation-original.json</code>
记录输入文件、动画序列、导出图像的SHA与取色限制。</p></section>
<small>仅私人研究：非原游戏可操作世界。人工移动、背景网格及帧速不能推断原服务器规则；
未证明游戏内调色板、实体ID、NPC/任务、碰撞或客户端实际选择器。原版权素材勿公开分发。</small>
</body></html>""")
    if scene21:
        html=html.replace("</body>", """<section><h2>4. 已验后期地图原图观察（跨版限定）</h2>
<p>后期mixed25地图1000.DAT、共前缀TW1图形字节；并非已认证TW1官方部署地图，
也不是原版可操作世界。全量图块验证通过才会加入此入口。</p>
<a href="scene-o2/index.html">打开有版本隔离的原图场景</a></section></body>""")
    return html

def emit_kit(original:Path,output:Path,spr_no:int,direction:int,action:int,
             scene21_private:Path|None=None)->dict:
    src,dest=safe_directories(original,output)
    if scene21_private is not None:
        from tools import stoneage_offline_original_map_o2 as map_o2
        # Sources and destination must be disjoint, existing, and private.
        map_o2.safe_directories(scene21_private,dest)
    require(isinstance(spr_no,int) and 0<=spr_no<=10000000 and 0<=direction<=32 and 0<=action<=256,
            "out-of-range original numeric selection")
    # The original parser validates four exact full-file hashes and real
    # underlying RD block membership. The source-owned metadata is also pinned.
    t=timeline(spr_no,direction,action)
    paths={name:src/name for name in ORIGINALS}
    html,custody=preview(t,paths)
    frames=unpack(html,custody)
    require(len(frames)>0 and len(frames)<=MAX_FRAMES,"original animation yielded no bounded frames")
    # Compute plan and immutable provenance before writing anything.
    landing=landing_html(spr_no,direction,action,len(frames),scene21_private is not None)
    viewer=SOURCE_VIEWER.read_bytes()
    require(b"default-src 'none'" in viewer and b"img-src blob:" in viewer,
            "local observation viewer network policy has changed")
    receipt={
        "schema":SCHEMA,"source_profile":"TW_WAEI_JSS_1_0_ACCEPTED_RETAIL_REDUMP_104630",
        "original_files":custody["original_files"],
        "original_source_status":custody["source_status"],
        "original_source_timeline":t,
        "sprite_numeric_selector":{"spr_no":spr_no,"direction":direction,"action":action},
        "derived_source_frame_positions":len(frames),
        "original_source_frame_png_sha256":[sha(raw) for _,raw in frames],
        "private_animation_html_sha256":sha(html.encode("utf-8")),
        "private_observer_html_sha256":sha(viewer),
        "private_entry_html_sha256":sha(landing.encode("utf-8")),
        "original_client_executable_launched":False,
        "historical_server_required_or_contacted":False,
        "network_required":False,
        "in_game_palette_or_fps_verified":False,
        "sprite_entity_name_or_type_verified":False,
        "original_game_world_entered":False,
        "locomotion_collision_quest_or_battle_reconstructed":False,
        "new_game_engine_selected":False,
        "original_copyright_content_committed_to_public_git":False,
        "research_offline_overlay_not_original_game":True,
        "optional_cross_version_original_map_scene":scene21_private is not None,
        "official_TW1_map_deployment_authenticated":False,
        "explicit_next":"PRIVATE_TW1_MAP_SOURCE_QUALIFICATION_IF_AVAILABLE"
    }
    (dest/"frames").mkdir()
    try:
        if scene21_private is not None:
            (dest/"scene-o2").mkdir()
            receipt["cross_version_map_o2_receipt"]=map_o2.emit(scene21_private,dest/"scene-o2")
        export_private(dest/"frames",frames,custody)
        write_private(dest/"animation-original.html",html,custody)
        (dest/"modern-observation-viewer.html").write_bytes(viewer)
        (dest/"index.html").write_text(landing,encoding="utf-8")
        (dest/"kit-receipt.json").write_text(
            json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    except BaseException:
        # This directory was required empty; remove only our own output on failure.
        shutil.rmtree(dest/"frames",ignore_errors=True)
        shutil.rmtree(dest/"scene-o2",ignore_errors=True)
        for n in ("animation-original.html","animation-original.json",
                  "modern-observation-viewer.html","index.html","kit-receipt.json"):
            (dest/n).unlink(missing_ok=True)
        raise
    return receipt

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--original-dir",required=True,type=Path)
    p.add_argument("--output-dir",required=True,type=Path)
    p.add_argument("--spr-no",type=int,default=100000)
    p.add_argument("--direction",type=int,default=0)
    p.add_argument("--action",type=int,default=6)
    p.add_argument("--scene21-private-dir",type=Path,default=None,
                   help="optional verified SCENE21 mixed25 private map; not a TW1 deployed map")
    a=p.parse_args()
    report=emit_kit(a.original_dir,a.output_dir,a.spr_no,a.direction,a.action,a.scene21_private_dir)
    print("PRIVATE_OFFLINE_ORIGINAL_RESOURCE_KIT_CREATED="+str(a.output_dir/"index.html"))
    print("SOURCE_VERIFIED_FRAMES="+str(report["derived_source_frame_positions"]))
    print("NO_HISTORICAL_SERVER_OR_ORIGINAL_GAME_WORLD_EXECUTION")

if __name__=="__main__":main()
