"""One public source-chain check for the registered Korean client token.

No login, reply, credit purchase, executable execution, site crawl or guessed
download is performed. A qualified public link is evidence of a lead, not bytes.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

TOKEN='NetmarbleStoneAge120'
URL='https://lab.welovesa.com/viewthread.php?tid=2117'
MAX_HTML_BYTES=2*1024*1024
HOSTS={'lab.welovesa.com','www.lab.welovesa.com'}
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
GATES=['您需要登录后才能查看','您需要登入後才能查看','您无权进行当前操作','您無權進行當前操作',
       '本帖隐藏的内容需要回复','本帖隱藏的內容需要回復','您需要回复才可以','您需要回復才可以',
       '下载附件需要','下載附件需要','阅读权限不足','閱讀權限不足','购买主题','購買主題']


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def qualified_thread(url):
    u=urlsplit(url)
    return u.scheme in ('http','https') and u.hostname in HOSTS and u.path=='/viewthread.php' and parse_qs(u.query).get('tid')==['2117']


class SourceRedirects(HTTPRedirectHandler):
    def redirect_request(self,request,fp,code,msg,headers,newurl):
        destination=urljoin(request.full_url,newurl)
        # Same source only; a move to a login page is recorded, never submitted.
        need(urlsplit(destination).hostname in HOSTS,'source redirect left registered public host')
        return super().redirect_request(request,fp,code,msg,headers,destination)


class Thread(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.stack=[];self.title=[];self.visible=[];self.post=[];self.links=[];self.current=None

    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);classes=attrs.get('class','').split();identifier=attrs.get('id','')
        inherited=self.stack[-1] if self.stack else {'hidden':False,'post':False}
        hidden=inherited['hidden'] or tag in ('script','style') or 'hidden' in attrs or bool(re.search(r'display\s*:\s*none',attrs.get('style',''),re.I))
        post=inherited['post'] or identifier.startswith('postmessage') or 't_msgfont' in classes
        state={'tag':tag,'hidden':hidden,'post':post}
        if tag not in VOID:self.stack.append(state)
        if tag=='a' and post and not hidden:
            self.current={'href':attrs.get('href',''),'text':[]}

    def handle_endtag(self,tag):
        if tag=='a' and self.current is not None:
            self.links.append({'href':self.current['href'],'text':' '.join(self.current['text']).strip()[:160]});self.current=None
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag:del self.stack[i:];break

    def handle_data(self,data):
        if not self.stack or self.stack[-1]['hidden']:return
        text=' '.join(data.split())
        if not text:return
        if any(x['tag']=='title' for x in self.stack):self.title.append(text)
        self.visible.append(text)
        if self.stack[-1]['post']:self.post.append(text)
        if self.current is not None:self.current['text'].append(text)


def decode(raw):
    if raw.startswith(b'\xef\xbb\xbf'):return raw.decode('utf-8-sig'),'UTF8_BOM_STRICT'
    declared=re.search(br'charset\s*=\s*["\']?([a-zA-Z0-9_-]+)',raw[:8192],re.I)
    codec=declared[1].decode('ascii').lower() if declared else None
    if codec in ('gbk','gb2312','gb18030'):return raw.decode('gb18030'),'GB18030_STRICT'
    if codec in ('big5','big5-hkscs'):return raw.decode('big5'),'BIG5_STRICT'
    if codec in ('utf-8','utf8'):return raw.decode('utf-8'),'UTF8_STRICT'
    try:return raw.decode('utf-8'),'UTF8_STRICT_UNDECLARED'
    except UnicodeDecodeError:return raw.decode('gb18030'),'GB18030_STRICT_UNDECLARED'


def inspect(raw,final_url,status,content_type):
    evidence={'http_status':status,'final_url':final_url,'content_type':content_type,
              'response_bytes':len(raw),'response_sha256':sha(raw),'source_html_published':False}
    need(len(raw)<=MAX_HTML_BYTES,'source response exceeds finite page limit')
    if status!=200:return {**evidence,'state':'SOURCE_HTTP_UNAVAILABLE','public_package_links':[]}
    if not qualified_thread(final_url):return {**evidence,'state':'SOURCE_REDIRECTED_OR_LOGIN_WALL','public_package_links':[]}
    text,encoding=decode(raw);parser=Thread();parser.feed(text);parser.close()
    title=' '.join(parser.title);post=' '.join(parser.post);visible=' '.join(parser.visible)
    gates=[marker for marker in GATES if marker in post or (not post and marker in visible)]
    base={**evidence,'encoding':encoding,'title':title[:160],
          'target_token_in_title':TOKEN.lower() in title.lower(),'target_token_in_post':TOKEN.lower() in post.lower(),
          'access_gate_markers':gates,'public_package_links':[]}
    if gates:return {**base,'state':'PUBLIC_SOURCE_ACCESS_GATED_STOP'}
    if TOKEN.lower() not in title.lower() or not post:
        return {**base,'state':'SOURCE_TOPIC_OR_POST_UNQUALIFIED_STOP'}
    links=[]
    for entry in parser.links:
        target=urljoin(final_url,entry['href']);u=urlsplit(target)
        if u.scheme not in ('http','https') or u.username or u.password:continue
        if TOKEN.lower() not in (target+' '+entry['text']).lower():continue
        direct=bool(re.search(r'\.(exe|msi|zip|rar|7z)(?:$|[/?#])',u.path,re.I))
        host=u.hostname or ''
        public_provider=(host=='mediafire.com' or host.endswith('.mediafire.com')) and u.path.startswith('/file/')
        if direct or public_provider:links.append({'url':target,'anchor_text':entry['text'],'kind':'DIRECT_FILE' if direct else 'EXPLICIT_PUBLIC_FILE_PROVIDER_LEAD'})
    unique={x['url']:x for x in links};base['public_package_links']=list(unique.values())
    if len(unique)==1:return {**base,'state':'ONE_PUBLIC_PACKAGE_LINK_OBSERVED_NOT_YET_DOWNLOADED'}
    return {**base,'state':'NO_UNAMBIGUOUS_PUBLIC_PACKAGE_LINK_STOP'}


def fetch(url):
    with build_opener(SourceRedirects()).open(Request(url,headers={'User-Agent':'Mozilla/5.0 StoneAgeHistoricalEvidence'}),timeout=45) as response:
        return response.read(MAX_HTML_BYTES+1),response.url,response.status,response.headers.get('Content-Type')


def run(fetcher=fetch):
    try:
        raw,final,status,content_type=fetcher(URL)
        result=inspect(raw,final,status,content_type)
    except (HTTPError,URLError,TimeoutError,OSError,ValueError,UnicodeError) as error:
        result={'state':'SOURCE_UNAVAILABLE_OR_UNQUALIFIED_THIS_BOUNDED_ATTEMPT',
            'error_type':type(error).__name__,'error':str(error)[:500],
            'http_status':error.code if isinstance(error,HTTPError) else None,
            'public_package_links':[],'source_html_published':False}
    return {'schema':'stoneage.kr_netmarble120_r27.actual_public_source.v1','date':'2026-10-26',
        'task':'KR-NETMARBLE120-CLIENT-SOURCE-27','requested_url':URL,'target_token':TOKEN,
        'public_source_attempts':1,'observation':result,
        'package':{'downloaded':False,'bytes':None,'sha256':None,'declared_version':None,
                   'extracted_client_files':0,'official_clean_authenticated':False},
        'boundaries':{'login_reply_credit_or_purchase_performed':False,'unrelated_source_crawl_performed':False,
            'original_program_executed':False,'original_asset_bytes_published':0,
            'korean_174_identity_proven':False,'token_120_interpreted_as_version':False,
            'historical_package_or_site_absence_proven':False}}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    result=run();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print('R27_PUBLIC_SOURCE_STATE='+result['observation']['state'])
    print('R27_PUBLIC_PACKAGE_LINKS='+str(len(result['observation']['public_package_links'])))
    print('R27_PACKAGE_DOWNLOADED=0; ORIGINAL_EXECUTION=0')


if __name__=='__main__':main()
