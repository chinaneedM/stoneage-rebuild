"""Public metadata replay only; original proprietary sources never enter Git or CI."""
import copy
import hashlib
import json
import pathlib
import unittest
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
OLD_NPC = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
OLD_DAT = ROOT / 'research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'
REPORT = ROOT / 'research/recovered/STONEAGE-INTEGRATION102-MEIRO-17-ORIGINAL-SOURCE-MAP-R1.json'


def git_blob_sha(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def load_checked(path, blob):
    b=path.read_bytes()
    if git_blob_sha(b) != blob:
        raise ValueError('prior public index Git blob changed')
    return json.loads(b)


def verify(report):
    prior = load_checked(OLD_NPC, 'a088b61a3212f7049e7793f587123ffb29bebad7')
    dat = load_checked(OLD_DAT, '1ef8c004179128ea44ffa4fb4259748bc8c83911')
    assert report['provenance']['actual_private_NPC_ZIP_SHA256']=='c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f'
    assert report['provenance']['original_CREATE_SHA256']=='4aac9ba239351b9bdb932fb1f47d58854023afd17d371119718684103c241574'
    assert report['baseline']['original_CURRENT_git_blob']=='c89e0e33537990aa2132b47c40fef49a985a935c'
    src = next(x for x in prior['source_files'] if x[0]=='genout/meiro.create')
    assert src[1]==2246 and src[2]==report['provenance']['original_CREATE_SHA256']
    cols=prior['columns']['create_rows']
    older={x[1]:dict(zip(cols,x)) for x in prior['create_rows'] if x[0]=='genout/meiro.create'}
    rows=report['original_numeric_rows_without_commercial_text']
    assert len(older)==len(rows)==17 and {x['ordinal'] for x in rows}==set(range(17))
    byfloor=Counter(); bytype=Counter()
    handlers={h['path'].removeprefix('npc/'):h for h in report['original_3_handler_full_SHA_without_commercial_text']}
    assert set(handlers)=={'genout/signb_119_99_92','genout/msg_121_23_15','genout/wpm_120_19_15'}
    originalfiles={r[0]:(r[1],r[2]) for r in prior['source_files']}
    for path,h in handlers.items():
        assert originalfiles[path]==(h['original_file_bytes'],h['original_file_SHA256'])
    for r in rows:
        x=older[r['ordinal']]
        assert r['floor']==x['original_floorid_numeric_nullable']
        assert r['position']==x['original_borncorner_int4_nullable'][:2]
        assert x['original_borncorner_int4_nullable'][:2]==x['original_borncorner_int4_nullable'][2:]
        assert r['source_window']==[x['original_start_byte'],x['original_end_byte']]
        assert r['original_window_SHA256']==x['original_config_block_sha256']
        assert r['type']==x['exact_enemy_template_token']
        assert r['graphic_numeric_alias']==x['original_graphicname_numeric_nullable']
        assert r['name_original_utf8_SHA256_or_null']==x['name_original_utf8_sha256_nullable']
        if r['type']!='npcgen_warp':
            ref=r['referenced_handler_path'].removeprefix('npc/')
            assert ref in handlers
            assert x['source_reference_relpath_exact_resolution_and_target_sha256']
            assert handlers[ref]['original_file_SHA256'] in json.dumps(x['source_reference_relpath_exact_resolution_and_target_sha256'])
        else:
            assert len(r['literal_target_floor_xy'])==3
        byfloor[r['floor']]+=1;bytype[r['type']]+=1
    assert {str(k):v for k,v in sorted(byfloor.items())}==report['source_COUNTS']['floors']
    assert dict(bytype)=={'npcgen_warp':14,'npcgen_signboard':1,'npcgen_man':1,'npcgen_warpman':1}
    w=report['warp_only_static_reverse_analysis']['all_original_warp_rows']
    assert len(w)==14 and set(x['ordinal'] for x in w)=={r['ordinal'] for r in rows if r['type']=='npcgen_warp'}
    for e in w:
        r=rows[e['ordinal']]
        assert e['from']==[r['floor'],*r['position']] and e['to']==r['literal_target_floor_xy']
    edges={(tuple(e['from']),tuple(e['to'])) for e in w}
    assert len(edges)==14
    reciprocal=sorted(e['ordinal'] for e in w if (tuple(e['to']),tuple(e['from'])) in edges)
    absent=sorted(set(e['ordinal'] for e in w)-set(reciprocal))
    assert reciprocal==sorted(report['warp_only_static_reverse_analysis']['strict_reciprocal_ordinals'])
    assert absent==sorted(report['warp_only_static_reverse_analysis']['without_strict_reciprocal_ordinals'])==[4,9]
    assert len(reciprocal)==12
    cols=dat['per_floor_source_row_columns']
    existing={int(x[0][:-4]):dict(zip(cols,x)) for x in dat['per_floor_source_rows'] if x[0].endswith('.dat') and x[0][:-4].isdigit()}
    qualified=report['prior_DAT_floor_qualifications']
    assert [x['floor'] for x in qualified]==[118,120,121,122]
    assert sorted(set(byfloor)-set(existing))==report['missing_prior_DAT_source_floor_ids']==[100,119]
    for q in qualified:
        a=existing[q['floor']]
        assert q['prior_original_DAT_SHA256']==a['source_full_file_SHA256']
        assert [q['prior_header_width'],q['prior_header_height']]==[a['original_header_width'],a['original_header_height']]
        assert q['source_CREATE_positions_in_bounds']==byfloor[q['floor']]
        assert q['prior_qualified_TW1_pixel_reference_occurrences']==a['number_of_nonzero_positions_matching_source_qualified_TW1_RD']
        for r in rows:
            if r['floor']==q['floor']:
                assert 0<=r['position'][0]<a['original_header_width']
                assert 0<=r['position'][1]<a['original_header_height']
    assert sum(byfloor[q['floor']] for q in qualified)==10
    assert report['original_warpman_control_literals_only']['WARP_target_floor_xy']==[122,6,5]
    assert report['original_warpman_control_literals_only']['FREE_condition_literal']=='LV>49'
    assert report['original_warpman_control_literals_only']['MONEY_literal']==-1
    limits=report['limits']
    for k in ['native_original_server_Create_spawn_executed','native_game_warp_effect_or_collision_observed','original_early_TW1_JSS1999_CN182_official_identity_proven','prior_MAP04_TW1_candidate_pixels_prove_same_deployment','original_handler_dialogue_published','original_png_DAT_RAR_zip_published','native_return_path_for_unpaired_config_inferred']:
        assert limits[k] is False
    assert limits['overall_completion_percent'] is None


class TestIntegration102(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload=json.loads(REPORT.read_text(encoding='utf-8'))

    def test_positive_source_replay(self):
        verify(self.payload)

    def test_wrong_span_rejected(self):
        p=copy.deepcopy(self.payload);p['original_numeric_rows_without_commercial_text'][0]['source_window'][0]+=1
        with self.assertRaises(AssertionError):verify(p)

    def test_wrong_floor_rejected(self):
        p=copy.deepcopy(self.payload);p['original_numeric_rows_without_commercial_text'][0]['floor']=999
        with self.assertRaises(AssertionError):verify(p)

    def test_false_reverse_rejected(self):
        p=copy.deepcopy(self.payload);p['warp_only_static_reverse_analysis']['without_strict_reciprocal_ordinals']=[]
        with self.assertRaises(AssertionError):verify(p)

    def test_invented_DAT_rejected(self):
        p=copy.deepcopy(self.payload);p['missing_prior_DAT_source_floor_ids']=[100]
        with self.assertRaises(AssertionError):verify(p)

    def test_original_runtime_claim_rejected(self):
        p=copy.deepcopy(self.payload);p['limits']['native_game_warp_effect_or_collision_observed']=True
        with self.assertRaises(AssertionError):verify(p)


if __name__=='__main__':
    unittest.main()
