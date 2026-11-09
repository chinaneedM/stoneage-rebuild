"""Verify the public Hotoru shop joins without reading any private game bytes."""
import csv
import gzip
import hashlib
import json
from pathlib import Path
import struct
import unittest

from tools.stoneage_integration14_hotoru_shop_items import FIELDS, REPORT, TARGETS, expanded, field_values, verify_cn_block
from tools.stoneage_item05_shop_stock import old_items

REC = Path(__file__).resolve().parents[1] / 'research/recovered'


def load(pattern):
    paths = list(REC.glob(pattern))
    if len(paths) != 1:
        raise AssertionError(pattern)
    return json.loads(paths[0].read_bytes())


class Integration14Public(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = load(REPORT)
        cls.shops = cls.report['shops']
        cls.items = cls.report['items']
        cls.index = old_items()

    def test_original_create_paths_and_parameter_hashes(self):
        i13 = load('*INTEGRATION13-HOTORU-FIVE-ROOMS-SOURCE*')
        i12 = load('*INTEGRATION12-HOTORU-TWO-ROOMS-SOURCE-JOINS*')
        a, = [r for r in i13['rooms']['1305']['source_create'] if r['functionset'] == 'ItemShop']
        b, = [r for r in i12['rooms']['1310']['source_create'] if r['functionset'] == 'ItemShop']
        for floor, r, key, param_sha in [
            ('1305', a, 'block_sha256', a['parameters'][0]['sha256']),
            ('1310', b, 'sha256', b['parameter_sha256']),
        ]:
            shop = self.shops[floor]
            self.assertEqual((shop['create_path'],shop['create_ordinal'],shop['xy'],shop['create_sha256'],
                              shop['argument_sha256']), (r['path'],r['ordinal'],r['xy'],r[key],param_sha))
        self.assertEqual(self.shops['1310']['xy'], [16, 16])

    def test_field_roles_and_presence_do_not_collapse(self):
        counts = {
            '1305': {'itemlist': (12,12,12,12), 'limititemno': (51,44,51,44), 'special_item': (0,0,0,0)},
            '1310': {'itemlist': (16,0,16,0), 'limititemno': (21,0,21,0), 'special_item': (5,0,5,0)},
        }
        for floor, shop in self.shops.items():
            for k, v in shop['fields'].items():
                self.assertEqual(hashlib.sha256(v['literal'].encode()).hexdigest(), v['value_sha256'])
                ids = expanded(v)
                values = [self.index[i][:2] for i in ids]
                summary = (len(ids),sum(a is not None for a,_ in values),sum(b is not None for _,b in values),
                           sum(a is not None and a == b for a,b in values))
                self.assertEqual(summary, counts[floor][k])
                self.assertEqual(v['counts'],dict(zip(('occurrences','primary','alternate','both_identical'),summary)))
        for n in TARGETS:
            membership = self.items[str(n)]['membership']
            self.assertEqual(membership['1305'], ['limititemno'])
            self.assertEqual(membership['1310'], ['itemlist','limititemno'] if n >= 1546 else [])

    def test_physical_alternate_rows_retain_seven_distinct_items(self):
        self.assertEqual({int(n) for n in self.items}, set(TARGETS))
        for n in TARGETS:
            r = self.items[str(n)]
            self.assertIsNone(r['primary_row'])
            self.assertEqual([None,r['alternate_row_sha256']],self.index[n][:2])
            self.assertEqual(r['fields']['imagenumber'],self.index[n][3])
            self.assertEqual(r['alternate_line'],n+1)
            self.assertIsNone(r['fields']['magicid'])
        a,b = [self.items[str(n)] for n in TARGETS[:2]]
        self.assertEqual(a['fields']['imagenumber'],b['fields']['imagenumber'])
        self.assertNotEqual(a['text_field_sha256']['argument'],b['text_field_sha256']['argument'])
        self.assertNotEqual(a['alternate_row_sha256'],b['alternate_row_sha256'])

    def test_cn50_hashes_match_the_already_identified_five_tw85_blocks(self):
        images = self.report['image_sources']
        self.assertEqual(images['24095']['source'],'TW10_REUSED_ITEM01_OBSERVATION')
        tw = load('*ITEM07-PATCH129*')
        expected = {str(r['mixed25_item_image_alias']):r['patch_source_occurrences'][0]['source_original_rd_sha256']
                    for r in tw['aliases'] if str(r['mixed25_item_image_alias']) in images
                    and r['mixed25_item_image_alias'] != 24095}
        self.assertEqual(len(expected),5)
        by_index = {str(images[a]['index']):a for a in expected}
        with gzip.open(REC/'cn50-resource-metadata/ADRN-R1.tsv.gz','rt') as f:
            matched = {r['index']:r for r in csv.DictReader(f,delimiter='\t') if r['index'] in by_index}
        self.assertEqual(set(by_index),set(matched))
        for index, a in by_index.items():
            cn = matched[index]
            image = images[a]
            self.assertEqual(cn['rd_block_sha256'],expected[a])
            self.assertEqual((image['offset'],image['rd_bytes'],image['attr_sha256'],image['rd_sha256']),
                             (int(cn['adder']),int(cn['size']),cn['attr_sha256'],expected[a]))

    def test_images_and_limit_flags_do_not_promote_index_only_evidence(self):
        r = self.report
        count = r['new_cn50_rd_decode_count']
        self.assertIn(count,(0,5))
        for a,v in r['image_sources'].items():
            if a == '24095':
                continue
            self.assertEqual('indexed_sha256' in v, bool(count))
            self.assertEqual('png_sha256' in v, bool(count))
            self.assertEqual('adrn_sha256' in v, bool(count))
            self.assertEqual(v['source'].startswith('CN50_ORIGINAL'),bool(count))
        for k in ('native_loading_verified','native_trade_verified','native_palette_selection_verified',
                  'same_official_deployment_verified'):
            self.assertIs(r[k],False)
        self.assertEqual({r['setup_literal_paths'][f'itemset{i}file'] for i in (3,4,5,6)}, {'data/itemset.txt'})

    def test_catalog_attribute_hash_is_distinct_from_full_record_hash(self):
        attr = bytes(range(52))
        record = struct.pack('<IIIiiii',10,100,3,0,0,1,1)+attr
        rd = b'abc'
        digest = lambda data: hashlib.sha256(data).hexdigest()
        meta = dict(index=10,offset=100,rd_bytes=3,size=[1,1],
                    attr_sha256=digest(attr),rd_sha256=digest(rd))
        self.assertEqual(verify_cn_block(record,rd,meta),(1,1))
        with self.assertRaises(ValueError):
            verify_cn_block(record,rd,{**meta,'attr_sha256':digest(record)})
        with self.assertRaises(ValueError):
            verify_cn_block(record,b'abd',meta)

    def test_missing_duplicated_and_reversed_original_argument_fields_fail(self):
        valid = b'ItemList:1,3-4\nLimitItemNo:1-5\nspecial_item:\n'
        self.assertEqual(tuple(field_values(valid)),FIELDS)
        self.assertEqual(expanded(field_values(valid)['itemlist']),[1,3,4])
        with self.assertRaises(KeyError):
            field_values(valid.replace(b'special_item:\n',b''))
        with self.assertRaises(ValueError):
            field_values(valid+b'ItemList:0\n')
        with self.assertRaises(ValueError):
            field_values(valid.replace(b'3-4',b'4-3'))


if __name__ == '__main__':
    unittest.main()
