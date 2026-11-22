"""PET-DETAIL14 pinned community W skill-sender comparison, not original-official runtime."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E="research/pets/PET-DETAIL-EVIDENCE14-THREE-PC-W-SKILL-SENDER-LINEAGES-R1.json"

def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def git_blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()

class ThreePcSkillSenderCrosswalk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=read(E)
        cls.native=read(cls.d["original_TW10"]["native_pet13_path"])
        cls.schema=read(cls.d["original_TW10"]["wire_schema_path"])
        cls.k_crosswalk=read(cls.d["crosswalk"]["K_schema_audit_path"])

    def test_source_receipts_and_unmodified_history(self):
        s=self.d["original_TW10"]
        self.assertEqual(git_blob(s["wire_schema_path"]),s["wire_schema_blob"])
        self.assertEqual(git_blob(s["native_pet13_path"]),s["native_pet13_blob"])
        self.assertEqual(git_blob("docs/CURRENT-STATE.md"),self.d["gates"]["original_current_blob"])
        self.assertEqual(s["authentic_exe_sha256"],self.native["source"]["original_member_sha256"])
        self.assertEqual(s["skill_slots"],self.native["W_original_native"]["skill_rows_per_pet"])
        self.assertEqual(s["skill_stride_bytes"],self.native["W_original_native"]["skill_row_bytes"])
        self.assertEqual(s["skill_buffer_per_pet_bytes"],7*106)

    def test_three_archives_six_files_and_sender_shape(self):
        rows=self.d["later_server_sources"]
        self.assertEqual(len(rows),3)
        self.assertEqual(len({x["repo"] for x in rows}),3)
        for x in rows:
            for k in ("commit","char_blob","header_blob"):
                self.assertEqual(len(x[k]),40)
            self.assertEqual(x["source_grade"],"PINNED_COMMUNITY_PC_SERVER_SOURCE_NOT_1999_2002_OFFICIAL_SAME_DEPLOYMENT")
            self.assertEqual(x["sender_case"],"case 'w'")
            self.assertEqual(x["W_prefix"],"W%d|")
            self.assertEqual(x["MAX_PET_COUNT"],5)
            self.assertEqual(x["MAX_PET_SKILL_SLOT_COUNT"],7)
            self.assertEqual(x["per_skill_field_count"],5)
            self.assertEqual(x["per_pet_skill_field_count"],35)
            self.assertEqual(x["source_skill_id_lookup"],"CHAR_getPetSkill(pindex,petskillloop)")
            self.assertEqual(x["source_skill_definition_lookup"],"PETSKILL_getPetskillArray(skillid)")
            self.assertEqual(x["valid_skill_field_order"],[
                "PETSKILL_ID","PETSKILL_FIELD","PETSKILL_TARGET",
                "PETSKILL_NAME","PETSKILL_COMMENT"])
            self.assertEqual(x["empty_definition_wire_literal"],"|||||")

    def test_original_W_client_shape_not_overstated_as_full_wire(self):
        s=self.schema["records"]["pet_skill_view_slot"]
        original=self.d["original_TW10"]
        self.assertEqual(s["slot_count"],7)
        self.assertEqual(s["record_width"],5)
        self.assertEqual([x["name"] for x in s["fields"]],original["W_fields"])
        self.assertEqual(original["full_packet_fields"],35)
        c=self.d["crosswalk"]
        self.assertEqual(c["sources_examined"],3)
        self.assertEqual(c["source_files_examined"],6)
        self.assertTrue(c["W_same_field_positions"])
        self.assertTrue(c["runtime_pet_instance_skill_ids_not_static_global_species_loadout"])
        self.assertEqual(c["first_known_K_cross_version_schema_mismatch_token"],20)
        self.assertEqual(self.k_crosswalk["cross_source_observation"]["first_incompatible_early_token"],20)
        self.assertFalse(c["full_wire_runtime_compatibility_proven"])
        self.assertFalse(c["native_early_official_server_W_sender_found"])
        self.assertFalse(c["native_early_official_pet_master_found"])
        self.assertTrue(c["later_repo_timestamp_not_original_era_proof"])

    def test_no_early_official_skill_claims_and_documents(self):
        g=self.d["gates"]
        self.assertEqual(g["TW10_dossiers"],124)
        self.assertEqual(g["TW10_partials"],124)
        for key in ("TW10_historically_full","new_early_official_birth_skills",
                    "new_early_official_skill_effects",
                    "new_early_official_server_files","new_official_pet_species"):
            self.assertEqual(g[key],0)
        self.assertIsNone(g["overall_percent"])
        doc=(ROOT/"docs/continuity/STONEAGE-PET-DETAIL14-THREE-PC-W-SKILL-SENDERS-20261122.md").read_text(encoding="utf-8")
        idx=(ROOT/"docs/pets/INDEX.md").read_text(encoding="utf-8")
        for row in self.d["later_server_sources"]:
            self.assertIn(row["repo"],doc)
        self.assertIn("PET-DETAIL14",idx)

if __name__=="__main__":
    unittest.main()
