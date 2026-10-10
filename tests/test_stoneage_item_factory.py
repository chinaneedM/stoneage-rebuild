import hashlib
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_item_factory_audit as factory

class OriginalFactoryTests(unittest.TestCase):
    def test_pinned_original_factory_mutation_rejected(self):
        raw=factory.SOURCE.read_text()
        self.assertIn("ITEM_makeItemAndRegist",raw)
        for profile in ("gavin","bismarck"):
            bodies={n:"native "+n for n in factory.NAMES}
            hashes={n:hashlib.sha256(s.encode()).hexdigest() for n,s in bodies.items()}
            factory.allocator.item.pet.player.validate_bodies(bodies,hashes)
            for name in factory.NAMES:
                with self.assertRaisesRegex(ValueError,"dependency drift"):
                    factory.allocator.item.pet.player.validate_bodies(bodies|{name:"stub"},hashes)

    def test_exact_function_inventory(self):
        with patch.object(factory.attack,"pp_file",return_value="preprocessed"), patch.object(factory.attack,"definition",side_effect=lambda _,n:n):
            self.assertEqual(set(factory.factory_originals("gavin",Path("/tmp"))),set(factory.NAMES))
            self.assertEqual(set(factory.factory_originals("bismarck",Path("/tmp"))),set(factory.NAMES))

    def test_profile_specific_direct_and_indirect_tables(self):
        g,b=factory.factory_controls("gavin"),factory.factory_controls("bismarck")
        for code in (g,b):
            for token in ("ITEM_makeItem(&item,1)", "ITEM_makeItemAndRegist(1)",
                          "ITEM_makeItemAndRegist(-1)","whole original generated and registered pool oracle",
                          "every integer field consumes original RAND including zero-width ranges",
                          "memcpy(reward_items,old_items", "mode!=3",
                          "REAL_HEADER_ITEM_FACTORY"):
                self.assertIn(token,code)
            for unresolved in ("FACTORY_SETUP", "FACTORY_TABLE_ORACLE","TABLE_KIND",
                               "TABLE_TYPE","DATA_FIELDS","LEAK_EXPECTED","ITEM_FIELD"):
                self.assertNotIn(unresolved,code)
            self.assertLess(code.index("whole original generated and registered pool oracle"),code.index("memcpy(reward_items,old_items"))
        self.assertIn("ITEM_gTable=factory_table",b)
        self.assertIn("ITEM_gIndex[1].index==1",b)
        self.assertIn("ITEM_tbl=allocator_table",g)
        self.assertIn("leak_level=%d",b)
        self.assertNotIn("ITEM_gTable",g)

    def test_continuity_of_existing_controls_and_only_last_mode_register(self):
        for p in ("gavin","bismarck"):
            old=factory.allocator.controls(p)
            new=factory.factory_controls(p)
            self.assertIn("cursor_results=2,2,-1,5,6,1",old)
            self.assertIn("if(mode!=3)return",new)
            self.assertIn("registered_index=%d",new)
            self.assertIn("whole_actor_oracle=1",new)
            self.assertIn("whole_arena_oracle=1",new)

if __name__=="__main__":
    unittest.main()
