import unittest

from tools.stoneage_npc_overability_lineage_probe import (
    DYNAMIC,
    STATIC_BLOCKING,
    STATIC_OVERABLE,
    UNRESOLVED,
    default_chain_closed,
    default_player_overable_value,
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

    def test_default_player_overable_decodes_fourth_flag_bit(self):
        default_player = r'''
        static Char player = {
          FALSE,
          {0},
          { {""} },
          { SETFLG(1,1,1,1,1,1,0,0), SETFLG(0,0,0,0,0,0,0,1) }
        };
        '''
        char_base = r'''
        typedef enum {
          CHAR_ISATTACK,
          CHAR_ISATTACKED,
          CHAR_ISOVER,
          CHAR_ISOVERED,
          CHAR_HAVEHEIGHT,
          CHAR_ISVISIBLE,
          CHAR_ISTRANSPARENT,
          CHAR_ISFLYING
        } CHAR_DATAFLG;
        '''
        self.assertEqual(
            default_player_overable_value(
                default_player_source=default_player,
                char_base_source=char_base,
            ),
            1,
        )

    def test_default_chain_requires_player_flags_before_functionset_init(self):
        char_data = r'''
        static defaultCharacterGet CHAR_defaultCharacterGet[] = {
          {1, &player, &lvplayer00, 0},
          {2, &player, &lvplayer00, 0},
        };
        BOOL CHAR_getDefaultChar(Char *nc, int image) {
          int j;
          Char *defaultchar = &player;
          for (j = 0; j < arraysizeof(nc->flg); j++)
            nc->flg[j] = defaultchar->flg[j];
          return TRUE;
        }
        '''
        npcgen = r'''
        static BOOL NPC_generateNPC(int a, int b) {
          Char one;
          CHAR_getDefaultChar(&one, 1);
          NPC_copyFunctionSetToChar(0, &one);
          CHAR_initCharOneArray(&one);
          return TRUE;
        }
        '''
        self.assertTrue(
            default_chain_closed(
                char_data_source=char_data,
                npcgen_source=npcgen,
            )
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
