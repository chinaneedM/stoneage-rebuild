import unittest

from tools.stoneage_npc_overability_lineage_probe import (
    DYNAMIC,
    STATIC_BLOCKING,
    STATIC_OVERABLE,
    UNRESOLVED,
    _function_body,
    classify_init_and_file,
    overability_setter_values,
    parse_functionset_init_map,
)


class NpcOverabilityLineageProbeTests(unittest.TestCase):

    def test_functionset_table_extracts_initfunc(self):
        text = r'''
        static FunctionNameSet functionSet[] = {
          { "Warp", "WarpInit", "", "" },
          { "TownPeople", "TownPeopleInit", "", "" },
        };
        '''
        self.assertEqual(
            parse_functionset_init_map(text),
            {"Warp": "WarpInit", "TownPeople": "TownPeopleInit"},
        )

    def test_comments_do_not_count_as_setters(self):
        text = r'''
        BOOL TownPeopleInit(int meindex) {
          // CHAR_setFlg(meindex, CHAR_ISOVERED, 1);
          /* CHAR_setFlg(meindex, CHAR_ISOVERED, 0); */
          return TRUE;
        }
        '''
        body = _function_body(text, "TownPeopleInit")
        self.assertEqual(overability_setter_values(body), ())

    def test_static_blocking_and_overable_classification(self):
        self.assertEqual(
            classify_init_and_file(init_values=(0,), file_values=(0,)),
            STATIC_BLOCKING,
        )
        self.assertEqual(
            classify_init_and_file(init_values=(1,), file_values=(1,)),
            STATIC_OVERABLE,
        )

    def test_same_file_zero_and_one_is_dynamic(self):
        self.assertEqual(
            classify_init_and_file(init_values=(0,), file_values=(0, 1)),
            DYNAMIC,
        )

    def test_missing_init_setter_is_unresolved(self):
        self.assertEqual(
            classify_init_and_file(init_values=(), file_values=(0,)),
            UNRESOLVED,
        )

    def test_function_body_balances_nested_braces(self):
        text = r'''
        BOOL DoorInit(int meindex) {
          if (meindex >= 0) {
            CHAR_setFlg(meindex, CHAR_ISOVERED, 0);
          }
          return TRUE;
        }
        BOOL OtherInit(int x) {
          CHAR_setFlg(x, CHAR_ISOVERED, 1);
          return TRUE;
        }
        '''
        body = _function_body(text, "DoorInit")
        self.assertEqual(overability_setter_values(body), (0,))
        self.assertNotIn("OtherInit", body)


if __name__ == "__main__":
    unittest.main()
