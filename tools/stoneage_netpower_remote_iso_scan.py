#!/usr/bin/env python3
"""Remotely scan public Internet Archive Korean NetPower CD images for StoneAge traces.

The scanner uses HTTP Range requests to read ISO-9660/Joliet directory sectors only.
It does not download full disc images and never writes carrier bytes to the repository.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
import struct
import time
import urllib.parse
import urllib.request

UA = "stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"
ADV = "https://archive.org/advancedsearch.php"
META = "https://archive.org/metadata/{}"
DOWNLOAD = "https://archive.org/download/{}/{}"

QUERY = '"NetPower" AND mediatype:software'
PERIOD = re.compile(r"(?i)(?:^|\D)(2000|2001)(?:\D|$)")
KOREAN = re.compile(r"(?i)(netpower|넷파워|제우미디어|korea|korean|한국)")
IMAGE = re.compile(r"(?i)\.(?:iso|img)$")
NEEDLE = re.compile(r"(?i)(stone\s*age|stoneage|sa_demo|(?:^|[/\\])sa\.exe|enium|스톤에이지)")
MAX_IMAGES = 16
MAX_DIRS = 600
MAX_ENTRIES = 12000


def get_json(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def search_items():
    params = [
        ("q", QUERY),
        ("fl[]", "identifier"), ("fl[]", "title"), ("fl[]", "date"),
        ("fl[]", "year"), ("fl[]", "creator"), ("fl[]", "description"),
        ("rows", "100"), ("page", "1"), ("output", "json"),
    ]
    return get_json(ADV + "?" + urllib.parse.urlencode(params)).get("response", {}).get("docs", [])


def metadata(identifier):
    return get_json(META.format(urllib.parse.quote(identifier, safe="")))


def clean(v, limit=700):
    if v is None:
        return ""
    if isinstance(v, list):
        v = ",".join(str(x) for x in v)
    s = " ".join(str(v).split())
    return "".join(ch for ch in s if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def candidate(doc):
    blob = " ".join(clean(doc.get(k), 1200) for k in ("title", "date", "year", "creator", "description"))
    return bool(KOREAN.search(blob) and PERIOD.search(blob))


def carrier_images(data):
    out = []
    for f in data.get("files", []):
        name = str(f.get("name", ""))
        size = int(f.get("size") or 0)
        if IMAGE.search(name) and size >= 10 * 1024 * 1024:
            out.append({
                "name": name,
                "size": size,
                "md5": str(f.get("md5", "")),
                "sha1": str(f.get("sha1", "")),
                "format": str(f.get("format", "")),
            })
    return out


class RemoteImage:
    def __init__(self, identifier, name, frame=2048, data_offset=0):
        self.identifier = identifier
        self.name = name
        self.frame = frame
        self.data_offset = data_offset
        self.url = DOWNLOAD.format(
            urllib.parse.quote(identifier, safe=""),
            urllib.parse.quote(name, safe="/"),
        )
        self.bytes_read = 0
        self.requests = 0

    def raw_range(self, start, length, timeout=25, attempts=3):
        last = None
        for attempt in range(attempts):
            try:
                req = urllib.request.Request(
                    self.url,
                    headers={
                        "User-Agent": UA,
                        "Range": f"bytes={start}-{start + length - 1}",
                        "Accept-Encoding": "identity",
                    },
                )
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    status = getattr(r, "status", 200)
                    content_range = r.headers.get("Content-Range", "")
                    if status != 206 and not content_range:
                        raise RuntimeError(f"range-not-honored status={status}")
                    data = r.read(length)
                    if len(data) != length:
                        raise RuntimeError(f"short-range expected={length} got={len(data)}")
                self.bytes_read += len(data)
                self.requests += 1
                return data
            except Exception as exc:
                last = exc
                if attempt + 1 < attempts:
                    time.sleep(0.8 * (attempt + 1))
        raise last

    def sector(self, lba):
        return self.raw_range(self.origin + lba * self.frame, 2048)

    def extent(self, lba, length):
        chunks = []
        remaining = length
        sector = lba
        while remaining > 0:
            block = self.sector(sector)
            take = min(remaining, 2048)
            chunks.append(block[:take])
            remaining -= take
            sector += 1
        return b"".join(chunks)


def infer_layout_from_probe(probe):
    """Infer logical-sector stride/origin from consecutive ISO volume descriptors."""
    starts = []
    for i in range(1, len(probe) - 6):
        if probe[i:i+5] != b"CD001" or probe[i+5] != 1:
            continue
        dtype = probe[i-1]
        if dtype in (1, 2, 255):
            starts.append((i-1, dtype))
    for idx, (pvd_start, dtype) in enumerate(starts):
        if dtype != 1:
            continue
        for next_start, next_type in starts[idx+1:]:
            frame = next_start - pvd_start
            if next_type in (2, 255) and 1800 <= frame <= 3000:
                origin = pvd_start - 16 * frame
                if 0 <= origin <= 1024 * 1024:
                    return frame, origin
                break
    return None


def detect_layout(identifier, name):
    errors = []
    for frame, origin, label in ((2048, 0, "iso2048"), (2352, 16, "mode1-2352")):
        img = RemoteImage(identifier, name, frame, origin)
        try:
            pvd = img.sector(16)
        except Exception as exc:
            errors.append(f"{label}:{type(exc).__name__}:{exc}")
            continue
        if len(pvd) >= 7 and pvd[0] == 1 and pvd[1:6] == b"CD001" and pvd[6] == 1:
            return img, pvd, label, errors
        errors.append(f"{label}:no-pvd")

    probe_img = RemoteImage(identifier, name)
    try:
        probe = probe_img.raw_range(0, 256 * 1024)
        inferred = infer_layout_from_probe(probe)
    except Exception as exc:
        errors.append(f"autodetect:{type(exc).__name__}:{exc}")
        inferred = None
    if inferred is not None:
        frame, origin = inferred
        label = f"auto-frame-{frame}-origin-{origin}"
        img = RemoteImage(identifier, name, frame, origin)
        try:
            pvd = img.sector(16)
        except Exception as exc:
            errors.append(f"{label}:{type(exc).__name__}:{exc}")
        else:
            if len(pvd) >= 7 and pvd[0] == 1 and pvd[1:6] == b"CD001" and pvd[6] == 1:
                return img, pvd, label, errors
            errors.append(f"{label}:no-pvd")
    else:
        errors.append("autodetect:no-layout")
    raise RuntimeError("; ".join(errors))


def le32(buf, offset):
    return struct.unpack_from("<I", buf, offset)[0]


def root_record(vd):
    length = vd[156]
    if length < 34:
        raise ValueError("invalid root directory record")
    rec = vd[156:156 + length]
    return le32(rec, 2), le32(rec, 10)


def decode_name(raw, joliet=False):
    if raw in (b"\x00", b"\x01"):
        return "." if raw == b"\x00" else ".."
    if joliet:
        try:
            s = raw.decode("utf-16-be", "replace")
        except Exception:
            s = raw.decode("latin-1", "replace")
    else:
        s = raw.decode("ascii", "replace")
    return s.split(";", 1)[0]


def parse_directory(data, joliet=False):
    pos = 0
    out = []
    while pos < len(data):
        length = data[pos]
        if length == 0:
            pos = ((pos // 2048) + 1) * 2048
            continue
        if pos + length > len(data) or length < 34:
            break
        rec = data[pos:pos + length]
        name_len = rec[32]
        raw_name = rec[33:33 + name_len]
        name = decode_name(raw_name, joliet)
        extent = le32(rec, 2)
        size = le32(rec, 10)
        flags = rec[25]
        if name not in (".", ".."):
            out.append((name, extent, size, bool(flags & 0x02)))
        pos += length
    return out


def find_joliet(img):
    for lba in range(17, 25):
        vd = img.sector(lba)
        if vd[1:6] != b"CD001":
            break
        if vd[0] == 255:
            break
        if vd[0] == 2 and vd[88:91] in (b"%/@", b"%/C", b"%/E"):
            return vd
    return None


def walk(img, vd, joliet=False):
    root_lba, root_size = root_record(vd)
    queue = [("", root_lba, root_size)]
    seen = set()
    hits = []
    entries = 0
    dirs = 0
    samples = []

    while queue and dirs < MAX_DIRS and entries < MAX_ENTRIES:
        prefix, lba, size = queue.pop(0)
        key = (lba, size)
        if key in seen:
            continue
        seen.add(key)
        dirs += 1
        if size <= 0 or size > 16 * 1024 * 1024:
            continue
        data = img.extent(lba, size)
        for name, child_lba, child_size, is_dir in parse_directory(data, joliet):
            entries += 1
            path = f"{prefix}/{name}" if prefix else name
            if len(samples) < 80:
                samples.append(path)
            if NEEDLE.search(path):
                hits.append((path, child_size, is_dir))
            if is_dir and child_size > 0:
                queue.append((path, child_lba, child_size))
            if entries >= MAX_ENTRIES:
                break

    return {
        "dirs": dirs,
        "entries": entries,
        "hits": hits,
        "samples": samples,
        "truncated": bool(queue),
    }


def scan_one(identifier, doc, f):
    name = f["name"]
    result = {
        "identifier": identifier,
        "title": clean(doc.get("title"), 300),
        "date": clean(doc.get("date") or doc.get("year"), 100),
        "name": name,
        "size": f["size"],
        "md5": f["md5"],
        "sha1": f["sha1"],
        "error": "",
    }
    try:
        img, pvd, layout, detect_errors = detect_layout(identifier, name)
        primary = walk(img, pvd, False)
        joliet_vd = find_joliet(img)
        joliet = walk(img, joliet_vd, True) if joliet_vd is not None else None
        result.update({
            "layout": layout,
            "detect_errors": detect_errors,
            "volume": pvd[40:72].decode("ascii", "replace").strip(),
            "primary": primary,
            "joliet": joliet,
            "requests": img.requests,
            "bytes_read": img.bytes_read,
        })
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main():
    print("StoneAge Korean NetPower remote directory scan — R1")
    print("SCOPE|http-range-directory-metadata-only|no-full-image-download|no-carrier-bytes-committed")
    docs = [d for d in search_items() if candidate(d)]
    rows = []
    errors = []
    for doc in docs:
        ident = str(doc.get("identifier", "")).strip()
        if not ident:
            continue
        try:
            data = metadata(ident)
        except Exception as exc:
            errors.append((ident, type(exc).__name__, str(exc)))
            continue
        for f in carrier_images(data):
            rows.append((ident, doc, f))

    rows = sorted(rows, key=lambda x: (clean(x[1].get("date") or x[1].get("year")), x[0], x[2]["name"]))[:MAX_IMAGES]
    print(f"COUNT|candidate_items|{len(docs)}")
    print(f"COUNT|image_candidates_selected|{len(rows)}")
    print(f"COUNT|metadata_errors|{len(errors)}")
    for ident, kind, msg in errors:
        print(f"ERROR|phase=metadata|identifier={clean(ident)}|kind={clean(kind)}|message={clean(msg)}")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        for res in ex.map(lambda args: scan_one(*args), rows):
            results.append(res)

    print(f"COUNT|scan_errors|{sum(bool(r['error']) for r in results)}")
    print(f"COUNT|images_scanned|{sum(not r['error'] for r in results)}")
    print(f"COUNT|stoneage_hits|{sum(len((r.get('primary') or {}).get('hits', [])) + len((r.get('joliet') or {}).get('hits', [])) for r in results)}")

    for r in results:
        base = (
            f"identifier={clean(r['identifier'])}|title={clean(r['title'])}|date={clean(r['date'])}|"
            f"name={clean(r['name'])}|size={r['size']}|md5={clean(r['md5'])}|sha1={clean(r['sha1'])}"
        )
        if r["error"]:
            print(f"SCAN_ERROR|{base}|message={clean(r['error'])}")
            continue
        print(
            f"IMAGE|{base}|layout={clean(r['layout'])}|volume={clean(r['volume'])}|"
            f"requests={r['requests']}|bytes_read={r['bytes_read']}|"
            f"primary_entries={r['primary']['entries']}|primary_dirs={r['primary']['dirs']}|"
            f"joliet={int(r['joliet'] is not None)}|"
            f"joliet_entries={(r['joliet'] or {}).get('entries',0)}|"
            f"truncated={int(r['primary']['truncated'] or bool((r['joliet'] or {}).get('truncated',False)))}"
        )
        for namespace in ("primary", "joliet"):
            tree = r.get(namespace)
            if not tree:
                continue
            for path, size, is_dir in tree["hits"]:
                print(
                    f"HIT|namespace={namespace}|identifier={clean(r['identifier'])}|image={clean(r['name'])}|"
                    f"path={clean(path)}|size={size}|directory={int(is_dir)}"
                )
        if not r["primary"]["hits"] and not (r.get("joliet") or {}).get("hits"):
            for path in r["primary"]["samples"][:12]:
                print(f"SAMPLE|identifier={clean(r['identifier'])}|image={clean(r['name'])}|path={clean(path,360)}")


if __name__ == "__main__":
    main()
