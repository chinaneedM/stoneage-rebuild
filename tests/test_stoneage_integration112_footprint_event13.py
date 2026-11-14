"""Replay rights-safe original NPC source joins; CI cannot read proprietary ZIP."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'research/recovered'
REPORT = R / 'STONEAGE-INTEGRATION112-FOOTPRINT-NPC-EVENT13-SOURCE-R1.json'
CHAR = R / 'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
QUEST = R / 'STONEAGE-INTEGRATION33-SAINASU-TWO-QUEST-CHAINS-SOURCE-R1.json'
ITEM = R / 'STONEAGE-INTEGRATION69-HEIRLOOM-EVENT13-NPC-ITEM-TW1-PIXEL-SOURCE-R1.json'
MAP = R / 'STONEAGE-TW10-25-FIELDMAP-COMPAT-R1.txt'
NAMES = R / 'STONEAGE-25-STABLE-MAP-NAMES-R1.txt'


class ThiefCaveEvent13Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v = json.loads(REPORT.read_text(encoding='utf-8'))
        cls.char = json.loads(CHAR.read_text(encoding='utf-8'))
        cls.quest = json.loads(QUEST.read_text(encoding='utf-8'))
        cls.item = json.loads(ITEM.read_text(encoding='utf-8'))
        cls.map_lines = MAP.read_text(encoding='utf-8').splitlines()
        cls.name_lines = NAMES.read_text(encoding='utf-8').splitlines()

    def test_precise_base_and_private_source_scope(self):
        b, c = self.v['baseline'], self.v['carrier']
        self.assertEqual(b['main'], 'c64a8a4ca7e70aaf61d0aa02a75a5c436c016e47')
        self.assertEqual(b['tree'], 'fd50c067cc71785832df4ac1126d4efcdc3827db')
        self.assertEqual((b['original_CURRENT_bytes'], b['original_CURRENT_git_blob']),
                         (2709173, 'c89e0e33537990aa2132b47c40fef49a985a935c'))
        self.assertEqual(c['original_NPC_zip_bytes'], 995176)
        self.assertEqual(c['original_NPC_zip_members_crc_pass'], 2205)
        self.assertEqual(c['original_NPC_zip_sha256'],
                         'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertEqual(c['identity'], 'LATER_PRESERVED_COMMUNITY_MIXED25_NPC_FILES')

    def test_five_source_members_exact_match_existing_CHAR01_manifest(self):
        manifest = {row[0]: row for row in self.char['source_files']}
        files = self.v['original_NPC_files']
        self.assertEqual(set(files), {'100/sb_nusu.create', '100/sb_nusu.template',
                                      '100/sb_nusu1.arg', '100/sb_nusu2.arg',
                                      '100/sb_nusu3.arg'})
        for path, info in files.items():
            old = manifest[path]
            self.assertEqual((info['bytes'], info['sha256'], info['crc32']),
                             (old[1], old[2], old[3]), path)
            self.assertEqual(len(info['sha256']), 64)

    def test_three_exact_create_windows_template_and_arg_source_links(self):
        rows = self.v['original_NPC_rows']
        self.assertEqual(len(rows), 3)
        for i, row in enumerate(rows):
            old = next(x for x in self.char['create_rows']
                       if (x[0], x[1]) == (row['create_file'], i))
            template = next(x for x in self.char['template_rows']
                            if (x[0], x[1]) == (row['template_file'], i))
            self.assertEqual([old[2], old[3], old[4]],
                             [*row['create_byte_window'], row['create_block_sha256']])
            self.assertEqual((old[5], old[6], old[8][:2], old[11]),
                             (row['floor'], row['source_bitmap_alias'], row['xy'],
                              row['template_key']))
            self.assertEqual((template[2], template[3], template[4]),
                             (row['template_block_sha256'], row['template_key'], 'NPCEnemy'))
            self.assertEqual(old[15][0][0], row['handler_file'])
            self.assertEqual(old[15][0][2], row['handler_sha256'])
            self.assertEqual(row['handler_sha256'],
                             self.v['original_NPC_files'][row['handler_file']]['sha256'])

    def test_original_numeric_pairs_and_item_semantics_remain_literal(self):
        rows = self.v['original_NPC_rows']
        self.assertEqual([x['floor'] for x in rows], [10701, 10703, 10705])
        self.assertEqual([x['xy'] for x in rows], [[23, 51], [6, 63], [44, 41]])
        self.assertEqual([x['source_bitmap_alias'] for x in rows],
                         [100405, 100436, 100230])
        self.assertEqual([x['handler_literal_fields']['enemyno'] for x in rows],
                         [[513, 516], [514, 518], [515, 519]])
        self.assertEqual([x['handler_literal_fields']['askbattlemsg_count'] for x in rows],
                         [3, 2, 3])
        for x in rows:
            p = x['handler_literal_fields']
            self.assertEqual((p['entype'], p['item'], p['time'], p['dieact']),
                             (2, 2431, 300, 0))
        self.assertTrue(any('not verified item drop' in s
                            for s in self.v['negative_evidence']))

    def test_existing_event13_script_and_original_itemset_are_consistent(self):
        v = self.v['same_preserved_source_event13']
        original = next(x for x in self.quest['original_raw_source_members']
                        if x['path'] == v['original_event13_script'])
        self.assertEqual(original['sha256'], v['original_event13_source_sha256'])
        sections = [x['fields'] for x in self.quest['source_event_sections']
                    if x['path'] == v['original_event13_script']]
        req = next(x for x in sections if x['TYPE'] == 'REQUEST')
        repeat = next(x for x in sections if x['TYPE'] == 'MESSAGE'
                      and x.get('GetItem') == '2431')
        accept = next(x for x in sections if x['TYPE'] == 'ACCEPT')
        for key, source in [('original_REQUEST_condition', req['EVENT']),
                            ('original_REQUEST_GetItem', req['GetItem']),
                            ('original_repeat_MESSAGE_condition', repeat['EVENT']),
                            ('original_repeat_MESSAGE_GetItem', repeat['GetItem']),
                            ('original_ACCEPT_condition', accept['EVENT']),
                            ('original_ACCEPT_DelItem', accept['DelItem']),
                            ('original_ACCEPT_GetItem', accept['GetItem'])]:
            self.assertEqual(v[key], source)
        row = next(x for x in self.item['original_two_table_item_source_rows']
                   if x['item_id'] == 2431)
        self.assertEqual(v['evidence_item_id'], 2431)
        self.assertEqual(v['preserved_itemset_name'], row['original_itemset_source_name'])
        self.assertEqual(v['original_two_itemset_row_sha256'],
                         row['original_two_CP950_original_row_sha256']['itemset.txt'])

    def test_prior_map_dimensions_only_not_new_DAT_or_gameplay(self):
        observations = self.v['existing_qualified_map_data']
        self.assertEqual(len(observations), 3)
        for r, npc in zip(observations, self.v['original_NPC_rows']):
            self.assertEqual(r['floor'], npc['floor'])
            old = next(line for line in self.map_lines
                       if line.startswith(f"COMPATIBLE|path={r['floor']}.DAT|"))
            self.assertIn(f"|sha256={r['original_DAT_sha256']}", old)
            self.assertIn('|width=80|height=80|bytes=38408|', old)
            name = next(line for line in self.name_lines
                        if line.startswith(f"MAP_NAME|floor={r['floor']}|"))
            self.assertIn('name=' + r['name'] + '%7C0|', name)
            self.assertTrue(all(0 <= v < 80 for v in npc['xy']))
        c = self.v['counts']
        self.assertEqual(c['new_original_files_discovered'], 0)
        self.assertEqual(c['new_source_qualified_NPC_item_quest13_numeric_edges'], 3)
        self.assertEqual((c['new_original_DAT_bytes_read'],
                          c['new_original_RD_bytes_read'],
                          c['native_game_or_server_execution']), (0, 0, 0))
        self.assertTrue(any('do not establish official early Taiwan' in s
                            for s in self.v['negative_evidence']))


if __name__ == '__main__':
    unittest.main()
