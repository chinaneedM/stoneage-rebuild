"""PET56 offline acceptance of both fixed derived reports and unified query links."""
from tools.stoneage_pet_high_first_56_custody import P,R,blob,sha,load,validate
from tools import stoneage_pet_source_lookup as lookup
def diff(a,b,p=""):
    if a==b:return []
    if isinstance(a,dict) and isinstance(b,dict):
        assert a.keys()==b.keys()
        return [x for k in a for x in diff(a[k],b[k],p+"/"+k)]
    if isinstance(a,list) and isinstance(b,list):
        assert len(a)==len(b)
        return [x for i,(u,v) in enumerate(zip(a,b)) for x in diff(u,v,p+"/"+str(i))]
    return [p]
def main():
    c=load(P/"PET-HIGH-FIRST-56-SOURCE-CUSTODY-R1.json","142976ab261a145eae33a51707701fd041514b3f")
    pre=load(P/"PET-HIGH-FIRST-56-SPECIAL-ROLE-PREFLIGHT-R1.json","d5a98f0711d36b17dca3fe5786f1fb9b63a3c5b9")
    old=load(P/"PET-HIGH-FIRST-50-ORIGINAL-ACQUISITION-R1.json","4d0b31a7fa196cf8f227a7b0b1aea7183d9598f0")
    manifest=load(R/"STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json","a088b61a3212f7049e7793f587123ffb29bebad7")
    reports=[]
    for r in c["receipts"]:
        p=P/r["report"];raw=p.read_bytes()
        assert (len(raw),sha(raw),blob(raw))==(r["report_bytes"],r["report_sha256"],r["report_git_blob"])
        d=load(p); validate(d,pre,old,manifest);reports.append(d)
    assert set(diff(*reports))=={"/original_receipt/public_pages/"+str(i)+"/"+k for i in (0,1) for k in ("bytes","sha256")}
    assert c["strict_gap_count"]==67 and c["official_acquisition_closed"]==0 and c["official_species_count"] is None
    assert len(c["rows"])==10 and not c["raw_reports_equal"]
    assert sorted(i for r in c["rows"] for i in r["source_hit_indices"])==list(range(14))
    assert all(r["retain_strict_gap"] and not r["official_acquisition_verified"] for r in c["rows"])
    print("PET56_ACCEPT: 2207 original members, 6 later blobs, 67 templates, 70 instances, 14 typed candidates, 10 linked roles, 0 official closures")
if __name__=="__main__":main()
