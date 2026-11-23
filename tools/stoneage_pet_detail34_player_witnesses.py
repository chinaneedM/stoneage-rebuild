"""Recheck the dated player catalogue and the 2003 forum growth result from saved bytes."""
import argparse
from decimal import Decimal
from hashlib import file_digest, sha256
from html import unescape
import json
from pathlib import Path
import re
import unicodedata
from zipfile import ZipFile

from tools.stoneage_pet39_tw10_album import ARCHIVE_SHA, ARCHIVE_SIZE, ROOT, TABLE_STRIDE

ALBUM = "research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json"
RECEIPT = "research/pets/PET-DETAIL-EVIDENCE34-EARLY-PC-PLAYER-CATALOGUE-AND-GROWTH-R1.json"
SOURCES = {
    "netease-index.html": (
        "https://www.moon-soft.com/program/bbs/readelite131452.htm", "gb2312",
        "b00778eb13c88a7cfa13ddfcee00158ef91f7292e979e75e8ba7e8622785fb14",
    ),
    "17173-acquisition.html": (
        "https://news.17173.com/z/stoneage/content/2001-6-14/n182_98793.html", "utf-8",
        "c1db6b1534a4a438e31e299f570b4d76aa15c1e2283678ded25f8170af184c70",
    ),
    "sina-beluyika.html": (
        "https://games.sina.com.cn/zhqu/sta/article/2003-05-31/10169.shtml", "gb18030",
        "07b5b7328f90187ef3043a97a5b7069a1ffdf987840c8a5664bd05b4f20a5a9c",
    ),
}
SIX_PETS = {7: 100255, 8: 100256, 12: 100260, 14: 100262, 25: 100273, 26: 100274}


def sha(raw):
    return sha256(raw).hexdigest()


def text(raw):
    return unescape(re.sub(r"<[^>]+>", "", raw)).strip()


def fragments(raw):
    return re.split(r"<br\b[^>]*>", raw, flags=re.I)


def mirror_rows(html):
    content = html[html.index("宠物名称&nbsp;&nbsp;属性"):]
    rows = []
    for fragment in fragments(content[:content.index("<BR>----")])[1:]:
        line = text(fragment)
        if not line:
            continue
        if "\xa0\xa0" not in line:
            rows[-1]["acquisition"] += " " + line
            continue
        name, fields = re.split(r"\xa0{2,}", line, maxsplit=1)
        if not re.fullmatch(r"[\u3400-\u9fff]+", name):
            raise ValueError("unexpected catalogue name layout")
        attribute = re.match(r"((?:[地水火风][０-９]{1,2})+)(\xa0{2,})(.+)$", fields)
        skills = None
        elements = None
        if attribute:
            elements = unicodedata.normalize("NFKC", attribute[1])
            fields = attribute[3]
            if len(attribute[2]) == 2:
                skills, fields = re.split(r"\xa0{2,}", fields, maxsplit=1)
        rows.append({"name": name, "elements": elements, "skills": skills, "acquisition": fields})
    return rows


def numbered_rows(html):
    content = html[html.index("宠物名称 属性 技能 Lv1出现地"):]
    records = []
    for fragment in fragments(content[:content.index("<!--infoPageNumber-->")])[1:]:
        match = re.fullmatch(r"(\*?)(\d+)\s+(\S+)\s+(.+)", text(fragment))
        if match:
            records.append((int(match[2]), match[3], match[4]))
    if [row[0] for row in records] != list(range(1, 125)):
        raise ValueError("17173 positions are no longer continuous")
    return records


def common_positions(mirror, numbered, phrase):
    return [pos for row, (pos, _, route) in zip(mirror, numbered, strict=True)
            if phrase in row["acquisition"] and phrase in route]


def catalogue_comparison(mirror, numbered):
    if len(mirror) != len(numbered):
        raise ValueError("catalogue row counts differ")
    pairs = list(zip(mirror, numbered, strict=True))
    differences = [{"position": pos, "netease": row["name"], "17173": name}
                   for row, (pos, name, _) in pairs if row["name"] != name]
    coordinate = re.compile(r"东\s*(\d+)\s*南\s*(\d+)")
    shared_coordinates = sum(bool(set(coordinate.findall(unicodedata.normalize("NFKC", row["acquisition"])))
                                  & set(coordinate.findall(unicodedata.normalize("NFKC", route))))
                             for row, (_, _, route) in pairs)
    return {
        "netease_editor_date_label": "2001-03-28 16:30:21",
        "17173_migrated_page_date_label": "2001-06-14",
        "catalogue_transport_direction": None,
        "rows_per_catalogue": len(pairs),
        "exact_names_at_same_position": len(pairs) - len(differences),
        "source_name_variants_at_same_position": differences,
        "netease_named_rows_with_elements": sum(row["elements"] is not None for row in mirror),
        "netease_named_rows_with_skill_text": sum(row["skills"] is not None for row in mirror),
        "shared_east_south_coordinate_rows": shared_coordinates,
        "shared_initial_pet_phrase_positions": common_positions(mirror, numbered, "出生人物的初期宠物"),
        "shared_jss_prize_phrase_positions": common_positions(mirror, numbered, "在日本为JSS送的奖品"),
        "shared_explicit_information_gap_positions": common_positions(mirror, numbered, "目前尚无信息"),
        "independent_acquisition_witnesses_established": False,
    }


