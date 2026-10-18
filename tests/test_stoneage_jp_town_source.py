"""Same-row village evidence and non-promotion guards; synthetic HTML only."""
from pathlib import Path
import json
import unittest
from tools.stoneage_jp_town_source import ORIGINAL,CAPTURE,SOURCE_SHA,IMAGES,IMAGE_ORIGINAL,IMAGE_CAPTURE,NAMES,REPORT,archive,classify_page,inspect_page,inspect_image


def specimen():
    rows=[]
    for i,name in enumerate(NAMES):
        rows.append(f'<tr><td><img src="{IMAGES}town1-{i+1}.gif" width="200" height="150"></td><td></td><td>{name}<br>synthetic description {i}</td></tr>')
        if i<3:rows.append('<tr><td></td><td></td><td></td></tr>')
    return '村の紹介<table>'+''.join(rows)+'</table><font onclick="location.href=\'town2.asp\';">村の施設の紹介</font>'


class JapaneseTownSourceTests(unittest.TestCase):
    def test_four_names_have_same_row_image_reference_and_description_digest(self):
        e=classify_page(specimen())
        self.assertEqual([x['name_as_written'] for x in e],NAMES)
        self.assertEqual([x['dom_cells']['row'] for x in e],[0,2,4,6])
        self.assertEqual(len({x['source_description_sha256'] for x in e}),4)

    def test_swapped_names_or_images_do_not_preserve_settlement_identity(self):
        for wrong in (specimen().replace(NAMES[0],'TEMP').replace(NAMES[1],NAMES[0]).replace('TEMP',NAMES[1]),specimen().replace('town1-1.gif','TEMP').replace('town1-2.gif','town1-1.gif').replace('TEMP','town1-2.gif')):
            with self.assertRaises(ValueError):classify_page(wrong)

    def test_missing_description_wrong_cell_or_dimensions_rejected(self):
        for wrong in (specimen().replace('<br>synthetic description 0',''),specimen().replace('width="200"','width="20"',1),specimen().replace('<td></td><td>'+NAMES[0],'<td>'+NAMES[0]+'</td><td>')):
            with self.assertRaises(ValueError):classify_page(wrong)

    def test_script_and_comment_pictures_do_not_invent_fifth_village(self):
        fake=f'<img src="{IMAGES}town1-1.gif" width="200" height="150">'
        self.assertEqual(len(classify_page('<!--'+fake+'--><script>'+fake+'</script>'+specimen())),4)

    def test_facilities_topic_and_static_target_are_actual_source_fields(self):
        for wrong in (specimen().replace('town2.asp','town3.asp'),specimen().replace('村の施設の紹介','invented label'),specimen().replace('村の紹介','invented topic')):
            with self.assertRaises(ValueError):classify_page(wrong)

    def test_wrong_page_epoch_host_or_same_size_error_body_rejected(self):
        exact=archive(ORIGINAL,CAPTURE)
        for wrong in (exact.replace('hangame.co.jp','example.org'),exact.replace(CAPTURE,IMAGE_CAPTURE),exact):
            with self.assertRaises(ValueError):inspect_page(b'x'*14371,wrong)

    def test_2006_illustration_not_2003_page_or_arbitrary_gif(self):
        with self.assertRaisesRegex(ValueError,'host/path/capture'):inspect_image(b'',archive(IMAGE_ORIGINAL,CAPTURE))
        with self.assertRaisesRegex(ValueError,'byte pin'):inspect_image(b'x'*27303,archive(IMAGE_ORIGINAL,IMAGE_CAPTURE))

    def test_records_keep_required_archive_fields_and_geography_unknowns(self):
        p=json.loads(REPORT.read_text());contract=json.loads(Path('research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json').read_text())['future_website']
        self.assertEqual(len(p['records']),4)
        self.assertEqual([x['region_name_as_written'] for x in p['records']],['サイナス島','サイナス','ジャルガ','ジャルガ'])
        for i,r in enumerate(p['records']):
            self.assertLessEqual(set(contract['record_contract']['required']),r.keys())
            self.assertIn(r['collection'],contract['required_collections'])
            self.assertIsNone(r['client_map_id_coordinates_routes_npcs_encounters'])
            self.assertIsNone(r['cross_region_aliases'])
            self.assertIsNone(r['population_area_or_world_town_census'])
            self.assertFalse(r['image']['building_function_or_original_client_map_proven'])
            self.assertNotEqual(r['rights_status'],'RELEASE_APPROVED')
            self.assertEqual(r['source_refs'][0]['actual_capture'],CAPTURE)
            if i==0:self.assertEqual(r['image']['actual_capture'],IMAGE_CAPTURE)
            else:self.assertIsNone(r['image']['actual_capture']);self.assertIsNone(r['image']['sha256'])
        self.assertFalse(p['boundaries']['four_entries_are_all_world_villages'])
        self.assertFalse(p['reviewed_image']['building_function_or_map_coordinates_inferred'])


if __name__=='__main__':unittest.main()
