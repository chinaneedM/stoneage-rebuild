"""Independent small original 2013 operator updater and CDX resource path index."""
import base64,hashlib,json,re,struct,urllib.request,urllib.parse
from pathlib import Path
from tools import stoneage_pet_high_first_116_cn85_file_archive as src
from tools import stoneage_pet_high_first_109_cn75_custody as prior
REPORT=src.P/"PET-CN2013-UPDATER-RESOURCE-INDEX-R1.json"
UPDATER="http://update5.cinsgame.com/saupdate/StoneAge.exe"
PREFIX="http://update5.cinsgame.com/saupdate/"
CAP=2*1024*1024
def sha(raw):return hashlib.sha256(raw).hexdigest()
def capture(url,cap):
    row=dict(url=url)
    try:
        req=urllib.request.Request(url,headers={"Accept-Encoding":"identity","User-Agent":"stoneage-rebuild-archaeology/1.0"})
        with urllib.request.build_opener(src.NoFollow()).open(req,timeout=35) as f:
            raw=f.read(cap+1);row.update(status=f.status,content_type=f.headers.get("Content-Type"),response_bytes=len(raw),response_sha256=sha(raw))
            if len(raw)>cap:return row|dict(result="BOUNDED_CAP_EXCEEDED"),None
            if f.status!=200:return row|dict(result="NOT_HTTP_200"),None
        return row|dict(result="HTTP_200_BOUNDED"),raw
    except (OSError,ValueError) as e:return row|dict(result="ACCESS_ERROR",error_type=type(e).__name__,error=str(e)[:180]),None
def pe_meta(raw):
    if len(raw)<64 or raw[:2]!=b"MZ":raise ValueError("not MZ")
    off=struct.unpack_from("<I",raw,60)[0]
    if off+24>len(raw) or raw[off:off+4]!=b"PE\0\0":raise ValueError("not PE")
    machine,n,ts,_,_,optional,flags=struct.unpack_from("<HHIIIHH",raw,off+4)
    if not 1<=n<=96 or off+24+optional+40*n>len(raw):raise ValueError("invalid sections")
    sections=[]
    for i in range(n):
        x=off+24+optional+40*i
        size,pos=struct.unpack_from("<II",raw,x+16)
        if size and pos+size>len(raw):raise ValueError("truncated PE")
        name=raw[x:x+8].split(b"\0",1)[0].decode("ascii","replace")
        sections.append(dict(name=name,raw_size=size,raw_offset=pos))
    return dict(machine=machine,coff_timestamp=ts,sections=sections)
def index():
    q="https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(dict(url=PREFIX,matchType="prefix",output="json",**{"from":"2010","to":"2016"},limit=200,fl="timestamp,original,statuscode,mimetype,digest,length"))
    row,raw=capture(q,CAP);row["entries"]=[]
    if raw is None:return row
    try:
        d=json.loads(raw);assert isinstance(d,list)
        if d:assert d[0]==["timestamp","original","statuscode","mimetype","digest","length"]
        row["raw_count"]=max(0,len(d)-1);row["limit_reached"]=row["raw_count"]>=200
        for item in d[1:]:
            assert len(item)==6
            rec=dict(zip(d[0],item));u=urllib.parse.urlsplit(rec["original"])
            if u.hostname!="update5.cinsgame.com" or not u.path.casefold().startswith("/saupdate/") or u.query:continue
            if rec["statuscode"]!="200":continue
            # Paths only, no response bodies or account identifiers.
            if not re.search(r"\.(?:exe|dll|bin|dat|ini|txt|zip|rar|cab|lst|xml|pak|cfg)$",u.path,re.I):continue
            row["entries"].append(rec)
        row["result"]="INDEX_PARSED"
    except (ValueError,AssertionError,TypeError,KeyError) as e:row["result"]="INDEX_PARSE_ERROR";row["error_type"]=type(e).__name__
    return row
def main():
    source=json.loads(src.R.parent.joinpath("PET-HIGH-FIRST-116-CN85-EXACT-FILE-ARCHIVE-R1.json").read_bytes())
    r=[x for x in source["prefix_results"] if x["target"]==UPDATER];assert len(r)==1
    x=r[0];assert x["cdx"]["timestamp"]=="20130130111551" and x["cdx"]["digest"]=="XFFGC5Y643VKHJTY7YOUB3L73BUPZ7DF" and x["result"]=="ACCESS_OR_PARSE_ERROR"
    row,raw=capture(x["replay_url"],CAP);row["cdx"]=x["cdx"]
    if raw is not None:
        row["sha1_base32"]=base64.b32encode(hashlib.sha1(raw).digest()).decode()
        row["cdx_digest_matches"]=row["sha1_base32"]==x["cdx"]["digest"]
        try:row["pe"]=pe_meta(raw)
        except (ValueError,struct.error) as e:row["pe_error"]=str(e)
        row["verified_original_updater"]=bool(row.get("pe") and row["cdx_digest_matches"])
        if row["verified_original_updater"]:
            # Publish only known operator resource-path tokens, not arbitrary binary strings.
            tokens=set()
            for match in re.finditer(rb"(?i)(?:[a-z0-9_-]+[/\\]){0,4}(?:album_\d+\.dat|(?:adrn|real|spradrn|spr)_\d+\.bin|petlifetype\.bin|sa_85_free\.exe|sa_25_payment\.exe|stoneageng\.dll)",raw):
                tokens.add(match.group().decode("ascii"))
            row["resource_path_tokens"]=sorted(tokens)
    d=dict(schema="stoneage.pet.cn2013.updater_resource_index.r1",prior_source_git_blob=src.idx.blob(src.R.parent.joinpath("PET-HIGH-FIRST-116-CN85-EXACT-FILE-ARCHIVE-R1.json").read_bytes()),updater=row,index=index(),official_closures=0,pet_payload_extracted=False,original_assets_published=False,original_client_verified=False)
    REPORT.write_bytes(prior.dump(d))
    print("PET_CN2013_REPORT_SHA256="+sha(REPORT.read_bytes()))
    print("PET_CN2013_SUMMARY="+json.dumps(d,ensure_ascii=False))
if __name__=="__main__":main()
