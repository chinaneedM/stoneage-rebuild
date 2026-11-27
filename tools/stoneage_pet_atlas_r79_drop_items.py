"""R79 pet drop source probe. Only bounded derived fields; no raw file publication."""
import hashlib, json, urllib.request, re
from pathlib import Path
URL="https://raw.githubusercontent.com/gavinlinasd/StoneAge/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56/gmsv/data/itemset6.txt"
BLOB="eac985796b59286c547db2abce7b3d604a5e6226"
IDS={1728,1729,1730,1731,1738,1739,1740,1741,1742,1743,1744,1745}
with urllib.request.urlopen(URL,timeout=45) as response:
    data=response.read(2777182)
assert len(data)==2777181
assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==BLOB
rows=[]
for line,raw in enumerate(data.splitlines(),1):
    if not raw.strip(): continue
    cells=raw.lstrip(b" ").split(b",")
    # ITEM_ID_TOKEN_INDEX 17, source C token index is 1-based.
    if len(cells)<17: continue
    token=cells[16].strip()
    if not re.fullmatch(rb"[0-9]+", token): continue
    item_id=int(token)
    if item_id not in IDS: continue
    name=cells[0]
    rows.append({"id":item_id,"line":line,"commented":raw.startswith(b"#"),"name_gb18030":name.decode("gb18030",errors="strict"),"row_sha256":hashlib.sha256(raw).hexdigest(),"field_count":len(cells)})
active=[r for r in rows if not r["commented"]]
result={"blob":BLOB,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"rows":rows,"missing_active_ids":sorted(IDS-{r["id"] for r in active}),"duplicate_active_ids":sorted(i for i in IDS if sum(r["id"]==i for r in active)>1),"qualification":"Static later comparison item name only, not official drop or acquisition proof."}
print("R79_ITEM_RECEIPT="+json.dumps(result,ensure_ascii=False,sort_keys=True))
