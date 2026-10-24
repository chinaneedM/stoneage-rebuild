import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import stoneage_quest_material_review_r116 as audit


class MaterialReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, cls.objects = audit.load_inputs()

    def test_independent_occurrence_count_and_exact_committed_replay(self):
        result = audit.verify()
        # Independent traversal of the two actual container names used by these
        # archives; does not use the production walk/selected implementation.
        ids = []
        for obj in self.objects.values():
            for key in ('records', 'catalog_records'):
                for row in obj.get(key, []):
                    if isinstance(row, dict) and (row.get('collection') == 'quests' or row.get('entity_type') == 'quest'):
                        ids.append(row['record_id'])
        self.assertEqual((len(ids), len(set(ids))), (73, 49))
        self.assertEqual(result['counts']['selected_record_occurrences'], len(ids))
        self.assertEqual(result['counts']['by_origin'], dict(zip(audit.CATEGORIES, (0, 0, 15, 34))))

    def test_version_story_and_repeatability_do_not_promote_to_base_or_permanent(self):
        objects = copy.deepcopy(self.objects)
        path = audit.PREFIX+'STONEAGE-JP2008-RIMFY-FAMILY-QUEST-SOURCE-R1.json'
        objects[path]['records'][0].update(origin_class='BASE_GAME_QUEST', repeatable=True, permanent=True)
        result = audit.summarize(self.manifest, objects)
        row = next(r for r in result['records'] if r['record_id'] == 'jp-2008-rimfy:quest')
        self.assertEqual(row['origin_class'], 'ORIGIN_UNRESOLVED')

    def test_permanent_services_do_not_promote_cooperation_collection_event(self):
        result = audit.summarize(self.manifest, self.objects)
        rows = [r for r in result['records'] if r['record_id'] in ('JP2008-COOP-07', 'JP2008-COOP-08')]
        self.assertEqual([r['origin_class'] for r in rows], ['OPERATOR_EVENT_QUEST']*2)

    def test_whole_file_event_class_not_inherited_by_unreviewed_children(self):
        objects = copy.deepcopy(self.objects)
        path = audit.PREFIX+'STONEAGE-JP2009-MYSTERY-DUNGEON-R111.json'
        row = copy.deepcopy(objects[path]['records'][2])
        row['record_id'] = 'SAME_FILE_BUT_NO_EVENT_ORIGIN_EVIDENCE'
        objects[path]['records'].append(row)
        result = audit.summarize(self.manifest, objects)
        actual = next(r for r in result['records'] if r['record_id'] == row['record_id'])
        self.assertEqual(actual['origin_class'], 'ORIGIN_UNRESOLVED')

    def test_nonquest_npc_and_migration_records_excluded(self):
        result = audit.summarize(self.manifest, self.objects)
        self.assertFalse(any(r['collection_as_stored'] in ('npcs', 'social', 'maps') for r in result['records']))
        self.assertEqual(result['prior_report_level_overlay']['record_count'], 6)

    def test_conflicting_same_id_never_silently_deduplicated(self):
        objects = copy.deepcopy(self.objects)
        path = audit.PREFIX+'STONEAGE-CN20-PET-COMMISSION-HABITATS-CATALOG-R1.json'
        row = copy.deepcopy(objects[path]['records'][0])
        row['version_profile'] = 'DIFFERENT_REGION_OR_BUILD'
        objects[path]['records'].append(row)
        with self.assertRaisesRegex(ValueError, 'body conflict'):
            audit.summarize(self.manifest, objects)

    def test_missing_event_record_rejected(self):
        objects = copy.deepcopy(self.objects)
        path = audit.PREFIX+'STONEAGE-CN2003-CHRISTMAS-NPC-SOURCE-R1.json'
        objects[path]['records'] = [r for r in objects[path]['records'] if r['record_id'] != 'cn-wayi-2003-christmas:exchange']
        with self.assertRaisesRegex(ValueError, 'event missing'):
            audit.summarize(self.manifest, objects)

    def test_missing_required_field_rejected(self):
        objects = copy.deepcopy(self.objects)
        path = audit.PREFIX+'STONEAGE-JP2008-RIMFY-FAMILY-QUEST-SOURCE-R1.json'
        del objects[path]['records'][0]['version_profile']
        with self.assertRaisesRegex(ValueError, 'Incomplete'):
            audit.summarize(self.manifest, objects)

    def test_no_collection_not_silently_migrated(self):
        result = audit.summarize(self.manifest, self.objects)
        rows = [r for r in result['records'] if r['collection_as_stored'] is None]
        self.assertEqual([r['record_id'] for r in rows], ['jp-gaiax-2005:special-map-4'])

    def test_json_pointer_escaping(self):
        rows = list(audit.walk({'a/b': {'~c': [{'record_id': 'x'}]}}))
        self.assertIn(('/a~1b/~0c/0', {'record_id': 'x'}), rows)

    def test_frozen_manifest_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            p = root/audit.MANIFEST
            p.parent.mkdir(parents=True)
            d = copy.deepcopy(self.manifest)
            d['files'].pop()
            p.write_text(json.dumps(d))
            with self.assertRaisesRegex(ValueError, 'manifest changed'):
                audit.load_inputs(root)

    def test_same_length_actual_source_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            p = root/audit.MANIFEST
            p.parent.mkdir(parents=True)
            shutil.copyfile(audit.ROOT/audit.MANIFEST, p)
            first = self.manifest['files'][0]['path']
            raw = (audit.ROOT/first).read_bytes()
            (root/first).write_bytes(b'!' + raw[1:])
            with self.assertRaisesRegex(ValueError, 'Source bytes changed'):
                audit.load_inputs(root)

    def test_report_tampering_rejected_after_valid_inputs(self):
        result = audit.summarize(self.manifest, self.objects)
        result['interpretation']['overall_restoration_percentage'] = 99
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            p = root/audit.REPORT
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps(result))
            with patch.object(audit, 'load_inputs', return_value=(self.manifest, self.objects)):
                with self.assertRaisesRegex(ValueError, 'semantic replay'):
                    audit.verify(root)


if __name__ == '__main__':
    unittest.main()
