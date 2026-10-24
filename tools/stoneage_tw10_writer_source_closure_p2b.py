"""Guard accepted derived native writer origin/source evidence, not names."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"research/recovered/STONEAGE-TW10-WRITER-SOURCE-CLOSURE-P2B-R1.json"
RVAS=["0x54cb","0x65ab","0x672b","0x7142","0x7466","0x7611","0x856d","0x10b8d","0x10c43","0x10ea5"]
CLASSES=["STACK_FRAME_MEMORY"]*7+["OTHER_MEMORY"]*2+["COMPUTED_OR_BITWISE"]
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def check(d=None):
    if d is None:d=json.loads(P.read_text())
    assert d["schema"]=="stoneage.tw10.writer_source_closure_p2b.r1"
    assert d["parent_git_blob"]=="a9adc6a94e8e062b730e0114df581c7b4ad20d62"
    original=(ROOT/"research/recovered/STONEAGE-TW10-GRAPHIC-UPSTREAM-CANDIDATES-P2B-R1.json").read_bytes()
    assert blob(original)==d["parent_git_blob"]
    parent=json.loads(original)
    assert [x[0] for x in parent["facts"]["native_write_candidates"]]==[int(x,16) for x in RVAS]
    assert d["action"]=={"run_id":40099299814,"job_id":120887951431,"head":"c333f6792fcd0720fa102f78c2fb9493220cd5f9","status":"completed","conclusion":"success","original_source_reacquired":True}
    a=d["artifact"]
    assert (a["id"],a["zip_bytes"],a["raw_bytes"])==(12562416023,2419,18564)
    assert a["zip_sha256"]=="aca92b0b8ee2cdf663ab65b4a1838c224cf99653e07ca73aea03c4d2b8473853"
    assert a["raw_sha256"]=="9f6170001e1696b0b24be6430c71490a932ebee4aa190b7562ebe4c7b10d3dc4"
    assert a["zip_independently_downloaded_and_hashed"] and not a["raw_full_text_in_git"]
    assert [x["rva"] for x in d["sites"]]==RVAS
    assert [x["nearest_local_value_source"] for x in d["sites"]]==CLASSES
    assert all(x["same_object_as_selector_proven"] is False for x in d["sites"])
    assert d["counts"]=={"candidate_native_writes":10,"stack_sources":7,"other_memory_sources":2,"arithmetic_sources":1,"named_entities_identified":0}
    assert all(v is (None if k=="overall_completion_percent" else False) for k,v in d["qualifications"].items())
    assert d["disposition"]=="STOP_GENERIC_NATIVE_SWEEPS_SWITCH_TO_AUTHENTIC_NAMED_SOURCE"
    assert len(d["reopen_triggers"])==3
    return True
if __name__=="__main__":
    check()
    print("P2B SOURCE CLOSURE PASS: 10 original writer sites and 7/2/1 lexical source classes; named identity OPEN")
