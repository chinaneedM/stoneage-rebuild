import unittest

from tools.stoneage_ordered_warp_runtime import load_ordered_materializable_runtime


class OrderedWarpRuntimeProbeContractTests(unittest.TestCase):

    def test_real_ordered_runtime_contract(self):
        runtime = load_ordered_materializable_runtime()
        self.assertEqual(len(runtime.topology.maps), 826)
        self.assertEqual(len(runtime.topology.legacy_warps), 2724)
        self.assertEqual(len(runtime.ordered_resolutions), 32)
        self.assertEqual(len(runtime.unresolved_ambiguous_sources), 0)
        self.assertEqual(
            runtime.unreachable_resolved_supplemental_ids,
            (820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 831),
        )


if __name__ == "__main__":
    unittest.main()
