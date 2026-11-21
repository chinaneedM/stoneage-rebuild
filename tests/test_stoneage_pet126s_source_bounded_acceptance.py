"""PET126S: source-custody, native callsite and seven-dimensional non-promotion."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research/recovered"
def read(name):return json.loads((R/name).read_text(encoding="utf-8"))

class PET126SSourceAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=read("STONEAGE-PET126S-CN50-PC-ORIGINAL-RUNTIME-ALBUM-U32-CONSUMER-R1.json")
        cls.matrix=read("STONEAGE-PET126S-PET20-PC-SEVEN-DIMENSION-SOURCE-DELTA-R1.json")
        cls.receipt=read("STONEAGE-PET126S-CN50-PC-NATIVE-PLUS36-ACCEPTANCE-R1.json")
        cls.prior=read("STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json")
        cls.pet126f=read("STONEAGE-PET126F-SOURCE-CUSTODY-SEVEN-DIMENSION-RESIDUAL-R1.json")
        cls.year=read("STONEAGE-PET126-YEAR2026-YTD-CLASSIC-PC-SOURCE-AND-MODULE-GAPS-R1.json")
    def test_real_original_pc_sha_and_exact_two_literal_sites(self):
        s=self.source
        self.assertEqual(s["source"]["exe_sha256"],self.receipt["source_original_exe_sha256"])
        self.assertEqual(s["source"]["original_instruction_count"],131461)
        sites=s["native_direct_access_to_runtime_record_plus36"]
        self.assertEqual(sites["all_hit_instruction_addresses"],["0x434774","0x439f0e"])
        self.assertEqual(sites["by_access_class"],{
            "EXPLICIT_MEMORY_WRITE":1,"EXPLICIT_MEMORY_TEST_OR_PUSH_READ":1})
        self.assertFalse(s["summary"]["indirect_alias_analysis_completed"])
    def test_five_stack_arguments_to_same_native_callee(self):
        obj=self.source["native_five_argument_album_field_callsite"]
        self.assertTrue(obj["native_plus36_u32_is_fourth_pushed_argument_at_this_single_callsite"])
        self.assertEqual((obj["callee_original_static_target"],obj["source_call_instruction_va"]),
                         ("0x453b68","0x439f2b"))
        self.assertTrue(obj["caller_cleans_exactly_20_bytes_after_call"])
        self.assertEqual(obj["static_cdecl_shaped_arguments_first_to_fifth"][3],
                         "original_runtime_record_plus36_value")
        instr={a["va"]:a["instruction"] for a in obj["callee_first_96_linear_instructions"]}
        self.assertEqual(instr["0x453bf4"],"mov    eax,DWORD PTR [ebp+0x14]")
        self.assertEqual(instr["0x453bf7"],"and    DWORD PTR [esi+0xc],0x0")
        self.assertEqual(instr["0x453bfb"],"mov    DWORD PTR [esi+0x8],eax")
        self.assertEqual(instr["0x453bcf"],"mov    DWORD PTR [ebp+0x14],eax")
        self.assertFalse(obj["callee_identity_as_real_bitmap_or_original_sprite_selector_proven"])
    def test_pet126r_name_candidate_totals_not_species(self):
        m=self.matrix["counters_source_rows_not_species"]
        c=self.prior["metrics"]
        self.assertEqual((len(self.prior["records"]),c["compiled_source_named_rows"],c["compiled_source_empty_rows"]), (362,305,57))
        self.assertEqual(m["CN50_hypothesis_SPR_hits"],190)
        self.assertEqual(m["TW10_CN50_exact_cross_version_SPR_segments"],124)
        self.assertIsNone(m["official_worldwide_PC_species_total"])
        self.assertEqual(m["CN50_same_build_official_species_proven"],0)
    def test_all_seven_dimensions_and_six_regions_open(self):
        m=self.matrix
        self.assertEqual([d["id"] for d in m["seven_dimensions"]],
                         [d["id"] for d in self.pet126f["seven_dimensions"]])
        self.assertEqual(len(m["seven_dimensions"]),7)
        self.assertTrue(all(not d["field_closed"] and d["reopen_condition"] for d in m["seven_dimensions"]))
        self.assertEqual(set(m["six_region_year2026_status"]),set(self.year["region_reviews"]))
        self.assertTrue(all(not v["year_complete"] and v["reopen_condition"]
                            for v in m["six_region_year2026_status"].values()))
        self.assertEqual(m["decision"]["year2026"],"NOT_YEAR_AUDITED")
        self.assertFalse(m["decision"]["another_module_authorized"])
        self.assertIsNone(m["decision"]["overall_percent"])
    def test_receipt_pins_source_blobs_and_negative_gates(self):
        c=self.receipt;m=self.matrix;s=self.source
        self.assertEqual(c["source_original_run"],44884234678)
        self.assertTrue(c["source_actions_success"])
        self.assertEqual(c["permanent_static_derived"]["git_blob_sha"],
                         "60f6f89b6616b4011702fe1983d52dada9aec486")
        self.assertEqual(c["permanent_seven_dimension_gap"]["git_blob_sha"],
                         "4f5d0c0ea0f6f4034093e465d48956487ece3969")
        self.assertFalse(c["negative"]["actually_drawn_original_SPR_or_REAL_graphic_proven"])
        self.assertFalse(c["negative"]["official_server_live_pet_issuance_proven"])
        self.assertFalse(c["negative"]["original_optical_disc_pressing_certified"])
        self.assertFalse(c["negative"]["pet_source_closed"])
        self.assertEqual(c["negative"]["historical_CURRENT_blob_unmodified"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
if __name__=="__main__":unittest.main()
