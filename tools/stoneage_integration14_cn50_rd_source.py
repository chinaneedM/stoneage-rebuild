"""Acquire five identified original RD blocks and encrypt them for private review."""
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

from tools.stoneage_stoneage5_cab_probe import iso_file_slice
from tools.stoneage_stoneage5_full_cab_acquisition import checked_layout, download_cab, hash_file
from tools.stoneage_stoneage5_msi_probe import find_entry, load_root

REC = Path(__file__).resolve().parents[1] / 'research/recovered'
ALIASES = {22408, 22373, 22388, 22368, 22410}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def targets():
    item07 = json.loads((REC/'STONEAGE-ITEM07-PATCH129-ITEM-ALIAS-CROSSVERSION-SOURCE-R1.json').read_bytes())
    by_sha = {}
    for row in item07['aliases']:
        alias = row['mixed25_item_image_alias']
        if alias in ALIASES:
            occurrence, = row['patch_source_occurrences']
            by_sha[occurrence['source_original_rd_sha256']] = alias
    if set(by_sha.values()) != ALIASES:
        raise ValueError('five exact ITEM07 compressed hashes required')
    with gzip.open(REC/'cn50-resource-metadata/ADRN-R1.tsv.gz', 'rt') as index:
        matches = [(by_sha[row['rd_block_sha256']], row)
                   for row in csv.DictReader(index, delimiter='\t') if row['rd_block_sha256'] in by_sha]
    if len(matches) != len(ALIASES) or {a for a, _ in matches} != ALIASES:
        raise ValueError('each compressed hash must have a unique CN50 position')
    return dict(matches)


def acquire(output, certificate):
    selected = targets()
    prior = json.loads((REC/'STONEAGE-STONEAGE5-REAL-CAB-PAYLOAD-R1.json').read_bytes())
    pins = {r['name']: (r['sha256'], r['size']) for r in prior['files']['inventory']}
    _, _, _, track, bin_row, url, _, entries = load_root()
    cab = find_entry(entries, 'DATA1.CAB')
    if (int(cab['size']), int(cab['extent']), int(bin_row['size'])) != (612584670, 28, 733057248):
        raise ValueError('carrier extent changed')
    prefix, status, _ = iso_file_slice(url, cab, track, 0, 65536)
    if status != 206:
        raise ValueError('carrier range unavailable')
    checked_layout(prefix)
    with tempfile.TemporaryDirectory(prefix='stoneage-i14-') as tmp:
        work = Path(tmp)
        cabfile = work/'DATA1.CAB'
        digest = download_cab(url, cab, track, int(bin_row['size']), cabfile)
        if digest != prior['source']['cab_sha256']:
            raise ValueError('complete original CAB SHA mismatch')
        subprocess.run(['cabextract', '-q', '-F', '*_31.bin', '-d', str(work), str(cabfile)], check=True)
        for name in ('adrn_31.bin', 'real_31.bin'):
            if hash_file(work/name) != pins[name]:
                raise ValueError('complete original resource SHA mismatch: '+name)
        output.mkdir(parents=True, exist_ok=True)
        private = work/'five-source-blocks.zip'
        receipts = {}
        with zipfile.ZipFile(private, 'w', zipfile.ZIP_DEFLATED) as archive, \
             (work/'adrn_31.bin').open('rb') as adrn, (work/'real_31.bin').open('rb') as real:
            for alias, row in sorted(selected.items()):
                index, offset, size = (int(row[k]) for k in ('index','adder','size'))
                adrn.seek(80*index)
                record = adrn.read(80)
                real.seek(offset)
                rd = real.read(size)
                if (sha(record), sha(rd)) != (row['attr_sha256'], row['rd_block_sha256']):
                    raise ValueError('original ADRN or RD source window mismatch')
                archive.writestr(f'{alias}.adrn', record)
                archive.writestr(f'{alias}.rd', rd)
                receipts[alias] = dict(index=index, offset=offset, bytes=size,
                                       adrn_sha256=sha(record), rd_sha256=sha(rd))
        subprocess.run(['openssl','cms','-encrypt','-binary','-aes256','-outform','DER',
                        '-in',str(private),'-out',str(output/'five-source-blocks.cms'),str(certificate)], check=True)
        (output/'source-receipt.json').write_text(json.dumps(
            dict(cab_sha256=digest, resource_files={n:pins[n] for n in ('adrn_31.bin','real_31.bin')},
                 private_zip_sha256=sha(private.read_bytes()), sources=receipts), sort_keys=True, indent=2)+'\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--certificate', type=Path, required=True)
    a = p.parse_args()
    acquire(a.output, a.certificate)
