import unittest
from tools.stoneage_private_scene_palette_r3 import sweep,anchor,candidate_rgba,palette_program_witness

class PrivateScenePaletteTests(unittest.TestCase):
    def test_grid_axes_are_source_direction(self):
        self.assertEqual(anchor(1,0),(32,-24))
        self.assertEqual(anchor(0,1),(32,24))
        self.assertEqual(anchor(1,1),(64,0))

    def test_diagonal_source_walk_not_row_major(self):
        self.assertEqual(sweep(3,3),[(0,2),(1,2),(0,1),(2,2),(1,1),(0,0),(2,1),(1,0),(2,0)])

    def test_rectangular_and_single_cell_walks_cover_once(self):
        for w,h in [(1,1),(1,4),(4,1),(2,5),(5,2),(64,64)]:
            self.assertEqual(set(sweep(w,h)),{(x,y)for y in range(h)for x in range(w)})

    def test_unbounded_or_noninteger_viewport_refused(self):
        for w,h in [(0,3),(65,2),(3,65),(True,1),(2.5,2)]:
            with self.assertRaises(ValueError):sweep(w,h)

    def test_source_rows_inverted_and_zero_is_transparent(self):
        rgb=bytes(v for i in range(256)for v in (i,i,i))
        result=candidate_rgba(bytes([0,16,17,18]),2,2,rgb)
        self.assertEqual(result,bytes([17,17,17,255,18,18,18,255,0,0,0,0,16,16,16,255]))

    def test_visible_reserved_slots_do_not_inherit_unverified_colors(self):
        for index in (1,15,240,255):
            with self.assertRaisesRegex(ValueError,'reserved'):
                candidate_rgba(bytes([index]),1,1,bytes(768))

    def test_palette_168_black_remains_opaque(self):
        self.assertEqual(candidate_rgba(bytes([168]),1,1,bytes(768)),bytes([0,0,0,255]))

    def test_bad_image_and_color_extents_refused(self):
        with self.assertRaises(ValueError):candidate_rgba(bytes(2),2,2,bytes(768))
        with self.assertRaises(ValueError):candidate_rgba(bytes(1),1,1,bytes(767))

    def test_unqualified_program_cannot_supply_palette_selection(self):
        with self.assertRaisesRegex(ValueError,'unqualified'):
            palette_program_witness(b'MZ'+bytes(561150))

if __name__=='__main__':unittest.main()
