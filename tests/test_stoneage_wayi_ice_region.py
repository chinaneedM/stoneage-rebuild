import hashlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from PIL import Image
from tools import stoneage_wayi_ice_region as ice


def fixture():
    description = '瑞爾亞斯：第十大莊園 別名又叫作冰世界 常年都是冰天雪地 風是寒冷 草與稻作都很難生長 桀傲不訓 '
    description += '新地圖包括' + '、'.join(ice.MAP_NAMES) + '。'
    scenes = []
    for name, caption, _ in ice.CAPTIONS:
        scenes.append('<table><tr><td>' + caption + '</td></tr><tr><td><table><tr><td>'
                      + f'<img src="../images/game/{name}" width="220" height="163">'
                      + '</td></tr></table></td></tr></table>')
    return '<html><p>' + description + '</p><table><tr><td>' + ''.join(scenes) + '</td></tr></table></html>'


class IceRegionSource(unittest.TestCase):
    def test_all_twelve_map_labels_preserve_source_order(self):
        r = ice.region_contract(fixture())
        self.assertEqual([x['label_as_written'] for x in r['named_maps']], list(ice.MAP_NAMES))
        self.assertTrue(all(x['floor_id'] is None and x['coordinates'] is None and not x['adjacency_proven'] for x in r['named_maps']))

    def test_ordinal_ten_is_not_total_map_or_estate_census(self):
        r = ice.region_contract(fixture())
        self.assertEqual(r['estate_ordinal_described'], 10)
        self.assertEqual(r['named_map_count'], 12)
        self.assertFalse(r['ordinal_is_verified_complete_estate_census'])

    def test_missing_map_cannot_be_inferred_from_other_versions(self):
        with self.assertRaises(ValueError):
            ice.region_contract(fixture().replace('、黃泉之境', ''))

    def test_nested_tables_bind_each_image_to_its_own_caption(self):
        refs = ice.caption_pairs(fixture())
        self.assertEqual([x['original_url'].rsplit('/', 1)[-1] for x in refs], ['pic3.jpg', 'pic3-3.jpg', 'pic3-1.jpg', 'pic3-4.jpg', 'pic3-2.jpg', 'pic3-5.jpg'])
        self.assertEqual(refs[1]['caption_as_written'], '薩爾亞斯之都-議會廳內部：')

    def test_caption_cannot_be_borrowed_from_neighboring_picture(self):
        swapped = fixture().replace('pic3-3.jpg', 'TEMP.jpg').replace('pic3-1.jpg', 'pic3-3.jpg').replace('TEMP.jpg', 'pic3-1.jpg')
        with self.assertRaises(ValueError):
            ice.caption_pairs(swapped)

    def test_duplicate_picture_rejected(self):
        with self.assertRaises(ValueError):
            ice.caption_pairs(fixture().replace('pic3-5.jpg', 'pic3-4.jpg'))

    def test_caption_name_conflict_is_preserved(self):
        r = ice.region_contract(fixture())
        conflict = r['name_conflict']
        self.assertEqual(conflict['caption_orders_with_other_prefix'], [1, 2, 4])
        self.assertFalse(conflict['automatically_merged_or_corrected'])
        self.assertEqual(conflict['disposition'], 'UNRESOLVED_VARIANT_OR_TYPO_OR_DISTINCT_NAME')

    def test_silent_name_normalization_requires_source_requalification(self):
        with self.assertRaises(ValueError):
            ice.region_contract(fixture().replace('薩爾亞斯', '瑞爾亞斯'))

    def test_comment_or_script_cannot_supply_environment_claim(self):
        for wrapper in ('<!-- {} -->', '<script>{}</script>'):
            with self.subTest(wrapper=wrapper), self.assertRaises(ValueError):
                ice.region_contract(fixture().replace('第十大莊園', wrapper.format('第十大莊園')))

    def test_difficult_crop_growth_not_impossible_or_numeric_formula(self):
        r = ice.region_contract(fixture())['environment_and_culture']
        self.assertEqual(r['grass_and_rice_growth_described'], 'DIFFICULT_NOT_IMPOSSIBLE')
        self.assertFalse(r['crop_growth_rate_or_weather_mechanic_recovered'])
        self.assertFalse(r['npc_behavior_program_recovered'])

    def test_24_hour_caption_not_observed_continuous_service(self):
        r = ice.region_contract(fixture())
        self.assertFalse(r['twenty_four_hour_store']['actual_always_open_service_verified'])
        self.assertTrue(all(not x['service_transaction_executed'] for x in r['scenes']))

    def test_jpeg_dimensions_come_from_actual_bytes(self):
        out = io.BytesIO()
        Image.new('RGB', (3, 2)).save(out, format='JPEG')
        raw = out.getvalue()
        name = 'pic3.jpg'
        original = ice.ROOT + 'images/game/' + name
        final = 'https://web.archive.org/web/20060105082058id_/' + original
        pin = {'final_url': final, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        with patch.dict(ice.IMAGE_PINS, {name: pin}, clear=True):
            r = ice.jpeg_contract(raw, final, original)
            self.assertEqual(r['actual_dimensions'], [3, 2])
            self.assertIsNone(r['named_npc_or_pet_identification'])
            with self.assertRaises(ValueError):
                ice.jpeg_contract(raw + b'changed', final, original)
            with self.assertRaises(ValueError):
                ice.jpeg_contract(raw, final.replace('20060105', '20050614'), original)

    def test_wrong_detail_url_and_source_bytes_rejected(self):
        for url in (ice.URL.replace('game01_01', 'game01_02'), ice.URL):
            with self.subTest(url=url), self.assertRaises(ValueError):
                ice.build(b'<html>fake</html>', url, {}, b'{}')

    def test_unterminated_scene_table_rejected(self):
        with self.assertRaises(ValueError):
            ice.caption_pairs(fixture()[:-8])

    def test_picture_capture_is_later_than_body_and_build_unknown(self):
        r = json.loads(Path('research/recovered/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.json').read_text())
        self.assertEqual(r['temporality']['html_capture_year'], 2005)
        self.assertEqual(r['temporality']['scene_capture_year'], 2006)
        self.assertFalse(r['temporality']['same_capture_instant'])
        self.assertIsNone(r['version_context']['exact_client_build'])
        self.assertFalse(r['version_context']['ice_region_equals_all_of_lost_world_proven'])
        self.assertTrue(all(x['actual_dimensions'] == [220, 163] for x in r['region']['scenes']))

    def test_riding_appearance_does_not_prove_player_unlock(self):
        r = json.loads(Path('research/recovered/STONEAGE-WAYI-OFFICIAL-ICE-REGION-R1.json').read_text())
        self.assertEqual(r['riding_visual_candidate']['grade'], 'HYPOTHESIS_VISUAL_APPEARANCE_ONLY')
        self.assertFalse(r['riding_visual_candidate']['normal_player_unlock_or_mount_rules_proven'])
        self.assertFalse(r['boundaries']['same_build_jss1999_or_tw10_promoted'])
        self.assertFalse(r['boundaries']['actual_game_server_or_service_transaction_executed'])
        self.assertFalse(r['boundaries']['original_html_jpeg_or_software_retained_in_git'])

    def test_catalog_uses_shared_contract_without_invented_npcs_or_pets(self):
        raw, archive = Path(ice.REPORT).read_bytes(), Path(ice.ARCHIVE).read_bytes()
        r = ice.catalog_contract(raw, archive)
        self.assertEqual(r['record_count'], 19)
        self.assertEqual(sum(x['collection'] == 'maps' for x in r['records']), 13)
        self.assertEqual(sum(x['collection'] == 'screens' for x in r['records']), 6)
        self.assertEqual(r['npc_pet_or_quest_entities_created'], 0)
        self.assertTrue(all(x['game_ids'] is None for x in r['records']))
        self.assertFalse(r['all_place_name_variants_canonicalized'])
        self.assertFalse(r['public_export_allowed'])
        self.assertFalse(r['website_or_game_implemented'])

    def test_catalog_requires_existing_collection_schema(self):
        archive = json.loads(Path(ice.ARCHIVE).read_text())
        archive['future_website']['required_collections'].remove('screens')
        with self.assertRaises(ValueError):
            ice.catalog_contract(Path(ice.REPORT).read_bytes(), json.dumps(archive).encode())

    def test_catalog_cannot_drop_required_source_fields(self):
        archive = json.loads(Path(ice.ARCHIVE).read_text())
        archive['future_website']['record_contract']['required'].append('required_but_unfilled')
        with self.assertRaises(ValueError):
            ice.catalog_contract(Path(ice.REPORT).read_bytes(), json.dumps(archive).encode())


if __name__ == '__main__':
    unittest.main()
