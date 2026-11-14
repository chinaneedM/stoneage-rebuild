"""Recheck immutable public original-source indexes against 40 original NPC/30 TW1 RD candidate receipts.

No proprietary original data in public CI. This tests the derived/public evidence boundary,
not the native original game or the private observer browser session.
"""
import collections
import json
import pathlib
import re
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-INTEGRATION106-SHOP-M3-40-SOURCE-TW1-ORIGINAL-2D-R1.json'
NPC = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
DAT = ROOT / 'research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'
ITEMS = ROOT / 'research/recovered/STONEAGE-ITEM-EQUIPMENT-SHOP-MODULE-01-224-SOURCE-ITEMLISTS-191-CREATE-REFERENCES-R1.json'
PET07 = ROOT / 'research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


class SourceBoundOriginalShopM3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc, cls.npc, cls.map, cls.items, cls.pet07 = map(load, [REPORT, NPC, DAT, ITEMS, PET07])
        cls.rows = cls.doc['original_CREATE_numeric_rows_with_SHA']
        cls.pixels = cls.doc['TW1_original_pixel_candidate_rows']

    def test_01_exact_prior_public_blob_anchors_and_unchanged_history(self):
        d = self.doc
        pinned = d['custody']['source_prior_public_index_blobs']
        for path, key in ((NPC,'CHAR01'),(DAT,'MAP04'),(ITEMS,'ITEM01_shop_creation_catalog'),(PET07,'PET07_tw1_spr_source')):
            actual = subprocess.check_output(['git','hash-object',str(path)],text=True).strip()
            self.assertEqual(actual,pinned[key])
        self.assertEqual(subprocess.check_output(['git','hash-object',str(ROOT/'docs/CURRENT-STATE.md')],text=True).strip(),d['baseline']['original_current_state_blob'])
        self.assertEqual((ROOT/'docs/CURRENT-STATE.md').stat().st_size,2709173)

    def test_02_create_40_actual_spans_replay_exact_old_full_index(self):
        old = sorted((r for r in self.npc['create_rows'] if r[0]=='genout/shop_m3.create'),key=lambda r:r[1])
        self.assertEqual(len(old),40)
        self.assertEqual(len(self.rows),40)
        for o,n in zip(old,self.rows):
            self.assertEqual(n['ordinal'],o[1]);self.assertEqual(n['source_span'],o[2:4])
            self.assertEqual(n['source_span_sha256'],o[4]);self.assertEqual(n['floor'],o[5])
            self.assertEqual(n['xy'],o[7][:2]);self.assertEqual(o[7][:2],o[7][2:])
            self.assertEqual(n['graphic'],o[6]);self.assertEqual(n['kind'],o[11])
            if o[15]:
                self.assertEqual(n['handler'].removeprefix('npc/'),o[15][0][0])
                self.assertEqual(n['handler_sha256'],o[15][0][2])
            else:
                self.assertIsNone(n['handler'])
                self.assertIsNone(n['handler_sha256'])

    def test_03_handler_files_exist_and_are_SHA_pinned(self):
        manifest={r[0]:r for r in self.npc['source_files']}
        self.assertEqual(len(self.doc['original_handler_sha256']),28)
        for r in self.rows:
            if r['handler'] is None:
                self.assertIsNone(r['handler_sha256'])
                continue
            key=r['handler'].removeprefix('npc/')
            self.assertIn(key,manifest)
            self.assertEqual(r['handler_bytes'],manifest[key][1])
            self.assertEqual(r['handler_sha256'],manifest[key][2])
            self.assertEqual(self.doc['original_handler_sha256'][r['handler']],manifest[key][2])

    def test_04_source_families_and_13_shops_not_new_stock(self):
        self.assertEqual(collections.Counter(r['kind'] for r in self.rows),{
            'npcgen_shop':13,'npcgen_man':8,'npcgen_mugon':6,'npcgen_limitshop':3,
            'npcgen_winhealer':3,'npcgen_dengon':3,'npcgen_petshop':2,'npcgen_petskillshop':2})
        old=[r for r in self.items['npcgen_shop_creation_rows'] if r['create_path']=='genout/shop_m3.create']
        self.assertEqual(len(old),13)
        self.assertEqual(self.doc['counts']['already_indexed_npcgen_shop_CREATE'],13)
        self.assertIs(self.doc['prior_content_dedup']['newly claimed_13_shops_or_30_RD_discoveries'],False)

    def test_05_old_DAT_geometry_no_fabrication(self):
        lookup={r[0].removesuffix('.dat'):(r[3],r[4]) for r in self.map['per_floor_source_rows']}
        n=0
        for r in self.rows:
            size=lookup.get(str(r['floor']))
            if size is None:
                n+=1;self.assertEqual(r['prior_source_DAT_dimension_status'],'NO_QUALIFIED_DAT')
            else:
                self.assertEqual(r['prior_DAT_dimensions'],list(size))
                x,y=r['xy'];self.assertTrue(0<=x<size[0] and 0<=y<size[1])
                self.assertEqual(r['prior_source_DAT_dimension_status'],'WITHIN_DAT_DIMENSIONS')
        self.assertEqual(n,2)
        self.assertEqual(self.doc['source_missing_DAT_floor_rows'],[
            {'ordinal':12,'floor':5000,'xy':[50,23]},
            {'ordinal':38,'floor':6000,'xy':[45,73]}])

    def test_06_30_unique_real_source_bitmap_candidates(self):
        self.assertEqual(len(self.pixels),30)
        self.assertEqual(len({r['graphic'] for r in self.pixels}),30)
        self.assertEqual(len({r['source_bitmap'] for r in self.pixels}),30)
        self.assertEqual({r['graphic'] for r in self.pixels},{r['graphic'] for r in self.rows})
        self.assertEqual(collections.Counter(r['source_kind'] for r in self.pixels),{
            'TW1_ADRN_ALIAS':24,'TW1_SPR_ACTION0_DIR0_FIRST_FRAME':6})
        for r in self.pixels:
            self.assertGreater(r['width'],0);self.assertGreater(r['height'],0)
            for field in ('rd_sha256','source_adrn_record_sha256','indexed_pixel_sha256',
                          'palet1_candidate_rgba_sha256','palet1_candidate_png_sha256'):
                self.assertRegex(r[field],r'^[0-9a-f]{64}$')

    def test_07_six_SPR_groups_qualified_in_prior_PET07(self):
        known={r[0] for r in self.pet07['source_groups']}
        spr=[r for r in self.pixels if r['source_kind']=='TW1_SPR_ACTION0_DIR0_FIRST_FRAME']
        self.assertEqual(sorted(r['graphic'] for r in spr),[100252,100279,100288,100291,100351,100367])
        self.assertTrue(all(r['graphic'] in known for r in spr))
        oldrd={r[0]:r[2] for r in self.pet07['source_actual_pixel_receipts']}
        for r in spr:
            self.assertEqual(oldrd[r['source_bitmap']],r['rd_sha256'])

    def test_08_coordinate_vs_handler_basename_negative(self):
        row=self.rows[24];actual=self.doc['source_counterexample']
        self.assertEqual((row['floor'],row['xy']),(5105,[22,8]))
        self.assertEqual(row['handler'],'npc/genout/ss_5105_24_10')
        self.assertTrue(actual['different_filename_coordinates_not_silently_corrected'])
        self.assertNotEqual([22,8],[24,10])

    def test_09_independent_private_custody_and_browser_boundary(self):
        z=self.doc['custody']['private_gallery'];self.assertEqual(z['bytes'],215924)
        self.assertEqual(z['sha256'],'308e4a6a0cd00af200a7f9208adf9e630413ed5cb53a3cb15e1cf7b10efcb7c8')
        self.assertEqual(z['members'],92);self.assertTrue(z['library_download_full_SHA_CRC_roundtrip_pass'])
        obs=self.doc['pixel_observation']['private_gallery_exact_browser_test']
        self.assertEqual((obs['cards'],obs['PNG_image_elements_loaded'],obs['distinct_png']),(40,40,30))
        self.assertEqual((obs['source_floor5001_filtered_cards'],obs['source_npcgen_shop_filtered_cards'],obs['reset_cards']),(3,13,40))
        self.assertEqual((obs['javascript_errors'],obs['external_http_requests']),(0,0))
        self.assertFalse(obs['original_game_runtime']);self.assertFalse(obs['original_file_url_navigation_success'])

    def test_10_no_original_game_or_proprietary_source_promotion(self):
        d=self.doc['strict_limits']
        for k in ('original_native_game_executed','official_same_deployment_proven','original_real_palette_selector_proven',
                  'commercial_text_or_images_uploaded_publicly','shop_stock_transaction_or_gameplay_verified',
                  'TW1_retail_pixels_imply_later_mixed25_NPC_identity'):
            self.assertIs(d[k],False)
        self.assertEqual(d['new_qualified_DAT_original_bytes_read'],0)
        for r in self.rows:
            self.assertFalse(any(k in r for k in ('original_text','script_body','original_bitmap_bytes','source_CP950_content')))


if __name__=='__main__':unittest.main()
