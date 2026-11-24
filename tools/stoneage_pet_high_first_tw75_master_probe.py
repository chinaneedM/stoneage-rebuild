"""PET15: public, bounded source acquisition for claimed 7.5 master and known comparison.
No executable launched; original archives/text remain runner-private.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import urllib.request
import urllib.error
from urllib.parse import urlsplit

from tools.stoneage_pet_high_first_tw85_pixels import ROOT
from tools.stoneage_enemybase_probe import INDEX

TARGET=ROOT/'research/pets/PET-HIGH-FIRST-15-CLAIMED-TW75-MASTER-PROBE-R1.json'
QUICK='5k9kp225b51zh7f'
MEDIA='https://www.mediafire.com'
GAVIN='https://raw.githubusercontent.com/gavinlinasd/StoneAge/1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56/gmsv/data/enemybase1.txt'
GAVIN_SHA='7ffb17b161c9d66fcbbaa4e8bcf48d1a9a56223b35770074ae9c3401d270f5d7'
GAVIN_BLOB='a19a508975e3a982fada323861b35b2edab79349'
LIMIT=16*1024*1024
NAMES={'烏力':'乌力','布魯頓':'布鲁顿','魯貝萊歐':'鲁贝莱欧','布林特':'布林特','黑烏力王':'黑乌力王',
       '弗奇肯':'弗奇肯','卡沃寇恩':'卡沃寇恩','卡沃裴特':'卡沃裴特','裘尼':'裘尼','艾克夫':'艾克夫'}
GROUPS={'魯貝萊歐':[101645],'布林特':[101685,101900],'黑烏力王':[101781],'弗奇肯':[101795],
        '卡沃寇恩':[101798],'裘尼':[101811],'艾克夫':[101857]}


def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def allowed(url):
    u=urlsplit(url); host=u.hostname or ''
    return u.scheme=='https' and (host=='mediafire.com' or host.endswith('.mediafire.com')
                                 or host=='raw.githubusercontent.com')
class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl):
            raise ValueError('redirect outside source host allowlist')
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def get(url):
    if not allowed(url):
        raise ValueError('source URL outside allowlist')
    opener=urllib.request.build_opener(Redirect())
    try:
        with opener.open(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; research source verification)'}),timeout=30) as resp:
            raw=resp.read(LIMIT+1)
            if len(raw)>LIMIT: raise ValueError('source exceeds bounded download')
            return raw,{'status':resp.status,'final_host':urlsplit(resp.url).hostname,
                        'bytes':len(raw),'sha256':sha(raw),'content_type':resp.headers.get('Content-Type')}
    except urllib.error.HTTPError as e:
        return None,{'status':e.code,'error':'HTTP_ERROR'}
    except (OSError,ValueError) as e:
        return None,{'status':None,'error':type(e).__name__,'detail':str(e)[:160]}


def selected(raw):
    # Exact names in source-specific encoding; preserve name/graphic differences.
    variants={}
    for enc in ('gb18030','cp950','utf-8'):
        try: text=raw.decode(enc)
        except UnicodeError: continue
        lines=text.splitlines()
        hit=sum(line.split(',',1)[0] in set(NAMES)|set(NAMES.values()) for line in lines)
        variants[enc]=(hit,lines)
    if not variants:
        raise ValueError('no strict supported text encoding')
    enc,(hits,lines)=max(variants.items(),key=lambda x:x[1][0])
    rows=[]; counts=collections.Counter()
    for n,line in enumerate(lines,1):
        if not line.strip() or line.lstrip().startswith('#'):continue
        f=line.split(','); counts[len(f)]+=1
        names=[k for k,v in NAMES.items() if f[0] in (k,v)]
        if not names or len(f)<=INDEX['SIZE']:continue
        row={'line':n,'source_name':f[0],'query_name':names[0],'columns':len(f),
             'template_id':int(f[INDEX['TEMPNO']]),'initnum':int(f[INDEX['INITNUM']]),
             'lvup_literal':f[INDEX['LVUPPOINT']],
             'base_vital_str_tgh_dex':[int(f[INDEX[k]]) for k in ('BASEVITAL','BASESTR','BASETGH','BASEDEX')],
             'elements_earth_water_fire_wind':[int(f[INDEX[k]]) for k in ('EARTHAT','WATERAT','FIREAT','WINDAT')],
             'skill_slots':[int(f[INDEX['PETSKILL'+str(k)]]) if f[INDEX['PETSKILL'+str(k)]].strip() else None for k in range(1,8)],
             'slot':int(f[INDEX['SLOT']]),'graphic':int(f[INDEX['IMGNUMBER']]),
             'pet_flag':int(f[INDEX['PETFLG']])}
        row['tw85_residual_graphics']=GROUPS.get(names[0],[])
        row['same_residual_graphic']=row['graphic'] in row['tw85_residual_graphics']
        rows.append(row)
    return {'bytes':len(raw),'sha256':sha(raw),'git_blob':blob(raw),'encoding':enc,'name_hits':hits,
            'column_counts':dict(counts),'selected_rows':rows,'source_row_count':sum(counts.values())}


def extract(raw,temp):
    # Only a text file, or a listed, bounded single enemybase1.txt member of a static archive.
    if raw[:2]!=b'PK' and raw[:6]!=b'7z\xbc\xaf\x27\x1c' and raw[:7]!=b'Rar!\x1a\x07\x00' and not raw.startswith(b'Rar!\x1a\x07\x01'):
        if b',4.50,' in raw:
            return raw,{'format':'PLAIN_TEXT'}
        return None,{'format':'UNRECOGNIZED_OR_NONDATA'}
    p=temp/'claimed-master.archive';p.write_bytes(raw)
    listing=subprocess.run(['7z','l','-slt',str(p)],capture_output=True,timeout=25)
    if listing.returncode!=0:return None,{'format':'ARCHIVE_LIST_FAILED'}
    entries=[]
    for block in listing.stdout.decode('utf-8','replace').split('\n\n'):
        d=dict(line.split(' = ',1) for line in block.splitlines() if ' = ' in line)
        if d.get('Path','').replace('\\','/').split('/')[-1].lower()=='enemybase1.txt' and d.get('Size','').isdigit():
            entries.append((d['Path'],int(d['Size'])))
    if len(entries)!=1 or not 0<entries[0][1]<=LIMIT:
        return None,{'format':'ARCHIVE','matching_members':len(entries)}
    name,size=entries[0]
    run=subprocess.run(['7z','x','-so',str(p),'--',name],capture_output=True,timeout=30)
    if run.returncode!=0 or len(run.stdout)!=size:
        return None,{'format':'MEMBER_EXTRACTION_FAILED','declared_size':size}
    return run.stdout,{'format':'ARCHIVE','member':name,'declared_size':size}


def run(temp):
    comparison, comp_http=get(GAVIN)
    if comparison is None: raise ValueError('pinned public comparison source unavailable')
    if (sha(comparison),blob(comparison))!=(GAVIN_SHA,GAVIN_BLOB):
        raise ValueError('comparison raw source identity changed')
    comp=selected(comparison)
    # Two prior web-indexed quotations; compare only numeric prefixes, not whole-table provenance.
    witnesses=[]
    for name,tid,init,base in [('烏力',1,10,[20,12,15,25]),('布魯頓',95,25,[25,35,14,24])]:
        rows=[x for x in comp['selected_rows'] if x['query_name']==name and x['template_id']==tid]
        witnesses.append({'name':name,'template_id':tid,'numeric_prefix_matches':
                          len(rows)==1 and rows[0]['initnum']==init and rows[0]['lvup_literal']=='4.50' and rows[0]['base_vital_str_tgh_dex']==base})
    probes=[]
    raw,info=get(MEDIA+'/api/1.5/file/get_info.php?quick_key='+QUICK+'&response_format=json')
    entry={'kind':'PUBLIC_FILE_INFO_API',**info}; links=[]
    if raw:
        try:
            response=json.loads(raw)['response']
            fi=response.get('file_info') or {}
            entry['result']=response.get('result')
            entry['error_code']=response.get('error')
            entry['filename']=fi.get('filename')
            entry['file_size']=fi.get('size')
            if isinstance(fi.get('links'),dict):
                links.extend(v for v in fi['links'].values() if isinstance(v,str) and allowed(v))
        except (ValueError,KeyError,TypeError): entry['result']='NOT_JSON_FILE_INFO'
    probes.append(entry)
    candidate=None
    for url in list(dict.fromkeys([MEDIA+'/file/'+QUICK,MEDIA+'/?'+QUICK]+links))[:4]:
        raw,info=get(url);probes.append({'kind':'PUBLIC_LANDING_OR_LINK',**info})
        if not raw: continue
        if raw.startswith((b'PK',b'7z',b'Rar!')) or b',4.50,' in raw[:4096]:
            candidate=raw;break
        page=raw.decode('utf-8','replace')
        # Only explicit download links on MediaFire, no credentials, no executable.
        match=re.search(r'<a\b[^>]*\bid=["\']downloadButton["\'][^>]*>',page,re.I)
        if match:
            href=re.search(r'\bhref=["\']([^"\']+)["\']',match.group(0),re.I)
            if href:
                direct=html.unescape(href.group(1))
                if allowed(direct):
                    data,info=get(direct);probes.append({'kind':'PUBLIC_EXPLICIT_DOWNLOAD',**info})
                    if data: candidate=data;break
    result={'status':'NOT_ACQUIRED','archive_sha256':None,'selected_master':None}
    if candidate:
        parsed,fmt=extract(candidate,temp)
        result.update(archive_sha256=sha(candidate),archive_bytes=len(candidate),extraction=fmt)
        if parsed:
            try: result.update(status='ACQUIRED_UNAUTHENTICATED_CANDIDATE',selected_master=selected(parsed))
            except ValueError: result['status']='ACQUIRED_NO_QUALIFIED_TABLE'
    return {'scope':'CLAIMED_TW75_UNAUTHENTICATED_PUBLIC_SOURCE_PROBE','quick_key':QUICK,
            'claim_url':'https://forum.gamer.com.tw/C.php?bsn=1571&snA=65960',
            'comparison_url':GAVIN,'comparison':comp,'comparison_http':comp_http,
            'quoted_prefix_witnesses':witnesses,'mediafire_probes':probes,'claimed_master':result,
            'same_deployment_official_master_verified':False,'raw_archives_published':False,
            'same_name_is_not_identity':True}


def verify(r):
    if r['comparison']['sha256']!=GAVIN_SHA or r['comparison']['git_blob']!=GAVIN_BLOB:
        raise ValueError('comparison source identity')
    if r['same_deployment_official_master_verified'] or r['raw_archives_published'] or not r['same_name_is_not_identity']:
        raise ValueError('unsupported promotion')
    if len(r['quoted_prefix_witnesses'])!=2:
        raise ValueError('quote comparison count')
    return {'source_rows':r['comparison']['source_row_count'],'selected_rows':len(r['comparison']['selected_rows']),
            'quote_prefix_matches':sum(x['numeric_prefix_matches'] for x in r['quoted_prefix_witnesses']),
            'residual_same_graphic_rows':sum(x['same_residual_graphic'] for x in r['comparison']['selected_rows']),
            'claimed_master_status':r['claimed_master']['status'],'http_probes':r['mediafire_probes']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--temp',type=Path);a=p.parse_args()
    r=run(a.temp) if a.temp else json.loads(TARGET.read_bytes())
    print(json.dumps(verify(r),ensure_ascii=False,sort_keys=True))
    if a.temp:TARGET.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
