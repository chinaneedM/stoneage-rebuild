import unittest

from tools.stoneage_jss_saupdate_launch_parameter_probe import (
    MFC42_ORDINAL_6199,
    function_contains,
)


class JssSaUpdateLaunchParameterProbeTests(unittest.TestCase):
    def test_mfc_mapping_is_pinned(self):
        self.assertEqual(MFC42_ORDINAL_6199, "CWnd::SetWindowTextA")

    def test_function_contains(self):
        f={"start_rva":0x1000,"end_rva":0x1100}
        self.assertTrue(function_contains(f,0x1080))
        self.assertFalse(function_contains(f,0x1200))


if __name__=="__main__":
    unittest.main()
