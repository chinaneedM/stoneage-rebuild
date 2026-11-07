"""Replay original TW1 SPR/ADRN/REAL for the source-qualified PET15 selection."""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import tempfile
import zipfile

from tools.stoneage_pet11_tw10_capture_sprite_source import MEMBERS, ZIP_BYTES, ZIP_SHA, rd_indices
from tools.stoneage_private_scene_actor_r7 import authenticate, need, sha
from tools.stoneage_rd_codec import RDDecodeError, decode_rd_block, parse_rd_header
from tools.stoneage_tw10_palette import initial_rgb
from tools.stoneage_tw10_resource_metadata import export_spr, parse_adrn_record

ROOT = Path(__file__).resolve().parents[1]
RECOVERED = ROOT / 'research/recovered'
METADATA = RECOVERED / 'tw10-resource-metadata'
SOURCE_MEMBERS = {
    **MEMBERS,
    'Palet_1.sap': (708, '32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0'),
}
PET07 = 'STONEAGE-PET-MODULE-07-TW10-BATCH-PUBLIC-R1.json'
PET10 = 'STONEAGE-PET-MODULE-10-ORIGINAL-MIXED25-SERVER-TABLES-R1.json'
PET07_HTML = (15123277, '58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76')
PET10_PRIVATE = (4100822, '640506addf01417390a7078f70aece167c99feecf4beeca8cb769f32972ff5d3')
TABLES = ('enemybase.txt', 'enemybase2.txt')
SPR_TABLES = tuple(f'SPR-{kind}-R1.tsv.gz' for kind in ('GROUP', 'ANIMATION', 'FRAME'))
REPORT = 'STONEAGE-PET-MODULE-15-TW10-ALL-SELECTED-MOTION-SOURCE-R1.json'
BOUNDED = 'terminal_zero_outside_canvas'
STRICT = 'strict'


def archived(name):
    return json.loads((RECOVERED / name).read_bytes())


def tsv(name):
    with gzip.open(METADATA / name, 'rt', encoding='ascii', newline='') as stream:
        yield from csv.DictReader(stream, delimiter='\t')


def selected_motion(graphics=None):
    """Use archived public records to select and independently replay the scope."""
    old = {row[0] for row in archived(PET07)['source_groups']}
    links = {table: defaultdict(list) for table in TABLES}
    keys = old.copy()
    source_rows = archived(PET10)['source_rows']
    for table in TABLES:
        for ordinal, template_id, graphic, flag, *_ in source_rows[table]:
            links[table][graphic].append([ordinal, template_id, flag])
            if flag == 1:
                keys.add(graphic)
    if graphics is not None:
        old = set()
        keys = set(graphics)
    groups = {}
    for row in tsv(SPR_TABLES[0]):
        key = int(row['spr_no'])
        if key in keys:
            need(key not in groups, 'ambiguous original TW1 SPR number')
            groups[key] = {
                'graphic': key, 'group_index': int(row['index']),
                'segment_sha256': row['segment_sha256'],
                'prior_pet07': key in old, 'source_sequences': int(row['anim_count']),
                'mixed25_same_number_rows': {table: links[table].get(key, []) for table in TABLES},
                'sequences': [],
            }
    need(old <= groups.keys(), 'PET07 scope lost an original TW1 SPR group')
    for row in tsv(SPR_TABLES[1]):
        key = int(row['spr_no'])
        if key in groups:
            g = groups[key]
            index = int(row['anim_index'])
            need(index == len(g['sequences']), 'source animation order')
            g['sequences'].append({
                'index': index, 'direction': int(row['direction']), 'action': int(row['anim_no']),
                'duration': int(row['duration']), 'frame_count': int(row['frame_count']), 'frames': [],
            })
    for row in tsv(SPR_TABLES[2]):
        key = int(row['spr_no'])
        if key in groups:
            frames = groups[key]['sequences'][int(row['anim_index'])]['frames']
            need(int(row['frame_index']) == len(frames) and row['sentinel'] == '0',
                 'source frame order or unsupported sentinel')
            frames.append([int(row[k]) for k in ('bmp_no', 'pos_x', 'pos_y', 'sound_no')])
    for group in groups.values():
        sequences = group['sequences']
        need(len(sequences) == group['source_sequences'], 'source sequence count')
        need(all(len(a['frames']) == a['frame_count'] > 0 for a in sequences), 'source frame count')
        need(len({(a['direction'], a['action']) for a in sequences}) == len(sequences),
             'multiple source sequences share one selector')
    return sorted(groups.values(), key=lambda group: group['graphic'])


