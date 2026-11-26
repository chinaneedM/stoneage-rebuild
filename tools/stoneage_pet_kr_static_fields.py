"""Static bounded source evidence. No execution or extraction of proprietary archives."""
import argparse, base64, concurrent.futures, hashlib, json, re, struct, urllib.request, urllib.parse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from stoneage_pet_kr_archive_targets import selection, ROOT

RECEIPT=ROOT/"research/pets/PET-KR-ARCHIVE-REPLAY-CI-OBSERVED-R1.json"
IMG=re.compile(r"/images/game_introduce/pet_caractor/4_\d+\.gif$",re.I)
FIELD=re.compile(r"^(?:[가-힣][가-힣0-9 ·/()＋+\-]{0,19}|[0-9]{1,4}(?:\s*[-~:/+%]\s*[0-9]{1,4})?%?)$")
class Rows(HTMLParser):
    def __init__(self,url):
        super().__init__(convert_charrefs=True)
        self.url=url; self.stack=[]; self.rows=[]; self.images=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ("script","style"): self.skip+=1
        if tag=="tr": self.stack.append({"cells":[],"active":None,"images":[]})
        if tag in ("td","th") and self.stack: self.stack[-1]["active"]=[]
        if tag=="img" and a.get("src"):
            u=urllib.parse.urlsplit(urllib.parse.urljoin(self.url,a["src"]))
            if u.hostname=="stoneage.enium.co.kr" and not u.query and not u.fragment and IMG.fullmatch(u.path):
                self.images.append(u.path)
                if self.stack: self.stack[-1]["images"].append(u.path)
    def handle_data(self,data):
        if self.stack and not self.skip and self.stack[-1]["active"] is not None:
            self.stack[-1]["active"].append(data)
    def handle_endtag(self,tag):
        if tag in ("script","style"): self.skip=max(0,self.skip-1)
        if tag in ("td","th") and self.stack and self.stack[-1]["active"] is not None:
            row=self.stack[-1]; row["cells"].append(" ".join(" ".join(row["active"]).split()));row["active"]=None
        if tag=="tr" and self.stack:
            row=self.stack.pop()
            if row["images"]:
                self.rows.append({"image_paths":row["images"],"cell_count":len(row["cells"]),"short_field_candidates":[{"cell_index":i,"value":s} for i,s in enumerate(row["cells"]) if FIELD.fullmatch(s)]})
def page(data,url):
    for enc in ("utf-8","cp949","euc-kr"):
        try: txt=data.decode(enc);break
        except UnicodeDecodeError:continue
    else: return {"status":"UNDECODABLE"}
    p=Rows(url);p.feed(txt);p.close()
    return {"encoding":enc,"numbered_image_paths":sorted(set(p.images)),"direct_row_candidates":p.rows,"field_semantics":"UNREVIEWED_DIRECT_HTML_ROW_NOT_NATIVE_PET_ID"}
def pe(data):
    if len(data)<64 or data[:2]!=b"MZ":raise ValueError("not MZ")
    p=struct.unpack_from("<I",data,60)[0]
    if p+24>len(data) or data[p:p+4]!=b"PE\0\0":raise ValueError("not PE")
    machine,n,stamp,_,_,opt,flags=struct.unpack_from("<HHIIIHH",data,p+4)
    q=p+24+opt
    if not 0<n<=96 or q+40*n>len(data):raise ValueError("section bounds")
    sections=[]
    for i in range(n):
        z=q+40*i
        name=data[z:z+8].split(b"\0")[0].decode("ascii","replace")
        vs,va,rs,ro=struct.unpack_from("<IIII",data,z+8)
        if rs and ro+rs>len(data):raise ValueError("section outside file")
        sections.append({"name":name,"virtual_size":vs,"raw_size":rs})
    versions=[]
    for m in re.finditer(b"\xbd\x04\xef\xfe",data):
        z=m.start()
        if z+52<=len(data):
            v=struct.unpack_from("<13I",data,z)
            if v[1]==0x10000:
                versions.append({"file":[v[2]>>16,v[2]&65535,v[3]>>16,v[3]&65535],"product":[v[4]>>16,v[4]&65535,v[5]>>16,v[5]&65535]})
    return {"format":"PE","machine":machine,"coff_timestamp":stamp,"characteristics":flags,"sections":sections,"fixed_version_signature_candidates":versions,"role":"UNCLASSIFIED_EXECUTABLE_NOT_EXECUTED"}
