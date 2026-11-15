"""PET32: verify two JSS 1999 battle/mail clauses against exact archived primary source.

Only two source-clause meanings are derived. No original HTML or full
commercial text is included in the committed machine receipt.
"""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

from tools.stoneage_jss_pet_patch_history import URL, SHA, change_rows
from tools.stoneage_jss1999_pet_source_census import SOURCE_BYTES
from tools.stoneage_jss_pet_faq import compact, require

PARENT = Path("research/recovered/STONEAGE-PET31-JSS1999-ALL-CLAUSE-CENSUS-R1.json")
EXPECTED = [
    ("1999-11-22", 31, 3, 90, "4e1b95514e7a7154bb2d01e4530738b3cbec7fdbaec14b723481a25be7353851"),
    ("1999-11-26", 30, 0, 25, "d4bc63f3f1ba485d41bbac66c1a39ddacbb6ae60e121506d5d4f8fb5219b1c56"),
]


def semantically_validate(date, clause):
    """Guard the explicit affirmative / negative scope without relying on keyword counts."""
    if date == "1999-11-22":
        require("戦闘中でもメールが使えるようになりました" in clause, "ordinary battle mail absent")
        require("ただし、ペットメールは使用できません" in clause, "pet-mail exclusion absent")
        require("ショートカット" in clause and "ウィンドウバー" in clause, "mail interface anchors absent")
    elif date == "1999-11-26":
        require("戦闘中のペットメールに関する不具合を修正しました" in clause, "battle pet-mail bug-fix wording absent")
    else:
        raise ValueError("unapproved date")


def build(raw, final_url):
    require(final_url == URL, "archive capture/final URL changed")
    require(len(raw) == SOURCE_BYTES and hashlib.sha256(raw).hexdigest() == SHA,
            "original JSS bytes/custody changed")
    history = change_rows(raw.decode("shift_jis", errors="strict"))
    require(len(history) == 40, "source row count changed")
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    require(parent["source"]["sha256"] == SHA and len(parent["dated_rows_1999"]) == 15,
            "previous PET31 source index changed")
    results = []
    for date, order, clause_order, length, digest in EXPECTED:
        row = history[order]
        require(row["date"] == date, "original chronology changed")
        clauses = [compact(c) for c in row["text"].split("・") if compact(c)]
        clause = clauses[clause_order]
        require(len(clause) == length and hashlib.sha256(clause.encode("utf-8")).hexdigest() == digest,
                "specific source clause SHA/length changed")
        previous = next(x for x in parent["dated_rows_1999"]
                        if x["original_source_order"] == order)
        require(previous["operator_written_date"] == date
                and previous["clauses"][clause_order]["normalized_sha256"] == digest,
                "PET31 previous source identity disagrees")
        semantically_validate(date, clause)
        if date == "1999-11-22":
            status_normal = "EXPLICITLY_AVAILABLE_BY_OPERATOR_CHANGELOG"
            status_pet = "EXPLICITLY_UNAVAILABLE_AS_OF_THIS_WRITTEN_CHANGE"
        else:
            status_normal = "NOT_RESTATED_IN_THIS_CLAUSE"
            status_pet = "BUG_FIX_RECORDED_WITH_UNSPECIFIED_SYMPTOM_AND_POLICY"
        results.append({
            "operator_date": date,
            "original_source_order": order,
            "clause_order_in_entry": clause_order,
            "normalized_characters": length,
            "normalized_sha256": digest,
            "ordinary_mail_during_battle": status_normal,
            "pet_mail_during_battle": status_pet,
            "actual_game_execution_proven": False,
        })
    return {
        "schema": "stoneage.pet32.jss1999_battle_mail_semantic_r1",
        "source": {"url": URL, "bytes": SOURCE_BYTES, "sha256": SHA,
                   "archive_capture": "20010417162544",
                   "source_type": "ARCHIVED_JSS_FIRST_PARTY_OPERATOR_CHANGELOG"},
        "parent_pet31_index": str(PARENT),
        "original_operator_dated_entries_total": 40,
        "original_operator_dated_entries_1999": 15,
        "source_bounded_semantic_records": results,
        "inference_barriers": {
            "keyword_pet_mail_does_not_mean_feature_allowed": True,
            "nov_26_bug_fix_does_not_prove_nov_22_battle_restriction_removed": True,
            "operator_written_dates_not_independently_observed_server_execution": True,
            "official_named_pet_release_not_proven": True,
            "client_or_server_build_not_recovered": True,
        },
        "new_official_named_pet_species": [],
        "year_1999": "NOT_YEAR_AUDITED",
        "current_frontier_year": 1999,
        "private_commercial_original_published": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.input:
        raw, final_url = args.input.read_bytes(), URL
    else:
        with urlopen(Request(URL, headers={"User-Agent": "StoneAge-Historical-Research/1.0"}),
                     timeout=60) as response:
            raw, final_url = response.read(), response.url
    result = build(raw, final_url)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_sha256": SHA,
                      "source_exact_clauses": len(result["source_bounded_semantic_records"]),
                      "ordinary_mail_1999_11_22": "AVAILABLE_DURING_BATTLE",
                      "pet_mail_1999_11_22": "EXPLICITLY_UNAVAILABLE",
                      "pet_mail_1999_11_26": "BUG_FIX_SCOPE_UNSPECIFIED",
                      "official_species_added": 0, "year_frontier": 1999}))


if __name__ == "__main__":
    main()
