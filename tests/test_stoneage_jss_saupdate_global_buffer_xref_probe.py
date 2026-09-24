import unittest
from tools.stoneage_jss_saupdate_global_buffer_xref_probe import TARGETS

class JssSaUpdateGlobalBufferXrefProbeTests(unittest.TestCase):
    def test_unknown_launch_buffers_are_pinned(self):
        values=dict((label,va) for va,label in TARGETS)
        self.assertEqual(values["unknown-launch-buffer-1"],0x85C2FC)
        self.assertEqual(values["unknown-launch-buffer-2"],0x85BEFC)

    def test_known_state_buffers_are_controls(self):
        labels={label for _,label in TARGETS}
        self.assertIn("realbin-state-buffer",labels)
        self.assertIn("battlebin-state-buffer",labels)

if __name__=="__main__":unittest.main()
