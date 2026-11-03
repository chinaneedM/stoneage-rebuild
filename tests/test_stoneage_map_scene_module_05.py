"""MAP05 original-source derived-only assertions.

Original commercial DAT/REAL/RD/private PNG are NEVER in this public CI.
These tests protect published source qualification, counts and negative claims.
"""
import copy,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'research/recovered'
M02=D/'STONEAGE-MAP-SCENE-MODULE-02-THREE-ORIGINAL-DAT-FLOOR-IMAGE-JOIN-R1.json'
M04=D/'STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'
M05=D/'STONEAGE-MAP-SCENE-MODULE-05-SOURCE-WINDOW-OBSERVATION-R1.json'
HEX=re.compile(r'^[0-9a-f]{64}$')
EXPECTED_UNRESOLVED=[11208,22413,24305,24306,24307,24308,24309,24310,24311,24312,24316,24322]


def validate(a,b,c):
    assert c['schema'].endswith('private_original_DAT_cells_to_real_RD_image_candidate_observation.r1')
    assert c['original_map1000_and_1001_bytes_checked_against_MAP02_source_floors']
    assert c['MAP04_private_real_pixel_ZIP_sha256']==b['provenance']['source_private_png_zip_sha256']
    assert c['MAP04_real_RD_source_bitmap_receipts_count']==4166
    assert c['private_source_PNG_SHA256_and_RGBA_replay_per_used_alias']==497
    assert c['private_original_pixel_content_added']==0
    assert c['private_artifact_member_count']==18
    assert c['private_artifact_bytes']==14774654
    assert HEX.fullmatch(c['private_artifact_sha256'])
    fs={x['source_floor_id']:x for x in c['source_floors']}
    assert set(fs)=={1000,1001}
    assert [(fs[x]['source_width'],fs[x]['source_height']) for x in (1000,1001)]==[(160,160),(30,30)]
    assert fs[1000]['original_DAT_source_sha256']==a['source_three_floors']['1000']['dat_sha256']
    assert fs[1001]['original_DAT_source_sha256']==a['source_three_floors']['1001']['dat_sha256']
    assert fs[1001]['original_DAT_source_sha256']==next(v[2] for v in b['per_floor_source_rows'] if v[0]=='1001.dat')
    assert fs[1000]['original_DAT_bytes']==8+6*fs[1000]['source_cells']
    assert fs[1001]['original_DAT_bytes']==8+6*fs[1001]['source_cells']
    assert fs[1000]['source_cells']==25600 and fs[1001]['source_cells']==900
    assert fs[1000]['first_two_plane_nonzero_numeric_references']==26324
    assert fs[1000]['MAP04_real_RD_covered_references']==26290
    assert fs[1000]['MAP02_and_MAP04_real_RD_covered_references']==26310
    assert fs[1000]['unmatched_reference_occurrences']==14
    assert fs[1000]['unmatched_unique_aliases']==EXPECTED_UNRESOLVED
    assert fs[1000]['numeric_references_alias_1_to_99_not_rendered_as_original_scene']==1578
    assert fs[1001]['first_two_plane_nonzero_numeric_references']==948
    assert fs[1001]['MAP04_real_RD_covered_references']==948
    assert fs[1001]['MAP02_and_MAP04_real_RD_covered_references']==948
    assert fs[1001]['unmatched_reference_occurrences']==0
    assert fs[1001]['unmatched_unique_aliases']==[]
    assert fs[1001]['numeric_references_alias_1_to_99_not_rendered_as_original_scene']==815
    for f in fs.values():
        assert f['MAP04_real_RD_covered_references']<=f['MAP02_and_MAP04_real_RD_covered_references']
        assert f['MAP02_and_MAP04_real_RD_covered_references']+f['unmatched_reference_occurrences']==f['first_two_plane_nonzero_numeric_references']
        assert 0<=f['numeric_references_alias_1_to_99_not_rendered_as_original_scene']<=f['MAP02_and_MAP04_real_RD_covered_references']
        assert HEX.fullmatch(f['original_DAT_source_sha256'])
    expected=[('1000-northwest-new',1000,[0,0,31,31],1025,0),('1000-gap-cluster',1000,[74,74,105,105],1178,14),('1000-southeast-new',1000,[110,110,141,141],1060,0),('1000-o29-overlap-baseline',1000,[48,92,72,132],1260,0),('1001-complete-source-window',1001,[0,0,29,29],948,0)]
    assert len(c['observation_windows'])==len(expected)
    for q,(name,f,rect,total,missing) in zip(c['observation_windows'],expected):
        assert (q['window'],q['floor'],q['source_coordinate_rect'],q['two_plane_numeric_nonzero_references'],q['source_unmatched_references'])==(name,f,rect,total,missing)
        assert q['cells']==(rect[2]-rect[0]+1)*(rect[3]-rect[1]+1)
        assert q['original_DAT_sha256']==fs[f]['original_DAT_source_sha256']
        assert q['source_qualified_RD_covered_in_union']+missing==total
        assert q['source_qualified_actual_TW1_RD_references']<=q['source_qualified_RD_covered_in_union']
        assert 0<=q['numeric_references_alias_1_to_99_not_rendered']<=q['source_qualified_RD_covered_in_union']
        assert ('unmatched_cell_coordinates_private_only' not in q)
    assert c['observation_windows'][1]['unmatched_aliases']==EXPECTED_UNRESOLVED
    assert c['observation_windows'][1]['unmatched_references_per_alias']
    assert sum(v[1] for v in c['observation_windows'][1]['unmatched_references_per_alias'])==14
    bnds=c['bounds']
    for k in ('native_original_client_started','native_original_server_started','source_later_map_and_retail_TW1_same_deployment_proven','actual_original_scene_rendering_proven','original_collision_layer_semantics_proven','source_original_bytes_embedded_in_public_report','source_proprietary_original_pixels_embedded_in_public_Git'):
        assert bnds[k] is False,k
    assert bnds['candidate_compositing_uses_modern_32x24_grid_not_native_engine'] is True
    assert bnds['source_geometry_fallback_offsets_are_hypothetical'] is True
    assert c['next'].startswith('MAP_MODULE_SOURCE_BOUNDED_PARTIAL')
    assert 'ITEM_EQUIPMENT_SHOP_MODULE_01' in c['next']

