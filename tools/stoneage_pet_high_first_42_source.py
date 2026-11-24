"""Reaccess only missing original instance fields and exact indexed reward commands."""
import argparse, json, re, tempfile
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
from tools import stoneage_preserved_item_shop_r44 as sparse
from tools.stoneage_pet_high_first_42_verify import verify
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    index=verify();inv={r['path']:r for r in json.loads(r40.R18.read_bytes())['all_server_occurrences']}
    selected=['enemy.txt','enemybase.txt',*['npc/'+s['path'] for s in index['scripts']]]
    sparse.EXPECTED={'setup.cf':r40.PINS['setup.cf'],**{'data/'+k:(inv[k]['size'],inv[k]['sha256']) for k in selected}}
    receipt={}
    with tempfile.TemporaryDirectory(prefix='pet42-private-') as work:
        members=sparse.acquire(Path(work),receipt,'unar')
        setup=r40.kv(members['setup.cf'],b'=')
        for k,v in ((b'enemyfile',b'enemy.txt'),(b'enemybasefile',b'enemybase.txt')):
            assert r40.one(setup,k)[1] in (v,b'data/'+v)
        es=r40.rows(members['data/enemy.txt'],34,3);bs=r40.rows(members['data/enemybase.txt'],56,6)
        ei=r40.idx(es,3);bi=r40.idx(bs,6)
        rows=[]
        for x in index['rows']:
            aid=x['award_instance_id'];((el,e),)=ei[aid];tid=int(e[4]);((bl,b),)=bi[tid]
            assert tid==x['template_id'] and int(b[36])==x['graphic'] and int(b[37])==x['template_pet_flag']==1
            assert [v.decode('ascii') for v in b[9:13]]==x['base_fields'] and [v.decode('ascii') for v in b[15:19]]==x['elements']
            rows.append(dict(award_instance_id=aid,template_id=tid,graphic=int(b[36]),instance_line=el,template_line=bl,instance_name=e[0].decode('cp950'),template_name=b[0].decode('cp950'),instance_level=r40.level(e),instance_pet_flag=int(e[13]),template_pet_flag=int(b[37])))
        scripts=[]
        for s in index['scripts']:
            raw=members['data/npc/'+s['path']];assert r40.sha(raw)==s['script_sha256']
            lines=raw.splitlines(); commands=[]
            for i,line in enumerate(lines,1):
                m=re.fullmatch(rb'\s*GetPet\s*:\s*(.*?)\s*',line,re.I)
                if not m:continue
                token=m[1];nums=[int(n) for n in re.findall(rb'\d+',token)]
                assert re.fullmatch(rb'[0-9, \t]+',token),repr(token)
                # Use pinned TYPE line, not an assumed adjacent EventNo.
                block=max((b for b in s['blocks'] if b['type_line']<i),key=lambda b:b['type_line'])
                assert re.fullmatch(rb'\s*TYPE\s*:\s*'+block['type'].encode()+rb'\s*',lines[block['type_line']-1],re.I)
                end=next(j for j in range(i,len(lines)) if lines[j].decode('cp950').strip().lower()=='eventend')
                d=r40.kv(b'\n'.join(lines[block['type_line']-1:end+1]))
                fields={}
                for key in (b'event',b'endsetflg',b'delpet',b'getitem',b'delitem',b'getstone',b'delstone'):
                    if key in d:
                        values=[]
                        for _,v in d[key]:
                            try: values.append(v.decode('ascii','strict'))
                            except UnicodeDecodeError: values.append({'non_ascii_value_sha256':r40.sha(v)})
                        fields[key.decode()]=values
                commands.append(dict(line=i,block_type=block['type'],block_ordinal=block['ordinal'],raw_numeric_tokens=token.decode('ascii'),numeric_literals=nums,fields=fields,source_block_end=end+1))
            assert [v['line'] for v in commands]==s['source_lines']
            assert [n for v in commands for n in v['numeric_literals']]==s['ordered_numeric_literals']
            scripts.append(dict(path=s['path'],commands=commands))
    out={'schema':'stoneage.pet42.original_member_replay.r1','scope':'SAVED_MIXED25_NOT_OFFICIAL_DEPLOYMENT','member_receipt':receipt,'original_member_count':len(members),'rows':rows,'scripts':scripts,'original_payload_published':False,'runtime_executed':False,'actual_awards_verified':False}
    raw=json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n';args.output.write_text(raw)
    print('PET42_META',json.dumps({k:v for k,v in out.items() if k not in ('rows','scripts','member_receipt')},ensure_ascii=False,separators=(',',':')))
    print('PET42_CUSTODY',json.dumps({k:v for k,v in receipt.items() if k!='range_receipts'},ensure_ascii=False,separators=(',',':')))
    print('PET42_RANGES',json.dumps(receipt['range_receipts'],ensure_ascii=False,separators=(',',':')))
    for k in ('rows','scripts'):
        for row in out[k]:print('PET42_ROW',k,json.dumps(row,ensure_ascii=False,separators=(',',':')))
    print('PET42_REPORT_SHA256',r40.sha(raw.encode()))
if __name__=='__main__':main()
