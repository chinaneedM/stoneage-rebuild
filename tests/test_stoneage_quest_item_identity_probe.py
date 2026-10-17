"""Synthetic candidate rows; never original item payload fixtures."""
from pathlib import Path
import tempfile
import unittest
from tools.stoneage_itemset_schema_probe import INDEX
from tools.stoneage_quest_item_identity_probe import extract, name_matches, report


def invented_row(name='杉之手环', codec='gb18030', item_id=123):
    fields = [b'' for _ in range(94)]
    fields[INDEX['name']] = name.encode(codec)
    fields[INDEX['secretname']] = b'synthetic'
    fields[INDEX['id']] = str(item_id).encode()
    return fields


class QuestItemIdentityTests(unittest.TestCase):
    def test_literal_query_encoding_candidates_remain_explicit(self):
        for codec, name in [('gb18030', '杉之手环'), ('big5', '杉之手環'), ('utf-8', '衫之手环')]:
            matches = name_matches(name.encode(codec))
            self.assertTrue(any(m['codec'] == codec and m['query'] == name and m['exact_name_match'] for m in matches))
        self.assertFalse(name_matches(b'synthetic unrelated item'))

    def test_selected_fields_preserve_blank_zero_negative_and_raw_pair(self):
        f = invented_row()
        f[INDEX['charm_raw_a']] = b'-5'
        f[INDEX['charm_raw_b']] = b'5'
        f[INDEX['vanishatdrop']] = b'0'
        r = extract(b','.join(f))['candidates'][0]
        self.assertEqual(r['numeric_fields']['id'], 123)
        self.assertEqual((r['numeric_fields']['charm_raw_a'], r['numeric_fields']['charm_raw_b']), (-5, 5))
        self.assertEqual(r['numeric_fields']['vanishatdrop'], 0)
        self.assertIsNone(r['numeric_fields']['dropatlogout'])
        self.assertNotIn('name', r)
        self.assertNotIn('description', r)

    def test_partial_name_match_is_only_a_candidate(self):
        m = name_matches('synthetic杉之手环variant'.encode('gb18030'))
        self.assertTrue(m)
        self.assertTrue(all(not r['exact_name_match'] for r in m))

    def test_bad_width_duplicate_ids_and_invalid_flags_rejected(self):
        f = invented_row()
        for body in (b','.join(f[:-1]), b','.join(f) + b'\n' + b','.join(f)):
            with self.assertRaises(ValueError):
                extract(body)
        f[INDEX['canpetmail']] = b'2'
        with self.assertRaisesRegex(ValueError, 'non-boolean'):
            extract(b','.join(f))

    def test_row_hash_and_physical_line_include_source_position(self):
        row = b','.join(invented_row())
        result = extract(b'# synthetic\n\n' + row + b'\n')
        self.assertEqual(result['row_count'], 1)
        self.assertEqual(result['candidates'][0]['physical_line'], 3)
        self.assertRegex(result['candidates'][0]['row_sha256'], r'^[a-f0-9]{64}$')

    def test_lookalike_unpinned_table_cannot_be_reported_as_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            setup = root / 'setup.cf'
            setup.write_text('itemset6file=data/itemset.txt\n')
            (root / 'itemset.txt').write_bytes(b','.join(invented_row()))
            with self.assertRaisesRegex(ValueError, 'hash/size'):
                report(root, setup)
            setup.write_text('itemset6file=data/invented.txt\n')
            with self.assertRaises(ValueError):
                report(root, setup)


if __name__ == '__main__':
    unittest.main()
