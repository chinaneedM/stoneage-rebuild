"""PET34: source-exact custody of September 1999 print beta notice, not a released-pet roster.

1999 Play Online No.015 original third-party preserved scanned PDF. Native text
extraction is unreliable; this script checks BYTES/PDF identity only and cannot
certify page transcription or claim a pet was released in-game.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://www.kingpin.info/download/kingpin/media/magazine/Play_Online_Issue_015_%28Japanese%29_1999-09.pdf"
BYTES = 31915180
SHA256 = "fd6cb9e4a3f7023115ebff91042d7c9b4a8c956b822c5ffd6379230ec5ee328c"
PAGES = 167


def require(test, message):
    if not test:
        raise ValueError(message)


def build(raw, final_url, pages):
    require(final_url == URL, "source redirect changed")
    require(len(raw) == BYTES, "wrong original magazine PDF size")
    require(raw.startswith(b"%PDF-"), "not the magazine PDF")
    require(hashlib.sha256(raw).hexdigest() == SHA256, "original magazine PDF SHA drift")
    require(pages == PAGES, "unexpected magazine page count")
    return {
        "schema": "stoneage.pet34.jp1999_september_beta_print_source_custody.r1",
        "source": {
            "public_preservation_url": URL,
            "publication": "Play Online",
            "issue": "No.015",
            "issue_month": "1999-09",
            "source_category": "CONTEMPORANEOUS_THIRD_PARTY_PRESERVED_MAGAZINE_SCAN",
            "bytes": BYTES,
            "sha256": SHA256,
            "page_count": PAGES,
            "pdf_original_saved_in_public_repo": False,
            "verified_from": "EXACT_BYTES_AND_NATIVE_PDF_PAGE_COUNT",
            "native_japanese_text_reliable": False,
            "manual_physical_copy_collation_proven": False
        },
        "preexisting_source_context": {
            "already_in_project": "research/origin/JSS-1999-ORIGIN-EVIDENCE-R1.md",
            "source_bounded_claim": "SEPTEMBER_1999_BETA_ANNOUNCED_200_PLAY_ONLINE_READER_ACCOUNT_SLOTS",
            "existing_announced_beta_window": "1999-09-01_TO_1999-09-30",
            "not_new_betatest_proof": True,
            "announced_beta_execution_proven_by_this_source": False
        },
        "new_direct_audit": {
            "probe_success_run_ids": [43712624585, 43713031321],
            "source_pdf_sha_now_independently_authenticated": True,
            "native_text_layer_garbled_in_probe": True,
            "probe_selective_exact_stoneage_keyword_pages": 0,
            "printed_page_036_original_artwork_human_legible_confirmed": False,
            "unverified_web_transcription_beta_bonus_detail": "CANDIDATE_ONLY_REQUIRES_ORIGINAL_PAGE_VISUAL_COLLATION",
            "beta_bonus_was_pet_proven": False,
            "original_beta_game_disc_or_executable_recovered": False,
            "original_retail_disc_and_species_roster_recovered": False,
            "any_specific_1999_species_obtainable_proven": False,
            "new_qualified_named_pets": [],
            "historical_1999_pet_population_count": None
        },
        "guardrails": {
            "beta_reward_word_is_not_pet_species": True,
            "unreadable_text_layer_does_not_prove_absence_of_pets": True,
            "magazine_issue_date_is_not_live_pet_release_date": True,
            "do_not_join_2001_manual_or_2003_revived_client_as_1999_build": True,
            "do_not_copy_scanned_magazine_page_or_original_game_assets_to_repo": True,
            "active_module": "PET",
            "current_frontier_year": 1999,
            "year_review_status": "NOT_YEAR_AUDITED"
        }
    }



def fetch_exact_magazine(max_attempts=3, fetcher=urlopen, pause=time.sleep):
    """Retry transient downloads, fail-closed unless the original URL, length and SHA match.

    A truncated PDF or an HTML error body must never reach PyMuPDF as an original scan.
    Keep source identity constraints exactly as strict as build().
    """
    require(max_attempts >= 1, "attempt count must be positive")
    last_error = None
    for attempt in range(max_attempts):
        try:
            with fetcher(Request(URL, headers={"User-Agent": "Mozilla/5.0 (compatible; StoneAgeHistoricalEvidence/1.0)"}), timeout=120) as response:
                raw = response.read(BYTES + 1)
                final_url = response.url
            require(final_url == URL, "source redirect changed")
            require(len(raw) == BYTES, "wrong original magazine PDF size")
            require(raw.startswith(b"%PDF-"), "not the magazine PDF")
            require(hashlib.sha256(raw).hexdigest() == SHA256, "original magazine PDF SHA drift")
            return raw, final_url
        except (OSError, ValueError) as exc:
            last_error = exc
            if attempt + 1 < max_attempts:
                pause(min(attempt + 1, 2))
    raise ValueError("original magazine PDF not recovered with exact URL/size/SHA after retries") from last_error


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    if args.input:
        raw = args.input.read_bytes()
        final = URL
    else:
        raw, final = fetch_exact_magazine()
    # The same exact-identity guard also covers a caller-supplied --input file.
    require(final == URL, "source redirect changed")
    require(len(raw) == BYTES, "wrong original magazine PDF size")
    require(raw.startswith(b"%PDF-"), "not the magazine PDF")
    require(hashlib.sha256(raw).hexdigest() == SHA256, "original magazine PDF SHA drift")
    import fitz
    pdf = fitz.open(stream=raw, filetype="pdf")
    report = build(raw, final, len(pdf))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"PET34_SOURCE_BYTES": len(raw),
                      "PET34_SOURCE_SHA256": hashlib.sha256(raw).hexdigest(),
                      "PET34_PAGES": len(pdf),
                      "PET34_NEW_NAMED_RELEASED_PETS": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
