"""Recover missing-TW1 item alias candidates from authenticated mixed25 ADRN/REAL."""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from html import escape
import io
import json
from pathlib import Path
import struct
import zlib

from tools.stoneage_item05_shop_stock import (
    ARCHIVE, ROOT, REPORT as SHOP_REPORT, TABLES, fingerprint, old_items,
    parse_table, read_sources, sha,
)
from tools.stoneage_pet11_tw10_capture_sprite_source import rd_indices
from tools.stoneage_private_scene_graphic_join_r1 import ADRN_SHA, REAL_SHA
from tools.stoneage_rd_codec import RDDecodeError, decode_rd_block
from tools.stoneage_tw10_palette import initial_rgb

REPORT = ROOT / 'research/recovered/STONEAGE-ITEM06-MIXED25-MISSING-TW1-ITEM-ALIAS-PIXELS-R1.json'
ASSETS = {
    'adrn_15.bin': (18765120, ADRN_SHA, '3113c408'),
    'real_15.bin': (763908374, REAL_SHA, 'bd8bab8d'),
    'Palet_1.sap': (708, '32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0', 'dacb3fc9'),
}


def missing_aliases(items):
    links = defaultdict(list)
    for item, row in sorted(items.items()):
        for table, alias, status in zip(TABLES, row[2:4], row[7:9]):
            if status == 'TW1_INDEX_NOT_FOUND':
                links[alias].append([table, item])
    return links


