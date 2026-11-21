"""PET126T: original classic-PC pet source coverage and no official species promotion."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/"research"/"recovered"

def source(filename):
    return json.loads((REC/filename).read_text(encoding="utf-8"))

def part(rows):
    named=[r for r in rows if r["label_as_compiled_GB18030"]]
    empty=[r for r in rows if not r["label_as_compiled_GB18030"]]
    hit=lambda a:sum(bool(r["same_CAB_SPR_group_for_hypothesis_present"]) for r in a)
    return {
        "slots":len(rows),"named":len(named),"empty":len(empty),
        "named_with_ordinal_hypothesis_SPR":hit(named),
        "named_without_ordinal_hypothesis_SPR":len(named)-hit(named),
        "empty_with_ordinal_hypothesis_SPR":hit(empty),
        "empty_without_ordinal_hypothesis_SPR":len(empty)-hit(empty),
        "exact_TW10_named_SPR_segments":sum(r["TW10_retail_exact_same_SPR_segment_at_this_ordinal"] is True for r in rows)
    }

class PET126TSourceGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit=source("STONEAGE-PET126T-PC-MODULE-SOURCE-COVERAGE-AND-STOP-GATE-R1.json")
        cls.album=source("STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json")
        cls.delta=source("STONEAGE-PET126S-PET20-PC-SEVEN-DIMENSION-SOURCE-DELTA-R1.json")
        cls.base=source("STONEAGE-PET-MODULE-20-FIELD-COVERAGE-AND-SOURCE-STOP-MATRIX-R1.json")
        cls.year=source("STONEAGE-PET126-YEAR2026-YTD-CLASSIC-PC-SOURCE-AND-MODULE-GAPS-R1.json")
        cls.queue=source("STONEAGE-PET27-GLOBAL-YEAR-VERSION-WORK-QUEUE-R1.json")
        cls.receipt=source("STONEAGE-PET126S-CN50-PC-NATIVE-PLUS36-ACCEPTANCE-R1.json")

    def test_all_362_records_and_original_two_half_coverage(self):
        rows=self.album["records"]
        tally=self.audit["machine_verified_album_source_partition"]["coverage"]
        self.assertEqual(tally["all"],part(rows))
        self.assertEqual(tally["first_181"],part(rows[:181]))
        self.assertEqual(tally["last_181"],part(rows[181:]))
        self.assertEqual((len(rows),tally["all"]["named"],tally["all"]["empty"]),(362,305,57))
        self.assertEqual((tally["first_181"]["named_with_ordinal_hypothesis_SPR"],
                          tally["first_181"]["empty_with_ordinal_hypothesis_SPR"],
                          tally["last_181"]["named_with_ordinal_hypothesis_SPR"],
                          tally["last_181"]["named_without_ordinal_hypothesis_SPR"]),(124,30,66,115))
        self.assertEqual(tally["all"]["exact_TW10_named_SPR_segments"],124)
        self.assertEqual(len({r["record_key"] for r in rows}),362)
        self.assertEqual(sorted(r["source_raw_first_i32"] for r in rows if r["label_as_compiled_GB18030"]),list(range(305)))

    def test_client_local_names_never_promote_to_official_live_species(self):
        rows=self.album["records"]
        self.assertTrue(all(r["CN50_name_to_SPR_native_selector_proven"] is False for r in rows))
        self.assertTrue(all(r["original_official_live_pet_release_proven"] is False
                            and r["original_server_species_identifier"] is None for r in rows))
        self.assertIsNone(self.album["metrics"]["historical_total_species"])
        self.assertIsNone(self.audit["machine_verified_album_source_partition"]["historical_total_official_species"])
        self.assertEqual(self.audit["machine_verified_album_source_partition"]["new_official_original_PC_species_confirmed_this_unit"],0)
        self.assertEqual(self.audit["machine_verified_album_source_partition"]["same_source_exe_sha256"],
                         self.receipt["source_original_exe_sha256"])
        self.assertFalse(self.delta["original_native_source_delta"]["native_original_pet_SPR_selector_proven"])
        self.assertFalse(self.delta["original_native_source_delta"]["native_runtime_execution_proven"])

    def test_seven_pet_fields_and_six_regions_remain_open(self):
        dim=self.audit["seven_dimensions"]
        self.assertEqual([d["id"] for d in dim],[d["id"] for d in self.base["seven_pet_dimensions"]])
        self.assertEqual([d["id"] for d in dim],[d["id"] for d in self.delta["seven_dimensions"]])
        self.assertEqual(len(dim),7)
        self.assertTrue(all(d["closed"] is False and d["reopen_with"] for d in dim))
        regions=self.audit["chronology"]["six_region_status"]
        self.assertEqual(set(regions),set(self.year["region_reviews"]))
        self.assertTrue(all(not d["year_closed"] and d["official_historical_species_count"] is None
                            and d["reopen_with"] for d in regions.values()))
        self.assertEqual(self.queue["current_frontier"]["year"],2026)
        self.assertEqual(self.audit["chronology"]["current_2026_year_gate"],"NOT_YEAR_AUDITED")
        self.assertTrue(self.audit["chronology"]["year_not_closed"])
        self.assertIsNone(self.audit["delivery_stop_gate"]["overall_game_completion_percent"])
        self.assertFalse(self.audit["delivery_stop_gate"]["user_authorized_switch_to_NPC"])
        self.assertFalse(self.audit["delivery_stop_gate"]["module_source_bounded_closed"])

    def test_historical_current_full_byte_blob_protected(self):
        b=(ROOT/"docs"/"CURRENT-STATE.md").read_bytes()
        self.assertEqual(len(b),2709173)
        git_sha=hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\\0"+b).hexdigest()
        self.assertEqual(git_sha,"c89e0e33537990aa2132b47c40fef49a985a935c")
        self.assertEqual(git_sha,self.audit["delivery_stop_gate"]["historical_current_state_git_blob_to_preserve"])

    def test_scope_and_milestone_source_fidelity(self):
        a=self.audit
        self.assertEqual(a["scope"],"ORIGINAL_CLASSIC_2D_PC_ONLY")
        self.assertEqual(a["source_level_this_unit"],
                         "INDEPENDENT_REPLAY_OF_ALREADY_COMMITTED_SOURCE_DERIVED_GIT_JSON_NO_NEW_PROPRIETARY_BYTES_AND_NO_NATIVE_EXECUTION")
        self.assertEqual(a["starting_main_head"],"4b95e3222a174eb5669ccd549414e98b6e1eb076")
        self.assertEqual(a["delivery_stop_gate"]["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(a["delivery_stop_gate"]["stage_B_and_wiki"],"GATED")
        self.assertFalse(a["delivery_stop_gate"]["future_original_game_design_started"])

if __name__=="__main__":
    unittest.main()
