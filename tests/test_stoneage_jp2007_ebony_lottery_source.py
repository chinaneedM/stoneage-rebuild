import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_jp2007_ebony_lottery_source as m


class EbonyLotteryTests(unittest.TestCase):
    def report(self):
        return json.loads(m.REPORT.read_text())

    def test_relative_lottery_rates_preserve_unknown_absolute_rates_and_wild_ecology(self):
        r = self.report(); m.validate(r)
        for change in (
            lambda d: d['extraction'].update(acquisition_context='WILD_ENCOUNTER'),
            lambda d: d['extraction'].update(absolute_rates_or_normalization_formula={'each':.5}),
            lambda d: d['extraction'].update(other_pet_names=['A','B','C','D']),
            lambda d: d['extraction'].update(guarantee_or_pity=10),
            lambda d: d['extraction']['named_pet_relative_rates'][0].update(base_probability=.01),
            lambda d: d['extraction']['named_pet_relative_rates'][1].update(changed_probability=.02),
            lambda d: d['extraction']['named_pet_relative_rates'][0].update(original_species_id=200),
            lambda d: d['extraction'].update(pet_stats_growth_skills_habitat={'habitat':'wild'}),
            lambda d: d['extraction']['price_as_reported'].update(purchase_unit_or_bundle_count=1),
            lambda d: d['extraction']['price_as_reported'].update(currency='GASH'),
        ):
            d = copy.deepcopy(r); change(d); d['catalog_records'] = m.catalog(d['extraction'])
            with self.assertRaises(ValueError): m.validate(d)

    def test_publication_availability_and_illustration_do_not_authenticate_original_runtime(self):
        r = self.report()
        for change in (
            lambda d: d.update(version_profile='TW10'),
            lambda d: d['source'].update(authority='DIRECT_OFFICIAL_HTML'),
            lambda d: d['negative_boundaries'].update(promised_change_proves_deployment=True),
            lambda d: d['negative_boundaries'].pop('absolute_probabilities_recovered'),
            lambda d: d['archive_discovery'].update(capture_fetched=True),
            lambda d: d['archive_discovery'].update(closest_timestamp='20070730000000'),
            lambda d: d['extraction'].update(year_in_window_body_explicit=True),
            lambda d: d['extraction'].update(timezone_explicit='JST'),
            lambda d: d['visual_observations'][1].update(left_right_named_species_join=['ギガドラン','ドルーザス']),
            lambda d: d['images'][0].update(sha256='0'*64),
            lambda d: d['comparison'].update(same_pet_ids_or_build_proven=True),
            lambda d: d['comparison'].update(modern_adoption_decided=True),
        ):
            d=copy.deepcopy(r); change(d)
            with self.assertRaises(ValueError): m.validate(d)

    def test_catalog_keeps_documentary_rights_and_currencies_separate(self):
        r=self.report()
        self.assertEqual([v['collection'] for v in r['catalog_records']], ['items','pets','pets','tutorials'])
        self.assertEqual(r['extraction']['price_as_reported']['currency'], 'GStone')
        self.assertTrue(r['comparison']['gash_capture_campaign_is_separate_acquisition_and_currency'])
        for key,value in [('game_ids',1),('source_refs',['OTHER']),('rights_status','PRODUCTION_APPROVED'),('version_profile','TW10')]:
            d=copy.deepcopy(r);d['catalog_records'][0][key]=value
            with self.assertRaises(ValueError):m.validate(d)

    def test_parent_and_parser_bytes_are_required_and_not_just_valid_json(self):
        r=self.report()
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            for p in r['parent_pins']+[r['parser_pin']]:
                out=root/p['path'];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((m.ROOT/p['path']).read_bytes())
            with patch.object(m,'ROOT',root):
                m.validate(r)
                for p in r['parent_pins']+[r['parser_pin']]:
                    out=root/p['path'];raw=out.read_bytes();out.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
                    with self.assertRaises(ValueError):m.validate(r)
                    out.unlink()
                    with self.assertRaises(FileNotFoundError):m.validate(r)
                    out.write_bytes(raw)

    def test_invalid_images_cannot_be_accepted_as_promotional_art(self):
        r=self.report()
        # A valid HTML body cannot smuggle an HTML error response into a JPEG slot.
        with self.assertRaises((ValueError,OSError)):
            m.inspect_images({'I1':b'<html>error</html>','I2':b'error'},r)

    def test_custody_preserves_both_independent_jobs_raw_reports_and_honest_input_history(self):
        receipt=m.verify_custody()
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);out=root/f'research/recovered/{m.STEM}-CUSTODY-R1.json'
            for p in receipt['permanent_pins']:
                target=root/p['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((m.ROOT/p['path']).read_bytes())
            out.write_text(json.dumps(receipt));m.verify_custody(root)
            for p in receipt['permanent_pins']:
                target=root/p['path'];raw=target.read_bytes();target.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
                with self.assertRaises(ValueError):m.verify_custody(root)
                target.unlink()
                with self.assertRaises(FileNotFoundError):m.verify_custody(root)
                target.write_bytes(raw)
            changes=[lambda d:d.update(content_commit='0'*40),lambda d:d.update(content_tree='0'*40),
                     lambda d:d.update(candidate_branch='main'),lambda d:d.update(historical_bytes_authenticated=True),
                     lambda d:d.update(server_execution_verified=True),lambda d:d['runs'].pop(),
                     lambda d:d['runs'].append(d['runs'][0]),lambda d:d['runs'][0].update(conclusion='failure'),
                     lambda d:d['runs'][0].update(branch='OTHER'),lambda d:d['permanent_pins'].pop(),
                     lambda d:d.update(initial_inputs=[]),lambda d:d.update(candidate_main_raw_bytes_equal=False),
                     lambda d:d['raw_replays']['main'].update(equals_initial_inputs=False),
                     lambda d:d['jobs_and_artifacts']['main'].update(job=d['jobs_and_artifacts']['candidate']['job']),
                     lambda d:d['jobs_and_artifacts']['main']['artifact'].update(id=d['jobs_and_artifacts']['candidate']['artifact']['id']),
                     lambda d:d['jobs_and_artifacts']['main']['artifact']['workflow_run'].update(head_branch='OTHER'),
                     lambda d:d['jobs_and_artifacts']['main'].update(zip_downloaded_and_digest_verified=False)]
            for change in changes:
                d=copy.deepcopy(receipt);change(d);out.write_text(json.dumps(d))
                with self.assertRaises(ValueError):m.verify_custody(root)
            out.unlink()
            with self.assertRaises(FileNotFoundError):m.verify_custody(root)


if __name__ == '__main__':unittest.main()
