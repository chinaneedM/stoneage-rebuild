from copy import deepcopy
import json
import unittest
from tools import stoneage_waei_cn20_island_hero as m


class IslandHeroTests(unittest.TestCase):
 def setUp(self):self.o=json.loads(m.REPORT.read_bytes())
 def reject(self, change):
  o=deepcopy(self.o);change(o)
  with self.assertRaises((ValueError,AssertionError)):m.validate_report(o)
 def test_exact_source_scoped_content(self):
  m.validate_report(self.o)
  self.assertEqual(self.o['records'][5]['source_qualified_guide']['birth_routes'][0]['source_step_order'],[2,3])
 def test_no_claim_mainland_was_open(self):
  self.reject(lambda o:o['records'][5]['source_qualified_guide'].update(described_availability='CN_DEPLOYED'))
 def test_no_same_capture_or_build_projection(self):
  self.reject(lambda o:o['boundaries'].update(same_capture_instant_or_exact_build=True))
  self.reject(lambda o:o['sources'][1].update(actual_capture='20011201212305'))
 def test_no_fish_village_flower_requirement(self):
  self.reject(lambda o:o['records'][5]['source_qualified_guide']['birth_routes'][0].update(source_step_order=[1,2,3]))
 def test_no_prerequisite_waiver_for_birth_exception(self):
  self.reject(lambda o:o['records'][5]['source_qualified_guide']['prerequisites'].update(birth_branch_waives_prerequisites_proven=True))
 def test_no_executable_threshold_or_save_flag(self):
  self.reject(lambda o:o['records'][5]['source_qualified_guide']['prerequisites'].update(executable_level_predicate_or_quest_flag={'min_level':80}))
 def test_no_shell_consumption_or_check_invented(self):
  self.reject(lambda o:o['records'][5]['source_qualified_guide']['steps'][2].update(shell_consumption_or_handoff_explicitly_described=True))
 def test_no_fifty_year_absolute_date_or_quest_requirement(self):
  self.reject(lambda o:o['records'][1]['source_qualified_description'].update(absolute_world_year_or_release_date='1951'))
  self.reject(lambda o:o['records'][5]['source_qualified_guide'].update(story_relative_years_from_this_guide_alone=50))
 def test_no_bola_name_normalization(self):
  self.reject(lambda o:o['records'][5]['source_qualified_guide']['steps'][2].update(destination_label_as_written='波拉岛'))
 def test_no_little_boar_black_wuli_identity(self):
  self.reject(lambda o:o['boundaries'].update(little_black_boar_equals_black_wuli_verified=True))
 def test_no_descendant_quest_or_actor_identity(self):
  self.reject(lambda o:o['boundaries'].update(recovered25_himiko_yayoi_same_entities_verified=True))
 def test_no_server_npc_id_or_spawn(self):
  self.reject(lambda o:o['records'][6].update(original_game_entity_id_or_cross_build_identity=100))
  self.reject(lambda o:o['records'][8].update(original_server_map_id_or_spawn_or_look=[100,70,40]))
 def test_preserve_locator_as_written(self):
  self.reject(lambda o:o['records'][6].update(coordinate_string_as_written='56,124'))
 def test_no_pixel_acquisition_from_html_size(self):
  self.reject(lambda o:o['selected_map_reference'].update(actual_format_dimensions_capture_or_hash={'size':[580,468]}))
 def test_no_image_rect_to_world_route(self):
  self.reject(lambda o:o['boundaries'].update(world_map_html_rects_are_game_coordinates=True))
  self.reject(lambda o:o['boundaries'].update(island_panel_to_area_route_identity_inferred=True))
 def test_actual_hero_href_is_not_probed_root(self):
  self.reject(lambda o:o['known_hero_entry'].update(href='/zhuanqu/stoneage2/strategy/index.asp'))
 def test_unread_navigation_typo_kept(self):
  self.reject(lambda o:o['records'][5]['source_qualified_guide']['unread_sibling_navigation'][0].__setitem__(0,'寻找孙女'))
 def test_no_reward_pet_or_experience(self):
  self.reject(lambda o:o['records'][5]['source_qualified_guide'].update(item_master_id_reward_pet_or_experience={'pet':'红暴'}))
 def test_no_op_authorship_or_production_adoption(self):
  self.reject(lambda o:o['boundaries'].update(official_host_means_operator_authored_or_independent_witness=True))
  self.reject(lambda o:o['boundaries'].update(automatic_new_game_adoption=True))
 def test_exact_entry_required(self):
  with self.assertRaises((ValueError,AssertionError)):m.build(b'',m.ENTRY_URL,[])


if __name__=='__main__':unittest.main()