def frames_of(group):
    return [frame[0] for animation in group['sequences'] for frame in animation['frames']]


def motion_summary(groups, missing):
    result = []
    for group in groups:
        row = {key: val for key, val in group.items() if key != 'sequences'}
        sequences = group['sequences']
        bitmaps = frames_of(group)
        row.update(
            frame_positions=len(bitmaps),
            distinct_bitmaps=len(set(bitmaps)),
            fully_observable_sequences=sum(all(f[0] not in missing for f in a['frames']) for a in sequences),
            source_directions=sorted({a['direction'] for a in sequences}),
            source_actions=sorted({a['action'] for a in sequences}),
        )
        result.append(row)
    return result


def extract_spr(source_zip, work):
    authenticate(source_zip, (ZIP_BYTES, ZIP_SHA))
    with zipfile.ZipFile(source_zip) as source:
        need(len(source.infolist()) == 379 and source.testzip() is None, 'original ZIP member CRC')
        for name, pin in SOURCE_MEMBERS.items():
            prefix = 'source/data/pal/' if name.endswith('.sap') else 'source/data/'
            with source.open(prefix + name) as source_stream, (work / name).open('wb') as target:
                while block := source_stream.read(1 << 20):
                    target.write(block)
            authenticate(work / name, pin)
    outputs = [work / name for name in SPR_TABLES]
    export_spr(work / 'spradrn_1.bin', work / 'spr_1.bin', *outputs)
    for path in outputs:
        need(gzip.decompress(path.read_bytes()) == gzip.decompress((METADATA / path.name).read_bytes()),
             'original replay differs from archived ' + path.name)


def decoded_bitmap(block):
    header = parse_rd_header(block)
    width, height = header['width_s'], header['height_s']
    need(0 < width <= 1024 and 0 < height <= 1024, 'original RD geometry bound')
    try:
        _, pixels = decode_rd_block(block)
    except RDDecodeError as strict_error:
        try:
            _, _, pixels, _, strict = rd_indices(block)
        except ValueError:
            return None, str(strict_error)
        need(not strict, 'strict decoders disagree')
        return pixels, BOUNDED
    _, _, check, _, strict = rd_indices(block)
    need(strict and check == pixels, 'original decoded index pixels differ')
    return pixels, STRICT


