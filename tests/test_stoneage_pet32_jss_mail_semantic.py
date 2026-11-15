import json
import unittest
from pathlib import Path

from tools import stoneage_pet32_jss_mail_semantic as pet32


class Pet32SourceSemanticContract(unittest.TestCase):
    def test_exact_clause_identity_and_negative_barrier(self):
        data = json.loads(Path("research/recovered/STONEAGE-PET32-JSS1999-BATTLE-MAIL-SEMANTIC-R1.json").read_text())
        pet31 = json.loads(pet32.PARENT.read_text())
        self.assertEqual(data["source"]["sha256"], pet32.SHA)
        self.assertEqual(len(data["source_bounded_semantic_records"]), 2)
        self.assertEqual([r["operator_date"] for r in data["source_bounded_semantic_records"]],
                         ["1999-11-22", "1999-11-26"])
        for r in data["source_bounded_semantic_records"]:
            p = next(x for x in pet31["dated_rows_1999"]
                     if x["original_source_order"] == r["original_source_order"])
            c = p["clauses"][r["clause_order_in_entry"]]
            self.assertEqual(r["normalized_sha256"], c["normalized_sha256"])
            self.assertEqual(r["normalized_characters"], c["normalized_characters"])
            self.assertFalse(r["actual_game_execution_proven"])
        self.assertEqual(data["source_bounded_semantic_records"][0]["pet_mail_during_battle"],
                         "EXPLICITLY_UNAVAILABLE_AS_OF_THIS_WRITTEN_CHANGE")
        self.assertEqual(data["source_bounded_semantic_records"][1]["pet_mail_during_battle"],
                         "BUG_FIX_RECORDED_WITH_UNSPECIFIED_SYMPTOM_AND_POLICY")
        self.assertTrue(all(data["inference_barriers"].values()))
        self.assertEqual(data["new_official_named_pet_species"], [])
        self.assertEqual(data["year_1999"], "NOT_YEAR_AUDITED")

    def test_finite_source_semantics_and_negative_guards(self):
        pet32.semantically_validate("1999-11-22",
            "戦闘中でもメールが使えるようになりました。 ショートカット、ウィンドウバー、ただし、ペットメールは使用できません。")
        pet32.semantically_validate("1999-11-26",
            "戦闘中のペットメールに関する不具合を修正しました。")
        with self.assertRaises(ValueError):
            pet32.semantically_validate("1999-11-22",
                "戦闘中でもメールが使えるようになりました。 ショートカット、ウィンドウバー、ペットメールは使用できます。")
        with self.assertRaises(ValueError):
            pet32.semantically_validate("1999-11-26", "ペットメールが使用可能になりました。")
        with self.assertRaises(ValueError):
            pet32.build(b"not-the-authentic-source", pet32.URL)


if __name__ == "__main__":
    unittest.main()
