"""Adversarial checks for complete native frame material and evidence boundaries."""
import copy
import json
import lzma
from pathlib import Path
import unittest
from tools import stoneage_cn5_animation_material_r26 as material
from tools.stoneage_original_animation_lab import reconstruct_group
from tools.stoneage_cn5_animation_r26_sql import verify


class NativeAnimationMaterialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(lzma.decompress(material.REPORT.read_bytes()))

    def group(self):
        g=copy.deepcopy(self.doc['groups'][0])
        return g['source'],[a['source'] for a in g['animations']],{
            a['source']['anim_index']:a['frames'] for a in g['animations']}

    def test_complete_permanent_archive_replays_all_pinned_sources(self):
        summary=material.validate(self.doc)
        self.assertEqual(json.loads(material.SUMMARY.read_bytes()),summary)
        self.assertEqual((summary['animation_occurrences'],summary['frame_occurrences'],summary['physical_bitmaps']),(312,1464,936))

    def test_full_group_reencoding_matches_prior_original_segment_sha(self):
        for group in self.doc['groups']:
            encoded=reconstruct_group(group['source'],[x['source'] for x in group['animations']],
                {x['source']['anim_index']:x['frames'] for x in group['animations']})
            self.assertEqual(len(encoded),6128)
            self.assertEqual(material.fingerprint(encoded)['sha256'],group['source']['segment_sha256'])

    def test_repeated_frame_position_cannot_be_deduplicated(self):
        group,animations,frames=self.group()
        self.assertEqual(frames[0][0]['bmp_no'],frames[0][1]['bmp_no'])
        frames[0].pop(0)
        with self.assertRaises(ValueError):reconstruct_group(group,animations,frames)

    def test_frame_offset_order_group_namespace_or_sentinel_change_rejected(self):
        for key,value in [('offset',0),('frame_index',1),('group_index',0),('sentinel',1)]:
            group,animations,frames=self.group();frames[0][0][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):reconstruct_group(group,animations,frames)

    def test_bitmap_signed_position_and_raw_sound_change_fail_complete_byte_hash(self):
        for key in ['bmp_no','pos_x','pos_y','sound_no']:
            group,animations,frames=self.group();frames[0][0][key]+=1
            with self.subTest(key=key),self.assertRaises(ValueError):reconstruct_group(group,animations,frames)

    def test_direction_action_or_raw_duration_cannot_change(self):
        for key in ['direction','anim_no','duration']:
            group,animations,frames=self.group();animations[0][key]+=1
            with self.subTest(key=key),self.assertRaises(ValueError):reconstruct_group(group,animations,frames)

    def test_group_extent_and_animation_count_must_be_complete(self):
        for key in ['anim_count','end_offset','next_offset']:
            group,animations,frames=self.group();group[key]+=1
            with self.subTest(key=key),self.assertRaises(ValueError):reconstruct_group(group,animations,frames)

    def test_source_byte_mutation_refused(self):
        path=material.CN+'SPR-GROUP-R1.tsv.gz';raw=(material.ROOT/path).read_bytes()
        with self.assertRaises(ValueError):material.check_source(path,raw+b'0')

    def test_complete_shared_assets_and_each_group_exclusive_assets_retained(self):
        s=self.doc['summary']
        self.assertEqual(s['bitmap_group_membership'],{'100700':296,'100701':296,'100702':296,'100700+100701+100702':48})
        self.assertEqual(len(self.doc['shared_bitmap_frame_references']),144)
        self.assertEqual({x['anim_no'] for x in self.doc['shared_bitmap_frame_references']},{12})

    def test_raw_sound_words_keep_exact_group_action_frame_locations(self):
        cues=self.doc['nonzero_raw_sound_word_references']
        first=[x for x in cues if x['direction']==0 and x['anim_no']==0]
        self.assertEqual([(x['spr_no'],x['frame_index'],x['raw_sound_word']) for x in first],
            [(100700,4,10000),(100701,5,3),(100701,6,10002),(100702,5,2),(100702,6,10003)])
        self.assertEqual(len(cues),64)
        self.assertTrue(all(x['event_name'] is None and x['audio_file'] is None and x['heard_or_played'] is False for x in cues))

    def test_independent_sql_full_source_join(self):
        result=verify(self.doc)
        self.assertEqual(result['complete_tw10_bitmap_rows'],125996)
        self.assertEqual(result['complete_cn5_bitmap_rows'],303197)
        self.assertEqual(result['joined_row_sha256'],'fd42796452dea38301a2cb038e08f527c1ad0bd57573768d746fa7f29e378315')

    def test_sql_rejects_corrupted_rd_binding(self):
        doc=copy.deepcopy(self.doc);doc['bitmaps'][0]['source']['rd_block_sha256']='0'*64
        with self.assertRaises(ValueError):verify(doc)

    def test_removed_shared_reference_refused(self):
        doc=copy.deepcopy(self.doc);doc['shared_bitmap_frame_references'].pop()
        with self.assertRaises(ValueError):material.validate(doc)

    def test_unproven_fps_or_tw10_identity_promotion_refused(self):
        for key in ['cn5_duration_unit_or_game_fps_proven','named_character_pet_or_npc_identity_proven',
                    'sound_words_linked_to_audio_files']:
            doc=copy.deepcopy(self.doc);doc['summary']['boundaries'][key]=True
            with self.subTest(key=key),self.assertRaises(ValueError):material.validate(doc)


if __name__=='__main__':unittest.main()
