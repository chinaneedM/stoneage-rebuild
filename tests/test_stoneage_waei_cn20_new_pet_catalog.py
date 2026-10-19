"""Reject invented species IDs, placeholder names and unacquired pixels."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from tools.stoneage_waei_cn20_new_pet_catalog import REPORT,URL,ENTRY_URL,build,parse_catalog,validate_report


class NewPetCatalogTests(unittest.TestCase):
    def report(self):return json.loads(REPORT.read_text())

    def test_placeholder_duplicates_stay_separate_unnamed_web_positions(self):
        o=self.report();validate_report(o);r=o['records']
        self.assertEqual([x['display_label_as_written'] for x in r[:6]],['???','???','??1','??2','??3','??4'])
        self.assertNotEqual(r[0]['record_id'],r[1]['record_id']);self.assertNotEqual(r[0]['image_reference']['original_url'],r[1]['image_reference']['original_url'])
        self.assertEqual(r[6]['name_as_written'],'阿米朵')
        r[0]['name_as_written']='未知恐龙'
        with self.assertRaisesRegex(ValueError,'Placeholder silently named'):validate_report(o)

    def test_file_numbers_and_case_not_sorted_or_promoted_to_species_ids(self):
        o=self.report();r=o['records'];self.assertTrue(r[0]['image_reference']['relative_src_as_written'].endswith('6.JPG'))
        self.assertTrue(r[3]['image_reference']['relative_src_as_written'].endswith('2.jpg'))
        self.assertTrue(r[8]['image_reference']['relative_src_as_written'].endswith('10.JPG'))
        r[0]['original_game_pet_id']=6
        with self.assertRaisesRegex(ValueError,'game identity'):validate_report(o)
        o=self.report();o['records'][3]['image_reference']['relative_src_as_written']='img/newpet/2.JPG'
        with self.assertRaises(ValueError):validate_report(o)

    def test_cell_name_image_association_not_alphabetical_filename_join(self):
        o=self.report();a,b=o['records'][8:10]
        a['display_label_as_written'],b['display_label_as_written']=b['display_label_as_written'],a['display_label_as_written']
        a['name_as_written']=a['display_label_as_written'];b['name_as_written']=b['display_label_as_written']
        with self.assertRaisesRegex(ValueError,'cell associations'):validate_report(o)

    def test_only_four_declared_sizes_and_no_actual_dimensions(self):
        o=self.report();self.assertEqual(sum(r['image_reference']['html_declared_dimensions'] is not None for r in o['records']),4)
        self.assertIsNone(o['records'][6]['image_reference']['html_declared_dimensions'])
        o['records'][6]['image_reference']['actual_dimensions']=[83,90]
        with self.assertRaisesRegex(ValueError,'acquired pixels'):validate_report(o)
        o=self.report();o['records'][6]['image_reference']['html_declared_dimensions']=[83,90]
        with self.assertRaisesRegex(ValueError,'declared dimensions'):validate_report(o)

    def test_jpg_suffix_not_verified_format_or_animation(self):
        o=self.report();o['records'][6]['image_reference']['actual_format_or_frames']={'format':'JPEG','frames':1}
        with self.assertRaisesRegex(ValueError,'format or animation'):validate_report(o)

    def test_web_range_104_not_complete_new_species_count_or_release_date(self):
        o=self.report();o['coverage']['full_original_species_census_or_104_newly_added_pets_proven']=True
        with self.assertRaisesRegex(ValueError,'full original roster'):validate_report(o)
        o=self.report();o['source']['page_label_authenticates_exact_build_or_addition_date']=True
        with self.assertRaisesRegex(ValueError,'dated additions'):validate_report(o)

    def test_unread_pagination_and_no_cross_version_stats(self):
        o=self.report();o['qualified_unread_pagination'][0]['body_or_images_read']=True
        with self.assertRaisesRegex(ValueError,'Unread pagination'):validate_report(o)
        o=self.report();o['records'][6]['stats_growth_capture_skill_or_riding_rules']={'growth':5}
        with self.assertRaisesRegex(ValueError,'gameplay data'):validate_report(o)

    def test_exact_table_structure_and_one_image_per_named_cell(self):
        nav='<table><tr><td>1-40</td><td><a href="new_pet1.asp">41-80</a></td><td><a href="new_pet2.asp">81-104</a></td></tr></table>'
        cell='<td><img src="img/newpet/a.JPG">label</td>'
        doc='新 增 宠 物'+nav+'<table>'+('<tr>'+cell*5+'</tr>')*8+'</table><span class="p12b">'
        grid,links=parse_catalog(doc);self.assertEqual(len(grid),8);self.assertEqual(len(links),2)
        for bad in [doc.replace('label</td>','</td>',1),doc.replace('<img src="img/newpet/a.JPG">','',1),doc.replace(cell,cell+cell,1)]:
            with self.assertRaises(ValueError):parse_catalog(bad)

    def test_error_page_and_other_capture_rejected(self):
        for entry_final,final in [(ENTRY_URL,URL),(ENTRY_URL,URL.replace('20011204194619','20020201000000'))]:
            with self.assertRaises(ValueError):build(b'e'*65653,entry_final,b'b'*69317,final)

    def test_archive_contract_and_positions_not_new_original_entities(self):
        o=self.report();validate_report(o)
        required=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']['record_contract']['required']
        for r in o['records']:
            self.assertLessEqual(set(required),r.keys());self.assertEqual(r['collection'],'pets');self.assertIsNone(r['cross_region_or_build_entity_identity'])
        o['records'][0]['source_position']['ordinal']=6
        with self.assertRaisesRegex(ValueError,'Web positions'):validate_report(o)


if __name__=='__main__':unittest.main()
