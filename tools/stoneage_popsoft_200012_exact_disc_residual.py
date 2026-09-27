#!/usr/bin/env python3
"""Retry only the two timed-out DiscMaster SHA1 queries from the Popsoft Dec-2000 exact-disc R1 probe."""
from __future__ import annotations
import hashlib,json,time,urllib.parse,urllib.request

UA="stoneage-rebuild-archaeology/1.0"
DISCM="https://discmaster.textfiles.com/search"
HASHES=(
 ("cd1","1D674459E1EC61706A688AA73C94DFDC1802C074"),
 ("cd2","97CF4340916C39D9AA56278C6B86615E8D486DEC"),
)

def clean(v,n=4000):
 return " ".join(str(v if v is not None else "").split()).replace("|","%7C")[:n]

def url(term):
 p=[("q",f'"{term}"'),("qfields","t"),("mode","deep"),("dedup","dedup"),
    ("limit","200"),("outputAs","json"),("showItemName","showItemName"),
    ("tsMin","1999"),("tsMax","2002")]
 return DISCM+"?"+urllib.parse.urlencode(p)

def rows(data):
 out=[]
 def walk(n):
  if isinstance(n,dict):
   if ("itemid" in n or "itemName" in n) and ("fileid" in n or "filename" in n or "href" in n): out.append(n)
   for v in n.values(): walk(v)
  elif isinstance(n,list):
   for v in n: walk(v)
 walk(data)
 return out

def query(term):
 last=None
 for attempt in range(1,4):
  try:
   req=urllib.request.Request(url(term),headers={"User-Agent":UA,"Accept":"application/json,*/*","Accept-Encoding":"identity"})
   with urllib.request.urlopen(req,timeout=50) as r:
    b=r.read(8*1024*1024+1)
    if len(b)>8*1024*1024: raise ValueError("response-too-large")
    data=json.loads(b.decode("utf-8"))
    return attempt,int(getattr(r,"status",r.getcode())),r.geturl(),b,rows(data),None
  except Exception as e:
   last=(type(e).__name__,str(e))
   if attempt<3: time.sleep(attempt*3)
 return 3,None,"",b"",[],last

def main():
 print("StoneAge Popsoft Dec-2000 exact-disc SHA1 residual — R2")
 print("PARENT|STONEAGE-POPSOFT-200012-EXACT-DISCS-R1.txt|two DiscMaster SHA1 timeouts only")
 print("SCOPE|DiscMaster full-text exact SHA1|serial bounded retry|no payload")
 errors=[]; hits=0
 for label,sha1 in HASHES:
  attempt,st,final,b,rr,err=query(sha1)
  if err:
   errors.append((label,err[0],err[1]))
   print(f"ERROR|label={label}|kind={clean(err[0])}|message={clean(err[1])}")
  else:
   print(f"QUERY|label={label}|attempt={attempt}|status={st}|rows={len(rr)}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|final={clean(final)}")
   for row in rr:
    hits+=1
    print(f"HIT|label={label}|itemid={clean(row.get('itemid'))}|itemName={clean(row.get('itemName'))}|fileid={clean(row.get('fileid'))}|filename={clean(row.get('filename'))}|size={clean(row.get('size'))}")
 print(f"COUNT|hashes={len(HASHES)}")
 print(f"COUNT|hits={hits}")
 print(f"COUNT|errors={len(errors)}")
 if hits:
  print("RESOLUTION|POPSOFT_DEC2000_SHA1_INDEX_HIT|inspect exact carrier next")
 elif errors:
  print("RESOLUTION|POPSOFT_DEC2000_SHA1_RESIDUAL_PARTIAL|retain failed hash only as technical residual")
 else:
  print("RESOLUTION|POPSOFT_DEC2000_EXACT_IMAGE_INDEX_BOUNDED|all exact filename/hash surfaces completed with zero hits")
 print("EVIDENCE_BOUNDARY|Zero preservation-index hits do not prove disc contents; no ISO payload is fetched.")

if __name__=="__main__":
 main()
