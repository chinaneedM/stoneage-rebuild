"""O60: verify source-qualified derivative only, with R18 immutable file pins."""
import copy,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"research/recovered/STONEAGE-O60-FOUR-VILLAGE-NOVICE-MENTORS-SOURCE-R1.json"
R18=ROOT/"research/recovered/STONEAGE-MIXED25-SERVER-FULL-SOURCE-R18.json"
def check(d,r18):
    def must(x): 
        if not x:raise ValueError("O60 source identity, mapping or historical gate")
    must(d["schema"]=="stoneage.o60.four_village_two_novice_teaching_scripts_and_map_cell_anchor.r1")
    must(d["source_scope"].endswith("NOT_JSS1999_TW10_OFFICIAL_DEPLOYMENT"))
    b=d["remote_base"];must(b["current_blob"]=="20050acf279a01555ab06a381dfcdc936bd381a6" and b["current_file_size_bytes"]==2708031 and b["preserved_unchanged"] is True)
    p=d["private_archive"];must((p["bytes"],p["sha256"],p["read_whole_sha_verified_this_round"])==(361255180,"d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5",True))
    pins={
        "npc/sa60/newbie/newbie.create":(6575,1548,"761dc3d1ed885fb76b22af446331e5a0db6cf3e59a27cf2ab136a62a88d81d0b","3f411954"),
        "npc/sa60/newbie/fighter":(6573,1432,"5cba22d6c22387b1b28576ab09d59989c3068d44c82e964da753caf4f9252289","20da5958"),
        "npc/sa60/newbie/petmaster":(6578,1365,"04ba49ba514eb469b4c12085c6733cd73c281c6ca682c813c2e35748ab6ac1db","e63fc8d8")
    }
    old={x["path"]:x for x in r18["all_server_occurrences"]}
    for path,expected in pins.items():
        f=d["private_original_file_receipts"][path]
        must((f["rar_index_zero_based"],f["bytes"],f["sha256"],f["rar_crc32"])==expected)
        must((old[path]["size"],old[path]["sha256"])==(f["bytes"],f["sha256"]))
    must(d["exact_creator_block_count"]==8 and d["all_creator_blocks_cp950_roundtrip"] is True and d["all_source_files_crc_sha_and_prior_R18_manifest_match"] is True)
    rows=d["teacher_creations"]
    expected=[
      (1000,[48,62],16496,"battle",[47,198],"26dafa17564a49647b6b06e5a0450c077cdfa858d985436e619dd67c483f595f"),
      (2000,[89,79],16496,"battle",[236,387],"a21686cd55acc659cfe6d5e8786221a0f654fccfbcbf2eb7c00d87fc81456942"),
      (3000,[97,86],16496,"battle",[429,580],"48fa8830df9e15c40f9ad543e0a77609915106cc228ca57afefbbcd7d1d1f16c"),
      (4000,[86,61],16496,"battle",[622,773],"3f5f1a1fa5f83dd743c8b1ba2a093a7d2f869f0a6b03aaafcdc4cf8baad4ccf1"),
      (1003,[19,15],16122,"pet",[813,966],"ed11e2add570813fe5109a3fd28102ab0e9a2922ce59e18aceff76daa001308b"),
      (2003,[11,12],16127,"pet",[1006,1159],"ede74e6f3a9a0e39a87d97f3666a1ce304a44420e8594dfdaaf847702e1fc73b"),
      (3003,[16,19],16122,"pet",[1199,1352],"8304e3dc90d2cb67f645ceafbb63ffb2e09461bb7b3e6e69e3ba62c9aa4de81d"),
      (4003,[14,17],16122,"pet",[1394,1547],"e045a67dc9e1b6353be66b7293a11e8719099c2c4865b1ca31a476519c38b6bb")]
    must(len(rows)==8)
    for x,e in zip(rows,expected):must((x["floor"],x["xy"],x["graphicname"],x["teacher"],x["block_byte_range"],x["block_sha256"])==e)
    keys=["NomalWindowMsg"]+["NomalWindowMsg"+str(i) for i in range(1,9)]
    for name,path in (("battle","fighter"),("pet","petmaster")):
        x=d["teacher_source_contracts"][name]
        must(x["path"]=="npc/sa60/newbie/"+path and x["source_template_pointer"]=="changeevent|file:sa60/newbie/"+path)
        must(x["source_create_count"]==4 and x["window_line_keys"]==keys and x["window_line_count"]==9 and x["main_message_count"]==1)
        must(x["event_number"]==-1 and x["type"]=="MESSAGE" and x["event_condition_literal"]=="LV>0" and x["event_end_literal_present"] is True and x["static_transaction_action_present"] is False)
        must(len(x["source_window_line_sha256"])==9 and len(set(x["source_window_line_sha256"]))==9 and all(len(y)==64 and all(z in "0123456789abcdef" for z in y) for y in x["source_window_line_sha256"]))
        if name=="battle":must(x["source_window_line_sha256"][6]=="6df118a98acba3bdc31d4561117aab093687489d1a1ac4fa4070ae2569d4b8cd")
        if name=="pet":must(x["source_window_line_sha256"][3]=="fb0f59148f39c9e4c80ffd598cfdfdd3fe344f795b3886bdf2bc8ed865ddcb56")
        must(len(x["topic_summary_derived_from_script"])>=5)
    maps=d["map_cell_source_anchors"];must(len(maps)==2)
    must((maps[0]["floor"],maps[0]["npc_xy"],maps[0]["raw_three_planes"],maps[0]["original_map_dat_sha256"])==(1000,[48,62],[243,0,49152],"94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e"))
    must((maps[1]["floor"],maps[1]["npc_xy"],maps[1]["raw_three_planes"],maps[1]["original_map_dat_sha256"])==(1003,[19,15],[5000,0,49152],"fc3037a1850c8baf06ad5874a4cb49ca5e13e9315c020f64c019417c33b694e6"))
    must([x["original_map_dat_bytes"] for x in maps]==[153608,5408])
    lim=d["boundaries"];must(all(v is True for k,v in lim.items() if k.endswith("_unproven") or k in ("script_file_presence_does_not_prove_setup_loaded",)))
    must(all(v is False for k,v in lim.items() if k in ("early_jss1999_or_tw10_source_proven","original_server_or_client_executed","original_game_world_entered","copyright_original_dialogue_or_map_published")))
    must(lim["overall_completion_percent"] is None)
    must(d["phase"]=={"stage_a":"7_PARTIAL_2_OPEN","stage_b":"GATED","wiki":"GATED","r79":"PAUSED_NON_BLOCKING"})
