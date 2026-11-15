"""Index the operator-hosted Taiwanese museum and link exact retail client names."""

import argparse
import json
import re
from base64 import b32encode
from hashlib import sha1, sha256
from html import unescape
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
SITE = "http://www7.waei.net:80/wgs/stoneage/content/museum/"
SNAPSHOT_PREFIX = "https://web.archive.org/web/"
IMAGE_TAG = re.compile(r'<img\b[^>]*\bsrc\s*=\s*"([^"]+)"[^>]*>', re.I)
FIELD = re.compile(r"編號\s*[:：]\s*(\d{4})\s+姓名\s*[:：]\s*(.+?)\s+屬性\s*[:：]\s*(.*?)\s*出現地點\s*[:：]\s*(.*?)\s+資料提供\s*[:：]", re.S)
ALBUM_PATH = ROOT / "research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json"


def text(fragment):
    """Collapse visible whitespace in the source's legacy table layout."""
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def entries(raw, source_url, album):
    page = raw.decode("cp950", errors="strict")
    page = re.sub(r"<(script|style)\b[^>]*>.*?</\1\s*>|<!--.*?-->", "", page, flags=re.I | re.S)
    image_tags = [m for m in IMAGE_TAG.finditer(page) if "/museum/pet/" in m[1].lower()]
    names = {row["name_as_written"]: row for row in album}
    if len(names) != len(album):
        raise ValueError("ambiguous names in the pinned retail index")
    rows = []
    for i, tag in enumerate(image_tags):
        stop = image_tags[i + 1].start() if i + 1 < len(image_tags) else len(page)
        visible = text(page[tag.end():stop])
        match = FIELD.search(visible)
        if not match or len(re.findall(r"編號\s*[:：]", visible)) != 1:
            raise ValueError("museum image has no unique complete source row")
        ordinal, name, element_text, location = match.groups()
        elements = re.findall(r"([地水火風])\s*[:：]\s*(\d+)", element_text)
        if len({key for key, _ in elements}) != len(elements):
            raise ValueError(f"duplicate element at museum entry {ordinal}")
        exact = names.get(name)
        rows.append({
            "web_ordinal": int(ordinal), "name_as_written": name,
            "web_image_url": urljoin(source_url, tag[1].strip()),
            "contributed_elements": {key: int(value) for key, value in elements},
            "contributed_location_sha256": sha256(location.encode("utf-8")).hexdigest(),
            "has_contributed_location": bool(location),
            "tw10_same_printed_name_graphic": exact["graphic_number"] if exact else None,
            "official_live_release_confirmed": False,
        })
    return rows


def index(directory, selected, album):
    pages, rows = [], []
    alias_rows = []
    for page_no in range(14):
        filename = "museum-pet.htm" if page_no == 0 else f"pet{page_no}.htm"
        stamp, original, digest = selected[filename]
        if original != SITE + filename:
            raise ValueError(f"unexpected original URL for {filename}")
        raw = (directory / filename).read_bytes()
        if b32encode(sha1(raw).digest()).decode("ascii") != digest:
            raise ValueError(f"CDX payload mismatch for {filename}")
        found = entries(raw, original, album)
        page_record = {
            "filename": filename, "archive_capture": stamp, "original_url": original,
            "replay_url": SNAPSHOT_PREFIX + stamp + "id_/" + original,
            "bytes": len(raw), "sha256": sha256(raw).hexdigest(), "cdx_payload_sha1_base32": digest,
            "ordinals": [row["web_ordinal"] for row in found],
        }
        pages.append(page_record)
        if page_no:
            rows.extend(dict(row, source_page=filename) for row in found)
        else:
            alias_rows = found
    if alias_rows != [{k: v for k, v in row.items() if k != "source_page"} for row in rows[:10]]:
        raise ValueError("museum landing page rows conflict with first gallery page")
    if [row["web_ordinal"] for row in rows] != list(range(1, 129)):
        raise ValueError("unexpected museum ordinal coverage")
    return {
        "schema": "stoneage.pet41.tw_early_wgs_museum.r1",
        "evidence": "OPERATOR_HOSTED_PLAYER_CONTRIBUTIONS",
        "pages": pages, "rows": rows,
        "matched_title_rows": sum(row["tw10_same_printed_name_graphic"] is not None for row in rows),
        "new_named_official_release_proofs": 0,
        "historical_pet_population_count": None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive_directory", type=Path)
    parser.add_argument("archive_manifest", type=Path)
    opts = parser.parse_args()
    selected = json.loads(opts.archive_manifest.read_text(encoding="utf-8"))
    if "pages" in selected:
        selected = {p["filename"]: (p["archive_capture"], p["original_url"], p["cdx_payload_sha1_base32"])
                    for p in selected["pages"]}
    album = json.loads(ALBUM_PATH.read_text(encoding="utf-8"))["records"]
    print(json.dumps(index(opts.archive_directory, selected, album), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
