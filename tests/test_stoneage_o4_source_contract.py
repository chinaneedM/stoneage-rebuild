"""Regression tests for a source-only private-asset O4 research tour.

No original DAT/RD/SAP/CP950 script/image is present or accessed in GitHub CI.
"""
import copy
import json
import unittest
from unittest.mock import patch

from tools import stoneage_o4_source_contract as o4


class SourceIdentityAndHistoricalBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r15,cls.r21,cls.r22,cls.w=o4.evidence()

    def test_full_original_map_overlap_not_visual_guesswork(self):
        a={(tuple(x['source_xy']),x['layer'],x['map_id']) for x in self.r15['views'][1]['placements']}
        b={(tuple(x['xy']),x['layer'],x['image_key']) for x in self.r21['placements'] if x['xy'][1]<=102}
        self.assertEqual(len(a),54)
        self.assertEqual(a,b)
        keys=set(self.r15['resources'])&set(self.r21['resources'])
        self.assertEqual(len(keys),36)
        for k in keys:
            self.assertEqual(self.r15['resources'][k]['PNG_sha256'],self.r21['resources'][k]['PNG_sha256'])
        self.assertEqual(self.r15['views'][1]['source_DAT_sha256'],self.r21['source_map_sha256'])

    def test_both_original_doorways_are_from_create_records_not_fabricated(self):
        self.assertEqual(len(self.r15['doorway_pair']),2)
        for i,x in enumerate(self.r15['doorway_pair']):
            self.assertEqual((x['source_floor'],*x['source_xy']),o4.EXPECTED_DOORS[i][0])
            self.assertEqual((x['destination_floor'],*x['destination_xy']),o4.EXPECTED_DOORS[i][1])
            self.assertEqual(x['source_block']['block_sha256'],self.w['source_create_blocks'][i]['byte_sha256'])

    def test_original_npc_is_static_document_not_runtime(self):
        self.assertEqual(self.r22['message']['bytes'],143)
        self.assertEqual(self.r22['target']['functionset'],'TownPeople')
        self.assertFalse(self.r22['native_dialogue_execution_verified'])
        self.assertFalse(self.w['original_npc_static']['dialogue_game_runtime_executed'])
        self.assertFalse(self.w['historical_limits']['original_game_world_entered'])
        self.assertIsNone(self.w['overall_percent'])

    def test_independent_private_pixel_proof_is_properly_scoped(self):
        r=self.w['independent_actual_pixel_replay']
        self.assertEqual(r['floor_1001_compared_pixel_count'],726455)
        self.assertEqual(r['floor_1000_compared_pixel_count'],716102)
        self.assertEqual(r['total_pixels_compared'],1442557)
        self.assertEqual(r['pixels_diff_gt1'],0)
        self.assertEqual(self.w['source_actual_replay']['original_image_subresources_loaded_in_Chromium'],67)
        self.assertTrue(self.w['ci_public_gate_never_reads_private_originals'])
        self.assertFalse(self.w['private_output']['original_png_dat_rd_or_script_text_in_git'])

    def test_private_source_archive_manifest_has_no_original_content(self):
        z=self.w['input_original_private_archives']
        self.assertEqual(len(z),4)
        self.assertEqual([x['size'] for x in z],[529126,2745658,1321290,2078427])
        self.assertEqual(len(set(x['sha256'] for x in z)),4)
        self.assertTrue(all(len(x['sha256'])==64 for x in z))
        self.assertTrue(self.w['private_output']['saved_private_library_path'].startswith('/石器时代/'))
        self.assertEqual(self.w['private_output']['zip_files'],12)

    def test_negative_tampered_original_source_map_must_be_refused(self):
        r21=copy.deepcopy(self.r21)
        r21['source_map_sha256']='0'*64
        base=json.loads
        with patch.object(o4.json,'loads',side_effect=[copy.deepcopy(self.r15),r21,copy.deepcopy(self.r22),copy.deepcopy(self.w)]):
            with self.assertRaisesRegex(ValueError,'map byte witnesses disagree'):
                o4.evidence()

    def test_negative_tampered_private_browser_proof_must_be_refused(self):
        w=copy.deepcopy(self.w)
        w['independent_actual_pixel_replay']['pixels_diff_gt1']=1
        with patch.object(o4.json,'loads',side_effect=[copy.deepcopy(self.r15),copy.deepcopy(self.r21),copy.deepcopy(self.r22),w]):
            with self.assertRaisesRegex(ValueError,'browser/Pillow'):
                o4.evidence()

    def test_negative_native_execution_false_promotion_must_be_refused(self):
        w=copy.deepcopy(self.w)
        w['historical_limits']['original_game_world_entered']=True
        with patch.object(o4.json,'loads',side_effect=[copy.deepcopy(self.r15),copy.deepcopy(self.r21),copy.deepcopy(self.r22),w]):
            with self.assertRaisesRegex(ValueError,'historical claim promoted'):
                o4.evidence()


