"""Public source-gate tests: no proprietary binaries or private archive in CI."""
from pathlib import Path
import json
import struct
import unittest

from tools.stoneage_world37_capture_required_table import (
    ARCHIVE_SHA, EXE_EXPECTED_SHA, MASTER_SHA, SECTIONS, DATA_VA,
    read_compiled_rows, read_items,
)

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-STAGE-A-WORLD37-R2B-COMPILED-CAPTURE-REQUIRED-ITEMS-R1.json'
WORLD31=ROOT/'research/recovered/STONEAGE-STAGE-A-WORLD31-ITEMSET-VARIANT-R1.json'
R2A=ROOT/'research/recovered/STONEAGE-STAGE-A-WORLD37-R2A-ORIGINAL-COMPILED-CAPTURE-TAIL-STATIC-R1.json'

class CaptureRequiredItems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(REPORT.read_text(encoding='utf-8'))
        cls.r2a=json.loads(R2A.read_bytes())
        cls.world31=json.loads(WORLD31.read_bytes()) if WORLD31.exists() else None

    def test_original_source_identity_and_prior_independent_section_pins(self):
        r=self.report
        self.assertEqual(r['archive_expected_sha256'],ARCHIVE_SHA)
        self.assertTrue(r['archive_in_this_invocation_sha256_verified'])
        self.assertEqual(r['exe_expected_sha256'],EXE_EXPECTED_SHA)
        self.assertFalse(r['exe_original_full_sha256_verified'])
        self.assertEqual(r['qualification'],'FOUR_PE_SECTIONS_REVERIFIED_NOT_FULL_EXE')
        self.assertEqual(r['original_source_file_backed_sections_sha256'],SECTIONS)
        self.assertEqual(SECTIONS,self.r2a['source_qualification']['four_file_backed_section_sha256_equal_previously_independently_verified_WORLD34_R2_R3'])
        self.assertEqual(r['exe_local_full_sha256'],self.r2a['local_libarchive_block_recovery']['sha256'])

    def test_compiled_table_11_nonzero_rows_and_117_zero_slots(self):
        t=self.report['original_condition_table']
        self.assertEqual((t['source_va'],t['capacity'],t['record_bytes'],t['active_rows'],t['zero_rows']), (DATA_VA,128,64,11,117))
        self.assertEqual(t['raw_table_sha256'],'fcec682619dbb83439f7160a99a35279290344c4b14d7190118c9de74648db56')
        self.assertEqual([r['source_record_index'] for r in t['rows']],list(range(11)))
        for r in t['rows']:
            self.assertRegex(r['record_sha256'],r'^[0-9a-f]{64}$')

    def test_key53_to_original_itemid_evidence(self):
        rows=self.report['original_condition_table']['rows']
        expected={524:[2456],961:[20219],953:[20223],962:[20222],777:[20253],796:[20247],812:[20259],
                  1105:[1690,1691,1692],8:[1810],145:[2236],146:[2236]}
        self.assertEqual({r['char_int_key_53_value']:r['required_item_id_candidates'] for r in rows},expected)
        refs=[i for r in rows for i in r['required_item_id_candidates']]
        self.assertEqual((len(refs),len(set(refs))),(13,12))
        self.assertEqual(refs.count(2236),2)

    def test_original_itemsets_distinct_presence_not_invented(self):
        r=self.report
        self.assertEqual(r['original_item_masters_sha256'],MASTER_SHA)
        if self.world31 is not None:
            self.assertEqual(r['original_item_masters_sha256']['itemset.txt'], self.world31['source_itemsets']['itemset.txt']['original_member_sha256'])
            self.assertEqual(r['original_item_masters_sha256']['itemset0710.txt'], self.world31['source_itemsets']['itemset0710.txt']['original_member_sha256'])
            self.assertEqual(self.world31['configured_itemset_from_world31_setup_cf'],'itemset.txt')
        self.assertEqual(r['summary'],{'selected_present':9,'alternate_present':12,'alternate_only_ids':[20247,20253,20259]})
        observed=r['original_item_id_crosswalk']
        self.assertEqual([x['item_id'] for x in observed],sorted(x['item_id'] for x in observed))
        self.assertEqual([x['item_id'] for x in observed if x['selected'] is None],[20247,20253,20259])
        for x in observed:
            self.assertIsNotNone(x['alternate_0710'])
            self.assertEqual(x['presence'], 'ONLY_ALTERNATE' if x['selected'] is None else 'IN_BOTH')
            if x['selected']:
                self.assertEqual(x['selected']['name_cp950'],x['alternate_0710']['name_cp950'])

    def test_actual_original_name_crosswalk_specifics(self):
        rows={x['item_id']:x for x in self.report['original_item_id_crosswalk']}
        self.assertEqual(rows[2456]['selected']['name_cp950'],'加特利奴喜愛的食物')
        self.assertEqual(rows[1690]['selected']['name_cp950'],'海藍之棒')
        self.assertEqual(rows[20247]['alternate_0710']['name_cp950'],'魔法鑽戒[地LV3-1]')
        self.assertEqual(rows[20253]['alternate_0710']['name_cp950'],'魔法鑽戒[水LV3-1]')
        self.assertEqual(rows[20259]['alternate_0710']['name_cp950'],'魔法鑽戒[火LV3-1]')

    def test_code_sites_not_runtime_claims(self):
        c=self.report['compiled_call_sites']
        self.assertEqual((c['precheck_key53']['source_va'],c['precheck_key53']['target_va']),(0x537d51,0x42db90))
        self.assertEqual((c['delete_key53']['source_va'],c['delete_key53']['target_va']),(0x537e6f,0x42db90))
        self.assertEqual((c['delete_inventory']['source_va'],c['delete_inventory']['target_va']),(0x538099,0x433ab0))
        for call in c.values():self.assertRegex(call['source_sha256'],r'^[0-9a-f]{64}$')
        b=self.report['negative_boundaries']
        for key in ('actual_conditional_item_consumption_executed','original_dynamic_capture_tail_executed',
                    'original_enemy_species_names_proven_by_key53', 'configured_original_item_master_selected_is_alternate',
                    'all_128_capture_rows_are_real_pet_species','same_build_official_TW1_or_JSS1999_server_verified',
                    'missing_selected_item_ids_are_invented_or_filled'):
            self.assertIs(b[key],False,key)
        self.assertEqual(b['overall_percent'],None)

    def test_synthetic_wrong_sentinel_rejected(self):
        blob=bytearray(128*64)
        struct.pack_into('<16i',blob,0,524,2456,*([-1]*9),*([0]*5))
        def take(va,n):
            self.assertEqual(va,DATA_VA)
            return bytes(blob[:n])
        rows,_=read_compiled_rows(take)
        self.assertEqual(len(rows),1)
        struct.pack_into('<i',blob,2*4,0)
        with self.assertRaisesRegex(ValueError,'invalid item ID'):
            read_compiled_rows(take)
        struct.pack_into('<i',blob,2*4,-1)
        struct.pack_into('<i',blob,3*4,3)
        with self.assertRaisesRegex(ValueError,'trailing item-slot padding'):
            read_compiled_rows(take)

    def test_synthetic_master_rejects_duplicate_or_wrong_field_width(self):
        row=[b'']*94
        row[16]=b'2456'
        line=b','.join(row)+b'\r\n'
        self.assertEqual(len(read_items(line)),1)
        with self.assertRaisesRegex(ValueError,'duplicate'):
            read_items(line+line)
        with self.assertRaisesRegex(ValueError,'master width'):
            read_items(b'single-field\n')

if __name__=='__main__':unittest.main()
