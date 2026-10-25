"""Bounded modern source-byte replay; does not certify StoneAge 1999/TW1.0 NPCs."""
import argparse, base64, binascii, hashlib, json
from pathlib import Path

SOURCE_SHA="6e066821bedd0bbef7e59cc3f020cad7783e51c5"
ARG_SHA="961b87cebad2fd7cb7875f9433df0e301f9f64b06c46a558475fc1a0344e9eec"
POINTS=((4,26,40,0,3),(5,42,38,1,14))
NUMS=(1272,1277,1277,1280,1280,1278,1273,1273,1275,1275)
KEYS=("entype","askbattlemsg1","startmsg","dieact","end msg","enemyno","deniedmsg","onebattle","time")

class InvalidEvidence(ValueError):pass

def gitblob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def analyze(raw,source_sha=SOURCE_SHA,arg_sha=ARG_SHA):
    if gitblob(raw)!=source_sha:raise InvalidEvidence("source git blob mismatch")
    try:
        lines=raw.decode("utf-8").splitlines()
        if lines[:3]!=["format: sa-map-entity-v2","map_id: 11208","npcs:"]:
            raise InvalidEvidence("source schema changed")
        if any(x and not x.startswith("  - {") for x in lines[3:]):
            raise InvalidEvidence("source entry layout changed")
        npc=[json.loads(x[4:]) for x in lines[3:] if x.startswith("  - {")]
    except (UnicodeDecodeError,json.JSONDecodeError) as e:
        raise InvalidEvidence("unparseable modern export") from e
    if len(npc)!=5 or len({x["id"] for x in npc})!=5:
        raise InvalidEvidence("unexpected npc count or duplicate id")
    hits=[x for x in npc if x.get("name")=="风的守护兽"]
    if len(hits)!=2:raise InvalidEvidence("guardian count changed")
    for r,(ident,x,y,block,line) in zip(hits,POINTS):
        if (r.get("id"),r.get("x"),r.get("y"))!=(ident,x,y):
            raise InvalidEvidence("instance identity changed")
        ops=r.get("functionOptions")
        if not isinstance(ops,list) or len(ops)!=1:
            raise InvalidEvidence("expected single function")
        op=ops[0]
        l=op.get("config",{}).get("legacy",{})
        z=l.get("source",{})
        if (op.get("name"),l.get("templateName"),l.get("functionset"),l.get("enemy"))!=(
            "原版 NPCEnemy","sb_kbu","NPCEnemy","sb_kbu|file:100/sb_kbu.arg"):
            raise InvalidEvidence("template/function claim changed")
        if (z.get("createFile"),z.get("createBlockIndex"),z.get("createLine"),
            z.get("templateFile"),z.get("templateLine"),z.get("matchConfidence"))!=(
            "100/sb_geno.create",block,line,"100/sb_geno.template",3,"exact"):
            raise InvalidEvidence("upstream path/block claim changed")
        a=l.get("arguments",[])
        if not isinstance(a,list) or len(a)!=1:raise InvalidEvidence("expected one argument")
        a=a[0]
        if (a.get("kind"),a.get("path"),a.get("resolved"),a.get("size"),
            a.get("sha256"),a.get("contentEncoding"))!=(
            "file","100/sb_kbu.arg",True,258,arg_sha,"base64"):
            raise InvalidEvidence("argument metadata changed")
        try:
            payload=base64.b64decode(a["contentBase64"],validate=True)
            decoded=payload.decode("gb18030")
        except (KeyError,binascii.Error,UnicodeDecodeError,ValueError) as e:
            raise InvalidEvidence("bad encoded argument") from e
        if len(payload)!=258 or hashlib.sha256(payload).hexdigest()!=arg_sha:
            raise InvalidEvidence("embedded bytes don't match digest")
        pairs=[s.split(":",1) for s in decoded.splitlines()]
        if tuple(k for k,v in pairs)!=KEYS:raise InvalidEvidence("field structure changed")
        fields=dict(pairs)
        if ((fields["entype"],fields["dieact"],fields["onebattle"],fields["time"])!=
            ("2","0","0","180") or
            tuple(int(n) for n in fields["enemyno"].split(","))!=NUMS):
            raise InvalidEvidence("numeric values changed")
        if any(not fields[n] for n in ("askbattlemsg1","startmsg","deniedmsg")) or fields["end msg"]:
            raise InvalidEvidence("dialogue boundary changed")
    return {
      "schema":"stoneage.npc_genkou_derived_arg_source.r1",
      "kind":"MODERN_COMMUNITY_DERIVED_BYTES_NOT_OFFICIAL",
      "upstream_commit":"e9b3f0cfd63b93c11fc77ca5331173dd6c5d2fc8",
      "upstream_file":"map/maps/11208/map.entity.yaml",
      "upstream_blob":source_sha,
      "modern_map":11208,"modern_npc_rows":5,
      "modern_npc_occurrences":[{"id":i,"x":x,"y":y,"create_block_index":b,"create_line":ln}
                                for i,x,y,b,ln in POINTS],
      "embedded_path":"100/sb_kbu.arg",
      "embedded_length":258,"embedded_sha256":arg_sha,
      "field_names":list(KEYS),
      "enemy_number_occurrences":list(NUMS),"enemy_numbers_distinct":len(set(NUMS)),
      "jss_2000_04_24_own_notice":"R116 separate first-party source: named cave progression correction",
      "certified_same_official_build":False,
      "certified_original_npc_id":None,"certified_original_quest_id":None,
      "original_server_execution":False,
      "origin_class":"ORIGIN_UNRESOLVED",
      "verified_base_quests_added":0,"overall_restoration_percentage":None
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=json.dumps(analyze(a.source.read_bytes()),ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output:a.output.write_text(result,encoding="utf-8")
    else:print(result,end="")

if __name__=="__main__":main()
