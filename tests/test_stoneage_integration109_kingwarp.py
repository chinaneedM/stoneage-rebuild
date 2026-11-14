"""Integration109: original source-bound, rights-safe static kingwarp crosswalk."""
import collections
import hashlib
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DERIVED = ROOT / 'research/recovered/STONEAGE-INTEGRATION109-KINGWARP-ORIGINAL-STATIC-ROUTES-R1.json'
PRIOR_SOURCE = ROOT / 'research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json'
PRIOR_MAP = ROOT / 'research/recovered/STONEAGE-25-STABLE-WORLD-CONTENT-COVERAGE-R1.txt'
SOURCE_NAME = 'genout/kingwarp.create'


def qualified_map_sizes():
    known = {}
    for line in PRIOR_MAP.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^FLOOR\|id=(\d+)\|path=([^|]+)\|width=(\d+)\|height=(\d+)\|map_sha256=([0-9a-f]{64})\|', line)
        if m:
            floor = int(m.group(1))
            assert m.group(2).lower() == f'{floor}.dat'
            known[floor] = (int(m.group(3)), int(m.group(4)), m.group(5))
    return known


def matches_prior_index(rows, prior_rows):
    if len(rows) != len(prior_rows):
        return False
    for n, (ours, old) in enumerate(zip(rows, prior_rows), 1):
        if not (
            ours[0] == n and old[1] == n - 1
            and ours[1:4] == old[2:5]
            and ours[4] == old[5]
            and old[7] == [ours[5], ours[6], ours[5], ours[6]]
            and old[11] == 'npcgen_warp'
            and old[12] == 'SAME_DIRECTORY_EXACT_TOKEN'
        ):
            return False
    return True


def inspect_coordinates(rows, maps):
    counters = collections.Counter()
    for r in rows:
        for floor, x, y, side in [(r[4], r[5], r[6], 'source'), (r[7], r[8], r[9], 'target')]:
            if floor not in maps:
                counters[side + '_unqualified'] += 1
            elif 0 <= x < maps[floor][0] and 0 <= y < maps[floor][1]:
                counters[side + '_within'] += 1
            else:
                counters[side + '_outside'] += 1
    return counters


def graph_components(rows):
    graph = collections.defaultdict(set)
    for r in rows:
        graph[r[4]].add(r[7])
        graph[r[7]].add(r[4])
    visited, groups = set(), []
    for root in graph:
        if root in visited:
            continue
        next_nodes = [root]
        members = set()
        while next_nodes:
            node = next_nodes.pop()
            if node in members:
                continue
            members.add(node)
            next_nodes.extend(graph[node] - members)
        visited.update(members)
        groups.append(members)
    return groups


class OriginalKingwarpStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(DERIVED.read_text(encoding='utf-8'))
        cls.source = json.loads(PRIOR_SOURCE.read_text(encoding='utf-8'))
        cls.rows = cls.d['original_create_rows']
        cls.prior = [x for x in cls.source['create_rows'] if x[0] == SOURCE_NAME]
        cls.maps = qualified_map_sizes()

    def test_source_custody_and_existing_parent_index_exact_match(self):
        d = self.d
        self.assertEqual(d['source_file'], 'npc/' + SOURCE_NAME)
        self.assertEqual(d['source_file_bytes'], 36355)
        self.assertEqual(d['source_file_sha256'], '33f29f58215d07e139df4cd94b8a9b8bacb87b0acdebba58af704a3174712983')
        self.assertEqual(d['source_file_crc32'], '31c690a2')
        self.assertEqual(d['private_original_subtree_zip_sha256'], 'c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f')
        self.assertEqual(d['private_original_subtree_zip_member_count_crc_pass'], 2205)
        f = next(x for x in self.source['source_files'] if x[0] == SOURCE_NAME)
        self.assertEqual(f[1:4], [d['source_file_bytes'], d['source_file_sha256'], d['source_file_crc32']])
        self.assertTrue(matches_prior_index(self.rows, self.prior))
        self.assertEqual(len(self.prior), 309)

    def test_original_sha_windows_preserve_all_appearances(self):
        rows = self.rows
        self.assertEqual(len(rows), 309)
        self.assertEqual([x[0] for x in rows], list(range(1, 310)))
        self.assertEqual(len({x[3] for x in rows}), 261)
        self.assertEqual(rows[0][:4], [1, 110, 219, '4785a9ae73ea21ba443301c52fa241997aaff9cd8b52418e171b10c13e4dba74'])
        self.assertEqual(rows[-1][1:3], [36248, 36355])
        self.assertTrue(all(re.fullmatch('[0-9a-f]{64}', x[3]) for x in rows))
        self.assertTrue(all(0 <= x[1] < x[2] <= self.d['source_file_bytes'] for x in rows))
        self.assertTrue(all(a[2] < b[1] for a, b in zip(rows, rows[1:])))

    def test_static_graph_counts_do_not_imply_live_travel(self):
        rows = self.rows
        floor_ids = {x[4] for x in rows} | {x[7] for x in rows}
        self.assertEqual(len(floor_ids), 35)
        self.assertEqual(len({x[4] for x in rows}), 34)
        self.assertEqual(len({(x[4], x[7]) for x in rows}), 75)
        tuples = {(x[4], x[5], x[6], x[7], x[8], x[9]) for x in rows}
        self.assertEqual(len(tuples), 261)
        exact_inverse = sum((x[7], x[8], x[9], x[4], x[5], x[6]) in tuples for x in rows)
        self.assertEqual(exact_inverse, 222)
        self.assertEqual(sorted((len(x) for x in graph_components(rows)), reverse=True), [11, 9, 9, 3, 3])

    def test_previously_qualified_map_dimensions_not_original_execution(self):
        rows = self.rows
        floor_ids = {x[4] for x in rows} | {x[7] for x in rows}
        mapped = floor_ids & set(self.maps)
        self.assertEqual(len(mapped), 26)
        self.assertEqual(sorted(floor_ids - mapped), [300,30605,30607,30689,30691,30692,30693,30694,30695])
        c = inspect_coordinates(rows, self.maps)
        self.assertEqual(c['source_within'], 268)
        self.assertEqual(c['target_within'], 264)
        self.assertEqual(c['source_unqualified'], 41)
        self.assertEqual(c['target_unqualified'], 45)
        self.assertEqual(c['source_outside'], 0)
        self.assertEqual(c['target_outside'], 0)

    def test_mutations_are_rejected_by_independent_public_joins(self):
        import copy
        bad = copy.deepcopy(self.rows)
        bad[0][3] = '0' * 64
        self.assertFalse(matches_prior_index(bad, self.prior))
        bad = copy.deepcopy(self.rows)
        bad[0][5] += 1
        self.assertFalse(matches_prior_index(bad, self.prior))
        bad = copy.deepcopy(self.rows)
        bad[0][7] = 99999
        self.assertNotEqual(set(x[7] for x in bad), set(x[7] for x in self.rows))
        bad = copy.deepcopy(self.rows)
        index = next(i for i, x in enumerate(bad) if x[4] == 30611)
        bad[index][5] = 99999
        self.assertGreater(inspect_coordinates(bad, self.maps)['source_outside'], 0)

    def test_rights_and_negative_evidence_boundary(self):
        self.assertIn('NOT_NATIVE_RUNTIME', self.d['evidence_status'])
        self.assertIn('COMMUNITY_PRESERVED', self.d['carrier_scope'])
        self.assertEqual(len(self.d['columns']), 10)
        self.assertTrue(all(len(r) == len(self.d['columns']) for r in self.rows))
        # Only numeric tuples + digests, not original commercial CREATE text or imagery.
        text = DERIVED.read_text(encoding='utf-8')
        for forbidden in ('NPCCREATE\n', 'enemy=npcgen_warp|', 'borncorner=', 'original_base64', '<img'):
            self.assertNotIn(forbidden, text)


if __name__ == '__main__':
    unittest.main()
