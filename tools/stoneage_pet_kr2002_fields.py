"""Static evidence extraction from exact verified KR2002 operator snapshots.
No original pages, images or executable/archive bytes are written or published.
No execution of downloaded material. Table cells retain factual labels/numbers only."""
import argparse, base64, collections, concurrent.futures, hashlib, json, re, struct, urllib.parse, urllib.request, urllib.error
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
RECEIPT="research/pets/PET-KR-ARCHIVE-REPLAY-RECEIPT-R1.json"
PREFIX="/images/game_introduce/pet_caractor/"
def read_receipt():
    s=json.loads((ROOT/RECEIPT).read_bytes())
    assert s["verified_exact_payloads"]==len(s["results"])==15
    assert all(x["original_payload_verified"] for x in s["results"])
    assert sum(x["bytes_read"] for x in s["results"])==3071746
    paths={p for x in s["results"] for p in x.get("local_images",[]) if p.startswith(PREFIX)}
    assert len(paths)==159
    numbered={p for p in paths if re.fullmatch(PREFIX+r"4_\d{3}\.gif",p)}
    assert numbered=={PREFIX+f"4_{i:03}.gif" for i in range(1,97)}
    return s
class Node:
    def __init__(self,tag,attrs,parent=None):
        self.tag=tag;self.a=dict(attrs);self.parent=parent;self.children=[]
    def walk(self,tag=None):
        for x in self.children:
            if isinstance(x,Node):
                if tag is None or x.tag==tag:yield x
                yield from x.walk(tag)
    def text(self):
        if self.tag in ("script","style"):return ""
        return " ".join(x.text() if isinstance(x,Node) else x for x in self.children)
class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.root=Node("root",[]);self.cur=self.root
    def handle_starttag(self,tag,attrs):
        if tag in ("td","th") and self.cur.tag in ("td","th"):self.cur=self.cur.parent
        if tag=="tr" and self.cur.tag=="tr":self.cur=self.cur.parent
        n=Node(tag,attrs,self.cur);self.cur.children.append(n)
        if tag not in ("img","br","hr","meta","input","link","area","base","param","col","embed","source","wbr"):self.cur=n
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if self.cur.tag==tag:self.handle_endtag(tag)
    def handle_endtag(self,tag):
        n=self.cur
        while n.parent is not None:
            if n.tag==tag:self.cur=n.parent;return
            n=n.parent
    def handle_data(self,data):self.cur.children.append(data)
def clean(s):return " ".join(s.split())
def imagepath(n,original):
    return urllib.parse.urlsplit(urllib.parse.urljoin(original,n.a.get("src",""))).path
def short_cells(tr):
    cells=[]
    for n in tr.children:
        if not isinstance(n,Node) or n.tag not in ("td","th"):continue
        t=clean(n.text())
        if t and len(t)<=70 and len(t.split())<=14:cells.append(t)
        elif t:cells.append(None)
        else:cells.append("")
    return cells
def parse_page(data,x):
    for enc in ("utf-8","cp949","euc-kr"):
        try:s=data.decode(enc);break
        except UnicodeDecodeError:continue
    else:enc="cp949-replace";s=data.decode("cp949","replace")
    tree=Tree();tree.feed(s)
    refs=[]
    for i,img in enumerate(tree.root.walk("img")):
        p=imagepath(img,x["original"])
        if not p.startswith(PREFIX):continue
        n=img.parent; ancestors=[]
        while n is not None:
            if n.tag=="tr":
                cells=short_cells(n)
                petimgs=[imagepath(z,x["original"]) for z in n.walk("img") if imagepath(z,x["original"]).startswith(PREFIX)]
                if 0<len(petimgs)<=5 and cells:
                    ancestors.append(dict(cells=cells,pet_image_paths=petimgs))
                if len(ancestors)>=3:break
            n=n.parent
        alt=clean(img.a.get("alt",""))
        refs.append(dict(image_ordinal=i,path=p,alt=alt if len(alt)<=40 else None,nearby_table_rows=ancestors))
    expected={p for p in x.get("local_images",[]) if p.startswith(PREFIX)}
    assert {r["path"] for r in refs}==expected,(x["original"],len(refs))
    # Factual numeric/name cells associated with source images only, not full prose.
    return dict(encoding=enc,image_occurrences=refs,unique_pet_image_paths=len(expected))
