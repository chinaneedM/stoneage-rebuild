"""MAP04 published derived contract tests. CI never reads private original DAT/RD art.

Full original-byte CRC/SHA, RD decoded pixels and candidate PNG integrity were
verified separately in private archival replay. This suite guards counts,
provenance, status boundaries and adversarial metadata corruption.
"""
import collections,copy,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
M01=ROOT/'research/recovered/STONEAGE-MAP-SCENE-MODULE-01-ORIGINAL-SOURCE-MANIFEST-R1.json'
M02=ROOT/'research/recovered/STONEAGE-MAP-SCENE-MODULE-02-THREE-ORIGINAL-DAT-FLOOR-IMAGE-JOIN-R1.json'
M04=ROOT/'research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'
HEX=re.compile(r'^[a-f0-9]{64}$')


def validate(m01,m02,data):
    assert data['schema'].endswith('original_955_verified_DAT_4166_real_TW1_RD_pixels_source_separated.r1')
    prov=data['provenance']; c=data['verified_counts'];b=data['bounds']
    assert prov['original_mixed25_community_RAR_sha256']==m01['original_rar_sha256']
    assert c['source_client_DAT_files_reextracted_from_actual_original_RAR_and_individually_sha_crc_matched']==m01['verified_counts']['client_original_DAT_full_crc_SHA']==971
    assert c['source_nonempty_DAT_files_matching_8_plus_6_cells_formula']==955
    assert c['source_DAT_zero_byte_placeholders']==13
    assert c['source_DAT_two_byte_nonmap_BGM_members']==3
    assert data['not_map_structured_short_or_zero_bytes']['short_two_byte_DAT_names']==['bgm0.dat','bgm1.dat','bgm2.dat']
    assert len(data['not_map_structured_short_or_zero_bytes']['zero_byte_DAT_names'])==13
    assert len(data['per_floor_source_rows'])==955
    assert len(data['source_TW1_real_RD_rows'])==4166
    assert len(data['unmatched_numeric_alias_rows'])==1125
    assert c['distinct_nonzero_numeric_alias_candidates']==4166+1125==5291
    assert c['TW1_ADRN_unique_matched_and_REAL_RD_actual_pixel_decoded_aliases']==4166
    assert c['original_RD_decode_source_format_failures']==0
    assert c['original_RD_distinct_indexed_pixel_sha256_content']==4063
    assert c['source_aliases_unmatched_to_TW1_ADRN']==1125
    assert c['unmatched_aliases_later_ADRN_unique_index_only_no_pixels']==85
    assert c['unmatched_aliases_later_ADRN_ambiguous_index_only_no_pixels']==2
    assert c['unmatched_aliases_absent_from_saved_later_ADRN_index']==1038
    assert c['private_real_RD_source_PNG_candidate_images']==4166
    assert prov['source_private_png_zip_members']==4169
    for sha in (prov['original_TW1_retail_P3H_zip_sha256'],prov['original_TW1_ADRN1_sha256'],prov['original_TW1_REAL1_sha256'],prov['original_TW1_Palet1_sha256'],prov['source_private_png_zip_sha256']):
        assert HEX.fullmatch(sha)

    old={(r[0],r[1].lower()):r for r in m01['original_decoded_source_rows']}
    cols=data['per_floor_source_row_columns'];assert len(cols)==12
    rows=data['per_floor_source_rows']
    assert len({r[0] for r in rows})==955
    assert all(r[0].endswith('.dat') for r in rows)
    assert sum(r[5] for r in rows)==c['original_16bit_cells_in_the_955_usable_DAT_files']==2852551
    assert sum(r[6]+r[7] for r in rows)==c['raw_numeric_nonzero_occurrences_across_first_two_planes']==3082072
    assert sum(r[10] for r in rows)==c['source_numeric_occurrences_with_actual_TW1_RD']==3045772
    assert sum(r[11] for r in rows)==c['source_numeric_occurrences_unmatched_TW1_ADRN']==36300
    for r in rows:
        (name,sz,srcsha,w,h,n,p0,p1,hit,missing,matchedocc,missingocc)=r
        assert old[(0,name)][2]==sz and old[(0,name)][3]==srcsha
        assert HEX.fullmatch(srcsha)
        assert sz==8+6*n and n==w*h and w>0 and h>0
        assert 0<=p0<=n and 0<=p1<=n
        assert matchedocc+missingocc==p0+p1
        assert hit+missing<=p0+p1
        assert 0<=hit<=4166 and 0<=missing<=1125

    rds=data['source_TW1_real_RD_rows']
    assert len(data['source_TW1_real_RD_rows_columns'])==7
    assert len({r[0] for r in rds})==4166
    assert [r[0] for r in rds]==sorted(r[0] for r in rds)
    for alias,pos,w,h,ln,sha,pixelsha in rds:
        assert alias>0 and pos<125996 and pos>=0
        assert w>0 and h>0 and ln>=16
        assert HEX.fullmatch(sha) and HEX.fullmatch(pixelsha)
    assert len({r[-1] for r in rds})==4063
    absent=data['unmatched_numeric_alias_rows']
    assert len(data['unmatched_numeric_alias_rows_columns'])==3
    assert len({r[0] for r in absent})==1125
    assert not {r[0] for r in rds}&{r[0] for r in absent}
    assert sum(r[1] for r in absent)==36300
    status=collections.Counter(r[2] for r in absent)
    assert status=={'LATER_UNIQUE_ADRN_INDEX_ONLY':85,'LATER_MULTIPLE_ADRN_RECORDS_INDEX_ONLY':2,'UNMAPPED_BOTH_SAVED_TW1_AND_LATER_ADRN_INDEXES':1038}
    assert set(r[0] for r in absent if r[2]=='LATER_MULTIPLE_ADRN_RECORDS_INDEX_ONLY')=={4,15999}

    prior={r['alias']:r for r in m02['per_alias_source_bitmap_metadata_rows'] if r.get('original_rd_decoded')}
    overlap=[r for r in rds if r[0] in prior]
    assert len(overlap)==c['MAP02_old_780_source_RD_overlap_exact_original_source_SHA_RGBA_and_PNG']==764
    assert len(rds)-len(overlap)==c['MAP04_actual_RD_aliases_outside_MAP02_prior_pixel_batch']==3402
    assert len(prior)-len(overlap)==c['MAP02_prior_RD_aliases_not_reused_by_MAP04_955_source_DAT']==16
    for alias,pos,w,h,ln,sha,pixelsha in overlap:
        assert prior[alias]['original_rd_sha256']==sha
        assert prior[alias]['rd_width']==w and prior[alias]['rd_height']==h
    for f in ('source_RAR_is_pure_official_original_client',
              'original_TW1_art_automatically_authenticates_later_DAT_floor_membership',
              'candidate_palette_is_proven_original_native_draw_selector',
              'raw_DAT_numeric_alias_is_verified_pet_or_npc_identity',
              'later_RAR_unread_REAL_original_pixels_counted_as_recovered',
              'DAT_map_native_collision_and_original_gameplay_tested',
              'MAP01_63_failed_extractions_reclassified_as_success',
              'source_raster_tiles_or_DAT_original_bytes_in_public_Git'):
        assert b[f] is False,f
    assert b['overall_restoration_percentage'] is None
    assert b['stage_B']=='GATED'
    assert c['original_native_commercial_software_run_and_verified']==0


