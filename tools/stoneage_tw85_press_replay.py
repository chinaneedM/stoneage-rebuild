"""Independent bounded byte replay of one 2006 public article. No HTML retained."""
import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://www.games.idv.tw/news.php?mode=view&nid=615"
MARKERS = ("魔域大冒險", "雷爾", "艾巴登", "支援前線", "伊甸大陸", "蒼龍")

class Plain(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

def derive(raw, content_type):
    codecs = []
    for text in (content_type, raw[:4096].decode("ascii", errors="ignore")):
        m = re.search(r'charset\s*=\s*["\x27]?([A-Za-z0-9_-]+)', text, re.I)
        if m: codecs.append(m.group(1))
    codecs.extend(["utf-8", "big5", "cp950", "gb18030"])
    for codec in dict.fromkeys(codecs):
        try:
            p = Plain()
            p.feed(raw.decode(codec, errors="strict"))
        except (UnicodeError, LookupError):
            continue
        visible = re.sub(r"\s+", "", "".join(p.parts))
        if all(s in visible for s in MARKERS):
            return {
                "schema": "stoneage.tw85.press.source_probe.r1",
                "url": URL,
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "decoder": codec,
                "marker_counts": {s: visible.count(s) for s in MARKERS},
                "raw_html_archived": False,
                "original_game_asset_archived": False,
                "evidence_kind": "PRESS_PAGE_BYTES_NOT_GAME_SERVER"
            }
    raise RuntimeError("Source no longer decodes with all bounded expected markers")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    with urlopen(Request(URL, headers={"User-Agent":"Mozilla/5.0 StoneAgeResearch/1.0", "Accept":"text/html"}), timeout=22) as resp:
        if resp.status != 200: raise RuntimeError(f"HTTP {resp.status}")
        raw = resp.read(800001)
        content_type = resp.headers.get("Content-Type", "")
    if not 2000 <= len(raw) <= 800000: raise RuntimeError("Source bytes outside bounded size")
    result = derive(raw, content_type)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("source_sha256="+result["sha256"]+" source_bytes="+str(result["bytes"]))

if __name__ == "__main__":
    main()
