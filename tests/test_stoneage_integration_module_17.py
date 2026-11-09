"""Public receipts for MAP09 room replay, NPC services and directional doors."""
import json
import unittest

from tools.stoneage_integration16_pet_rooms import PINS, ROOT, service_candidates, upstream
from tools.stoneage_integration17_map09 import FLOORS17, MAP09_PINS


class Map09PetRoomEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pins = {k: v for k, v in PINS.items() if k != 'map07'} | MAP09_PINS
        cls.source = upstream(pins)
        report_path = ROOT / 'research/recovered/STONEAGE-INTEGRATION17-THREE-PET-ROOMS-SOURCE-R1.json'
        cls.report = json.loads(report_path.read_bytes())
        cls.pins = {k: v[1] for k, v in pins.items()}

    def test_replayed_rooms_and_endpoint_dat_match_both_original_catalogues(self):
        report = self.report
        self.assertEqual(report['upstream_git_blobs'], self.pins)
        self.assertEqual(tuple(map(int, report['rooms'])), FLOORS17)
        self.assertEqual(report['map09_archive'],
                         {k: self.source['map09_custody'][k] for k in ('bytes', 'sha256', 'members')})
        members = report['server_RAR_members_rechecked']
        self.assertEqual(set(members), {'1403', '3103', '3203', 'mapwarp.txt'})
        self.assertEqual(members['mapwarp.txt']['sha256'], self.source['map01']['mapwarp']['source_sha256'])
        for floor, room in report['rooms'].items():
            self.assertTrue(members[floor]['archive_path'].endswith('/' + floor))
            self.assertEqual({k: members[floor][k] for k in room['ls2map']}, room['ls2map'])
        original = {r[0]: r[1:3] for r in self.source['map04']['per_floor_source_rows']}
        for floor, room in report['rooms'].items():
            prior = self.source['map09']['maps'][floor]
            replay = report['room_replay'][floor]
            self.assertEqual([room['dat']['bytes'], room['dat']['sha256']], original[floor + '.dat'])
            self.assertEqual(room['dat']['sha256'], prior['source_sha256'])
            self.assertEqual(room['canvas']['rgba_sha256'], prior['frame_RGBA_sha256']['combined'])
            self.assertEqual(replay['frame_RGBA_sha256'], prior['frame_RGBA_sha256'])
            self.assertEqual(replay['draw_positions'], prior['draw_positions'])
            self.assertEqual(len(replay['image_aliases']), prior['unique_draw_aliases'])
        self.assertEqual(set(report['village_endpoint_DAT']), {'1400', '3100', '3200'})
        for floor, row in report['village_endpoint_DAT'].items():
            self.assertEqual([row['bytes'], row['sha256']], original[floor + '.dat'])

    def test_six_services_and_static_graphic_sources_are_exact(self):
        graphics = {r['graphic']: r for r in self.report['graphics']}
        self.assertEqual(set(graphics), {16016, 16017, 16019, 16033, 16035, 16209})
        creates = {(r[0], r[1]): r for r in self.source['char']['create_rows']}
        for floor, room in self.report['rooms'].items():
            candidates = list(service_candidates(self.source, int(floor)))
            self.assertEqual(len(room['services']), 2)
            for service, candidate in zip(room['services'], candidates, strict=True):
                path, ordinal, parameter, role, parameter_sha, create_sha, alias = candidate
                self.assertEqual(service['create'], [path, ordinal, create_sha])
                self.assertEqual(service['parameter'], [parameter, parameter_sha])
                self.assertEqual(service['role'], role)
                self.assertEqual(service['graphic'], alias)
                self.assertEqual(service['xy'], creates[path, ordinal][7][:2])
                self.assertEqual(service['graphic_dimensions'], graphics[alias]['dimensions'])
                self.assertEqual(service['graphic_px'], [a+b for a, b in
                                 zip(service['marker_px'], graphics[alias]['signed_adrn_offset'])])
        existing = {r['graphic']: r for r in self.source['world11']['decoded_static_graphics']}
        for alias, graphic in graphics.items():
            if alias in (16016, 16033):
                self.assertEqual(graphic['mode'], 'TWO_DECODERS_ORIGINAL_RD')
                self.assertNotIn(alias, existing)
            else:
                self.assertEqual(graphic['mode'], 'WORLD11_REUSED_ORIGINAL_PNG')
                for key in ('adrn_sha256', 'rd_sha256', 'png_sha256', 'rgba_sha256'):
                    self.assertEqual(graphic[key], existing[alias][key])

    def test_independent_create_routes_confirm_asymmetric_tamtam_door(self):
        self.assertEqual(self.report['original_mapwarp_sha256'], self.source['map01']['mapwarp']['source_sha256'])
        creates = {(r[0], r[1]): r for r in self.source['char']['create_rows']}
        tr = next(r for r in self.source['char']['template_rows'] if r[:2] == ['genout/npcgen.template', 21])
        self.assertEqual(tr[3:5], ['npcgen_warp', 'Warp'])
        expected = {
            '1403': ('genout/warp_y.create', [1497, 1498, 1499, 1500], [115, 116, 117, 118]),
            '3103': ('genout/warp_y2.create', [695, 696, 697], [82, 83, 84]),
            '3203': ('genout/warp_y2.create', [716, 717, 718, 719], [103, 104, 105, 106]),
        }
        for floor, room in self.report['rooms'].items():
            path, lines, ordinals = expected[floor]
            edges = room['warps']
            self.assertEqual([e['line'] for e in edges], lines)
            directions = {(tuple(e['source']), tuple(e['target'])) for e in edges}
            for edge, ordinal in zip(edges, ordinals, strict=True):
                row = creates[path, ordinal]
                self.assertEqual(edge['warp_create'], [path, ordinal, row[4]])
                self.assertEqual(edge['warp_template'], tr[:3])
                self.assertEqual(edge['source'], [row[5], *row[7][:2]])
                local = 'source' if edge['source'][0] == int(floor) else 'target'
                self.assertEqual(edge['room_dat_u16'], edge[local + '_dat_u16'])
                self.assertEqual(edge['reverse_listed'],
                                 (tuple(edge['target']), tuple(edge['source'])) in directions)
        last = self.report['rooms']['3103']['warps'][-1]
        self.assertEqual((last['source'], last['target'], last['reverse_listed']),
                         ([3103, 16, 21], [3100, 44, 69], False))

    def test_tutor_preflight_resolves_the_pinned_original_rd_gaps(self):
        preflight = self.report['tutor_source_preflight']
        pinned = upstream({
            'scene26r2': ('STONEAGE-SCENE26-R2-FOUR-ORIGINAL-PET-TUTOR-ROOMS-SOURCE-R1.json', preflight['scene26_r2_blob']),
            'scene26r3': ('STONEAGE-SCENE26-R3-NPC16122-16127-ORIGINAL-ALIAS-CROSSVERSION-R1.json',
                          preflight['scene26_r3_blob']),
        })
        self.assertTrue(preflight['actual_mixed25_RD_and_RGBA_replayed'])
        self.assertFalse(preflight['placed_in_tutor_rooms'])
        self.assertEqual(preflight['mixed25_spr_matches'], 0)
        graphics = {r['graphic']: r for r in preflight['graphics']}
        self.assertEqual(set(graphics), {16122, 16127})
        for alias, graphic in graphics.items():
            rows = pinned['scene26r3']['derived_original_reference_query']['sources'][str(alias)]['logical_alias_entries']
            self.assertEqual({r['reference']['profile'] for r in rows}, {'CN50', 'PATCH129'})
            self.assertTrue(all(r['content']['rd_sha256'] == graphic['rd_sha256'] for r in rows))
        original = pinned['scene26r2']['source_tutor_four_CREATE_rows']
        for restored, old in zip(preflight['candidate_rooms'], original, strict=True):
            floor = old['source_floor_id']
            self.assertEqual((restored['floor'], restored['xy'], restored['graphic'], restored['dat_sha256']),
                             (floor, old['original_borncenter'], old['original_source_graphicname'],
                              old['original_DAT_whole_sha256']))
            self.assertEqual(restored['frame_RGBA_sha256'], self.source['map09']['maps'][str(floor)]['frame_RGBA_sha256'])

    def test_offline_and_private_acceptance_stays_within_source_scope(self):
        bounds = self.report['bounds']
        for key in ('official_same_deployment', 'original_client_or_server_executed',
                    'native_renderer_or_collision_verified', 'native_storage_or_training_verified',
                    'proprietary_sources_published'):
            self.assertIs(bounds[key], False)
        self.assertIsNone(bounds['overall_percent'])
        self.assertTrue(self.report['private_package']['library_roundtrip_sha256_and_crc_verified'])
        self.assertTrue(self.report['private_generation_byte_for_byte_replay'])
        self.assertTrue(self.report['integration16_legacy_zip_byte_identical'])
        self.assertTrue(self.report['invented_reverse_rejected'])
        self.assertTrue(self.report['substituted_map_tile_rejected'])
        browser = self.report['browser']
        self.assertTrue(browser['exact_zip_index_file_url'])
        self.assertEqual((browser['external_requests'], browser['browser_errors']), (0, 0))
        self.assertEqual([r['floor'] for r in browser['rooms']], list(FLOORS17))
        self.assertEqual(sum(r['warp_rows_visible'] for r in browser['rooms']), 11)


if __name__ == '__main__':
    unittest.main()
