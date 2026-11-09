"""Join original Hotoru shop parameters, seven physical item rows and image evidence."""
import argparse
import csv
import gzip
import html
from io import BytesIO
import json
from pathlib import Path
import struct
import zipfile

from tools.stoneage_item05_shop_stock import old_items, setup_keys
from tools.stoneage_integration13_hotoru_rooms import identity
from tools.stoneage_preserved_item_shop_r44 import EXPECTED, arg_fields, inventory_tokens, need, parse_items, sha
from tools.stoneage_itemset_schema_probe import INDEX

ROOT = Path(__file__).resolve().parents[1]
REC = ROOT / 'research/recovered'
REPORT = 'STONEAGE-INTEGRATION14-HOTORU-SHOP-ITEM-SOURCE-R1.json'
TARGETS = (1508, 1509, 1546, 1547, 1548, 1549, 1550)
SHOPS = {
    1305: ('genout/shop_m.create', 64, [17, 18], 'genout/ss_1305_17_18'),
    1310: ('genout/shop_m2.create', 119, [16, 16], 'genout/ss_1310_18_15'),
}
FIELDS = ('itemlist', 'limititemno', 'special_item')
COLS = ('imagenumber', 'cost', 'type', 'fieldtype', 'target', 'level', 'magicid', 'magicprob')
ICON_ZIP = (5868386, 'cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa')


def load(pattern):
    paths = list(REC.glob(pattern))
    need(len(paths) == 1, 'unique input report: ' + pattern)
    return json.loads(paths[0].read_bytes())


def field_values(raw):
    args = arg_fields(raw)
    return {k: dict(literal=args[k].decode('ascii'), tokens=inventory_tokens(args[k]) if args[k] else [],
                    value_sha256=sha(args[k])) for k in FIELDS}


def expanded(field):
    return [n for lo, hi in field['tokens'] for n in range(lo, hi+1)]


def shops_and_tables(originals):
    from tools.stoneage_scene14_independent_replay import source_blocks

    inventory = {r['path']: (r['size'],r['sha256'])
                 for r in load('*MIXED25-SERVER-FULL-SOURCE-R18.json')['all_server_occurrences']}
    inventory['setup.cf'] = EXPECTED['setup.cf']
    raw = {}
    names = ['setup.cf', 'itemset.txt', 'itemset0710.txt', 'npc/genout/npcgen.template']
    names += ['npc/'+p for create, _, _, arg in SHOPS.values() for p in (create,arg)]
    for name in names:
        data = (originals/name).read_bytes()
        need((len(data), sha(data)) == inventory[name], 'original member SHA: '+name)
        raw[name] = data

    char = load('*CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json')
    creates = {(r[0],r[1]): r for r in char['create_rows']}
    tb = [g for g in source_blocks(raw['npc/genout/npcgen.template'])
          if g['fields'].get(b'templatename') == b'npcgen_shop']
    need(len(tb) == 1 and tb[0]['fields'][b'functionset'] == b'ItemShop', 'original template function')
    primary, alternate = (parse_items(raw[p])[0] for p in ('itemset.txt','itemset0710.txt'))
    result = {}
    for floor, (create, ordinal, xy, arg) in SHOPS.items():
        data = raw['npc/'+create]
        block = source_blocks(data)[ordinal]
        prior = creates[create,ordinal]
        f = block['fields']
        corner = list(map(int,f[b'borncorner'].split(b',')))
        need(block['start'] == prior[2] and sha(data[prior[2]:prior[3]]) == prior[4], 'original CREATE span')
        need(int(f[b'floorid']) == floor and corner == xy*2, 'original CREATE coordinates')
        need(f[b'enemy'] == ('npcgen_shop|file:'+arg).encode('ascii'), 'original argument pointer')
        params = raw['npc/'+arg]
        fields = field_values(params)
        for field in fields.values():
            ids = expanded(field)
            field['counts'] = dict(occurrences=len(ids), primary=sum(i in primary for i in ids),
                                   alternate=sum(i in alternate for i in ids),
                                   both_identical=sum(i in primary and i in alternate
                                                      and primary[i][2] == alternate[i][2] for i in ids))
        result[str(floor)] = dict(create_path=create, create_ordinal=ordinal, xy=xy, create_sha256=prior[4],
                                  argument_path=arg, argument_sha256=sha(params), fields=fields,
                                  rate_literals={k:arg_fields(params)[k].decode('ascii') for k in
                                                 ('buy_rate','sell_rate','special_rate')})
    return raw, result, primary, alternate


