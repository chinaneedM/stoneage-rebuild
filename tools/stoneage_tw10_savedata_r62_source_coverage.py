"""R62: source-only post-WriteFile operand coverage across retained R27–R58 reports.

Enumerates accepted research surfaces, not executable instructions from an original client.
A site/address mention is never equivalent to decoded operands or feasible runtime behavior.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

SCHEMA = "tw10-r62-retained-report-postcall-operand-coverage"
NAME = re.compile(r"^STONEAGE-TW10-SAVEDATA-NATIVE-IO-R(\d+)-(ORIGINAL|DERIVED|SPEC)\.json$")
SITES = (0x4C692, 0x4C6F7)
CONTROL = {
    28: "3671661219120d45bd922e05b6df371523b42432",
    44: "39c1c0f673747fb560cc285d627490e5cd38047a",
    45: "1e7fb71cec336c1b4fc531d4f4a6933c9f66d415",
}
def need(ok, why):
    if not ok:
        raise ValueError("R62 source-coverage: "+why)
def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()

def collect(report):
    """Identify site-bearing metadata separately from full mnemonic+operand rows."""
    mentions={str(site): [] for site in SITES}
    full={str(site): [] for site in SITES}
    def visit(x, loc, depth):
        need(depth < 45, "unexpected nested report depth")
        if isinstance(x, dict):
            site=x.get("site_rva")
            if site in SITES and isinstance(site,int):
                label=str(site)
                mentions[label].append(loc)
                if isinstance(x.get("mnemonic"),str) and x["mnemonic"] and isinstance(x.get("operands"),list):
                    full[label].append({"path":loc,"mnemonic":x["mnemonic"],"operand_count":len(x["operands"])})
            for k,v in x.items():
                if isinstance(v,(list,dict)): visit(v,loc+"."+str(k),depth+1)
        elif isinstance(x,list):
            for i,v in enumerate(x):
                if isinstance(v,(dict,list)):visit(v,loc+"["+str(i)+"]",depth+1)
    visit(report,"$",0)
    return mentions,full

def analyze_sources(sources):
    """sources maps registered filename to raw JSON bytes; no original bytes are accepted."""
    names={}
    versions={}
    for filename,raw in sources.items():
        m=NAME.match(filename)
        need(m is not None and 27<=int(m.group(1))<=58,"unexpected report filename")
        n=int(m.group(1))
        need(n not in versions,"duplicate versioned report")
        versions[n]=filename
        names[filename]=raw
    need(set(versions)==set(range(27,59)),"not the complete retained R27-R58 report-series coverage")
    for n,expected in CONTROL.items():
        need(git_blob(names[versions[n]])==expected,"pinned R"+str(n)+" source custody")
    summary=[]
    full_totals={str(i):[] for i in SITES}
    mention_totals={str(i):0 for i in SITES}
    for n in sorted(versions):
        filename=versions[n]
        raw=names[filename]
        try:
            report=json.loads(raw)
        except Exception as e:
            raise ValueError("R62 invalid derived JSON R"+str(n)) from e
        mentions,full=collect(report)
        summary.append({
            "report":"R"+str(n), "file":filename, "git_blob":git_blob(raw),
            "postcall_site_mentions":{s:len(mentions[s]) for s in mentions},
            "full_instruction_shape_hits":{s:full[s] for s in full},
        })
        for s in mention_totals:
            mention_totals[s]+=len(mentions[s])
            for hit in full[s]:
                full_totals[s].append({"report":"R"+str(n),**hit})

    report28=json.loads(names[versions[28]])
    w=next(x for x in report28["contexts"] if x["api"]=="WriteFile")
    need(w["root_candidate_rva"]==0x4C5B4 and w["graph"]["nodes"]==139 and
         w["graph"]["edges"]==156 and not w["graph"]["frontier"],"R28 bounded write root")
    for site, after in ((0x4C68C,SITES[0]),(0x4C6F1,SITES[1])):
        rows=[q for q in w["inputs"]["queries"] if q["site_rva"]==after and q["register"]=="eax"]
        need(len(rows)==1 and rows[0]["reaching_candidates"]==[
            {"origin":"unknown_call","rva":site,"semantic":None}
        ] and rows[0]["actual_register_value_known"] is False, "R28 EAX opaque")
    report44=json.loads(names[versions[44]])
    c44=next(x for x in report44["native_contexts"] if x["native_root_candidate_rva"]==0x4C5B4)
    stack_sites={x["site_rva"] for x in c44["inherited_stack_effect_candidates"]}
    need(set(SITES)<=stack_sites and
         report44["actual_esp_stack_contents_or_frame_preservation_proven"] is False,
         "R44 partial stack-site metadata is not ABI proof")
    report45=json.loads(names[versions[45]])
    c45=next(x for x in report45["native_api_contexts"] if x["site_rva"]==0x4C68C)
    need(set(SITES)<=set(c45["bounded_node_rvas"]) and
         report45["actual_write_frame_preservation_or_callee_effects_proven"] is False,
         "R45 candidate graph does not prove call preservation")
    return {
        "schema":SCHEMA, "registered_original_derived_report_versions":"R27-R58",
        "report_count":len(summary),"reports":summary,
        "postcall_sites_rva":list(SITES),
        "postcall_site_metadata_mentions":mention_totals,
        "decoded_postcall_operand_rows_found":full_totals,
        "all_decoded_postcall_instruction_rows_missing_from_registered_reports":
            all(not full_totals[str(s)] for s in SITES),
        "site_mentions_are_not_instruction_operands_or_execution":True,
        "source_reuse_precedes_narrow_original_derived_probe":True,
        "actual_native_return_count_or_callee_abi_proven":False,
        "actual_savedata_write_flush_close_or_persistence_proven":False,
        "original_executable_or_save_payload_executed":False,
        "next":"If decoded rows are absent, nonexecuting targeted 0x4c692/0x4c6f7 operand/branch/flag and caller-ABI inventory; otherwise reuse pinned rows first."
    }

def load_directory(path):
    out={}
    for f in path.glob("STONEAGE-TW10-SAVEDATA-NATIVE-IO-R*.json"):
        if NAME.match(f.name):
            out[f.name]=f.read_bytes()
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--directory",type=Path,default=Path("research/recovered"))
    p.add_argument("--verify",type=Path)
    a=p.parse_args()
    d=analyze_sources(load_directory(a.directory))
    if a.verify:
        need(d==json.loads(a.verify.read_text()),"coverage replay drift")
        print("TW10_R62_SOURCE_DISCOVERY=PASS; ORIGINAL_NATIVE_PERSISTENCE=OPEN")
    else:
        print(json.dumps(d,sort_keys=True))

if __name__=="__main__":
    main()
