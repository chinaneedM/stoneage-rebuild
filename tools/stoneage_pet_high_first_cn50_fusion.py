"""Replay dated fusion screenshots and link their displayed names to the CN50 album."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from html import unescape
from itertools import groupby
import json
from pathlib import Path
import re

from tools.stoneage_pet_high_first_cn50_catalog import git_blob
from tools.stoneage_pet_high_first_cn50_sina import compiled_catalogues, element_claim
from tools.stoneage_stoneage5_cab_probe import parse_cab_files, parse_cab_header

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "research/pets/PET-HIGH-FIRST-CN50-FUSION-PANELS-R1.json"
URL = "https://games.sina.com.cn/z/sta/image{}.shtml"
PAGES = {
    1: (46774, "e377c04cad06fa8159bf045b6c52fad051eb997ed77d9e40915e8b2fd227cefb", "13:08"),
    2: (47144, "952bd87208bc49c159abaffed62ea9e0df5b8a25a56983ddc9eb4507c8db967d", "13:48"),
    3: (48042, "7f9ddfad91dcd2904f1e734cd64d09b96960cb7c3509afce091d91abb285d7d9", "13:52"),
}
NUMBERS = tuple(i for i in range(252, 297) if i not in range(256, 260))
# Transcribed from the in-game name field in the 41 GIFs, in printed row order.
PANEL_NAMES = (
    "庫瑪斯 雷瑪特 菲斯瑪 貝庫爾 畢格艾斯 裘比斯 阿卡西斯 洛可洛斯 法茲蒙特 雷格特 "
    "洛克爾 米恩斯特 利西亞 佩羅亞 伊利曼亞 卡力洛亞 奧普薩斯 利普多爾 邦克普斯 拉佛洛斯 "
    "迪亞古斯 馬魯古斯 爾洛普 卡克普 西修 哈爾修 弗利修 巴利 雅特拉斯 伊利亞德 米尼奈巴 "
    "德拉斯 科倫特 邦歐里 加雷 加古特 邦西普 伊亞歐萊 拉格多魯 西頓克爾 克羅那斯"
).split()
FOLD_NAME = str.maketrans("庫瑪貝爾畢茲亞羅奧薩馬魯倫歐萊頓", "库玛贝尔毕兹亚罗奥萨马鲁伦欧莱顿")
STATS = ("level", "xp", "next_xp", "current_hp", "max_hp", "attack", "defense", "agility", "loyalty")
ELEMENTS = ("earth", "water", "fire", "wind")
PET_INPUTS = ("机豹", "蒙奇", "猴子")
EXAMPLES = (("黑暴", "猴子", "黑暴"), ("机豹", "火蛇", "克克洛斯"))
MSI_JOIN = ROOT / "research/recovered/STONEAGE-STONEAGE5-REAL-CAB-MSI-PATH-JOIN-R1.json"
MSI_GIT_BLOB = "b2532248355b35cd9d4ed7d15d3f59aeeb9beadf"
MAY_PAGE = {
    "url": "https://games.sina.com.cn/zhqu/sta/article/2003-05-15/5848.shtml?from=wap",
    "article_date": "2003-05-15",
    "bytes": 70101,
    "sha256": "b60650b407fc8c8ad46658663d4662c792db4ff0ff16a574e9c2e8cd6cd5c0e4",
}
CAB_SHA = "d5dbf5a664211c2cee5fa92645a9e00290c1a4023a4b52ebf46c9402c2bcdfde"


def hex_hash(raw):
    return sha256(raw).hexdigest()


def stat_glyphs(image, lo, hi, y):
    def white(rgb):
        return min(rgb) > 205 and max(rgb) - min(rgb) < 6

    columns = [
        tuple(white(image.getpixel((x, row))) for row in range(y, y + 10))
        for x in range(lo, hi)
    ]
    return [tuple(group) for drawn, group in groupby(columns, any) if drawn]


def read_panels(directory):
    from PIL import Image

    images = {}
    receipts = {}
    for n in NUMBERS:
        path = directory / f"image-{n}.gif"
        raw = path.read_bytes()
        with Image.open(path) as im:
            if (im.format, im.size, im.n_frames) != ("GIF", (252, 247), 1):
                raise ValueError(f"unexpected image format for {n}")
            images[n] = im.convert("RGB")
        receipts[n] = {"sha256": hex_hash(raw), "bytes": len(raw)}

    # Each labelled digit is read in isolation before decoding the entire batch.
    examples = (
        (289, 99, 118, 82), (289, 61, 87, 58), (289, 99, 118, 106),
        (280, 61, 87, 202), (260, 61, 87, 202), (261, 61, 87, 202),
        (254, 61, 87, 202), (252, 61, 87, 202), (289, 61, 87, 154), (264, 61, 87, 178),
    )
    digits = {}
    for value, (n, lo, hi, y) in enumerate(examples):
        glyph, = stat_glyphs(images[n], lo, hi, y)
        digits[glyph] = str(value)
    if len(digits) != 10:
        raise ValueError("numeric glyphs are not unique")

    windows = (
        (61, 87, 58), (99, 118, 82), (99, 118, 106), (61, 88, 130), (108, 135, 130),
        (61, 87, 154), (61, 87, 178), (61, 87, 202), (61, 87, 226),
    )
    bars = ((161, (0, 255, 0)), (185, (0, 255, 255)), (209, (255, 0, 0)), (233, (255, 255, 0)))
    for n, im in images.items():
        values = {
            label: int("".join(digits[g] for g in stat_glyphs(im, *window)))
            for label, window in zip(STATS, windows, strict=True)
        }
        lengths = [sum(im.getpixel((x, y)) == color for x in range(171, 252)) for y, color in bars]
        weights = [round(length / 8) for length in lengths]
        if lengths != [min(weight * 8, 79) for weight in weights] or sum(weights) != 10:
            raise ValueError(f"unexpected element bars for {n}")
        receipts[n].update({
            "observed_stats": values,
            "element_bar_pixels": dict(zip(ELEMENTS, lengths, strict=True)),
            "observed_elements": dict(zip(ELEMENTS, weights, strict=True)),
        })
    return receipts


def page_rows(directory):
    for page, (size, fingerprint, time) in PAGES.items():
        raw = (directory / f"fusion-{page}.html").read_bytes()
        html = raw.decode("gb18030")
        if (len(raw), hex_hash(raw)) != (size, fingerprint) or f"2003-07-17 {time}" not in html:
            raise ValueError(f"source response or displayed date changed on page {page}")
        start = html.index("融合方法")
        table = html[start:html.index("</table>", start)]
        for row in re.findall(r"<tr\b[^>]*>(.*?)</tr\s*>", table, re.I | re.S):
            no, image, recipes = re.findall(r"<td\b[^>]*>(.*?)</td\s*>", row, re.I | re.S)
            img_url = re.search(r'\bsrc="(http://image2\.sina\.com\.cn/gm/zhuanqu/sq1/[^"]+\.gif)"', image)[1]
            lines = []
            for line in re.split(r"<br\b[^>]*>", recipes, flags=re.I):
                plain = "".join(unescape(re.sub(r"<[^>]*>", "", line)).split()).replace("＋", "+")
                if plain:
                    lines.append(plain)
            yield page, int(no), img_url, lines


def may_catalogue(directory, july_rows):
    raw = (directory / "may-fusion.html").read_bytes()
    if (len(raw), hex_hash(raw)) != (MAY_PAGE["bytes"], MAY_PAGE["sha256"]):
        raise ValueError("May editorial catalogue response changed")
    source = raw.decode("gb18030")
    start = source.index("融合方法", source.index("宠物名称", source.index("编号")))
    table = source[start:source.index("</table>", start)]
    compiled, native = compiled_catalogues()
    july = {row["printed_number"]: row for row in july_rows}
    may_rows = []
    for row in re.findall(r"<tr\b[^>]*>(.*?)</tr\s*>", table, re.I | re.S):
        cells = re.findall(r"<td\b[^>]*>(.*?)</td\s*>", row, re.I | re.S)
        num, name, elements, recipes = (
            "".join(unescape(re.sub(r"<[^>]*>", "", cell)).split()) for cell in cells
        )
        number = int(num)
        observed = element_claim(elements)
        slot = native[name]["ordinal"] if name in native else None
        if slot is not None and compiled[slot]["source_raw_first_i32"] != number - 1:
            raise ValueError(f"May catalogue name and number disagree at {number}")
        image = july.get(number)
        may_rows.append({
            "printed_number": number, "name_as_printed": name,
            "reported_elements": observed, "formula_cell_has_text": bool(recipes),
            "cn50_album_ordinal_by_exact_name": slot,
            "july_panel_same_printed_number": image is not None,
            "july_elements_match_by_printed_number": (
                all(observed.get(key, 0) == value for key, value in image["image"]["observed_elements"].items())
                if image else None
            ),
        })
    return {**MAY_PAGE, "rows": may_rows}


def album_links():
    compiled, native = compiled_catalogues()
    for number, display_name in zip(NUMBERS, PANEL_NAMES, strict=True):
        localized = display_name.translate(FOLD_NAME)
        row = native[localized]
        ordinal = row["ordinal"]
        if compiled[ordinal]["source_raw_first_i32"] != number - 1:
            raise ValueError(f"separate name and number links disagree for {display_name}")
        yield number, display_name, localized, ordinal


def installed_inventory():
    raw = MSI_JOIN.read_bytes()
    if git_blob(raw) != MSI_GIT_BLOB:
        raise ValueError("preserved installed path inventory changed")
    files = json.loads(raw)["installed_files"]
    names = [Path(row["installed_path"]).name.casefold() for row in files]
    candidates = sorted(
        name for name in names
        if re.match(r"(enemybase|enemy[0-9]|petskill|petmix|gmsv|saac)", name)
    )
    audio_count = sum(Path(name).suffix in {".sab", ".sap", ".wav"} for name in names)
    return files, {
        "files": len(files), "directory_sha256": CAB_SHA,
        "msi_installed_path_join_git_blob": MSI_GIT_BLOB,
        "audio_files": audio_count, "master_candidates_by_filename": candidates,
    }


def cab_inventory(path):
    with path.open("rb") as src:
        directory = src.read(65536)
    header = parse_cab_header(directory)
    raw_files, end = parse_cab_files(directory, header)
    if hex_hash(directory[:end]) != CAB_SHA:
        raise ValueError("preserved cabinet directory changed")
    installed_files, receipt = installed_inventory()
    for raw, installed in zip(raw_files, installed_files, strict=True):
        if (raw["index"], raw["name"], raw["size"]) != (
            installed["cab_index"], installed["cab_file_key"], installed["size"]
        ):
            raise ValueError("cabinet and installed path inventories disagree")
    return receipt


def replay(directory, cab):
    links = {number: (display, compiled, ordinal) for number, display, compiled, ordinal in album_links()}
    images = read_panels(directory)
    tuples = defaultdict(set)
    rows = []
    for page, number, url, lines in page_rows(directory):
        valid = [
            tuple(line.split("+")) for line in lines
            if re.fullmatch(r"[\u3400-\u9fff]+(?:\+[\u3400-\u9fff]+){2}", line)
        ]
        for recipe in valid:
            tuples[recipe].add(number)
        display, compiled, ordinal = links[number]
        inputs = Counter(key for recipe in valid for key in PET_INPUTS if key in recipe)
        rows.append({
            "printed_number": number,
            "page": page,
            "image_url": url.replace("http:", "https:", 1),
            "image": images[number],
            "displayed_name": display,
            "cn50_compiled_name": compiled,
            "cn50_album_ordinal": ordinal,
            "ordered_triplet_lines": len(valid),
            "other_lines": len(lines) - len(valid),
            "triplet_lines_with_input_as_written": dict(inputs),
        })
    if tuple(row["printed_number"] for row in rows) != NUMBERS:
        raise ValueError("unexpected catalogue row numbers")
    summary = {key: sum(r["triplet_lines_with_input_as_written"].get(key, 0) for r in rows) for key in PET_INPUTS}
    return {
        "schema": "stoneage.pet.cn50_sina_2003_fusion_panels.r1",
        "scope": "DATED_EDITORIAL_GIF_PANELS_AND_SAME_NAME_SOURCE_CLIENT_LOOKUP",
        "images": {"format": "GIF", "width": 252, "height": 247, "frames_per_image": 1},
        "pages": {
            str(n): {"url": URL.format(n), "bytes": size, "sha256": pin, "displayed_at": f"2003-07-17 {time}"}
            for n, (size, pin, time) in PAGES.items()
        },
        "preserved_client_cabinet": cab_inventory(cab),
        "may_editorial_catalogue": may_catalogue(directory, rows),
        "image_serving_build_or_operator_verified": False,
        "printed_number_is_official_pet_id": False,
        "observations_are_official_template_or_growth_parameters": False,
        "summary": {
            "level_one_panels": len(rows),
            "total_recipe_lines": sum(r["ordered_triplet_lines"] + r["other_lines"] for r in rows),
            "ordered_triplet_lines": sum(r["ordered_triplet_lines"] for r in rows),
            "triplet_lines_with_input_as_written": summary,
            "exact_ordered_triplets_linked_to_multiple_results": sum(len(v) > 1 for v in tuples.values()),
        },
        "conflict_examples": [
            {"inputs_as_written": list(recipe), "linked_printed_numbers": sorted(tuples[recipe])}
            for recipe in EXAMPLES
        ],
        "records": rows,
    }


def verify(report):
    expected = list(album_links())
    actual = [
        (row["printed_number"], row["displayed_name"], row["cn50_compiled_name"], row["cn50_album_ordinal"])
        for row in report["records"]
    ]
    receipts = [r["image"] for r in report["records"]]
    if actual != expected or len({im["sha256"] for im in receipts}) != len(expected):
        raise ValueError("catalogue mapping or unique image extent changed")
    for im in receipts:
        stats = im["observed_stats"]
        if (
            (stats["level"], stats["xp"], stats["next_xp"], stats["loyalty"]) != (1, 0, 2, 100)
            or stats["current_hp"] != stats["max_hp"]
            or sum(im["observed_elements"].values()) != 10
            or any(im["element_bar_pixels"][key] != min(im["observed_elements"][key] * 8, 79) for key in ELEMENTS)
        ):
            raise ValueError("invalid level-one panel observation")
    may = report["may_editorial_catalogue"]["rows"]
    if (
        [row["printed_number"] for row in may] != list(range(252, 297))
        or [row["printed_number"] for row in may if row["cn50_album_ordinal_by_exact_name"] is None] != [255]
        or [row["printed_number"] for row in may if not row["july_panel_same_printed_number"]] != [256, 257, 258, 259]
        or sum(row["july_elements_match_by_printed_number"] is True for row in may) != 41
    ):
        raise ValueError("May text and July panel cross-check changed")
    if report["schema"] != "stoneage.pet.cn50_sina_2003_fusion_panels.r1":
        raise ValueError("unexpected panel evidence schema")
    if (
        report["image_serving_build_or_operator_verified"]
        or report["printed_number_is_official_pet_id"]
        or report["observations_are_official_template_or_growth_parameters"]
        or report["preserved_client_cabinet"] != installed_inventory()[1]
    ):
        raise ValueError("unsupported deployment or template claim")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-directory", type=Path)
    parser.add_argument("--cab", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if (args.source_directory is None) != (args.cab is None) or (args.write and args.cab is None):
        parser.error("provide both --source-directory and --cab to replay the sources")
    stored = json.loads(TARGET.read_bytes()) if TARGET.exists() else None
    report = replay(args.source_directory, args.cab) if args.cab else stored
    verify(report)
    if args.write:
        TARGET.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif report != stored:
        raise ValueError("original-source replay differs from saved receipt")
    print(json.dumps(report["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
