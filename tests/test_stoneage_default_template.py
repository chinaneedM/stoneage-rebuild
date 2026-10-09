import json
import unittest
from tools.stoneage_default_template_audit import (
    PIN_PATH, PINNED, enums, expected_data, expression, top_entries, vectors,
)


class DefaultTemplateTests(unittest.TestCase):
    def setUp(self):
        self.rows=json.loads(PIN_PATH.read_text())['profiles']

    def test_integer_parser_evaluates_packed_initializer_and_rejects_calls(self):
        self.assertEqual(expression('((((100)<<16)&0xffff0000)|((20)&0x0000ffff))',{}),6553620)
        with self.assertRaises(ValueError):expression('call(1)',{})

    def test_enum_parser_honors_explicit_values_and_separate_enums(self):
        self.assertEqual(enums('typedef enum { A, B=4, C, } One; typedef enum { D=B+3, E } Two;'),
                         {'A':0,'B':4,'C':5,'D':7,'E':8})

    def test_initializer_parser_preserves_nested_groups_and_expression_commas(self):
        self.assertEqual(top_entries('{0,{1,2},{{""},{""}},{63,128}}'),
                         ['0','{1,2}','{{""},{""}}','{63,128}'])

    def test_all_table_members_and_unmatched_extremes_have_four_dirty_fills(self):
        for row in self.rows.values():
            cases=vectors(row['table_rows'])
            self.assertEqual(len(cases),228)
            self.assertEqual(len(set(cases)),228)
            for image in [*(v[0] for v in row['table_rows']),31010,-1,0,2147483647]:
                self.assertEqual({f for i,f in cases if i==image},{0,90,165,255})

    def test_profile_ordinals_are_not_collapsed_into_symbolic_witness_layout(self):
        self.assertEqual({p:r['enum_values']['CHAR_DATAINTNUM'] for p,r in self.rows.items()},
                         {'gavin':162,'iris':159,'bismarck':131})
        self.assertEqual({p:r['enum_values']['CHAR_WORKTICKETTIME'] for p,r in self.rows.items()},
                         {'gavin':314,'iris':313,'bismarck':199})
        self.assertNotIn('CHAR_WORKCHATROOMNUM',self.rows['bismarck']['enum_values'])

    def test_tail_initializer_is_excluded_by_original_copy_boundary(self):
        for row in self.rows.values():
            ev=row['enum_values'];data=[17]*ev['CHAR_DATAINTNUM']
            data[ev['CHAR_BECOMEPIG']]=-1;data[ev['CHAR_BECOMEPIG_BBI']]=100250
            result=expected_data(row,data)
            self.assertEqual(result[:ev['CHAR_INITDATA']],[17]*ev['CHAR_INITDATA'])
            self.assertTrue(all(v==0 for v in result[ev['CHAR_INITDATA']:]))
            self.assertEqual((result[ev['CHAR_BECOMEPIG']],result[ev['CHAR_BECOMEPIG_BBI']]),(0,0))

    def test_receipts_preserve_positional_diagnostics_and_bismarck_shift(self):
        self.assertEqual({p:r['excess_initializer_ints'] for p,r in self.rows.items()},
                         {'gavin':8,'iris':10,'bismarck':0})
        self.assertEqual((self.rows['bismarck']['template_pig_value'],self.rows['bismarck']['template_pig_image']),
                         (100250,0))

    def test_source_identity_includes_real_template_headers_animation_and_version(self):
        self.assertEqual(set(self.rows),set(PINNED))
        for p,row in self.rows.items():
            self.assertEqual(row['source_sha'],PINNED[p])
            for suffix in ('defaultPlayer.h','char_base.h','anim_tbl.h','version.h','char_data.c'):
                self.assertTrue(any(path.endswith(suffix) for path in row['files']))
            self.assertTrue(row['all_rows_share_player'])
            self.assertTrue(row['actual_headers_table_and_defaultPlayer'])
            self.assertTrue(row['original_build_and_ABI_not_claimed'])


if __name__=='__main__':unittest.main()