def growth_result(html):
    header = html.index("总成长率</div>")
    content = html[html.index("</tr>", header):html.index("经过评选", header)]
    cells = re.findall(r"<td\b[^>]*>(.*?)</td>", content, re.I | re.S)
    if len(cells) != 12 * 7:
        raise ValueError("growth results contain a missing or extra table cell")
    rows = []
    for start in range(0, len(cells), 7):
        values = [text(cell) for cell in cells[start:start + 7]]
        if not all(re.fullmatch(r"\d+\.\d{4}", x) for x in values[1:6]):
            raise ValueError("growth result contains an invalid decimal cell")
        post = re.search(r"forumid=239&postid=(\d+)", cells[start])
        if not post:
            raise ValueError("contest row lost its original forum locator")
        hp, attack, defense, agility, printed = map(Decimal, values[1:6])
        delta = attack + defense + agility - printed
        rows.append({
            "forum_post_id": int(post[1]),
            "hp": str(hp), "attack": str(attack), "defense": str(defense), "agility": str(agility),
            "printed_total": str(printed), "atk_def_agi_minus_printed_total": str(delta),
            "printed_rank": int(values[6]) if values[6] else None,
        })
    if len(rows) != 12 or len({row["forum_post_id"] for row in rows}) != 12:
        raise ValueError("growth results table extent changed")
    if [row["printed_rank"] for row in rows] != [1, 2, 3] + [None] * 9:
        raise ValueError("printed rankings changed")
    return rows


def checked_album(archive_path):
    with archive_path.open("rb") as archive:
        digest = file_digest(archive, "sha256").hexdigest()
    if (archive_path.stat().st_size, digest) != (ARCHIVE_SIZE, ARCHIVE_SHA):
        raise ValueError("TW10 retail archive pin mismatch")
    original = json.loads((ROOT / ALBUM).read_bytes())
    with ZipFile(archive_path) as zipfile:
        exe = zipfile.read("source/sa_3.exe")
    if sha(exe) != original["archive"]["files"]["source/sa_3.exe"]["sha256"]:
        raise ValueError("retail executable hash differs")
    return exe, {row["graphic_number"]: row for row in original["records"]}


def observed_name(graphic, exe, rows):
    row = rows[graphic]
    offset = row["source_file_offset"]
    original = exe[offset:offset + TABLE_STRIDE]
    name = original[4:24].split(b"\0", 1)[0].decode("cp950")
    if sha(original) != row["source_row_sha256"] or name != row["name_as_written"]:
        raise ValueError("matched client album row differs")
    return {"graphic_number": graphic, "name_as_written": name, "file_offset": offset, "row_sha256": sha(original)}


def audit(directory, archive):
    sources, pages = {}, {}
    for filename, (url, encoding, expected) in SOURCES.items():
        raw = (directory / filename).read_bytes()
        if sha(raw) != expected:
            raise ValueError("web response SHA mismatch: " + filename)
        sources[filename] = {"url": url, "bytes": len(raw), "sha256": expected, "encoding": encoding}
        pages[filename] = raw.decode(encoding, errors="strict")
    mirror = mirror_rows(pages["netease-index.html"])
    numbered = numbered_rows(pages["17173-acquisition.html"])
    compare = catalogue_comparison(mirror, numbered)
    exe, original_rows = checked_album(archive)
    skills = []
    for position, graphic in SIX_PETS.items():
        row = mirror[position - 1]
        skills.append({
            "netease_position_1_based": position, "name_as_written": row["name"],
            "element_text_normalized": row["elements"], "skill_column_text": row["skills"],
            "tw10_client_observation": observed_name(graphic, exe, original_rows),
            "skill_at_birth_established": False,
        })
    return {
        "schema": "stoneage.pet_detail34.period_player_catalogue_and_growth.r1",
        "sources": sources,
        "tw10_retail_archive": {"sha256": ARCHIVE_SHA, "bytes": ARCHIVE_SIZE, "sa_3_exe_sha256": sha(exe)},
        "catalogue_comparison": compare,
        "six_netease_skill_witnesses": skills,
        "name_variant_client_anchors": [observed_name(g, exe, original_rows) for g in (100269, 100310)],
        "growth_contest": {
            "listed_subject": "贝鲁伊卡", "event_date_label": "2003-05-30",
            "result_published_date_label": "2003-05-31", "eligibility_as_published": "未转生",
            "tw10_client_observation": observed_name(100328, exe, original_rows),
            "published_rows": growth_result(pages["sina-beluyika.html"]),
            "original_forum_screenshots_recovered": False,
            "in_game_verification_outcome_recovered": False,
        },
        "official_same_deployment_master_recovered": False,
        "official_birth_capture_skills_or_growth_fields_newly_verified": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path)
    parser.add_argument("tw10_archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.source_directory, args.tw10_archive), ensure_ascii=False, indent=2) + "\n", end="")


if __name__ == "__main__":
    main()
