import copy,json,unittest
from pathlib import Path
from tools import stoneage_tw10_graphic_upstream_p2b as probe
REPORT=Path(__file__).resolve().parents[1]/"research/recovered/STONEAGE-TW10-GRAPHIC-UPSTREAM-CANDIDATES-P2B-R1.json"
def check(d):
    assert d["schema"]=="stoneage.tw10.graphic-upstream-p2b.acceptance.r1"
    assert d["source_run"]["status"]=="completed" and d["source_run"]["conclusion"]=="success"
    assert d["source_run"]["zip_sha256"]=="f0bc6cb2851d253168dfd85d011548e9f5515a84149d476c30782865384d60f7"
    assert d["source_run"]["raw_json_sha256"]=="7ec6a7da6d915d410a839f70d9bf2bc1358253832a18da8f83050aa702818afd"
    assert d["prior_failed_attempt"]["conclusion"]=="failure" and d["prior_failed_attempt"]["counted_as_success"] is False
    assert d["facts"]["candidate_writes_0x124"]==len(d["facts"]["native_write_candidates"])==10
    assert d["facts"]["lexical_memory_displacement_references"]==45
    assert d["facts"]["lexical_0x124_references"]+d["facts"]["lexical_0x80_references"]==45
    assert len({i[0] for i in d["facts"]["native_write_candidates"]})==10
    assert [i[0] for i in d["facts"]["native_write_candidates"]]==[0x54cb,0x65ab,0x672b,0x7142,0x7466,0x7611,0x856d,0x10b8d,0x10c43,0x10ea5]
    assert all(len(i[1])==64 for i in d["facts"]["native_write_candidates"])
    assert d["boundaries"]["overall_restoration_percent"] is None
    assert all(v is False for k,v in d["boundaries"].items() if k!="overall_restoration_percent")
    assert d["facts"]["named_entities_confirmed"]==0
    ctx=probe.context()
    assert ctx["static_candidate_count"]==d["facts"]["physical_bitmap_candidates"]
    return True
class Acceptance(unittest.TestCase):
    def test_report(self):self.assertTrue(check(json.loads(REPORT.read_text())))
    def test_never_promote_naming_or_failures(self):
        j=json.loads(REPORT.read_text())
        for k,v in [("named_npc_bitmap",True),("source_original_executable_run",True),("overall_restoration_percent",100)]:
            d=copy.deepcopy(j);d["boundaries"][k]=v
            with self.assertRaises(AssertionError):check(d)
        d=copy.deepcopy(j);d["prior_failed_attempt"]["conclusion"]="success"
        with self.assertRaises(AssertionError):check(d)
        d=copy.deepcopy(j);d["facts"]["native_write_candidates"][0][0]=1
        with self.assertRaises(AssertionError):check(d)
if __name__=="__main__":unittest.main()
