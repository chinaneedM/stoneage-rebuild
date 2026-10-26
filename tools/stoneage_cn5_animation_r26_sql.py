"""Independent SQLite join over permanent source tables, not the report builder."""
import csv
import gzip
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'research/recovered'


def source_rows(profile,name):
    with gzip.open(BASE/(profile+'-resource-metadata')/(name+'-R1.tsv.gz'),'rt',encoding='utf-8',newline='') as f:
        for row in csv.DictReader(f,delimiter='\t'):
            yield {k:(v if k.endswith('sha256') else int(v)) for k,v in row.items()}


def verify(doc):
    db=sqlite3.connect(':memory:')
    db.executescript('''
        CREATE TABLE cg(idx INTEGER PRIMARY KEY, spr INTEGER UNIQUE);
        CREATE TABLE tg(spr INTEGER PRIMARY KEY);
        CREATE TABLE a(g INTEGER,spr INTEGER,ai INTEGER,off INTEGER,dir INTEGER,act INTEGER,dur INTEGER,n INTEGER,ending INTEGER,PRIMARY KEY(spr,ai));
        CREATE TABLE f(g INTEGER,spr INTEGER,ai INTEGER,fi INTEGER,off INTEGER,bmp INTEGER,x INTEGER,y INTEGER,snd INTEGER,sentinel INTEGER,PRIMARY KEY(spr,ai,fi));
        CREATE TABLE b(bmp INTEGER PRIMARY KEY,off INTEGER,size INTEGER,x INTEGER,y INTEGER,w INTEGER,h INTEGER,sha TEXT);
        CREATE TABLE old(bmp INTEGER PRIMARY KEY,size INTEGER,sha TEXT);
    ''')
    db.executemany('INSERT INTO cg VALUES(?,?)',((r['index'],r['spr_no']) for r in source_rows('cn50','SPR-GROUP')))
    db.executemany('INSERT INTO tg VALUES(?)',((r['spr_no'],) for r in source_rows('tw10','SPR-GROUP')))
    selection=[x[0] for x in db.execute('SELECT cg.spr FROM cg LEFT JOIN tg ON cg.spr=tg.spr WHERE tg.spr IS NULL ORDER BY cg.idx LIMIT 3')]
    if selection!=[100700,100701,100702]:raise ValueError('independent source-order selection differs')
    db.executemany('INSERT INTO a VALUES(?,?,?,?,?,?,?,?,?)',
        ((r['group_index'],r['spr_no'],r['anim_index'],r['offset'],r['direction'],r['anim_no'],r['duration'],r['frame_count'],r['end_offset'])
         for r in source_rows('cn50','SPR-ANIMATION') if r['spr_no'] in selection))
    db.executemany('INSERT INTO f VALUES(?,?,?,?,?,?,?,?,?,?)',
        ((r['group_index'],r['spr_no'],r['anim_index'],r['frame_index'],r['offset'],r['bmp_no'],r['pos_x'],r['pos_y'],r['sound_no'],r['sentinel'])
         for r in source_rows('cn50','SPR-FRAME') if r['spr_no'] in selection))
    db.executemany('INSERT INTO b VALUES(?,?,?,?,?,?,?,?)',
        ((r['bitmapno'],r['adder'],r['size'],r['xoff'],r['yoff'],r['width'],r['height'],r['rd_block_sha256']) for r in source_rows('cn50','ADRN')))
    db.executemany('INSERT INTO old VALUES(?,?,?)',
        ((r['bitmapno'],r['size'],r['rd_block_sha256']) for r in source_rows('tw10','ADRN')))
    db.execute('CREATE INDEX old_content ON old(size,sha)')
    actual=list(db.execute('''SELECT f.g,f.spr,f.ai,f.fi,f.off,f.bmp,f.x,f.y,f.snd,f.sentinel,
        a.off,a.dir,a.act,a.dur,a.n,a.ending,b.off,b.size,b.x,b.y,b.w,b.h,b.sha
        FROM f JOIN a ON f.spr=a.spr AND f.ai=a.ai AND f.g=a.g JOIN b ON f.bmp=b.bmp
        WHERE f.sentinel=0 ORDER BY f.spr,f.ai,f.fi'''))
    bitmaps={r['source']['bitmapno']:r['source'] for r in doc['bitmaps']};expected=[]
    for group in doc['groups']:
        for animation in group['animations']:
            a=animation['source']
            for f in animation['frames']:
                if f['sentinel']:continue
                b=bitmaps[f['bmp_no']]
                expected.append(tuple([f[k] for k in ('group_index','spr_no','anim_index','frame_index','offset','bmp_no','pos_x','pos_y','sound_no','sentinel')]
                    +[a[k] for k in ('offset','direction','anim_no','duration','frame_count','end_offset')]
                    +[b[k] for k in ('adder','size','xoff','yoff','width','height','rd_block_sha256')]))
    if actual!=expected:raise ValueError('independent full frame/animation/RD multiset differs')
    rd_matches=db.execute('''SELECT COUNT(*) FROM (SELECT DISTINCT b.size,b.sha FROM f JOIN b ON f.bmp=b.bmp)
        AS c JOIN old ON old.size=c.size AND old.sha=c.sha''').fetchone()[0]
    members=list(db.execute('SELECT bmp,COUNT(DISTINCT spr) FROM f GROUP BY bmp ORDER BY bmp'))
    if (len(actual),len(members),rd_matches)!=(1464,936,0):raise ValueError('independent TW1 content coverage differs')
    common=db.execute('SELECT COUNT(*) FROM (SELECT bmp FROM f GROUP BY bmp HAVING COUNT(DISTINCT spr)=3)').fetchone()[0]
    cues=db.execute('SELECT COUNT(*) FROM f WHERE snd<>0').fetchone()[0]
    if (common,cues)!=(48,64):raise ValueError('independent shared/cue occurrence differs')
    old_count=db.execute('SELECT COUNT(*) FROM old').fetchone()[0]
    cn_count=db.execute('SELECT COUNT(*) FROM b').fetchone()[0]
    db.close()
    return {'status':'PASS','independent_join_rows':len(actual),'selected_bitmaps':len(members),
        'complete_cn5_bitmap_rows':cn_count,'complete_tw10_bitmap_rows':old_count,
        'exact_rd_matches_in_tw10':rd_matches,'common_three_group_bitmaps':common,
        'raw_nonzero_sound_word_occurrences':cues,
        'joined_row_sha256':hashlib.sha256(json.dumps(actual,separators=(',',':')).encode()).hexdigest()}


if __name__=='__main__':
    doc=json.loads(lzma.decompress((BASE/'STONEAGE-CN5-ANIMATION-MATERIAL-R26.json.xz').read_bytes()))
    result=verify(doc)
    recorded=json.loads((BASE/'STONEAGE-CN5-ANIMATION-MATERIAL-R26-INDEPENDENT.json').read_bytes())
    if result!=recorded:raise ValueError('permanent independent result drift')
    print(json.dumps(result,sort_keys=True))
