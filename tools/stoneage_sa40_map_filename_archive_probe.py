#!/usr/bin/env python3
"""Archive-domain filename probe for the dated StoneAge 4.0 full-map patch.

The 2002-11-08 Sina download record exposes the source-derived basename
shiqi4updatex_02_11_08.zip, while the historical CGI object itself has no
capture in the exact-URL probes. This probe searches only Sina archive-domain
indexes for that exact basename. Metadata only; no package payload is fetched.
"""

from __future__ import annotations

import concurrent.futures
import json
import urllib.parse
import urllib.request

UA="stoneage-rebuild-archaeology/1.0"
CDX="https://web.archive.org/cdx/search/cdx"
BASENAME="shiqi4updatex_02_11_08.zip"
PUBLISHED_DATE="20021108"
WINDOWS=(
    ("2002-post","20021108","20021231"),
    ("2003","20030101","20031231"),
    ("2004","20040101","20041231"),
    ("2005","20050101","20051231"),
)

# Both scopes are directly grounded in the historical Sina download surface.
# games.sina.com.cn domain matching also covers archived dN.games.sina.com.cn
# delivery hosts without inventing any concrete dN hostname.
SCOPES=(
    ("games1-sina","games1.sina.com.cn"),
    ("games-sina-domain","games.sina.com.cn"),
)


def clean(value,limit=1800):
    text=" ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch>=" " and ch!="\x7f").replace("|","%7C")[:limit]


def fetch_bytes(url,timeout=30):
    req=urllib.request.Request(
        url,
        headers={
            "User-Agent":UA,
            "Accept":"application/json,text/plain;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req,timeout=timeout) as response:
        return int(getattr(response,"status",response.getcode())),response.geturl(),response.read()


def parse_cdx_json(body):
    data=json.loads(body.decode("utf-8"))
    if not isinstance(data,list) or not data:
        return ()
    header=data[0]
    if not isinstance(header,list) or not all(isinstance(x,str) for x in header):
        return ()
    rows=[]
    for raw in data[1:]:
        if not isinstance(raw,list):
            continue
        row=dict(zip(header,raw))
        rows.append(row)
    return tuple(rows)


def cdx_url(domain,date_from,date_to):
    filters=[
        "statuscode:200",
        "original:.*shiqi4updatex_02_11_08[.]zip.*",
    ]
    params=[
        ("url",domain),
        ("matchType","domain"),
        ("output","json"),
        ("fl","timestamp,original,statuscode,mimetype,digest,length"),
        ("from",date_from),
        ("to",date_to),
        ("collapse","digest"),
        ("limit","500"),
    ]
    params.extend(("filter",value) for value in filters)
    return CDX+"?"+urllib.parse.urlencode(params)


def probe_scope(label,domain,window_label,date_from,date_to):
    endpoint=cdx_url(domain,date_from,date_to)
    status,final,body=fetch_bytes(endpoint,timeout=20)
    rows=parse_cdx_json(body)
    return {
        "label":label,
        "domain":domain,
        "window_label":window_label,
        "date_from":date_from,
        "date_to":date_to,
        "endpoint":endpoint,
        "status":status,
        "final":final,
        "rows":rows,
        "body_bytes":len(body),
    }


def main():
    print("StoneAge 4.0 full-map patch filename archive-domain probe — R1")
    print("SCOPE|source-derived-exact-basename+Sina-domain-CDX|metadata-only|no-payload-download")
    print(f"TARGET|published_date={PUBLISHED_DATE}|basename={BASENAME}|windows={len(WINDOWS)}")

    errors=[]
    hits=[]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures={}
        for label,domain in SCOPES:
            for window_label,date_from,date_to in WINDOWS:
                future=executor.submit(probe_scope,label,domain,window_label,date_from,date_to)
                futures[future]=(label,domain,window_label,date_from,date_to)
        for future in concurrent.futures.as_completed(futures):
            label,domain,window_label,date_from,date_to=futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                errors.append((f"{label}:{window_label}",type(exc).__name__,str(exc)))

    for result in sorted(results,key=lambda row:(row["label"],row["date_from"])):
        label=result["label"]
        print(
            f"CDX|label={label}|domain={result['domain']}|window={result['window_label']}|"
            f"from={result['date_from']}|to={result['date_to']}|status={result['status']}|"
            f"body_bytes={result['body_bytes']}|rows={len(result['rows'])}|final={clean(result['final'])}"
        )
        for row in result["rows"]:
            original=str(row.get("original") or "")
            if BASENAME.lower() not in original.lower():
                continue
            key=(str(row.get("timestamp") or ""),original,str(row.get("digest") or ""))
            if key not in hits:
                hits.append(key)
            print(
                f"CDX_HIT|label={label}|window={result['window_label']}|timestamp={clean(row.get('timestamp'))}|"
                f"original={clean(original)}|statuscode={clean(row.get('statuscode'))}|"
                f"mimetype={clean(row.get('mimetype'))}|digest={clean(row.get('digest'))}|"
                f"length={clean(row.get('length'))}"
            )

    for label,kind,message in sorted(errors):
        print(f"ERROR|scope={clean(label)}|kind={clean(kind)}|message={clean(message)}")

    print(f"COUNT|scopes|{len(SCOPES)}")
    print(f"COUNT|windows|{len(WINDOWS)}")
    print(f"COUNT|unique_hits|{len(hits)}")
    print(f"COUNT|errors|{len(errors)}")
    if hits:
        print("RESOLUTION|SA40_FILENAME_ARCHIVE_HIT|verify capture identity and recover transiently before any map comparison")
    elif errors:
        print("RESOLUTION|PARTIAL_NO_HIT|one or more Sina filename-domain archive surfaces were unavailable")
    else:
        print("RESOLUTION|SA40_FILENAME_ARCHIVE_NO_HIT|bounded Sina filename-domain CDX search returned no capture")


if __name__=="__main__":
    main()