def verify_cn_block(record, rd, source):
    need(len(record) == 80, 'CN50 original ADRN record size')
    phys, offset, size, _, _, w, h = struct.unpack_from('<IIIiiii', record)
    # The published catalog hashes attributes beginning at byte 28, not all 80 bytes.
    need((phys, offset, size, len(rd), [w,h], sha(record[28:]), sha(rd)) ==
         (source['index'], source['offset'], source['rd_bytes'], source['rd_bytes'],
          source['size'], source['attr_sha256'], source['rd_sha256']), 'CN50 original record and block')
    return w, h


def image_sources(originals, icon_zip, cn_zip, cn_receipt, aliases):
    from PIL import Image
    from tools.stoneage_private_scene_palette_r3 import candidate_rgba
    from tools.stoneage_rd_codec import decode_rd_block
    from tools.stoneage_scene14_independent_replay import decode
    from tools.stoneage_tw10_palette import initial_rgb

    palette = (originals/'Palet_1.sap').read_bytes()
    paths = load('*STONEAGE5-REAL-CAB-MSI-PATH-JOIN-R1.json')
    pal_row, = [r for r in paths['installed_files'] if r['installed_path'].lower() == 'data/pal/palet_1.sap']
    need((len(palette),sha(palette)) == (pal_row['size'],pal_row['sha256']), 'CN50 and mixed25 palette match')
    by_alias = {r['mixed25_item_image_alias']:r for r in load('*ITEM07-PATCH129*')['aliases']}
    cross_version = {a:by_alias[a]['patch_source_occurrences'][0] for a in aliases if a != 24095}
    wanted = {a:row['source_original_rd_sha256'] for a,row in cross_version.items()}
    with gzip.open(REC/'cn50-resource-metadata/ADRN-R1.tsv.gz','rt') as stream:
        matches = {h: [] for h in wanted.values()}
        for row in csv.DictReader(stream,delimiter='\t'):
            if row['rd_block_sha256'] in matches:
                matches[row['rd_block_sha256']].append(row)
    result, images = {}, {}
    need((icon_zip.stat().st_size,sha(icon_zip.read_bytes())) == ICON_ZIP,'original ITEM01 observer ZIP')
    with zipfile.ZipFile(icon_zip) as z:
        need(z.testzip() is None,'original ITEM01 observer ZIP CRC')
        receipts = json.loads(z.read('private-RD-source-receipts.json'))['source_image_rows']
        old, = [r for r in receipts if r['source_itemset_image_number_alias'] == 24095]
        png = z.read('source-TW1-original-RD-candidates/'+old['private_PNG'])
        image = Image.open(BytesIO(png)).convert('RGBA')
        need((sha(png),sha(image.tobytes())) == (old['candidate_PNG_SHA256'],old['candidate_RGBA_SHA256']),
             'existing alias 24095 candidate PNG and pixels')
        images[24095] = png
        result[24095] = dict(source='TW10_REUSED_ITEM01_OBSERVATION',index=old['retail_ADRN_ordinal'],
                             rd_sha256=old['original_RD_SHA256'], indexed_sha256=old['original_indexed_pixel_SHA256'],
                             size=list(image.size),png_sha256=sha(png),rgba_sha256=sha(image.tobytes()))
    for a, digest in sorted(wanted.items()):
        row, = matches[digest]
        result[a] = dict(source='CN50_HASH_MATCH_INDEX_ONLY', index=int(row['index']), offset=int(row['adder']),
                         rd_bytes=int(row['size']), rd_sha256=digest, attr_sha256=row['attr_sha256'],
                         size=[int(row['width']),int(row['height'])],
                         patch_index=cross_version[a]['original_patch_record_index'])
    if cn_zip is not None:
        receipt = json.loads(cn_receipt.read_bytes())
        prior_cab = load('*STONEAGE5-REAL-CAB-PAYLOAD-R1.json')
        pins = {r['name']: [r['sha256'],r['size']] for r in prior_cab['files']['inventory']}
        need(receipt['cab_sha256'] == prior_cab['source']['cab_sha256']
             and receipt['resource_files'] == {n:pins[n] for n in ('adrn_31.bin','real_31.bin')},
             'source transfer parent pins')
        need(sha(cn_zip.read_bytes()) == receipt['private_zip_sha256'], 'private source transfer SHA')
        rgb = initial_rgb(palette)
        with zipfile.ZipFile(cn_zip) as z:
            names = {f'{a}.{ext}' for a in wanted for ext in ('rd','adrn')}
            need(len(z.namelist()) == len(names) and set(z.namelist()) == names and z.testzip() is None,
                 'private source transfer CRC and extent')
            for a in wanted:
                r = result[a]
                rd, record = z.read(f'{a}.rd'), z.read(f'{a}.adrn')
                w, h = verify_cn_block(record, rd, r)
                size = r['rd_bytes']
                need(receipt['sources'][str(a)] == dict(
                    index=r['index'], offset=r['offset'], bytes=size, adrn_sha256=sha(record),
                    attr_sha256=r['attr_sha256'], rd_sha256=r['rd_sha256']), 'source job block receipt')
                header, pixels = decode_rd_block(rd, size)
                need(decode(rd) == (w,h,pixels) and [header['width_s'],header['height_s']] == [w,h],
                     'independent original index replay')
                rgba = candidate_rgba(pixels,w,h,rgb)
                buf = BytesIO()
                Image.frombytes('RGBA',(w,h),rgba).save(buf,format='PNG')
                images[a] = png = buf.getvalue()
                r.update(source='CN50_ORIGINAL_RD_WITH_BYTE_IDENTICAL_PALETTE_CANDIDATE',
                         adrn_sha256=sha(record), record_alias_field=struct.unpack_from('<i',record,76)[0],
                         indexed_sha256=sha(pixels), png_sha256=sha(png), rgba_sha256=sha(rgba))
    return result, images, identity(palette)


