"""Independently verify updater receipt, then inspect exact original launcher for public update paths."""
import argparse,base64,hashlib,json,re,urllib.parse,zipfile
from pathlib import Path
from tools import stoneage_pet_cn2013_updater_resource_index as prev
from tools import stoneage_pet_high_first_109_cn75_custody as prior
REPORT=prev.REPORT.parent/"PET-CN2013-UPDATER-PATH-WITNESSES-R1.json"
SHA="f6098c7274365e9a2398814047290f27f4adc9a8aa352703b1680d51ca901123"
ZIP="7e28b1cc5a78f1e4f71362830eefdb0850f37976a387455a673e2a45efbc8db7"
BLOB="ad3eb30198ef62ee0e9adfe81cebace70bb86f59"
EXE="e926a5f5a0eb6ae409b680a6a57f2ced65137328332e4efebcd92cb6f21d1a2e"
def sha(b):return hashlib.sha256(b).hexdigest()
def receipt(path):
    assert path.stat().st_size==1074 and sha(path.read_bytes())==ZIP
    with zipfile.ZipFile(path) as z:
        assert len(z.namelist())==1
        raw=z.read(z.namelist()[0])
    assert raw==prev.REPORT.read_bytes() and sha(raw)==SHA and prev.src.idx.blob(raw)==BLOB
    d=json.loads(raw);u=d["updater"]
    assert u["verified_original_updater"] and u["cdx_digest_matches"] and u["response_bytes"]==118784 and u["response_sha256"]==EXE
    assert u["resource_path_tokens"]==["sa_25_payment.exe","sa_85_free.exe"]
    assert not d["original_assets_published"] and d["official_closures"]==0
    assert d["index"]["result"]=="ACCESS_ERROR"
    return u
def scan(raw):
    # Only public operator hosts and finite resource filename tokens. Never
    # publish arbitrary binary strings, credentials, query strings or keys.
    rows=set()
    pat=r"(?i)(?:https?://)?(?:[a-z0-9-]+\.)*(?:cinsgame\.com|cins\.cn)(?::[0-9]{1,5})?(?:/[a-z0-9_.%/-]{0,180})?"
    paths=r"(?i)(?<![a-z0-9_.-])(?:[a-z0-9_-]+[/\\]){0,5}(?:[a-z0-9_-]*(?:update|patch|version|filelist|download|serverlist|stoneage|sa_85_free|sa_25_payment|album|adrn|real|spradrn|spr|petlife)[a-z0-9_.-]*\.(?:ini|txt|lst|xml|cfg|exe|dll|dat|bin|zip|rar|cab))(?![a-z0-9_.-])"
    for encoding in ("ascii","utf16le_even","utf16le_odd"):
        if encoding=="ascii":
            data=raw.decode("latin1");factor=1;offset=0
        else:
            offset=int(encoding.endswith("odd"));data=raw[offset:].decode("utf-16le","replace");factor=2
        for kind,pattern in (("OPERATOR_HOST_OR_PATH_LITERAL",pat),("RESOURCE_OR_UPDATE_FILENAME_LITERAL",paths)):
            for m in re.finditer(pattern,data):
                token=m.group();pos=offset+m.start()*factor
                # Domain suffix must end at boundary; no embedded unrelated domains.
                if kind.startswith("OPERATOR") and m.end()<len(data) and data[m.end()] in ".@":continue
                rows.add((kind,token,encoding,pos))
    return [dict(kind=k,token=t,encoding=e,file_offset=o) for k,t,e,o in sorted(rows)]
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--artifact",type=Path,required=True);a=ap.parse_args()
    u=receipt(a.artifact)
    row,raw=prev.capture(u["url"],prev.CAP)
    candidates=[]
    if raw is not None:
        row["identity_matches"]=len(raw)==118784 and sha(raw)==EXE and base64.b32encode(hashlib.sha1(raw).digest()).decode()==u["cdx"]["digest"]
        if row["identity_matches"]:
            assert prev.pe_meta(raw)==u["pe"]
            candidates=scan(raw)
    d=dict(schema="stoneage.pet.cn2013.updater_path_witnesses.r1",prior_artifact=15119463843,prior_zip_sha256=ZIP,prior_report_sha256=SHA,prior_report_git_blob=BLOB,reacquisition=row,path_literals=candidates,original_assets_published=False,original_client_verified=False,official_closures=0,pet_payload_extracted=False)
    REPORT.write_bytes(prior.dump(d));print("PET_CN2013_PATHS_SHA256="+sha(REPORT.read_bytes()),flush=True)
    print("PET_CN2013_PATHS="+json.dumps(d,ensure_ascii=False),flush=True)
if __name__=="__main__":main()
