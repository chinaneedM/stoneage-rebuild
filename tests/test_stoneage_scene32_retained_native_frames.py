"""Later visual witnesses and capture limitations must survive continuity joins."""
import copy
import json
from pathlib import Path
import struct
import unittest
import zlib
from tools import stoneage_scene32_retained_native_frames as m

def synthetic_png(rows,filter_types):
    w=len(rows[0])//3;previous=bytes(w*3);scan=bytearray()
    for row,f in zip(rows,filter_types):
        encoded=bytearray()
        for x,value in enumerate(row):
            a=row[x-3]if x>=3 else 0;b=previous[x];c=previous[x-3]if x>=3 else 0
            if f==1:p=a
            elif f==2:p=b
            elif f==3:p=(a+b)//2
            elif f==4:
                q=a+b-c;pa,pb,pc=abs(q-a),abs(q-b),abs(q-c);p=a if pa<=pb and pa<=pc else b if pb<=pc else c
            else:p=0
            encoded.append((value-p)&255)
        scan.append(f);scan.extend(encoded);previous=row
    def chunk(k,v):return struct.pack('>I',len(v))+k+v+struct.pack('>I',zlib.crc32(k+v)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,len(rows),8,2,0,0,0))+chunk(b'IDAT',zlib.compress(scan))+chunk(b'IEND',b'')

class RetainedFrameReviewTest(unittest.TestCase):
    def setUp(self):
        s=m.sources();self.raw=copy.deepcopy(s['STONEAGE-P3H-WINDOWS-ACTUAL-R1.json']);self.review=copy.deepcopy(s['STONEAGE-P3H-VISUAL-REVIEW-R1.json']);self.primary=copy.deepcopy(s['STONEAGE-P3I-PRIMARY-ACTUAL-R1.json'])

    def join(self):return m.join_evidence(self.raw,self.review,self.primary)

    def test_raw_false_and_later_viewed_true_coexist(self):
        r=self.join();self.assertEqual(r['raw_report_viewed_flags'],[False]*3)
        self.assertEqual(r['prior_visual_witness_frame_indices'],[0,1]);self.assertTrue(r['previous_visual_task_already_satisfied'])
        self.assertEqual(r['new_original_images_discovered'],0)

    def test_published_report_replays_complete_join(self):
        self.assertEqual(json.loads(m.REPORT.read_text()),self.join())

    def test_do_not_rewrite_old_raw_false_to_true(self):
        self.raw['runtime']['observations'][0]['frame']['assistant_viewed_original']=True
        with self.assertRaisesRegex(ValueError,'raw report'):self.join()

    def test_do_not_drop_later_visual_review(self):
        self.review['assistant_directly_viewed_frame_indices']=[]
        with self.assertRaisesRegex(ValueError,'later visual witness'):self.join()

    def test_same_filenames_do_not_replace_capture_identity(self):
        self.review['frames'][0]['png_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'identity'):self.join()

    def test_duplicate_occurrence_must_remain(self):
        self.raw['runtime']['observations'].pop()
        with self.assertRaisesRegex(ValueError,'complete frame occurrences'):self.join()

    def test_nonuniform_image_is_not_qualified_game_scene(self):
        self.assertTrue(self.raw['runtime']['observations'][0]['frame']['nonuniform_pixels'])
        self.review['visible_game_picture_verified']=True
        with self.assertRaisesRegex(ValueError,'black display'):self.join()

    def test_readable_global_primary_is_not_private_game_backbuffer(self):
        self.primary['probe']['original_private_surface_read']=True
        with self.assertRaisesRegex(ValueError,'private backbuffer'):self.join()

    def test_primary_lock_success_does_not_identify_game_content(self):
        self.primary['assessment']='ORIGINAL_WORLD_RENDER_VERIFIED'
        with self.assertRaisesRegex(ValueError,'attribution'):self.join()

    def test_existing_captures_do_not_reopen_native_driver_branch(self):
        self.assertFalse(self.join()['p3i_reopening_authorized_by_these_same_images'])
        self.primary['original_run']['original_world_entered']=True
        with self.assertRaisesRegex(ValueError,'native-world'):self.join()

    def test_standard_png_decoder_all_five_filters(self):
        rows=[bytes((x*31+y*17)%256 for x in range(9))for y in range(5)]
        w,h,rgb=m.decode_rgb_png(synthetic_png(rows,list(range(5))))
        self.assertEqual((w,h,rgb),(3,5,b''.join(rows)))

    def test_png_crc_corruption_is_rejected(self):
        raw=bytearray(synthetic_png([bytes([0,0,0,255,255,255])],[0]));raw[-1]^=1
        with self.assertRaisesRegex(ValueError,'CRC'):m.decode_rgb_png(bytes(raw))

    def test_incomplete_png_is_rejected(self):
        with self.assertRaises(ValueError):m.decode_rgb_png(synthetic_png([bytes(9)],[0])[:-12])

    def test_illegal_filter_is_not_silent_black(self):
        with self.assertRaisesRegex(ValueError,'row filter'):m.decode_rgb_png(synthetic_png([bytes(9)],[5]))

    def test_metrics_keep_half_open_box_and_exact_black_count(self):
        r=m.pixel_metrics(3,2,b'\0'*9+b'\0'*3+b'\xff'*3+b'\0'*3)
        self.assertEqual((r['black_pixels'],r['nonblack_pixels'],r['nonblack_bbox'],r['colors']),(5,1,[1,1,2,2],2))

if __name__=='__main__':unittest.main()
