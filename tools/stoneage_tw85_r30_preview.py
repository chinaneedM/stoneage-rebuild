"""R30: select bounded R28-unmatched original animation frames, privately decode actual TW85 RD.

A qualified *same preserved MSI carrier* is not an authenticated clean official
release, original game screenshot, runtime palette or identified pet/character.
This module never publishes originals or a decoded preview without session RSA
public-key encryption. Original packages/pixels live only on ephemeral runner.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse
import base64
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import secrets
import struct
import zipfile

from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_original_observation_lab import gray_png
from tools.stoneage_tw85_spr137_material_r28 import ORIGINALS as SPR_ORIGINALS
from tools.stoneage_tw85_frame_bitmap_r29 import INPUTS as R29_PINS
from tools.stoneage_wayi85_sixpart_acquisition import acquire as acquire_tw85

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research/recovered"
SOURCE=REC/"tw85-spr137-r28/SOURCE-DERIVED-R28.json"
NATIVE=REC/"adrn129-tw85-real-pair/NATIVE-R1.tsv.gz"
SPR_GROUP=REC/"tw85-spr137-r28/SPR-GROUP-R28.tsv.gz"
SPR_ANIM=REC/"tw85-spr137-r28/SPR-ANIMATION-R28.tsv.gz"
SPR_FRAME=REC/"tw85-spr137-r28/SPR-FRAME-R28.tsv.gz"
R29=REC/"tw85-frame-bitmap-r29/REPORT-R29.json"
COMMON=REC/"STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json"
ADRN_ORIGINAL=(33297600,"16ba4fa3825b2c4b6645bab8b4fe3152a262a4789c8bb89e3043a7d3f0d53681")
REAL_ORIGINAL=(1607321502,"e0f9c0d20fd3d9daae0701d8a872c9842e27d3da1be4d449d558c9c76d1c5f5b")
SUBPATH=Path("Program Files/WAYI/石器時代 魔域大冒險/data")
SCOPE="UNVERIFIED_COMMUNITY_PRESERVED_CLAIMED_TW85_SAME_557_FILE_MSI_CARRIER"
MAX_IMAGES=8
PIXEL_LIMIT=256*256
MAX_RD_BYTES=300000


def require(ok,msg):
    if not ok:raise ValueError(msg)


def sha(buf):
    return hashlib.sha256(buf).hexdigest()


def file_sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        while b:=f.read(1024*1024):h.update(b)
    return h.hexdigest()


def items(path):
    with gzip.open(path,"rt",encoding="utf-8",newline="") as stream:
        yield from csv.DictReader(stream,delimiter="\t")


def verified_inputs():
    r28=json.loads(SOURCE.read_bytes())
    r29=json.loads(R29.read_bytes())
    r06=json.loads((REC/"adrn129-tw85-real-pair/REPORT-R1.json").read_bytes())
    manifest=json.loads(COMMON.read_bytes())
    expected={
      "SPR_FRAME":SPR_FRAME,"SPR_GROUP":SPR_GROUP,
      "R06_NATIVE":NATIVE,"R28_SOURCE":SOURCE,"CARRIER":COMMON
    }
    for name,path in expected.items():
        require(file_sha(path)==r29["source_pins"]["R28_FRAME" if name=="SPR_FRAME" else
          "R28_GROUP" if name=="SPR_GROUP" else name]["sha256"],
          "immutable source evidence drift: "+name)
    require(r29["same_saved_carrier_verified_against_full_file_inventory"] if
            "same_saved_carrier_verified_against_full_file_inventory" in r29 else
            r29["boundaries"]["same_saved_carrier_verified_against_full_file_inventory"],
            "same saved source carrier not accepted")
    require(r28["source"]=="TW85-INSTALLER-MSI-CLIENT_UNVERIFIED_COMMUNITY_PRESERVED",
            "historical version claim promoted")
    expected_orig={
       "spradrn_137.bin":SPR_ORIGINALS["spradrn_137.bin"],
       "spr_137.bin":SPR_ORIGINALS["spr_137.bin"],
       "adrn_158.bin":ADRN_ORIGINAL,"real_158.bin":REAL_ORIGINAL
    }
    manifest_files=manifest["inspection"]["inventory"]["samples"][0]["files"]
    require(len(manifest_files)==557,"old original MSI path inventory drift")
    for name,(length,digest) in expected_orig.items():
        source=[r for r in manifest_files if r["path"].endswith("/data/"+name)]
        require(len(source)==1 and source[0]["size"]==length and source[0]["sha256"]==digest,
                "original four-file provenance mismatch: "+name)
    require(r28["pair"]=={name:{"bytes":size,"sha256":digest}
       for name,(size,digest) in SPR_ORIGINALS.items()},
       "old original SPR pair differs")
    require(r06["containers"]["adrn"]["sha256"]==ADRN_ORIGINAL[1] and
            r06["containers"]["real"]["sha256"]==REAL_ORIGINAL[1],
            "old original ADRN REAL pair differs")
    require(r29["frame_mapping_classifications"]=={"SINGLE_ORIGINAL_RD_RECORD":730907},
            "complete same sample material join not accepted")
    return r28,r29


def safe_native_map():
    native=defaultdict(list)
    count=0
    for x in items(NATIVE):
        require(int(x["index"])==count,"native original ADRN position drift")
        native[int(x["bitmapno"])].append(x)
        count+=1
    require(count==416220,"original 416220 RD records lost")
    return native


def candidate(f,a,group,native):
    if not (6<=len(f)<=12 and int(a["frame_count"])==len(f)):return False
    if any(int(x["sentinel"])!=0 or int(x["bmp_no"])==0xffffffff for x in f):return False
    if len({int(x["bmp_no"]) for x in f[:MAX_IMAGES]})<3:return False
    for x in f[:MAX_IMAGES]:
        options=native.get(int(x["bmp_no"]),[])
        if len(options)!=1:return False
        n=options[0]
        if (int(n["width"])<=0 or int(n["height"])<=0
            or int(n["width"])*int(n["height"])>PIXEL_LIMIT
            or int(n["size"])>MAX_RD_BYTES
            or int(n["rd_flag"]) not in (0,1)
            or n["rd_status"] not in ("HEADER_MATCH","HEADER_MISMATCH")):return False
    return True


def plan():
    r28,r29=verified_inputs()
    native=safe_native_map()
    exact={int(x["tw85_index"]) for x in r28["joins"]["reference_relationships"]["CN50"]
           if x["relation"]=="SAME_ID_AND_EXACT_FULL_SPR_SEGMENT"}
    require(len(exact)==1185,"R28 exact reference group category changed")
    groups=list(items(SPR_GROUP))
    require(len(groups)==1739,"R28 grouped source count changed")
    ani=iter(items(SPR_ANIM));frm=iter(items(SPR_FRAME))
    selected=None
    all_anim=all_frames=0
    for index,g in enumerate(groups):
        require(int(g["index"])==index,"R28 group physical order changed")
        for j in range(int(g["anim_count"])):
            a=next(ani);require(int(a["group_index"])==index and int(a["anim_index"])==j,"animation order")
            frames=[next(frm) for _ in range(int(a["frame_count"]))]
            require(all(int(x["group_index"])==index and int(x["anim_index"])==j
                        and int(x["frame_index"])==k for k,x in enumerate(frames)),
                    "original frame position order lost")
            all_anim+=1;all_frames+=len(frames)
            if (selected is None and index not in exact
                and candidate(frames,a,g,native)):
                poses=[]
                for x in frames[:MAX_IMAGES]:
                    n=native[int(x["bmp_no"])][0]
                    poses.append({
                        "index_in_animation":int(x["frame_index"]),
                        "original_spr_frame_offset":int(x["offset"]),
                        "bitmapno":int(x["bmp_no"]),"pos_x":int(x["pos_x"]),
                        "pos_y":int(x["pos_y"]),"raw_sound_word":int(x["sound_no"]),
                        "native_adrn_index":int(n["index"]),"native_adrn_record_sha256":n["record_sha256"],
                        "adder":int(n["adder"]),"size":int(n["size"]),
                        "rd_block_sha256":n["rd_sha256"],"rd_flag":int(n["rd_flag"]),
                        "width":int(n["width"]),"height":int(n["height"])
                    })
                selected={"source_group_index":index,"original_spr_no":int(g["spr_no"]),
                          "source_group_full_spr_segment_sha256":g["segment_sha256"],
                          "original_animation_index":j,
                          "original_direction_numeric":int(a["direction"]),
                          "original_action_numeric":int(a["anim_no"]),
                          "original_duration_word":int(a["duration"]),
                          "original_animation_frame_count":len(frames),"sample_frames":poses}
    require(next(ani,None) is None and next(frm,None) is None,"unconsumed original SPR rows")
    require((all_anim,all_frames)==(113737,735666),"R28 full corpus drift")
    require(selected is not None,"NO_BOUNDED_DECODABLE_SOURCE_ANIMATION")
    return {"schema":"stoneage.tw85_original_private_rd_visual_sample_plan.r30",
            "source_claim":SCOPE,"four_original_files_in_same_verified_inventory":True,
            "source_paths":{"R28":"research/recovered/tw85-spr137-r28/",
                            "R06":"research/recovered/adrn129-tw85-real-pair/",
                            "R29":"research/recovered/tw85-frame-bitmap-r29/"},
            "sample":selected,"original_full_frames_checked":all_frames,
            "original_full_animations_checked":all_anim,
            "selection_rule":"earliest R28 unmatched CN50 SPR original group/animation with 6..12 frames, first up to 8 non-sentinel uniquely indexed, 3 distinct RD keys, <=256*256 pixels/frame",
            "limits":{"original_clean_official_build_proven":False,"same_running_version_proven":False,
                      "palette_rgb_proven":False,"true_sprite_identity_proven":False,
                      "original_game_executed":False,"original_frames_or_colors_published_in_git":False}}


def write_plan(output):
    report=plan()
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","selection":{k:v for k,v in report["sample"].items() if k!="sample_frames"},
                      "bitmapnos":[x["bitmapno"] for x in report["sample"]["sample_frames"]]},sort_keys=True))


def original_check(path,sizehash):
    require(path.is_file() and not path.is_symlink() and path.stat().st_size==sizehash[0],
            "missing/incorrect original actual payload: "+path.name)
    require(file_sha(path)==sizehash[1],"original real file SHA256 mismatch: "+path.name)


def reconstruct(data_root,plan_path,private_dir):
    """Produce private image-only material only after source exact SHA and every RD SHA."""
    data_root=Path(data_root);private_dir=Path(private_dir)
    p=json.loads(Path(plan_path).read_bytes())
    require(p==plan(),"source plan input unexpectedly changed")
    adrn=data_root/"adrn_158.bin";real=data_root/"real_158.bin"
    original_check(adrn,ADRN_ORIGINAL)
    original_check(real,REAL_ORIGINAL)
    manifest={"schema":"stoneage.tw85_original_rd_private_gray_sample.r30",
              "source_claim":SCOPE,"source_primary_paths":["data/adrn_158.bin","data/real_158.bin"],
              "real_original_sha256":REAL_ORIGINAL[1],"adrn_original_sha256":ADRN_ORIGINAL[1],
              "original_spr_pair_already_qualified_at_R28":True,
              "sample":p["sample"],"frames":[],"observer_bounded_result":"ACTUAL_SOURCE_RD_BYTES_DECODED_TO_ORIGINAL_INDEX_VALUES_IN_GRAY_PRIVATE_PREVIEW",
              "historical_palette_rgb_verified":False,
              "original_game_rendered_or_executed":False,
              "named_pet_or_avatar_verified":False,
              "gameplay_sound_event_verified":False}
    private_dir.mkdir(parents=True,exist_ok=True)
    with adrn.open("rb") as af,real.open("rb") as rf:
        for entry in p["sample"]["sample_frames"]:
            af.seek(80*entry["native_adrn_index"])
            raw=af.read(80)
            require(sha(raw)==entry["native_adrn_record_sha256"],"actual source ADRN record sha drift")
            bit,offset,size,_,_,w,h=struct.unpack_from("<IIIiiii",raw)
            require((bit,offset,size,w,h)==tuple(entry[k] for k in
                    ("bitmapno","adder","size","width","height")),"native record/source table differing")
            require(16<=size<=MAX_RD_BYTES and offset+size<=REAL_ORIGINAL[0],
                    "source original RD extent invalid")
            rf.seek(offset)
            block=rf.read(size)
            require(len(block)==size and sha(block)==entry["rd_block_sha256"],
                    "real original RD block differs from R06 prior source SHA")
            header,pixels=decode_rd_block(block,authoritative_block_size=size)
            require((header["width_s"],header["height_s"],header["flag"])==
                    (w,h,entry["rd_flag"]),"actual original RD dimensions/flag differ")
            need_index=entry["index_in_animation"]
            png=gray_png(pixels,w,h)
            name=f"frame_{need_index:02d}_bmp_{bit}.png"
            (private_dir/name).write_bytes(png)
            manifest["frames"].append({"index":need_index,"bitmapno":bit,"source_record_sha256":sha(raw),
                    "source_RD_sha256":sha(block),"source_palette_index_sha256":sha(pixels),
                    "private_png_sha256":sha(png),"private_png_name":name,"width":w,"height":h,
                    "original_sprite_x":entry["pos_x"],"original_sprite_y":entry["pos_y"],
                    "raw_sound_word":entry["raw_sound_word"]})
    require(len(manifest["frames"])==len(p["sample"]["sample_frames"]),
            "incomplete private material reconstruction")
    (private_dir/"PRIVATE-R30.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    return manifest


def sealed_zip(private_dir,public_key_path,cipher_path,envelope_path):
    """AES-GCM encrypted private PNG package, AES key RSA-OAEP wrapped to session public key."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes,serialization
    source=Path(private_dir);files=sorted(source.iterdir())
    require(len(files)>=2 and all(x.is_file() and
          (x.name=="PRIVATE-R30.json" or x.suffix==".png") for x in files),
          "must package only bounded actual verified images and source receipt")
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:archive.write(path,path.name)
    raw=buf.getvalue()
    pub=serialization.load_pem_public_key(Path(public_key_path).read_bytes())
    sym=AESGCM.generate_key(bit_length=256)
    nonce=secrets.token_bytes(12)
    cipher=AESGCM(sym).encrypt(nonce,raw,b"stoneage-r30-original-private-sample")
    key_cipher=pub.encrypt(sym,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                            algorithm=hashes.SHA256(),label=None))
    out=Path(cipher_path);out.write_bytes(cipher)
    metadata={"schema":"stoneage.r30.session_public_key_aes256gcm_encrypted_private_image.r1",
              "ciphertext_bytes":len(cipher),"ciphertext_sha256":sha(cipher),
              "nonce_base64":base64.b64encode(nonce).decode("ascii"),
              "wrapped_key_base64":base64.b64encode(key_cipher).decode("ascii"),
              "associated_data_utf8":"stoneage-r30-original-private-sample",
              "plaintext_zip_sha256":sha(raw),"plaintext_zip_bytes":len(raw),
              "public_source_files_or_unencrypted_original_art_in_artifact":False,
              "private_key_written_to_ci":False}
    Path(envelope_path).write_text(json.dumps(metadata,indent=2,sort_keys=True)+"\n")
    return metadata


