"""CHAR09: independently replay public NPCEnemy numeric links against CHAR01/PET10.

The public test checks only source-derived metadata; the original RAR, NPC text,
SPR payload, sprites and runtime execution are not delivered to CI.
"""
import copy
import json
import unittest
from collections import Counter
from pathlib import Path

REC = Path(__file__).resolve().parents[1] / 'research' / 'recovered'


def load(name):
    return json.loads((REC / name).read_text(encoding='utf-8'))


def verify(out, char01, char04, pet):
    assert out['schema'] == 'stoneage.char09.npcenemy_source_and_enemy_table_spr_numeric_join.r1'
    assert out['original_rar_sha256'] == char01['original_rar_sha256'] == pet['preserved_original_rar']['sha256']
    assert out['original_npc_tree_source_count'] == len(char01['source_files']) == 2205
    assert len(char01['create_rows']) == len(char04['create_source_rows']) == 4985
    assert len(out['create_refs']) == 279
    assert len(out['argument_files']) == 260
    assert len(out['source_enemy_number_to_paired_template_and_spr']) == 230
    assert len(out['original_spradrn_5_byte_custody']['duplicate_numeric_keys']) == 5
    assert out['original_spradrn_5_byte_custody']['record_count'] == 847
    assert out['original_spradrn_5_byte_custody']['distinct_graphic_numbers'] == 841
    assert out['original_spradrn_5_byte_custody']['sha256'] == '5f13c956cf013e073298ab91667d3aaa17767b26ba94d696514726950ce94de6'
    for name in ('enemy.txt','enemy2.txt','enemybase.txt','enemybase2.txt'):
        # Original full-file source SHA cannot be reconstructed from publicly retained rows;
        # its saved digest is still pinned and source table row counts can be checked.
        assert out['original_table_byte_custody'][name]['rows'] == len(pet['source_rows'][name])
        assert len(out['original_table_byte_custody'][name]['sha256']) == 64

    known_files = {r[0]: r[2] for r in char01['source_files']}
    creates = {(r[0],r[1]):r for r in char01['create_rows']}
    derived = {(r[0],r[1]):r for r in char04['create_source_rows']}
    templates = {(r[0],r[1]):r for r in char01['template_rows']}
    argfiles = {r[0]:r for r in out['argument_files']}
    assert len(argfiles) == 260
    assert len(out['create_refs']) == len({(r[0],r[1]) for r in out['create_refs']})
    assert {x[0] for x in out['create_refs']} == set(out['create_file_sha256'])
    assert {r[7] for r in out['create_refs']} == set(argfiles)
    assert all(out['create_file_sha256'][p] == known_files[p] for p in out['create_file_sha256'])
    expected_npcenemy = {(r[0],r[1]) for r in char04['create_source_rows'] if r[2] == 'NPCEnemy'}
    assert expected_npcenemy == {(r[0],r[1]) for r in out['create_refs']}
    for row in out['create_refs']:
        path,ordinal,source_sha,floor,tpath,tordinal,templ_sha,apath,asha=row
        original=creates[(path,ordinal)]
        assert source_sha == original[4] and floor == original[5]
        assert derived[(path,ordinal)][2] == 'NPCEnemy'
        assert templates[(tpath,tordinal)][2] == templ_sha
        assert templates[(tpath,tordinal)][4] == 'NPCEnemy'
        assert [tpath,tordinal] in original[13]
        assert asha == argfiles[apath][1] == known_files[apath]
        assert any(x[0] == apath and x[2] == asha for x in original[15])
    # An arg path is one source script, not a distinct NPC or distinct enemy per create row.
    counts=out['counts']
    assert counts['NPCEnemy_config_refs']==279
    assert counts['unique_original_arg_files']==260
    assert counts['distinct_paired_source_enemy_instance_IDs']==230
    assert counts['distinct_paired_source_template_IDs']==214
    assert counts['distinct_original_source_graphic_numbers']==117
    assert counts['original_sprite_index_graphic_numbers_qualified']==117
    assert counts['full_real_SPR_action_and_RD_pixel_coverage_proven_by_this_package']==0
    assert counts['same_ID_both_pair_tables_instance_rows_equal_bytes']==0
    assert counts['same_ID_both_pair_tables_template_rows_equal_bytes']==145
    assert counts['same_ID_both_pair_tables_template_or_graphic_or_PETFLG_differences']==0
    assert counts['same_ID_not_in_both_instance_tables']==0
    gym = sum(int((argfiles[r[7]][6] or 0)>0) for r in out['create_refs'])
    assert gym == counts['gym_refs'] == 200
    assert len(out['create_refs'])-gym==counts['normal_refs']==79
    assert sum(len(argfiles[r[7]][3]) for r in out['create_refs']) == counts['main_enemy_roster_token_instances_per_config'] == 3930
    assert sum(len(argfiles[r[7]][4]) for r in out['create_refs']) == counts['companion_enemy_roster_token_instances_per_config'] == 7000

    inst1={r[1]:r for r in pet['source_rows']['enemy.txt']}
    inst2={r[1]:r for r in pet['source_rows']['enemy2.txt']}
    templ1={r[1]:r for r in pet['source_rows']['enemybase.txt']}
    templ2={r[1]:r for r in pet['source_rows']['enemybase2.txt']}
    sprrows=pet['source_rows']['spradrn_5.bin']
    spra={}
    for r in sprrows: spra.setdefault(r[1],[]).append(r)
    assert set(x[0] for x in out['source_enemy_number_to_paired_template_and_spr']) == {
        n for a in argfiles.values() for n in (*a[3],*a[4])
    }
    assert len({r[0] for r in out['source_enemy_number_to_paired_template_and_spr']})==230
    for row in out['source_enemy_number_to_paired_template_and_spr']:
        nid,tid,gid,pflag,si,offset,acount,res,inst_equal,temp_equal=row
        i1=inst1[nid]; i2=inst2[nid]
        assert i1[2]==i2[2]==tid
        b1=templ1[tid];b2=templ2[tid]
        assert (b1[2],b1[3]) == (b2[2],b2[3]) == (gid,pflag)
        assert int(i1[-1]==i2[-1])==inst_equal
        assert int(b1[-1]==b2[-1])==temp_equal
        assert spra[gid]==[[si,gid,offset,acount,res]]
    assert all(v is False for v in out['bounds'].values() if v is not None)
    assert out['bounds']['overall_restoration_percent'] is None
    assert out['module_status']=='SOURCE_BOUNDED_PARTIAL'
    assert out['next']=='MAP_SCENE_MODULE_01_SOURCE_BOUNDED_BATCH'


