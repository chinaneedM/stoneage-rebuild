"""Observe the remaining source-bounded TW1 character-number SPR groups privately.

This is a source-number interval, not an authenticated character/variant roster.
Sentinel frame positions remain in the original sequence, with no invented image.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
from tools import stoneage_char10_tw10_full_motion as previous
from tools import stoneage_pet15_tw10_full_motion as motion

REPORT=motion.RECOVERED/'STONEAGE-CHAR11-TW10-REMAINING-BODY-MOTION-R1.json'
SENTINEL=0xffffffff
GROUP_KEYS=set(range(100000,100240))-set(range(100000,100221,20))


def selected():
    groups=motion.selected_motion(GROUP_KEYS,allow_sentinels=True)
    motion.need({g['graphic'] for g in groups}==GROUP_KEYS,'remaining TW1 source interval incomplete')
    for g in groups:
        g.pop('mixed25_same_number_rows');g.pop('prior_pet07')
    return groups


def sentinels(groups):
    return [{'graphic':g['graphic'],'source_animation_index':s['index'],
             'direction':s['direction'],'action':s['action'],'source_frame_index':i,
             'original_frame_words':f}
            for g in groups for s in g['sequences'] for i,f in enumerate(s['frames']) if f[0]==SENTINEL]


def observer(groups,receipts):
    page=previous.observer(groups,receipts)
    page=page.replace('CHAR10','CHAR11').replace('十二个源SPR数字候选','228个源SPR数字候选')
    page=page.replace('全部源动作','其余人物候选全部源动作')
    page=page.replace('完整解压后打开。','0xFFFFFFFF源帧位置标记保留；该位置无已核实位图，不猜原客户端处理。完整解压后打开。')
    return page


def synthetic_fixture():
    groups=selected()
    numbers={n for g in groups for n in motion.frames_of(g) if n!=SENTINEL}
    receipts={n:{'candidate_png_sha256':'synthetic-fixture','status':'SYNTHETIC_BROWSER_FIXTURE'} for n in numbers}
    return observer(groups,receipts).replace('<title>',
        '<meta name="synthetic-fixture" content="metadata-and-test-pixels-only"><title>',1)


def export(source_zip,target):
    target=target.resolve()
    motion.need(motion.ROOT not in target.parents and not target.exists(),'new private delivery must be outside Git')
    groups=selected()
    wanted={n for g in groups for n in motion.frames_of(g) if n!=SENTINEL}
    with tempfile.TemporaryDirectory() as tmp,zipfile.ZipFile(target,'x') as out:
        work=Path(tmp);motion.extract_spr(source_zip,work)
        receipts=motion.write_bitmaps(work,wanted,out)
        out.writestr('CHAR11.html',observer(groups,receipts),compress_type=zipfile.ZIP_DEFLATED)
        out.writestr('private-pixel-receipts.json',json.dumps(receipts,sort_keys=True),compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(target) as z:motion.need(z.testzip() is None,'private ZIP member CRC')
    unresolved={n:r['status'] for n,r in receipts.items() if 'indices_sha256' not in r}
    missing={**unresolved,SENTINEL:'unresolved_source_sentinel_no_bitmap'}
    summary=motion.motion_summary(groups,missing)
    for g,row in zip(groups,summary):
        numbers=motion.frames_of(g)
        row['distinct_bitmaps']=len(set(numbers)-{SENTINEL})
        row['source_sentinel_positions']=numbers.count(SENTINEL)
    with target.open('rb') as stream:zip_sha=hashlib.file_digest(stream,'sha256').hexdigest()
    report={'schema':'stoneage.char11.tw10_remaining_body_motion.r1',
      'source_scope':'TW10_RETAIL_SPR_100000_100239_MINUS_CHAR10_NOT_AUTHENTICATED_CHARACTER_OR_VARIANT_ROSTER',
      'source_archive_bytes':motion.ZIP_BYTES,'source_archive_sha256':motion.ZIP_SHA,'source_members':motion.SOURCE_MEMBERS,
      'group_keys':sorted(GROUP_KEYS),'groups':summary,
      'source_sequences':sum(len(g['sequences']) for g in groups),
      'source_frame_positions':sum(len(motion.frames_of(g)) for g in groups),
      'source_sentinel_positions':sentinels(groups),'distinct_original_bitmaps':len(wanted),
      'source_bitmap_statuses':dict(Counter(r['status'] for r in receipts.values())),
      'bounded_bitmaps':[n for n,r in receipts.items() if r['status']==motion.BOUNDED],
      'unrendered_bitmap_keys':unresolved,
      'unrendered_source_sequences':sum(len(g['sequences'])-r['fully_observable_sequences'] for g,r in zip(groups,summary)),
      'actual_pixel_receipts_sha256':motion.sha(json.dumps(receipts,sort_keys=True).encode()),
      'private_zip_bytes':target.stat().st_size,'private_zip_sha256':zip_sha,
      'boundaries':{k:False for k in ['official_character_or_variant_roster_verified','source_action_names_inferred',
       'source_duration_unit_verified','native_palette_verified','original_game_executed','native_sentinel_semantics_verified',
       'proprietary_images_in_git','all_historical_actors_restored']}}
    report['source_bitmap_reference_positions']=report['source_frame_positions']-len(report['source_sentinel_positions'])
    return report


def main():
    p=argparse.ArgumentParser()
    p.add_argument('source_zip',type=Path,nargs='?');p.add_argument('private_zip',type=Path,nargs='?')
    p.add_argument('--synthetic-fixture',type=Path);args=p.parse_args()
    if args.synthetic_fixture:
        if args.source_zip or args.private_zip:p.error('fixture and private-source export are separate modes')
        args.synthetic_fixture.write_text(synthetic_fixture());return
    if not args.source_zip or not args.private_zip:p.error('original source ZIP and new private ZIP are required')
    report=export(args.source_zip,args.private_zip);REPORT.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['groups','source_members','group_keys']},sort_keys=True))
if __name__=='__main__':main()