class O60SourceGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=json.loads(D.read_bytes());cls.r18=json.loads(R18.read_bytes())
    def test_source_join_original_R18_and_two_original_map_cells(self):check(self.d,self.r18)
    def test_unsupported_promotions_and_fields_rejected(self):
        changes=[
           ("boundaries","original_game_world_entered",True),
           ("boundaries","early_jss1999_or_tw10_source_proven",True),
           ("boundaries","script_file_presence_does_not_prove_setup_loaded",False),
           ("teacher_source_contracts","pet","static_transaction_action_present",True),
           ("teacher_source_contracts","battle","window_line_count",8)]
        for x in changes:
            d=copy.deepcopy(self.d)
            if len(x)==3:d[x[0]][x[1]]=x[2]
            else:d[x[0]][x[1]][x[2]]=x[3]
            with self.subTest(change=x),self.assertRaises(ValueError):check(d,self.r18)
        d=copy.deepcopy(self.d);d["teacher_creations"][4]["xy"]=[19,21]
        with self.assertRaises(ValueError):check(d,self.r18)
        d=copy.deepcopy(self.d);d["map_cell_source_anchors"][1]["raw_three_planes"]=[5000,0,49155]
        with self.assertRaises(ValueError):check(d,self.r18)
if __name__=="__main__":unittest.main()
