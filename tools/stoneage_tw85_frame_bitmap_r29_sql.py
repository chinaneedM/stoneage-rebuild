"""Independent SQLite R29 verifier of every original frame row against original RD index.

No use of R29 builder helper joins or classifications; compare the whole saved
two-table join to an independently constructed SQL database from R28 and R06.
"""
from __future__ import annotations
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"research/recovered"
FRAME=BASE/"tw85-spr137-r28/SPR-FRAME-R28.tsv.gz"
NATIVE=BASE/"adrn129-tw85-real-pair/NATIVE-R1.tsv.gz"
R28_SOURCE=BASE/"tw85-spr137-r28/SOURCE-DERIVED-R28.json"
DERIVED=BASE/"tw85-frame-bitmap-r29"
GROUP=DERIVED/"GROUP-MATERIAL-R29.tsv.gz"
BITMAP=DERIVED/"BITMAP-BINDINGS-R29.tsv.gz"
REPORT=DERIVED/"REPORT-R29.json"


def need(condition,reason):
    if not condition:raise ValueError(reason)


def fingerprint(path):
    digest=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):digest.update(chunk)
    return digest.hexdigest()


def csv_rows(path):
    with gzip.open(path,"rt",encoding="utf-8",newline="") as f:
        yield from csv.DictReader(f,delimiter="\t")