class TestMap04(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m01=json.loads(M01.read_text());cls.m02=json.loads(M02.read_text());cls.data=json.loads(M04.read_text())
    def test_full_public_derived_contract(self):validate(self.m01,self.m02,self.data)
    def mutate(self,fn):
        d=copy.deepcopy(self.data);fn(d)
        with self.assertRaises(AssertionError):validate(self.m01,self.m02,d)
    def test_no_native_official_deployment_inference(self):
        self.mutate(lambda d:d['bounds'].__setitem__('original_TW1_art_automatically_authenticates_later_DAT_floor_membership',True))
    def test_no_pixel_recovery_from_later_index_only(self):
        self.mutate(lambda d:d['verified_counts'].__setitem__('original_RD_decode_source_format_failures',1))
    def test_zero_DAT_not_arbitrarily_materialized(self):
        self.mutate(lambda d:d['verified_counts'].__setitem__('source_DAT_zero_byte_placeholders',12))
    def test_source_hash_mutation_fails(self):
        self.mutate(lambda d:d['per_floor_source_rows'][0].__setitem__(2,'0'*64))
    def test_original_legacy_MAP02_overlap_must_survive(self):
        self.mutate(lambda d:d['verified_counts'].__setitem__('MAP02_old_780_source_RD_overlap_exact_original_source_SHA_RGBA_and_PNG',780))
    def test_no_force_unique_on_later_duplicate_numeric_alias(self):
        def mutate(d):
            r=next(x for x in d['unmatched_numeric_alias_rows'] if x[0]==15999)
            r[2]='LATER_UNIQUE_ADRN_INDEX_ONLY'
        self.mutate(mutate)
    def test_no_source_counts_from_non_structured_BGM(self):
        self.mutate(lambda d:d['not_map_structured_short_or_zero_bytes']['short_two_byte_DAT_names'].remove('bgm0.dat'))
if __name__=='__main__':unittest.main()