def export(originals, icon_zip, private_zip, cn_zip=None, cn_receipt=None):
    need((cn_zip is None) == (cn_receipt is None), 'provide source package and receipt together')
    private_zip = private_zip.resolve()
    need(not private_zip.exists() and ROOT not in private_zip.parents,'private package must be new and outside Git')
    raw, shops, primary, alternate = shops_and_tables(originals)
    prior = old_items()
    rows, private = {}, {}
    for n in TARGETS:
        need(n not in primary and n in alternate,'target must be absent from primary and present in alternate')
        line, offset, body, cols = alternate[n]
        need(prior[n][:2] == [None,sha(body)],'existing ITEM01 row pin')
        membership = {floor: [k for k,v in shop['fields'].items() if n in expanded(v)]
                      for floor,shop in shops.items()}
        rows[n] = dict(alternate_line=line, alternate_byte_offset=offset, alternate_row_sha256=sha(body),
                       alternate_bytes=len(body), primary_row=None, membership=membership,
                       fields={k:int(cols[INDEX[k]]) if cols[INDEX[k]] else None for k in COLS},
                       text_field_sha256={k:sha(cols[INDEX[k]]) for k in
                                          ('name','effectstring','argument','usefunc')})
        private[n] = (body,cols)
    pixels, images, palette = image_sources(originals,icon_zip,cn_zip,cn_receipt,
                                            {r['fields']['imagenumber'] for r in rows.values()})
    report = dict(schema='stoneage.integration14.hotoru_shop_item_source.r1',
                  mixed25_carrier_sha256=load('*MIXED25-SERVER-FULL-SOURCE-R18.json')['source_parent']['source_package_sha256'],
                  original_members={p:identity(b) for p,b in sorted(raw.items())},
                  setup_literal_paths=setup_keys(raw['setup.cf']), shops=shops, items=rows,
                  image_sources=pixels, palette_candidate=palette,
                  native_loading_verified=False, native_trade_verified=False,
                  native_palette_selection_verified=False, same_official_deployment_verified=False,
                  new_cn50_rd_decode_count=sum(v['source'].startswith('CN50_ORIGINAL') for v in pixels.values()))
    with zipfile.ZipFile(private_zip,'x',zipfile.ZIP_DEFLATED) as z:
        z.writestr('index.html',observer(shops,rows,private,images))
        z.writestr('source-joins.json',json.dumps(report,sort_keys=True,indent=2)+'\n')
        for a,png in images.items():
            z.writestr(f'images/{a}.png',png)
        for n,(line,_) in private.items():
            z.writestr(f'original-rows/{n}.cp950',line)
        for shop in shops.values():
            name = 'npc/'+shop['argument_path']
            z.writestr('source/'+name,raw[name])
        if cn_zip is not None:
            z.writestr('source/cn50-rd-blocks.zip',cn_zip.read_bytes())
            z.writestr('source/cn50-rd-receipt.json',cn_receipt.read_bytes())
            z.writestr('source/Palet_1.sap',(originals/'Palet_1.sap').read_bytes())
    with zipfile.ZipFile(private_zip) as z:
        need(z.testzip() is None,'private output CRC')
        report['private_package'] = {**identity(private_zip.read_bytes()),'members':len(z.namelist())}
    return report


