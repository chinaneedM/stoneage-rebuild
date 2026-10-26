"""Metadata-only R33 historical palette cross-carrier source auditor."""
import json,hashlib,re,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCES={
"research/recovered/STONEAGE-WAYI85-MSI-CLIENT-PAYLOAD-R1.json":"18a68c9d4275763ef0ed7a347cca940cffe0fee2",
"research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt":"564233902b10c60760d4f93b1ea65d4dd1469206",
"research/recovered/STONEAGE-TW10-PALETTE-P2B-ACTUAL-COLOR-SOURCE-R1.json":"4569af739f7a54e4a5c0241c894ea5e26cb421fc",
"research/recovered/tw85-rd-private-r30/PLAN-R30.json":"59bbb09d55c33076e1616499a2710c8de588dcee",
"research/recovered/tw85-rd-private-r30/SOURCE-R30.json":"9fb54267a59561ce8b1dfaa387b857f17a94a896"}
def guard(value, reason):
    if not value: raise ValueError(reason)
def gitblob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()
def load(root=ROOT):
    raw={}
    for path,sha in SOURCES.items():
        payload=(Path(root)/path).read_bytes()
        guard(gitblob(payload)==sha,"input source Git blob changed: "+path)
        raw[path]=payload.decode("utf-8")
    return raw
def derive(raw):
    data=list(SOURCES)
    t85=json.loads(raw[data[0]]); t10=raw[data[1]]
    p2=json.loads(raw[data[2]]); plan=json.loads(raw[data[3]]); s30=json.loads(raw[data[4]])
    inventory=t85["inspection"]["inventory"]["samples"][0]["files"]
    guard(len(inventory)==557,"bad preservation carrier count")
    x=[v for v in inventory if re.search(r"/data/pal/palet_\d+\.sap$",v["path"],re.I)]
    y=[dict(v.split("=",1) for v in line.split("|")[1:]) for line in t10.splitlines() if line.startswith("CORE_FILE|category=palette|")]
    guard(len(x)==len(y)==16,"palette inventory incomplete")
    ordinal=lambda p:int(re.search(r"palet_(\d+)\.sap$",p,re.I).group(1))
    keysx=[ordinal(v["path"]) for v in x];keysy=[ordinal(v["path"]) for v in y]
    guard(set(keysx)==set(keysy)==set(range(16)) and len(set(keysx))==16 and len(set(keysy))==16,"palette ordinal collision")
    pairs=[]
    for i in range(16):
        a=x[keysx.index(i)];b=y[keysy.index(i)]
        guard(a["size"]==708 and int(b["size"])==708,"palette original size differs")
        guard(a["sha256"]==b["sha256"] and bool(re.fullmatch(r"[0-9a-f]{64}",a["sha256"])),"original palette digest differs")
        pairs.append(dict(palette_index=i,tw10_path=b["path"],tw85_path=a["path"],size=708,sha256=a["sha256"]))
    guard(p2["original_palette_sha256"]==pairs[0]["sha256"],"P2B original palette mismatch")
    guard(p2["original_actual_palette"]["rgb_sha256"]=="e02d929c63d9edce15891c28748758ef8da90d28fed5f525fd86ec73d34364e3","TW10 source instruction RGB changed")
    guard(p2["actual_scene_palette_selection_proven"] is False,"incorrect P2B runtime selection")
    a=plan["sample"]["sample_frames"];b=s30["frames"]
    guard(len(a)==len(b)==8,"R30 sample missing")
    frames=[]
    for i,(p,q) in enumerate(zip(a,b)):
        guard(p["bitmapno"]==q["bitmapno"]==303039+i,"R30 bitmap number mismatch")
        guard(p["rd_block_sha256"]==q["source_RD_sha256"],"original RD digest mismatch")
        guard(p["native_adrn_record_sha256"]==q["source_record_sha256"],"original ADRN record mismatch")
        guard(p["width"]==q["width"] and p["height"]==q["height"],"original dimensions mismatch")
        guard(bool(re.fullmatch(r"[0-9a-f]{64}",q["source_palette_index_sha256"])),"invalid R30 index pixels")
        frames.append(dict(frame=i,bitmapno=q["bitmapno"],width=q["width"],height=q["height"],original_rd_sha256=q["source_RD_sha256"],source_index_pixels_sha256=q["source_palette_index_sha256"],adrn_record_sha256=q["source_record_sha256"]))
    guard(t85["official_clean_client_authenticated"] is False,"unreviewed official certification")
    return pairs,frames,p2["original_palette_sha256"],p2["original_actual_palette"]["rgb_sha256"]
def check(root=ROOT):
    report=json.loads((Path(root)/"research/recovered/STONEAGE-TW85-PALETTE-SAME-CARRIER-R33.json").read_text(encoding="utf-8"))
    pairs,frames,sap,rgb=derive(load(root))
    guard(report["schema"]=="stoneage.original_palette_same_carrier.r33.v1","schema mismatch")
    guard(report["original_palette_pairs_exact"]==pairs,"report exact palette pairs differ")
    guard(report["prior_r30_eight_indexed_frames"]==frames,"report R30 source frames differ")
    guard(report["tw10_original_palet0_sap_sha256"]==sap and report["tw10_original_palet0_rgb_after_initialization_sha256"]==rgb,"report TW10 palette interpretation differs")
    guard(report["source_git_blob_pins"]==SOURCES,"source blob provenance differs")
    guard(report["source_file_count_557"]==557,"incorrect carrier count")
    guard(all(v is False for v in report["unverified"].values()),"historical false-color or runtime claim")
    guard(report["original_binary_or_image_published"] is False,"proprietary asset disclosure")
    return report
if __name__=="__main__":
    argparse.ArgumentParser().parse_args()
    q=check()
    print(json.dumps({"R33_SHA256_identical_palette_pairs":len(q["original_palette_pairs_exact"]),"R30_original_indexed_frame_witnesses":len(q["prior_r30_eight_indexed_frames"]),"authenticated_TW85_runtime_color":False}))
