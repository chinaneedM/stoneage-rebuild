"""Pin the GitHub Actions source artifact ZIP and its exact Git-derived JSON."""
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPO="chinaneedM/stoneage-rebuild"
RUN=40091960688
JOB=120866302979
ARTIFACT=12559626425
SOURCE_HEAD="18f9a50f3af402d1c8447bd274fd830ee33d1a3d"
GIT_BLOB="7eef214be6f6b4f70e96c5c04c5fe31dd36165b3"
FILE="research/recovered/STONEAGE-TW10-CN50-REAL-RECORD-DIFF-R1.json"


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def blob_sha(blob):
    return hashlib.sha1(b"blob "+str(len(blob)).encode()+b"\0"+blob).hexdigest()


def verify_zip(archive, expected):
    with zipfile.ZipFile(io.BytesIO(archive)) as f:
        records=[x for x in f.infolist() if not x.is_dir()]
        if len(records)!=1 or not records[0].filename.endswith(".json") or records[0].file_size>1024*1024:
            raise ValueError("unexpected-archive-members")
        raw=f.read(records[0])
    if raw!=expected:
        raise ValueError("raw-metadata-does-not-match-Git")
    j=json.loads(raw)
    if j.get("result")!="DERIVED_RECORD_LEVEL_DIFF_OF_REACQUIRED_ORIGINAL_RESOURCE_BYTES":
        raise ValueError("not-original-byte-derived-report")
    return {"entry":records[0].filename,"zip_bytes":len(archive),"zip_sha256":sha256(archive),
            "raw_bytes":len(raw),"raw_sha256":sha256(raw)}


def api_json(path,token):
    req=urllib.request.Request("https://api.github.com/repos/"+REPO+path,headers={
        "Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
        "User-Agent":"StoneAge-Custody","X-GitHub-Api-Version":"2022-11-28"})
    with urllib.request.urlopen(req,timeout=45) as r:
        return json.load(r)


def read_zip(token):
    req=urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/actions/artifacts/{ARTIFACT}/zip",
        headers={"Authorization":"Bearer "+token,"User-Agent":"StoneAge-Custody"})
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl):
            return None
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=45) as r:
            if r.status!=200:
                raise ValueError("bad-archive-http-status")
            data=r.read(3000001)
    except urllib.error.HTTPError as e:
        if e.code not in (302,303,307,308):
            raise
        location=e.headers.get("Location") or ""
        url=urllib.parse.urlsplit(location)
        if not (url.scheme=="https" and url.hostname and
                (url.hostname.endswith(".blob.core.windows.net")
                 or url.hostname.endswith(".githubusercontent.com"))):
            raise ValueError("unsafe-archive-redirect-host")
        # Signed Azure/GitHub artifact link: never forward the GitHub token.
        with urllib.request.urlopen(urllib.request.Request(location,headers={
                "User-Agent":"StoneAge-Custody"}),timeout=100) as r:
            data=r.read(3000001)
    if len(data)>3000000:
        raise ValueError("unexpected-large-derived-artifact")
    return data


def build(root,token):
    raw=(root/FILE).read_bytes()
    if blob_sha(raw)!=GIT_BLOB:
        raise ValueError("pinned-Git-blob-missing")
    run=api_json(f"/actions/runs/{RUN}",token)
    job=api_json(f"/actions/jobs/{JOB}",token)
    artifact=api_json(f"/actions/artifacts/{ARTIFACT}",token)
    if run.get("head_sha")!=SOURCE_HEAD or (run.get("status"),run.get("conclusion"))!=("completed","success"):
        raise ValueError("invalid-original-source-run")
    if job.get("run_id")!=RUN or (job.get("status"),job.get("conclusion"))!=("completed","success"):
        raise ValueError("invalid-original-source-job")
    if artifact.get("expired") is not False or artifact.get("workflow_run",{}).get("id")!=RUN:
        raise ValueError("wrong-source-artifact")
    report=verify_zip(read_zip(token),raw)
    if report["zip_bytes"]!=artifact.get("size_in_bytes"):
        raise ValueError("archive-size-not-matching-provider")
    return {"schema":"stoneage.tw10_cn50.original_record_source_custody_r1",
            "source_run":RUN,"source_job":JOB,"source_head":SOURCE_HEAD,
            "source_artifact":ARTIFACT,"source_artifact_name":artifact["name"],
            "report_path":FILE,"report_blob_sha":GIT_BLOB,
            "report_raw_sha256":report["raw_sha256"],"report_bytes":report["raw_bytes"],
            "artifact_zip_sha256":report["zip_sha256"],"artifact_zip_bytes":report["zip_bytes"],
            "artifact_json_entry":report["entry"],
            "result":"ACTUAL_CI_ZIP_JSON_EQUAL_IMMUTABLE_GIT_REPORT",
            "original_client_binaries_preserved_in_Git":False,
            "official_pressing_mastering_independently_authenticated":False,
            "original_server_data_inferred":False}


def main():
    token=os.getenv("GH_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN required")
    data=build(Path(__file__).resolve().parents[1],token)
    output=Path(sys.argv[1]);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print(f"CUSTODY|zip_sha256={data['artifact_zip_sha256']}|raw_sha256={data['report_raw_sha256']}")


if __name__=="__main__":
    main()