class ModernResearchCursor(unittest.TestCase):
    def test_complete_bounded_two_way_tour(self):
        c=o4.Cursor()
        self.assertEqual(c.location,(1001,11,15))
        c=o4.manual_step(c,-1,0)
        self.assertEqual(c.location,(1001,10,15))
        c=o4.manual_warp(c)
        self.assertEqual(c.location,(1000,63,99))
        self.assertFalse(o4.can_inspect_original_document(c))
        for i in range(4):
            c=o4.manual_step(c,0,1)
        self.assertEqual(c.location,(1000,63,103))
        self.assertTrue(o4.can_inspect_original_document(c))
        for i in range(4):
            c=o4.manual_step(c,0,-1)
        c=o4.manual_warp(c)
        self.assertEqual(c.location,(1001,10,15))
        self.assertEqual(len(c.journal),2)
        self.assertTrue(all(j[2]=='MANUAL_APPLICATION_NOT_ORIGINAL_GAMEPLAY' for j in c.journal))

    def test_no_autowarp_when_arriving_at_exact_destination(self):
        c=o4.manual_warp(o4.Cursor(1001,10,15))
        self.assertEqual(c.location,(1000,63,99))
        self.assertEqual(len(c.journal),1)
        self.assertEqual(c,o4.Cursor(1000,63,99,c.journal))

    def test_neighbor_door_wrong_or_out_of_window_rejected(self):
        for c in (o4.Cursor(),o4.Cursor(1001,10,16),o4.Cursor(1000,63,100),o4.Cursor(1000,63,103)):
            with self.assertRaisesRegex(ValueError,'no certified source doorway'):
                o4.manual_warp(c)
        with self.assertRaisesRegex(ValueError,'original image sample window'):
            o4.manual_step(o4.Cursor(1000,66,103),1,0)
        with self.assertRaisesRegex(ValueError,'original image sample window'):
            o4.manual_step(o4.Cursor(1001,7,15),-1,0)

    def test_manual_movement_refuses_teleport_diagonal_float_and_invalid_floor(self):
        for xy in ((2,0),(1,1),(0,0),(1.0,0),(-2,0)):
            with self.assertRaisesRegex(ValueError,'modern single-grid'):
                o4.manual_step(o4.Cursor(),*xy)
        with self.assertRaisesRegex(ValueError,'unsourced floor'):
            o4.manual_step(o4.Cursor(9999,2,2),1,0)

    def test_original_static_NPC_document_is_only_at_exact_cell(self):
        self.assertFalse(o4.can_inspect_original_document(o4.Cursor(1000,63,102)))
        self.assertFalse(o4.can_inspect_original_document(o4.Cursor(1001,63,103)))
        self.assertTrue(o4.can_inspect_original_document(o4.Cursor(1000,63,103)))


if __name__=='__main__':
    unittest.main()
