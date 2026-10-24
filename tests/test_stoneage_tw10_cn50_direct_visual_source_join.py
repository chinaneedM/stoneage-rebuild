"""Replay original two-version physical graphics metadata without game payloads."""
import copy
import tempfile
import unittest
from pathlib import Path
from tools.stoneage_tw10_cn50_direct_visual_source_join import (
    build, compare_physical_records, selected_adrn, verify_source)


class DirectOriginalVisualJoinTests(unittest.TestCase):
    def test_real_pinned_taiwan_and_mainland_catalogs(self):
        result=build()
        self.assertEqual(result["counts"]["direct_original_id_matches"],101)
        self.assertEqual(result["counts"]["map_collision_attr_raw_hash_equal"],101)
        self.assertEqual(result["counts"]["verified_named_npcs"],0)
        self.assertEqual(result["records"][0]["bitmap_id"],5846)
        self.assertEqual(result["records"][-1]["bitmap_id"],5946)
        self.assertFalse(result["limitations"]["same_physical_bitmap_proves_same_server_npc"])

    def test_empty_and_forged_size_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"a"
            p.write_bytes(b"bad")
            with self.assertRaises(ValueError):
                verify_source(p,"0"*64,3)
            with self.assertRaises(ValueError):
                verify_source(p,"0"*64,100)

    def test_direct_blob_mismatch_and_named_npc_rejected(self):
        from tools.stoneage_tw10_cn50_direct_visual_source_join import ROOT,CANDIDATE
        import json
        base=json.loads((ROOT/CANDIDATE).read_text(encoding="utf8"))
        fake=dict(base)
        fake["records"]=[dict(row) for row in base["records"]]
        fake["records"][0]["verified_npc_name"]="invented"
        row={k:"1" for k in ("size","xoff","yoff","width","height",
                             "rd_flag","rd_width","rd_height","rd_size_field","attr_sha256","rd_block_sha256")}
        row.update({"bitmapno":"5846","index":"0"})
        a={i:dict(row) for i in range(5846,5947)}
        with self.assertRaises(ValueError):
            compare_physical_records(fake,a,a)
        b=copy.deepcopy(a)
        b[5846]["rd_block_sha256"]="changed"
        with self.assertRaises(ValueError):
            compare_physical_records(base,a,b)

    def test_extra_catalog_rows_and_missing_ids_refused(self):
        with tempfile.TemporaryDirectory() as d:
            import gzip
            p=Path(d)/"one.gz"
            with gzip.open(p,"wt",encoding="utf8") as o:
                o.write("bitmapno\tindex\tsize\txoff\tyoff\twidth\theight\trd_flag\trd_width\trd_height\trd_size_field\tattr_sha256\trd_block_sha256\n")
                o.write("5846\t0\t16\t0\t0\t1\t1\t0\t1\t1\t16\t" + "a"*64 + "\t" + "b"*64 + "\n")
            with self.assertRaises(ValueError):
                selected_adrn(p,{5846,5847},2)
