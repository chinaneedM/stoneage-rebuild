import struct
import unittest

from tools.stoneage_map09_batch_scenes import independent_positions, placements, ready_names, bounds


def dat(parts):
    return struct.pack('<II',2,2)+b''.join(struct.pack('<4H',*part) for part in parts)


class Observer(unittest.TestCase):
    def test_independent_traversal_retains_repeated_planes(self):
        raw=dat([[100]*4,[100]*4,[0]*4])
        info,expected=placements(raw)
        self.assertEqual(independent_positions(raw),expected)
        self.assertEqual(len(expected),8)
        self.assertEqual([p['xy'] for p in expected[:4]],[[0,1],[1,1],[0,0],[1,0]])

    def test_low_values_and_third_plane_are_not_visible_candidates(self):
        raw=dat([[0,1,99,100],[0,0,0,0],[102]*4])
        info,expected=placements(raw)
        self.assertEqual(independent_positions(raw),expected)
        self.assertEqual([p['image_key'] for p in expected],[100])
        self.assertEqual(info['source_low_nonzero_not_rendered'],2)
        self.assertEqual(info['planes'][2]['nonzero_cells'],4)

    def test_ready_filter_excludes_missing_source_positions(self):
        index={'per_floor_source_row_columns':['original_DAT_file_basename','number_of_nonzero_positions_missing_source_qualified_TW1_RD'],
               'per_floor_source_rows':[['1.dat',0],['2.dat',1],['3.dat',0]]}
        self.assertEqual(set(ready_names(index)),{'1.dat','3.dat'})

    def test_empty_visible_map_preserves_all_grid_corners(self):
        info,selected=placements(dat([[0]*4]*3))
        size,origin=bounds(info,selected,{})
        self.assertEqual(size,[97,81])
        self.assertEqual(origin,[16,40])

    def test_original_negative_offsets_cannot_be_cropped(self):
        info,selected=placements(dat([[100,0,0,0],[0]*4,[0]*4]))
        size,origin=bounds(info,selected,{100:{'xoff':-90,'yoff':-80,'width':200,'height':180}})
        self.assertGreaterEqual(origin[0]-90,16)
        self.assertGreaterEqual(origin[1]-80,16)
        self.assertGreaterEqual(size[0],232)
        self.assertGreaterEqual(size[1],212)


if __name__=='__main__':unittest.main()
