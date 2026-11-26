"""Verify the captured 2012 horse panels and their conditional model comparison."""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
from fractions import Fraction
from hashlib import sha256
import html
import json
from pathlib import Path
import re

from tools.stoneage_pet_growth_model import RANK_ROLL_RANGES, pet_level_increments, pet_rank_from_template_base
from tools.stoneage_pet_high_first_77_panel_witnesses import REPORT, REPORT_BLOB, ROOT, WITNESSES, birth_deltas, blob, inputs, panels


EVIDENCE = ROOT / "research/pets/PET-HIGH-FIRST-78-2012-HORSE-PANEL-WITNESSES-R1.json"
NUMBER_COLUMNS = ("hp", "attack", "defense", "quick")
SAMPLE = re.compile(
    r"(\d+\s+\d+\s+\d+\s+\d+)\s*│\s*(\d+)\s*│\s*"
    r"(\d+\s+\d+\s+\d+\s+\d+)\s*│\s*([0-9.]+\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+)"
)


def read_panels(raw):
    text = html.unescape(re.sub(r"<[^>]*>", " ", raw.decode("utf-8").split("</body>")[0]))
    # The mirror repeats its own table in HTML metadata, the visible body and
    # serialized page state. The source rows in this capture are distinct.
    samples = {}
    for a, level, b, averages in SAMPLE.findall(text):
        key = (tuple(map(int, a.split())), int(level), tuple(map(int, b.split())), tuple(averages.split()))
        samples.setdefault(key, dict(initial=list(key[0]), final_level=key[1], final=list(key[2]),
                                     reported_averages=list(key[3])))
    return list(samples.values())


def capture_rows(receipt, directory):
    # Local acquisition bytes are transient. The repository holds only fingerprints
    # and the numeric projection, so routine CI needs no third-party HTML.
    raw = (directory / receipt["capture_filename"]).read_bytes()
    assert (len(raw), sha256(raw).hexdigest()) == (receipt["bytes"], receipt["sha256"])
    return read_panels(raw)


def verify_capture(evidence, directory):
    for post in evidence["posts"]:
        raw_rows = capture_rows(post, directory)
        assert raw_rows == [{k: row[k] for k in raw_rows[0]} for row in post["rows"]]
    old = capture_rows(evidence["older_repost_capture"], directory)
    projected = {(tuple(r["initial"]), r["final_level"], tuple(r["final"])) for r in old}
    assert all((tuple(r["initial"]), r["final_level"], tuple(r["final"])) in projected
               for r in json.loads(WITNESSES.read_bytes())["rows"])
    image = evidence["photo"]
    raw = (directory / image["capture_filename"]).read_bytes()
    assert (len(raw), sha256(raw).hexdigest()) == (image["bytes"], image["sha256"])


def arithmetic_conflicts(row):
    conflicts = []
    for column, (start, end, shown) in enumerate(zip(row["initial"], row["final"],
                                                    row["reported_averages"], strict=True)):
        n = row["final_level"] - 1
        growth = Fraction(end - start, n)
        places = max(2, len(shown.partition(".")[2]))
        # Allow either rounding or truncation at the reported precision.
        if abs(growth - Fraction(shown)) >= Fraction(1, 10**places):
            conflicts.append(dict(field=NUMBER_COLUMNS[column], exact_increment=str(growth),
                                  reported_average=shown))
    return conflicts


def minimum_final_quick(base, row):
    rank = pet_rank_from_template_base(*base)
    lower_growth_base = (*base[:3], base[3] - 2)
    dex_gain = pet_level_increments(lower_growth_base, rank, (0,) * 10, RANK_ROLL_RANGES[rank][0])[3]
    internal_lower_bound = row["initial"][3] * 100 + (row["final_level"] - 1) * dex_gain
    return internal_lower_bound // 100


def derive(evidence):
    assert evidence["schema"] == "stoneage.pet78.2012_horse_panels.r1"
    assert evidence["official_deployment_proven"] is False
    assert evidence["same_deployment_birth_and_growth_proven"] is False
    assert evidence["older_repost_capture"]["numeric_rows_matched"] == 12
    raw = REPORT.read_bytes()
    assert blob(raw) == REPORT_BLOB
    row = next(r for r in json.loads(raw)["rows"] if r["template_id"] == evidence["template_id"] == 904)
    template = inputs()["master"]["pet_flag_1_field_projections"][row["position"]]
    assert (template["name"], template["elements"]) == ("葛雷馬恩", [0, 0, 20, 80])
    a = template["base"]
    b = row["selected_fields_differing_from_claim"]["base"]
    deltas = birth_deltas()
    claimed = panels(a, template["initnum"], deltas)
    saved = panels(b, template["initnum"], deltas)
    counts = Counter()
    conflicts = []
    exclusive = []
    for post in evidence["posts"]:
        expected_date = datetime.fromtimestamp(post["ptt_epoch"], timezone(timedelta(hours=8))).isoformat()
        assert post["published_asia_taipei"] == expected_date
        for index, observed in enumerate(post["rows"]):
            initial = tuple(observed["initial"])
            in_claimed, in_saved = initial in claimed, initial in saved
            classification = "BOTH" if in_claimed and in_saved else "CLAIMED_ONLY" if in_claimed else "SAVED_ONLY" if in_saved else "NEITHER"
            counts[classification] += 1
            assert observed["conditional_initial_panel"] == classification
            disagreements = arithmetic_conflicts(observed)
            assert observed["published_arithmetic_conflicts"] == disagreements
            if disagreements:
                conflicts.append([post["id"], index + 1])
            if classification != "BOTH":
                exclusive.append((post["id"], index + 1, observed))
    assert len(evidence["posts"]) == 5 and counts == {"BOTH": 16, "CLAIMED_ONLY": 1}
    assert len(exclusive) == 1 and exclusive[0][:2] == ("main", 7)
    discriminator = exclusive[0][2]
    lower = minimum_final_quick(a, discriminator)
    assert lower == 164 > discriminator["final"][3] == 154
    assert conflicts == [["main", 7], ["main", 8]]
    picture = evidence["photo"]
    linked = next(post for post in evidence["posts"] if post["id"] == picture["post_id"])["rows"][picture["printed_row"] - 1]
    assert linked["initial"] == picture["nickname_numbers"] and picture["actual_level1_panel_visible"] is False
    assert (picture["level"], picture["visible_final_panel"]) == (linked["final_level"], linked["final"])
    assert linked["conditional_initial_panel"] == "BOTH"
    return dict(posts=5, rows=17, conditional_birth_compatibility=dict(counts), row_arithmetic_conflicts=conflicts,
                exclusive_row_conditional_level122_quick_lower_bound=lower,
                screenshot_confirmed_final_panels=1, same_deployment_accepted=0)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--captured-sources", type=Path)
    args = p.parse_args()
    evidence = json.loads(EVIDENCE.read_bytes())
    if args.captured_sources:
        verify_capture(evidence, args.captured_sources)
    print(json.dumps(derive(evidence), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