def main():
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest="operation",required=True)
    a=sub.add_parser("plan");a.add_argument("--out",type=Path,required=True)
    b=sub.add_parser("material");b.add_argument("--source-work",type=Path,required=True)
    b.add_argument("--plan",type=Path,required=True)
    b.add_argument("--private-dir",type=Path,required=True)
    b.add_argument("--public-key",type=Path,required=True)
    b.add_argument("--cipher",type=Path,required=True)
    b.add_argument("--envelope",type=Path,required=True)
    args=parser.parse_args()
    if args.operation=="plan":write_plan(args.out)
    else:
        work=args.source_work;work.mkdir(parents=True,exist_ok=True)
        acquire_tw85(work,work/"acquisition-R30.json")
        root=work/"msi-client"/SUBPATH
        info=reconstruct(root,args.plan,args.private_dir)
        sealed=sealed_zip(args.private_dir,args.public_key,args.cipher,args.envelope)
        print(json.dumps({"status":"ACTUAL_ORIGINAL_RD_PRIVATE_SAMPLE_VERIFIED",
                          "sample_bitmapnos":[x["bitmapno"] for x in info["frames"]],
                          "actual_rd_blocks":len(info["frames"]),
                          "cipher_sha256":sealed["ciphertext_sha256"],
                          "original_program_executed":False,
                          "original_images_only_in_encrypted_artifact":True},sort_keys=True))


if __name__=="__main__":main()
