"""R38: exact previously observed archived operator GIFs, sealed private custody."""
import argparse, base64, hashlib, io, json, tempfile, time, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "research/pets/PET-ATLAS-R38-JP-KR-GIF-CUSTODY-PLAN-R1.json"
PLAN_PIN = "e6318f40b462ee6963a5c4700c8f759ac320920c"
KEY_PIN = "d0429134219d9e95b2d080825389227d3c17718d"
CAP = 256000

def blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def read(path, pin):
    raw = path.read_bytes()
    assert blob(raw) == pin, path
    return json.loads(raw)

def targets():
    plan = read(PLAN, PLAN_PIN)
    a,b,c,d = [read(ROOT / p, h) for p,h in plan["receipt_pins"].items()]
    expected = {}
    def add(k, digest, stamp, url):
        if not digest:
            return
        old = expected.get(k)
        assert old is None or old[0] == digest
        if old is None:
            expected[k] = digest,stamp,url
    for x in a["records"]:
        add(("JP",x["web_ordinal"]),x["best_archival_observation_sha256_or_null"],x["best_archival_observation_capture_or_null"],x["original_image_url"])
    for x in b["records"]:
        add(("JP",x["web_ordinal"]),x["image_original_sha256_or_null"],x["image_observed_archive_capture_or_null"],x["historical_operator_original_image_url"])
    for x in b["independent_followup_after_initial_receipt"]["records"]:
        add(("JP",x["web_ordinal"]),x["image_original_sha256_or_null"],x["image_archive_capture_or_null"],x["original_image_url"])
    for x in c["results"]+d["results"]:
        if x["verified"]:
            add(("KR",x["original"]),x["sha256"],x["timestamp"],x["original"])
    rows=plan["targets"]
    actual={(x["region"],x.get("ordinal",x["original"])):(x["sha256"],x["timestamp"],x["original"]) for x in rows}
    assert len(rows)==len(actual)==len(expected)==70 and actual==expected
    assert sum(x["region"]=="JP" for x in rows)==38
    assert sum(x["region"]=="KR" for x in rows)==32
    assert len({x["sha256"] for x in rows})==70
    return rows

def verify(raw, row):
    assert 0<len(raw)<=CAP
    assert hashlib.sha256(raw).hexdigest()==row["sha256"], "SHA256 mismatch"
    if "bytes" in row:
        assert len(raw)==row["bytes"]
    if "cdx_digest" in row:
        assert base64.b32encode(hashlib.sha1(raw).digest()).decode()==row["cdx_digest"]
    with Image.open(io.BytesIO(raw)) as im:
        assert im.format=="GIF" and im.size==(row["width"],row["height"])
        count=im.n_frames
        assert 1<=count<=256
        if "frames" in row:
            assert count==row["frames"]
        for i in range(count):
            im.seek(i)
            im.convert("RGBA").load()
    return count

def selftest():
    f=io.BytesIO()
    Image.new("P",(2,3)).save(f,format="GIF")
    raw=f.getvalue()
    row={"sha256":hashlib.sha256(raw).hexdigest(),"width":2,"height":3,"frames":1}
    assert verify(raw,row)==1
    for bad in (b"not gif",raw+b"x"):
        try:
            verify(bad,row)
        except AssertionError:
            pass
        else:
            raise AssertionError("invalid payload accepted")


