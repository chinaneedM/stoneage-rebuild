import unittest

from tools.stoneage_client_hitmap_lineage_probe import (
    ALGORITHM_FEATURES,
    HEADER_FEATURES,
    algorithm_features,
    header_features,
)


MAP_SOURCE = r"""
#if 1
void readHitMap(int x1, int y1, int x2, int y2,
                unsigned short *tile, unsigned short *parts,
                unsigned short *event, unsigned short *hitMap)
{
    int width = x2 - x1, height = y2 - y1, i, j, k, l;
    short hit, hitX, hitY; unsigned long bmpNo;
    for (i=0;i<height;i++) for (j=0;j<width;j++) {
        if (tile[i*width+j] > CG_INVISIBLE ||
            (60 <= tile[i*width+j] && tile[i*width+j] <= 79)) {
            realGetNo(tile[i*width+j], &bmpNo);
            realGetHitFlag(bmpNo, &hit);
            if (hit == 0 && hitMap[i*width+j] != 2) hitMap[i*width+j] = 1;
            else if (hit == 2) hitMap[i*width+j] = 2;
        } else {
            switch (tile[i*width+j]) {
            case 0:
                if ((event[i*width+j] & MAP_SEE_FLAG) == 0) break;
            case 1: case 2: case 5: case 6: case 9: case 10:
                if (hitMap[i*width+j] != 2) hitMap[i*width+j] = 1;
                break;
            case 4: hitMap[i*width+j] = 2; break;
            }
        }
    }
    for (i=0;i<height;i++) for (j=0;j<width;j++) {
        if (parts[i*width+j] > CG_INVISIBLE) {
            realGetNo(parts[i*width+j], &bmpNo);
            realGetHitFlag(bmpNo, &hit);
            if (hit == 0) {
                realGetHitPoints(bmpNo, &hitX, &hitY);
                for (k=0;k<hitY;k++) for(l=0;l<hitX;l++)
                    if ((i - k) >= 0 && (j + l) < width)
                        hitMap[(i-k)*width+j+l] = 1;
            } else if (hit == 2) {
                realGetHitPoints(bmpNo, &hitX, &hitY);
                hitMap[i*width+j] = 2;
            } else if (hit == 1 && parts[i*width+j] >= 15680 &&
                       parts[i*width+j] <= 15732) {
                hitMap[i*width+j] = 1;
            }
        } else if (60 <= parts[i*width+j] && parts[i*width+j] <= 79) {
            realGetNo(parts[i*width+j], &bmpNo);
            realGetHitFlag(bmpNo, &hit);
        } else {
            switch (parts[i*width+j]) {
            case 1: case 2: case 5: case 6: case 9: case 10: break;
            case 4: hitMap[i*width+j] = 2; break;
            }
        }
        if ((event[i*width+j] & 0x0fff) == EVENT_NPC)
            hitMap[i*width+j] = 1;
    }
}
BOOL checkHitMap(int gx, int gy)
{
    int x = gx - mapAreaX1, y = gy - mapAreaY1;
    if (pc.skywalker) return FALSE;
    if (x < 0 || mapAreaWidth <= x || y < 0 || mapAreaHeight <= y)
        return TRUE;
    if (hitMap[y * mapAreaWidth + x] == 1) return TRUE;
    return FALSE;
}
#endif
"""

HEADER_SOURCE = r"""
typedef struct {
    unsigned char atari_x, atari_y;
    unsigned short hit;
    short height;
    unsigned int bmpnumber;
} MAP_ATTR;
struct ADRNBIN {
    unsigned long bitmapno;
    MAP_ATTR attr;
};
#ifdef _SA_VERSION_25
#define FOO 1
#endif
"""


class ClientHitmapLineageProbeTests(unittest.TestCase):

    def test_complete_algorithm_vector(self):
        features = algorithm_features(MAP_SOURCE)
        self.assertEqual(set(features), set(ALGORITHM_FEATURES))
        self.assertTrue(all(features.values()))

    def test_complete_header_vector(self):
        features = header_features(HEADER_SOURCE)
        self.assertEqual(set(features), set(HEADER_FEATURES))
        self.assertTrue(all(features.values()))

    def test_missing_special_case_is_visible(self):
        altered = MAP_SOURCE.replace("15680", "16680").replace("15732", "16732")
        features = algorithm_features(altered)
        self.assertFalse(features["parts_15680_15732"])

    def test_missing_map_attr_embedding_is_visible(self):
        altered = HEADER_SOURCE.replace("MAP_ATTR attr;", "int attr;")
        features = header_features(altered)
        self.assertFalse(features["adrnbin_embeds_map_attr"])


if __name__ == "__main__":
    unittest.main()
