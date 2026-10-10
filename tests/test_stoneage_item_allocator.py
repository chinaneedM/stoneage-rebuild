import hashlib,unittest
from unittest.mock import patch
from tools import stoneage_item_allocator_audit as allocator

class AllocatorTests(unittest.TestCase):
    def test_initializer_and_dependency_mutations_rejected(self):
        bodies={n:'original '+n for n in allocator.NAMES}
        frozen={n:hashlib.sha256(b.encode()).hexdigest() for n,b in bodies.items()}
        for n in allocator.NAMES:
            with self.assertRaisesRegex(ValueError,'dependency drift'):
                allocator.item.pet.player.validate_bodies(bodies|{n:'changed'},frozen)
        with self.assertRaisesRegex(ValueError,'dependency drift'):
            allocator.item.pet.player.validate_bodies(bodies|{'ITEM_setLUAFunction':'stub'},frozen)

    def test_source_function_inventory_exact(self):
        with patch.object(allocator.attack,'pp_file',return_value='preprocessed'),patch.object(allocator.attack,'definition',side_effect=lambda _,n:n):
            from pathlib import Path
            self.assertEqual(set(allocator.original_parts('gavin',Path('/tmp'))),set(allocator.NAMES))
            self.assertEqual(set(allocator.original_parts('bismarck',Path('/tmp'))),set(allocator.NAMES)|{'ITEM_setLUAFunction'})

    def test_profiles_keep_complete_lua_domain(self):
        b=allocator.controls('bismarck');g=allocator.controls('gavin')
        self.assertIn('template.lua[j]',b)
        self.assertIn('initialized.luafunctable[j]=NULL',b)
        self.assertIn('sizeof empty_lua',b)
        self.assertIn('ITEM_setLUAFunction(1,ITEM_LASTFUNCTION',b)
        self.assertNotIn('ITEM_setLUAFunction',g)
        self.assertNotIn('lua_State',g)

    def test_full_oracles_before_fixture_restoration(self):
        for p in ('gavin','bismarck'):
            text=allocator.controls(p)
            self.assertLess(text.index('whole pool seven actors and arena allocator oracle'),text.index('memcpy(reward_items,saved_items'))
            self.assertNotIn('Sindex',text)
            for marker in ('template_immutable=1','table_immutable=1','reserved_zero_preserved=1','cursor_results=2,2,-1,5,6,1'):
                self.assertIn(marker,text)

    def test_original_reward_and_growth_oracles_retained(self):
        for p in ('gavin','bismarck'):
            text=allocator.item.item_observations(p)
            for marker in ('whole original item array oracle','whole seven actor terminal oracle','whole arena terminal oracle','REAL_HEADER_PLAYER_LEVEL','REAL_HEADER_PET_GROWTH'):
                self.assertIn(marker,text)

    def test_unresolved_placeholders_fail_review(self):
        for p in ('gavin','bismarck'):
            text=allocator.controls(p)
            for marker in ('TABLE_TYPE','TABLE_PTR','TABLE_SIZE','ITEM_ARRAY','ITEM_SIZE','ITEM_COUNT','ITEM_TYPE','ITEM_FIELD','LUA_TEMPLATE','LUA_ORACLE','LUA_INVALID','LUA_SENTINEL','LUA_ACTIVE'):
                self.assertNotIn(marker,text)

if __name__=='__main__':unittest.main()
