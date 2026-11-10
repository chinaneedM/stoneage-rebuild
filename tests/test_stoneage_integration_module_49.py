"""Source-bounded numeric/sha contracts for INTEGRATION49 (no private assets).

Does not simulate original native NPC spawn, teleport, renderer, or shop.
"""
import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / 'research/recovered/STONEAGE-INTEGRATION49-28-ORIGINAL-ROOM-NPC-WARP-SOURCE-ATLAS-R1.json'
CHAR = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
MAP = ROOT / 'research/recovered/STONEAGE-MAP07-28-ORIGINAL-DAT-SOURCE-SCENE-RECEIPT-R1.json'
REC = ROOT / 'research/recovered/STONEAGE-INTEGRATION10-TWELVE-RECOVERED-DAT-SEVEN-CHECKPOINT-SCENES-R1.json'
CURRENT = ROOT / 'docs/CURRENT-STATE.md'


def git_blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def lookup_rows(index):
    return {(r[0],r[1]):r for r in index['create_rows']}


def validate_create_record(r, char_rows, file_rows, templates):
    key=(r['source_CREATE_path'],r['source_CREATE_block_ordinal'])
    assert key in char_rows, key
    src=char_rows[key]
    assert src[5]==r['source_floor_id']
    assert src[4]==r['source_CREATE_block_sha256']
    assert src[2:4]==r['source_block_start_end_exclusive']
    assert r['source_CREATE_file_sha256']==file_rows[src[0]][2]
    assert src[6]==r['graphic_alias']
    assert src[14]==r['original_name_SHA256']
    assert r['template_source']==src[13][0]
    assert r['template_block_SHA256']==templates[tuple(src[13][0])][2]
    assert r['source_functionset']==(templates[tuple(src[13][0])][4] or 'EMPTY_FUNCTIONSET_LITERAL')
    assert r['source_arg_refs']==[{'path':a[0],'sha256':a[2]} for a in (src[15] or [])]
    if src[7] is not None:
        assert r['coordinate']==src[7][:2]
        assert r['coordinate_field']=='borncorner_point'
    elif src[8] is not None:
        assert r['coordinate']==src[8][:2]
        assert r['coordinate_field']=='borncenter_first_two_literal'
    else:
        assert r['coordinate'] is None
        assert r['coordinate_field']=='NO_COORDINATE_IN_CREATE'
        assert r['original_DAT_third_plane_value'] is None


class TestOriginalRoomNPCWarpAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas=load(ATLAS)
        cls.char=load(CHAR)
        cls.map=load(MAP)
        cls.recovered=load(REC)
        cls.rows=lookup_rows(cls.char)
        cls.files={r[0]:r for r in cls.char['source_files']}
        cls.templates={(r[0],r[1]):r for r in cls.char['template_rows']}
        cls.room_records=[n for room in cls.atlas['rooms'] for n in room['source_records']]
        cls.warp=[n for n in cls.room_records if n['source_functionset']=='Warp']

    def test_prior_char01_immutable_blob(self):
        self.assertEqual(git_blob_sha(CHAR.read_bytes()),self.atlas['source_origins']['mixed25_CHAR01_public_source_index_git_blob'])

    def test_prior_map07_immutable_blob(self):
        self.assertEqual(git_blob_sha(MAP.read_bytes()),self.atlas['source_origins']['MAP07_public_original_source_receipt_git_blob'])

    def test_preserved_historical_CURRENT(self):
        self.assertEqual(git_blob_sha(CURRENT.read_bytes()),self.atlas['historical_CURRENT_original_blob_preserved'])
        self.assertGreater(CURRENT.stat().st_size,2700000)

    def test_all_28_dat_against_old_original_source_report(self):
        old={r['floor']:r for r in self.map['maps']}
        rooms=self.atlas['rooms']
        self.assertEqual(len(rooms),28)
        self.assertEqual(set(old),{r['floor_id'] for r in rooms})
        for room in rooms:
            m=old[room['floor_id']]
            self.assertEqual(room['original_DAT_sha256'],m['source_dat_sha256'])
            self.assertEqual(room['original_DAT_bytes'],m['source_dat_bytes'])
            self.assertEqual(room['original_DAT_dimensions'],m['source_map_geometry'])
            self.assertEqual(room['candidate_draw_positions'],m['modern_candidate_draw_positions'])
            self.assertEqual(room['original_TW1_candidate_distinct_aliases'],m['distinct_modern_candidate_numeric_aliases'])

    def test_139_original_create_records_unique_and_content(self):
        self.assertEqual(len(self.room_records),139)
        self.assertEqual(len({(x['source_CREATE_path'],x['source_CREATE_block_ordinal']) for x in self.room_records}),139)
        for r in self.room_records:
            validate_create_record(r,self.rows,self.files,self.templates)

    def test_roles_are_exact_functionsets_not_filenames(self):
        expected={'Warp':56,'ItemShop':32,'EMPTY_FUNCTIONSET_LITERAL':18,'TownPeople':8,'PetShop':6,'PetSkillShop':6,'WindowHealer':5,'Windowman':3,'ExChangeMan':3,'Charm':2}
        self.assertEqual(dict(Counter(r['source_functionset'] for r in self.room_records)),expected)
        self.assertEqual(self.atlas['summary']['source_NPC_functionset_roles'],dict(sorted(expected.items())))

    def test_three_events_without_native_coordinates_kept_unplaced(self):
        missing=[r for r in self.room_records if r['coordinate'] is None]
        self.assertEqual([r['source_floor_id'] for r in missing],[1003,2003,3003])
        self.assertTrue(all(r['source_functionset']=='ExChangeMan' for r in missing))

    def test_parent_floor_groups_derived_from_source_warp(self):
        groups=defaultdict(list)
        for room in self.atlas['rooms']:
            group={r['warp_target_source_literals'][0] for r in room['source_records'] if r['source_functionset']=='Warp'}
            self.assertEqual(group,{room['parent_floor_from_room_warp_literals']})
            groups[room['parent_floor_from_room_warp_literals']].append(room['floor_id'])
        self.assertEqual({k:len(v) for k,v in groups.items()},{1000:3,1100:5,1200:5,1300:5,2000:5,3000:5})

    def test_all_56_warps_have_original_numeric_marker(self):
        self.assertEqual(len(self.warp),56)
        for r in self.warp:
            self.assertEqual(r['original_DAT_third_plane_value'],49155)
            self.assertIsNotNone(r['coordinate'])
            self.assertEqual(len(r['warp_target_source_literals']),3)

    def test_50_exact_symmetric_links_have_old_parent_create(self):
        exact=[r for r in self.warp if r['source_reverse']['status']=='EXACT_SYMMETRIC_COORDINATE']
        self.assertEqual(len(exact),50)
        for r in exact:
            rev=r['source_reverse'];self.assertEqual(rev['original_return_target'],[r['source_floor_id'],*r['coordinate']])
            src=self.rows[(rev['reverse_CREATE_path'],rev['reverse_CREATE_block_ordinal'])]
            self.assertEqual(src[4],rev['reverse_CREATE_block_sha256'])
            self.assertEqual(src[5],r['warp_target_source_literals'][0])
            self.assertEqual((src[7] or src[8])[:2],r['warp_target_source_literals'][1:])

    def test_six_adjacent_return_exceptions_keep_native_literal(self):
        odd=[r for r in self.warp if r['source_reverse']['status']=='SAME_PARENT_POINT_RETURN_TO_ADJACENT_ROOM_CELL']
        self.assertEqual(len(odd),6)
        self.assertEqual([r['source_floor_id'] for r in odd],[1101,2005,3001,3002,3003,3005])
        for r in odd:
            back=r['source_reverse']['original_return_target']
            self.assertEqual(back[0],r['source_floor_id'])
            self.assertEqual(sum(abs(back[i+1]-r['coordinate'][i]) for i in (0,1)),1)
            self.assertNotEqual(back,[r['source_floor_id'],*r['coordinate']])

    def test_only_50_distinct_reverse_create_rows(self):
        refs={(r['source_reverse']['reverse_CREATE_path'],r['source_reverse']['reverse_CREATE_block_ordinal']) for r in self.warp}
        self.assertEqual(len(refs),50)
        self.assertEqual(self.atlas['summary']['unique_reverse_parent_CREATE_source_blocks'],50)

    def test_prior_integration10_already_recovered_parent_1100_and_1300(self):
        d={r['floor']:r['sha256'] for r in self.recovered['recovered_DAT']}
        self.assertEqual(d[1100],'50e01ffb3cdb66560543f01d4b371f9f160f57610fc1379b541679b3044f9831')
        self.assertEqual(d[1300],'97448b7e2478fdb8469b09b5f05a2b0b908174d0eb4bec066f7d526fa052af20')
        for r in self.atlas['rooms']:
            if r['parent_floor_from_room_warp_literals'] in (1100,1300):
                self.assertEqual(r['parent_DAT_after_INTEGRATION10'],'RECOVERED_ALREADY_IN_INTEGRATION10_NOT_REREAD_THIS_UNIT')

    def test_original_material_counts_not_claimed_new(self):
        sm=self.atlas['summary']
        self.assertEqual(sm['source_room_DAT_read_and_SHA_CRC_verified'],28)
        self.assertEqual(sm['independently_replayed_source_candidate_composite_RGBA'],28)
        self.assertEqual(sm['private_marked_scene_previews'],28)
        for k in ['new_original_DAT_discovered','new_original_NPC_CREATE_files_discovered','new_original_RD_decodes']:
            self.assertEqual(sm[k],0)

    def test_no_cross_build_runtime_or_geography_promotion(self):
        b=self.atlas['bounds']
        self.assertTrue(b['original_room_DAT_bytes_reopened'])
        self.assertTrue(b['original_NPC_CREATE_source_bytes_reopened'])
        self.assertTrue(self.atlas['room_groups_are_source_warp_parent_floor_not_assumed_early_official_village_names'])
        self.assertTrue(all(not v for k,v in b.items() if k not in ('original_room_DAT_bytes_reopened','original_NPC_CREATE_source_bytes_reopened')))
        self.assertFalse(self.atlas['source_origins']['tw10_sprites_original_same_runtime_with_mixed25_source_proven'])

    def test_negative_warp_false_symmetric_rejected(self):
        original=next(r for r in self.warp if r['source_reverse']['status'].startswith('SAME_PARENT'))
        bad=copy.deepcopy(original)
        bad['source_reverse']['status']='EXACT_SYMMETRIC_COORDINATE'
        with self.assertRaises(AssertionError):
            assert bad['source_reverse']['original_return_target']==[bad['source_floor_id'],*bad['coordinate']]

    def test_negative_original_create_coordinate_tampering_rejected(self):
        original=next(r for r in self.room_records if r['coordinate'] is not None)
        bad=copy.deepcopy(original);bad['coordinate']=[0,0]
        with self.assertRaises(AssertionError):
            validate_create_record(bad,self.rows,self.files,self.templates)

    def test_negative_missing_source_as_zero_x_y_rejected(self):
        original=next(r for r in self.room_records if r['coordinate'] is None)
        bad=copy.deepcopy(original);bad['coordinate']=[0,0]
        with self.assertRaises(AssertionError):
            validate_create_record(bad,self.rows,self.files,self.templates)

if __name__=='__main__':unittest.main()
