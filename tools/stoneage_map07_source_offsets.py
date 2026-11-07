"""Export only source-verified TW1 ADRN drawing offsets for MAP07 private reconstruction.

No commercial bitmap, source DAT, or executable leaves this workflow.
"""
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json"
SOURCE=ROOT/"research/recovered/tw10-resource-metadata/ADRN-R1.tsv.gz"

def verified_rows():
    catalog=json.loads(CATALOG.read_bytes())
    if len(catalog["source_TW1_real_RD_rows"])!=4166:
        raise ValueError("source catalog changed")
    lookup={int(r[1]):r for r in catalog["source_TW1_real_RD_rows"]}
    if len(lookup)!=4166:
        raise ValueError("duplicate original index")
    result={}
    with gzip.open(SOURCE,"rt",encoding="utf-8",newline="") as fp:
        for row in csv.DictReader(fp,delimiter="\t"):
            index=int(row["index"])
            if index not in lookup:
                continue
            r=lookup[index]
            if (int(row["width"]),int(row["height"]),row["rd_block_sha256"])!=(r[2],r[3],r[5]):
                raise ValueError("RD/index consistency "+str(index))
            if index in result:
                raise ValueError("duplicate ADRN index")
            result[index]={
                "alias":r[0],"index":index,
                "xoff":int(row["xoff"]),"yoff":int(row["yoff"]),
                "width":int(row["width"]),"height":int(row["height"]),
                "source_RD_sha256":r[5],
                "source_index_pixels_sha256":r[6]}
    if len(result)!=4166:
        raise ValueError("incomplete 4166 original ADRN records")
    return {"schema":"stoneage.map07.tw10.original_adrn_source_offsets.r1",
        "original_TW1_ADRN1_sha256":catalog["provenance"]["original_TW1_ADRN1_sha256"],
        "original_TW1_p3h_sha256":catalog["provenance"]["original_TW1_retail_P3H_zip_sha256"],
        "stage_A_native_draw_order_verified":False,
        "same_official_dat_and_image_deployment_verified":False,
        "rows":[result[i] for i in sorted(result)]}

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    data=verified_rows()
    output=a.output/"source-offsets-public-derived.json"
    output.write_text(json.dumps(data,ensure_ascii=False,separators=(",",":"))+"\n")
    print(json.dumps({"qualified_offset_rows":len(data["rows"]),
        "bytes":output.stat().st_size,
        "sha256":hashlib.sha256(output.read_bytes()).hexdigest()}))
if __name__=="__main__":
    main()