def observer(shops, rows, private, images):
    field_names = {'itemlist':'ItemList','limititemno':'LimitItemNo','special_item':'special_item'}
    context = []
    for f,shop in shops.items():
        label = '医院商人' if f == '1305' else '营养剂名人家商人'
        values = ' · '.join(f'{field_names[k]} {v["literal"] or "空"}' for k,v in shop['fields'].items())
        context.append(f'<h2>{f} · {label} {shop["xy"]}</h2><p>{html.escape(values)}</p>')
    cells = []
    for n,r in rows.items():
        _,cols = private[n]
        name,effect,arg = (html.escape(cols[INDEX[k]].decode('cp950')) for k in ('name','effectstring','argument'))
        a = r['fields']['imagenumber']
        origin = '台湾 1.0 候选' if a == 24095 else '大陆 5.0 候选'
        img = f'<img src="images/{a}.png" alt="图号 {a}"><small>{origin}</small>' if a in images else '原图待取'
        fields = [' / '.join(field_names[k] for k in r['membership'][f]) or '—' for f in shops]
        cells.append(f'<tr><td>{img}<small>{a}</small></td><td><b>{n} · {name}</b><br>{effect}<br>{arg}</td>'
                     f'<td>{fields[0]}</td><td>{fields[1]}</td><td>{r["fields"]["cost"]}</td></tr>')
    return ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" '
            'content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" '
            'content="default-src \'none\'; img-src \'self\' file:; style-src \'unsafe-inline\'">'
            '<title>霍特爾商店原配置对照</title><style>body{font:16px system-ui;background:#10232a;color:#eef1ec;'
            'padding:28px;max-width:1050px;margin:auto}table{border-collapse:collapse;width:100%}'
            'td,th{border-bottom:1px solid #48616a;padding:10px;text-align:left}img{width:64px;'
            'image-rendering:pixelated;display:block}small{color:#a9c2bf}b,h1{color:#f5ce88}</style>'
            '<h1>霍特爾商店原配置对照</h1><p>七个编号均只见于备用物品表。图片保留各自来源，'
            '原生调色板选择与实际交易待证。cost 是原表字段。</p>' + ''.join(context)
            + '<table><thead><tr><th>候选图</th><th>备用表原行</th><th>医院</th><th>营养剂名人家</th>'
            '<th>cost</th></tr></thead><tbody>' + ''.join(cells) + '</tbody></table></html>')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('originals','icon_zip','private_zip','report'):
        p.add_argument(name,type=Path)
    p.add_argument('--cn-zip',type=Path)
    p.add_argument('--cn-receipt',type=Path)
    a = p.parse_args()
    report = export(a.originals,a.icon_zip,a.private_zip,a.cn_zip,a.cn_receipt)
    a.report.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
