"""R14: recover actual private CN50 portraits and PET101 residual motion pixels.
No official pressing/identity, native runtime or complete visual atlas claim.
"""
import argparse,collections,hashlib,json,mmap,struct,subprocess,tempfile
from pathlib import Path
from tools import stoneage_cn50_original_resource_catalog as cat
from tools import stoneage_pet_high_first_100_cn50_full_motion as pre
from tools import stoneage_pet_atlas_r4_private_source as secure
from tools.stoneage_pet_high_first_57_coverage import ROOT,blob,gzrows
from tools.stoneage_pet_high_first_67_bulk_pixels import decode
from tools.stoneage_rd_codec import decode_rd_block
from tools.stoneage_original_observation_lab import gray_png
from tools.stoneage_stoneage5_msi_probe import load_root,find_entry
from tools.stoneage_stoneage5_cab_probe import iso_file_slice
from tools.stoneage_stoneage5_full_cab_acquisition import EXPECTED_SIZE,checked_layout,download_cab,extracted_inventory
PINS={
"research/pets/PET-HIGH-FIRST-CN50-NATIVE-SPR-ALBUM-R1.json":"98fea71c051dfa887b91154a8a72d17c67b57744",
"research/pets/PET-HIGH-FIRST-101-CN50-ORIGINAL-RD-R1.json":"f7a50af4bb440008a227d1522d65004dd38a58a6",
"research/recovered/cn50-resource-metadata/MANIFEST-R1.json":"5063cf2fade4e0739ac35c38a90dfff1a43db960",
"research/recovered/cn50-resource-metadata/ADRN-R1.tsv.gz":"127670eaf2bc19ba9d15776d090a8307058f729d",
"research/pets/PET-ATLAS-R8-SESSION-PUBLIC.pem":"c7fced628655332ad1b6ad34385e385fddde2e6f"}
def sha(b):return hashlib.sha256(b).hexdigest()
def stable(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def pinned(p):
    b=(ROOT/p).read_bytes();assert blob(b)==PINS[p],p
    return b
def plan():
    paths=list(PINS)
    album,prior,manifest=[json.loads(pinned(p)) for p in paths[:3]]
    pinned(paths[3]);pinned(paths[4])
    positions=album["records"];old=prior["observations"]
    assert len(positions)==305 and len(old)==90
    assert all(v["status"]=="DUAL_DECODED_INDEX_PIXELS" for v in old.values())
    portraits={n for row in positions for n in row["portrait_bitmap_numbers_in_file_order"]}
    motion={v["bitmap"] for v in old.values()}
    assert len(portraits)==309 and len(motion)==90
    assert sum(len(row["portrait_bitmap_numbers_in_file_order"])>1 for row in positions)==4
    by=collections.defaultdict(list)
    for row in gzrows(ROOT/paths[3]):
        n=int(row["bitmapno"])
        if n in portraits|motion:
            by[n].append(dict(index=int(row["index"]),bitmap=n,offset=int(row["adder"]),size=int(row["size"]),width=int(row["width"]),height=int(row["height"]),xoff=int(row["xoff"]),yoff=int(row["yoff"]),rd_sha256=row["rd_block_sha256"],attr_sha256=row["attr_sha256"]))
    assert set(by)==portraits|motion and all(len(v)==1 for v in by.values())
    rows={v[0]["index"]:v[0] for v in by.values()}
    for a in positions:
        n=a["portrait_lookup_after_ordered_load"]
        assert n==a["portrait_bitmap_numbers_in_file_order"][-1] and by[n][0]["rd_sha256"]==a["portrait_lookup_rd_sha256"]
    for i,v in old.items():
        assert all(rows[int(i)][k]==v[k] for k in ("bitmap","offset","size","width","height","rd_sha256","attr_sha256"))
    assert prior["source_cab_sha256"]==manifest["source"]["cab_sha256"]
    return positions,old,manifest,rows,portraits,motion
def one(r,adrn,real,folder,old):
    i=r["index"];raw=adrn[i*80:(i+1)*80]
    assert struct.unpack_from("<IIIiiii",raw)==tuple(r[k] for k in ("bitmap","offset","size","xoff","yoff","width","height"))
    assert sha(raw[28:])==r["attr_sha256"]
    o,s,w,h=[r[k] for k in ("offset","size","width","height")]
    assert 0<=o and 16<=s<=len(real)-o
    b=real[o:o+s];assert sha(b)==r["rd_sha256"]
    z=decode(b,w,h);receipt=dict(r,adrn_sha256=sha(raw),**z,path=None,png_sha256=None,indexed_pixel_sha256=z["index_pixels_sha256"])
    if old is not None:
        assert old["adrn_sha256"]==receipt["adrn_sha256"] and old["index_pixels_sha256"]==receipt["indexed_pixel_sha256"] and z["status"]=="DUAL_DECODED_INDEX_PIXELS"
    if z["status"]=="DUAL_DECODED_INDEX_PIXELS":
        header,px=decode_rd_block(b,authoritative_block_size=s)
        assert (header["width_s"],header["height_s"],sha(px))==(w,h,z["index_pixels_sha256"])
        p=gray_png(px,w,h);name=f"bitmap-{i}.png";(folder/name).write_bytes(p)
        receipt.update(path=name,png_sha256=sha(p))
    return receipt
def export(out,pub):
    positions,old,manifest,rows,portraits,motion=plan()
    assert blob(pub.read_bytes())==PINS[list(PINS)[4]]
    source,_,lookup=cat.qualify_sources(ROOT)
    _,_,_,track,carrier,url,_,entries=load_root()
    cab=find_entry(entries,"DATA1.CAB");assert cab and int(cab["size"])==EXPECTED_SIZE
    prefix,status,_=iso_file_slice(url,cab,track,0,65536);assert status==206
    _,expected=checked_layout(prefix)
    with tempfile.TemporaryDirectory(prefix="cn50-r14-") as tmp:
        root=Path(tmp);cabfile=root/"DATA1.CAB";directory=root/"contents";directory.mkdir()
        digest=download_cab(url,cab,track,int(carrier["size"]),cabfile)
        assert digest==source["source"]["cab_sha256"]==manifest["source"]["cab_sha256"]
        with cabfile.open("rb") as f:assert f.read(len(prefix))==prefix
        subprocess.run(["cabextract","-q","-d",str(directory),str(cabfile)],check=True,timeout=1500)
        inventory=extracted_inventory(directory,expected)
        assert len(inventory)==413 and all(lookup.get(x["name"])==(x["size"],x["sha256"]) for x in inventory)
        files=cat.verify_four(directory,lookup);assert files==manifest["source"]["input_containers"]
        folder=root/"private";folder.mkdir()
        with (directory/cat.NAMES["adrn"]).open("rb") as a,(directory/cat.NAMES["real"]).open("rb") as b,mmap.mmap(a.fileno(),0,access=mmap.ACCESS_READ) as adrn,mmap.mmap(b.fileno(),0,access=mmap.ACCESS_READ) as real:
            images={str(i):one(r,adrn,real,folder,old.get(str(i))) for i,r in sorted(rows.items())}
        for v in images.values():
            v["portrait_candidate"]=v["bitmap"] in portraits;v["pet101_motion"]=v["bitmap"] in motion
        summary=dict(positions=len(positions),portrait_candidates=len(portraits),motion_candidates=len(motion),distinct_rows=len(images),grades=dict(collections.Counter(v["status"] for v in images.values())),pngs=sum(v["path"] is not None for v in images.values()))
        report=dict(schema="stoneage.pet.atlas_r14.cn50_private.r1",source_pins=PINS,source_cab_sha256=digest,source_files=files,positions=positions,bitmaps=images,summary=summary,official_identity_verified=False,official_clean_pressing_verified=False,original_runtime_verified=False,original_palette_runtime_verified=False,original_assets_published=False)
        (folder/"receipt.json").write_text(stable(report),encoding="utf8")
        e=secure.seal(folder,pub,out)
        print("R14_SUMMARY="+stable(summary),flush=True)
        print("R14_CIPHER_SHA256="+e["cipher_sha256"],flush=True)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan-only",action="store_true");p.add_argument("--output",type=Path);p.add_argument("--public-key",type=Path);a=p.parse_args()
    pos,old,m,rows,portraits,motion=plan()
    print("R14_PLAN="+stable(dict(positions=len(pos),portraits=len(portraits),motion=len(motion),distinct_rows=len(rows))),flush=True)
    if not a.plan_only:
        assert a.output and a.public_key
        export(a.output,a.public_key)
if __name__=="__main__":main()
