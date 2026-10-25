import struct
import unittest
from tools import stoneage_sound3_original_content as m


def wav(payload=b'1234', rate=22000):
    fmt = struct.pack('<HHIIHH', 1, 1, rate, rate, 1, 8)
    chunks = b'fmt '+struct.pack('<I', 16)+fmt+b'data'+struct.pack('<I', len(payload))+payload
    return b'RIFF'+struct.pack('<I', len(chunks)+4)+b'WAVE'+chunks


class Sound3(unittest.TestCase):
    def test_identical_tail_copies_are_occurrences_not_new_sounds(self):
        w = wav()
        r = m.inspect(f'0:{len(w)}:one.wav\n'.encode(), w*3)
        self.assertEqual(r['physical_record_occurrences'], 3)
        self.assertEqual(r['distinct_full_wave_blocks'], 1)
        self.assertEqual(r['table_records'][0]['physical_offsets_in_full_container'], [0, len(w), len(w)*2])
        self.assertEqual([c['directly_addressed_by_retained_table'] for c in r['copies']], [True, False, False])

    def test_duplicate_table_entries_keep_distinct_indices_and_offsets(self):
        w = wav();n = len(w)
        r = m.inspect(f'0:{n}:one.wav\n{n}:{n}:two.wav\n'.encode(), w*2)
        self.assertEqual(r['duplicate_table_wave_groups'][0]['table_indices'], [0, 1])

    def test_unclassified_or_different_tail_rejected(self):
        w = wav();table = f'0:{len(w)}:one.wav\n'.encode()
        for raw in [w+b'x', w+wav(b'5678')]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                m.inspect(table, raw)

    def test_address_gaps_overlap_bounds_and_unparsed_lines_rejected(self):
        w = wav();n = len(w)
        for t in [f'1:{n}:one.wav', f'0:{n+1}:one.wav', 'header not understood',
                  f'0:{n}:one.wav\n0:{n}:two.wav']:
            with self.subTest(t=t), self.assertRaises(ValueError):
                m.inspect(t.encode(), w*2)

    def test_odd_and_unusual_sample_rate_preserved_not_normalized(self):
        w = wav(rate=5564)
        r = m.inspect(f'0:{len(w)}:one.wav\n'.encode(), w)
        self.assertEqual(r['table_records'][0]['wave']['sample_rate'], 5564)

    def test_non_wave_and_riff_outer_extent_rejected(self):
        w = wav()
        for raw in [b'x'*len(w), w[:4]+b'\0'*4+w[8:]]:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                m.inspect(f'0:{len(raw)}:one.wav\n'.encode(), raw)


if __name__ == '__main__':
    unittest.main()
