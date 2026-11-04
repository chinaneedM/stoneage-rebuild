"""WORLD07: source-pinned later GETPET handler, distinct from mixed25 archived scripts.
CI fetches original UTF-8/legacy C bytes from a fixed public GitHub commit, then
verifies native Git blob identity. Does NOT execute a commercial server.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"research"/"recovered"
NAMES={
    "npc_exchangeman.c":"7a9cc7ea6d76bfdae367c580db4ce6fcb42d7d15",
    "enemy.c":"72e43f44a76db4baa23dfcea568f16d54d3bf620",
    "setup.cf":"9d5992bfb1065d6c405ebe4a0677acb7be0de5f9",
}

def read(name):return json.loads((DATA/name).read_text(encoding="utf-8"))
def git_blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\x00"+raw).hexdigest()

def function_body(source,signature):
    m=re.search(signature+ r"\s*\{",source,re.S)
    if not m: raise AssertionError("Missing true definition: "+signature)
    a=m.end()-1
    depth=0
    for k in range(a,len(source)):
        if source[k]=="{": depth+=1
        elif source[k]=="}":
            depth-=1
            if depth==0:return source[a:k+1]
    raise AssertionError("Missing function closing brace")

class World07GetPet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w=read("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-07-GETPET-HANDLER-SOURCE-SEMANTICS-R1.json")
        cls.g=read("STONEAGE-GAMEPLAY07-GETPET-NPCENEMY-ORIGINAL-SKILL-SOURCE-R1.json")
        cls.w05=read("STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-05-GETPET-INSTANCE-TEMPLATE-SPR-R1.json")
    def test_29_original_directives_and_exact_preserved_duplicates(self):
        src=sorted((x["original_source_relative_path"],f["original_source_physical_line"],
                    f["source_line_sha256"],tuple(f["source_integer_tokens_ordered"]))
                   for x in self.g["source_GetPet_original_NPC_files"] for f in x["script_commands"])
        actual=sorted((x["original_source_path"],x["original_line_1based"],
                       x["original_line_sha256"],tuple(x["original_GETPET_integer_literals_in_order"]))
                      for x in self.w["original_GETPET_source_lines"])
        self.assertEqual(actual,src)
        m=self.w["source_derived_crosscheck"]["original_script_summary"]
        self.assertEqual((len(actual),sum(len(x[3]) for x in actual),len({n for x in actual for n in x[3]})),
                         (29,44,36))
        self.assertEqual(m["source_multi_integer_directive_lines"],4)
        self.assertEqual(m["original_CREATE_static_refs"],24)
        self.assertEqual(m["wrong_direct_enemybase_integer_ID_collisions"],26)
        self.assertEqual(m["two_template_PETFLG_conflicts"],3)
        self.assertTrue(m["preserved_dupe_482_syntax"])
        self.assertEqual(sorted(m["original_backup_script_paths"]),
                         ["giiru/event/event30_5.old","quiz/equiz_04.BAK"])
        self.assertEqual(set(n for x in actual for n in x[3]),
                         {x["source_GETPET_literal_numeric"] for x in self.w05["GETPET_instance_template_graph"]})
    def test_source_provenance_and_no_history_promotion(self):
        w=self.w
        self.assertEqual(w["pinned_later_source"]["repository"],"pimpcapital/longzoro-sa")
        self.assertEqual(w["pinned_later_source"]["commit"],"57b14e2bb373ba851c14db28a239273e4a8831bb")
        self.assertEqual([x["git_blob_sha"] for x in w["pinned_later_source"]["files"]],list(NAMES.values()))
        self.assertTrue(all(w["critical_boundaries"].values()))
        self.assertEqual(w["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual((w["stage_B"],w["wiki"],w["R79"]),("GATED","GATED","PAUSED_NON_BLOCKING"))
        self.assertIsNone(w["overall_percent"])
        self.assertEqual(w["full_historical_CURRENT_Git_blob_sha"],
                         "c89e0e33537990aa2132b47c40fef49a985a935c")
    def test_exact_pinned_C_functions_in_source_when_available(self):
        directory=os.environ.get("STONEAGE_WORLD07_PINNED_SOURCE_DIR")
        if not directory:self.skipTest("No external C source supplied: derived-only local test")
        d=Path(directory)
        raw={p:(d/p).read_bytes() for p in NAMES}
        for p,s in NAMES.items():self.assertEqual(git_blob_sha(raw[p]),s)
        a=raw["npc_exchangeman.c"].decode("latin-1")
        b=raw["enemy.c"].decode("latin-1")
        setup=raw["setup.cf"].decode("latin-1")
        add=function_body(a,r"BOOL\s+NPC_EventAddPet\s*\(int\s+meindex,\s*int\s+talker,\s*char\s*\*buff2,\s*int\s+mode\)")
        from_enemy=function_body(b,r"int\s+ENEMY_createPetFromEnemyIndex\s*\(\s*int\s+charaindex,\s*int\s+array\)")
        init_enemy=function_body(b,r"BOOL\s+ENEMY_initEnemy\s*\(\s*char\s*\*filename\s*\)")
        temp_array=function_body(b,r"int\s+ENEMYTEMP_getEnemyTempArray\s*\(\s*int\s+enemyindex\)")
        self.assertGreaterEqual(a.count('NPC_Util_GetStrFromStrWithDelim( buff, "GetPet"'),1)
        self.assertIn('NPC_EventAddPet( meindex, talker, buff2,0)',a)
        self.assertIn('NPC_EventAddPet( meindex, talker, buff2,1)',a)
        for term in ['CHAR_MAXPETHAVE','strstr(buff2,",")','rand()%i + 1',
                     'enemyid = atoi( buf2)','enemyid = atoi( buff2)',
                     'ENEMY_getEnemyNum()','ENEMY_getInt( i, ENEMY_ID) == enemyid',
                     'ENEMY_createPetFromEnemyIndex( talker, i)',
                     'CHAR_ENDEVENT']:
            self.assertIn(term,add)
        for term in ['ENEMYTEMP_getEnemyTempArray( array)',
                     'E_T_IMGNUMBER','E_T_PETSKILL1','CHAR_PETID',
                     'CHAR_setCharPet( charaindex, havepetelement, newindex)']:
            self.assertIn(term,from_enemy)
        self.assertIn('ENEMY_TEMPNO',init_enemy)
        self.assertIn('enemytemparray = i',init_enemy)
        self.assertIn('ENEMY_enemy[enemyindex].enemytemparray',temp_array)
        self.assertIn('enemyfile=./data/enemy1.txt',setup)
        self.assertIn('enemybasefile=./data/enemybase1.txt',setup)
if __name__=="__main__":unittest.main()
