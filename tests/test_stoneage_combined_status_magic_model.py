import unittest

from tools.stoneage_combined_status_magic_model import (
    CombinedStatusMagicDomain, parse_status_magic_option as parse,
    expected_actual_outcomes, validate_actual_outcomes,
)


class StatusMagicParserTests(unittest.TestCase):
    def test_pinned_actual_matrix_has_six_safe_casts_twelve_safe_failures_twentyfour_unsafe_cells(self):
        rows=expected_actual_outcomes()
        self.assertEqual(len(rows),42)
        self.assertEqual(sum(row[5] is True for row in rows),6)
        self.assertEqual(sum(row[5] is False for row in rows),12)
        self.assertEqual(sum(row[4]=="unsafe" for row in rows),24)
        validate_actual_outcomes(rows)

    def test_actual_matrix_detects_duration_success_status_and_profile_drift(self):
        rows=list(expected_actual_outcomes())
        index=next(i for i,row in enumerate(rows) if row[0:3]==("iris","cp950",139))
        for column,value in ((6,4),(7,3),(8,100),(1,"gbk")):
            altered=rows.copy();row=list(altered[index]);row[column]=value;altered[index]=tuple(row)
            with self.assertRaisesRegex(CombinedStatusMagicDomain,"matrix_drift"):
                validate_actual_outcomes(altered)

    def test_actual_matrix_detects_missing_duplicate_or_diagnostic_classification(self):
        rows=list(expected_actual_outcomes())
        for altered in (rows[:-1],rows+[rows[0]],rows[:-1]+[rows[0]]):
            with self.assertRaises(CombinedStatusMagicDomain):
                validate_actual_outcomes(altered)
        row=list(rows[0]);row[4]="unsafe";rows[0]=tuple(row)
        with self.assertRaises(CombinedStatusMagicDomain):
            validate_actual_outcomes(rows)

    def parse(self,raw,kind="change",profile="iris",charset="cp950"):
        return parse(raw,kind=kind,profile=profile,execution_charset=charset)

    def test_recovery_zero_and_base_status(self):
        for label,status in (("全",0),("毒",1),("亂",6),("默",10)):
            self.assertEqual(self.parse(label.encode("cp950"),"recovery").status,status)

    def test_change_reads_explicit_turn_success(self):
        raw="毒 turn=5 Θ=75".encode("cp950")
        out=self.parse(raw)
        self.assertEqual((out.status,out.turn,out.success),(1,5,75))

    def test_change_no_turn_is_unsafe_instead_of_default_duration(self):
        for raw in ("毒 成=75".encode("cp950"),"毒 turn".encode("cp950")):
            with self.assertRaises(CombinedStatusMagicDomain):
                self.parse(raw)

    def test_implicit_loop_increment_skips_first_ascii_after_two_byte_label(self):
        # +2 in body and +1 in for-loop swallow the 't' of 'turn'.
        with self.assertRaisesRegex(CombinedStatusMagicDomain,"missing_turn"):
            self.parse("毒turn=5 Θ=75".encode("cp950"))
        out=self.parse("毒 turn=5 Θ=75".encode("cp950"))
        self.assertEqual(out.turn,5)

    def test_success_search_begins_after_turn_marker(self):
        out=self.parse("毒 Θ=99 turn=4".encode("cp950"))
        self.assertEqual((out.turn,out.success),(4,15))

    def test_missing_numeric_field_keeps_default_and_separator_skips_one_byte(self):
        out=self.parse("毒 turn=q Θ=q".encode("cp950"))
        self.assertEqual((out.turn,out.success),(3,15))
        out=self.parse("毒 turn12 Θ34".encode("cp950"))
        self.assertEqual((out.turn,out.success),(2,4))

    def test_profile_success_markers_are_preserved(self):
        for profile,label,marker,charset in (
            ("gavin","毒","成","gbk"),("iris","毒","Θ","cp950"),
            ("bismarck","中毒","成功","gbk"),
        ):
            out=self.parse((label+" turn=7 "+marker+"=45").encode(charset),profile=profile,charset=charset)
            self.assertEqual((out.status,out.turn,out.success),(1,7,45))

    def test_utf8_prefix_collision_retains_source_status_identity(self):
        out=self.parse("眼 turn=4 Θ=70".encode(),charset="utf-8")
        self.assertEqual(out.status,3)

    def test_empty_source_returns_false_but_null_dereferences(self):
        for kind in ("change","recovery"):
            self.assertFalse(self.parse(b"",kind).accepted)
            with self.assertRaisesRegex(CombinedStatusMagicDomain,"null_option"):
                self.parse(None,kind)

    def test_short_table_nonmatch_rejects_while_full_table_safely_scans(self):
        with self.assertRaisesRegex(CombinedStatusMagicDomain,"short_status_table"):
            self.parse(b"x","recovery")
        self.assertFalse(self.parse(b"x","recovery","bismarck","utf-8").accepted)
        self.assertEqual(self.parse("x沉默".encode(),"recovery","bismarck","utf-8").status,10)

    def test_change_excludes_wildcard_and_integer_overflow(self):
        with self.assertRaises(CombinedStatusMagicDomain):
            self.parse("全 turn=3 Θ=15".encode("cp950"))
        with self.assertRaisesRegex(CombinedStatusMagicDomain,"integer_overflow"):
            self.parse("毒 turn=2147483648 Θ=15".encode("cp950"))

    def test_profile_charset_and_embedded_nul_reject(self):
        for raw,profile,charset in ((b"","iris","latin1"),(b"","bismarck","cp950"),
                                    (b"a\0b","iris","cp950")):
            with self.assertRaises(CombinedStatusMagicDomain):
                self.parse(raw,profile=profile,charset=charset)


if __name__=="__main__":
    unittest.main()
