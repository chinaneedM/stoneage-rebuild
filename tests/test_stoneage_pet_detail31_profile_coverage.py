"""Regression contract for full 124 original TW1 classic PC client pet dossiers."""
import copy
from decimal import Decimal
import json
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_pet_detail31_profile_coverage import audit
from tools.stoneage_pet_detail34_player_witnesses import RECEIPT, mirror_rows


ROOT = Path(__file__).resolve().parents[1]


class Pet31ProfileCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = audit(ROOT)

    def test_all_124_indexed_by_permanent_id(self):
        self.assertEqual(self.report["source_qualified_pet_dossiers"],124)
        self.assertEqual([x["pet_id"] for x in self.report["records"]],
                         ["PET-%06d" % i for i in range(1,125)])
        self.assertEqual(self.report["records"][0]["client_name_original"],"烏力")
        self.assertEqual(self.report["records"][-1]["client_graphic"],100430)

    def test_client_art_not_promoted_to_official_server_identity(self):
        c=self.report["field_coverage_counts_NOT_OFFICIAL_SPECIES_TOTALS"]
        self.assertEqual(c["client_name"],124)
        self.assertEqual(c["sprite_segment"],124)
        self.assertEqual(c["source_motion"],124)
        for field in ("official_pet_id","official_live_release","level1_stats",
                      "initial_stat_ranges","elements","growth","skills",
                      "capture","award","historically_complete"):
            with self.subTest(field=field):
                self.assertEqual(c[field],0)
        self.assertIsNone(self.report["overall_project_percent"])

    def test_missing_faces_have_same_source_motion_fallback_only(self):
        c=self.report["field_coverage_counts_NOT_OFFICIAL_SPECIES_TOTALS"]
        self.assertEqual(c["original_portrait"],120)
        self.assertEqual(c["original_pose_fallback_only"],4)
        self.assertEqual(
            self.report["missing_original_portrait_pet_ids"],
            ["PET-000116","PET-000117","PET-000118","PET-000119"],
        )
        for row in self.report["records"][115:119]:
            self.assertTrue(row["original_pose_fallback_when_face_missing"])
            self.assertIsNone(row["original_portrait_rd"])

    def test_false_or_zero_must_not_mean_unknown(self):
        from tools.stoneage_pet_detail31_profile_coverage import present
        self.assertTrue(present(False))
        self.assertTrue(present(0))
        self.assertFalse(present(None))

    def _fixture_root(self, root):
        from shutil import copy2, copytree
        dst = Path(root) / "research/pets"
        dst.mkdir(parents=True)
        copy2(ROOT / "research/pets/PET-ID-REGISTRY-R1.json",
              dst / "PET-ID-REGISTRY-R1.json")
        copytree(ROOT / "research/pets/profiles", dst / "profiles")
        return Path(root)

    def test_operator_issuance_does_not_require_server_numeric_pet_id(self):
        # The official release evidence is independent from an inaccessible
        # historical PET numeric server ID. A source-graded operator statement
        # must not be rejected merely because source_pet_id stays null.
        with tempfile.TemporaryDirectory() as tmp:
            root = self._fixture_root(tmp)
            file = root / "research/pets/profiles/TW10-G100250-WULI.json"
            j=json.loads(file.read_text(encoding="utf-8"))
            j["actual_official_pet_identity"]["status"]="VERIFIED_OFFICIAL_OPERATOR_SOURCE"
            j["actual_official_pet_identity"]["official_living_pet_release_proven"]=True
            self.assertIsNone(j["actual_official_pet_identity"]["source_pet_id"])
            file.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
            report=audit(root)
            counts=report["field_coverage_counts_NOT_OFFICIAL_SPECIES_TOTALS"]
            self.assertEqual(counts["official_live_release"],1)
            self.assertEqual(counts["official_pet_id"],0)

    def test_ungraded_formal_early_stat_is_not_silently_promoted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=self._fixture_root(tmp)
            file=root / "research/pets/profiles/TW10-G100250-WULI.json"
            j=json.loads(file.read_text(encoding="utf-8"))
            j["combat_stats"]["level_1"]["values"]["derived_hp"]=35
            # Grade intentionally stays OPEN_NOT_PROVEN, so this is a leak.
            file.write_text(json.dumps(j,ensure_ascii=False),encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "formally populated field lacks source grade"):
                audit(root)

    def test_source_registry_original_dossier_hashes_and_pc_scope(self):
        for row in self.report["records"]:
            self.assertEqual(len(row["dossier_git_blob"]),40)
            self.assertEqual(row["source_motion_sequences"],56)
            self.assertTrue(row["dossier_path"].startswith("research/pets/profiles/TW10-G"))
        self.assertEqual(self.report["fully_historical_pet_species_certified"],0)

    def test_period_player_evidence_does_not_fill_official_fields(self):
        replay = json.loads((ROOT / RECEIPT).read_bytes())
        comparison = replay["catalogue_comparison"]
        self.assertEqual(comparison["rows_per_catalogue"], 124)
        self.assertEqual(comparison["exact_names_at_same_position"], 122)
        self.assertFalse(comparison["independent_acquisition_witnesses_established"])
        self.assertEqual([r["position"] for r in comparison["source_name_variants_at_same_position"]], [21, 60])
        self.assertEqual(replay["official_birth_capture_skills_or_growth_fields_newly_verified"], 0)
        self.assertEqual(sum(r["skill_column_text"] is None for r in replay["six_netease_skill_witnesses"]), 2)
        self.assertTrue(all(not r["skill_at_birth_established"] for r in replay["six_netease_skill_witnesses"]))
        growth = replay["growth_contest"]
        self.assertFalse(growth["in_game_verification_outcome_recovered"])
        rows = growth["published_rows"]
        self.assertEqual(len(rows), 12)
        for row in rows:
            expected = sum(Decimal(row[k]) for k in ("attack", "defense", "agility")) - Decimal(row["printed_total"])
            self.assertEqual(Decimal(row["atk_def_agi_minus_printed_total"]), expected)
        self.assertEqual(rows[2]["printed_rank"], 3)
        self.assertEqual(rows[2]["atk_def_agi_minus_printed_total"], "-0.0360")

    def test_legacy_empty_skill_cells_keep_acquisition_text_separate(self):
        rows = mirror_rows(
            "宠物名称&nbsp;&nbsp;属性<BR>"
            "布伊&nbsp;&nbsp;地６水４&nbsp;&nbsp;&nbsp;某村<BR>"
            "加比&nbsp;&nbsp;地５风５&nbsp;&nbsp;毒攻击&nbsp;&nbsp;某洞<BR>----"
        )
        self.assertIsNone(rows[0]["skills"])
        self.assertEqual(rows[0]["acquisition"], "某村")
        self.assertEqual(rows[1]["skills"], "毒攻击")
        self.assertEqual(rows[1]["acquisition"], "某洞")


if __name__=="__main__":
    unittest.main()
