from copy import deepcopy
import json
import unittest
from tools import stoneage_waei_hero_source_relations as m


class SourceRelationsTests(unittest.TestCase):
 def setUp(self):self.o=json.loads(m.REPORT.read_bytes())
 def reject(self, change):
  o=deepcopy(self.o);change(o)
  with self.assertRaises((ValueError,AssertionError)):m.validate_report(o)
 def test_exact_six_relations_and_resolvable_pointers(self):m.validate_report(self.o)
 def test_no_shared_release_or_build(self):
  self.reject(lambda o:o['records'][0]['source_scoped_values'].update(same_official_release_or_build='TW2.0'))
 def test_no_locator_snap_or_interaction_radius(self):
  self.reject(lambda o:o['records'][1]['source_scoped_values'].update(offset_map_or_same_entity='one tile interaction offset'))
  self.reject(lambda o:o['boundaries'].update(coordinate_offset_or_interaction_radius_derived=True))
 def test_no_same_name_entity_merge(self):
  self.reject(lambda o:o['records'][1].update(game_entity_identity_or_new_rule='SAME_NPC'))
 def test_unnamed_flower_cannot_inherit_item_id(self):
  self.reject(lambda o:o['records'][2]['source_scoped_values'].update(guide_flower_equals_item_2415=True))
 def test_shell_label_cannot_inherit_item_id(self):
  self.reject(lambda o:o['records'][2]['source_scoped_values'].update(guide_shell_equals_item_2414=True))
 def test_empty_item_atoms_not_unconditional(self):
  self.reject(lambda o:o['records'][3]['source_scoped_values'].update(zero_item_atoms_proves_unconditional_or_no_level_requirement=True))
 def test_fish_birth_not_found_in_incomplete_config(self):
  self.reject(lambda o:o['records'][3]['source_scoped_values'].update(source_described_fish_route_proves_descendant_birth_condition=True))
 def test_two_npc_sample_not_whole_bundle_absence(self):
  self.reject(lambda o:o['records'][4]['source_scoped_values'].update(black_wuli_missing_from_entire_bundle_or_game_proven=True))
 def test_access_does_not_invent_shell_consumption(self):
  self.reject(lambda o:o['records'][4]['source_scoped_values'].update(shell_check_or_consumption_at_hero_entry_verified=True))
 def test_opposite_exchange_not_patch_or_conflict(self):
  self.reject(lambda o:o['records'][5]['source_scoped_values'].update(opposite_direction_is_contradiction_or_patch_order_proven=True))
 def test_fixed_metadata_pins(self):
  blobs=[__import__('pathlib').Path(p).read_bytes() for p,_ in m.INPUTS];blobs[1]+=b' '
  with self.assertRaises((ValueError,AssertionError)):m.build(blobs)


if __name__=='__main__':unittest.main()
