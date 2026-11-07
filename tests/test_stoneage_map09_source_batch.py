"""Conservation and evidence-boundary checks; public CI never receives original grids."""
import copy
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research/recovered'


def validate(report,index,gaps,browser):
    rows={r[0][:-4]:dict(zip(index['per_floor_source_row_columns'],r)) for r in index['per_floor_source_rows']}
    ready={key for key,row in rows.items() if row['number_of_nonzero_positions_missing_source_qualified_TW1_RD']==0}
    assert len(ready)==691 and set(report['maps'])==ready
    assert report['verified_maps']==691 and report['verified_full_canvas_states']==2073
    assert all(value is False for value in report['boundaries'].values())
    assert report['stage_A']=='7_PARTIAL_2_OPEN' and report['stage_B']==report['wiki']=='GATED' and report['overall_percent'] is None
    assert report['new_original_RD_decodes']==0
    assert report['original_DAT_archive']=={'bytes':1988312,'sha256':'c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a','members':955}
    assert report['original_pixel_archive']['sha256']==index['provenance']['source_private_png_zip_sha256']
    available={r[0] for r in index['source_TW1_real_RD_rows']}
    assert len(set(report['qualified_image_aliases']))==report['qualified_images']
    assert set(report['qualified_image_aliases'])<=available
    for floor,item in report['maps'].items():
        old=rows[floor]
        assert (item['source_bytes'],item['source_sha256'])==(old['source_file_bytes'],old['source_full_file_SHA256'])
        assert item['geometry']==[old['original_header_width'],old['original_header_height']]
        assert item['draw_positions']+item['low_nonzero_not_rendered']==old['first_plane_nonzero_numeric_occurrences']+old['second_plane_nonzero_numeric_occurrences']
        assert item['independent_all_three_frames_equal'] is True
        assert set(item['frame_RGBA_sha256'])=={'combined','plane0','plane1'}
        assert all(re.fullmatch('[0-9a-f]{64}',x) for x in item['frame_RGBA_sha256'].values())
    excluded=gaps['excluded_maps']
    assert len(excluded)==264 and {key[:-4] for key in excluded}==set(rows)-ready
    assert sum(row['unqualified_gt99_occurrences']==0 for row in excluded.values())==60
    assert sum(row['unqualified_gt99_occurrences']>0 for row in excluded.values())==204
    assert len(gaps['unqualified_gt99_alias_totals'])==1114
    assert sum(gaps['unqualified_gt99_alias_totals'].values())==29748
    for name,row in excluded.items():
        assert row['source_sha256']==rows[name[:-4]]['source_full_file_SHA256']
        assert row['unqualified_gt99_occurrences']==sum(row['unqualified_gt99_alias_occurrences'].values())
        assert all(int(key)>99 and int(key) not in available for key in row['unqualified_gt99_alias_occurrences'])
    assert browser['scope']=='SYNTHETIC_ONLY_NO_ORIGINAL_ASSETS' and browser['transport']=='LOOPBACK_HTTP_SYNTHETIC_FIXTURE'
    assert browser['all_RGBA_hashes_equal'] is True and browser['full_frame_states']==len(browser['frames'])==9
    assert browser['JS_errors']==browser['external_requests']==[]
    assert browser['actual_original_assets_browser_executed'] is False and browser['original_client_executed'] is False
    return True


class SourceBatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((REC/'STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json').read_bytes())
        cls.i=json.loads((REC/'STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json').read_bytes())
        cls.g=json.loads((REC/'STONEAGE-MAP09-264-EXCLUDED-SOURCE-GAPS-R1.json').read_bytes())
        cls.b=json.loads((REC/'STONEAGE-MAP09-SYNTHETIC-BROWSER-R1.json').read_bytes())

    def test_originals_and_all_qualified_maps_conserve(self): self.assertTrue(validate(self.r,self.i,self.g,self.b))
    def test_reject_omitted_map(self):
        r=copy.deepcopy(self.r);r['maps'].pop(next(iter(r['maps'])))
        with self.assertRaises(AssertionError):validate(r,self.i,self.g,self.b)
    def test_reject_source_hash_drift(self):
        r=copy.deepcopy(self.r);next(iter(r['maps'].values()))['source_sha256']='0'*64
        with self.assertRaises(AssertionError):validate(r,self.i,self.g,self.b)
    def test_reject_original_browser_promotion(self):
        b=copy.deepcopy(self.b);b['actual_original_assets_browser_executed']=True
        with self.assertRaises(AssertionError):validate(self.r,self.i,self.g,b)
    def test_reject_native_collision_promotion(self):
        r=copy.deepcopy(self.r);r['boundaries']['native_collision_verified']=True
        with self.assertRaises(AssertionError):validate(r,self.i,self.g,self.b)
    def test_reject_conflating_low_values_with_visible_missing_images(self):
        g=copy.deepcopy(self.g);next(x for x in g['excluded_maps'].values() if x['unqualified_gt99_occurrences']==0)['unqualified_gt99_occurrences']=1
        with self.assertRaises(AssertionError):validate(self.r,self.i,g,self.b)


if __name__=='__main__':unittest.main()