def rar(data):
    if not data.startswith(b"Rar!\x1a\x07\x00"):return {"format":"RAR_VARIANT_UNPARSED"}
    p=7; ext=Counter(); count=0; members=[]; complete=False
    while p+7<=len(data) and count<10000:
        crc,typ,flags,hs=struct.unpack_from("<HBHH",data,p)
        if hs<7 or p+hs>len(data):raise ValueError("RAR header bounds")
        add=struct.unpack_from("<I",data,p+7)[0] if flags&0x8000 and hs>=11 else 0
        if typ==0x74:
            if hs<32:raise ValueError("short RAR file header")
            pack,unpack=struct.unpack_from("<II",data,p+7)
            ns=struct.unpack_from("<H",data,p+26)[0]
            off=32
            if flags&0x100:
                if hs<40:raise ValueError("short large header")
                hp,hu=struct.unpack_from("<II",data,p+32);pack+=hp<<32;unpack+=hu<<32;off=40
            if off+ns>hs:raise ValueError("RAR name bounds")
            name=data[p+off:p+off+ns].split(b"\0")[0].decode("cp949","replace").replace("\\","/").rsplit("/",1)[-1]
            suffix=Path(name).suffix.lower()
            ext[suffix or "(none)"]+=1; count+=1
            if re.fullmatch(r"[A-Za-z0-9_. -]{1,80}",name) and suffix in (".exe",".dll",".bin",".dat",".spr",".ini",".txt",".bmp",".gif",".jpg",".wav",".mp3",".pak",".zip",".rar",".html",".htm"):
                members.append({"basename":name,"packed_bytes":pack,"unpacked_bytes":unpack})
            add=pack
        if typ==0x7b:complete=True;break
        nxt=p+hs+add
        if nxt<=p or nxt>len(data):raise ValueError("RAR data bounds")
        p=nxt
    return {"format":"RAR4","file_headers":count,"extensions":dict(sorted(ext.items())),"technical_member_metadata":members,"end_header_seen":complete,"role":"STATIC_CONTAINER_INDEX_NOT_CLIENT_PROOF"}
def inspect(pair):
    x,prior=pair
    out={"original":x["original"],"timestamp":x["timestamp"],"expected_sha256":prior["sha256"],"verified":False}
    try:
        url="https://web.archive.org/web/"+x["timestamp"]+"id_/"+x["original"]
        req=urllib.request.Request(url,headers={"User-Agent":"stoneage-rebuild-source-review/1.0","Accept-Encoding":"identity"})
        with urllib.request.urlopen(req,timeout=20) as f:
            final=urllib.parse.unquote(f.geturl()); status=f.status; data=f.read(8*1024*1024+1)
        digest=hashlib.sha256(data).hexdigest()
        out.update(bytes_read=len(data),sha256=digest,actual_cdx_digest=base64.b32encode(hashlib.sha1(data).digest()).decode())
        out["verified"]=bool(status==200 and len(data)<=8*1024*1024 and final.startswith("https://web.archive.org/web/"+x["timestamp"]+"id_/") and final.split("id_/",1)[1].replace(":80/","/")==x["original"].replace(":80/","/") and digest==prior["sha256"] and out["actual_cdx_digest"]==x["cdx_digest"])
        if not out["verified"]:return out
        out["derived"]=page(data,x["original"]) if x["kind"]=="official_site_page_candidate" else pe(data) if data.startswith(b"MZ") else rar(data)
    except Exception as e: out["error_type"]=type(e).__name__
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument("--verify",action="store_true");a=p.parse_args()
    spec=selection(); prior=json.loads(RECEIPT.read_bytes())["report"]["results"]
    assert len(prior)==15 and all(x["original_payload_verified"] for x in prior)
    assert all((x["original"],x["timestamp"],x["cdx_digest"])==(y["original"],y["timestamp"],y["cdx_digest"]) for x,y in zip(spec["targets"],prior))
    assert page(b'<table><tr><td><img src="/images/game_introduce/pet_caractor/4_001.gif"></td><td>42</td></tr></table>',spec["targets"][0]["original"])["direct_row_candidates"][0]["short_field_candidates"]==[{"cell_index":1,"value":"42"}]
    assert rar(b"Rar!\x1a\x07\x00"+struct.pack("<HBHH",0,0x7b,0,7))["end_header_seen"]
    if a.verify:print("PET_KR_STATIC_SELECTION_PASS 15");return
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: rows=list(pool.map(inspect,zip(spec["targets"],prior)))
    print(json.dumps({"schema":"stoneage.pet.kr_static_fields.r1","results":rows,"exact_payloads":sum(x["verified"] for x in rows),"derived_success":sum("derived" in x for x in rows),"new_official_pet_identities":0,"original_payloads_published":False,"native_execution":False},ensure_ascii=False,indent=2))
    assert all(x["verified"] and "derived" in x for x in rows)
if __name__=="__main__":main()
