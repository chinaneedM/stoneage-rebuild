import collections
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT='research/recovered/STONEAGE-INTEGRATION95-DUNGEON00-147-ORIGINAL-WARP-AND-PRIOR-DAT-R1.json'
CHAR='research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
MAP='research/recovered/STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json'

def load(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))

def sha(b):
    return hashlib.sha256(b).hexdigest()

class INTEGRATION95_OriginalDungeonSourceOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=load(REPORT)
        cls.char=load(CHAR)
        cls.maps=load(MAP)
        cls.rows=cls.r['original_warp_raw_source_rows_numeric_only']
        cls.map_by_id={int(m[0][:-4]):m for m in cls.maps['per_floor_source_rows'] if m[0][:-4].isdigit()}

    def test_01_single_exact_original_17289_source_and_147_public_old_spans(self):
        src=self.r['original_private_source']; self.assertEqual(src['member'],'npc/genout/dungeon00.create')
        self.assertEqual((src['original_file_bytes'],src['original_file_SHA256'],src['original_file_crc32_hex']),
                         (17289,'1b3d189ea8ae5e42de4321efce19d3fb9517f0b25b6130ff0cb73761cd62514b','c36d56ad'))
        oldfile=next(x for x in self.char['source_files'] if x[0]=='genout/dungeon00.create')
        self.assertEqual(oldfile[1:4],[src['original_file_bytes'],src['original_file_SHA256'],src['original_file_crc32_hex']])
        prior=sorted([x for x in self.char['create_rows'] if x[0]=='genout/dungeon00.create'],key=lambda x:x[1]);self.assertEqual(len(prior),147)
        self.assertEqual([r['ordinal'] for r in self.rows],list(range(147)))
        for x,y in zip(prior,self.rows):
            self.assertEqual([x[1],[x[2],x[3]],x[4],x[5],x[7][:2],x[11]],
              [y['ordinal'],y['source_byte_window'],y['original_block_SHA256'],y['source_floor'],y['source_xy'],'npcgen_warp'])
        self.assertEqual(sha(''.join(y['original_block_SHA256'] for y in self.rows).encode('ascii')),src['all_147_original_byte_spans_ordered_SHA256_text_chain'])
        self.assertEqual(src['original_unacquired_generator_input_GEN_verified'],False)
        self.assertFalse(src['RAR_parent_reread_this_unit'])

    def test_02_147_exact_source_coordinate_warp_rows_digest(self):
        s=''.join(f"{r['ordinal']}|{r['source_floor']}|{r['source_xy'][0]},{r['source_xy'][1]}|{r['target_floor']}|{r['target_xy'][0]},{r['target_xy'][1]}|{int(r['strict_reciprocal_candidate'])}\n" for r in self.rows)
        self.assertEqual(sha(s.encode('ascii')),self.r['original_private_source']['actual_original_numeric_warp_rows_SHA256_encoding'])
        self.assertEqual(len(self.rows),147)
        self.assertTrue(all(r['source_floor']>0 and r['target_floor']>0 for r in self.rows))
        self.assertTrue(all(len(r['source_xy'])==len(r['target_xy'])==2 for r in self.rows))

    def test_03_literal_exact_reverse_140_and_seven_preserved(self):
        pairs={(r['source_floor'],*r['source_xy'],r['target_floor'],*r['target_xy']):r['ordinal'] for r in self.rows}
        self.assertEqual(len(pairs),147)
        unpaired=[]
        for r in self.rows:
            rev=pairs.get((r['target_floor'],*r['target_xy'],r['source_floor'],*r['source_xy']))
            self.assertEqual(rev,r['strict_reciprocal_source_ordinal'])
            self.assertEqual(rev is not None,r['strict_reciprocal_candidate'])
            if rev is None:unpaired.append(r['ordinal'])
        self.assertEqual(unpaired,[14,29,30,67,68,69,70])
        self.assertEqual(self.r['counts']['original_exact_strict_reciprocal_row_occurrences'],140)
        self.assertEqual(self.r['counts']['exact_paired_source_row_pairs'],70)
        self.assertEqual(len(self.r['seven_rows_without_strict_reverse_CONFIG_not_gameplay_one_way']),7)

    def test_04_source_floor_graph_is_64_nodes_117_direction_pairs_five_groups(self):
        directed={(r['source_floor'],r['target_floor']) for r in self.rows}
        floors={f for edge in directed for f in edge}
        self.assertEqual((len(floors),len(directed)),(64,117))
        self.assertEqual(len(self.rows)-len(directed),30)
        comps=self.r['derived_weak_COMPONENT_floor_lists_SOURCE_CONSTRAINT_ONLY']
        self.assertEqual(sorted(map(len,comps),reverse=True),[31,10,9,8,6])
        self.assertEqual(sorted(f for comp in comps for f in comp),sorted(floors))
        membership={f:i for i,comp in enumerate(comps) for f in comp}
        self.assertTrue(all(membership[a]==membership[b] for a,b in directed))
        for comp in comps:
            todo={comp[0]};seen=set()
            while todo:
                f=todo.pop()
                if f in seen:continue
                seen.add(f);todo.update(g for a,b in directed for g in ([b] if a==f else [a] if b==f else []) if g not in seen)
            self.assertEqual(seen,set(comp))
        self.assertEqual(len(self.r['derived_strong_COMPONENT_floor_lists_SOURCE_CONSTRAINT_ONLY']),7)
        self.assertEqual(sorted(map(len,self.r['derived_strong_COMPONENT_floor_lists_SOURCE_CONSTRAINT_ONLY']),reverse=True),[26,10,9,8,5,5,1])

    def test_05_prior_MAP04_original_955_DAT_custody_no_new_DAT_raw_read(self):
        floors=self.r['all_64_floors_prior_original_DAT_catalog_qualification'];self.assertEqual(len(floors),64)
        self.assertEqual(len(set(x['floor_id'] for x in floors)),64)
        missing=[]
        for x in floors:
            original=self.map_by_id.get(x['floor_id'])
            self.assertFalse(x['actual_DAT_raw_bytes_reread_this_unit'])
            if not original:
                missing.append(x['floor_id'])
                self.assertIsNone(x['prior_source_DAT_SHA256'])
            else:
                self.assertEqual([x['same_saved_mixed25_original_DAT_name'],x['prior_source_DAT_SHA256'],x['prior_source_DAT_bytes'],x['original_dimensions'],x['prior_MAP04_first_two_plane_original_numeric_nonzero_positions'],x['prior_MAP04_source_qualified_original_TW1_RD_occurrences'],x['prior_MAP04_not_matched_original_TW1_RD_occurrences']],
                                 [original[0],original[2],original[1],original[3:5],original[6:8],original[10],original[11]])
        self.assertEqual(missing,[100,200,1100,10301,10302,10303,10304,10305,10306,10307,10308])
        self.assertEqual(self.r['counts']['distinct_source_floor_IDs_matched_prior_real_DAT_catalog'],53)
        self.assertEqual(self.r['counts']['original_new_DAT_source_raw_bytes_reread'],0)

    def test_06_205_prior_DAT_coordinate_bounds_only(self):
        sources=targets=both=0
        for r in self.rows:
            s=self.map_by_id.get(r['source_floor']);t=self.map_by_id.get(r['target_floor'])
            self.assertEqual(r['source_DAT_known_prior'],s is not None)
            self.assertEqual(r['target_DAT_known_prior'],t is not None)
            if s:
                sources+=1
                self.assertTrue(r['source_xy_within_prior_DAT_dimensions'])
                self.assertLess(r['source_xy'][0],s[3]);self.assertLess(r['source_xy'][1],s[4])
            else:self.assertIsNone(r['source_xy_within_prior_DAT_dimensions'])
            if t:
                targets+=1
                self.assertTrue(r['target_xy_within_prior_DAT_dimensions'])
                self.assertLess(r['target_xy'][0],t[3]);self.assertLess(r['target_xy'][1],t[4])
            else:self.assertIsNone(r['target_xy_within_prior_DAT_dimensions'])
            both+=bool(s and t)
        self.assertEqual((sources,targets,both),(105,100,92))
        self.assertEqual(self.r['counts']['known_DAT_endpoints_outside_prior_header_dimensions'],0)

    def test_07_private_archive_CRC_and_approved_custody_metadata_only(self):
        z=self.r['private_original_source_custody'];self.assertEqual(z['zip_bytes'],10610)
        self.assertEqual(z['zip_SHA256'],'0e13f780dbd4263e74284329072c0bbb5c8f845647da2bf7916962b9de1a07d5')
        self.assertEqual(z['zip_members_all_CRC_success'],3)
        self.assertEqual(z['private_offline_modern_synthetic_2D_graph_HTML_SHA256'],'1a447d095480a5b559741d58b430ead677771ad13c4d3dd3be826aca1f082c1e')
        self.assertTrue(z['independent_library_upload_redownload']['exact_private_ZIP_SHA_and_all_bytes_match_after_3rd_party_retrieval'])
        self.assertTrue(z['independent_library_upload_redownload']['source_3_members_all_CRC_success'])
        self.assertFalse(z['original_commercial_CREATE_bytes_published_to_public_git'])

    def test_08_real_browser_was_modern_source_graph_not_game(self):
        b=self.r['private_original_source_custody']['modern_browser_actual_execution']
        self.assertEqual([x['floor_nodes'] for x in b['component_filter_runs']],[31,10,9,8,6])
        self.assertEqual([x['source_edges'] for x in b['component_filter_runs']],[67,20,16,34,10])
        self.assertEqual((b['all_source_numeric_floor_nodes'],b['all_source_numeric_edges']),(64,147))
        self.assertEqual((b['zero_JS_errors'],b['zero_external_HTTP_requests'],b['zero_console_errors']),(0,0,0))
        self.assertFalse(b['original_client_executed']);self.assertFalse(b['file_URL_navigation_success_claimed'])

    def test_09_historical_stage_and_scope_not_overpromoted(self):
        self.assertEqual(self.r['stage']['Stage_A'],'7_PARTIAL_2_OPEN')
        self.assertEqual((self.r['stage']['Stage_B'],self.r['stage']['wiki']),('GATED','GATED'))
        self.assertEqual(self.r['stage']['R79'],'PAUSED_NON_BLOCKING')
        self.assertIsNone(self.r['stage']['overall_percent'])
        self.assertEqual(self.r['counts']['official_original_client_warp_runtime_proved'],0)
        self.assertGreaterEqual(len(self.r['negative_evidence']),8)
        self.assertFalse(self.r['original_private_source']['RAR_parent_reread_this_unit'])
        self.assertFalse(self.r['original_private_source']['original_unacquired_generator_input_GEN_verified'])

if __name__=='__main__':
    unittest.main()
