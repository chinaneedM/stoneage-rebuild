"""PET07 source-derived checks. CI never downloads TW1 protected art or launches game.
The original pixels have been checked separately in an authenticated private source run.
"""
import copy,gzip,csv,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/recovered/STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json'
PREV=ROOT/'research/recovered/STONEAGE-PET-MODULE-06-CONSOLIDATED-VISUAL-COVERAGE-R1.json'
INDEX=ROOT/'research/recovered/tw10-resource-metadata/SPR-GROUP-R1.tsv.gz'
HEX=re.compile(r'^[0-9a-f]{64}$')
def certify(r,prior,source_rows):
 assert r['schema']=='stoneage.pet_module_07_tw10_batched_actual_rd_pixels_source_derived_r1'
 assert '2016_COMMUNITY' in r['source_scope'] and 'NO_NATIVE_GAMEPLAY' in r['source_scope']
 assert r['original_source_zip']['sha256']=='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
 assert r['original_source_member_sha256']['real_1.bin']=='408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13'
 assert r['original_source_member_sha256']['spr_1.bin']=='53d5b2d40453a30fd1569637ebf0db7b3010542b00970ec83af0295a3b3ae31a'
 assert r['original_source_member_sha256']['adrn_1.bin']=='47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8'
 assert r['counts']['PET06_prior_source_groups']==9
 assert r['counts']['TW1_numeric_graphic_candidate_groups_batch']==130
 expected={x[0] for x in prior['graphic_rows'] if x[2][0]>0}
 assert len(expected)==130
 groups=r['source_groups']; assert len(groups)==130 and [g[0] for g in groups]==sorted(expected)
 assert len(set(g[0]for g in groups))==130
 total_frames=0;total_anim=0
 for g in groups:
  no,ix,whole,anims,frames,actions,unique=g
  assert (no,ix) in source_rows
  row=source_rows[(no,ix)]
  assert row['segment_sha256']==whole and HEX.fullmatch(whole)
  assert anims==int(row['anim_count']) and anims>=3
  assert len(actions)==3 and [a[:2] for a in actions]==[[0,0],[2,0],[1,0]]
  assert all(n>=1 and HEX.fullmatch(h) and duration>=0 for action,d,n,h,duration in actions)
  assert frames==sum(a[2]for a in actions)
  assert 1<=unique<=frames
  total_frames+=frames;total_anim+=anims
 assert total_anim==7568 and total_frames==3255
 pix=r['source_actual_pixel_receipts']
 assert len(pix)==2176
 assert [x[0]for x in pix]==sorted({x[0]for x in pix})
 assert all(x[0]>0 and x[1]>=0 and x[4]==1 and 0<x[5]<=400 and 0<x[6]<=400 and x[7]>=1 and all(HEX.fullmatch(x[i]) for i in (2,3,8)) for x in pix)
 bad=r['source_undecodable_actual_RD_blocks'];assert [x['bitmap']for x in bad]==[82729,100249]
 assert len({x['bitmap']for x in bad})==2
 assert not {x['bitmap']for x in bad}&{x[0]for x in pix}
 assert sum(x[7]for x in pix)+sum(x['original_frame_positions'] for x in r['source_renderable_sequences_excluded'])>=3255
 assert {x['graphic']for x in r['source_renderable_sequences_excluded']}=={100266,100401}
 assert r['counts']['source_RD_blocks_not_decodable_without_fabrication']==2
 assert r['counts']['actual_TW1_RD_blocks_redecoded_from_original_source']==2176
 assert r['counts']['source_sequences_with_unrenderable_frame']==2
 assert r['counts']['preexisting_PET06_same_bitmap_id_overlap']==115
 assert r['counts']['cumulative_private_gallery']=={'graphic_keys':130,'source_action_direction_sequences':451,'frame_position_occurrences':3817,'distinct_png_bitmaps':2540}
 assert r['source_validation']['browser_sequence_selectors_checked']==451 and r['source_validation']['browser_verified'] is True
 assert r['source_validation']['browser_error_count']==r['source_validation']['browser_external_network_requests']==0
 assert r['source_validation']['original_client_executed'] is False
 assert r['private_original_image_bytes_in_public_Git'] is False
 assert all(v is False for k,v in r['historical_boundary'].items() if k!='overall_completion_percent')
 assert r['historical_boundary']['overall_completion_percent'] is None
 assert r['private_artifacts']['catalog']['public_git'] is False and r['private_artifacts']['contact']['public_git'] is False
 return True
