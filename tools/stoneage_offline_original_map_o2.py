"""O2 private mixed25 town-map pixels integrated as an explicitly qualified OFFLINE observation.

This is NOT an official TW1 map, not a native game session, and never copies
copyrighted scene data into Git. It consumes only the already source-qualified
SCENE21 private output and independently replays its bounded raw pixels.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import zipfile

from tools import stoneage_scene21_town1000 as scene

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "stoneage.private_offline_map_o2_bridge.r1"
SCENE_HTML = "stoneage-town1000-scene21-observer.html"
VIEW_TEMPLATE = ROOT / "tools/stoneage_scene21_observer.html"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inspect_public() -> dict:
    """Re-check the frozen public contract; this contains no original game pixels."""
    r = json.loads(scene.REPORT.read_bytes())
    scene.validate(r)
    require(r["remaining_unresolved_map_image_keys"] == [], "bounded source keys")
    return r


def safe_directories(source: Path, output: Path) -> tuple[Path, Path]:
    src, dst, repo = source.expanduser().resolve(), output.expanduser().resolve(), ROOT.resolve()
    require(src.is_dir() and not source.is_symlink(), "verified SCENE21 private source directory required")
    require(dst.is_dir() and not output.is_symlink() and not any(dst.iterdir()),
            "output directory must exist, be empty and not be a symlink")
    require(src != dst and src not in dst.parents and dst not in src.parents,
            "output cannot overlap the source evidence")
    require(repo != src and repo not in src.parents and repo != dst and repo not in dst.parents,
            "copyrighted original resources must remain outside the public repository")
    return src, dst


def require_real_file(path: Path) -> bytes:
    require(path.is_file() and not path.is_symlink(), "missing/linked private source " + path.name)
    return path.read_bytes()


def verify_private(source: Path) -> dict:
    """Verify 77 original map cells, 56 RD payloads and all eight full-frame composites.

    The map is mixed25 preserved data. Original art bytes are qualified through
    the already archived exact TW1/mixed25 resource-prefix evidence. That does
    not authenticate an original Taiwan 1.0 deployed map.
    """
    from PIL import Image
    from tools.stoneage_rd_codec import decode_rd_block
    from tools.stoneage_scene14_independent_replay import decode as independent_decode
    from tools.stoneage_private_scene_palette_r3 import candidate_rgba
    from tools.stoneage_tw10_palette import initial_rgb

    require(source.is_dir(), "private SCENE21 directory not found")
    r = inspect_public()
    report_bytes = require_real_file(source / "source-derived-report.json")
    require(json.loads(report_bytes) == r, "private SCENE21 report differs from frozen public source")
    source_zip = require_real_file(source / "private-original-subset.zip")
    records = {int(k): v for k, v in r["resources"].items()}
    expected_names = {"1000.DAT", "Palet_1.sap"} | {str(k) + ".rd" for k in records}
    images = {}
    with zipfile.ZipFile(io.BytesIO(source_zip)) as z:
        names = z.namelist()
        require(len(names) == len(expected_names) and set(names) == expected_names,
                "exact bounded DAT/palette/56 RD inventory only")
        require(all(z.getinfo(n).file_size == (153608 if n == "1000.DAT" else
                    708 if n == "Palet_1.sap" else records[int(n[:-3])]["size"])
                    for n in names), "original archive member byte-length mismatch")
        dat, pal = z.read("1000.DAT"), z.read("Palet_1.sap")
        require(digest(dat) == r["source_map_sha256"] and
                digest(pal) == r["source_palette_sha256"], "source DAT or SAP mismatch")
        cells, placements, words = scene.map_cells(dat)
        require(cells == r["cells"] and placements == r["placements"] and
                words == r["NPC_cell_original_three_u16"], "entire 77-cell original map mismatch")
        for key, row in records.items():
            rd = z.read(str(key) + ".rd")
            require(digest(rd) == row["RD_sha256"], "source RD digest mismatch")
            header, px = decode_rd_block(rd, authoritative_block_size=len(rd))
            w, h, independent = independent_decode(rd)
            require((w, h, independent) == (row["width"], row["height"], px),
                    "two RD decoders disagree")
            require(digest(px) == row["index_sha256"], "original pixel-index digest mismatch")
            rgba = candidate_rgba(px, w, h, initial_rgb(pal))
            require(digest(rgba) == row["RGBA_candidate_sha256"],
                    "source candidate palette/orientation digest mismatch")
            images[key] = Image.frombytes("RGBA", (w, h), rgba)
    frames = {}
    for name, expected in r["frames"].items():
        require(name.startswith(("old_", "expanded_")), "invalid bounded scene state")
        old = name.startswith("old_")
        parts = "_parts1_" in name
        npc = name.endswith("_npc1")
        generated = scene.render(images, records, placements, old, parts, npc,
                                 r["origin"], r["canvas_size"])
        require(digest(generated.tobytes()) == expected["RGBA_sha256"],
                "full map recomposition pixel mismatch " + name)
        raw = require_real_file(source / (name + ".png"))
        require(digest(raw) == expected["PNG_sha256"], "private PNG digest mismatch " + name)
        with Image.open(io.BytesIO(raw)) as image:
            require(image.size == tuple(r["canvas_size"]) and
                    image.convert("RGBA").tobytes() == generated.tobytes(),
                    "PNG decoded pixels differ from full original composite")
        frames[name] = raw
    require(len(frames) == 8 and len(images) == 56 and len(placements) == 85,
            "bounded original image coverage is incomplete")
    model = {"report": r, "frames": {
        k: __import__("base64").b64encode(v).decode("ascii") for k, v in frames.items()
    }}
    template = VIEW_TEMPLATE.read_text(encoding="utf-8")
    require(template.count("__PRIVATE_SCENE_JSON__") == 1,
            "historical observer injection boundary changed")
    expected_html = template.replace("__PRIVATE_SCENE_JSON__",
                                     json.dumps(model, separators=(",", ":")))
    source_html = require_real_file(source / SCENE_HTML)
    require(source_html == expected_html.encode("utf-8"),
            "private observer HTML no longer matches audited in-repository template")
    receipt = {
        "schema": SCHEMA,
        "material_scope": "PRESERVED_MIXED25_MAP_WITH_BYTE_QUALIFIED_TW1_GRAPHIC_PREFIX",
        "source_report_git_path": str(scene.REPORT.relative_to(ROOT)),
        "source_report_sha256": digest(scene.REPORT.read_bytes()),
        "private_source_report_sha256": digest(report_bytes),
        "private_subset_zip_sha256": digest(source_zip),
        "map_source_sha256": digest(dat),
        "palette_source_sha256": digest(pal),
        "map_floor": 1000,
        "map_source_cells_verified": len(cells),
        "source_original_map_image_occurrences_verified": len(placements),
        "original_RD_images_independently_decoded": len(images),
        "verified_private_composites": {k: {
            "PNG_sha256": digest(v), "RGBA_sha256": r["frames"][k]["RGBA_sha256"]
        } for k, v in frames.items()},
        "original_client_executable_started": False,
        "original_game_world_entered": False,
        "original_server_used": False,
        "authentic_TW1_deployed_map_verified": False,
        "native_tile_order_palette_collision_verified": False,
        "modern_offline_research_overlay_only": True,
        "original_resource_pixels_verified_against_existing_custody": True,
        "historical_build_versions_automatically_combined": False,
        "copyrighted_assets_published": False,
        "overall_restoration_percent": None,
        "next_evidence_gate": "TW1_ORIGINAL_MAP_SOURCE_OR_EXPLICIT_LATER_VERSION_SCOPE"
    }
    return {"receipt": receipt, "frames": frames, "html": source_html}


def landing_html(receipt: dict) -> str:
    require(receipt["schema"] == SCHEMA, "O2 private source receipt required")
    return ("""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none';style-src 'unsafe-inline'">
