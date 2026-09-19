#!/usr/bin/env python3
"""Extract sparse Latin recovery tokens from temporary OCR text.

The intended input is OCR generated from public historical magazine scans.
This parser deliberately emits only token-level evidence useful for locating
client/download artifacts. It never stores or reproduces full OCR text.
"""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path

URL_RE = re.compile(r"""(?ix)
\b(?:
    https?://
  | ftp://
  | www\.
)
[a-z0-9][a-z0-9._~:/?#\[\]@!$&'()*+,;=%-]{3,}
""")

DOMAIN_RE = re.compile(r"""(?ix)
\b
(?:[a-z0-9-]+\.)+
(?:co\.kr|or\.kr|ne\.kr|com|net|org|kr)
(?:/[a-z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?
""")

FILE_RE = re.compile(r"""(?ix)
\b[a-z0-9][a-z0-9._-]{1,120}\.
(?:exe|zip|rar|cab|lzh|lha|arj|msi|com|bat|dll|bin|dat)
\b
""")

SIZE_RE = re.compile(r"""(?ix)
\b\d{1,5}(?:[.,]\d{1,3})?\s*(?:kb|mb|gb)\b
""")

KEY_RE = re.compile(
    r"(?i)\b(?:stone\s*age|stoneage|enium|inium|hananet|cnet|"
    r"client|download|setup|install|installer|patch|update|gameplus)\b"
)

TRIM = ".,;:!?)]}>\"'|"


def clean_token(value: str) -> str:
    value = " ".join(value.split())
    value = value.strip(TRIM)
    return value[:240]


def classify(text: str):
    hits = []
    for kind, regex in (
        ("url", URL_RE),
        ("file", FILE_RE),
        ("size", SIZE_RE),
        ("domain", DOMAIN_RE),
        ("keyword", KEY_RE),
    ):
        for match in regex.finditer(text):
            token = clean_token(match.group(0))
            if token:
                hits.append((kind, token))
    return hits


def parse_filename(path: Path):
    m = re.search(r"page(\d+)_psm(\d+)", path.stem, re.I)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def analyze(ocr_dir: Path):
    evidence = collections.defaultdict(set)
    files = 0
    for path in sorted(ocr_dir.glob("*.txt")):
        meta = parse_filename(path)
        if meta is None:
            continue
        page, psm = meta
        files += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for kind, token in classify(text):
            evidence[(page, kind, token)].add(psm)
    return files, evidence


def emit(files: int, evidence):
    print("StoneAge NetPower 2000-09 sparse Latin OCR token probe — R1")
    print("SCOPE|token-only|no-scan-bytes|no-full-ocr-text")
    print(f"COUNT|ocr_text_inputs|{files}")
    print(f"COUNT|unique_page_tokens|{len(evidence)}")
    for (page, kind, token), modes in sorted(
        evidence.items(),
        key=lambda item: (item[0][0], item[0][1], item[0][2].lower()),
    ):
        mode_text = ",".join(str(x) for x in sorted(modes))
        stability = "cross_psm" if len(modes) >= 2 else "single_psm"
        print(
            f"TOKEN|page={page}|kind={kind}|psm={mode_text}|"
            f"stability={stability}|value={token}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ocr-dir", type=Path, required=True)
    args = parser.parse_args()
    files, evidence = analyze(args.ocr_dir)
    emit(files, evidence)


if __name__ == "__main__":
    main()
