"""Replay rights-safe source metadata, never require original proprietary images in CI."""
import collections
import csv
import gzip
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-INTEGRATION111-MINING-TWO-TEAMS-TW10-22-ORIGINAL-BITMAP-CANDIDATES-R1.json'
CHAR=ROOT/'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
QUEST=ROOT/'research/recovered/STONEAGE-QUEST12-MINING-COMPETITION-ORIGINAL-SOURCE-R1.json'
PET15=ROOT/'research/recovered/STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json'
ADRN=ROOT/'research/recovered/tw10-resource-metadata/ADRN-R1.tsv.gz'

class MiningTwoTeamOriginal2D(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v=json.loads(REPORT.read_text(encoding='utf-8'))
        cls.char=json.loads(CHAR.read_text(encoding='utf-8'))
        cls.quest=json.loads(QUEST.read_text(encoding='utf-8'))
        cls.pet=json.loads(PET15.read_text(encoding='utf-8'))
        cls.source={x[0]:x for x in cls.char['source_files']}
        cls.blocks={(x[0],x[1]):x for x in cls.char['create_rows']}

    def test_accepted_TW1_and_separate_mixed25_provenance(self):
        p=self.v['source_qualifications'];base=self.v['baseline']
        self.assertEqual(base['main'],'a64e9f5c4079fe891b34e4c79c43d7b44a081d43')
        self.assertEqual(base['tree'],'412781cab452df38539176c45059369211bd0b4c')
        self.assertEqual(base['original_CURRENT_git_blob'],'c89e0e33537990aa2132b47c40fef49a985a935c')
        self.assertEqual(base['original_CURRENT_bytes'],2709173)
        self.assertEqual(p['private_TW1_zip_bytes'],372626292)
        self.assertEqual(p['private_TW1_zip_sha256'],'3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24')
        self.assertEqual(p['original_TW1_member_crc'],379)
        self.assertEqual(p['private_mixed25_NPC_zip_sha256'],self.quest['source_archive_sha256'])
        self.assertEqual(p['original_NPC_member_crc'],2205)
        self.assertEqual(p['prior_CHAR01_git_blob'],self.quest['prior_manifest_git_blob_sha1'])
        self.assertEqual(p['prior_QUEST12_git_blob'],'95631cbaeea40260bfc14f7c37039950b495e000')

    def test_all_27_original_source_files_match_prior_full_npc_manifest(self):
        files=self.v['original_source_files']
        self.assertEqual(len(files),27)
        self.assertEqual(self.v['counts']['mixed25_original_handler_files_read'],24)
        for path,fields in files.items():
            x=self.source[path]
            self.assertEqual((fields['bytes'],fields['sha256'],fields['crc32']),(x[1],x[2],x[3]))
            self.assertTrue(re.fullmatch(r'[0-9a-f]{64}',fields['sha256']))
        for x in self.quest['source_files']:
            if x['path'] in files:
                self.assertEqual((x['bytes'],x['sha256'],x['crc32']),
                                 (files[x['path']]['bytes'],files[x['path']]['sha256'],files[x['path']]['crc32']))

    def test_24_exact_original_CREATE_byte_spans_names_and_refs(self):
        rows=self.v['original_create_rows'];self.assertEqual(len(rows),24)
        by_path=collections.Counter(x['source_file'] for x in rows)
        self.assertEqual(by_path,{'genout/giruev2.create':21,'giiru/event/giruev2.create':2,'300/sb_bac.create':1})
        for r in rows:
            prior=self.blocks[(r['source_file'],r['source_block_ordinal'])]
            self.assertEqual(prior[2:5],[*r['original_create_byte_window'],r['original_create_block_sha256']])
            self.assertEqual(prior[5],r['floor'])
            self.assertEqual(prior[6],r['source_graphicname'])
            self.assertEqual(prior[11],r['source_function'])
            self.assertEqual((prior[7] or prior[8])[:2],r['xy'])
            self.assertTrue(0<=r['xy'][0]<50 and 0<=r['xy'][1]<50)
            self.assertEqual(len(r['original_spawn_parameters']),4)
            if r['source_handler_ref']:
                self.assertIn([r['source_handler_ref'],'EXACT_SAME_NPC_SUBTREE_PATH',r['handler_sha256']],prior[15])
                self.assertEqual(self.v['original_source_files'][r['source_handler_ref']]['sha256'],r['handler_sha256'])
            self.assertTrue(re.fullmatch('[0-9a-f]{64}',r['original_create_block_sha256']))
        self.assertEqual([r['source_function'] for r in rows].count('changeevent'),2)
        self.assertEqual([r['source_function'] for r in rows].count('npcgen_man'),20)
        self.assertEqual([r['source_function'] for r in rows].count('npcgen_warpman'),1)

    def test_prior_QUEST12_two_principals_miner_and_21_background_roles(self):
        rows=self.v['original_create_rows']
        groups=[(self.quest['principal_creates'],'giiru/event/giruev2.create'),
                (self.quest['generated_support_creates'],'genout/giruev2.create'),
                (self.quest['miner_create'],'300/sb_bac.create')]
        for prior,path in groups:
            for item in prior:
                got=next(x for x in rows if x['source_file']==path and x['source_block_ordinal']==item['ordinal'])
                self.assertEqual(got['original_create_block_sha256'],item['block_sha256'])
                self.assertEqual(got['source_graphicname'],item['graphic_alias'])
                self.assertEqual(got['original_create_byte_window'],[item['start_byte'],item['end_byte']])
        self.assertEqual(collections.Counter(x['source_short_name'] for x in rows),
                         {'帖尼姆團團員':10,'巴巴洛組組員':10,'入場管理人':1,
                          '帖尼姆':1,'巴巴洛':1,'礦工巴卡斯':1})
        self.assertEqual(len({tuple(r['xy']) for r in rows}),24)
        self.assertEqual(self.quest['map_source_observations'][0]['geometry'],[50,50])
        self.assertEqual(self.quest['map_source_observations'][0]['floor'],31805)

    def test_22_ACTUAL_TW1_ADRN_RD_hashed_original_blocks_against_prior_index(self):
        originals=self.v['original_TW1_actual_RD_pixel_candidates']
        self.assertEqual(len(originals),22)
        wanted={x['source_bitmap_number']:x for x in originals}
        self.assertEqual(len(wanted),22)
        self.assertEqual(set(wanted),{r['source_graphicname'] for r in self.v['original_create_rows']}-{100401})
        found={}
        with gzip.open(ADRN,'rt',encoding='ascii',newline='') as raw:
            for row in csv.DictReader(raw,delimiter='\t'):
                key=int(row['bitmapno'])
                if key in wanted:
                    self.assertNotIn(key,found)
                    found[key]=row
        self.assertEqual(set(found),set(wanted))
        for key,r in wanted.items():
            t=found[key]
            self.assertEqual((r['original_adrn_index'],r['original_real_offset'],r['original_RD_block_bytes'],
                              r['width'],r['height'],r['original_RD_flag']),
                             tuple(int(t[field]) for field in ['index','adder','size','width','height','rd_flag']))
            self.assertEqual(r['original_RD_sha256'],t['rd_block_sha256'])
            self.assertEqual(r['original_adrn_index'],key)
            self.assertTrue(0<r['width']<=1024 and 0<r['height']<=1024)
            for field in ['original_adrn_record_sha256','original_source_index_pixels_sha256',
                          'private_Palet_1_candidate_png_sha256']:
                self.assertRegex(r[field],r'^[0-9a-f]{64}$')
        self.assertEqual(sum(r['original_RD_block_bytes'] for r in originals),39941)
        self.assertEqual(self.v['counts']['TW1_independent_decoders_matching_blocks'],22)

    def test_miner_is_existing_pet15_SPR_not_new_static_bitmap(self):
        m=self.v['prior_pet15_existing_miner']
        self.assertEqual(m['source_graphicname'],100401)
        self.assertEqual(m['source_xy'],[26,23])
        self.assertFalse(m['newly_decoded_in_this_unit'])
        group=next(x for x in self.pet['groups'] if x['graphic']==100401)
        self.assertEqual(group['source_sequences'],104)
        self.assertTrue(group['prior_pet07'])
        self.assertNotIn(100401,[r['source_bitmap_number'] for r in self.v['original_TW1_actual_RD_pixel_candidates']])

    def test_private_custody_and_non_public_pixels(self):
        c=self.v['private_observation'];self.assertEqual(c['zip_bytes'],212169)
        self.assertEqual(c['zip_members'],25)
        self.assertEqual(c['zip_sha256'],'efda438c7a57c83bbcc800d0ea0b1ca145d64ea6e7c87d5e0f697aebc330804a')
        self.assertRegex(c['contact_preview_png_sha256'],'^[0-9a-f]{64}$')
        self.assertEqual(self.v['counts']['private_Palet1_png_files_generated'],22)
        self.assertFalse(any(self.v['limitations'][k] for k in self.v['limitations'] if k!='overall_percent'))
        self.assertIsNone(self.v['limitations']['overall_percent'])
        self.assertEqual(self.v['stage']['A'],'7 PARTIAL + 2 OPEN')

    def test_deliberate_source_mutation_and_crossversion_promotion_rejected(self):
        original=self.v['original_create_rows'][0]
        key=(original['source_file'],original['source_block_ordinal'])
        self.assertNotEqual('0'*64,self.blocks[key][4])
        self.assertNotEqual(original['original_create_byte_window'][0]+1,self.blocks[key][2])
        source_bitmap=self.v['original_TW1_actual_RD_pixel_candidates'][0]
        self.assertNotEqual('f'*64,source_bitmap['original_RD_sha256'])
        self.assertFalse(self.v['limitations']['same_historical_deployment_TW1_later_mixed25_proven'])
        self.assertFalse(self.v['limitations']['original_palette_selected_at_runtime_proven'])

if __name__=='__main__':unittest.main()