def static_pe(data):
    assert data[:2]==b"MZ" and len(data)>=64
    off=struct.unpack_from("<I",data,60)[0]; assert data[off:off+4]==b"PE\0\0"
    machine,sections,timestamp,_,_,opt_size,flags=struct.unpack_from("<HHIIIHH",data,off+4)
    sec=[]
    for i in range(sections):
        p=off+24+opt_size+40*i
        assert p+40<=len(data)
        name=data[p:p+8].split(b"\0")[0].decode("ascii","replace")
        vs,va,rs,ra=struct.unpack_from("<IIII",data,p+8)
        sec.append(dict(name=name,virtual_size=vs,raw_size=rs,raw_offset=ra))
    # Only bounded file/resource identifiers, no program logic or executable text.
    terms=sorted(set(x.decode("ascii","replace") for x in re.findall(rb"(?i)[A-Za-z0-9_\-]{2,40}\.(?:exe|dll|dat|bin|ini|bmp|gif|spr|rar|zip|cab|txt)",data)))[:80]
    return dict(format="PE",machine=machine,section_count=sections,coff_timestamp=timestamp,sections=sec,file_tokens=terms,classification="NOT_AUTHENTICATED_GAME_CLIENT")
def static_rar(data):
    if not data.startswith(b"Rar!\x1a\x07\x00"):return dict(format="RAR_OTHER_VERSION",members=[],classification="UNCLASSIFIED_MATERIAL")
    pos=7; members=[]; stop="EOF"
    for _ in range(10000):
        if pos+7>len(data):break
        crc,typ,flags,size=struct.unpack_from("<HBHH",data,pos)
        if size<7 or pos+size>len(data):stop="INVALID_HEADER";break
        packed=0
        if flags&0x8000:
            if pos+11>len(data):stop="TRUNCATED_LONG_HEADER";break
            packed=struct.unpack_from("<I",data,pos+7)[0]
        if typ==0x74:
            if size<32:stop="INVALID_FILE_HEADER";break
            pack,unpack,host,crc32,ftime,ver,method,nlen,attr=struct.unpack_from("<IIBIIBBHI",data,pos+7)
            name_off=32
            if flags&0x100:
                if size<40:stop="INVALID_LARGE_FILE_HEADER";break
                hp,hu=struct.unpack_from("<II",data,pos+32);pack+=hp<<32;unpack+=hu<<32;name_off+=8
            if name_off+nlen>size:stop="INVALID_NAME";break
            name=data[pos+name_off:pos+name_off+nlen].split(b"\0")[0]
            try:name=name.decode("cp949")
            except UnicodeDecodeError:name=name.decode("latin1")
            members.append(dict(name=name[:180],packed_size=pack,unpacked_size=unpack,crc32=f"{crc32:08x}",method=method))
            packed=pack
        if typ==0x7b:stop="END_ARCHIVE";break
        nxt=pos+size+packed
        if nxt<=pos or nxt>len(data):stop="BOUNDS";break
        pos=nxt
    return dict(format="RAR4",members=members,header_scan_end=stop,classification="NOT_AUTHENTICATED_GAME_CLIENT",member_contents_decompressed=False)
def fetch(x):
    result=dict(original=x["original"],timestamp=x["timestamp"],source_sha256=x["sha256"],source_digest=x["cdx_digest"],status="NOT_READ",official_native_identity_verified=False)
    try:
        req=urllib.request.Request(x["final_url"],headers={"User-Agent":"stoneage-rebuild-source-review/1.0","Accept-Encoding":"identity"})
        with urllib.request.urlopen(req,timeout=20) as f:
            data=f.read(8*1024*1024+1);final=f.geturl()
        assert len(data)==x["bytes_read"] and hashlib.sha256(data).hexdigest()==x["sha256"] and base64.b32encode(hashlib.sha1(data).digest()).decode()==x["cdx_digest"] and final==x["final_url"]
        result["status"]="EXACT_REPLAY"
        if x["kind"]=="official_site_page_candidate":result.update(parse_page(data,x))
        elif x["magic"]=="PE_MZ":result["static_material"]=static_pe(data)
        elif x["magic"]=="RAR":result["static_material"]=static_rar(data)
        return result
    except Exception as e:
        result.update(status="REPLAY_OR_PARSE_ERROR",error_type=type(e).__name__,error_detail=str(e)[:160]);return result
def main():
    p=argparse.ArgumentParser();p.add_argument("--verify",action="store_true");a=p.parse_args();s=read_receipt()
    if a.verify:
        print("PET_KR2002_RECEIPT_PASS");return
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(fetch,s["results"]))
    report=dict(schema="stoneage.pet.kr2002.fields.r1",results=results,exact_replays=sum(x["status"]=="EXACT_REPLAY" for x in results),new_official_species_count=None,new_official_identities=0,original_payloads_published=False)
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
