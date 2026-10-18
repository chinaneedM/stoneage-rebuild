"""Negative provenance and GIF admission cases use generated images, never source pixels."""
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import unittest
from PIL import Image
from tools.stoneage_jp_pet_visual_sample import PARENT, MANIFEST, REPORT, SELECTION, build, inspect_image, validate_manifest


def generated_gif(size=(60, 65), frames=1, color=0):
    out = BytesIO()
    ims = [Image.new('RGB', size, (color, i * 80, 180)) for i in range(frames)]
    ims[0].save(out, format='GIF', save_all=frames > 1, append_images=ims[1:], duration=100, loop=0)
    return out.getvalue()


def fixture():
    raw = PARENT.read_bytes()
    manifest = json.loads(MANIFEST.read_text())
    acquired = {}
    for i, pin in enumerate(manifest['entries']):
        data = generated_gif(color=i * 16)
        pin.update(bytes=len(data), sha256=sha256(data).hexdigest())
        acquired[pin['web_ordinal']] = data, pin['strict_replay_url']
    return raw, manifest, acquired


class PetVisualSampleTests(unittest.TestCase):
    def test_exact_parent_catalog_required(self):
        _, manifest, _ = fixture()
        with self.assertRaisesRegex(ValueError, 'Parent catalog'):
            validate_manifest(b'{}', manifest)

    def test_names_references_and_page_capture_cannot_be_reassigned(self):
        raw, manifest, _ = fixture()
        for key, wrong in [('name_as_written', 'invented alias'), ('original_url', manifest['entries'][1]['original_url']), ('page_capture', '20060604065940')]:
            m = deepcopy(manifest); m['entries'][0][key] = wrong
            with self.assertRaises(ValueError):
                validate_manifest(raw, m)

    def test_finite_selection_and_distinct_table_groups(self):
        raw, manifest, acquired = fixture()
        result = build(raw, manifest, acquired)
        self.assertEqual(result['selection'], SELECTION)
        self.assertEqual(result['coverage']['qualified_new_images'], 12)
        self.assertEqual(result['coverage']['qualified_with_parent'], 13)
        self.assertEqual(result['coverage']['remaining_unacquired_references'], 111)
        for change in ('extra', 'reorder', 'duplicate'):
            m = deepcopy(manifest)
            if change == 'extra': m['entries'].append(deepcopy(m['entries'][0]))
            elif change == 'reorder': m['entries'].reverse()
            else: m['entries'][1] = deepcopy(m['entries'][0])
            with self.assertRaisesRegex(ValueError, 'selection'):
                validate_manifest(raw, m)

    def test_image_host_path_capture_and_raw_mode_are_pinned(self):
        _, m, acquired = fixture(); pin = m['entries'][0]; data, url = acquired[2]
        for wrong in (url.replace('images.hangame.co.jp', 'example.org'), url.replace('20060604065940', pin['page_capture']), url.replace('id_/', 'im_/')):
            with self.assertRaisesRegex(ValueError, 'host/path/capture'):
                inspect_image(data, wrong, pin)
        wrong = deepcopy(pin); wrong['actual_capture'] = wrong['page_capture']
        m['entries'][0] = wrong
        with self.assertRaisesRegex(ValueError, 'archived image URL'):
            validate_manifest(PARENT.read_bytes(), m)

    def test_wrong_error_body_and_swapped_images_rejected(self):
        _, m, a = fixture(); pin = m['entries'][0]
        for data in (b'x' * pin['bytes'], a[10][0]):
            with self.assertRaisesRegex(ValueError, 'byte pin'):
                inspect_image(data, pin['strict_replay_url'], pin)

    def test_dimensions_and_actual_frames_verified_beyond_hash(self):
        _, m, _ = fixture(); pin = deepcopy(m['entries'][0])
        data = generated_gif(size=(65, 60)); pin.update(bytes=len(data), sha256=sha256(data).hexdigest())
        with self.assertRaisesRegex(ValueError, 'dimensions'):
            inspect_image(data, pin['strict_replay_url'], pin)
        data = generated_gif(frames=2); pin.update(bytes=len(data), sha256=sha256(data).hexdigest())
        with self.assertRaisesRegex(ValueError, 'frame count'):
            inspect_image(data, pin['strict_replay_url'], pin)
        pin['frames'] = 2
        inspect_image(data, pin['strict_replay_url'], pin)

    def test_missing_extra_or_unreviewed_source_not_silently_accepted(self):
        raw, m, a = fixture()
        a.pop(2)
        with self.assertRaisesRegex(ValueError, 'bytes missing'):
            build(raw, m, a)
        raw, m, a = fixture(); a[124] = a[2]
        with self.assertRaisesRegex(ValueError, 'Extra unselected'):
            build(raw, m, a)
        m['entries'][0]['visual_review']['status'] = 'NOT_VIEWED'
        with self.assertRaisesRegex(ValueError, 'visual review'):
            validate_manifest(raw, m)

    def test_failed_attempt_remains_reference_only_not_historical_absence(self):
        raw, m, a = fixture(); pin = m['entries'][0]
        pin['status'] = 'UNAVAILABLE_THIS_BOUNDED_ATTEMPT'
        for k in ('actual_capture','strict_replay_url','sha256','bytes','format','actual_size','frames','visual_review'):
            pin.pop(k, None)
        pin['attempts'] = [{'attempt':1,'error_type':'TimeoutError','error':'synthetic finite failure'}]
        a.pop(2)
        result = build(raw,m,a)
        first = result['records'][0]
        self.assertFalse(first['image']['pixels_acquired'])
        self.assertIsNone(first['image']['sha256'])
        self.assertIsNone(first['visual_review'])
        self.assertEqual(result['coverage']['unavailable_this_attempt'],1)
        self.assertEqual(result['coverage']['remaining_unacquired_references'],112)
        self.assertEqual(first['verification_status'],'REFERENCE_ONLY_PIXEL_SOURCE_UNAVAILABLE_THIS_ATTEMPT')

    def test_per_record_epoch_archive_fields_unknowns_and_rights_survive_export(self):
        p = json.loads(REPORT.read_text())
        contract=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        self.assertEqual(p['coverage']['new_image_capture_year_counts'], {'2003':5,'2006':4,'2008':2,'2016':1})
        for r in p['records']:
            self.assertLessEqual(set(contract['record_contract']['required']),r.keys())
            self.assertIn(r['collection'],contract['required_collections'])
            self.assertNotEqual(r['rights_status'],'RELEASE_APPROVED')
            self.assertEqual(len(r['source_refs']),2)
            self.assertNotEqual(r['source_refs'][0]['actual_capture'],r['source_refs'][1]['actual_capture'])
            self.assertIsNone(r['client_species_graphic_ids'])
            self.assertIsNone(r['cross_region_aliases'])
            self.assertIsNone(r['stats_growth_habitat_skills'])
            self.assertFalse(r['image']['original_client_sprite_or_animation_proven'])
        one_hundred = next(r for r in p['records'] if r['web_ordinal']==100)
        self.assertTrue(one_hundred['image']['actual_capture'].startswith('2016'))
        self.assertTrue(one_hundred['source_refs'][0]['actual_capture'].startswith('2004'))


if __name__ == '__main__':
    unittest.main()