class Map05SourceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=json.loads(M02.read_text());cls.b=json.loads(M04.read_text());cls.c=json.loads(M05.read_text())
    def test_exact_published_derivation(self):validate(self.a,self.b,self.c)
    def test_reject_relabel_unmatched_as_recovered(self):
        d=copy.deepcopy(self.c);d['source_floors'][0]['unmatched_reference_occurrences']=0
        with self.assertRaises(AssertionError):validate(self.a,self.b,d)
    def test_reject_non_source_M02_DAT(self):
        d=copy.deepcopy(self.c);d['source_floors'][0]['original_DAT_source_sha256']='f'*64
        with self.assertRaises(AssertionError):validate(self.a,self.b,d)
    def test_reject_same_deployment_promotion(self):
        d=copy.deepcopy(self.c);d['bounds']['source_later_map_and_retail_TW1_same_deployment_proven']=True
        with self.assertRaises(AssertionError):validate(self.a,self.b,d)
    def test_reject_original_scene_or_client_execution_claims(self):
        for key in ('actual_original_scene_rendering_proven','native_original_client_started'):
            d=copy.deepcopy(self.c);d['bounds'][key]=True
            with self.assertRaises(AssertionError):validate(self.a,self.b,d)
    def test_reject_fictional_glyph_restoration(self):
        d=copy.deepcopy(self.c);d['private_original_pixel_content_added']=12
        with self.assertRaises(AssertionError):validate(self.a,self.b,d)
    def test_reject_low_numeric_selector_promotion(self):
        d=copy.deepcopy(self.c);d['source_floors'][1]['numeric_references_alias_1_to_99_not_rendered_as_original_scene']=0
        with self.assertRaises(AssertionError):validate(self.a,self.b,d)
    def test_reject_source_byte_leak_into_public(self):
        d=copy.deepcopy(self.c);d['bounds']['source_proprietary_original_pixels_embedded_in_public_Git']=True
        with self.assertRaises(AssertionError):validate(self.a,self.b,d)

if __name__=='__main__':unittest.main()
