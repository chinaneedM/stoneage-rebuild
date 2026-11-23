"""Reproducible 305 original PC source rows with TW1 as optional evidence."""
import unittest

from tools.stoneage_pet_high_first_cn50_catalog import COLUMNS, TARGET, build, render


class HighFirstCN50SourceAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.stats = build()
        cls.mapping = {r[0]: dict(zip(COLUMNS, r)) for r in cls.rows}

    def test_exact_305_source_rows_replay(self):
        self.assertEqual(render(self.rows), TARGET.read_text(encoding="utf-8"))
        self.assertEqual(len(self.rows), 305)
        self.assertEqual(len(self.mapping), 305)
        self.assertEqual(len({r[2] for r in self.rows}), 305)

    def test_high_version_records_are_not_gated_by_tw10(self):
        n = [x for x in self.mapping.values()
             if x["early_tw10_relation_OPTIONAL_NOT_ENTRY_GATE"] == "EARLY_TW10_NOT_LINKED"]
        self.assertEqual(len(n), 181)
        for v in n:
            self.assertEqual(v["earlier_tw10_name_if_evidenced"], "")
            self.assertTrue(v["cn50_original_rd_sha256"])
            self.assertEqual(v["official_live_release"], "NOT_VERIFIED")

    def test_bounded_formula_spr_does_not_claim_native_selector(self):
        self.assertEqual((self.stats["has_formula_spr"], self.stats["no_formula_spr"]), (190, 115))
        self.assertEqual((self.stats["unlinked_has_spr"], self.stats["unlinked_no_spr"]), (66, 115))
        self.assertEqual(self.stats["duplicate_spr_hash_rows"], 5)
        for v in self.mapping.values():
            self.assertEqual(v["native_name_to_spr_identity"], "NOT_VERIFIED")
            self.assertEqual(v["same_build_original_server_pet_id"], "NOT_VERIFIED")
            self.assertEqual(v["birth_growth_skill_capture"], "NOT_VERIFIED")
            if v["cn50_formula_spr_source_group_present"] == "NO":
                self.assertEqual(v["cn50_formula_spr_segment_sha256_UNVERIFIED"], "")

    def test_period_names_not_asserted_official_new_species(self):
        n = [v for v in self.mapping.values()
             if v["period_name_attestation_year_NOT_FIRST_RELEASE"]]
        self.assertEqual(len(n), 7)
        self.assertEqual({v["cn50_original_compiled_name"] for v in n},
                         {"葛雷吉鲁", "葛雷洛比", "葛雷马恩", "葛雷基欧",
                          "艾迪希洛", "蒙奇", "菲奇亚"})
        self.assertEqual({v["period_name_attestation_year_NOT_FIRST_RELEASE"] for v in n},
                         {"2002", "2003"})
        self.assertTrue(all(v["official_live_release"] == "NOT_VERIFIED" for v in n))

    def test_named_egg_is_local_art_candidate_not_confirmed_species(self):
        egg = self.mapping["OBS-CN50-SLOT-0353"]
        self.assertEqual(egg["cn50_original_compiled_name"], "宠物蛋")
        self.assertEqual(egg["early_tw10_relation_OPTIONAL_NOT_ENTRY_GATE"],
                         "EARLY_TW10_NOT_LINKED")
        self.assertEqual(egg["official_live_release"], "NOT_VERIFIED")
        self.assertEqual(self.stats["EARLY_TW10_PORTRAIT_FULL_RD_SHA_EXACT"] +
                         self.stats["EARLY_TW10_NAMED_SPR_PORTRAIT_ABSENT"] +
                         self.stats["EARLY_TW10_NOT_LINKED"], 305)


if __name__ == "__main__":
    unittest.main()