def replay():
    report=json.loads(REPORT.read_bytes())
    need(report["schema"]=="stoneage.tw85_frame_to_bitmap_same_saved_carrier.r29",
         "report source type drift")
    source=json.loads(R28_SOURCE.read_bytes())
    need(fingerprint(FRAME)==report["source_pins"]["R28_FRAME"]["sha256"]
         and fingerprint(NATIVE)==report["source_pins"]["R06_NATIVE"]["sha256"],
         "R28/R06 original-derived bytes differ")
    for file in (GROUP,BITMAP):
        want=report["tables"][file.name]
        need(file.stat().st_size==want["bytes"] and fingerprint(file)==want["sha256"],
             "published joined-table fingerprint drift")
    con=sqlite3.connect(":memory:")
    con.executescript("""
       CREATE TABLE original_bitmap(id INTEGER, physical INTEGER, rd_size INTEGER,
         width INTEGER,height INTEGER, rd_sha TEXT,
         PRIMARY KEY(physical));
       CREATE INDEX id_original_bitmap ON original_bitmap(id);
       CREATE TABLE rawframe(phys INTEGER PRIMARY KEY,grp INTEGER,id INTEGER,
         is_sentinel INTEGER, has_cue INTEGER);
       CREATE INDEX grp_rawframe ON rawframe(grp);
       CREATE INDEX id_rawframe ON rawframe(id);
    """)
    batch=[]
    for i,row in enumerate(csv_rows(NATIVE)):
        need(int(row["index"])==i,"physical ADRN order lost")
        batch.append((int(row["bitmapno"]),i,int(row["size"]),int(row["width"]),int(row["height"]),row["rd_sha256"]))
        if len(batch)==20000:
            con.executemany("INSERT INTO original_bitmap VALUES(?,?,?,?,?,?)",batch);batch=[]
    if batch:con.executemany("INSERT INTO original_bitmap VALUES(?,?,?,?,?,?)",batch)
    need(con.execute("SELECT COUNT(*) FROM original_bitmap").fetchone()[0]==416220,
         "not all original REAL-verified bitmap rows loaded")
    batch=[]
    for f in csv_rows(FRAME):
        batch.append((int(f["offset"]),int(f["group_index"]),int(f["bmp_no"]),
                      int(f["sentinel"]),int(int(f["sound_no"])!=0)))
        if len(batch)==20000:
            con.executemany("INSERT INTO rawframe VALUES(?,?,?,?,?)",batch);batch=[]
    if batch:con.executemany("INSERT INTO rawframe VALUES(?,?,?,?,?)",batch)
    need(con.execute("SELECT COUNT(*) FROM rawframe").fetchone()[0]==735666,
         "not all original R28 frame positions loaded")
    s=con.execute("""SELECT COUNT(*),SUM(is_sentinel),COUNT(DISTINCT CASE WHEN is_sentinel=0 THEN id END),
          SUM(CASE WHEN is_sentinel=0 AND NOT EXISTS
            (SELECT 1 FROM original_bitmap b WHERE b.id=rawframe.id) THEN 1 ELSE 0 END),
          SUM(CASE WHEN is_sentinel=0 AND (SELECT COUNT(*) FROM original_bitmap b WHERE b.id=rawframe.id)>1
            THEN 1 ELSE 0 END)
          FROM rawframe""").fetchone()
    need(tuple(s)==(735666,4759,397443,0,0),
         "full row/frame-ID/duplicate/missing SQL classification changed")
    binding_iter=csv_rows(BITMAP)
    linked_rows=0
    for bmp,refcount in con.execute("""SELECT id,COUNT(*) FROM rawframe WHERE is_sentinel=0 GROUP BY id ORDER BY id"""):
        bound=next(binding_iter,None)
        need(bound is not None and int(bound["bitmapno"])==bmp
             and int(bound["occurrences"])==refcount,"bitmap joined row or occurrence changed")
        candidates=list(con.execute("""SELECT physical,rd_size,width,height,rd_sha
                                     FROM original_bitmap WHERE id=? ORDER BY physical""",(bmp,)))
        need(len(candidates)==1,"unexpected bitmap multiplicity in independent check")
        c=candidates[0]
        need(int(bound["native_candidates"])==1 and int(bound["native_indices"])==c[0],
             "derived bitmap selected wrong physical candidate")
        need(bound["complete_rd_content_keys"]==str(c[1])+":"+c[4]
             and bound["sizes"]==str(c[1]) and bound["widths"]==str(c[2])
             and bound["heights"]==str(c[3])
             and bound["qualification"]=="SINGLE_ORIGINAL_RD_RECORD",
             "derived bitmap shape or SHA differs from native original source")
        linked_rows+=1
    need(next(binding_iter,None) is None and linked_rows==397443,
         "extra bitmap candidate rows added")
    groups=list(csv_rows(GROUP))
    need(len(groups)==1739 and len({int(x["group_index"]) for x in groups})==1739,
         "group occurrence evidence collapsed")
    joined_group={int(x[0]):x for x in con.execute("""
      SELECT grp,COUNT(*),SUM(is_sentinel),SUM(CASE WHEN is_sentinel=0 THEN 1 ELSE 0 END),
           COUNT(DISTINCT CASE WHEN is_sentinel=0 THEN id END),SUM(has_cue)
      FROM rawframe GROUP BY grp ORDER BY grp""")}
    original_relationships=source["joins"]["reference_relationships"]["CN50"]
    old_indices={int(x["tw85_index"]) for x in original_relationships}
    buckets=Counter()
    for group in groups:
        idx=int(group["group_index"])
        row=joined_group.get(idx)
        need(row is not None,"missing original group")
        _,total,sentinel,mapped,unique,cues=row
        want="EXACT_CN50_SPR_SEGMENT" if idx in old_indices else "R28_UNMATCHED_CN50_SPR_SEGMENT"
        need(group["source_scope"]==want and
             int(group["frame_occurrences"])==total and
             int(group["sentinel_frames"])==sentinel and
             int(group["mapped_frames"])==mapped and
             int(group["single_frames"])==mapped and
             int(group["missing_frames"])==0 and
             int(group["multiple_same_rd_frames"])==0 and
             int(group["multiple_different_rd_frames"])==0 and
             int(group["distinct_bitmap_ids"])==unique and
             int(group["missing_bitmap_ids"])==0 and
             int(group["raw_sound_word_occurrences"])==cues,
             "group frame link or evidence tag altered: "+str(idx))
        buckets[want]+=1
    need(buckets=={"EXACT_CN50_SPR_SEGMENT":1185,"R28_UNMATCHED_CN50_SPR_SEGMENT":554},
         "R28 unmatched scope regrouping changed")
    distinct_rd=con.execute("""SELECT COUNT(DISTINCT CAST(rd_size AS TEXT)||':'||rd_sha)
      FROM original_bitmap WHERE id IN (SELECT id FROM rawframe WHERE is_sentinel=0)""").fetchone()[0]
    # Verify the per-group distinct complete RD keys without relying on source-builder grouping.
    per_rd={int(i):int(c) for i,c in con.execute("""
      SELECT f.grp, COUNT(DISTINCT CAST(b.rd_size AS TEXT)||':'||b.rd_sha)
      FROM rawframe f JOIN original_bitmap b ON f.id=b.id
      WHERE f.is_sentinel=0 GROUP BY f.grp""")}
    need(all(int(g["distinct_mapped_rd_contents"])==per_rd.get(int(g["group_index"]),0)
             for g in groups),"per-group RD content distinctness drift")
    expect=dict(report["frame_mapping_classifications"])
    need(expect=={"SINGLE_ORIGINAL_RD_RECORD":730907}
         and report["distinct_referenced_bitmap_ids"]==linked_rows,
         "published source union changed")
    limits=report["boundaries"]
    need(limits["clean_official_pressing_authenticated"] is False
         and limits["named_pet_avatar_npc_or_action_identified"] is False
         and limits["actual_RD_pixels_reacquired_or_rendered_this_run"] is False
         and limits["original_client_executed"] is False
         and limits["new_original_package_bytes_downloaded"] is False
         and limits["overall_completion_percent"] is None,
         "historical grade or game runtime promoted")
    con.close()
    return {"status":"PASS","independent_original_frame_rows":s[0],"sentinel":s[1],
        "distinct_referenced_bitmap_ids":s[2],"missing_native_frame_occurrences":s[3],
        "ambiguous_native_frame_occurrences":s[4],"source_native_records":416220,
        "exact_single_native_rd_frame_occurrences":730907,
        "distinct_complete_rd_contents_mapped":distinct_rd,
        "groups_checked":len(groups),"old_source_groups":buckets["EXACT_CN50_SPR_SEGMENT"],
        "R28_unmatched_source_groups":buckets["R28_UNMATCHED_CN50_SPR_SEGMENT"],
        "named_species_or_rendered_pixel_proven":False}


def main():
    p=argparse.ArgumentParser();p.add_argument("--receipt",type=Path);a=p.parse_args()
    result=replay()
    if a.receipt:a.receipt.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))


if __name__=="__main__":main()