class TestCHAR09(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs=[
            load('STONEAGE-CHARACTER-NPC-MODULE-09-ORIGINAL-NPCENEMY-ROSTER-BRIDGE-R1.json'),
            load('STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'),
            load('STONEAGE-CHARACTER-NPC-MODULE-04-SAME-CARRIER-GRAPHIC-FUNCTION-JOIN-R1.json'),
            load('STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json'),
        ]
    def test_exact_public_metadata_replay(self): verify(*self.docs)
    def reject(self, edit):
        d=copy.deepcopy(self.docs[0]);edit(d)
        with self.assertRaises((AssertionError,KeyError,TypeError,IndexError)): verify(d,*self.docs[1:])
    def test_reject_missing_NPC_source(self):self.reject(lambda d:d['create_refs'].pop())
    def test_reject_false_same_source_identity(self):self.reject(lambda d:d['source_enemy_number_to_paired_template_and_spr'][0].__setitem__(2,-9))
    def test_reject_unverified_original_pixels(self):self.reject(lambda d:d['counts'].__setitem__('full_real_SPR_action_and_RD_pixel_coverage_proven_by_this_package',117))
    def test_reject_fake_arg_SHA(self):self.reject(lambda d:d['argument_files'][0].__setitem__(1,'0'*64))
    def test_reject_fake_original_template_sha(self):self.reject(lambda d:d['create_refs'][0].__setitem__(6,'1'*64))
    def test_reject_fake_original_custody(self):self.reject(lambda d:d.__setitem__('original_rar_sha256','x'*64))
    def test_reject_invalid_per_config_gym_count(self):self.reject(lambda d:d['argument_files'][0].__setitem__(6,123))
    def test_reject_sprite_index_guess(self):self.reject(lambda d:d['source_enemy_number_to_paired_template_and_spr'][0].__setitem__(4,999))
    def test_reject_original_official_deployment(self):self.reject(lambda d:d['bounds'].__setitem__('same_custody_archive_proves_original_official_release',True))

if __name__=='__main__':unittest.main()
