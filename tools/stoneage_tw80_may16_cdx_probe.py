"""Safe metadata-only Wayback CDX probe; does not retrieve original game data."""
from __future__ import annotations
import argparse
import json
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

TARGET="http://www.wayi.com.tw/stoneage/actives/940329/page_3.html"
FIELDS=["timestamp","original","statuscode","mimetype","digest"]
def build_url():
    return "https://web.archive.org/cdx/search/cdx?"+urlencode([
        ("url",TARGET),("output","json"),("filter","statuscode:200"),
        ("from","2005"),("to","2007"),("fl",",".join(FIELDS)),
        ("collapse","timestamp:6")])
def classify(rows):
    if not isinstance(rows,list) or not rows or rows[0]!=FIELDS:
        raise ValueError("Invalid CDX header")
    if len(rows)-1>20:
        raise ValueError("Unbounded CDX listing")
    accepted=[]
    for row in rows[1:]:
        if not isinstance(row,list) or len(row)!=5:
            raise ValueError("Malformed CDX row")
        stamp,original,status,mime,digest=row
        if not isinstance(stamp,str) or len(stamp)!=14 or not stamp.isascii() or not stamp.isdecimal() or not 2005<=int(stamp[:4])<=2007:
            raise ValueError("Out-of-era capture")
        if not isinstance(original,str) or original.lower()!=TARGET.lower():
            raise ValueError("Unrelated original URL")
        if status!="200" or not isinstance(mime,str) or len(mime)>90 or not isinstance(digest,str) or len(digest)>70:
            raise ValueError("Unexpected metadata")
        accepted.append({"timestamp":stamp,"original":original,"index_status":status,"mimetype":mime,"cdx_digest":digest})
    return accepted
def report(raw=None,error=None):
    base={"schema":"stoneage-tw80-may16-operator-cdx-index-r1","source_url":TARGET,"index_url":build_url(),
          "index_window":"2005-2007","status":"UNVERIFIED","captures":[],
          "original_page_content_authenticated":False,"original_client_binary_retrieved":False,"original_pet_runtime_verified":False}
    if error is not None:
        base.update(status="NETWORK_INDETERMINATE",error_class=str(error))
        return base
    try:
        rows=classify(json.loads(raw))
    except (ValueError,TypeError,KeyError):
        base["status"]="CDX_RESPONSE_INDETERMINATE"
        return base
    base.update(status="INDEX_HITS_UNAUTHENTICATED_CONTENT" if rows else "EMPTY_INDEX_NOT_PROOF_OF_ABSENCE",captures=rows)
    return base
def probe():
    req=Request(build_url(),headers={"Accept":"application/json","User-Agent":"StoneAge-Source-Index/1.0"})
    try:
        with urlopen(req,timeout=8) as stream:
            payload=stream.read(65537)
        if len(payload)>65536:
            return report(error="INDEX_RESPONSE_TOO_LARGE")
        return report(raw=payload.decode("utf-8"))
    except (HTTPError,URLError,TimeoutError,OSError,UnicodeError) as exc:
        return report(error=type(exc).__name__)
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--probe",action="store_true")
    opts=parser.parse_args()
    print(json.dumps(probe() if opts.probe else {"target":TARGET,"status":"OFFLINE_READY","index_url":build_url()},sort_keys=True,indent=2))
