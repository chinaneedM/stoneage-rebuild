"""One original official link, no assumed game content or original assets in Git."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ORIGINAL = "http://www.wayi.com.tw/stoneage/game/game01_02.asp"
REQUESTED = "https://web.archive.org/web/20050614002509id_/" + ORIGINAL
ARCHIVE = re.compile(r"^https://web\.archive\.org/web/(\d{14})(?:id_)?/http://www\.wayi\.com\.tw/stoneage/game/game01_02\.asp$", re.I)
KEYWORDS = ("寵物", "人物", "世界", "故事", "地圖", "技能", "任務", "大陸", "冰", "冒險", "石器", "村")

def check_final_url(url):
    match = ARCHIVE.fullmatch(url)
    if not match:
        raise ValueError("Actual response not exact archived official page")
    return match.group(1)

class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.in_title = False
        self.title = []
        self.pieces = []
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1
        if tag == "title":
            self.in_title = True
    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1
        if tag == "title":
            self.in_title = False
    def handle_data(self, value):
        if self.hidden:
            return
        s = " ".join(value.split())
        if not s:
            return
        (self.title if self.in_title else self.pieces).append(s)

def inspect(raw, final_url):
    actual = check_final_url(final_url)
    if len(raw) < 350 or len(raw) > 300000:
        raise ValueError("Unexpected body size")
    html = raw.decode("big5", errors="strict")
    if not re.search(r"<html|<body", html, re.I):
        raise ValueError("Non-HTML response")
    parsed = Visible()
    parsed.feed(html)
    significant = [t for t in parsed.pieces if len(t) >= 5]
    if not significant:
        raise ValueError("No eligible visible page content")
    matches = [t for t in significant if any(word in t for word in KEYWORDS)]
    samples = [x[:100] for x in (matches or significant)[:16]]
    return {"schema": "stoneage.wayi.intro-detail02.probe.r1",
        "original_url": ORIGINAL, "requested_url": REQUESTED,
        "final_url": final_url, "actual_capture": actual,
        "response_sha256": hashlib.sha256(raw).hexdigest(), "response_bytes": len(raw),
        "codec": "BIG5_STRICT", "title_preview": " ".join(parsed.title)[:120],
        "selected_text_previews": samples, "eligible_text_pieces": len(significant),
        "matching_text_pieces": len(matches), "topic_unqualified": True,
        "original_html_or_images_retained": False, "exact_client_build": None,
        "npc_pet_quest_runtime_confirmed": False}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    args = p.parse_args()
    attempts = []
    for n in range(2):
        try:
            with urlopen(Request(REQUESTED, headers={"User-Agent": "Mozilla/5.0 StoneAgeHistoricalEvidence"}), timeout=35) as r:
                final = r.url
                raw = r.read(300001)
            break
        except HTTPError as exc:
            attempts.append({"attempt": n + 1, "status": exc.code})
            if n == 1 or exc.code not in (502, 503, 504):
                raise
    report = inspect(raw, final)
    if report["response_sha256"] != "0868e56a81d7037e434a09fd0824a6eb59747494099087f8d1eaeaaa37fb690c" or report["response_bytes"] != 26414 or report["actual_capture"] != "20050614005428":
        raise ValueError("Replayed response differs from accepted primary-source byte pin")
    # Source excerpts are bounded diagnostic output only; not preserved as full HTML.
    visible = Visible()
    visible.feed(raw.decode("big5", errors="strict"))
    # Establish whether this page describes released systems, future plans, or a survey.
    head = []
    spent = 0
    for node in visible.pieces[:110]:
        if spent >= 3600:
            break
        short = node[:min(140, 3600 - spent)]
        spent += len(short)
        head.append(short)
    print("BOUNDED_PAGE_OPENING=" + json.dumps(head, ensure_ascii=False))
    for anchor, after, budget in (("寵物裝備系統", 65, 4100), ("任務日誌", 28, 1800)):
        index = next((i for i, value in enumerate(visible.pieces) if anchor in value), None)
        if index is not None:
            window = visible.pieces[max(0, index - 3):index + after]
            emitted = []
            used = 0
            for part in window:
                if used >= budget:
                    break
                item = part[:min(175, budget - used)]
                used += len(item)
                emitted.append(item)
            print("BOUNDED_CONTEXT_" + anchor + "=" + json.dumps(emitted, ensure_ascii=False))
    report["transient_attempts"] = attempts
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for k in ("final_url", "response_bytes", "response_sha256", "title_preview", "selected_text_previews"):
        print("PROBE_" + k.upper() + "=" + json.dumps(report[k], ensure_ascii=False))

if __name__ == "__main__":
    main()
