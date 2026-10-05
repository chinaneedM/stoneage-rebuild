import hashlib
import unittest

from tools.stoneage_recovered25_combined_magic_probe import (
    EXPECTED_MAGIC_IDS,
    analyze_parsed_rows,
    combined_magic_ids,
)


def parsed_rows(ids=EXPECTED_MAGIC_IDS):
    rows=[]
    for offset,magic_id in enumerate(ids):
        function=(
            b"MAGIC_Recovery"
            if offset%2==0
            else b"MAGIC_StatusChange"
        )
        option=f"synthetic-{magic_id}".encode("ascii")
        fields=[
            b"name",b"comment",function,option,
            str(magic_id).encode("ascii"),
            b"1",b"1",b"0",b"",
        ]
        values={
            "ID":magic_id,
            "FIELD":1,
            "TARGET":1,
            "TARGET_DEADFLG":0,
            "IDX":None,
        }
        rows.append((fields,values))
    return rows


class CombinedMagicCrosslinkTests(unittest.TestCase):
    def test_combined_exact_rows_define_expected_magic_set(self):
        self.assertEqual(combined_magic_ids(),EXPECTED_MAGIC_IDS)
        self.assertEqual(len(EXPECTED_MAGIC_IDS),19)

    def test_complete_population_closes_without_exact_second_pass(self):
        result=analyze_parsed_rows(
            parsed_rows(),0,expected_exact_rows=None
        )
        self.assertTrue(result["population_closed"])
        self.assertFalse(result["exact_rows_closed"])
        self.assertEqual(result["missing"],())
        self.assertEqual(len(result["rows"]),19)

    def test_missing_magic_id_stays_open(self):
        result=analyze_parsed_rows(
            parsed_rows(EXPECTED_MAGIC_IDS[:-1]),
            0,
            expected_exact_rows=None,
        )
        self.assertFalse(result["population_closed"])
        self.assertEqual(result["missing"],(306,))

    def test_malformed_table_stays_open(self):
        result=analyze_parsed_rows(
            parsed_rows(),1,expected_exact_rows=None
        )
        self.assertFalse(result["population_closed"])

    def test_duplicate_magic_id_is_rejected(self):
        rows=parsed_rows()
        rows.append(rows[0])
        with self.assertRaisesRegex(ValueError,"duplicate"):
            analyze_parsed_rows(rows,0,expected_exact_rows=None)

    def test_non_magic_function_token_is_rejected(self):
        rows=parsed_rows()
        fields,values=rows[0]
        rows[0]=([*fields[:2],b"OTHER",*fields[3:]],values)
        with self.assertRaisesRegex(ValueError,"MAGIC_ prefix"):
            analyze_parsed_rows(rows,0,expected_exact_rows=None)

    def test_exact_rows_are_independent_second_pass_pin(self):
        loose=analyze_parsed_rows(
            parsed_rows(),0,expected_exact_rows=None
        )
        exact=tuple(
            (
                row["id"],row["function"],row["function_sha256"],
                row["field"],row["target"],row["target_deadflg"],
                row["idx"],row["option_bytes"],row["option_sha256"],
                row["option_contains_nul"],
            )
            for row in loose["rows"]
        )
        pinned=analyze_parsed_rows(
            parsed_rows(),0,expected_exact_rows=exact
        )
        self.assertTrue(pinned["exact_rows_closed"])


if __name__=="__main__":
    unittest.main()
