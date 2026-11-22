"""PET-DETAIL13 original TW1 W skill slot writer + K capacity UI public replay.

No private original commercial EXE in CI. The separate private-source replay
must be run on an authorized local source archive for byte/objdump verification.
"""
import hashlib
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH="research/pets/PET-DETAIL-EVIDENCE13-TW10-ORIGINAL-W-SKILL-UI-BRIDGE-R1.json"
DOC="docs/continuity/STONEAGE-PET-DETAIL13-TW10-ORIGINAL-W-SKILL-UI-BRIDGE-20261122.md"

def read(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def gitblob(path):
    data=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()

class OriginalTW10PetSkills(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=read(PATH)
        cls.k=read(cls.d["prior_source_refs"]["K_client_original"]["path"])
        cls.schema=read(cls.d["prior_source_refs"]["original_gameplay_wire_schema"]["path"])
        cls.detail12=read(cls.d["prior_source_refs"]["K_to_UI_detail12"]["path"])

    def test_source_sha_and_immutable_history(self):
        d=self.d
        for x in d["prior_source_refs"].values():
            self.assertEqual(gitblob(x["path"]),x["git_blob"])
        self.assertEqual(gitblob("docs/CURRENT-STATE.md"),d["evidence_limits"]["original_CURRENT_git_blob"])
        self.assertEqual(d["source"]["original_member_sha256"],self.k["original_source"]["exe_sha256"])
        self.assertEqual(d["source"]["private_archive_sha256"],self.detail12["source"]["archive_sha256"])
        self.assertEqual(d["source"]["private_archive_bytes"],372626292)
        self.assertTrue(d["source"]["actual_original_archive_read_in_this_work"])
        self.assertFalse(d["source"]["original_binary_or_original_machinecode_published"])

    def test_original_W_memory_layout_and_source_field_order(self):
        w=self.d["W_original_native"]
        self.assertEqual(w["skill_rows_per_pet"],7)
        self.assertEqual(w["skill_row_bytes"],106)
        self.assertEqual(w["per_pet_bytes"],742)
        self.assertEqual(w["seven_record_storage_bytes"],7*106)
        self.assertEqual(w["five_local_pet_slot_storage_bytes_if_index_in_K_range"],5*742)
        self.assertEqual([(f["offset"],f["bytes"]) for f in w["row_layout"]],[(0,2),(2,2),(4,2),(6,2),(8,25),(33,73)])
        self.assertEqual(sum(f["bytes"] for f in w["row_layout"]),106)
        self.assertEqual(w["W_following_row_name_token_indices_1based"],[4,9,14,19,24,29,34])
        s=self.schema["records"]["pet_skill_view_slot"]
        self.assertEqual(s["slot_count"],w["skill_rows_per_pet"])
        self.assertEqual(s["record_width"],5)
        self.assertEqual([x["name"] for x in s["fields"]],["skill_id","field_context","target_class","name","comment"])
        self.assertFalse(w["W_pet_slot_count_bound_directly_checked"])

    def test_cross_packet_K_capacity_has_exact_original_struct_field(self):
        w=self.d["W_original_native"]
        token=w["K_max_skill_slots_field_token"]
        actual=self.k["k_parser"]["field_map"]
        k=next(v for v in actual if v["token"]==token)
        self.assertEqual(k["struct_offset"],64)
        self.assertEqual(k["name_from_early_lineage"],"max_skill_slots")
        self.assertEqual(w["K_original_pet_stride_bytes"],self.k["k_parser"]["stride"])
        self.assertEqual(int(w["K_original_pet_struct_base_va"],16)+64,int(w["K_capacity_field_zero_slot_va"],16))
        self.assertEqual(int(w["per_pet_base_va"],16)+8,0x17f7af0)
        self.assertEqual(int(w["per_pet_base_va"],16)+33,0x17f7b09)
        self.assertEqual(len(w["K_display_limit_source_read_va"]),2)
        self.assertEqual(len(w["W_ui_occupied_check_va"]),2)
        self.assertTrue(w["K_max_skill_slots_effective_display_limit_proven"])

    def test_private_replay_contract_is_specific_but_not_fake_CI_source_run(self):
        d=self.d
        r=d["private_replay"]
        self.assertEqual(len(r["source_windows"]),r["windows_passed"])
        self.assertEqual(len(r["disassembler_instruction_checks"]),r["disassembler_instructions_passed"])
        self.assertEqual(len(r["independent_u32_displacement_checks"]),r["u32_displacements_passed"])
        self.assertEqual([r["windows_passed"],r["disassembler_instructions_passed"],r["u32_displacements_passed"]],[7,22,8])
        for w in r["source_windows"]:
            self.assertEqual(len(w["sha256"]),64)
            self.assertEqual(w["end"]-w["start"]>0,True)
        self.assertEqual(len({a["va"] for a in r["disassembler_instruction_checks"]}),22)
        self.assertEqual(len({a["va"] for a in r["independent_u32_displacement_checks"]}),8)
        self.assertTrue(r["actual_private_replay_succeeded"])
        self.assertFalse(d["W_original_native"]["ui_path_truly_executed"])

    def test_no_early_official_skill_or_species_inflation(self):
        d=self.d
        e=d["evidence_limits"]
        for key in ("new_early_TW10_official_pet_skill_loadout_confirmed","new_early_TW10_server_pet_master_confirmed",
                    "new_early_TW10_official_birth_stats_confirmed","new_early_TW10_server_side_skill_effects_confirmed",
                    "new_original_live_pet_instances_captured","new_official_released_pet_species_confirmed",
                    "fully_historically_restored_dossiers"):
            self.assertEqual(e[key],0)
        self.assertEqual(e["TW10_dossier_count_unchanged"],124)
        self.assertTrue(e["no_early_K_W_sender_official_runtime_compatibility_claim"])
        self.assertTrue(e["no_W_index_validity_bounds_claim"])
        self.assertIsNone(e["overall_completion_percent"])
        self.assertIn("PET-DETAIL13",(ROOT/DOC).read_text(encoding="utf-8"))
        self.assertIn("PET-DETAIL13",(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8"))
        self.assertIn("test_stoneage_pet_detail13_tw10_w_skill_ui_bridge_r1.py",(ROOT/".github/workflows/validate-stoneage-pet-cn50-source-observations.yml").read_text(encoding="utf-8"))

if __name__=="__main__":unittest.main()
