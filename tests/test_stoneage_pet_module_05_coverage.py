"""Cross-check PET05 source-bounded preview against PET01 / PET03 archived numeric facts."""
import json,copy,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"research/recovered"
def data(n):return json.loads((ROOT/n).read_text(encoding="utf-8"))
def validate(d,src,skill):
 assert d["schema"]=="stoneage.pet_module_05_consolidated_visual_coverage_over_later_source_templates.r1"
 assert d["evidence_limits"]["official_original_pet_species_count"] is None
 assert d["evidence_limits"]["original_game_runtime_entered"] is False
 assert d["evidence_limits"]["source_original_graphics_bulk_published"] is False
 assert d["evidence_limits"]["overall_completion_percent"] is None
 G=src["graphic_registry"];T=src["petflag1_template_tuples"];S={x[0]:x for x in skill["source_template_rows"]}
 assert len(G)==len(d["graphic_rows"])==598 and len(T)==len(d["template_rows"])==1024
 graphics={r[0]:r for r in G}
 previews={r["graphic_id"]:r for r in d["qualifying_private_original_pixel_groups"]}
 assert set(previews)=={100250,100251,100252,100327,100328,100329,100330}
 for source,encoded in zip(G,d["graphic_rows"]):
  ident,lines,tw,cn,tw85,mixed,hashes=source
  expect=[ident,len(lines),[len(tw),len(cn),len(tw85),len(mixed)],ident in previews,previews[ident]["sequences"] if ident in previews else 0,previews[ident]["frames"] if ident in previews else 0,previews[ident]["unique_bitmaps"] if ident in previews else 0]
  assert encoded==expect
 for t,record in zip(T,d["template_rows"]):
  s=S[t[0]];g=graphics[t[2]]
  assert record==[t[0],t[1],t[2],t[15],s[3],s[4],s[5],[len(x) for x in g[2:6]],int(t[2] in previews)]
 c=d["counts"]
 assert c["source_petflag1_template_rows"]==1024 and c["server_graphic_candidate_keys"]==598
 assert c["server_graphic_candidates_with_any_client_index"]==542
 assert c["server_graphic_candidates_no_index_in_four_samples"]==56
 assert [c[k] for k in ("graphic_candidate_index_matches_tw1","graphic_candidate_index_matches_cn5","graphic_candidate_index_matches_tw85","graphic_candidate_index_matches_mixed25")]==[130,344,542,260]
 assert c["private_gallery_qualified_original_pixel_graphics"]==7
 assert c["private_gallery_qualified_template_source_rows"]==22
 assert c["private_gallery_nonqualified_source_graphic_keys"]==591
 assert [c[k] for k in ("source_visual_animation_sequences","source_visual_ordered_frame_occurrences","source_visual_distinct_original_png")]==[76,718,440]
 assert [c[k] for k in ("source_template_positive_skill_slots","source_template_skills_matched","source_template_skills_missing")]==[2886,2784,102]
class Pet05(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=data("STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json")
  cls.skill=data("STONEAGE-PET-MODULE-03-SAME-SOURCE-SKILL-JOIN-R1.json")
  cls.r=data("STONEAGE-PET-MODULE-05-CONSOLIDATED-VISUAL-COVERAGE-R1.json")
 def test_full_catalog(self):validate(self.r,self.src,self.skill)
 def test_denies_unobserved_promotion(self):
  b=copy.deepcopy(self.r);b["graphic_rows"][0][3]=True
  with self.assertRaises(AssertionError):validate(b,self.src,self.skill)
 def test_denies_species_claim(self):
  b=copy.deepcopy(self.r);b["evidence_limits"]["official_original_pet_species_count"]=598
  with self.assertRaises(AssertionError):validate(b,self.src,self.skill)
 def test_denies_dropped_skill_deficit(self):
  b=copy.deepcopy(self.r);b["template_rows"][0][5]+=1
  with self.assertRaises(AssertionError):validate(b,self.src,self.skill)
if __name__=="__main__":unittest.main()
