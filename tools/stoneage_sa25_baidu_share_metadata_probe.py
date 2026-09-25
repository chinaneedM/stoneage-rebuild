#!/usr/bin/env python3
"""Probe public Baidu share metadata for StoneAge 2.5 recovery leads.

Only public GET requests are used. Known extraction codes must already be
published by a source. The probe does not log in, guess passwords, download
payload files, or execute anything. It emits page fingerprints and any
filename/size metadata literally exposed by the public share HTML.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import urllib.parse
import urllib.request
import http.cookiejar

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"

TARGETS = (
    ("judingwan-25", "1nu7DLcX", "ylru"),
    ("judingwan-25-legacy", "1eS9MzOe", "qnsv"),
    ("246sa-25", "1cHlV27B0rckWGC2cH21dGg", "7ck4"),
    ("cangbaowan-25", "1a2cOmPxo5GjFPFfU5Mj2Ug", ""),
)

STATUS_PHRASES = (
    ("MISSING", ("链接不存在", "页面不存在", "文件不存在", "分享的文件不存在", "分享的文件已经被取消", "分享的文件已经被删除", "啊哦，你来晚了")),
    ("EXPIRED", ("分享链接已过期", "链接已失效", "分享已过期")),
    ("NEEDS_CODE", ("请输入提取码", "提取文件", "提取码")),
)

NAME_PATTERNS = (
    re.compile(r'"server_filename"\s*:\s*"((?:\\.|[^"])*)"', re.I),
    re.compile(r'"filename"\s*:\s*"((?:\\.|[^"])*)"', re.I),
    re.compile(r'"path"\s*:\s*"((?:\\.|[^"])*)"', re.I),
)
SIZE_RE = re.compile(r'"size"\s*:\s*(?:"(\d+)"|(\d+))', re.I)
FSID_RE = re.compile(r'"fs_id"\s*:\s*(?:"(\d+)"|(\d+))', re.I)
SHAREID_RE = re.compile(r'"shareid"\s*:\s*(?:"(\d+)"|(\d+))', re.I)
UK_RE = re.compile(r'"uk"\s*:\s*(?:"(\d+)"|(\d+))', re.I)
TITLE_RE = re.compile(r"(?is)<title[^>]*>(.*?)</title>")

def clean(v: object, n: int = 1200) -> str:
    return " ".join(str(v if v is not None else "").split()).replace("|", "%7C")[:n]

def decode_js_string(s: str) -> str:
    try:
        return json.loads('"' + s + '"')
    except Exception:
        return html.unescape(s.replace("\\/", "/"))

def extract_names(text: str) -> tuple[str, ...]:
    out: list[str] = []
    seen: set[str] = set()
    for pat in NAME_PATTERNS:
        for m in pat.finditer(text):
            v = decode_js_string(m.group(1))
            if not v or v in seen:
                continue
            seen.add(v)
            out.append(v)
    return tuple(out)

def extract_ints(pat: re.Pattern[str], text: str) -> tuple[int, ...]:
    vals: list[int] = []
    for m in pat.finditer(text):
        raw = m.group(1) or m.group(2)
        try:
            vals.append(int(raw))
        except Exception:
            pass
    return tuple(dict.fromkeys(vals))

def classify(text: str, names: tuple[str, ...]) -> str:
    for label, phrases in STATUS_PHRASES:
        if any(p in text for p in phrases):
            if label == "NEEDS_CODE" and names:
                continue
            return label
    if names:
        return "PUBLIC_METADATA_EXPOSED"
    return "PAGE_RETRIEVED_METADATA_UNRESOLVED"

def _read_response(r) -> tuple[int, str, dict[str, str], bytes]:
    body = r.read(5_000_001)
    if len(body) > 5_000_000:
        raise ValueError("page-too-large")
    return int(getattr(r, "status", r.getcode())), r.geturl(), dict(r.headers.items()), body

def _headers(referer: str | None = None) -> dict[str, str]:
    out = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/json,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.5",
    }
    if referer:
        out["Referer"] = referer
    return out

def fetch_share(share_id: str, pwd: str) -> tuple[int, str, dict[str, str], bytes]:
    base = f"https://pan.baidu.com/s/{share_id}"
    url = base + (f"?pwd={urllib.parse.quote(pwd)}" if pwd else "")
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=35) as r:
        return _read_response(r)

def verify_published_code(share_id: str, pwd: str) -> tuple[dict[str, object], tuple[int, str, dict[str, str], bytes] | None]:
    """Submit only a source-published extraction code, then re-read the public page.

    No account/login is used and no file download endpoint is called.
    """
    short = share_id[1:] if share_id.startswith("1") else share_id
    base = f"https://pan.baidu.com/s/{share_id}"
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    # Prime anonymous share cookies required by Baidu's normal web flow.
    req = urllib.request.Request(base, headers=_headers())
    with opener.open(req, timeout=35) as r:
        _read_response(r)

    verify_url = (
        "https://pan.baidu.com/share/verify?"
        + urllib.parse.urlencode({
            "channel": "chunlei",
            "clienttype": "0",
            "web": "1",
            "app_id": "250528",
            "surl": short,
        })
    )
    data = urllib.parse.urlencode({"pwd": pwd}).encode("ascii")
    req = urllib.request.Request(
        verify_url,
        data=data,
        headers={**_headers(base), "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with opener.open(req, timeout=35) as r:
        _, _, _, verify_body = _read_response(r)
    try:
        result = json.loads(verify_body.decode("utf-8", "replace"))
    except Exception:
        result = {"parse_error": True, "body_sha256": hashlib.sha256(verify_body).hexdigest()}

    if result.get("errno") != 0:
        return result, None

    # Some responses provide randsk even when a Set-Cookie is not persisted.
    randsk = str(result.get("randsk") or "")
    headers = _headers(base)
    if randsk:
        headers["Cookie"] = "BDCLND=" + randsk
    req = urllib.request.Request(base, headers=headers)
    with opener.open(req, timeout=35) as r:
        return result, _read_response(r)

def analyze(label: str, share_id: str, pwd: str, body: bytes, final: str) -> list[str]:
    text = body.decode("utf-8", "replace")
    names = extract_names(text)
    sizes = extract_ints(SIZE_RE, text)
    fsids = extract_ints(FSID_RE, text)
    shareids = extract_ints(SHAREID_RE, text)
    uks = extract_ints(UK_RE, text)
    tm = TITLE_RE.search(text)
    title = html.unescape(re.sub(r"(?is)<[^>]+>", " ", tm.group(1))).strip() if tm else ""
    lines = [
        f"SHARE|label={clean(label)}|id={clean(share_id)}|pwd_known={1 if pwd else 0}|final={clean(final,3000)}",
        f"PAGE|label={clean(label)}|bytes={len(body)}|sha256={hashlib.sha256(body).hexdigest()}|title={clean(title,1000)}",
        f"STATUS|label={clean(label)}|value={classify(text,names)}|names={len(names)}|sizes={len(sizes)}|fsids={len(fsids)}|shareids={len(shareids)}|uks={len(uks)}",
    ]
    for i, name in enumerate(names[:200], 1):
        lines.append(f"NAME|label={clean(label)}|index={i}|value={clean(name,3000)}")
    for i, size in enumerate(sizes[:200], 1):
        lines.append(f"SIZE|label={clean(label)}|index={i}|value={size}")
    for i, fsid in enumerate(fsids[:100], 1):
        lines.append(f"FS_ID|label={clean(label)}|index={i}|value={fsid}")
    for i, value in enumerate(shareids[:30], 1):
        lines.append(f"SHARE_ID_META|label={clean(label)}|index={i}|value={value}")
    for i, value in enumerate(uks[:30], 1):
        lines.append(f"UK_META|label={clean(label)}|index={i}|value={value}")
    return lines

def main() -> int:
    print("StoneAge 2.5 public Baidu-share metadata probe — R2")
    print("SCOPE|public-share-page+normal-published-code-verification|no-login|no-code-guessing|no-payload-download")
    errors = 0
    exposed = 0
    for label, share_id, pwd in TARGETS:
        try:
            st, final, headers, body = fetch_share(share_id, pwd)
            print(f"HTTP|label={label}|status={st}|content_type={clean(headers.get('Content-Type'))}|content_length={clean(headers.get('Content-Length'))}")
            rows = analyze(label, share_id, pwd, body, final)
            for row in rows:
                print(row)
            initial_status = next((row.split("value=",1)[1].split("|",1)[0] for row in rows if row.startswith("STATUS|")), "")
            if any("value=PUBLIC_METADATA_EXPOSED" in row for row in rows):
                exposed += 1

            if pwd and initial_status == "NEEDS_CODE":
                verify, verified = verify_published_code(share_id, pwd)
                errno = verify.get("errno", "")
                print(f"VERIFY|label={clean(label)}|published_code=1|errno={clean(errno)}|has_randsk={1 if verify.get('randsk') else 0}")
                if verified is not None:
                    vst, vfinal, vheaders, vbody = verified
                    print(f"VERIFIED_HTTP|label={clean(label)}|status={vst}|content_type={clean(vheaders.get('Content-Type'))}|content_length={clean(vheaders.get('Content-Length'))}")
                    vrows = analyze(label + ":verified", share_id, pwd, vbody, vfinal)
                    for row in vrows:
                        print(row)
                    if any("value=PUBLIC_METADATA_EXPOSED" in row for row in vrows):
                        exposed += 1
        except Exception as e:
            errors += 1
            print(f"ERROR|label={clean(label)}|kind={type(e).__name__}|message={clean(e,1500)}")
    print(f"COUNT|targets|{len(TARGETS)}")
    print(f"COUNT|metadata_exposed|{exposed}")
    print(f"COUNT|errors|{errors}")
    if exposed:
        print("RESOLUTION|PUBLIC_SHARE_METADATA_RECOVERED|compare exposed names/sizes before any byte-level follow-up")
    elif errors == len(TARGETS):
        print("RESOLUTION|PUBLIC_SHARE_TRANSPORT_BLOCKED|do not infer share absence")
    else:
        print("RESOLUTION|PUBLIC_SHARE_PAGES_RETRIEVED_NO_FILE_METADATA|retain exact share IDs and published codes")
    print("EVIDENCE_BOUNDARY|Modern Baidu shares are descendant/community recovery leads only; page metadata cannot establish 2002 operator provenance or clean-client status.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
