"""Public provenance checks; never substitutes for private full-canvas replay."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'research/recovered'


def validate(report, acquisition, index):
    floors = {'1200', '1400', '3100', '3300', '5100', '5500'}
    assert set(report['maps']) == floors
    assert acquisition['status'] == 'VERIFIED_955_ORIGINAL_DAT_ENCRYPTED'
    assert all(acquisition[k] is False for k in (
        'original_executable_executed', 'original_client_rendering_verified',
        'official_same_deployment_verified', 'raw_originals_in_public_git'))
    assert all(v is False for v in report['boundaries'].values())
    assert report['source_run_id'] == 42361185994
    assert report['source_head'] == '7c7fbeddf26f4538aea350a7678a2545dd3b24c9'
    assert report['source_artifact_id'] == 13569996494
    assert report['source_artifact_zip_sha256'] == '0e945d09deecac0b3459a674edfb34c3c43e2144fd0700de7cdc521380f3aa09'
    assert acquisition['qualified_carrier']['sha256'] == index['provenance']['original_mixed25_community_RAR_sha256']
    assert report['source_report_sha256'] == hashlib.sha256((REC/'STONEAGE-MAP08-955-DAT-SOURCE-ACQUISITION-R1.json').read_bytes()).hexdigest()
    original = {r[0]: dict(zip(index['per_floor_source_row_columns'], r)) for r in index['per_floor_source_rows']}
    assert set(acquisition['members']) == set(original) and len(original) == 955
    for name, row in original.items():
        member = acquisition['members'][name]
        assert (member['bytes'], member['sha256']) == (row['source_file_bytes'], row['source_full_file_SHA256'])
    a = report['all_955_original_DAT_archive']
    assert a['members'] == 955 and a['uncompressed_bytes'] == sum(m['bytes'] for m in acquisition['members'].values()) == 17122946
    assert (a['bytes'], a['sha256']) == (acquisition['private_archive_plaintext']['bytes'], acquisition['private_archive_plaintext']['sha256'])
    images = {str(r[0]): r for r in index['source_TW1_real_RD_rows']}
    for key, row in report['resources'].items():
        orig = images[key]
        assert (row['source_adrn_index'], row['width'], row['height'], row['source_RD_sha256'], row['source_index_pixels_sha256']) == (orig[1], orig[2], orig[3], orig[5], orig[6])
    for floor, row in report['maps'].items():
        orig = original[floor+'.dat']
        info = row['structure']
        assert (row['source_bytes'], row['source_sha256']) == (orig['source_file_bytes'], orig['source_full_file_SHA256'])
        assert [info['width'], info['height']] == [orig['original_header_width'], orig['original_header_height']]
        assert info['modern_draw_candidate_positions']+info['source_low_nonzero_not_rendered'] == orig['first_plane_nonzero_numeric_occurrences']+orig['second_plane_nonzero_numeric_occurrences']
        assert orig['number_of_nonzero_positions_missing_source_qualified_TW1_RD'] == 0
        assert set(row['frames']) == {'plane0', 'plane1', 'combined'}
        assert row['distinct_draw_candidate_aliases'] <= len(report['resources'])
    return True


class Map08(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads((REC/'STONEAGE-MAP08-SIX-LARGE-SOURCE-SCENES-R1.json').read_bytes())
        cls.a = json.loads((REC/'STONEAGE-MAP08-955-DAT-SOURCE-ACQUISITION-R1.json').read_bytes())
        cls.i = json.loads((REC/'STONEAGE-MAP-SCENE-MODULE-04-955-ORIGINAL-DAT-4166-RD-PIXEL-INDEX-R1.json').read_bytes())

    def test_exact_source_identities_and_conservation(self):
        self.assertTrue(validate(self.r, self.a, self.i))

    def test_reject_unrendered_value_loss(self):
        r = copy.deepcopy(self.r); r['maps']['1200']['structure']['source_low_nonzero_not_rendered'] += 1
        with self.assertRaises(AssertionError): validate(r, self.a, self.i)

    def test_reject_native_execution_promotion(self):
        r = copy.deepcopy(self.r); r['boundaries']['original_client_executed'] = True
        with self.assertRaises(AssertionError): validate(r, self.a, self.i)

    def test_reject_changed_original_DAT(self):
        a = copy.deepcopy(self.a); a['members']['1200.dat']['sha256'] = '0'*64
        with self.assertRaises(AssertionError): validate(self.r, a, self.i)

    def test_reject_changed_original_RD(self):
        r = copy.deepcopy(self.r); next(iter(r['resources'].values()))['source_RD_sha256'] = '0'*64
        with self.assertRaises(AssertionError): validate(r, self.a, self.i)

    def test_reject_incomplete_private_source_custody(self):
        a = copy.deepcopy(self.a); a['members'].pop('1200.dat')
        with self.assertRaises(AssertionError): validate(self.r, a, self.i)


if __name__ == '__main__': unittest.main()
