import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-MAP07-28-ORIGINAL-DAT-SOURCE-SCENE-RECEIPT-R1.json'
INDEX=ROOT/'research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'

def assert_public_consistency(report, index):
    names={1002,1003,1004}|set(range(1101,1106))|set(range(1201,1206))|set(range(1301,1306))|set(range(2001,2006))|set(range(3001,3006))
    assert len(report['maps'])==28 and {r['floor'] for r in report['maps']}==names
    assert len(report['qualified_image_source_rows'])==234
    columns=index['per_floor_source_row_columns']
    maps={r[0]:dict(zip(columns,r)) for r in index['per_floor_source_rows']}
    images={r[0]:r for r in index['source_TW1_real_RD_rows']}
    for m in report['maps']:
        row=maps[str(m['floor'])+'.dat']
        assert m['source_dat_sha256']==row['source_full_file_SHA256']
        assert m['source_dat_bytes']==row['source_file_bytes']==5408
        assert m['source_map_geometry']==[30,30]
        assert m['modern_candidate_draw_positions']+m['source_low_numeric_nonzero_not_rendered']==row['first_plane_nonzero_numeric_occurrences']+row['second_plane_nonzero_numeric_occurrences']
        assert row['number_of_nonzero_positions_missing_source_qualified_TW1_RD']==0
        assert m['distinct_modern_candidate_numeric_aliases']<=row['first_two_planes_unique_aliases_with_unique_TW1_index_and_actual_RD_pixels']
        assert m['modern_candidate_canvas_size']==[1889,1425]
        assert m['independent_RGBA_canvas_verified'] is True
    assert sum(m['modern_candidate_draw_positions'] for m in report['maps'])==4408
    assert sum(m['source_low_numeric_nonzero_not_rendered'] for m in report['maps'])==21510
    assert sum(m['source_dat_bytes'] for m in report['maps'])==151424
    assert len({m['source_dat_sha256'] for m in report['maps']})==28
    assert len({r['alias'] for r in report['qualified_image_source_rows']})==234
    for row in report['qualified_image_source_rows']:
        original=images[row['alias']]
        assert (row['original_ADRN_index'],row['width'],row['height'],row['original_RD_sha256'],row['source_indexed_pixel_sha256'])==(original[1],original[2],original[3],original[5],original[6])
    assert report['source_mixed25_parent_carrier']['sha256']==index['provenance']['original_mixed25_community_RAR_sha256']
    assert report['source_TW10_archived_pixel_candidates']['archive_sha256']==index['provenance']['source_private_png_zip_sha256']
    assert report['source_TW10_archived_pixel_candidates']['ADRN1_original_sha256']==index['provenance']['original_TW1_ADRN1_sha256']
    assert len(report['source_actions'])==2 and all(x['conclusion']=='success' for x in report['source_actions'])
    assert report['summary']['private_scene_PNG_count']==84
    assert report['summary']['new_original_RD_decodes']==0
    assert report['private_deliverable']['members']==351
    assert report['private_deliverable']['durable_Library_custody_reconfirmed'] is True
    custody=report['private_deliverable']['library_roundtrip']
    assert custody['subsequent_exported_snapshot_upload']=='succeeded'
    assert custody['independently_downloaded_back'] is True
    assert custody['downloaded_bytes']==report['private_deliverable']['bytes']==34044818
    assert custody['downloaded_sha256']==report['private_deliverable']['sha256']
    assert custody['downloaded_zip_members']==report['private_deliverable']['members']==351
    assert custody['downloaded_zip_crc_passed'] is True
    assert all(value is False for value in report['boundaries'].values())
    assert report['overall_percent'] is None and report['stage_B']=='GATED' and report['wiki']=='GATED'

class Map07(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads(REPORT.read_bytes())
        cls.i=json.loads(INDEX.read_bytes())
    def test_exact_origins_and_conservation(self):
        assert_public_consistency(self.r,self.i)
    def test_reject_forged_native_execution(self):
        r=json.loads(json.dumps(self.r));r['boundaries']['native_original_client_execution_verified']=True
        with self.assertRaises(AssertionError):assert_public_consistency(r,self.i)
    def test_reject_changed_source_sha(self):
        r=json.loads(json.dumps(self.r));r['maps'][0]['source_dat_sha256']='0'*64
        with self.assertRaises(AssertionError):assert_public_consistency(r,self.i)
    def test_reject_hiding_unrendered_source_values(self):
        r=json.loads(json.dumps(self.r));r['maps'][1]['source_low_numeric_nonzero_not_rendered']=0
        with self.assertRaises(AssertionError):assert_public_consistency(r,self.i)
    def test_reject_invented_RD_fingerprint(self):
        r=json.loads(json.dumps(self.r));r['qualified_image_source_rows'][0]['original_RD_sha256']='invented'
        with self.assertRaises(AssertionError):assert_public_consistency(r,self.i)
    def test_reject_omitted_verified_Library_custody(self):
        r=json.loads(json.dumps(self.r));r['private_deliverable']['durable_Library_custody_reconfirmed']=False
        with self.assertRaises(AssertionError):assert_public_consistency(r,self.i)
    def test_reject_false_source_lineage(self):
        r=json.loads(json.dumps(self.r));r['source_mixed25_parent_carrier']['sha256']='fake'
        with self.assertRaises(AssertionError):assert_public_consistency(r,self.i)

if __name__=='__main__':
    unittest.main()
