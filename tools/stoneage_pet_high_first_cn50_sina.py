"""Index dated Sina PC pet catalogue claims against independently pinned CN50 names."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from html import unescape
import json
from pathlib import Path
import re

from tools.stoneage_pet126k_cn50_original_exe_probe import EXPECTED
from tools.stoneage_pet126m_cn50_pe_album_xrefs import pe32_text_identity
from tools.stoneage_pet_detail36_cn50_album_portrait_join import ALBUM
from tools.stoneage_pet_high_first_cn50_catalog import ROOT, git_blob
from tools.stoneage_pet_high_first_cn50_native import TARGET as NATIVE

REPORT = ROOT / "research/pets/PET-HIGH-FIRST-CN50-SINA2003-CATALOG-R1.json"
PAGE_URL = "https://games.sina.com.cn/zhqu/sta/cwzl/chongwu{}.shtml"
PAGE_PINS = {
    "02": (83644, "203b144e1378c1b21559ab07a55047bb09ede9de516a5d750e69284a28851e12", 122),
    "03": (73292, "4bd30515dab24b1734417ddd2d7e39e320948bf20a1b502269240e2bc1ccdf72", 115),
}
ROW_PIN = "8b1058a43c267dfeaa298d4c2c472209cebd24d9"
NATIVE_PIN = "98fea71c051dfa887b91154a8a72d17c67b57744"
ELEMENTS = {"地": "earth", "水": "water", "火": "fire", "风": "wind"}
YEAR_CARD_PAGE = {
    "original_url": "http://news.17173.com/content/2002-4-18/n955_871742.html",
    "archive_url": "https://web.archive.org/web/20030411062929id_/http://news.17173.com:80/content/2002-4-18/n955_871742.html",
    "displayed_article_date": "2002-04-18",
    "stated_card_launch_date": "2002-04-20",
    "response_bytes": 15013,
    "response_sha256": "993ac25035484dcc83e5d931f37b9fd2b75f79b90e94ae0b44d2072279cf4f0d",
}
YEAR_CARD_CONTEXT = {
    "february_profile": {
        "file": "year-x.html",
        "url": "https://web.archive.org/web/20030228025258id_/http://news.17173.com:80/content/2002-2-8/n955_871422.html",
        "displayed_date": "2002-02-08",
        "response_bytes": 14939,
        "response_sha256": "89004e5518001dc743a3a549b572629f30025e8f6e757f38d21f26bef8403af7",
    },
    "taiwan_january_collection": {
        "file": "year-card-early.html",
        "url": "https://web.archive.org/web/20030228022044id_/http://news.17173.com:80/content/2002-1-29/n107_23735.html",
        "displayed_date": "2002-01-29",
        "response_bytes": 13658,
        "response_sha256": "2b51243b5daf071e2fe73c4e536ce84d1b05bc28e330dbf0c70522720a96e63d",
        "stated_region": "TW",
        "stated_cards_in_complete_set": 56,
        "stated_reward_variants": 4,
    },
}
YEAR_BEAST_HEADING = r"([地水火风])之属性(?:奇兽|年兽)——(葛雷[\u3400-\u9fff]+)"
SILENCE_TEXT = "沉默中无法吟唱咒术。"
SILENCE_WINDOWS = (
    ("command_menu_checks_status", 0x403CAB, 0x403CCE,
     "0c296172ead86b56b933b8993e8c0baac903097108a56e846e7c45b6c1974128"),
    ("warning_and_menu_state_reset", 0x403D1F, 0x403D4E,
     "b4d0a2a9a2a7e7ce7b78aaa852054e0a22d70ef7aae54f0f64df15ace0e36c17"),
    ("status_argument_equals_one", 0x443154, 0x443164,
     "ce6d3c993b3e041d7d809c0b9f5b33185fef11e468ffe6bc88c259c550411b48"),
    ("incoming_state_dispatch", 0x45C034, 0x45C06C,
     "a710f0c7fa8eb98c5d3f85197b6ba04da0085f5b6c9e7bca9b01b40d26973c01"),
    ("battle_menu_reads_same_status", 0x40656E, 0x406595,
     "e102e1e90b3e1c37f1706ab29061c866c50aefad20099fcb1c15ef8a2f324152"),
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(label):
    return "".join(label.split())


def text_cell(cell):
    return " ".join(unescape(re.sub(r"<[^>]*>", " ", cell)).split())


def source_pages(directory):
    for page, (size, fingerprint, count) in PAGE_PINS.items():
        raw = (directory / f"sina-{page}.html").read_bytes()
        if (len(raw), sha(raw)) != (size, fingerprint):
            raise ValueError(f"Sina preserved response fingerprint changed: {page}")
        html = raw.decode("gb18030")
        header = html.index("LV1的捕捉地点或取得方式")
        extent = html[header:html.index("</table>", header)]
        rows = [
            [text_cell(cell) for cell in re.findall(r"<td\b[^>]*>(.*?)</td\s*>", block, re.I | re.S)]
            for block in re.findall(r"<tr\b[^>]*>(.*?)</tr\s*>", extent, re.I | re.S)
        ]
        if len(rows) != count or any(len(row) != 5 for row in rows):
            raise ValueError(f"Sina catalogue table shape changed: {page}")
        yield page, rows


def compiled_catalogues():
    catalogues = []
    for file, pin in ((ROOT / ALBUM, ROW_PIN), (NATIVE, NATIVE_PIN)):
        raw = file.read_bytes()
        if git_blob(raw) != pin:
            raise ValueError(f"CN50 catalogue source changed: {file.name}")
        catalogues.append(json.loads(raw)["records"])
    compiled, native = catalogues
    by_ordinal = {row["ordinal"]: row for row in compiled}
    for row in native:
        source = by_ordinal[row["ordinal"]]
        if (source["label_as_compiled_GB18030"] != row["compiled_name"]
            or source["source_exe_row_sha256"] != row["exe_row_sha256"]):
            raise ValueError("saved client name/SPR source row conflict")
    return by_ordinal, {compact(row["compiled_name"]): row for row in native}


def element_claim(value):
    value = compact(value)
    if not re.fullmatch(r"(?:[地水火风][0-9]{1,2})+", value):
        raise ValueError(f"unexpected printed element format: {value!r}")
    pairs = re.findall(r"([地水火风])([0-9]{1,2})", value)
    claim = {ELEMENTS[key]: int(number) for key, number in pairs}
    if len(claim) != len(pairs) or sum(claim.values()) != 10:
        raise ValueError(f"invalid printed element distribution: {value!r}")
    return claim


def replay(directory):
    _, native = compiled_catalogues()
    rows = []
    for page, entries in source_pages(directory):
        for position, (number, label, elements, skill, acquisition) in enumerate(entries, 1):
            # Keep page position even when the printed number is duplicated or non-numeric.
            if not re.fullmatch(r"[0-9]+|转", number):
                raise ValueError(f"unexpected printed catalogue number: {number!r}")
            pet = native.get(compact(label))
            rows.append({
                "page": page, "row_in_pet_table": position,
                "printed_number": int(number) if number.isdecimal() else None,
                "rebirth_variant_label": number == "转",
                "normalized_row_sha256": sha(
                    json.dumps([number, label, elements, skill, acquisition], ensure_ascii=False).encode()
                ),
                "cn50_album_ordinal_by_name_only": pet["ordinal"] if pet else None,
                "reported_elements": element_claim(elements),
                "innate_skill_cell_has_text": bool(skill),
                "level_one_acquisition_cell_has_text": bool(acquisition),
            })
    return rows


def replay_year_card(source):
    raw = source.read_bytes()
    if (len(raw), sha(raw)) != (YEAR_CARD_PAGE["response_bytes"], YEAR_CARD_PAGE["response_sha256"]):
        raise ValueError("year card archive fingerprint changed")
    html = raw.decode("gb18030")
    if not all(anchor in html for anchor in ("2002-4-18", "4月20日上市", "注册后均可得年兽一只")):
        raise ValueError("archive lost the dated card and registration text")
    claims = re.findall(YEAR_BEAST_HEADING, html)
    if [element for element, _ in claims] != list(ELEMENTS):
        raise ValueError("unexpected list of four year-beast names")
    return [{"published_name": name, "main_element": ELEMENTS[element]} for element, name in claims]


def verify_year_card_context(directory, beast_names):
    html = {}
    for key, receipt in YEAR_CARD_CONTEXT.items():
        raw = (directory / receipt["file"]).read_bytes()
        if (len(raw), sha(raw)) != (receipt["response_bytes"], receipt["response_sha256"]):
            raise ValueError(f"year card companion fingerprint changed: {receipt['file']}")
        html[key] = raw.decode("gb18030")
    names = [name for _, name in re.findall(YEAR_BEAST_HEADING, html["february_profile"])]
    if names != [variant["published_name"] for variant in beast_names]:
        raise ValueError("February profile and April list names disagree")
    if not all(anchor in html["taiwan_january_collection"] for anchor in ("台湾消息", "56张", "四只不同属性", "扑满乌力")):
        raise ValueError("Taiwan collection evidence changed")


def summarize(rows):
    compiled, native = compiled_catalogues()
    native_by_ordinal = {row["ordinal"]: row for row in native.values()}
    if len(native_by_ordinal) != 305 or len(rows) != 237:
        raise ValueError("unexpected compiled or web catalogue extent")
    for page, (_, _, count) in PAGE_PINS.items():
        if [r["row_in_pet_table"] for r in rows if r["page"] == page] != list(range(1, count + 1)):
            raise ValueError(f"invalid source row positions: {page}")
    numbers = Counter(row["printed_number"] for row in rows if row["printed_number"] is not None)
    linked = Counter(row["cn50_album_ordinal_by_name_only"] for row in rows
                     if row["cn50_album_ordinal_by_name_only"] is not None)
    singles, number_conflicts, unlinked_tw10 = [], [], []
    for row in rows:
        ordinal = row["cn50_album_ordinal_by_name_only"]
        if linked[ordinal] != 1:
            continue
        singles.append(row)
        if compiled[ordinal]["source_raw_first_i32"] + 1 != row["printed_number"]:
            number_conflicts.append([row["page"], row["row_in_pet_table"], ordinal])
        if native_by_ordinal[ordinal]["earlier_tw10_relation"] == "EARLY_TW10_NOT_LINKED":
            unlinked_tw10.append(row)
    return {
        "compiled_name_slots_with_sina_citation": len(linked),
        "single_source_row_per_name": len(singles),
        "multiple_source_rows_per_name_ordinals": sorted(i for i, count in linked.items() if count > 1),
        "unmatched_sina_rows": len(rows) - sum(linked.values()),
        "same_number_as_client_index_plus_one_among_single_name_links": len(singles) - len(number_conflicts),
        "other_number_among_single_name_links": number_conflicts,
        "duplicate_printed_numbers": sorted(n for n, count in numbers.items() if count > 1),
        "missing_printed_numbers_from_1_to_244": sorted(set(range(1, 245)) - numbers.keys()),
        "single_name_links_with_acquisition_cell": sum(r["level_one_acquisition_cell_has_text"] for r in singles),
        "single_name_links_with_skill_cell": sum(r["innate_skill_cell_has_text"] for r in singles),
        "single_name_links_without_earlier_tw10_link": len(unlinked_tw10),
        "single_name_links_without_earlier_tw10_link_with_acquisition_cell":
            sum(r["level_one_acquisition_cell_has_text"] for r in unlinked_tw10),
    }


def silence_metadata():
    return {
        "source_filename": "sa_5000.exe",
        "source_bytes": EXPECTED["sa_5000.exe"][0],
        "source_sha256": EXPECTED["sa_5000.exe"][1],
        "message": SILENCE_TEXT,
        "message_file_offset": 0x6FFCC,
        "code_windows": [
            {"role": role, "start_va": start, "end_va_exclusive": end, "sha256": pin}
            for role, start, end, pin in SILENCE_WINDOWS
        ],
        "client_state_and_command_menu_verified_statically": True,
        "specific_pet_effect_duration_and_server_owner_verified": False,
    }


def verify_silence(program_file):
    program = program_file.read_bytes()
    if (len(program), sha(program)) != EXPECTED["sa_5000.exe"]:
        raise ValueError("incorrect CN50 source executable")
    literal = SILENCE_TEXT.encode("gb18030")
    start = silence_metadata()["message_file_offset"]
    if program.find(literal + b"\0") != start or program.count(literal + b"\0") != 1:
        raise ValueError("silence message source location changed")
    base, (_, rva, offset, length) = pe32_text_identity(program)
    for role, start, end, pin in SILENCE_WINDOWS:
        left, right = offset + start - base - rva, offset + end - base - rva
        if not (offset <= left < right <= offset + length and sha(program[left:right]) == pin):
            raise ValueError(f"silence code window changed: {role}")


def make_report(rows, year_beasts):
    _, native = compiled_catalogues()
    if [variant["main_element"] for variant in year_beasts] != list(ELEMENTS.values()):
        raise ValueError("year card coverage changed")
    card_rows = []
    for variant in year_beasts:
        name = variant["published_name"]
        card_rows.append({
            "published_name": name, "main_element": variant["main_element"],
            "cn50_album_ordinal_by_name_only": native[name]["ordinal"],
        })
    return {
        "schema": "stoneage.pet.cn50_sina_2003_source_crosswalk.r1",
        "scope": "MAINLAND_CLASSIC_PC_SINA_EDITORIAL_AND_PRESERVED_CN50_CLIENT",
        "pages": {
            page: {"url": PAGE_URL.format(page), "displayed_date": "2003-04-07",
                   "response_bytes": size, "response_sha256": pin, "rows": count}
            for page, (size, pin, count) in PAGE_PINS.items()
        },
        "client_source_git_blobs": {"compiled_album": ROW_PIN, "native_spr_lookup": NATIVE_PIN},
        "client_silence_state": silence_metadata(),
        "cn30_year_card_announcement": {
            **YEAR_CARD_PAGE,
            "registration_documents_one_animal": True,
            "individual_awards_verified": False,
            "named_variants": card_rows,
        },
        "year_card_adjacent_archives": YEAR_CARD_CONTEXT,
        "selection": "NAME_EXACT_AFTER_WHITESPACE_REMOVAL",
        "serving_version_and_official_release_established_by_web_join": False,
        "published_number_is_server_species_id": False,
        "metrics": summarize(rows),
        "rows": rows,
    }


def render(result):
    header = {key: value for key, value in result.items() if key != "rows"}
    head = json.dumps(header, ensure_ascii=False, indent=2, sort_keys=True).removesuffix("\n}")
    rows = ",\n".join(
        "    " + json.dumps(row, ensure_ascii=False, sort_keys=True) for row in result["rows"]
    )
    return head + ',\n  "rows": [\n' + rows + "\n  ]\n}\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-directory", type=Path)
    parser.add_argument("--client", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write and (args.source_directory is None or args.client is None):
        parser.error("--write requires both source pages and the pinned client")
    if args.client:
        verify_silence(args.client)
    if args.source_directory:
        rows = replay(args.source_directory)
        year_beasts = replay_year_card(args.source_directory / "yeararchive.html")
        verify_year_card_context(args.source_directory, year_beasts)
    else:
        archived = json.loads(REPORT.read_bytes())
        rows = archived["rows"]
        year_beasts = archived["cn30_year_card_announcement"]["named_variants"]
    result = make_report(rows, year_beasts)
    rendered = render(result)
    if args.write:
        REPORT.write_text(rendered, encoding="utf-8")
    elif rendered != REPORT.read_text(encoding="utf-8"):
        raise SystemExit("Sina catalogue receipt does not match the replay")
    print(json.dumps(result["metrics"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