def resolve_aliases(raw, wanted):
    rows = defaultdict(list)
    if len(raw) % 80:
        raise ValueError('original ADRN record extent')
    for offset in range(0, len(raw), 80):
        alias, = struct.unpack_from('<I', raw, offset + 76)
        if alias in wanted:
            rows[alias].append((offset // 80, raw[offset:offset + 80]))
    return rows


def render_bitmap(block, width, height, palette):
    from PIL import Image

    try:
        header, pixels = decode_rd_block(block)
    except RDDecodeError as exc:
        try:
            w, h, pixels, _, strict = rd_indices(block)
        except ValueError:
            return 'not_decoded', str(exc), None, None
        if strict:
            raise ValueError('independent decoders disagree on strict status') from exc
        status = 'bounded_terminal_zero'
    else:
        w, h, check, _, strict = rd_indices(block)
        if not strict or check != pixels or (header['width_s'], header['height_s']) != (w, h):
            raise ValueError('independent decoders disagree on indexed pixels')
        status = 'strict'
    if (w, h) != (width, height):
        raise ValueError('original ADRN/RD geometry differs')
    image = Image.frombytes('P', (width, height), pixels).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    image.putpalette(palette)
    buffer = io.BytesIO()
    image.save(buffer, 'PNG', transparency=0)
    png = buffer.getvalue()
    with Image.open(io.BytesIO(png)) as replay:
        if replay.transpose(Image.Transpose.FLIP_TOP_BOTTOM).tobytes() != pixels:
            raise ValueError('candidate PNG indexed-pixel round trip differs')
    return status, None, pixels, png


def source_pin(path, pin):
    fingerprint(path, pin[:2])
    crc = 0
    with path.open('rb') as stream:
        while chunk := stream.read(1 << 20):
            crc = zlib.crc32(chunk, crc)
    if f'{crc:08x}' != pin[2]:
        raise ValueError('whole source CRC mismatch: ' + path.name)


def recover(directory, original_archive, output):
    for file, pin in ASSETS.items():
        source_pin(directory / file, pin)
    wanted = missing_aliases(old_items())
    rows = resolve_aliases((directory / 'adrn_15.bin').read_bytes(), wanted)
    palette = initial_rgb((directory / 'Palet_1.sap').read_bytes())
    originals = read_sources(original_archive)
    tables = {name: parse_table(originals['data/' + name]) for name in TABLES}
    shop_ids = set(json.loads(SHOP_REPORT.read_bytes())['projection']['all_slot_ids_including_zero'])
    records, cards = [], []
    with (directory / 'real_15.bin').open('rb') as real:
        for alias in sorted(wanted):
            refs = wanted[alias]
            matches = rows.get(alias, [])
            row = {'alias': alias, 'references': refs, 'shop_item_ids': sorted({i for _, i in refs} & shop_ids)}
            records.append(row)
            if len(matches) != 1:
                row['status'] = 'absent' if not matches else 'ambiguous'
                continue
            index, record = matches[0]
            bitmap, start, size, _, _, width, height = struct.unpack_from('<IIIiiii', record)
            if not (16 <= size <= 1_000_000 and start + size <= ASSETS['real_15.bin'][0] and
                    0 < width <= 1024 and 0 < height <= 1024):
                raise ValueError('original ADRN bounds')
            real.seek(start)
            block = real.read(size)
            if len(block) != size:
                raise ValueError('short original RD block')
            status, error, pixels, png = render_bitmap(block, width, height, palette)
            row.update(status=status, index=index, bitmap=bitmap, width=width, height=height,
                       record_sha256=sha(record), rd_sha256=sha(block))
            if error:
                row['decode_error'] = error
            if png is None:
                continue
            row.update(indices_sha256=sha(pixels), private_png_sha256=sha(png))
            details = ' · '.join(
                f'{table} #{item} {tables[table][item]["name"]}' for table, item in refs)
            image = base64.b64encode(png).decode('ascii')
            cards.append(f'<article><img loading="lazy" alt="别名 {alias}" src="data:image/png;base64,{image}">'
                         f'<h2>别名 {alias}</h2><p>{escape(details)}</p></article>')
    counts = Counter(row['status'] for row in records)
    source_report = {
        'schema': 'stoneage.item06.mixed25_pixels_for_missing_tw1_aliases.r1',
        'source_archive_sha256': ARCHIVE[1], 'original_members': ASSETS,
        'legacy_tw1_missing_alias_count': len(wanted), 'counts': counts, 'aliases': records,
        'private_rendered_count': len(cards), 'uses_native_selector_or_palette': False,
        'same_official_deployment_authenticated': False, 'original_client_executed': False,
        'private_original_pixel_data_published': False,
    }
    heading = (f'<h1>混合 2.5 · 补取的物品原图候选</h1><p>{len(cards)} 张原 RD 索引图可查，'
               f'{counts["absent"]} 个别名在此载体也缺索引。<br>'
               '别名取自原 ADRN +76，与物理位图号分列。Palet_1、倒行和透明用于查阅。原版图像选择与同一官方部署仍待证。</p>')
    html = ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src data:; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'">'
            '<title>石器时代 · 物品原图候选</title><style>body{max-width:1180px;margin:auto;padding:25px;background:#f8f5ec;color:#292921;font:16px/1.5 system-ui}'
            'input{font:inherit;padding:7px;width:min(350px,90%);margin-bottom:15px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}'
            'article{background:#fffdf7;border:1px solid #d6cebc;padding:12px}img{width:64px;height:64px;object-fit:contain;image-rendering:pixelated}h2{font-size:18px;margin:3px 0}p{overflow-wrap:anywhere}</style>'
            + heading + '<label>查别名、编号或原名 <input id="query" type="search"></label><main>' + ''.join(cards)
            + '</main><script>const q=document.getElementById("query"), cards=[...document.querySelectorAll("article")];'
              'q.addEventListener("input",()=>{const value=q.value.trim().toLowerCase();for(const card of cards)'
              'card.hidden=!card.textContent.toLowerCase().includes(value)});</script></html>')
    payload = html.encode('utf-8')
    if ROOT in output.resolve().parents:
        raise ValueError('private pixels must stay outside Git')
    output.write_bytes(payload)
    source_report['private_html'] = {'bytes': len(payload), 'sha256': sha(payload)}
    return source_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('qualified_directory', type=Path)
    parser.add_argument('private_archive', type=Path)
    parser.add_argument('private_html', type=Path)
    args = parser.parse_args()
    report = recover(args.qualified_directory, args.private_archive, args.private_html)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('counts', 'private_rendered_count', 'private_html')}))


if __name__ == '__main__':
    main()
