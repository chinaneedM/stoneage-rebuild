"""Bounded exact snapshot replay; output derived metadata only. Never execute payloads."""
import argparse, base64, concurrent.futures, hashlib, json, re, urllib.request, urllib.parse, urllib.error
from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
SPEC="research/pets/PET-KR-ARCHIVE-TARGETS-R1.json"
def gitblob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def selection():
    s=json.loads((ROOT/SPEC).read_bytes())
    raw=(ROOT/s["source"]["path"]).read_bytes()
    assert gitblob(raw)==s["source"]["git_blob"]
    rows=[x.split("|") for x in raw.decode("utf-8").splitlines() if x.startswith("URL|")]
    assert len(rows)==s["source"]["records"]==20000
    unique={tuple(x[2:]) for x in rows}
    assert len(unique)==s["source"]["unique_metadata_records"]
    from collections import Counter
    assert dict(Counter(x[0][:4] for x in unique))==s["source"]["unique_years"]
    for x in s["targets"]:
        assert tuple(x[k] for k in ("timestamp","status","mimetype","cdx_length","cdx_digest","original")) in unique
        assert x["timestamp"].startswith("2002")
        u=urllib.parse.urlsplit(x["original"])
        assert u.hostname=="stoneage.enium.co.kr" and not u.query
    assert len(s["targets"])==15
    return s
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.links=[]; self.images=[]; self.title=[]; self.in_title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="title":self.in_title=True
        if tag in ("a","frame","iframe") and (a.get("href") or a.get("src")): self.links.append(a.get("href") or a.get("src"))
        if tag=="img" and a.get("src"):self.images.append(a["src"])
    def handle_endtag(self,tag):
        if tag=="title":self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.title.append(data)
def replay(x):
    out=dict(x,bytes_read=0,sha256=None,cdx_digest_matches=False,exact_replay_url=False,original_payload_verified=False,official_pet_identity_verified=False)
    url="https://web.archive.org/web/"+x["timestamp"]+"id_/"+x["original"]
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"stoneage-rebuild-source-review/1.0","Accept-Encoding":"identity"})
        with urllib.request.urlopen(req,timeout=14) as f:
            out["http_status"]=f.status; out["final_url"]=f.geturl(); out["content_type"]=f.headers.get("Content-Type")
            data=f.read(8*1024*1024+1)
        if len(data)>8*1024*1024:
            out["status"]="SIZE_LIMIT_EXCEEDED"; return out
        out["bytes_read"]=len(data);out["sha256"]=hashlib.sha256(data).hexdigest()
        digest=base64.b32encode(hashlib.sha1(data).digest()).decode()
        out["actual_sha1_base32"]=digest;out["cdx_digest_matches"]=digest==x["cdx_digest"]
        final=urllib.parse.unquote(out["final_url"])
        out["exact_replay_url"]=final.startswith("https://web.archive.org/web/"+x["timestamp"]+"id_/") and final.split("id_/",1)[1].replace(":80/","/")==x["original"].replace(":80/","/")
        magic="PE_MZ" if data.startswith(b"MZ") else "RAR" if data.startswith(b"Rar!\x1a\x07") else "HTML_OR_OTHER"
        out["magic"]=magic
        expected_kind=(magic in ("PE_MZ","RAR")) if x["kind"]=="later_material_candidate" else magic=="HTML_OR_OTHER"
        out["original_payload_verified"]=bool(out["http_status"]==200 and out["cdx_digest_matches"] and out["exact_replay_url"] and expected_kind)
        out["status"]="EXACT_DIGEST_REPLAY" if out["original_payload_verified"] else "RESPONSE_NOT_EXACT_PAYLOAD_PROOF"
        if x["kind"]=="official_site_page_candidate" and out["original_payload_verified"]:
            for encoding in ("utf-8","cp949","euc-kr"):
                try: text=data.decode(encoding);break
                except UnicodeDecodeError:continue
            else: text=data.decode("cp949","replace")
            p=Page();p.feed(text)
            def eligible(values):
                clean=set()
                for v in values:
                    u=urllib.parse.urlsplit(urllib.parse.urljoin(x["original"],v))
                    if u.hostname=="stoneage.enium.co.kr" and not u.query and not u.fragment and not any(t in u.path.lower() for t in ("login","webboard","member")):
                        clean.add(u.path)
                return sorted(clean)[:100]
            out["page_title"]=" ".join(p.title).strip()[:100];out["local_links"]=eligible(p.links);out["local_images"]=eligible(p.images)
        return out
    except urllib.error.HTTPError as e:
        out.update(status="HTTP_ERROR",http_status=e.code);return out
    except Exception as e:
        out.update(status="REQUEST_ERROR",error_type=type(e).__name__);return out
def main():
    p=argparse.ArgumentParser();p.add_argument("--verify",action="store_true");a=p.parse_args();s=selection()
    if a.verify:
        print("PET_KR_ARCHIVE_TARGETS_PASS",len(s["targets"]));return
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results=list(pool.map(replay,s["targets"]))
    report=dict(schema="stoneage.pet.kr_archive_replay.r1",source=s["source"],results=results,verified_exact_payloads=sum(x["original_payload_verified"] for x in results),new_official_pet_identities=0,original_payloads_published=False)
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
