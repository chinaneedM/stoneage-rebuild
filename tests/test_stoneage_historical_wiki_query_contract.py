"""Acceptance examples join archived domains, without a website or search runtime."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class QueryContractTests(unittest.TestCase):
    def test_archived_inputs_and_six_qualified_queries(self):
        contract = json.loads((ROOT / 'research/recovered/STONEAGE-HISTORICAL-WIKI-QUERY-CONTRACT-DRAFT-R1.json').read_text())
        sources = {}
        for ident, pin in contract['inputs'].items():
            raw = (ROOT / pin['path']).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(), pin['git_blob'])
            sources[ident] = json.loads(raw)
        self.assertEqual(len(contract['queries']), 6)
        for query in contract['queries']:
            with self.subTest(query=query['id']):
                self.assertTrue(query['qualified_answer'])
                for check in query['checks']:
                    value = sources[query['source']]
                    for part in check['pointer'].split('/')[1:]:
                        value = value[int(part)] if isinstance(value, list) else value[part]
                    self.assertEqual(value, check['expected'])
        self.assertFalse(contract['website_implemented'])
        self.assertFalse(contract['public_export_enabled'])
        self.assertFalse(contract['historical_site_structure_fully_recovered'])


if __name__ == '__main__': unittest.main()