def write_bitmaps(work, wanted, output_zip):
    from PIL import Image

    adrn = (work / 'adrn_1.bin').read_bytes()
    palette = initial_rgb((work / 'Palet_1.sap').read_bytes())
    metadata = {int(row['bitmapno']): row for row in tsv('ADRN-R1.tsv.gz')
                if int(row['bitmapno']) in wanted}
    records = {}
    for offset in range(0, len(adrn), 80):
        record = adrn[offset:offset + 80]
        number = int.from_bytes(record[:4], 'little')
        if number in wanted:
            need(number not in records, 'ambiguous original physical bitmap key')
            records[number] = (offset // 80, record)
    need(wanted == records.keys() == metadata.keys(), 'missing original ADRN bitmap')
    receipts = {}
    with (work / 'real_1.bin').open('rb') as real:
        for number in sorted(records):
            index, record = records[number]
            fields = parse_adrn_record(record)
            offset, size = fields['adder'], fields['size']
            width, height = fields['width'], fields['height']
            need(16 <= size <= 1_000_000 and 0 <= offset <= SOURCE_MEMBERS['real_1.bin'][0] - size,
                 'original ADRN bitmap extent')
            real.seek(offset)
            block = real.read(size)
            previous = metadata[number]
            digest = sha(block)
            need(len(block) == size and digest == previous['rd_block_sha256'] and
                 (index, offset, size, width, height) ==
                 tuple(int(previous[key]) for key in ('index', 'adder', 'size', 'width', 'height')),
                 'original RD block and archived metadata differ')
            need((width, height) == (int.from_bytes(block[4:8], 'little', signed=True),
                                     int.from_bytes(block[8:12], 'little', signed=True)),
                 'original ADRN/RD geometry differs')
            pixels, status = decoded_bitmap(block)
            row = {'status': status, 'rd_sha256': digest, 'adrn_sha256': sha(record)}
            if pixels is not None:
                image = Image.frombytes('P', (width, height), pixels)
                image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                image.putpalette(palette)
                buffer = io.BytesIO()
                image.save(buffer, 'PNG', transparency=0)
                png = buffer.getvalue()
                with Image.open(io.BytesIO(png)) as replay:
                    need(replay.transpose(Image.Transpose.FLIP_TOP_BOTTOM).tobytes() == pixels,
                         'PNG failed exact source-index round trip')
                output_zip.writestr(f'images/{number}.png', png)
                row.update(indices_sha256=sha(pixels), candidate_png_sha256=sha(png))
            receipts[number] = row
    return receipts


def write_observer(prior, private_catalog, groups, receipts, output):
    authenticate(prior, PET07_HTML)
    authenticate(private_catalog, PET10_PRIVATE)
    before, rest = prior.read_text().split('<script type="application/json" id="source">', 1)
    old_data, after = rest.split('</script>', 1)
    # The new observer has its own PNGs. Verify the legacy selection and preserve its artifact.
    old = json.loads(old_data)
    need({g['graphic'] for g in old['groups']} == {g['graphic'] for g in groups if g['prior_pet07']},
         'PET07 private/public selections differ')
    catalog = json.loads(private_catalog.read_bytes())['source_tables']
    model = {'groups': [], 'images': {str(n): f'images/{n}.png' for n, r in receipts.items()
                                      if 'candidate_png_sha256' in r},
             'bounded': [n for n, r in receipts.items() if r['status'] == BOUNDED]}
    for group in groups:
        graphic = group['graphic']
        names = {}
        for table in TABLES:
            names[table] = []
            for ordinal, template, flag in group['mixed25_same_number_rows'][table]:
                row = catalog[table][ordinal - 1]
                fields = row['original_cp950_fields']
                need((row['record_ordinal'], int(fields[6]), int(fields[36]), int(fields[37])) ==
                     (ordinal, template, graphic, flag), 'PET10 private/public row mismatch')
                names[table].append(f'{fields[0]}（{template}，PETFLG={flag}）')
        model['groups'].append({
            'graphic': graphic, 'label': '台湾1.0原SPR候选',
            'sources': '\n'.join(f'{table}：{", ".join(names[table]) or "无同号行"}'
                                 for table in TABLES),
            'sequences': [{'action': a['action'], 'direction': a['direction'],
                           'duration_raw': a['duration'], 'frames': [f[0] for f in a['frames']],
                           'source_fields': [f[1:] for f in a['frames']]} for a in group['sequences']],
        })
    before = before.replace('img-src data:', "img-src 'self' file:")
    before = before.replace('PET07', 'PET15')
    before = before.replace('<div id="tiles" class="grid"></div>', '')
    before = before.replace('<label>动作原码', '<label>SPR图号 <select id="graphic"></select></label><label>动作原码')
    warning_start = before.index('<p class="warn">')
    warning_end = before.index('</p>', warning_start) + 4
    before = before[:warning_start] + (
        '<p class="warn">台湾1.0原动画索引与位图。旧PET07样本及混合2.5备用表新增的'
        '一个同号候选，展示源中保存的方向、动作和帧位置。候选配色、倒行与透明处理'
        '用于离线查阅。混合2.5的名字仅属于相应表，台湾1.0同名身份尚未确认。'
        '请完整解压后打开此页。</p>'
    ) + before[warning_end:]
    hint = before.index('<p class="hint">')
    before = before[:hint] + (
        '<p class="hint">重复位置保留。180毫秒是查阅播放间隔，原duration的单位待证。'
        '原帧偏移与声音字段只显示数值。</p></section><div id="tiles" class="grid"></div></main>\n'
    )
    after = after.replace("$('image').src=D.images[String(bitmap)];",
                          "const path=D.images[String(bitmap)];$('image').hidden=!path;"
                          "if(path)$('image').src=path;else $('image').removeAttribute('src');")
    after = after.replace(r"（单位未知）\n原图出处：'+seq.source+'\n像素：真实原RD先前解码的候选PNG；非原游戏运行画面'",
                          r"（单位未知）\n原帧偏移、声音字段：'+seq.source_fields[i].join(' / ')+"
                          r"'\n'+(path?(D.bounded.includes(bitmap)?'原RD末尾多一透明索引，显示画布范围内原索引':'严格解码原RD'):'原帧暂无法观察')+"
                          r"'\n混合2.5来源候选\n'+current.sources")
    after = after.replace("pic.src=D.images[String(first.frames[0])];",
                          "const path=D.images[String(first.frames[0])];if(path)pic.src=path;else pic.hidden=true;pic.loading='lazy';")
    after = after.replace("current=g;i=0;", "current=g;$('graphic').value=String(g.graphic);i=0;")
    after = after.replace("selectGroup(D.groups[0])",
                          "$('graphic').replaceChildren(...D.groups.map(g=>new Option(g.graphic,g.graphic)));"
                          "$('graphic').onchange=()=>selectGroup(D.groups.find(g=>g.graphic===Number($('graphic').value)));"
                          "selectGroup(D.groups[0])")
    need('seq.source+' not in after and 'D.bounded.includes' in after, 'PET07 observer template changed')
    data = json.dumps(model, ensure_ascii=False, separators=(',', ':')).replace('<', r'\u003c')
    output.writestr('PET15.html', before + '<script type="application/json" id="source">' + data + '</script>' + after,
                    compress_type=zipfile.ZIP_DEFLATED)


def export(source_zip, prior, private_catalog, target):
    target = target.resolve()
    need(ROOT not in target.parents and not target.exists(), 'new private delivery must be outside Git')
    groups = selected_motion()
    wanted = {n for group in groups for n in frames_of(group)}
    with tempfile.TemporaryDirectory() as workdir, zipfile.ZipFile(target, 'x') as output:
        work = Path(workdir)
        extract_spr(source_zip, work)
        receipts = write_bitmaps(work, wanted, output)
        write_observer(prior, private_catalog, groups, receipts, output)
        output.writestr('private-bitmap-receipts.json', json.dumps(receipts, separators=(',', ':')),
                        compress_type=zipfile.ZIP_DEFLATED)
    need(len(wanted) == len(receipts), 'bitmap count')
    prior_receipts = {row[0]: row for row in archived(PET07)['source_actual_pixel_receipts']}
    need(prior_receipts.keys() <= receipts.keys(), 'previous PET07 bitmap set outside current source scope')
    for n, old in prior_receipts.items():
        row = receipts[n]
        need((row['rd_sha256'], row.get('indices_sha256')) == (old[2], old[3]),
             'old PET07 source indices or raw RD changed')
    missing = {n: row['status'] for n, row in receipts.items() if 'indices_sha256' not in row}
    statuses = Counter(row['status'] if n not in missing else 'unrendered'
                       for n, row in receipts.items())
    report = {
        'schema': 'stoneage.pet15.tw10_all_selected_motion.r1',
        'source_members': SOURCE_MEMBERS, 'source_archive_sha256': ZIP_SHA,
        'groups': motion_summary(groups, missing),
        'frame_positions': sum(len(frames_of(g)) for g in groups),
        'distinct_original_bitmaps': len(wanted),
        'source_bitmap_statuses': dict(statuses),
        'unrendered_bitmaps': missing,
        'bounded_bitmaps': [n for n, row in receipts.items() if row['status'] == BOUNDED],
        'prior_pet07_strict_bitmaps_replayed': len(prior_receipts),
        'actual_source_bitmap_receipts_sha256': sha(json.dumps(receipts, separators=(',', ':')).encode()),
        'private_zip_bytes': target.stat().st_size,
        'original_client_executed': False,
        'same_historical_deployment_authenticated': False,
        'official_pet_identity_authenticated': False,
        'native_palette_or_frame_timing_verified': False,
        'proprietary_images_published': False,
    }
    with target.open('rb') as stream:
        report['private_zip_sha256'] = hashlib.file_digest(stream, 'sha256').hexdigest()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original_zip', type=Path)
    parser.add_argument('pet07_html', type=Path)
    parser.add_argument('pet10_private_catalog', type=Path)
    parser.add_argument('private_output_zip', type=Path)
    args = parser.parse_args()
    print(json.dumps(export(args.original_zip, args.pet07_html, args.pet10_private_catalog,
                            args.private_output_zip), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