<title>石器时代｜离线原图场景考察 O2</title>
<style>body{background:#152126;color:#f1f4f2;font:16px/1.7 system-ui,"Microsoft YaHei",sans-serif;
max-width:900px;margin:30px auto;padding:0 20px}a{color:#9dd4fa}
section{padding:16px;border:1px solid #617781;margin:12px 0;border-radius:9px}</style></head><body>
<h1>石器时代｜原图地图离线观察</h1>
<section><strong>版本隔离：</strong>该1000.DAT地图来自后期保存的mixed25载体，地图本身
不能标成官方台湾1.0。绘图源像素与台湾1.0的已验证前缀有严格字节关系，但原生层级、
配色选择、遮挡、碰撞、传送或原服务器NPC行为仍未证明。</section>
<p><a href="stoneage-town1000-scene21-observer.html">打开已验证的原图场景观察台</a></p>
<p>可查77个原地图格、85次原图位置引用、56个解码原图候选和8张完整拼合画面。
这是现代研究工具，不是原游戏世界；操作选择器为人工观察。</p>
<p>本地证据：<code>map-o2-receipt.json</code>；八张校验PNG在 <code>frames/</code>。
所有原图仅供私人研究，不得公开发布。</p></body></html>""")


def emit(source: Path, output: Path) -> dict:
    src, dst = safe_directories(source, output)
    verified = verify_private(src)
    receipt, frames = verified["receipt"], verified["frames"]
    try:
        (dst / "frames").mkdir()
        for key, data in frames.items():
            (dst / "frames" / (key + ".png")).write_bytes(data)
        (dst / SCENE_HTML).write_bytes(verified["html"])
        (dst / "map-o2-receipt.json").write_text(
            json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        (dst / "index.html").write_text(landing_html(receipt), encoding="utf-8")
    except BaseException:
        shutil.rmtree(dst / "frames", ignore_errors=True)
        for item in (SCENE_HTML, "map-o2-receipt.json", "index.html"):
            (dst / item).unlink(missing_ok=True)
        raise
    return receipt


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scene21-private-dir", type=Path, required=True)
    p.add_argument("--private-output-dir", type=Path, required=True)
    args = p.parse_args()
    result = emit(args.scene21_private_dir, args.private_output_dir)
    print(json.dumps({
        "O2": "VERIFIED_ORIGINAL_PIXELS_MIXED25_MAP_NOT_AUTHENTICATED_TW1_MAP",
        "scene": str(args.private_output_dir / "index.html"),
        "original_game_world_entered": result["original_game_world_entered"],
        "source_images": result["original_RD_images_independently_decoded"],
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
