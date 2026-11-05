"""WORLD20 rights-safe encounter habitat source graph acceptance; no proprietary originals in CI."""
from collections import Counter
from pathlib import Path
import copy, json, re, unittest

ROOT=Path(__file__).resolve().parents[1]
REC=ROOT/'research'/'recovered'
REPORT=REC/'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-20-ENCOUNTER-HABITAT-SOURCE-R1.json'
WORLD15=REC/'STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-15-VILLAGE-EXIT-ENCOUNTER-SOURCE-R1.json'
PET07=REC/'STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json'
HEX=re.compile(r'^[0-9a-f]{64}$')


def verify(d):
    assert d['schema']=='stoneage.stage_a.world20.source_bound_encounter_habitat_batch.r1'
    assert d['source_scope']=='COMMUNITY_MIXED25_PRESERVED_ARCHIVE_STATIC_NOT_VERIFIED_OFFICIAL_DEPLOYMENT'
    assert d['original_archive_sha256']=='d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5'
    counts=d['counts'];source=d['source_files']
    assert {k:(v['size_bytes'],v['sha256']) for k,v in source.items()}=={
       'encount.txt':(43420,'70bbd997d98508a0587df183b5bdd48222ff42db91bf21bea632e0ed6f2fea87'),
       'group1.txt':(70176,'4a02f2a3fa3d2dcf5589d8a2a560313c35d5a0a7e5e0589cc8df5f7df159ea8f'),
       'group.txt':(68201,'58f722822f5bd95070297092d106622f236f54a1cb1ee5865c91d90210295eac'),
       'enemy.txt':(222463,'cc7418d3b6726f1c458fef9e44a24696d05f076b67c62a56ed2293e26ae63bb6'),
       'enemybase.txt':(147750,'1be7d5226798f7abaabe1f1e74aa1533fcd10e3eaf43f6497d63afa91df3e8b7'),
       'setup.cf':(9715,'b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d')}
    assert source['encount.txt']['valid_rows']==660 and source['group1.txt']['valid_rows']==1257
    assert source['enemy.txt']['valid_rows']==2087 and source['enemybase.txt']['valid_rows']==988
    assert len(source['enemy.txt']['excluded_malformed_rows'])==1
    assert len(source['enemybase.txt']['excluded_malformed_rows'])==7
    assert d['setup_selected']=={'encounter':'encount.txt','group':'group1.txt','enemy':'enemy.txt','template':'enemybase.txt'}
    areas,groups,enemies,templates=(d[k] for k in ['source_areas','source_resolved_groups','source_enemy_instances','source_templates'])
    assert [len(x) for x in [areas,groups,enemies,templates]]==[660,688,719,208]
    A={x['id']:x for x in areas}; G={x['id']:x for x in groups}; E={x['id']:x for x in enemies}; T={x['id']:x for x in templates}
    assert len(A)==len(areas) and len(G)==len(groups) and len(E)==len(enemies) and len(T)==len(templates)
    referenced_group_slots=[];seen_group_refs=set();group_slots=[];graphics=set();floor_counts=Counter()
    for a in areas:
        assert a['source_line']>=1 and HEX.fullmatch(a['source_line_sha256'])
        assert len(a['raw_rectangle'])==4 and len(a['raw_fields_6_9'])==4
        floor_counts[a['floor']]+=1
        slots=set()
        for ix,gid,raw_weight,status in a['group_slots']:
            assert ix not in slots and ix in range(10);slots.add(ix)
            assert isinstance(raw_weight,str)
            assert status==('GROUP_FOUND' if gid in G else 'GROUP_MISSING')
            referenced_group_slots.append((gid,status));seen_group_refs.add(gid)
        assert a['distinct_resolved_template_ids']==sorted(set(a['distinct_resolved_template_ids']))
        actual_templates={E[eid]['template'] for group in a['group_slots'] if group[1] in G for _,eid,_,status in G[group[1]]['enemy_slots'] if status=='INSTANCE_FOUND'}
        assert a['distinct_resolved_template_ids']==sorted(actual_templates)
    for g in groups:
        assert g['source_line']>=1 and HEX.fullmatch(g['source_line_sha256']) and len(g['raw_fields_2_3'])==2
        slots=set()
        for ix,eid,weight,status in g['enemy_slots']:
            assert ix in range(10) and ix not in slots;slots.add(ix)
            assert status==('INSTANCE_FOUND' if eid in E else 'INSTANCE_MISSING')
            group_slots.append(eid)
    for e in enemies:
        assert HEX.fullmatch(e['source_line_sha256']) and e['template'] in T
        assert e['template_status']=='TEMPLATE_FOUND'
        assert len(e['raw_level_fields_5_6'])==2
    for t in templates:
        assert HEX.fullmatch(t['source_line_sha256']) and isinstance(t['graphic'],int)
        assert t['raw_petflag'] in (0,1)
        graphics.add(t['graphic'])
        assert t['tw1_pet07_same_numeric_graphic_has_qualified_prior_pixel']==(t['graphic'] in set(d['TW1_pet07_art_qualified']['different_carrier_numeric_candidate_graphic_ids']))
    missing=sorted(seen_group_refs-set(G))
    assert missing==d['missing_group_ids_selected_group1_only'] and len(missing)==31
    assert 799 in missing and d['world15_crosscheck']['group_799_missing_selected_and_backup'] is True
    assert d['world15_crosscheck']['area88_has_group414'] is True
    assert d['world15_crosscheck']['group414_enemy563_template531'] is True
    assert E[563]['template']==531 and any(row[1]==563 for row in G[414]['enemy_slots'])
    assert len(floor_counts)==421 and [[k,v] for k,v in sorted(floor_counts.items())]==d['floor_area_counts']
    assert len(referenced_group_slots)==counts['area_group_slot_occurrences']==1965
    assert len(seen_group_refs)==counts['distinct_referenced_groups']==719
    assert len(groups)==counts['distinct_resolved_groups']==688
    assert sum(status=='GROUP_MISSING' for _,status in referenced_group_slots)==counts['missing_group_slot_occurrences']==39
    assert len(group_slots)==counts['distinct_resolved_group_enemy_slot_occurrences']==1069
    assert len(set(group_slots))==counts['distinct_referenced_enemy_instances']==719
    assert len(templates)==counts['distinct_template_ids']==208
    assert counts['distinct_missing_enemy_instances']==counts['distinct_missing_templates']==0
    assert len(graphics)==counts['distinct_numeric_graphic_ids']==157
    art=d['TW1_pet07_art_qualified']
    assert art['source_public_report_blob']=='0b5f81b41a642025ab53a12884638fdee887470e'
    assert art['certified_TW1_original_P3H_SHA256']=='3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24'
    assert len(art['different_carrier_numeric_candidate_graphic_ids'])==counts['distinct_numeric_graphic_ids_with_prior_TW1_PET07_real_pixel_source']==107
    assert art['different_carrier_numeric_candidate_graphic_ids']==sorted(set(art['different_carrier_numeric_candidate_graphic_ids']))
    assert len(art['private_observer_pinned_thumbnails'])==art['thumbnail_graphics_whose_PNG_SHA_matches_PET07_RD_candidate']==104
    assert set(map(int,art['private_observer_pinned_thumbnails']))<=set(art['different_carrier_numeric_candidate_graphic_ids'])
    for x in art['private_observer_pinned_thumbnails'].values():
        assert isinstance(x['original_bitmap'],int) and HEX.fullmatch(x['png_sha256'])
    assert len(d['inverted_coordinate_area_ids'])==counts['inverted_coordinate_rectangle_original_area_ids']==12
    assert d['inverted_coordinate_area_ids']==[a['id'] for a in areas if a['raw_rectangle'][0]>a['raw_rectangle'][2] or a['raw_rectangle'][1]>a['raw_rectangle'][3]]
    b=d['boundaries']; assert b['stage_A']=='7_PARTIAL_2_OPEN' and b['stage_B_wiki']=='GATED'
    assert b['R79']=='PAUSED_NON_BLOCKING' and b['overall_percent'] is None
    for k,v in b.items():
        if isinstance(v,bool):assert v is False,k
    assert d['next']=='STAGE-A-OFFLINE-WORLD-CONTENT-21_SOURCE_BOUNDED_NEXT_ORIGINAL_QUEST_PET_RELATION'
    return True


class SourceBoundHabitatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.data=json.loads(REPORT.read_text(encoding='utf-8'))
    def test_exact_full_660_area_719_group_replay(self):self.assertTrue(verify(self.data))
    def test_world15_provenance_and_conserved_six_existing_areas(self):
        old=json.loads(WORLD15.read_text(encoding='utf-8'))
        self.assertEqual(old['archive_sha256'],self.data['original_archive_sha256'])
        for filename,member in self.data['source_files'].items():
            if filename in old['verified_members']:
                self.assertEqual(member['sha256'],old['verified_members'][filename]['sha256'])
        areas={x['id']:x for x in self.data['source_areas']}
        for row in old['area_rectangles']:
            if row['id'] in self.data['world15_crosscheck']['area_ids']:
                a=areas[row['id']];self.assertEqual(a['raw_rectangle'],row['rectangle'])
                self.assertEqual(a['source_line_sha256'],row['line_sha256'])
    def test_previous_TW1_actual_sprite_selection_only_cross_carrier(self):
        prior=json.loads(PET07.read_text(encoding='utf-8'))
        graphic={x[0] for x in prior['source_groups']}
        current={x['graphic'] for x in self.data['source_templates']}
        self.assertEqual(sorted(graphic&current),self.data['TW1_pet07_art_qualified']['different_carrier_numeric_candidate_graphic_ids'])
    def test_reject_missing_group_as_real(self):
        d=copy.deepcopy(self.data)
        x=next(x for x in d['source_areas'] if any(z[1]==799 for z in x['group_slots']))
        next(y for y in x['group_slots'] if y[1]==799)[3]='GROUP_FOUND'
        with self.assertRaises(AssertionError):verify(d)
    def test_reject_false_template_reference(self):
        d=copy.deepcopy(self.data);d['source_enemy_instances'][0]['template']=9999999
        with self.assertRaises(AssertionError):verify(d)
    def test_reject_undecoded_graphic_promoted_to_observed(self):
        d=copy.deepcopy(self.data);d['TW1_pet07_art_qualified']['different_carrier_numeric_candidate_graphic_ids'].append(999999)
        with self.assertRaises(AssertionError):verify(d)
    def test_reject_erased_original_inverted_rectangles(self):
        d=copy.deepcopy(self.data);a=next(x for x in d['source_areas'] if x['id']==94)
        a['raw_rectangle']=sorted(a['raw_rectangle'])
        with self.assertRaises(AssertionError):verify(d)
    def test_reject_runtime_encounter_claim(self):
        d=copy.deepcopy(self.data);d['boundaries']['original_encounters_triggered_or_probabilities_verified']=True
        with self.assertRaises(AssertionError):verify(d)
    def test_reject_early_official_misidentification(self):
        d=copy.deepcopy(self.data);d['boundaries']['mixed25_source_certified_as_TW1_or_JSS1999_or_CN182']=True
        with self.assertRaises(AssertionError):verify(d)
    def test_reject_wrong_group_slot_count(self):
        d=copy.deepcopy(self.data);d['counts']['area_group_slot_occurrences']+=1
        with self.assertRaises(AssertionError):verify(d)

if __name__=='__main__':unittest.main()
