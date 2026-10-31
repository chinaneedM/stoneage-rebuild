import copy
import json
import unittest
from pathlib import Path
from tools.stoneage_o13_named_sprite_boundary import get_sources, validate

class O13SourceBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources=get_sources()

    def check_bad(self, mutate):
        args=copy.deepcopy(self.sources)
        mutate(args)
        with self.assertRaises((ValueError, AssertionError,KeyError,TypeError)):
            validate(**args)

    def test_original_source_only_contract(self):
        assert validate(**self.sources)['server_rows']==7

    def test_false_official_name_prohibited(self):
        self.check_bad(lambda a: a['o13'].__setitem__('official_tw1_species_join_proven',True))

    def test_missing_duplicate_line_prohibited(self):
        self.check_bad(lambda a: a['o13']['server_occurrences'].pop())

    def test_conflicting_flag_preserved(self):
        self.check_bad(lambda a: a['o13']['server_occurrences'][5].__setitem__('flag_column_38',1))

    def test_copy_name_over_other_version_prohibited(self):
        self.check_bad(lambda a: a['o13']['server_occurrences'][0].__setitem__('name_zh_Hant','官方台湾1.0宠物'))

    def test_sound_index_namespace_mismatch_prohibited(self):
        self.check_bad(lambda a: a['o13'].__setitem__('o12_compiled_sound_number_73','sam_18.wav'))

    def test_animation_positions_cannot_drop_repeated_frames(self):
        self.check_bad(lambda a: a['o13'].__setitem__('prior_O11_ordered_frame_positions',208))

    def test_original_game_execution_false_claim(self):
        self.check_bad(lambda a: a['o13'].__setitem__('historical_game_runtime_executed',True))

    def test_no_unsupported_original_pet_master(self):
        self.check_bad(lambda a: a['o13'].__setitem__('original_pet_master_restored',True))

    def test_no_audio_event_automatic_claim(self):
        self.check_bad(lambda a: a['o13'].__setitem__('actual_sound_event_selected',True))

    def test_no_fabricated_project_percent(self):
        self.check_bad(lambda a: a['o13'].__setitem__('overall_restoration_percent',95))

    def test_wrong_tw1_provenance_rejected(self):
        self.check_bad(lambda a: a['o13']['source_git_blob_pins'].__setitem__('O11_original_TW1_SPR_and_pixel_material','bad'))

    def test_no_false_absence_of_embedded_master(self):
        self.check_bad(lambda a: a['o13']['tw1_private_archive_inventory_actual'].__setitem__('presence_not_proven_absent_embedded_resources',False))

    def test_wrong_animation_segment_rejected(self):
        self.check_bad(lambda a: a['o13']['same_numeric_group_original_spr_full_segment_sha'].__setitem__('100250','bad'))

if __name__=='__main__': unittest.main()
