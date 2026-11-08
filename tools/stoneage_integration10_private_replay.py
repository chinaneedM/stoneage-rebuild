"""Independent NumPy replay of the private seven checkpoint canvases; no assets in Git."""
import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import zipfile
import zlib

import numpy as np
from PIL import Image


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def replay(archive, report):
    r = json.loads(report.read_bytes())
    assert sha(archive.read_bytes()) == r['private_archive']['sha256']
    states = 0
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == r['private_archive']['members']
        images = {}
        for key, row in r['source_pixel_resources'].items():
            png = z.read('tiles/' + key + '.png')
            assert sha(png) == row['candidate_PNG_sha256']
            pixels = np.asarray(Image.open(io.BytesIO(png)).convert('RGBA'))
            assert sha(pixels.tobytes()) == row['candidate_RGBA_sha256']
            assert set(np.unique(pixels[:, :, 3])) <= {0, 255}
            images[int(key)] = pixels
        maps = {}
        for row in r['recovered_DAT']:
            raw = z.read(f'source/{row["floor"]}.dat')
            assert sha(raw) == row['sha256'] and f'{zlib.crc32(raw)&0xffffffff:08x}' == row['crc32']
            w, h = struct.unpack_from('<II', raw)
            assert [w, h] == [row['width'], row['height']] and len(raw) == 8+6*w*h
            planes = np.frombuffer(raw, dtype='<u2', offset=8).reshape(3, h, w)
            for i, plane in enumerate(planes):
                assert sha(plane.tobytes()) == row['planes'][i]['sha256']
                assert int(np.count_nonzero(plane)) == row['planes'][i]['nonzero']
            maps[row['floor']] = planes
        for row in r['source_windows']:
            x, y = row['xy']
            planes = maps[row['floor']]
            assert [int(v) for v in planes[:, y, x]] == row['checkpoint_three_u16']
            positions = []
            # Independent diagonal traversal, direct raw grid indexing.
            for plane in (0, 1):
                for diagonal in range(-10, 11):
                    for xx in range(x+5, x-6, -1):
                        yy = xx-diagonal-x+y
                        if y-5 <= yy <= y+5:
                            key = int(planes[plane, yy, xx])
                            if key > 99:
                                positions.append((plane, xx, yy, key))
            assert len(positions) == row['draw_positions']
            for mode in ('plane0', 'plane1', 'combined'):
                width, height = row['canvas_size']
                ox, oy = row['origin']
                canvas = np.empty((height, width, 4), dtype=np.uint8)
                canvas[:] = [17, 35, 42, 255]
                for plane, xx, yy, key in positions:
                    if mode == 'plane0' and plane == 1 or mode == 'plane1' and plane == 0:
                        continue
                    meta = r['source_pixel_resources'][str(key)]
                    pixels = images[key]
                    hh, ww = pixels.shape[:2]
                    left = ox+(xx-x+yy-y+10)*32+meta['xoff']
                    top = oy+(yy-y-xx+x)*24+meta['yoff']
                    assert 0 <= left <= width-ww and 0 <= top <= height-hh
                    dst = canvas[top:top+hh, left:left+ww]
                    mask = pixels[:, :, 3] == 255
                    dst[mask] = pixels[mask]
                frame = row['frames'][mode]
                assert sha(canvas.tobytes()) == frame['candidate_RGBA_sha256']
                png = z.read(row['label']+'-'+mode+'.png')
                assert sha(png) == frame['candidate_PNG_sha256']
                assert np.array_equal(canvas, np.asarray(Image.open(io.BytesIO(png)).convert('RGBA')))
                states += 1
    return dict(recovered_DAT=12, pixel_resources=len(images), complete_canvases=states, all_equal=True,
                original_client_executed=False)


if __name__ == '__main__':
    print(json.dumps(replay(Path(sys.argv[1]), Path(sys.argv[2]))))
