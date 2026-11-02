"""PET06 is an additive bounded original-pixel source update to PET05."""
import json,copy,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"research/recovered"
def rd(name):return json.loads((ROOT/name).read_text(encoding="utf-8"))
def check(old,new):
 assert old["schema"]=="stoneage.pet_module_05_consolidated_visual_coverage_over_later_source_templates.r1"
 assert new["schema"]=="stoneage.pet_module_06_consolidated_visual_coverage_source_additive.r1"
 assert new["evidence_limits"]["official_original_pet_species_count"] is None
 assert new["evidence_limits"]["original_game_runtime_entered"] is False
 assert new["evidence_limits"]["source_original_graphics_bulk_published"] is False
 assert new["evidence_limits"]["overall_completion_percent"] is None
 assert len(old["graphic_rows"])==len(new["graphic_rows"])==598
 assert len(old["template_rows"])==len(new["template_rows"])==1024
 changed={100297:(3,22,16),100298:(3,30,23)}
 for a,b in zip(old["graphic_rows"],new["graphic_rows"]):
  if a[0] in changed:
   count,frames,imgs=changed[a[0]]
   assert a[:3]==b[:3] and a[3:] == [False,0,0,0]
   assert b[3:]==[True,count,frames,imgs]
  else:assert a==b
 for a,b in zip(old["template_rows"],new["template_rows"]):
  assert a[:8]==b[:8]
  assert b[8] == (1 if a[2] in changed else a[8])
 c=new["counts"]
 assert c["source_petflag1_template_rows"]==1024
 assert c["server_graphic_candidate_keys"]==598
 assert [c[k] for k in ("private_gallery_qualified_original_pixel_graphics","private_gallery_qualified_template_source_rows","private_gallery_nonqualified_source_graphic_keys","source_visual_animation_sequences","source_visual_ordered_frame_occurrences","source_visual_distinct_original_png")]==[9,25,589,82,770,479]
 assert len(new["qualifying_private_original_pixel_groups"])==9
 assert new["private_artifacts"]["O28_zip"]["sha256"]=="2169cd77e9f9ad36327542ab2218d2d950325b916236c755cb0e67849f71168c"
 assert new["browser_validation"]["animation_sequence_selections_checked"]==82
class PET06(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.old=rd("STONEAGE-PET-MODULE-05-CONSOLIDATED-VISUAL-COVERAGE-R1.json")
  cls.new=rd("STONEAGE-PET-MODULE-06-CONSOLIDATED-VISUAL-COVERAGE-R1.json")
 def test_new_source_additive(self): check(self.old,self.new)
 def test_no_silent_extra_preview(self):
  b=copy.deepcopy(self.new);b["graphic_rows"][0][3]=True
  with self.assertRaises(AssertionError):check(self.old,b)
 def test_no_official_name(self):
  b=copy.deepcopy(self.new);b["evidence_limits"]["official_original_pet_species_count"]=9
  with self.assertRaises(AssertionError):check(self.old,b)
if __name__=="__main__":unittest.main()
