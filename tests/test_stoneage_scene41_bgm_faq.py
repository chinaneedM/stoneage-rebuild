import unittest
from tools.stoneage_scene41_bgm_faq import EXPECTED_NAMES, DESCRIPTORS, parse_page, original_names, SOURCE_URL, ROOT
import json
class Scene41SourceBoundary(unittest.TestCase):
    def test_exact_original_names(self):
        self.assertEqual(set(original_names()),set(EXPECTED_NAMES))
    def example(self, labels=DESCRIPTORS, names=EXPECTED_NAMES, date="2001-06-14", end="在北岛守桥的愿藏很烦"):
        lines=" ".join(n+" "+v for n,v in zip(names,labels))
        txt=f"<html><head><title>石器时代之全问答集</title></head><body>石器时代之全问答集 {date} 作者：未知 我可以更改石器时代的音乐吗？ {lines} {end}</body></html>"
        return (txt+" "*2100).encode("gb18030")
    def test_frozen_source_semantics(self):
        x=parse_page(self.example(),SOURCE_URL)
        self.assertEqual(x["row_count"],11)
        self.assertEqual(x["cross_reference_exact_file_name_count"],11)
        self.assertIs(x["game_sound_event_playback_observed"],False)
        self.assertIs(x["historical_published_bytes_authentic"],False)
        self.assertIs(x["original_taiwan_v1_event_selector_verified"],False)
    def test_bad_event_label_rejected(self):
        vals=list(DESCRIPTORS);vals[7]="抓到宠物"
        with self.assertRaises(AssertionError):parse_page(self.example(labels=vals),SOURCE_URL)
    def test_bad_filename_rejected(self):
        vals=list(EXPECTED_NAMES);vals[7]="sabgm_s2"
        with self.assertRaises(AssertionError):parse_page(self.example(names=vals),SOURCE_URL)
    def test_doubled_filename_rejected(self):
        names=list(EXPECTED_NAMES);names[8]="sabgm_s0"
        with self.assertRaises(AssertionError):parse_page(self.example(names=names),SOURCE_URL)
    def test_bad_date_rejected(self):
        with self.assertRaises(AssertionError):parse_page(self.example(date="2004-09-07"),SOURCE_URL)
    def test_bad_location_rejected(self):
        with self.assertRaises(AssertionError):parse_page(self.example(),"https://example.com/stoneage")
    def test_encoding_break_inside_section_rejected(self):
        b=self.example();needle="魔王战斗音乐".encode("gb18030");p=b.index(needle)
        b=b[:p]+b"\xff"+b[p:]
        with self.assertRaises(AssertionError):parse_page(b,SOURCE_URL)
    def test_frozen_actual_original_source_identity(self):
        p=ROOT/"research/recovered/STONEAGE-SCENE41-17173-BGM-PLAYER-CLAIMS-R1.json"
        d=json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual((d["current_http_bytes"],d["current_http_sha256"],d["selected_decoding"]),
                         (50771,"3c9af2d5456e52b184580ffa05b7039b7473bac475b32bace3b17caf810a63de","utf-8"))
        self.assertEqual(tuple(x["basename"] for x in d["rows"]),EXPECTED_NAMES)
        self.assertEqual(tuple(x["faq_player_label"] for x in d["rows"]),DESCRIPTORS)
    def test_source_not_native_playback_or_official_build(self):
        p=ROOT/"research/recovered/STONEAGE-SCENE41-17173-BGM-PLAYER-CLAIMS-R1.json"
        d=json.loads(p.read_text(encoding="utf-8"))
        for k in ("game_sound_event_playback_observed","original_taiwan_v1_event_selector_verified","historical_published_bytes_authentic","original_article_first_publication_time_verified"):
            self.assertIs(d[k],False,k)
        self.assertEqual(d["new_original_source_client_audio_files"],0)
    def test_all_historical_names_but_no_extra_wav(self):
        s=original_names()
        self.assertEqual(len(s),11)
        self.assertNotIn("sabgm_b2",s)
        self.assertNotIn("sabgm_t2",s)
if __name__=="__main__": unittest.main()
