"""Replay the six fixed public catalogues without treating submitted rows as server data."""
import argparse
from collections import Counter
from hashlib import sha256
from html import unescape
import json
from pathlib import Path
import re

from tools.stoneage_pet_high_first_77_panel_witnesses import REPORT, REPORT_BLOB, ROOT, birth_deltas, blob, inputs, panels


EVIDENCE = ROOT / "research/pets/PET-HIGH-FIRST-79-CATALOGUE-PANEL-SCREEN-R1.json"
PAGES = {755: ("079", 10, "楊格斯"), 777: ("126", 54, "佩露夏"), 901: ("225", 30, "葛雷基歐"),
         902: ("226", 30, "葛雷洛比"), 903: ("227", 30, "葛雷吉鲁"), 904: ("228", 30, "葛雷馬恩")}
GRADES = {(True, True): "BOTH", (True, False): "CLAIMED_ONLY", (False, True): "SAVED_ONLY",
          (False, False): "NEITHER"}


def plain(fragment):
    return unescape(re.sub(r"<[^>]*>", "", fragment)).strip()


def read_page(raw):
    text = raw.decode("utf-8")
    title = plain(re.search(r"<title>(.*?)</title>", text, re.S | re.I)[1]).split(">>")[0].strip()
    numeric_rows = []
    announced = {}
    for tr in re.findall(r"<tr\b[^>]*>(.*?)</tr\s*>", text, re.S | re.I):
        # The site emits some <th> cells with </td> closing tags.
        cells = [plain(c) for c in re.findall(r"<t[hd]\b[^>]*>(.*?)</t[hd]\s*>", tr, re.S | re.I)]
        if len(cells) == 12 and all(c.isdecimal() for c in cells[:6]):
            numeric_rows.append(list(map(int, cells[:6])))
        for i, cell in enumerate(cells[:-1]):
            if cell in {"血值", "攻值", "防值", "敏值"}:
                match = re.fullmatch(r"(\d+)\s*~\s*(\d+)", cells[i + 1])
                if match:
                    announced[cell] = list(map(int, match.groups()))
    assert list(announced) == ["血值", "攻值", "防值", "敏值"] and numeric_rows
    return title, list(announced.values()), numeric_rows


def verify(evidence, captured_sources=None):
    assert evidence["schema"] == "stoneage.pet79.catalogue_panels.r1"
    assert evidence["submitted_measurement_date_or_build_verified"] is False
    assert evidence["official_deployment_proven"] is False
    raw = REPORT.read_bytes()
    assert blob(raw) == REPORT_BLOB
    variants = {row["template_id"]: row for row in json.loads(raw)["rows"] if row["selected_fields_differing_from_claim"]}
    claims = inputs()["master"]["pet_flag_1_field_projections"]
    deltas = birth_deltas()
    assert [p["template_id"] for p in evidence["pages"]] == list(PAGES) == list(variants)
    result = []
    totals = Counter()
    for page in evidence["pages"]:
        tid = page["template_id"]
        number, family, label = PAGES[tid]
        assert (page["catalogue_number"], page["page_name"]) == (int(number), label)
        assert page["url"] == f"https://ww.welovesa.com/pet.php?pet_id={number}&pet_type={family}&trans=0"
        if captured_sources:
            captured = (captured_sources / f"catalog-{number}.html").read_bytes()
            assert (len(captured), sha256(captured).hexdigest()) == (page["capture_bytes"], page["capture_sha256"])
            assert read_page(captured) == (label, page["site_stat_ranges"], page["displayed_rows"])

        variant = variants[tid]
        master = claims[variant["position"]]
        assert master["name"].replace("魯", "鲁") == label
        claimed = panels(master["base"], master["initnum"], deltas)
        saved = panels(variant["selected_fields_differing_from_claim"]["base"], master["initnum"], deltas)
        eligible = [tuple(r[2:]) for r in page["displayed_rows"] if r[:2] == [0, 1]]
        occurrences = Counter(GRADES[(candidate in claimed, candidate in saved)] for candidate in eligible)
        distinct = Counter(GRADES[(candidate in claimed, candidate in saved)] for candidate in set(eligible))
        outside_displayed_ranges = sum(any(x < lo or x > hi for x, (lo, hi) in zip(panel, page["site_stat_ranges"], strict=True))
                                       for panel in eligible)
        item = dict(template_id=tid, selected_rows=len(eligible), distinct_panels=len(set(eligible)),
                    skipped_levels_or_rebirth=len(page["displayed_rows"]) - len(eligible),
                    occurrence_grades=dict(occurrences), distinct_grades=dict(distinct),
                    outside_site_stat_ranges=outside_displayed_ranges)
        assert item == page["screen"]
        result.append(item)
        totals.update(occurrences)
    assert sum(x["selected_rows"] for x in result) == 279
    assert sum(x["distinct_panels"] for x in result) == 219
    assert sum(x["skipped_levels_or_rebirth"] for x in result) == 2
    assert totals == {"BOTH": 169, "CLAIMED_ONLY": 16, "SAVED_ONLY": 6, "NEITHER": 88}
    return dict(occurrence_grades=dict(totals), pages=result, official_deployment_proven=False)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--captured-sources", type=Path)
    args = p.parse_args()
    print(json.dumps(verify(json.loads(EVIDENCE.read_bytes()), args.captured_sources), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
