import unittest
from tools.stoneage_exit_lifetime_watch_audit import (
    _definition, item_limit, watch_vectors, watch_oracle, lifetime_oracle,
    PIN_PATH, PINNED,
)
import json


class LifetimeWatchTests(unittest.TestCase):
    def test_exact_function_extraction_cannot_select_strict_prefix(self):
        synthetic = 'int getStrict(int i){return 10;} int get(int i){return 20;} int getOther(int i){return 30;}'
        body = _definition(synthetic, 'get')
        self.assertIn('return 20;', body)
        self.assertNotIn('Strict', body)
        self.assertNotIn('Other', body)
        with self.assertRaises(ValueError):
            _definition(synthetic, 'ge')

    def test_item_cardinality_expression_fails_closed(self):
        self.assertEqual(item_limit('(9+15*3)'), 54)
        self.assertEqual(item_limit('(9+15)'), 24)
        for expr in ('__import__("os")', 'unknown+1', '512', '0', '9**3', '-1'):
            with self.assertRaises(ValueError):
                item_limit(expr)

    def test_chain_matrix_covers_head_middle_tail_and_detached_link(self):
        rows = list(watch_vectors())
        self.assertEqual(len(rows), 84)
        self.assertEqual(len(set(rows)), len(rows))
        for count in range(4):
            for action in (1,2):
                self.assertEqual({r[2] for r in rows if r[0] == action and r[1] == count}, set(range(count+1)))
        self.assertTrue(all(target == count+1 for action,count,target,slot in rows if action == 0))

    def test_original_finish_defect_is_retained_separately_from_exit(self):
        for count in range(4):
            r = watch_oracle((3,count,0,4))
            self.assertEqual(r[1], max(count-1,0))
            self.assertEqual(r[-2], (1 << (count+1))-1)  # all nodes exited
            self.assertEqual(r[-1], 1 | (2 if count else 0))  # only first watch deleted
        r = watch_oracle((3,3,0,4))
        self.assertEqual(r[2+3*2:2+3*4], (1,-1,3,1,2,-1))  # residual live chain

    def test_slot_validity_and_stale_access_remain_profile_specific(self):
        limits = {'items':24,'pool':30}
        self.assertEqual(lifetime_oracle('gavin',limits,(1,1,1)), (0,0,54,54,73,73,2,0))
        self.assertEqual(lifetime_oracle('iris',limits,(1,1,0)), (0,0,54,54,73,73,0,0))
        self.assertEqual(lifetime_oracle('bismarck',limits,(1,1,1)), (0,0,54,54,-1,-1,0,0))
        self.assertEqual(lifetime_oracle('bismarck',limits,(1,0,1)), (1,1,0,0,73,73,2,0))

    def test_identity_receipt_keeps_guard_and_cardinality_disagreements(self):
        rows = json.loads(PIN_PATH.read_text())['profiles']
        self.assertEqual(set(rows), set(PINNED))
        for profile,d in rows.items():
            self.assertEqual(d['source_sha'], PINNED[profile])
            self.assertEqual(d['contracts']['work_getter_checks_live_slot'], profile == 'bismarck')
            self.assertEqual(d['contracts']['exit_ticket_block_checks_live_slot'], profile == 'bismarck')
            self.assertEqual(d['limits']['items'], 54 if profile == 'bismarck' else 24)
            self.assertEqual(d['limits']['pool'], 30)
            self.assertTrue(all(len(sha) == 64 for sha in d['functions'].values()))


if __name__ == '__main__':
    unittest.main()
