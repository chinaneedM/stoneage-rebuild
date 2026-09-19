#!/usr/bin/env python3
"""Query Arquivo.pt for StoneAge Korea 2000 path metadata only."""

import argparse
import json
import time
import urllib.parse
import urllib.request


UA = "stoneage-rebuild-archaeology/1.0"
API = "https://arquivo.pt/textsearch"

QUERIES = (
    ("inium-url", '"stoneage.enium.co.kr"'),
    ("inium-site-korean", '"스톤에이지" site:stoneage.enium.co.kr'),
    ("hananet-korean", '"스톤에이지" site:hananet.net'),
    ("hananet-latin", 'stoneage site:hananet.net'),
    ("cnet-korean", '"스톤에이지" site:korea.cnet.com'),
    ("cnet-latin", 'stoneage site:korea.cnet.com'),
)


def fetch_json(params, timeout=30):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def clean(value):
    value = "" if value is None else str(value)
    return "".join(ch for ch in value if ch >= " " and ch != "\x7f")[:800]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from-year", default="2000")
    p.add_argument("--to-year", default="2005")
    args = p.parse_args()

    rows = []
    errors = []
    for label, query in QUERIES:
        params = {
            "q": query,
            "from": args.from_year,
            "to": args.to_year,
            "maxItems": "50",
            "prettyPrint": "false",
        }
        try:
            data = fetch_json(params)
        except Exception as exc:
            errors.append((label, type(exc).__name__, str(exc)))
            continue
        for item in data.get("response_items", []):
            rows.append(
                (
                    label,
                    clean(item.get("timestamp") or item.get("date")),
                    clean(item.get("originalURL")),
                    clean(item.get("title")),
                    clean(item.get("mimeType")),
                    clean(item.get("contentLength")),
                    clean(item.get("digest")),
                    clean(item.get("linkToArchive")),
                )
            )
        time.sleep(0.5)

    unique = {}
    for row in rows:
        unique[(row[0], row[2], row[1])] = row

    print("StoneAge Korea 2000 Arquivo.pt metadata probe — R1")
    print("SCOPE|metadata-only|no-client-binary-download")
    print(f"YEARS|from={args.from_year}|to={args.to_year}")
    for label, kind, message in errors:
        print(f"ERROR|{clean(label)}|{clean(kind)}|{clean(message)}")
    print(f"COUNT|results|{len(unique)}")
    for row in sorted(unique.values(), key=lambda x: (x[0], x[1], x[2])):
        print("RESULT|" + "|".join(clean(x) for x in row))


if __name__ == "__main__":
    main()
