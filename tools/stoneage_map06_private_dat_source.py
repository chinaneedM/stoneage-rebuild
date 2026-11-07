"""Recover two pinned DAT members; only metadata and CMS ciphertext leave CI."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
import zlib
from tools.stoneage_private_scene_source_r2 import acquire_bundle, qualify_carrier, seal

PINS={
 '1005.dat':(5408,'a6c9d1e43223a8afc515e37367d58cfcc6c301909e9e060d4c80d35fcb87c7c9','340d1d6a'),
 '1006.dat':(7208,'aa2e7d2bdb138545a3efa30f9482d563b1781810a856b4a91c12ce83eb08ab4a','17acbe19')}


def extract(bundle):
    import libarchive
    qualify_carrier(bundle)
    result={}
    with libarchive.file_reader(str(bundle)) as archive:
        for entry in archive:
            path=entry.pathname.replace('\\','/').lower()
            name=path.rsplit('/',1)[-1]
            if '/stoneage2.5/map/' not in path or name not in PINS:continue
            raw=b''.join(entry.get_blocks())
            actual=(len(raw),hashlib.sha256(raw).hexdigest(),f'{zlib.crc32(raw)&0xffffffff:08x}')
            if name in result or actual!=PINS[name]:raise ValueError('original DAT identity mismatch: '+name)
            result[name]=raw
    if set(result)!=set(PINS):raise ValueError('missing original DAT')
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True)
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    report={'schema':'stoneage.map06.private_dat_source.r1','original_program_executed':False,'raw_originals_published':False}
    try:
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp);bundle=acquire_bundle(work,report);raw=extract(bundle)
            report['members']={n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'} for n,b in raw.items()}
            zip_path=work/'private-dat.zip'
            with zipfile.ZipFile(zip_path,'x',zipfile.ZIP_DEFLATED) as z:
                for name,b in raw.items():z.writestr(name,b)
            report['transfer']=seal(zip_path,args.certificate,args.output/'private-dat.der')
            report['status']='PINNED_DAT_EXTRACTED_AND_ENCRYPTED'
    except Exception as exc:
        report['status']='FAILED';report['error']={'type':type(exc).__name__,'message':str(exc)[:400]};raise
    finally:
        (args.output/'source-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
