import json, unittest, copy
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
def validate(batch,d):
 c=d["counts"]; rows=d["code_rows"]
 assert d["schema"]=="stoneage.pet_module_04_skillcode_source_bounded_crosswalk.r1"
 assert d["limits"]["pet_skill_eligibility_or_learning_proven"] is False
 assert d["limits"]["overall_restoration_percent"] is None
 im={}
 for line,i,t,a,b,k in batch["enemy_instances"]: im.setdefault(i,set()).add(t)
 p=Counter(x[1] for x in batch["petflag1_template_tuples"])
 n=Counter(x[1] for x in batch["petflag0_template_refs"])
 seen=Counter(); pairs=Counter(); codes=Counter()
 assert len(rows)==c["rows"]==253
 for line,i,t,s,status,actual,p1,p0 in rows:
  assert line==len(seen)+1
  seen[line]+=1
  assert actual==sorted(im.get(i,set()))
  expect="MATCH" if t in im.get(i,set()) else ("MISMATCH" if i in im else "ABSENT")
  assert status==expect and p1==p[t] and p0==n[t]
  assert s.endswith("&") and (len(s)-1)%2==0
  toks=[s[j:j+2] for j in range(0,len(s)-1,2)]
  assert toks and len(toks)==len(set(toks))
  for x in toks: assert len(x)==2 and x.isascii() and x.isalpha(); codes[x]+=1
  pairs[(i,t)]+=1
 assert c["MATCH"]==sum(r[4]=="MATCH" for r in rows)==160
 assert c["MISMATCH"]==sum(r[4]=="MISMATCH" for r in rows)==12
 assert c["ABSENT"]==sum(r[4]=="ABSENT" for r in rows)==81
 assert c["template_petflag1"]==sum(r[6]>0 for r in rows)==171
 assert c["template_only_petflag0"]==sum(r[6]==0 and r[7]>0 for r in rows)==4
 assert c["template_absent"]==sum(r[6]==0 and r[7]==0 for r in rows)==78
 assert c["unique_pairs"]==len(pairs)==250
 assert c["duplicate_pair_excess"]==sum(v-1 for v in pairs.values())==3
 assert c["unique_instance_ids"]==len({r[1] for r in rows})==250
 assert c["unique_strings"]==len({r[3] for r in rows})==47
 assert c["code_tokens"]==len(codes)==79
 kind={}
 for line,skillid,code in d["skill_kindcode_rows"]: kind.setdefault(code,[]).append(skillid)
 assert len(d["skill_kindcode_rows"])==c["skill_rows_with_kindcode"]
 assert len(kind)==c["distinct_skill_kindcodes"]
 assert len(d["non_two_letter_skill_kindcodes"])==c["non_two_letter_kindcodes"]
 assert d["code_lookup"]==[[k,codes[k],sorted(kind[k])] for k in sorted(codes)]
class PET04Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.b=json.loads((ROOT/"research/recovered/STONEAGE-PET-MODULE-01-BATCH-SOURCE-SPR-INDEX-R1.json").read_text())
  cls.d=json.loads((ROOT/"research/recovered/STONEAGE-PET-MODULE-04-SKILLCODE-CROSSWALK-R1.json").read_text())
 def test_full_numeric_conservation(self): validate(self.b,self.d)
 def test_conflict_not_autofixed(self):
  x=copy.deepcopy(self.d); next(r for r in x["code_rows"] if r[4]=="MISMATCH")[4]="MATCH"
  with self.assertRaises(AssertionError): validate(self.b,x)
 def test_unsupported_runtime_promotion_rejected(self):
  x=copy.deepcopy(self.d); x["limits"]["pet_skill_eligibility_or_learning_proven"]=True
  with self.assertRaises(AssertionError): validate(self.b,x)
if __name__=="__main__": unittest.main()
