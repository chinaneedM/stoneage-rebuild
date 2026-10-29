import copy
import json
import unittest

from tools.stoneage_scene18_derived_acceptance import REPORT, FALSE, validate, crossversion


class Scene18Evidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_bytes())

    def reject(self, mutate):
        r = copy.deepcopy(self.report)
        mutate(r)
        with self.assertRaises((ValueError, KeyError)):
            validate(r)

    def test_authentic_derived_source(self):
        self.assertEqual(validate(self.report)['physical_bitmapno'], 5894)

    def test_scope_cannot_be_official(self):
        self.reject(lambda r: r.update(source_scope='OFFICIAL_TW10'))

    def test_runtime_and_pixel_promotions_rejected(self):
        for k in FALSE:
            with self.subTest(field=k):
                self.reject(lambda r: r.update({k: True}))

    def test_percent_remains_unknown(self):
        self.reject(lambda r: r.update(overall_completion_percent=100))

    def test_unread_REAL_not_promoted(self):
        self.reject(lambda r: r.update(original_real_bytes_read=1668))

    def test_npc_key_not_physical_index(self):
        self.reject(lambda r: r.update(source_graphic_key=5894))

    def test_alias_collision_preserved_as_failure(self):
        self.reject(lambda r: r['source_record_matches'].append(copy.deepcopy(r['source_record_matches'][0])))

    def test_wrong_extent_rejected(self):
        self.reject(lambda r: r['source_record_matches'][0].update(original_real_offset=25018538))

    def test_wrong_whole_hash_rejected(self):
        self.reject(lambda r: r['archived_original_ADRN'].update(whole_sha256='0'*64))

    def test_crc_not_optional(self):
        self.reject(lambda r: r['archived_original_ADRN'].update(full_RAR_CRC32_verified=False))

    def test_decoder_failure_cannot_be_called_dual_success(self):
        self.reject(lambda r: r['archived_original_ADRN'].update(independent_decompressors_equal=True))

    def test_decoder_failure_cannot_be_erased(self):
        self.reject(lambda r: r['archived_original_ADRN']['secondary_decoder_failure'].update(message='success'))

    def test_missing_range_rejected(self):
        self.reject(lambda r: r['range_receipts'].pop())

    def test_duplicate_range_rejected(self):
        self.reject(lambda r: r['range_receipts'].__setitem__(1, copy.deepcopy(r['range_receipts'][0])))

    def test_byte_conservation(self):
        self.reject(lambda r: r['range_receipts'][0].update(bytes=65535))

    def test_range_hash_format(self):
        self.reject(lambda r: r['range_receipts'][0].update(sha256='unknown'))

    def test_prior_crossversion_record_does_not_certify_unread_pixels(self):
        r = crossversion()
        self.assertEqual([v['profile'] for v in r['prior_samples']], ['TW10', 'CN50', 'TW85_NATIVE'])
        self.assertIsNone(r['mixed25_REAL_RD_sha256'])
        self.assertIs(r['mixed25_RD_equality_verified'], False)
        self.assertIs(r['original_NPC_name_or_dialogue_authenticated'], False)
        self.assertEqual(r, json.loads((REPORT.parent/'STONEAGE-SCENE18-CROSSVERSION-CANDIDATE-R1.json').read_bytes()))


if __name__ == '__main__':
    unittest.main()
