"""Bounded static cross-carrier pet-shop code comparison, NOT original server execution."""
import hashlib
import json
import os
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-O57-PETSHOP-CODE-CROSS-CARRIER-R1.json'
O18 = ROOT / 'research/recovered/STONEAGE-O18-MAP1003-SAME-CARRIER-NAMED-CONTENT-R1.json'
O19 = ROOT / 'research/recovered/STONEAGE-O19-ONE-PETSHOP-CREATE-ARGUMENT-LINK-R1.json'
CODE_BLOB = '5f18141188fb7a1bd2ce236a4559e54dc1a82294'

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()

def section(code: str, name: str, next_name: str) -> str:
    """Match a function definition followed by '{', never a C prototype."""
    def definition(symbol):
        return r"\b(?:int|void|BOOL)\s+" + re.escape(symbol) + r"\s*\([^;{}]*\)\s*(?://[^\n]*\n\s*)?\{"
    match = re.search(definition(name), code, flags=re.S)
    if match is None:
        raise AssertionError('source function definition is missing: ' + name)
    end = re.search(definition(next_name), code[match.end():], flags=re.S)
    if end is None:
        raise AssertionError('source next-function definition is missing: ' + next_name)
    return code[match.start():match.end() + end.start()]

class O57PetshopComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding='utf-8'))
        cls.o18 = json.loads(O18.read_text(encoding='utf-8'))
        cls.o19 = json.loads(O19.read_text(encoding='utf-8'))

    def test_exact_prior_mixed25_petshop_source_contract(self):
        linked = self.o19['linked_actual_original_argument']
        legacy = self.o18['original_NPC_message_members']['ps_1003_12_13']
        self.assertEqual(linked['path'], 'gmsv/data/npc/genout/ps_1003_12_13')
        self.assertEqual(linked['bytes'], 397)
        self.assertEqual(linked['sha256'], legacy['sha256'])
        self.assertEqual(linked['sha256'], self.report['preserved_mixed25']['argument_sha256'])
        self.assertEqual(self.o19['original_create']['floorid'], 1003)
        self.assertEqual(self.o19['original_create']['borncorner'], [12, 13, 12, 13])
        self.assertTrue({'nomal_rate', 'special_rate', 'special_pet', 'pool_cost', 'pool_flg'}.issubset(set(legacy['field_labels'])))
        self.assertFalse(self.o18['bounds']['original_shop_transaction_executed'])
        self.assertFalse(self.o19['source_scope']['official_2003_or_tw10_same_deployment_proven'])

    def test_qualified_but_not_official_historical_status(self):
        r = self.report
        self.assertEqual(r['later_code_snapshot']['commit'], '2f736808ff4361f5429ee919b718c88fabb60346')
        self.assertEqual(r['later_code_snapshot']['git_blob_sha1'], CODE_BLOB)
        self.assertEqual(r['later_code_snapshot']['size_bytes'], 52497)
        self.assertEqual(r['source_qualification'], 'INDEPENDENT_2026_PUBLIC_INTEGRATION_NOT_OFFICIAL_OR_SAME_DEPLOYMENT')
        self.assertFalse(r['negative_claims']['mixed25_matching_server_binary_proven'])
        self.assertFalse(r['negative_claims']['official_tw10_or_jss1999_shop_rule_proven'])
        self.assertFalse(r['negative_claims']['historical_pet_sale_deposit_withdraw_executed'])
        self.assertFalse(r['negative_claims']['original_1003_dat_exits_reread'])
        self.assertIsNone(r['overall_completion_percent'])

    def test_source_blob_guard_rejects_mutation(self):
        payload = b'fixture'
        self.assertNotEqual(git_blob_sha(payload), CODE_BLOB)
        self.assertNotEqual(git_blob_sha(payload + b'!'), git_blob_sha(payload))

    def test_pinned_later_source_exhibits_specific_petshop_branches(self):
        src = os.environ.get('STONEAGE_O57_PETSHOP_SOURCE')
        if not src:
            self.skipTest('actual pinned source supplied only in source-verification CI')
        raw = Path(src).read_bytes()
        self.assertEqual(len(raw), 52497)
        self.assertEqual(git_blob_sha(raw), CODE_BLOB)
        code = raw.decode('utf-8')
        init = section(code, 'NPC_PetShopInit', 'NPC_PetShopTalked')
        menu = section(code, 'NPC_PetShop_selectWindow', 'NPC_PetShopWindowTalked')
        cost = section(code, 'NPC_GetCost', 'NPC_PetDel')
        sale = section(code, 'NPC_PetDel', 'NPC_PetDel2')
        deposit = section(code, 'NPC_PetDel2', 'NPC_PetDel3')
        withdraw = section(code, 'NPC_PetDel3', 'NPC_getDrawPet')
        for key in ('nomal_rate', 'special_rate', 'pool_flg'):
            self.assertIn('"' + key + '"', init)
        self.assertIn('"special_pet"', cost)
        self.assertIn('CHAR_WORK_SPECIALRATE', cost)
        self.assertIn('CHAR_BASEBASEIMAGENUMBER', cost)
        self.assertIn('NPC_GETPOOLCOST(toindex)', menu)
        self.assertIn('#ifdef _NPC_DEPOTPET', menu)
        self.assertIn('CHAR_WORK_POOLFLG', menu)
        self.assertIn('CHAR_getCharPetElement(talkerindex)', code)
        self.assertIn('CHAR_RIDEPET', sale)
        self.assertIn('CHAR_PETFAMILY', sale)
        self.assertIn('CHAR_DEFAULTPET, -1', sale)
        self.assertIn('CHAR_RIDEPET', deposit)
        self.assertIn('CHAR_DEFAULTPET, -1', deposit)
        self.assertIn('CHAR_setCharPoolPet(talker, emptyindex, petindex)', deposit)
        self.assertIn('CHAR_setCharPet(talker, selectpet, -1)', deposit)
        self.assertIn('CHAR_DelGold(talker, NPC_GETPOOLCOST(talker))', deposit)
        self.assertIn('CHAR_getCharPetElement(talker)', withdraw)
        self.assertIn('CHAR_setCharPet(talker, emptyindex, petindex)', withdraw)
        self.assertIn('CHAR_setCharPoolPet(talker, selectpet, -1)', withdraw)
        # A script key is NOT proof of a runtime price override. This code
        # does not parse it as a quoted config key anywhere in this file.
        self.assertNotIn('"pool_cost"', code)
        self.assertRegex(code, r'#define\s+NPC_GETPOOLCOST\(talker\)\s*\(50\s*\+\s*CHAR_getInt\(talker,\s*CHAR_LV\)\s*\*\s*4\)')
        self.assertEqual(self.report['later_code_snapshot']['code_path']['deposit_clears_default_pet'], True)
        self.assertEqual(self.report['later_code_snapshot']['code_path']['script_pool_cost_consumed_in_this_file'], False)

if __name__ == '__main__':
    unittest.main()