#!/usr/bin/env python3
"""Clean-client acceptance probe for a locally extracted raw StoneAge CD image.

Designed for ephemeral CI use after downloading a public preservation archive.
It emits only derived metadata: disc/file hashes, ISO/Joliet file tree, executable
headers, and bounded text snippets. It never copies client/media bytes into git.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import struct
import urllib.request

from tools.stoneage_netpower_remote_iso_scan import (
    decode_name,
    find_joliet,
    parse_directory,
    root_record,
)

REDUMP_BASE = "http://redump.org/disc/104630"
EXPECTED_RAR_MD5 = "b37a4a47f4eb608cac67e4ddf7a1621a"
EXPECTED_RAR_SHA1 = "b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded"
EXPECTED_BIN_SIZE = 523_449_360
UA = "stoneage-rebuild-archaeology/1.0 (+https://github.com/chinaneedM/stoneage-rebuild)"

TEXT_EXT = {".txt", ".ini", ".inf", ".cfg", ".url", ".htm", ".html", ".log"}
EXEC_EXT = {".exe", ".dll", ".ocx", ".cpl"}
RESOURCE_NAMES = {"real.bin", "adrn.bin", "spr.bin", "spradrn.bin"}
URL_RE = re.compile(rb"(?i)(?:https?://|ftp://|www\.)[^\x00-\x20\"'<>]{4,240}")
HOST_RE = re.compile(rb"(?i)\b(?:[a-z0-9-]{1,63}\.)+(?:com|net|org|co\.kr|com\.tw|net\.tw|ne\.jp|jp)\b")


def clean(value, limit=1600):
    text = " ".join(str(value if value is not None else "").split())
    return "".join(ch for ch in text if ch >= " " and ch != "\x7f").replace("|", "%7C")[:limit]


def file_hashes(path, chunk=4 * 1024 * 1024):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            size += len(data)
            md5.update(data)
            sha1.update(data)
            sha256.update(data)
    return size, md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()


class LocalImage:
    def __init__(self, path, frame, origin):
        self.path = path
        self.frame = frame
        self.origin = origin
        self.fh = open(path, "rb")
        self.file_size = os.path.getsize(path)

    def close(self):
        self.fh.close()

    def sector(self, lba):
        offset = self.origin + lba * self.frame
        self.fh.seek(offset)
        data = self.fh.read(2048)
        if len(data) != 2048:
            raise RuntimeError(f"short sector lba={lba} got={len(data)}")
        return data

    def iter_extent(self, lba, length, sector_batch=128):
        remaining = int(length)
        sector = int(lba)
        while remaining > 0:
            count = min(sector_batch, (remaining + 2047) // 2048)
            offset = self.origin + sector * self.frame
            raw_len = (count - 1) * self.frame + 2048
            self.fh.seek(offset)
            raw = self.fh.read(raw_len)
            if len(raw) != raw_len:
                raise RuntimeError(
                    f"short extent lba={sector} count={count} expected={raw_len} got={len(raw)}"
                )
            parts = []
            for idx in range(count):
                start = idx * self.frame
                take = min(2048, remaining)
                parts.append(raw[start:start + take])
                remaining -= take
                if remaining <= 0:
                    break
            yield b"".join(parts)
            sector += count

    def extent(self, lba, length):
        return b"".join(self.iter_extent(lba, length))


def detect_layout(path):
    for frame, origin, label in (
        (2048, 0, "iso2048"),
        (2352, 16, "mode1-2352"),
    ):
        img = LocalImage(path, frame, origin)
        try:
            pvd = img.sector(16)
            if pvd[0] == 1 and pvd[1:6] == b"CD001" and pvd[6] == 1:
                return img, pvd, label
        except Exception:
            pass
        img.close()
    raise RuntimeError("unable to detect ISO-9660 layout")


def walk_full(img, vd, joliet=False, max_dirs=5000, max_entries=100000):
    root_lba, root_size = root_record(vd)
    queue = [("", root_lba, root_size)]
    seen = set()
    rows = []
    dirs = 0

    while queue:
        prefix, lba, size = queue.pop(0)
        key = (lba, size)
        if key in seen:
            continue
        seen.add(key)
        dirs += 1
        if dirs > max_dirs:
            raise RuntimeError("directory limit exceeded")
        data = img.extent(lba, size)
        for name, child_lba, child_size, is_dir in parse_directory(data, joliet):
            path = f"{prefix}/{name}" if prefix else name
            rows.append(
                {
                    "path": path,
                    "lba": child_lba,
                    "size": child_size,
                    "is_dir": is_dir,
                }
            )
            if len(rows) > max_entries:
                raise RuntimeError("entry limit exceeded")
            if is_dir and child_size > 0:
                queue.append((path, child_lba, child_size))
    return rows


def hash_extent(img, lba, size):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    for chunk in img.iter_extent(lba, size):
        md5.update(chunk)
        sha1.update(chunk)
        sha256.update(chunk)
    return md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()


def read_bounded(img, row, limit=2 * 1024 * 1024):
    if row["size"] > limit:
        return b""
    return img.extent(row["lba"], row["size"])


def decode_text(data):
    for enc in ("utf-8", "cp950", "big5", "cp936", "gbk", "cp949", "shift_jis", "latin-1"):
        try:
            text = data.decode(enc)
            printable = sum(ch.isprintable() or ch in "\r\n\t" for ch in text)
            if not text or printable / max(1, len(text)) > 0.92:
                return enc, text
        except UnicodeDecodeError:
            pass
    return "latin-1", data.decode("latin-1", "replace")


def pe_header(data):
    if len(data) < 0x40 or data[:2] != b"MZ":
        return None
    pe_off = struct.unpack_from("<I", data, 0x3C)[0]
    if pe_off + 24 > len(data) or data[pe_off:pe_off + 4] != b"PE\x00\x00":
        return {"mz": True, "pe": False}
    machine, sections, timestamp = struct.unpack_from("<HHI", data, pe_off + 4)
    return {
        "mz": True,
        "pe": True,
        "machine": machine,
        "sections": sections,
        "timestamp": timestamp,
    }


def print_redump_endpoints():
    for suffix in ("sha1", "md5", "sfv", "cue"):
        url = f"{REDUMP_BASE}/{suffix}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read(256 * 1024)
                final = r.geturl()
            text = body.decode("utf-8", "replace")
            print(
                f"REDUMP_EXPORT|kind={suffix}|url={clean(final)}|bytes={len(body)}|"
                f"text={clean(text,5000)}"
            )
        except Exception as exc:
            print(
                f"REDUMP_EXPORT_ERROR|kind={suffix}|kind_error={type(exc).__name__}|"
                f"message={clean(exc)}"
            )


def scan_disc(bin_path):
    size, md5, sha1, sha256 = file_hashes(bin_path)
    print(
        f"DISC_IMAGE|path={clean(os.path.basename(bin_path))}|size={size}|"
        f"md5={md5}|sha1={sha1}|sha256={sha256}|"
        f"expected_size_match={int(size==EXPECTED_BIN_SIZE)}"
    )

    img, pvd, layout = detect_layout(bin_path)
    try:
        volume = pvd[40:72].decode("ascii", "replace").strip()
        joliet_vd = find_joliet(img)
        primary = walk_full(img, pvd, False)
        joliet = walk_full(img, joliet_vd, True) if joliet_vd is not None else []
        chosen = joliet if joliet else primary
        print(
            f"FILESYSTEM|layout={layout}|volume={clean(volume)}|"
            f"primary_entries={len(primary)}|joliet={int(joliet_vd is not None)}|"
            f"joliet_entries={len(joliet)}|chosen_namespace={'joliet' if joliet else 'primary'}"
        )

        files = [row for row in chosen if not row["is_dir"]]
        dirs = [row for row in chosen if row["is_dir"]]
        print(f"COUNT|directories|{len(dirs)}")
        print(f"COUNT|files|{len(files)}")

        total_file_bytes = 0
        exec_count = 0
        resource_count = 0
        endpoint_hits = set()

        for row in chosen:
            kind = "DIR" if row["is_dir"] else "FILE"
            print(
                f"TREE|kind={kind}|path={clean(row['path'],2200)}|"
                f"lba={row['lba']}|size={row['size']}"
            )
            if row["is_dir"]:
                continue

            total_file_bytes += row["size"]
            md5f, sha1f, sha256f = hash_extent(img, row["lba"], row["size"])
            base = row["path"].rsplit("/", 1)[-1]
            ext = os.path.splitext(base)[1].lower()
            lower_base = base.lower()
            special = (
                ext in EXEC_EXT
                or ext in TEXT_EXT
                or lower_base in RESOURCE_NAMES
                or "stone" in lower_base
                or "server" in lower_base
                or "update" in lower_base
                or "patch" in lower_base
                or "setup" in lower_base
                or "install" in lower_base
            )
            print(
                f"HASH|path={clean(row['path'],2200)}|size={row['size']}|"
                f"md5={md5f}|sha1={sha1f}|sha256={sha256f}|special={int(special)}"
            )

            if ext in EXEC_EXT:
                exec_count += 1
                data = read_bounded(img, row, 4 * 1024 * 1024)
                pe = pe_header(data)
                print(
                    f"EXEC|path={clean(row['path'])}|size={row['size']}|"
                    f"pe={int(bool(pe and pe.get('pe')))}|"
                    f"machine={pe.get('machine','') if pe else ''}|"
                    f"sections={pe.get('sections','') if pe else ''}|"
                    f"timestamp={pe.get('timestamp','') if pe else ''}"
                )
                for match in URL_RE.findall(data) + HOST_RE.findall(data):
                    endpoint_hits.add(match.decode("latin-1", "replace"))

            if lower_base in RESOURCE_NAMES:
                resource_count += 1

            if ext in TEXT_EXT:
                data = read_bounded(img, row, 2 * 1024 * 1024)
                if data:
                    enc, text = decode_text(data)
                    print(
                        f"TEXT|path={clean(row['path'])}|encoding={enc}|"
                        f"text={clean(text,5000)}"
                    )
                    for match in URL_RE.findall(data) + HOST_RE.findall(data):
                        endpoint_hits.add(match.decode("latin-1", "replace"))

        print(f"COUNT|logical_file_bytes|{total_file_bytes}")
        print(f"COUNT|executables|{exec_count}")
        print(f"COUNT|resource_container_named_files|{resource_count}")
        print(f"COUNT|endpoint_hits|{len(endpoint_hits)}")
        for value in sorted(endpoint_hits):
            print(f"ENDPOINT|value={clean(value,1200)}")
    finally:
        img.close()


def print_aux_logs(directory):
    names = (
        "!submissionInfo.json",
        "!submissionInfo.txt",
        "STONEAGE_disc.txt",
        "STONEAGE_drive.txt",
        "STONEAGE_20230309T204228.txt",
        "STONEAGE.cue",
        "STONEAGE_img.cue",
    )
    for name in names:
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue
        size = os.path.getsize(path)
        if size > 256 * 1024:
            print(f"AUX|name={clean(name)}|size={size}|text=SKIPPED_TOO_LARGE")
            continue
        data = open(path, "rb").read()
        enc, text = decode_text(data)
        # Avoid leaking arbitrary local paths/usernames from preservation logs.
        text = re.sub(r"(?i)(?:[A-Z]:\\|/home/|/Users/)[^\r\n\t ]+", "<LOCAL_PATH>", text)
        print(
            f"AUX|name={clean(name)}|size={size}|encoding={enc}|"
            f"text={clean(text,8000)}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", required=True)
    parser.add_argument("--aux-dir", required=False, default="")
    args = parser.parse_args()

    print("StoneAge Taiwan 2000 clean-client acceptance — R1")
    print("SCOPE|ephemeral-preserved-disc-analysis|derived-metadata-only|no-payload-commit")
    print_redump_endpoints()
    if args.aux_dir:
        print_aux_logs(args.aux_dir)
    scan_disc(args.bin)


if __name__ == "__main__":
    main()
