"""Copyright-safe source-boundary and mutation tests for finite SCENE29 evidence."""
import copy
import json
import struct
import unittest
from tools import stoneage_scene29_tw10_battle_pet as src

class SourceIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=src.check_public()

    def mutate(self, fn):
        r=copy.deepcopy(self.original)
        fn(r)
        with self.assertRaises(ValueError):src.check_public(r)

    def test_real_published_source_report_and_derived_three_sab(self):
        r=self.original
        self.assertEqual([m['index'] for m in r['sab_maps']],[0,100,145])
        self.assertEqual(r['source_sab_cell_occurrences'],1200)
        self.assertEqual(sum(m['cells'] for m in r['sab_maps']),1200)
        self.assertEqual(len({x for m in r['sab_maps'] for x in m['unique_tile_bitmap_ids']}),158)
        self.assertTrue(all('grid' not in m and m['original_grid_layout_publicly_included'] is False for m in r['sab_maps']))
        self.assertEqual(r['original_rd_decoded'],158)
        self.assertEqual(r['pet_source']['unique_pet_bitmaps'],48)

    def test_mutated_private_source_grid_digest_refused(self):
        self.mutate(lambda r:r['sab_maps'][0].__setitem__('original_grid_payload_sha256','0'*64))

    def test_original_grid_position_payload_is_not_published(self):
        self.assertFalse(self.original['original_tile_position_payload_publicly_included'])
        self.mutate(lambda r:r.__setitem__('original_tile_position_payload_publicly_included',True))
        self.mutate(lambda r:r['sab_maps'][0].__setitem__('grid',[[100]*20]*20))

    def test_false_map_identity_not_accepted(self):
        self.mutate(lambda r:r['sab_maps'][1].__setitem__('index',0))

    def test_swapped_original_source_sha_rejected(self):
        self.mutate(lambda r:r['sab_maps'][0].__setitem__('sha256',r['sab_maps'][2]['sha256']))

    def test_adulterated_original_container_slice_rejected(self):
        self.mutate(lambda r:r['sab_maps'][2].__setitem__('battle_container_slice_offset',0))

    def test_missing_original_RD_bitmap_disallowed(self):
        self.mutate(lambda r:r['unique_tile_bitmaps'].pop())

    def test_fabricated_runtime_world_is_never_accepted(self):
        self.mutate(lambda r:r.__setitem__('original_game_world_entered',True))
        self.mutate(lambda r:r.__setitem__('original_battle_sab_selected_at_runtime',True))
        self.mutate(lambda r:r.__setitem__('native_battle_actor_placement_verified',True))
        self.mutate(lambda r:r.__setitem__('original_executable_executed_in_this_package',True))

    def test_private_manual_observation_must_be_real(self):
        self.mutate(lambda r:r['private_chromium_observation_receipt'].__setitem__('network_requests',1))
        self.mutate(lambda r:r['private_chromium_observation_receipt'].__setitem__('page_errors',1))
        self.mutate(lambda r:r['private_chromium_observation_receipt'].__setitem__('checks_passed',0))

    def test_foreign_pet_or_action_identity_not_promoted(self):
        self.mutate(lambda r:r['pet_source'].__setitem__('pet_role','ORIGINAL_BATTLE_ACTOR'))
        self.mutate(lambda r:r.__setitem__('original_pet_species_verified',True))
        self.mutate(lambda r:r.__setitem__('original_action1_semantics_verified',True))

    def test_original_image_palette_flags_stay_unproved(self):
        self.mutate(lambda r:r.__setitem__('native_battle_palette_verified',True))
        self.mutate(lambda r:r['provenance'].__setitem__('selected_map_runtime_witness','guessed'))
        self.mutate(lambda r:r.__setitem__('proprietary_art_published_in_git',True))

    def test_actual_source_pixel_geometry_summary(self):
        self.mutate(lambda r:r['unique_tile_bitmaps'][0].__setitem__('decoded_pixel_bytes',6))
        self.mutate(lambda r:r.__setitem__('original_rd_total_encoded_bytes',0))

    def test_bad_sab_envelope_and_length(self):
        with self.assertRaises(ValueError):src.validate_map(b'BAD '+b'\0'*800,0)
        with self.assertRaises(ValueError):src.validate_map(b'SAB '+b'\0'*799,0)
        self.assertEqual(src.validate_map(b'SAB '+b'\0'*800,0),[[0]*20 for _ in range(20)])

    def test_rle_independent_decoder_actual_conventions(self):
        def block(raw):return b'RD\x01\x00'+struct.pack('<iiI',3,2,16+len(raw))+raw
        # literal 0x02 (A B), repetition 0x82 (C C), zeros 0xC2
        self.assertEqual(src.alternate_rle(block(bytes([0x02,65,66,0x82,67,0xC2])),3,2),b'ABCC\0\0')
        # Original allows a literal of length 6; 20-bit count has prefix 0x20
        self.assertEqual(src.alternate_rle(block(bytes([0x20,0,6,1,2,3,4,5,6])),3,2),bytes([1,2,3,4,5,6]))
        with self.assertRaises(ValueError):src.alternate_rle(block(bytes([0x82])),3,2)
        with self.assertRaises(ValueError):src.alternate_rle(block(bytes([0xC7])),3,2)
        with self.assertRaises(ValueError):src.alternate_rle(block(bytes([0x01,4])),3,2)

    def test_commercial_archive_not_required_for_public_replay(self):
        self.assertIsNone(self.original['overall_restoration_percentage'])
        self.assertFalse(self.original['original_battle_encounter_link_verified'])
        self.assertEqual(self.original['provenance']['source_SAB_grid_model'],'SOURCE_20X20_BE_U16_CANDIDATE')

if __name__=='__main__':unittest.main()