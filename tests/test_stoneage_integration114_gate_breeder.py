"""Only rights-safe indexed source metadata; no original commercial files in Actions."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'research/recovered'


class GuardBreederSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v=json.loads((R/'STONEAGE-INTEGRATION114-GATE-BREEDER-ORIGINAL-SOURCE-R1.json').read_text(encoding='utf-8'))
        cls.char=json.loads((R/'STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json').read_text(encoding='utf-8'))
        cls.world=(R/'STONEAGE-25-STABLE-WORLD-CONTENT-COVERAGE-R1.txt').read_text(encoding='utf-8').splitlines()
        cls.names=(R/'STONEAGE-25-STABLE-MAP-NAMES-R1.txt').read_text(encoding='utf-8').splitlines()

    def test_exact_remote_and_distinct_historical_sources(self):
        a=self.v['base'];s=self.v['source']
        self.assertEqual(a['main'],'8c864e94a708d96dff817a82814cbd4d9c6dcae2')
        self.assertEqual(a['tree'],'88abad5cf499bb84fef00028bf4086fbf6ddd711')
        self.assertEqual((a['preserved_CURRENT_sha1'],a['preserved_CURRENT_bytes']),
                         ('c89e0e33537990aa2132b47c40fef49a985a935c',2709173))
        self.assertEqual(s['private_zip_bytes'],995176)
        self.assertEqual(s['CRC_passed_member_count'],2205)
        self.assertEqual(s['private_zip_sha256'],
                         'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertIn('LATER_COMMUNITY',s['carrier'])

    def test_nine_exact_files_against_original_CHAR01_source_index(self):
        files=self.v['source']['source_files'];self.assertEqual(len(files),9)
        old={r[0]:r for r in self.char['source_files']}
        for key,record in files.items():
            self.assertIn(key,old)
            self.assertEqual((record['bytes'],record['sha256'],record['crc32']),
                             (old[key][1],old[key][2],old[key][3]))
            self.assertEqual(len(record['sha256']),64)
        self.assertEqual(self.v['counts']['original_files_reread'],9)

    def test_five_create_byte_windows_and_same_source_handler_links(self):
        rows=self.v['original_source_rows'];self.assertEqual(len(rows),5)
        for r in rows:
            match=next(x for x in self.char['create_rows']
                       if (x[0],x[1])==(r['original_source_create'],r['create_block_ordinal']))
            self.assertEqual((match[2:5],match[5],match[6],match[11],match[7] or match[8]),
                             ([*r['original_create_byte_window'],r['original_create_block_sha256']],
                              r['original_floor'],r['original_graphicname'],r['template_token'],
                              [*r['original_xy'],1,1]))
            self.assertIn([r['original_handler_file'],'EXACT_SAME_NPC_SUBTREE_PATH',
                           r['original_handler_sha256']],match[15])
            self.assertIn([r['template_file'],r['create_block_ordinal']],match[13])
            template=next(x for x in self.char['template_rows']
                          if (x[0],x[1])==(r['template_file'],r['create_block_ordinal']))
            self.assertEqual((template[2],template[3],template[4]),
                             (r['original_template_sha256'],r['template_token'],'NPCEnemy'))

    def test_actual_source_numeric_groupings(self):
        rows=self.v['original_source_rows']
        self.assertEqual([r['original_floor'] for r in rows],[10007,10007,10007,10919,20711])
        self.assertEqual([r['original_xy'] for r in rows],
                         [[29,39],[28,39],[30,39],[4,7],[19,4]])
        m=self.v['material_findings']
        self.assertEqual(m['three_brothers_same_original_enemy_number_sequence'],[294,295,296,297,298])
        self.assertEqual(m['three_brothers_same_literal_warp_destination'],[10007,29,37])
        self.assertEqual(m['two_examiner_different_original_enemy_sequences'],[[941,942],[943,944]])
        self.assertEqual(m['sbc_literal_destination'],[10920,55,28])
        self.assertEqual(m['jba_literal_destination'],[20711,23,4])
        for r in rows[:3]:
            a=r['original_arg_literals']
            self.assertEqual(a['enemyno'],m['three_brothers_same_original_enemy_number_sequence'])
            self.assertEqual([a['warpfl'],a['warpx'],a['warpy']],m['three_brothers_same_literal_warp_destination'])
            self.assertIsNone(a['onebattle'])
        for r in rows[3:]:self.assertEqual(r['original_arg_literals']['onebattle'],1)

    def test_jba_original_graphic_and_template_mismatch_is_not_normalized(self):
        r=self.v['original_source_rows'][-1]
        self.assertEqual((r['original_graphicname'],r['original_template_type']),(100437,100436))
        self.assertEqual(self.v['original_source_rows'][3]['original_graphicname'],
                         self.v['original_source_rows'][3]['original_template_type'])
        self.assertEqual(self.v['material_findings']['jba_graphicname_vs_template_type_differ'],
                         {'original_create_graphicname':100437,'original_template_type':100436})
        self.assertTrue(any('never silently normalize' in s for s in self.v['negative_evidence']))

    def test_prior_maps_bounds_are_not_native_gameplay_or_new_DAT(self):
        maps=self.v['prior_map_geometries'];self.assertEqual(len(maps),4)
        for m in maps:
            line=next(x for x in self.world if x.startswith('FLOOR|id='+str(m['floor'])+'|'))
            self.assertIn('width='+str(m['width'])+'|height='+str(m['height']),line)
            self.assertIn('map_sha256='+m['source_DAT_sha256'],line)
            self.assertTrue(any(n.startswith('MAP_NAME|floor='+str(m['floor'])+'|')
                                for n in self.names))
        by={x['floor']:x for x in maps}
        for r in self.v['original_source_rows']:
            src=by[r['original_floor']];dest=by[r['original_arg_literals']['warpfl']]
            self.assertTrue(0<=r['original_xy'][0]<src['width'])
            self.assertTrue(0<=r['original_xy'][1]<src['height'])
            self.assertTrue(0<=r['original_arg_literals']['warpx']<dest['width'])
            self.assertTrue(0<=r['original_arg_literals']['warpy']<dest['height'])
        c=self.v['counts']
        self.assertEqual((c['source_qualified_static_NPC_to_warp_destination_edges'],
                          c['new_original_DAT_bytes_read'],c['new_original_RD_bytes_read'],
                          c['native_original_game_or_server_sessions']),(5,0,0,0))


if __name__=='__main__':
    unittest.main()
