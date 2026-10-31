"""Mutation/negative tests on metadata only; no original asset downloads or images."""
import copy
import json
import unittest

from tools.stoneage_o17_map1003_source_contract import REPORT, validate

class O17Map1003ContractTests(unittest.TestCase):
    def setUp(self):
        self.report=json.loads(REPORT.read_bytes())

    def test_exact_accepted_derived_receipt(self):
        self.assertEqual(validate(self.report)["source_original_placements"],134)

    def test_evidence_boundary_mutations_are_rejected(self):
        changes=[
            ("map","sha256","0"*64),("map","plane_image_occurrences",[134,0]),
            ("map","third_plane_semantics_known",True),
            ("original_source","mixed25_REAL_actual_read",True),
            ("original_source","mixed25_ADRN_actual_read",True),
            ("original_source","mixed25_graphic_sha_still_depends_on_archived_prefix_witness",False),
            ("material","distinct_graphic_keys",[]),
            ("material","rd_flags",{"1":37}),
            ("material","reserved_nonzero_palette_keys",{"401":[1]}),
            ("candidate","original_world_entered",True),
            ("candidate","same_deployed_build_proven",True),
            ("candidate","original_client_runtime_colors_proven",True),
            ("candidate","combined_RGBA_sha256","0"*64),
            ("candidate","independent_full_rgba_overlay_equal",False),
            ("private","zip_readback_verified",False),
            ("private","proprietary_assets_published",True)]
        for section,field,value in changes:
            with self.subTest(section=section,field=field):
                changed=copy.deepcopy(self.report)
                changed[section][field]=value
                with self.assertRaises(ValueError):
                    validate(changed)

if __name__=="__main__":
    unittest.main()
