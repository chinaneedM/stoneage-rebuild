"""Reject normalization into an undocumented server XP rule."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from tools.stoneage_waei_cn20_level_exp_table import REPORT, URL, HEADERS, INTRO, build, extract_grid, observations, validate_report


class CN20LevelExperienceTests(unittest.TestCase):
    def report(self):return json.loads(REPORT.read_text())

    def reject_semantic(self,key,value,message):
        o=self.report();o['records'][0]['semantic_boundaries'][key]=value
        with self.assertRaisesRegex(ValueError,message):validate_report(o)

    def test_ambiguous_source_header_not_cumulative_or_next_level_or_pet_rule(self):
        for key in ['incremental_versus_cumulative','current_versus_destination_level','player_versus_pet_applicability']:
            self.reject_semantic(key,'CONFIRMED_SERVER_RULE','Ambiguous XP')
        self.reject_semantic('reincarnation_scaling_or_carryover',1.2,'runtime rule')

    def test_visible_last_level_not_cap_or_fitted_formula(self):
        self.reject_semantic('last_visible_level_is_game_cap_proven',True,'cap')
        self.reject_semantic('formula_or_extrapolated_levels',{'83':6470000},'fitted formula')
        self.reject_semantic('source_values_have_been_corrected_or_smoothed',True,'smoothed')

    def test_exact_original_values_and_three_source_columns(self):
        o=self.report();data=o['records'][0]['source_table_observations']
        self.assertEqual([(data[i-1]['required_exp_as_written']) for i in [1,29,57,80,81,82]],
                         ['2','81000','1131649','5836843','5874952','6166513'])
        data[80]['required_exp_as_written']='6230000'
        with self.assertRaisesRegex(ValueError,'silently corrected'):validate_report(o)
        o=self.report();o['records'][0]['source_table_observations'][0]['source_pair_group']=2
        with self.assertRaises(ValueError):validate_report(o)

    def test_blank_pairs_not_invented_levels_83_and_84(self):
        o=self.report();o['records'][0]['source_table_observations'].append({'level_label_as_written':'83','required_exp_as_written':'0','source_data_row':27,'source_pair_group':3})
        with self.assertRaisesRegex(ValueError,'extrapolated'):validate_report(o)
        o=self.report();o['table_shape']['blank_pairs']=[]
        with self.assertRaisesRegex(ValueError,'Blank source slots'):validate_report(o)

    def test_six_cell_pairs_not_flattened_row_order(self):
        grid=[HEADERS]+[[str(i),str(i*2),str(i+28),str(i*3),str(i+56),str(i*4)] for i in range(1,29)]
        grid[-2][4:]=['',''];grid[-1][4:]=['','']
        data,blank=observations(grid)
        self.assertEqual(data[28],{'level_label_as_written':'29','required_exp_as_written':'3','source_data_row':1,'source_pair_group':2})
        self.assertEqual(len(data),82);self.assertEqual(len(blank),2)
        for cells in [['','10'],['83',''],['1','2,000']]:
            bad=deepcopy(grid);bad[-1][4:]=cells
            with self.assertRaises(ValueError):observations(bad)
        bad=deepcopy(grid);bad[1][2]='1'
        with self.assertRaisesRegex(ValueError,'Exactly one observed'):observations(bad)

    def test_exact_introduction_and_headers_ignore_page_navigation(self):
        grid=[HEADERS]+[['1','2','3','4','5','6']]*28
        table='<table>'+''.join('<tr>'+''.join('<td>'+c+'</td>' for c in row)+'</tr>' for row in grid)+'</table>'
        self.assertEqual(extract_grid('<nav>1 2 29 81000</nav>'+INTRO+table),grid)
        for bad in [table,INTRO+table.replace('所需经验值','数值',1),INTRO+table+INTRO]:
            with self.assertRaises(ValueError):extract_grid(bad)

    def test_wrong_capture_and_error_body_rejected(self):
        for final in [URL,URL.replace('20011204165711','20020204000000')]:
            with self.assertRaises(ValueError):build(b'x'*75141,final)

    def test_official_page_label_not_25_installer_or_other_original_build(self):
        for field in ['cn25_jss1999_tw10_cn182_same_rule_proven','upgrade_path_is_software_download_target']:
            o=self.report();o['boundaries'][field]=True
            with self.assertRaisesRegex(ValueError,'misattributed'):validate_report(o)
        o=self.report();o['source']['page_title_as_written']='石器时代2.5'
        with self.assertRaisesRegex(ValueError,'CN2.0'):validate_report(o)

    def test_archive_contract_and_no_original_server_execution(self):
        o=self.report();validate_report(o)
        required=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        self.assertLessEqual(set(required),o['records'][0].keys())
        self.assertEqual(o['coverage']['new_original_pages'],0)
        self.assertFalse(o['qualified_unread_entry']['body_or_images_read'])
        o['records'][0]['actual_server_rule_or_execution_verified']=True
        with self.assertRaisesRegex(ValueError,'original server execution'):validate_report(o)


if __name__=='__main__':unittest.main()
