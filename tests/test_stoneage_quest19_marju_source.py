"""QUEST19 public-only validation of archived Marju mail, rope-stone and treasurebag evidence."""
import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def data():
    return load("research/recovered/STONEAGE-QUEST19-MARJU-POST-TREASUREBAG-SOURCE-R1.json")
def source():
    return load("research/recovered/STONEAGE-QUEST-STORY-MODULE-01-ORIGINAL-EXCHANGEMAN-QUEST-SOURCE-BLOCK-CATALOG-R1.json")

class Quest19PublicAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=data();cls.old=source()
        cls.map=load("research/recovered/STONEAGE-MAP09-691-SOURCE-READY-SCENES-R1.json")["maps"]
        cls.items={row[0]:row for n in range(1,8) for row in load(f"research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-{n:02d}-R1.json")["rows"]}

    def test_old_source_create_and_script_sha_unchanged(self):
        r=self.r;old=self.old
        c=[x for x in old["source_creation_references"] if x["create_source_path"]==r["creator"]["path"]]
        self.assertEqual(len(c),12)
        self.assertEqual({x["create_source_sha"] for x in c},{r["creator"]["sha256"]})
        self.assertEqual({x["create_brace_ordinal"] for x in c},set(range(12)))
        scripts={x["path"]:x for x in r["original_scripts"]}
        self.assertEqual(set(scripts),{x["original_script_path"] for x in c})
        oldscripts={x["path"]:x for x in old["source_scripts"]}
        for path,s in scripts.items():
            o=oldscripts[path]
            self.assertEqual((s["source_bytes"],s["sha256"],s["crc32"],s["source_type_counts"]),(o["original_size"],o["original_sha256"],o["original_crc32"],o["actual_block_type_counts"]))
        actors={x["script"]:x for x in r["npc_placements"]}
        for row in c:
            actor=actors[row["original_script_path"]]
            self.assertEqual((actor["ordinal"],actor["floor"],actor["graphic_alias"]),(row["create_brace_ordinal"],row["floorid"],row["graphic_alias_numeric"]))

    def test_old_27_event_semantics_and_source_commands(self):
        r=self.r
        names={x["path"] for x in r["original_scripts"]}
        blocks=[x for x in self.old["source_event_blocks"] if x["script_path"] in names]
        self.assertEqual(len(blocks),r["original_event_blocks"]["count"])
        self.assertEqual(dict(Counter(x["raw_type"] for x in blocks)),r["original_event_blocks"]["types"])
        counts=Counter()
        for block in blocks:
            self.assertEqual(len(block["source_section_decoded_cp950_normalized_UTF8_sha256"]),64)
            counts.update(block["source_operations"])
        self.assertEqual(dict(counts),r["original_event_blocks"]["source_operations"])
        self.assertEqual(sorted({f for b in blocks for f in b["end_set_flags"]}),[37,38])
        self.assertTrue(r["private_source"]["public_quest01_blob"])

    def test_original_numeric_pool_literals_and_duplicates(self):
        p=self.r["numeric_random_candidate_pools"]
        self.assertEqual([(k,len(p[k]["literal_list"]),p[k]["script_occurrences"]) for k in ("MAIL","P36","P49")],[("MAIL",3,1),("P36",36,6),("P49",49,4)])
        for row in p.values():
            literal=",".join(str(x) for x in row["literal_list"])
            self.assertEqual(hashlib.sha256(literal.encode("ascii")).hexdigest(),row["original_argument_sha256"])
        allpool=[a for x in p.values() for a in x["literal_list"]]
        self.assertEqual(len(set(allpool)),59)
        self.assertEqual(sum(len(x["literal_list"])*x["script_occurrences"] for x in p.values()),415)
        self.assertEqual(len(set(p["P36"]["literal_list"])),27)
        self.assertEqual(len(set(p["P49"]["literal_list"])),29)
        self.assertEqual(self.r["random_candidates"]["source_GetRandItem_commands"],11)
        oldset={i for x in self.old["source_event_blocks"] if x["script_path"] in {p["path"] for p in self.r["original_scripts"]} for i in x["item_numeric_refs"].get("GetRandItem",[])}
        self.assertEqual(oldset,set(allpool))

    def test_all_10_bags_have_5_distinct_qualified_numeric_candidates(self):
        r=self.r;rows=r["treasurebag_npc_relocation"]["bag_rows"]
        self.assertEqual(len(rows),10)
        self.assertEqual({x["floor"] for x in rows},{118,122})
        alltargets=set()
        actors={x["script"]:x for x in r["npc_placements"]}
        for b in rows:
            self.assertEqual(b["source_spawn"],actors[b["script"]]["spawn_xy"])
            self.assertEqual(b["floor"],actors[b["script"]]["floor"])
            self.assertEqual(len(b["target_xy"]),5)
            self.assertEqual(len({tuple(x) for x in b["target_xy"]}),5)
            w,h=self.map[str(b["floor"])]["geometry"]
            for x,y in b["target_xy"]:
                self.assertTrue(0<=x<w and 0<=y<h)
                alltargets.add((b["floor"],x,y))
            self.assertIn(b["source_spawn"],b["target_xy"])
            literal=",".join(f'{b["floor"]}.{x}.{y}' for x,y in b["target_xy"])
            self.assertEqual(hashlib.sha256(literal.encode("ascii")).hexdigest(),b["literal_NpcWarp_arg_sha256"])
        self.assertEqual(len(alltargets),50)
        self.assertEqual(len([x for x in rows if x["item_pool"]=="P36"]),6)
        self.assertEqual(len([x for x in rows if x["item_pool"]=="P49"]),4)
        self.assertEqual(r["treasurebag_npc_relocation"]["original_NpcWarp_commands"],10)
        self.assertEqual(r["treasurebag_npc_relocation"]["bag_spawn_in_own_candidates"],10)
        self.assertEqual(self.map["118"]["source_sha256"],r["treasurebag_npc_relocation"]["MAP09_118"]["source_DAT_sha256"])
        self.assertEqual(self.map["122"]["source_sha256"],r["treasurebag_npc_relocation"]["MAP09_122"]["source_DAT_sha256"])
        self.assertNotIn("119",self.map)
        self.assertNotIn("1300",self.map)

    def test_original_item_row_identifiers_and_cross_carrier_art(self):
        r=self.r
        ids=r["item_crosswalk"]["source_item_IDs"]
        self.assertEqual(len(ids),61)
        self.assertEqual(len(set(ids)),61)
        names={x["path"] for x in r["original_scripts"]}
        prior={i for b in self.old["source_event_blocks"] if b["script_path"] in names for k,v in b["item_numeric_refs"].items() if k!="GetStone" for i in v}
        self.assertEqual(set(ids),prior)
        aliases=set();qualified=set();nonqualified=[]
        for id in ids:
            src=self.items[id]
            self.assertIsNotNone(src[1])
            self.assertEqual(src[1],src[2])
            self.assertEqual(src[3],src[4])
            aliases.add(src[3])
            if src[8]=="REAL_RD_DECODED_CROSS_CARRIER":
                qualified.add(src[3])
            else:
                nonqualified.append((id,src[3],src[8]))
        self.assertEqual(len(aliases),58)
        self.assertEqual(len(qualified),57)
        self.assertEqual(nonqualified,[(2687,24314,"TW1_INDEX_NOT_FOUND")])
        self.assertEqual(r["item_crosswalk"]["unmatched_TW1_index_item_id"],2687)
        self.assertTrue(r["item_crosswalk"]["source_item_graphic_identity_same_build_UNPROVEN"])

    def test_bounded_gameplay_and_no_official_promotion(self):
        r=self.r
        self.assertEqual(r["stage_A"],"7_PARTIAL_2_OPEN")
        self.assertEqual(r["stage_B"],"GATED")
        self.assertEqual(r["savedata_R79"],"PAUSED_NON_BLOCKING")
        self.assertIsNone(r["restoration_percent"])
        for v in r["bounds"].values():self.assertFalse(v)
        self.assertTrue(r["treasurebag_npc_relocation"]["not_player_teleport"])
        self.assertFalse(r["treasurebag_npc_relocation"]["actual_NpcWarp_selection_UNPROVEN"] is False)
        self.assertFalse(r["random_candidates"]["actual_reward_UNPROVEN"] is False)
        self.assertFalse(r["private_source"]["original_commercial_bytes_published"])
        self.assertFalse(r["private_source"]["parent_community_RAR_reverified_this_unit"])

if __name__=="__main__":unittest.main()