class TestPet07(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(P.read_text(encoding='utf-8'));cls.prior=json.loads(PREV.read_text(encoding='utf-8'))
  with gzip.open(INDEX,'rt',encoding='utf-8',newline='') as f:
   cls.source_rows={(int(x['spr_no']),int(x['index'])):x for x in csv.DictReader(f,delimiter='\t')}
 def test_full_batch(self):self.assertTrue(certify(self.r,self.prior,self.source_rows))
 def test_reject_early_pet_identity_promotion(self):
  altered=copy.deepcopy(self.r);altered['historical_boundary']['TW1_pet_species_names_authenticated']=True
  with self.assertRaises(AssertionError):certify(altered,self.prior,self.source_rows)
 def test_reject_missing_group(self):
  altered=copy.deepcopy(self.r);altered['source_groups'].pop()
  with self.assertRaises(AssertionError):certify(altered,self.prior,self.source_rows)
 def test_reject_stitched_source_frame_count(self):
  altered=copy.deepcopy(self.r);altered['source_groups'][0][5][0][2]+=1
  with self.assertRaises(AssertionError):certify(altered,self.prior,self.source_rows)
 def test_reject_unjustified_palette(self):
  altered=copy.deepcopy(self.r);altered['historical_boundary']['native_original_color_palette_runtime_proven']=True
  with self.assertRaises(AssertionError):certify(altered,self.prior,self.source_rows)
 def test_reject_fake_clean_rd(self):
  altered=copy.deepcopy(self.r);altered['source_undecodable_actual_RD_blocks']=[]
  with self.assertRaises(AssertionError):certify(altered,self.prior,self.source_rows)
 def test_reject_pixel_sha_tamper(self):
  altered=copy.deepcopy(self.r);altered['source_actual_pixel_receipts'][0][2]='invalid'
  with self.assertRaises(AssertionError):certify(altered,self.prior,self.source_rows)


class TestPet15(unittest.TestCase):
    """Replay selection and motion metadata without distributing the original images."""

    @classmethod
    def setUpClass(cls):
        from tools import stoneage_pet15_tw10_full_motion as pet15

        cls.report = pet15.archived(pet15.REPORT)
        cls.groups = pet15.selected_motion()
        cls.pet15 = pet15

    def test_all_source_sequences_and_frame_positions(self):
        report = self.report
        missing = {int(key) for key in report['unrendered_bitmaps']}
        self.assertEqual(report['groups'], self.pet15.motion_summary(self.groups, missing))
        frames = [frame for group in self.groups for frame in self.pet15.frames_of(group)]
        self.assertEqual((len(self.groups), len(frames), len(set(frames))), (131, 73500, 32155))
        self.assertEqual((report['frame_positions'], report['distinct_original_bitmaps']), (73500, 32155))
        self.assertEqual(sum(group['source_sequences'] for group in report['groups']), 7672)
        self.assertEqual(sum(group['fully_observable_sequences'] for group in report['groups']), 7672)

    def test_backup_candidate_and_configured_table_flag_disagreement(self):
        added, = [group for group in self.groups if not group['prior_pet07']]
        self.assertEqual(added['graphic'], 100400)
        expected = {'enemybase.txt': {574: 0, 600: 0}, 'enemybase2.txt': {574: 1, 600: 1}}
        for table, rows in added['mixed25_same_number_rows'].items():
            self.assertEqual(len(rows), 7)
            by_template = {template: flag for _, template, flag in rows}
            self.assertEqual({template: by_template[template] for template in (574, 600)}, expected[table])

    def test_strict_and_bounded_pixels_stay_separate(self):
        report = self.report
        self.assertEqual(report['source_bitmap_statuses'], {
            self.pet15.STRICT: 32150,
            self.pet15.BOUNDED: 5,
        })
        self.assertEqual(report['bounded_bitmaps'], [82729, 100249, 109890, 113576, 118187])
        self.assertEqual(report['unrendered_bitmaps'], {})
        self.assertEqual(report['prior_pet07_strict_bitmaps_replayed'], 2176)
        self.assertEqual(report['source_archive_sha256'], self.pet15.ZIP_SHA)
        for key in ('actual_source_bitmap_receipts_sha256', 'private_zip_sha256'):
            self.assertRegex(report[key], HEX)
        for key in ('original_client_executed', 'same_historical_deployment_authenticated',
                    'official_pet_identity_authenticated', 'native_palette_or_frame_timing_verified',
                    'proprietary_images_published'):
            self.assertIs(report[key], False)


if __name__ == '__main__':
    unittest.main()
