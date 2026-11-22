"""Validate all CN5 preserved-client source-only pet album observations, not live official pets."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECOVERED=ROOT/"research"/"recovered"
PET=ROOT/"research"/"pets"
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))
def git_blob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()

class CN50SourceOnlyObservations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=read(RECOVERED/"STONEAGE-PET126R-CN50-PC-ORIGINAL-ALBUM-FULL-362-SLOT-SOURCE-CATALOGUE-R1.json")
        cls.tw=read(RECOVERED/"STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json")
        cls.batch=read(PET/"CN50-SOURCE-OBSERVATIONS-R1.json")
        cls.progress=read(PET/"PET-PROGRESS-R1.json")
        cls.registry=read(PET/"PET-ID-REGISTRY-R1.json")

    def test_source_counts_and_dated_provenance(self):
        source=self.src["records"]
        named=[x for x in source if x["label_as_compiled_GB18030"] is not None]
        self.assertEqual((len(source),len(named),len(source)-len(named)),(362,305,57))
        self.assertEqual(sum(x["label_as_compiled_GB18030"] is not None for x in source[:181]),124)
        self.assertEqual(sum(x["label_as_compiled_GB18030"] is not None for x in source[181:]),181)
        prefix={x["label_as_compiled_GB18030"] for x in source[:181] if x["label_as_compiled_GB18030"] is not None}
        tail=[x["label_as_compiled_GB18030"] for x in source[181:]]
        self.assertEqual(len(set(tail)),181)
        self.assertFalse(prefix.intersection(tail))
        inputs=self.batch["source_pins"]
        self.assertEqual(git_blob(ROOT / inputs["original_CN50_preserved_compiled_catalogue"]["path"]),inputs["original_CN50_preserved_compiled_catalogue"]["git_blob"])
        self.assertEqual(git_blob(ROOT / inputs["original_TW10_independent_retail"]["path"]),inputs["original_TW10_independent_retail"]["git_blob"])
        self.assertEqual(len(self.tw["records"]),124)
        self.assertEqual(inputs["original_CN50_preserved_compiled_catalogue"]["original_exe_sha256"],self.src["source"]["original_exe_sha256"])
        self.assertEqual(self.batch["original_source_362_slot_partition"],{
            "all_slots":362,"all_named":305,"all_empty":57,
            "first_181_slots_named":124,"first_181_slots_empty":57,
            "later_181_slots_named":181,"later_181_slots_empty":0
        })
        self.assertFalse(self.batch["source_limits"]["third_party_preserved_CN50_media_official_original_pressing_certified"])
        self.assertFalse(self.batch["source_limits"]["ordinal_graphic_formula_native_CN50_pet_selector_confirmed"])
        self.assertFalse(self.batch["source_limits"]["matched_physical_SPR_sha_proves_original_pet_name_graphic_binding"])
        self.assertFalse(self.batch["source_limits"]["source_trailing_u32_is_orig_portrait_alias_proven"])
        self.assertFalse(self.batch["source_limits"]["source_EXE_or_commercial_asset_executed_or_retrieved_this_unit"])
        self.assertEqual(self.batch["source_limits"]["historical_current_git_blob_unchanged"],git_blob(ROOT/"docs/CURRENT-STATE.md"))
        self.assertEqual(self.batch["source_limits"]["year_2026"],"NOT_YEAR_AUDITED")

    def test_all_181_docs_against_full_compiled_native_row_source(self):
        records=self.batch["records"]
        originals=self.src["records"][181:]
        self.assertEqual(len(records),181)
        self.assertEqual([x["observation_id"] for x in records],[f"OBS-CN50-SLOT-{n:04d}" for n in range(181,362)])
        with_spr=0;without_spr=0;source_spaces=[]
        seen=set()
        for b,o in zip(records,originals):
            self.assertEqual(b["compiled_album_slot_zero_based"],o["ordinal"])
            self.assertEqual(b["original_compiled_name_literal"],o["label_as_compiled_GB18030"])
            self.assertEqual(b["original_compiled_name_search_normalized"],o["label_as_compiled_GB18030"].strip())
            self.assertEqual(b["original_exe_source_row_offset"],o["source_exe_row_offset"])
            self.assertEqual(b["original_exe_row_sha256"],o["source_exe_row_sha256"])
            self.assertEqual(b["original_album_first_i32_source_literal"],o["source_raw_first_i32"])
            self.assertEqual(b["original_album_trailing_u32_source_literal"],o["source_raw_trailing_u32"])
            self.assertEqual(b["first_i32_meaning"],"LOCAL_COMPILED_ALBUM_NUMBER_NOT_SERVER_PET_SPECIES_ID")
            self.assertEqual(b["trailing_u32_meaning"],"UNRESOLVED_NATIVE_FIELD_NOT_CONFIRMED_PORTRAIT_ID")
            self.assertEqual(b["status"],"CLIENT_COMPILED_NAME_SOURCE_OBSERVATION_ONLY_NOT_OFFICIAL_PET_ROSTER")
            self.assertFalse(b["source_qualification"]["original_official_publisher_disc_or_patch_certified"])
            self.assertFalse(b["source_qualification"]["independently_authenticated_original_live_official_pet_species"])
            self.assertIsNone(b["source_qualification"]["observed_build_exact_historical_distribution_date"])
            s=b["source_same_cab_spr_segment"]
            self.assertEqual(s["tentative_TW10_formula_graphic_number_NOT_NATIVE_SELECTOR"],o["TW10_ordinal_based_graphic_hypothesis"])
            self.assertEqual(s["matching_same_CAB_physical_SPR_group_at_hypothetical_number"],o["same_CAB_SPR_group_for_hypothesis_present"])
            self.assertEqual(s["hypothetical_SPR_segment_sha256"],o["same_CAB_SPR_group_hash_for_hypothesis"])
            self.assertFalse(s["original_same_build_name_to_SPR_native_selector_proven"])
            self.assertFalse(s["sprite_pixels_independently_rendered_for_this_record"])
            self.assertIsNone(s["actual_native_graphic_number"])
            if s["matching_same_CAB_physical_SPR_group_at_hypothetical_number"]:
                self.assertEqual(len(s["hypothetical_SPR_segment_sha256"]),64)
                with_spr+=1
            else:
                self.assertIsNone(s["hypothetical_SPR_segment_sha256"])
                without_spr+=1
            missing=b["official_history_and_gameplay_missing"]
            self.assertIsNone(missing["assigned_permanent_PET_id"])
            self.assertIsNone(missing["original_same_deployment_pet_species_id"])
            self.assertFalse(missing["official_live_release_confirmed"])
            for field in ("actual_first_release_date","original_portrait_source_RD",
                          "original_level_1_stats_range","original_elements",
                          "original_growth_values_and_formula","innate_and_learned_skills",
                          "original_wild_capture_locations_and_conditions",
                          "quest_event_commercial_or_fusion_acquisition_proven"):
                self.assertIsNone(missing[field])
            mdpath=ROOT/b["doc_path"]
            self.assertTrue(mdpath.is_file(),mdpath)
            doc=mdpath.read_text(encoding="utf-8")
            self.assertIn(b["observation_id"],doc)
            self.assertIn(json.dumps(o["label_as_compiled_GB18030"],ensure_ascii=False),doc)
            self.assertIn(o["source_exe_row_sha256"],doc)
            self.assertIn("未确认官服实际发行宠物",doc)
            self.assertNotIn("PET-000125",doc)
            self.assertNotIn(b["observation_id"],seen)
            seen.add(b["observation_id"])
            if o["label_as_compiled_GB18030"].endswith(" "):source_spaces.append(o["ordinal"])
        self.assertEqual((with_spr,without_spr),(66,115))
        self.assertEqual(source_spaces,[223])
        self.assertEqual(self.batch["candidate_observations_counts"]["assigned_new_permanent_PET_ids"],0)
        self.assertEqual(self.batch["candidate_observations_counts"]["confirmed_new_official_living_original_PC_species"],0)
        self.assertEqual(self.batch["candidate_observations_counts"]["later_181_source_named_rows_with_hypothetical_SPR_present"] if "later_181_source_named_rows_with_hypothetical_SPR_present" in self.batch["candidate_observations_counts"] else self.batch["candidate_observations_counts"]["with_same_CAB_SPR_group_at_TW10_ordinal_hypothesis"],66)

    def test_pet_registry_and_historical_progress_still_124(self):
        self.assertEqual(len(self.registry["catalog_entries"]),124)
        count=self.progress["per_pet_profile_counts"]
        self.assertEqual((count["individual_detailed_profiles"],count["fully_historically_verified_pet_profiles"]),(124,0))
        other=self.progress["other_version_source_observations"]
        self.assertEqual((other["later_181_slots_new_individual_source_observation_documents"],other["later_181_source_named_rows_with_hypothetical_SPR_present"],other["later_181_source_named_rows_without_hypothetical_SPR"],other["newly_allocated_permanent_PET_numbers"]),(181,66,115,0))
        listing=(ROOT/"docs/pets/CN50-SOURCE-OBSERVATIONS.md").read_text(encoding="utf-8")
        self.assertEqual(listing.count("| [OBS-CN50-SLOT-"),181)
        self.assertIn("不是历史上新增181只宠物",listing)
        self.assertIn("SOURCE",self.batch["entry_tier"])

if __name__=="__main__":unittest.main()
