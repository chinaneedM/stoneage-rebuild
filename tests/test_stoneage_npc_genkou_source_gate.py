"""Synthetic-only structural negatives; no original NPC dialogues/assets in repository."""
import base64,hashlib,json,unittest
from tools.stoneage_npc_genkou_source_gate import analyze,InvalidEvidence,gitblob,POINTS,NUMS

def fixture():
    text="entype:2\naskbattlemsg1:XXX\nstartmsg:YYY\ndieact:0\nend msg:\nenemyno:"+",".join(map(str,NUMS))+"\ndeniedmsg:ZZZ\nonebattle:0\ntime:180\n"
    padding=258-len(text.encode())
    assert padding>=0
    text=text.replace("askbattlemsg1:XXX","askbattlemsg1:"+"X"*(3+padding))
    b=text.encode()
    assert len(b)==258
    dig=hashlib.sha256(b).hexdigest()
    arg={"kind":"file","path":"100/sb_kbu.arg","resolved":True,"size":258,
         "sha256":dig,"contentEncoding":"base64","contentBase64":base64.b64encode(b).decode()}
    rows=[]
    for ident,x,y,block,line in POINTS:
        rows.append({"id":ident,"x":x,"y":y,"name":"风的守护兽","functionOptions":[{
          "name":"原版 NPCEnemy","config":{"legacy":{
            "source":{"createFile":"100/sb_geno.create","createBlockIndex":block,
                      "createLine":line,"templateFile":"100/sb_geno.template",
                      "templateLine":3,"matchConfidence":"exact"},
            "templateName":"sb_kbu","functionset":"NPCEnemy",
            "enemy":"sb_kbu|file:100/sb_kbu.arg","arguments":[dict(arg)]}}}]})
    return rows,dig

def dump(rows):
    return ("format: sa-map-entity-v2\nmap_id: 11208\nnpcs:\n"+
            "".join("  - "+json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n" for r in rows)+
            "warps:\n"+
            "".join("  - "+json.dumps({"id":i,"trigger":"step"},ensure_ascii=False,separators=(",",":"))+"\n" for i in (1,2,3))+
            "interactives: []\n").encode()

class NegativeCases(unittest.TestCase):
    def setUp(self):self.rows,self.sha=fixture()
    def check(self,rows,raw=None,override_blob=None):
        raw=raw or dump(rows)
        return analyze(raw,source_sha=override_blob or gitblob(raw),arg_sha=self.sha)
    def bad(self,change):
        rows,_=fixture();change(rows)
        with self.assertRaises(InvalidEvidence):self.check(rows)
    def test_positive(self):
        a=self.check(self.rows)
        self.assertEqual(a["enemy_numbers_distinct"],6)
        self.assertEqual(len(a["modern_npc_occurrences"]),2)
        self.assertFalse(a["certified_same_official_build"])
        self.assertIsNone(a["certified_original_quest_id"])
    def test_source_digest_lease(self):
        raw=dump(self.rows)
        with self.assertRaises(InvalidEvidence):self.check(self.rows,raw+b"\n",gitblob(raw))
    def test_mutated_name(self):self.bad(lambda r:r[0].update(name="已认证"))
    def test_mutated_position(self):self.bad(lambda r:r[0].update(x=27))
    def test_lost_occurrence(self):self.bad(lambda r:r.pop(1))
    def test_duplicate_id(self):self.bad(lambda r:r[1].update(id=4))
    def test_function(self):self.bad(lambda r:r[0]["functionOptions"][0].update(name="Test"))
    def test_template(self):self.bad(lambda r:r[0]["functionOptions"][0]["config"]["legacy"].update(templateName="wrong"))
    def test_file_path(self):self.bad(lambda r:r[0]["functionOptions"][0]["config"]["legacy"]["source"].update(createFile="wrong"))
    def test_source_line(self):self.bad(lambda r:r[0]["functionOptions"][0]["config"]["legacy"]["source"].update(createLine=99))
    def test_wrong_sha(self):self.bad(lambda r:r[0]["functionOptions"][0]["config"]["legacy"]["arguments"][0].update(sha256="0"*64))
    def test_payload_mutation(self):self.bad(lambda r:r[0]["functionOptions"][0]["config"]["legacy"]["arguments"][0].update(contentBase64="!!!!"))
    def test_schema_promotion(self):
        raw=dump(self.rows).replace(b"sa-map-entity-v2",b"official-game-master")
        with self.assertRaises(InvalidEvidence):self.check(self.rows,raw=raw)

if __name__=="__main__":unittest.main()
