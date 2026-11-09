"""Public replay of the source joins. Original files stay in the private package."""
import json
import unittest

from tools.stoneage_integration16_pet_rooms import (
    FLOORS, PINS, REPORT, ROOT, service_candidates, upstream,
)


class PetRoomEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = upstream()
        cls.report = json.loads((ROOT / 'research/recovered' / REPORT).read_bytes())

    def test_rooms_match_pinned_source_dat_and_canvas(self):
        self.assertEqual(self.report['upstream_git_blobs'], {k: v[1] for k, v in PINS.items()})
        self.assertEqual(tuple(map(int, self.report['rooms'])), FLOORS)
        map07 = {r['floor']: r for r in self.source['map07']['maps']}
        for floor, room in self.report['rooms'].items():
            map09 = self.source['map09']['maps'][floor]
            self.assertEqual(room['dat']['sha256'], map07[int(floor)]['source_dat_sha256'])
            self.assertEqual(room['dat']['sha256'], map09['source_sha256'])
            self.assertEqual(room['canvas']['rgba_sha256'], map09['frame_RGBA_sha256']['combined'])
            self.assertEqual(room['canvas_size'], map09['canvas_size'])
            self.assertEqual(room['origin'], map09['origin'])
            left, top, width, height = room['observer_view_box']
            for service in room['services']:
                x, y = service['graphic_px']
                w, h = service['graphic_dimensions']
                self.assertTrue(left <= x <= x + w <= left + width <= room['canvas_size'][0])
                self.assertTrue(top <= y <= y + h <= top + height <= room['canvas_size'][1])
        self.assertEqual([r['server_client_changed_cells'] for r in self.report['rooms'].values()],
                         [[0, 60], [0, 88], [0, 0]])

    def test_each_service_retains_its_exact_source_identity(self):
        char = self.source['char']
        creates = {(r[0], r[1]): r for r in char['create_rows']}
        templates = {(r[0], r[1]): r for r in char['template_rows']}
        graphics = {g['graphic']: g for g in self.report['graphics']}
        seen = []
        for floor, room in self.report['rooms'].items():
            candidates = list(service_candidates(self.source, int(floor)))
            self.assertEqual(len(room['services']), 2)
            for row, source in zip(room['services'], candidates, strict=True):
                path, ordinal, parameter, role, parameter_sha, create_sha, alias = source
                original = creates[path, ordinal]
                self.assertEqual(row['floor'], int(floor))
                self.assertEqual(row['role'], role)
                self.assertEqual(row['create'], [path, ordinal, create_sha])
                self.assertEqual(row['parameter'], [parameter, parameter_sha])
                self.assertEqual(row['xy'], original[7][:2])
                self.assertEqual(row['graphic'], alias)
                self.assertEqual(row['template'][:2], original[13][0])
                self.assertEqual(row['template'][2], templates[tuple(row['template'][:2])][2])
                x, y = row['xy']
                ox, oy = room['origin']
                self.assertEqual(row['marker_px'], [ox + (x + y)*32, oy + (y - x)*24])
                graphic = graphics[alias]
                self.assertEqual(row['graphic_px'], [a + b for a, b in
                                 zip(row['marker_px'], graphic['signed_adrn_offset'])])
                self.assertEqual(row['graphic_dimensions'], graphic['dimensions'])
                seen.append((alias, role, int(floor), create_sha))
        self.assertEqual(len({r[3] for r in seen}), 6)
        self.assertEqual([r[:3] for r in seen if r[0] == 16046],
                         [(16046, 'PetShop', 1103), (16046, 'PetSkillShop', 2003)])

    def test_reused_and_redecoded_images_are_separated(self):
        prior = {r['graphic']: r for r in self.source['world11']['decoded_static_graphics']}
        graphics = self.report['graphics']
        self.assertEqual([r['graphic'] for r in graphics], [16027, 16035, 16036, 16046, 16047])
        for graphic in graphics:
            alias = graphic['graphic']
            self.assertNotEqual(graphic['bitmap'], alias)
            if alias in (16035, 16036, 16046):
                self.assertEqual(graphic['mode'], 'WORLD11_REUSED_ORIGINAL_PNG')
                for key in ('adrn_ordinal', 'adrn_sha256', 'rd_sha256', 'indexed_sha256',
                            'rgba_sha256', 'png_sha256', 'dimensions', 'signed_adrn_offset'):
                    self.assertEqual(graphic[key], prior[alias][key])
            else:
                self.assertEqual(graphic['mode'], 'TWO_DECODERS_ORIGINAL_RD')
                self.assertNotIn(alias, prior)

    def test_original_door_endpoints_are_reciprocal_rows(self):
        self.assertEqual(self.report['original_mapwarp_sha256'], self.source['map01']['mapwarp']['source_sha256'])
        expected = {
            '1103': [(1439, [1100, 61, 109], [1103, 15, 21]), (1441, [1100, 62, 109], [1103, 16, 21])],
            '1203': [(1562, [1200, 39, 34], [1203, 15, 21]), (1564, [1200, 40, 34], [1203, 16, 21])],
            '2003': [(1523, [2000, 75, 57], [2003, 10, 15]), (1525, [2000, 75, 58], [2003, 10, 16])],
        }
        for floor, rows in expected.items():
            want = []
            for line, source, target in rows:
                want.extend(((line, source, target), (line + 1, target, source)))
            self.assertEqual([(r['line'], r['source'], r['target']) for r in self.report['rooms'][floor]['warps']], want)

    def test_claims_are_limited_to_original_files_and_private_replay(self):
        bounds = self.report['bounds']
        for key in ('official_same_deployment', 'original_client_or_server_executed',
                    'native_renderer_or_collision_verified', 'native_storage_or_training_verified',
                    'proprietary_sources_published'):
            self.assertIs(bounds[key], False, key)
        self.assertIsNone(bounds['overall_percent'])
        browser = self.report['browser']
        self.assertTrue(browser['exact_zip_index_file_url'])
        self.assertEqual((browser['external_requests'], browser['browser_errors']), (0, 0))
        self.assertEqual([r['floor'] for r in browser['rooms']], list(FLOORS))
        self.assertEqual(sum(r['details_verified'] for r in browser['rooms']), 6)
        self.assertTrue(all(r['overlay_changes_pixels_and_hides_again'] for r in browser['rooms']))
        self.assertEqual(self.report['parent_rar']['sha256'], self.source['map01']['original_rar_sha256'])
        self.assertEqual(self.report['private_package']['filename'],
                         'StoneAge-INTEGRATION16-three-pet-rooms-private.zip')
        self.assertTrue(self.report['private_package']['library_roundtrip_sha256_and_crc_verified'])


if __name__ == '__main__':
    unittest.main()
