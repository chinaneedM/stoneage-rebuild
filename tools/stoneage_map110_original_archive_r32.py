"""Independent offline guard for R32 public metadata; does not claim replay of original bytes."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from tools.stoneage_map110_actual_cells_r32 import ROOT, SOURCES, TIMELINE, verify_timeline, original_git_blob

ARCHIVE=ROOT/"research/recovered/STONEAGE-ORIGINAL-MAP110-CELL-DELTA-R32.json"

def need(test,message):
 if not test:raise ValueError(message)

def guard(obj,timeline_bytes):
 need(obj.get("schema")=="stoneage.map110_archived_2003_original_cell_delta.r32","schema")
 need(obj.get("timeline_git_blob")==original_git_blob(timeline_bytes),"timeline source changed")
 verify_timeline(timeline_bytes.decode("utf-8"))
 need(obj.get("map_token")==110 and obj.get("map_original_path")=="map/110.DAT","map identity")
 packages=obj.get("source_packages")
 need(isinstance(packages,dict) and set(packages)==set(SOURCES),"source package count")
 for label,src in SOURCES.items():
  record=packages[label]
  need(record=={"capture":src["capture"],"container_sha256":src["container_sha256"],
                "original_dat_sha256":src["file_sha256"]},"source SHA or capture mismatch")
 result=obj.get("result",{})
 need(result.get("width")==46 and result.get("height")==45,"dimensions")
 need(result.get("total_cells_per_plane")==2070 and result.get("total_actual_cells_compared")==6210,"cell count")
 planes=result.get("plane_diffs")
 need(isinstance(planes,list) and len(planes)==3,"three planes exactly")
 for index,p in enumerate(planes):
  need(p.get("ordinal")==index+1,"original ordinal order")
  for sha in ("june_plane_sha256","dec_plane_sha256"):
   need(isinstance(p.get(sha),str) and len(p[sha])==64 and all(c in "0123456789abcdef" for c in p[sha]),"original plane SHA")
  changes=p.get("changes")
  need(isinstance(changes,list) and len(changes)==p.get("changed_cell_count"),"diff consistency")
  need(p.get("old_nonzero_count") in range(2071) and p.get("new_nonzero_count") in range(2071),"nonzero total")
  if index<2:
   need(not changes and p["june_plane_sha256"]==p["dec_plane_sha256"],"unchanged planes must be byte identical")
  else:
   need(len(changes)==3 and p["june_plane_sha256"]!=p["dec_plane_sha256"],"three-cell third-plane difference")
  ids=[]
  delta=0
  for c in changes:
   idx=c.get("index")
   need(type(idx) is int and 0<=idx<2070,"cell index bound")
   need(c.get("x_rowmajor_candidate")==idx%46 and c.get("y_rowmajor_candidate")==idx//46,"coordinate arithmetic")
   a,b=c.get("june_u16"),c.get("dec_u16")
   need(type(a) is int and type(b) is int and 0<=a<=65535 and 0<=b<=65535 and a!=b,"actual u16 change")
   ids.append(idx);delta+=int(b!=0)-int(a!=0)
  need(ids==sorted(set(ids)),"changed cells canonical and unique")
  need(p["new_nonzero_count"]-p["old_nonzero_count"]==delta,"nonzero cell conservation")
 for key in ("no_named_map_or_quest_role","no_map_grid_released","event_plane_runtime_semantics_unverified",
             "world_coordinates_not_authenticated","june_equals_preserved25_by_whole_file_prior_witness_only"):
  need(obj.get(key) is True,"original source boundary promotion")
 return {"map_token":110,"changed_ordinal_planes":[p["changed_cell_count"] for p in planes],
         "changed_flat_indices":[c["index"] for c in planes[2]["changes"]],
         "third_plane_nonzero_delta":planes[2]["new_nonzero_count"]-planes[2]["old_nonzero_count"]}

def verify(path=ARCHIVE):
 raw=path.read_bytes()
 obj=json.loads(raw)
 summary=guard(obj,TIMELINE.read_bytes())
 return {"source_report_sha256":hashlib.sha256(raw).hexdigest(),**summary}

if __name__=="__main__":
 print(json.dumps(verify(),sort_keys=True,ensure_ascii=False,indent=2))
