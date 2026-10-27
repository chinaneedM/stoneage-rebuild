"""Source-qualified PRIVATE recovered25 map-ID to ADRN/REAL indexed art probe.
Only creates source-index grayscale PNGs outside public Git. NOT an original game scene.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="stoneage.private_recovered25_scene_graphic_join.r1"
ADRN_SIZE=18765120
ADRN_SHA="92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74"
REAL_SIZE=763908374
REAL_SHA="c7640643804d550bc07e33661103fb7b5f557ee01e68a5a5d92382c5305c2b0d"
MAX_SOURCE_IDS=16
MAX_PIXELS=8000000

def sha_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1048576),b""):
            h.update(block)
    return h.hexdigest()

def authenticate(path:Path,size:int,sha:str)->None:
    if not path.is_file() or path.stat().st_size!=size or sha_file(path)!=sha:
        raise ValueError("source size/SHA256 mismatch: "+path.name)

def requires_mapping(n:int)->bool:
    # Established recovered collision coverage domain; NOT a verified draw selector.
    return type(n) is int and (n>99 or 60<=n<=79)

def resolve_ids(adrn:bytes,ids:set[int],real_length:int)->dict[int,list[dict]]:
    if len(adrn)%80: raise ValueError("ADRN 80-byte alignment failed")
    if not ids or len(ids)>MAX_SOURCE_IDS or any(not requires_mapping(n) or n>65535 for n in ids):
        raise ValueError("select one to sixteen bounded map-ID candidates")
    out={n:[] for n in sorted(ids)}
    for off in range(0,len(adrn),80):
        row=adrn[off:off+80]
        map_number=struct.unpack_from("<I",row,76)[0]
        if map_number not in out: continue
        bitmap,start,length,xoff,yoff,width,height=struct.unpack_from("<IIIiiii",row,0)
        if length<16 or start>real_length or length>real_length-start:
            raise ValueError("ADRN points outside authenticated REAL")
        out[map_number].append({
            "index":off//80,"map_number":map_number,"bitmapno":bitmap,
            "offset":start,"size":length,"xoff":xoff,"yoff":yoff,
            "width":width,"height":height,
            "source_record_sha256":hashlib.sha256(row).hexdigest()})
    return out

def _chunk(tag:bytes,data:bytes)->bytes:
    payload=tag+data
    return struct.pack(">I",len(data))+payload+struct.pack(">I",zlib.crc32(payload)&0xffffffff)

def gray_png(pixels:bytes,w:int,h:int)->bytes:
    if not (0<w<=8192 and 0<h<=8192 and w*h==len(pixels)<=MAX_PIXELS):
        raise ValueError("unbounded indexed image")
    scan=b"".join(b"\0"+pixels[y*w:(y+1)*w] for y in range(h))
    header=struct.pack(">IIBBBBB",w,h,8,0,0,0,0)
    return (b"\x89PNG\r\n\x1a\n"+_chunk(b"IHDR",header)+
        _chunk(b"tEXt",b"Comment\0PALETTE INDICES AS GRAYSCALE - NOT ORIGINAL SCENE COLORS")+
        _chunk(b"IDAT",zlib.compress(scan,9))+_chunk(b"IEND",b""))

def join(materialized,adrn_bytes:bytes,real_path:Path,*,decode=None,
         expected_adrn:tuple[int,str]=(ADRN_SIZE,ADRN_SHA),
         expected_real:tuple[int,str]=(REAL_SIZE,REAL_SHA))->tuple[dict,list[tuple[str,bytes]]]:
    from tools.stoneage_rd_codec import decode_rd_block
    decoder=decode or decode_rd_block
    if len(adrn_bytes)!=expected_adrn[0] or hashlib.sha256(adrn_bytes).hexdigest()!=expected_adrn[1]:
        raise ValueError("ADRN authenticated source SHA mismatch")
    authenticate(real_path,*expected_real)
    area,request=materialized.payload,materialized.request
    provenance=dict(materialized.provenance)
    if (request.world_profile!="recovered25" or
        provenance.get("world_profile")!="recovered25" or
        provenance.get("evidence_role")!="LATER_RECOVERED" or
        provenance.get("content_role")!="LATER_RECOVERED" or
        provenance.get("payload_sha256")!=area.payload_sha256 or
        provenance.get("payload_kind")!=area.source_kind or
        provenance.get("event_plane_status")!=area.event_plane_status or
        any(getattr(request,k)!=getattr(area,k) for k in ("floor_id","x1","x2","y1","y2"))):
        raise ValueError("map provenance or region request mismatch")
    if not (0<=area.x1<=area.x2<area.map_width and 0<=area.y1<=area.y2<area.map_height):
        raise ValueError("region bounds exceeded")
    width=area.x2-area.x1+1
    height=area.y2-area.y1+1
    if not (1<=width<=64 and 1<=height<=64) or len(area.tile_ids)!=width*height or len(area.object_ids)!=width*height:
        raise ValueError("invalid bounded region cell count")
    client=area.source_kind=="CLIENT_DAT_THREE_PLANE" and area.event_plane_status=="RECOVERED_CLIENT_DAT"
    server=area.source_kind=="SERVER_LS2MAP_TWO_PLANE" and area.event_plane_status=="ABSENT_IN_LS2MAP_WORLD_EVENT_LAYER_SEPARATE"
    if not (client or server) or (client and (area.event_ids is None or len(area.event_ids)!=width*height)) or (server and area.event_ids is not None):
        raise ValueError("client/server event plane integrity failed")
    for values in (area.tile_ids,area.object_ids,area.event_ids or ()):
        if any(type(n) is not int or not 0<=n<=65535 for n in values):
            raise ValueError("invalid uint16 map-plane ID")
    ids=set(n for n in (*area.tile_ids,*area.object_ids) if requires_mapping(n))
    if not ids or len(ids)>MAX_SOURCE_IDS:
        raise ValueError("region has no map ID or too many source image IDs; reduce viewport")
    candidates=resolve_ids(adrn_bytes,ids,real_path.stat().st_size)
    files=[]
    resources=[]
    with real_path.open("rb") as real:
        for map_id,records in candidates.items():
            evidence={"map_id":map_id,"occurrences":records,"rendered_artwork":False,"status":"OPEN"}
            if not records:
                evidence["status"]="SOURCE_ADRN_MAPPING_MISSING"
            elif len(records)!=1:
                evidence["status"]="DUPLICATE_ADRN_MAP_NUMBER_SELECT_RULE_OPEN"
            else:
                record=records[0]
                w,h=record["width"],record["height"]
                if not (0<w<=8192 and 0<h<=8192 and w*h<=MAX_PIXELS):
                    evidence["status"]="SPECIAL_OR_OVERSIZED_IMAGE_NOT_RENDERED"
                else:
                    real.seek(record["offset"])
                    block=real.read(record["size"])
                    if len(block)!=record["size"]: raise ValueError("short original RD block")
                    header,pixels=decoder(block,authoritative_block_size=record["size"])
                    if (header["width_s"],header["height_s"])!=(w,h):
                        raise ValueError("ADRN/RD dimensions disagree")
                    png=gray_png(pixels,w,h)
                    name=f"map-id-{map_id:05}.png"
                    files.append((name,png))
                    evidence.update({"status":"PRIVATE_INDEXED_PIXEL_PREVIEW_ONLY",
                        "rendered_artwork":True,"filename":name,
                        "rd_block_sha256":hashlib.sha256(block).hexdigest(),
                        "decoded_palette_indices_sha256":hashlib.sha256(pixels).hexdigest(),
                        "private_grayscale_png_sha256":hashlib.sha256(png).hexdigest()})
            resources.append(evidence)
    report={"schema":SCHEMA,"source_profile":"LATER_RECOVERED",
        "source_bundle_role":"RECOVERED25_PRESERVED_UNVERIFIED_OFFICIAL_RELEASE",
        "original_client_executed":False,"original_world_entered":False,
        "authentic_scene_rendered":False,"scene_projection_verified":False,
        "palette_selection_verified":False,"alpha_semantics_verified":False,
        "collision_lookup_not_draw_selection":True,
        "source_adrn_sha256":expected_adrn[1],"source_real_sha256":expected_real[1],
        "source_pins_are_project_official":(
            expected_adrn==(ADRN_SIZE,ADRN_SHA) and expected_real==(REAL_SIZE,REAL_SHA)),
        "source_map_payload_sha256":area.payload_sha256,
        "source_kind":area.source_kind,"event_plane_status":area.event_plane_status,
        "floor_id":area.floor_id,"viewport_inclusive":[area.x1,area.y1,area.x2,area.y2],
        "map_plane_cell_count":width*height,
        "map_ids_required":sorted(ids),"resources":resources,"preview_count":len(files),
        "private_pngs_are_original_index_data_not_original_game_capture":True,
        "interface_language":"zh-CN"}
    return report,files

def export_private(target:Path,report:dict,files:list[tuple[str,bytes]])->Path:
    target=Path(target).expanduser().resolve()
    if target==ROOT or ROOT in target.parents or not target.is_dir() or any(target.iterdir()):
        raise ValueError("private export must be empty directory outside public repository")
    if len(files)>MAX_SOURCE_IDS or len(files)!=report["preview_count"]:
        raise ValueError("export count mismatch")
    try:
        for name,raw in files:
            if not re.fullmatch(r"map-id-\d{5}\.png",name) or not raw.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("unsafe private artwork filename or content")
            with (target/name).open("xb") as f:f.write(raw)
        with (target/"source-manifest.json").open("x",encoding="utf-8") as f:
            json.dump(report,f,ensure_ascii=False,indent=2)
            f.write("\n")
    except BaseException:
        for name,_ in files:(target/name).unlink(missing_ok=True)
        (target/"source-manifest.json").unlink(missing_ok=True)
        raise
    return target/"source-manifest.json"

def main():
    p=argparse.ArgumentParser(description="PRIVATE recovered25 map-ID to source artwork index probe, NOT gameplay capture")
    for name in ("client-dat-dir","server-map-root","adrn","real","output-dir"):
        p.add_argument("--"+name,type=Path,required=True)
    for name in ("floor","x1","y1","x2","y2"):
        p.add_argument("--"+name,type=int,required=True)
    a=p.parse_args()
    if not (0<=a.x1<=a.x2 and 0<=a.y1<=a.y2 and a.x2-a.x1<64 and a.y2-a.y1<64):
        raise ValueError("invalid viewport")
    from tools.stoneage_local_runtime_core import WorldRegionRequest,load_runtime_bootstrap_file
    from tools.stoneage_recovered25_world_profile_adapter import Recovered25WorldProfileAdapter
    from tools.stoneage_recovered25_region_payload import Recovered25RegionPayloadSource
    profile=load_runtime_bootstrap_file(ROOT/"game/RUNTIME-BOOTSTRAP-RECOVERED25-R1.json")
    adapter=Recovered25WorldProfileAdapter.from_repository(profile)
    source=Recovered25RegionPayloadSource(profile=profile,adapter=adapter,
        client_dat_dir=a.client_dat_dir,server_map_root=a.server_map_root)
    region=source.materialize_region(WorldRegionRequest(
        floor_id=a.floor,x1=a.x1,y1=a.y1,x2=a.x2,y2=a.y2,world_profile="recovered25"))
    report,images=join(region,a.adrn.read_bytes(),a.real)
    output=export_private(a.output_dir,report,images)
    print("PRIVATE_RECOVERED25_SOURCE_IMAGE_CONTACT_PROBE="+str(output))
    print("ORIGINAL_TILE_ARTWORK_LAYOUT_PALETTE_ALPHA_GAMEPLAY=NOT_VERIFIED")

if __name__=="__main__":main()
