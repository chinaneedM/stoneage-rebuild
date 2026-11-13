"""INTEGRATION100 derived-only checks, safe for a public Git checkout without proprietary NPC originals."""
import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
MAP = ROOT / 'research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'
REPORT = ROOT / 'research/recovered/STONEAGE-INTEGRATION100-AIRWAY-15-ORIGINAL-NPC-SOURCE-R1.json'


def git_sha(path):
    b = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\x00' + b).hexdigest()

class TestAirwaySourceIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REPORT.read_text(encoding='utf8'))
        cls.old = json.loads(INDEX.read_text(encoding='utf8'))
        cls.maps = json.loads(MAP.read_text(encoding='utf8'))
        cls.rows = [r for r in cls.old['create_rows'] if r[0]=='genout/airway.create']
        cls.handlers = {r[0]:r for r in cls.old['source_files']}
        cls.floors = {int(r[0][:-4]):r for r in cls.maps['per_floor_source_rows']}
        cls.out = cls.data['original_CREATE_source_rows_sha_anchored']

    def test_prior_full_public_git_blobs_not_staging_bytes(self):
        self.assertEqual(git_sha(INDEX), 'a088b61a3212f7049e7793f587123ffb29bebad7')
        self.assertEqual(git_sha(MAP), '1ef8c004179128ea44ffa4fb4259748bc8c83911')

    def test_15_original_create_rows_and_original_sha_links(self):
        self.assertEqual(len(self.rows), 15)
        self.assertEqual(len(self.out),15)
        for row,observed in zip(self.rows,self.out):
            with self.subTest(ordinal=row[1]):
                self.assertEqual(row[1],observed['ordinal'])
                self.assertEqual([row[2],row[3]],observed['create_source_byte_halfopen'])
                self.assertEqual(row[4],observed['create_block_sha256'])
                self.assertEqual(row[5],observed['floorid'])
                self.assertEqual(row[6],observed['original_graphic_numeric_alias'])
                self.assertEqual(row[7][:2],observed['spawn_xy'])
                self.assertEqual(row[10],observed['original_direction'])
                self.assertEqual(row[11],observed['original_enemy_template'])
                self.assertEqual(row[14],observed['original_name_field_sha256'])
                self.assertEqual(len(row[15]),1)
                self.assertEqual('npc/'+row[15][0][0],observed['original_handler_file'])
                self.assertEqual(row[15][0][1],'EXACT_SAME_NPC_SUBTREE_PATH')
                self.assertEqual(row[15][0][2],observed['handler_full_sha256'])
                self.assertEqual(self.handlers[row[15][0][0]][1],observed['handler_original_bytes'])
                self.assertEqual(self.handlers[row[15][0][0]][2],observed['handler_full_sha256'])

    def test_physical_source_identity_and_no_proprietary_payload(self):
        source = self.handlers['genout/airway.create']
        self.assertEqual(source[1],2747)
        self.assertEqual(source[2],'faaf7850d8cc400764b6f4b700dafced16664a988069e15b3ba18315d52ded9e')
        self.assertEqual(self.data['private_source_custody']['actual_private_npc_ZIP_sha256'],'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertEqual(self.data['private_source_custody']['actual_private_npc_ZIP_crc_validated'],2205)
        self.assertEqual(self.data['private_source_custody']['original_CREATE_block_byte_window_SHA_verifications'],15)

    def test_original_npc_and_sign_categories_and_dedup(self):
        self.assertEqual(Counter(x['original_enemy_template'] for x in self.out),{'npcgen_man':5,'npcgen_signboard':10})
        self.assertEqual(len({x['original_handler_file'] for x in self.out}),15)
        self.assertEqual(len({x['handler_full_sha256'] for x in self.out}),12)
        self.assertEqual(Counter(x['text_source_class'] for x in self.out),{'guide':5,'destination_sign':8,'airdrop_sign':2})
        self.assertEqual(sum(x['sign_source_literal_amount_string']=='1000s' for x in self.out),8)
        self.assertEqual(sum(x['text_source_class']=='airdrop_sign' and x['sign_source_literal_amount_string'] is None for x in self.out),2)

    def test_six_distinct_floor_ids_and_bounded_prior_dat(self):
        self.assertEqual(sorted({x['floorid'] for x in self.out}),[2000,4000,5000,5100,5543,6000])
        self.assertEqual([x for x in [5000,6000] if x in self.floors],[])
        for x in self.out:
            source = self.floors.get(x['floorid'])
            if source:
                previous=x['prior_original_DAT']
                self.assertIsNotNone(previous)
                self.assertEqual(previous['git_prior_full_DAT_sha256'],source[2])
                self.assertEqual((previous['width'],previous['height']),(source[3],source[4]))
                self.assertTrue(0 <= x['spawn_xy'][0] < source[3])
                self.assertTrue(0 <= x['spawn_xy'][1] < source[4])
                self.assertIs(previous['in_header_bounds'],True)
            else:self.assertIsNone(x['prior_original_DAT'])
        self.assertEqual(sum(x['prior_original_DAT'] is not None for x in self.out),8)
        self.assertEqual(sum(x['prior_original_DAT'] is None for x in self.out),7)

    def test_negative_operational_limits_and_unchanged_current(self):
        l=self.data['limits']
        self.assertIs(l['name_and_sign_text_may_describe_route_not_actual_flight_or_teleport'],True)
        for key in ('signboard_literal_1000s_is_actual_charged_fee','prior_DAT_header_in_bounds_is_native_passability','original_TW1_JSS1999_or_CN182_same_deployment_proven','original_raw_private_dialogue_or_original_proprietary_art_in_public_Git','original_client_or_server_execution_this_unit','new_Retail_TW1_RD_decoding_or_observer_this_unit','source_only_active_live_NPC_spawns_proven'):
            self.assertIs(l[key],False)
        self.assertEqual(self.data['historical_preservation']['CURRENT_blob_sha'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual(self.data['historical_preservation']['Stage_A'],'7 PARTIAL + 2 OPEN')
        self.assertIsNone(self.data['historical_preservation']['overall_percent'])

if __name__ == '__main__':
    unittest.main()