def seal_gifs(private, public, out):
    """R38-specific strict GIF allowlist; leave R4's PNG policy untouched."""
    import re, secrets, zipfile
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes, serialization
    receipt=json.loads((private/"receipt.json").read_text(encoding="utf-8"))
    expected={"receipt.json"}
    for x in receipt["results"]:
        if x["verified"]:
            name=x["path"]
            assert re.fullmatch(r"(jp|kr)-[0-9]{3}\.gif",name)
            assert name not in expected
            expected.add(name)
            verify((private/name).read_bytes(),x["target"])
    files=list(private.iterdir())
    assert {x.name for x in files}==expected
    assert all(x.is_file() and not x.is_symlink() for x in files)
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):
            z.write(p,p.name)
    raw=buf.getvalue()
    pub=serialization.load_pem_public_key(public.read_bytes())
    key=AESGCM.generate_key(bit_length=256)
    nonce=secrets.token_bytes(12)
    aad=b"stoneage-pet-atlas-r4-private-source"
    enc=AESGCM(key).encrypt(nonce,raw,aad)
    wrapped=pub.encrypt(key,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    envelope=dict(schema="stoneage.pet.atlas_r4.envelope.r1",cipher_sha256=hashlib.sha256(enc).hexdigest(),plain_sha256=hashlib.sha256(raw).hexdigest(),plain_bytes=len(raw),cipher_bytes=len(enc),nonce=base64.b64encode(nonce).decode(),wrapped_key=base64.b64encode(wrapped).decode(),aad=aad.decode())
    out.mkdir(parents=True,exist_ok=False)
    (out/"private.enc").write_bytes(enc)
    (out/"envelope.json").write_text(json.dumps(envelope,sort_keys=True))
    return envelope

def seal_selftest():
    import zipfile
    from cryptography.hazmat.primitives.asymmetric import rsa,padding
    from cryptography.hazmat.primitives import hashes,serialization
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    f=io.BytesIO()
    Image.new("P",(2,3)).save(f,format="GIF")
    raw=f.getvalue()
    row={"sha256":hashlib.sha256(raw).hexdigest(),"width":2,"height":3,"frames":1}
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        source=root/"source"
        source.mkdir()
        (source/"jp-001.gif").write_bytes(raw)
        (source/"receipt.json").write_text(json.dumps({"results":[{"verified":True,"path":"jp-001.gif","target":row}]}))
        priv=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        pub=root/"public.pem"
        pub.write_bytes(priv.public_key().public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
        out=root/"sealed"
        e=seal_gifs(source,pub,out)
        cipher=(out/"private.enc").read_bytes()
        assert len(cipher)==e["cipher_bytes"] and hashlib.sha256(cipher).hexdigest()==e["cipher_sha256"]
        key=priv.decrypt(base64.b64decode(e["wrapped_key"]),padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        plain=AESGCM(key).decrypt(base64.b64decode(e["nonce"]),cipher,e["aad"].encode())
        assert len(plain)==e["plain_bytes"] and hashlib.sha256(plain).hexdigest()==e["plain_sha256"]
        with zipfile.ZipFile(io.BytesIO(plain)) as z:
            assert z.testzip() is None and set(z.namelist())=={"receipt.json","jp-001.gif"} and z.read("jp-001.gif")==raw
        (source/"unexpected.exe").write_bytes(b"x")
        try:
            seal_gifs(source,pub,root/"rejected")
        except AssertionError:
            assert not (root/"rejected").exists()
        else:
            raise AssertionError("unexpected member accepted")
    print("R38_SEAL_ROUNDTRIP=PASS",flush=True)

class ExactRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Exact capture only; archive redirects are not evidence of this target.
        raise ValueError("redirect rejected")

def export(region, out, pub):
    assert blob(pub.read_bytes())==KEY_PIN
    rows=[x for x in targets() if x["region"]==region]
    # Only re-fetch bytes actually read but lost due to the packaging defect.
    selected={"JP":set(range(1,21)),"KR":set(range(1,9))|set(range(19,25))}[region]
    opener=urllib.request.build_opener(ExactRedirect())
    results=[]
    with tempfile.TemporaryDirectory(prefix="pet-r38-") as tmp:
        folder=Path(tmp)
        for i,row in enumerate(rows,1):
            if i not in selected:
                continue
            url="https://web.archive.org/web/"+row["timestamp"]+"id_/"+row["original"]
            entry={"target":row,"capture_url":url,"verified":False,"path":None}
            try:
                req=urllib.request.Request(url,headers={"User-Agent":"StoneAge historical source verification/1.0"})
                with opener.open(req,timeout=12) as response:
                    assert response.status==200 and response.geturl()==url
                    raw=response.read(CAP+1)
                frames=verify(raw,row)
                path=f"{region.lower()}-{i:03d}.gif"
                (folder/path).write_bytes(raw)
                entry.update(verified=True,path=path,bytes=len(raw),frames=frames)
            except Exception as exc:
                entry["error"]=type(exc).__name__+": "+str(exc)[:180]
            results.append(entry)
            print("R38_RESULT="+json.dumps({"region":region,"index":i,"verified":entry["verified"],"error":entry.get("error")}),flush=True)
            time.sleep(1)
        receipt={"schema":"stoneage.pet.atlas_r38.private_web_gif_receipt.r1","region":region,"plan_blob":PLAN_PIN,"results":results,"native_client_identity_verified":False,"original_assets_published":False}
        (folder/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True),encoding="utf-8")
        envelope=seal_gifs(folder,pub,out)
        print("R38_SEALED="+json.dumps({"region":region,"verified":sum(x["verified"] for x in results),"target_count":len(rows),"cipher_sha256":envelope["cipher_sha256"]}),flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--plan-only",action="store_true")
    p.add_argument("--region",choices=["JP","KR"])
    p.add_argument("--output",type=Path)
    p.add_argument("--public-key",type=Path)
    args=p.parse_args()
    selftest()
    seal_selftest()
    rows=targets()
    print("R38_PLAN="+json.dumps({"JP":38,"KR":32,"count":len(rows),"plan_blob":PLAN_PIN}),flush=True)
    if not args.plan_only:
        assert args.region and args.output and args.public_key
        export(args.region,args.output,args.public_key)
if __name__=="__main__":
    main()
