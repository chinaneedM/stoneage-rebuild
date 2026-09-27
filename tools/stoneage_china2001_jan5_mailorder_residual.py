#!/usr/bin/env python3
"""Strictly retry failed China.com Jan-2001 article replays from R1.

R1 falsely promoted ordinary neighboring news pages because their global footer
contained "游戏《石器时代》专题". This residual:
- retries only the three failed archived page captures;
- classifies a target only if article text contains mail-order/trial-giveaway
  semantics, not merely the global StoneAge footer.
"""
from __future__ import annotations
import hashlib, html, re, time, urllib.request

UA="stoneage-rebuild-archaeology/1.0"
TARGETS=(
 ("jan6-80570","20010211062656","http://game.china.com:80/zh_cn/news/news1/444/20010106/80570.html"),
 ("jan4-78775-alt","20010309011418","http://game.china.com:80/zh_cn/news/news1/444/20010104/78775.html"),
 ("jan4-78782","20010309093437","http://game.china.com:80/zh_cn/news/news1/444/20010104/78782.html"),
)
STRICT=("邮购","郵購","试玩版","試玩版","赠送活动","贈送活動","注册用户名单","註冊用戶名單")
CONTEXT=("石器时代","石器時代")

def clean(v,n=5000):
 return " ".join(str(v or "").split()).replace("|","%7C")[:n]

def fetch(url,timeout=45,max_bytes=2*1024*1024):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*;q=0.2","Accept-Encoding":"identity"})
 with urllib.request.urlopen(req,timeout=timeout) as r:
  b=r.read(max_bytes+1)
  if len(b)>max_bytes: raise ValueError("response-too-large")
  return int(getattr(r,"status",r.getcode())),r.geturl(),b

def decode(b):
 for enc in ("gb18030","gbk","gb2312","big5","utf-8","latin1"):
  try:return enc,b.decode(enc)
  except UnicodeDecodeError:pass
 return "latin1",b.decode("latin1","replace")

def plain(text):
 text=re.sub(r"(?is)<script\b.*?</script>"," ",text)
 text=re.sub(r"(?is)<style\b.*?</style>"," ",text)
 return re.sub(r"\s+"," ",html.unescape(re.sub(r"(?s)<[^>]+>"," ",text))).strip()

def replay(ts,orig): return f"https://web.archive.org/web/{ts}id_/{orig}"

def main():
 print("StoneAge China.com Jan-2001 article strict residual — R2")
 print("PARENT|STONEAGE-CHINA2001-JAN5-MAILORDER-ROUTE-R1|failed-replays-only + false-positive correction")
 print("STRICT_RULE|StoneAge footer alone is noise; target requires mailorder/trial-giveaway semantic token")
 errors=[];done=0;matches=0
 for label,ts,orig in TARGETS:
  ok=False
  for attempt in range(1,4):
   try:
    st,final,b=fetch(replay(ts,orig))
    enc,text=decode(b); p=plain(text)
    strict=[t for t in STRICT if t.lower() in p.lower()]
    ctx=[t for t in CONTEXT if t.lower() in p.lower()]
    print(f"PAGE|label={label}|attempt={attempt}|status={st}|bytes={len(b)}|sha256={hashlib.sha256(b).hexdigest()}|encoding={enc}|strict={clean(','.join(strict))}|context={clean(','.join(ctx))}|final={clean(final)}")
    for tok in strict:
     i=p.lower().find(tok.lower())
     print(f"SNIPPET|label={label}|token={clean(tok)}|text={clean(p[max(0,i-350):i+1000],1900)}")
    done+=1;matches+=int(bool(strict));ok=True;break
   except Exception as e:
    print(f"RETRY_ERROR|label={label}|attempt={attempt}|kind={type(e).__name__}|message={clean(e)}")
    if attempt<3:time.sleep(attempt*2)
    else:errors.append((label,type(e).__name__,str(e)))
  if ok:time.sleep(1)
 print(f"COUNT|targets|{len(TARGETS)}")
 print(f"COUNT|completed|{done}")
 print(f"COUNT|strict_matches|{matches}")
 print(f"COUNT|errors|{len(errors)}")
 for label,kind,msg in errors: print(f"ERROR|scope={label}|kind={kind}|message={clean(msg)}")
 if matches:
  print("RESOLUTION|STRICT_TARGET_SEMANTICS_FOUND|inspect exact page body/hrefs before historical promotion")
 elif done==len(TARGETS) and not errors:
  print("RESOLUTION|JAN4_6_NEIGHBOR_RESIDUAL_BOUNDED|no mailorder/trial semantics; R1 StoneAge-footer matches are false positives")
 else:
  print("RESOLUTION|JAN4_6_NEIGHBOR_RESIDUAL_PARTIAL|retain unresolved captures only")
 print("CORRECTION|R1 ARTICLE_RECOVERED resolution is not accepted unless strict target semantics are present.")
if __name__=="__main__":main()
