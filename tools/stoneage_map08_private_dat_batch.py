"""MAP08 private source acquisition: all 955 exact, previously pinned DAT; no raw assets in Git."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
import zlib

from tools.stoneage_private_scene_source_r2 import acquire_bundle, qualify_carrier, seal

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json"

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def pinned():
    report=json.loads(INDEX.read_bytes())
    assert report["schema"].startswith("stoneage.")
    cols=report["per_floor_source_row_columns"]
    rows={r[0]:dict(zip(cols,r)) for r in report["per_floor_source_rows"]}
    assert len(rows)==955
    pins={}
    for name,row in sorted(rows.items()):
        assert name.endswith(".dat") and name[:-4].isdigit()
        assert row["source_file_bytes"]==8+6*row["original_header_width"]*row["original_header_height"]
        pins[name]=(row["source_file_bytes"],row["source_full_file_SHA256"])
    return pins

def extract(bundle,pins):
    import libarchive
    got={}
    with libarchive.file_reader(str(bundle)) as archive:
        for entry in archive:
            path=entry.pathname.replace("\\","/").lower()
            name=path.rsplit("/",1)[-1]
            if "/stoneage2.5/map/" not in path or name not in pins:
                continue
            raw=b"".join(entry.get_blocks())
            if name in got or (len(raw),digest(raw))!=pins[name]:
                raise ValueError("DAT source conflict: "+name)
            got[name]=raw
            if len(got)==len(pins):
                break
    if set(got)!=set(pins):
        raise ValueError("missing pinned original DATs: "+str(sorted(set(pins)-set(got))))
    return got

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--certificate",required=True,type=Path)
    a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    report={"schema":"stoneage.map08.original_dat_private_batch_source.r1",
        "status":"NOT_VERIFIED","original_executable_executed":False,
        "original_client_rendering_verified":False,
        "official_same_deployment_verified":False,"raw_originals_in_public_git":False}
    try:
        pins=pinned()
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp)
            carrier=acquire_bundle(work,report)
            report["qualified_carrier"]=qualify_carrier(carrier)
            got=extract(carrier,pins)
            report["members"]={n:{"bytes":len(raw),"sha256":digest(raw),
                "crc32":f"{zlib.crc32(raw)&0xffffffff:08x}"}
                for n,raw in sorted(got.items())}
            archive=work/"map08-original-dat-private.zip"
            with zipfile.ZipFile(archive,"x",zipfile.ZIP_DEFLATED) as z:
                for name,raw in sorted(got.items()):
                    z.writestr(name,raw)
            with zipfile.ZipFile(archive) as z:
                if z.testzip() is not None or len(z.namelist())!=len(pins):
                    raise ValueError("private DAT archive CRC/member count")
            report["private_archive_plaintext"]={"bytes":archive.stat().st_size,
                "sha256":digest(archive.read_bytes()),"members":len(got)}
            report["transfer"]=seal(archive,a.certificate,a.output/"map08-private-dat.der")
            report["status"]="VERIFIED_955_ORIGINAL_DAT_ENCRYPTED"
    except Exception as ex:
        report["status"]="FAILED"
        report["error"]={"type":type(ex).__name__,"message":str(ex)[:300]}
        raise
    finally:
        (a.output/"source-report.json").write_text(
            json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
        print(json.dumps({"status":report["status"],"members":len(report.get("members",{}))}))
if __name__=="__main__":
    main()
