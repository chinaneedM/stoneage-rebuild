import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from tools import stoneage_material_review_r102 as m

class MaterialReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((m.ROOT/m.MANIFEST).read_text())
        cls.objects = {p['path']: json.loads((m.ROOT/p['path']).read_text())
                       for p in cls.manifest['files']}
        cls.payload = (m.ROOT/m.JP_SOURCE).read_text()
        cls.review = json.loads((m.ROOT/m.REVIEW).read_text())

    def test_full_frozen_replay(self):
        self.assertEqual(m.audit(), json.loads((m.ROOT/m.REPORT).read_text()))

    def test_changed_source_rejected_before_semantic_counting(self):
        real = Path.read_bytes
        target = m.ROOT/m.JP_SOURCE
        def changed(path):
            data = real(path)
            return data+b' ' if path == target else data
        with patch.object(Path, 'read_bytes', changed), self.assertRaisesRegex(ValueError, 'Frozen evidence'):
            m.audit()

    def test_manifest_cannot_silently_drop_files(self):
        real = Path.read_bytes
        target = m.ROOT/m.MANIFEST
        def changed(path):
            return b'{}' if path == target else real(path)
        with patch.object(Path, 'read_bytes', changed), self.assertRaisesRegex(ValueError, 'manifest'):
            m.audit()

    def test_json_pointer_escaping_and_nested_records(self):
        row = dict.fromkeys(m.FIELDS, 'x')
        obj = {'a/b~c': [row, {'inner': row}]}
        groups, files, near = m.collect({'sample': obj})
        self.assertEqual([x[1] for x in groups['x']], ['/a~1b~0c/0', '/a~1b~0c/1/inner'])
        self.assertEqual(files, {'sample'})
        self.assertEqual(near, [])

    def test_seven_fields_do_not_require_collection(self):
        row = dict.fromkeys(m.FIELDS, 'x')
        groups, _, near = m.collect({'sample': [row, {'record_id':'y','entity_type':'pet'}]})
        self.assertEqual(len(groups), 1)
        self.assertEqual(near[0]['missing'], sorted(m.FIELDS-{'record_id','entity_type'}))

    def test_provenance_enrichment_requires_exact_original_builder(self):
        objects = dict(self.objects)
        altered = copy.deepcopy(objects[m.JP_CATALOG])
        altered['records'][0]['illustration']['same_instant_as_page_proven'] = True
        objects[m.JP_CATALOG] = altered
        with self.assertRaisesRegex(ValueError, 'documented enrichment'):
            m.summarize(objects, self.payload, self.manifest)

    def test_first_page_cannot_be_added_as_new_pet_positions(self):
        objects = dict(self.objects)
        altered = copy.deepcopy(objects[m.CN_FIRST])
        altered['records'][0]['record_id'] += ':invented'
        objects[m.CN_FIRST] = altered
        with self.assertRaisesRegex(ValueError, 'inclusion'):
            m.summarize(objects, self.payload, self.manifest)

    def test_unknown_variant_is_not_silently_deduplicated(self):
        objects = dict(self.objects)
        row = copy.deepcopy(objects[m.CN_FIRST]['records'][0])
        row['record_revision'] = 'invented'
        objects['synthetic_test_only'] = row
        with self.assertRaisesRegex(ValueError, 'Unexplained distinct-body'):
            m.summarize(objects, self.payload, self.manifest)

    def test_cross_region_ids_are_not_alias_merged(self):
        objects = dict(self.objects)
        jp = copy.deepcopy(objects[m.JP_PETS])
        jp['records'][0]['record_id'] = objects[m.CN_FINITE]['records'][0]['record_id']
        objects[m.JP_PETS] = jp
        with self.assertRaisesRegex(ValueError, 'web-position union'):
            m.summarize(objects, self.payload, self.manifest)

    def test_baseline_domain_status_cannot_be_closed(self):
        review = copy.deepcopy(self.review)
        review['domains'][5]['complete'] = True
        with self.assertRaises(ValueError):
            m.validate_review(review, self.objects)
        review = copy.deepcopy(self.review)
        review['domains'][5]['baseline_status'] = 'COMPLETE'
        with self.assertRaisesRegex(ValueError, 'Baseline status'):
            m.validate_review(review, self.objects)

    def test_counts_cannot_be_promoted_to_completion_or_export(self):
        for key, value in [('overall_completion_percentage',99),('public_export_approved',True),
                           ('new_historical_source_acquired',True)]:
            review = copy.deepcopy(self.review)
            review['boundaries'][key] = value
            with self.assertRaisesRegex(ValueError, 'boundary'):
                m.validate_review(review, self.objects)

if __name__ == '__main__':
    unittest.main()
