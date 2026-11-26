"""PET108: archival metadata for 2004 CN7.5 mirror routes and two magazine titles."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import urllib.parse
from tools import stoneage_pet_high_first_104_cn70_archive_index as idx
from tools import stoneage_pet_high_first_104_accept as replay
ROUTES=(
("official-test-and-retail","http://www.wayi.com.cn/zhuanqu/shiqi/xia.asp"),
("official-upgrade","http://www.wayi.com.cn/down/index.asp"),
("网易","http://game.163.com/stoneage/editor/040921_262136.html"),
("网游名人堂","http://www.popvip.com/file/show_file.asp?file_id=80"),
("网游海岸线","http://www.vcng.com/web/common/article.jsp?channelid=14&articleid=5527"),
("硅谷动力","http://games.enet.com.cn/download/D0420041022001.html"),
("火狐","http://www.skyhu.com/html/50291.htm"),
("21cn","http://download.21cn.com/list.php?id=48874"),
("游戏之王","http://www.gameking.com.cn/gk/download/04/10/22/15224273.htm"),
("中游网","http://download.cgame.cn/view.asp?letmesee=4953"),
("天使","http://down.sa20.com/down4/~softview|softid|899.html"),
("9991网","http://9991.com/down/down.asp?id=12"),
("天空游戏","http://down.tkgame.com/soft/673.htm"),
("wegame网","http://files.wegame.com/detail_9091.html"),
("智者网","http://down.zhie.net.cn/software.asp?id=211"),
("网游在线","http://www.play119.com/down/softview.aspx?ID=244"),
("喜满你网","http://www.xicn.net/download/games/item/2004-10-25/174244.html"),
("游戏总动员","http://www.3g168.com/download/show.asp?ID=1471"),
("游戏365","http://down.g365.net/soft/575.shtml"),
("52PK游戏网","http://down.52pk.net/soft/385.htm"),
("游戏娱乐网","http://dl.72g.com/list3.aspx?DownLoadID=425"),
)
MAG_QUERIES=('title:"游戏族" AND mediatype:software','title:"家用电脑与游戏" AND mediatype:software','title:"GameStar" AND year:2004 AND mediatype:software','title:"家用电脑与游戏" AND year:2004')
def jobs():
    out=[]
    for name,u in ROUTES:
        q=urllib.parse.urlencode(dict(url=u,output="json",**{"from":"2004","to":"2007"},limit=100,fl="timestamp,original,statuscode,mimetype,digest,length"))
        out.append(("WAYBACK_CDX",u,"https://web.archive.org/cdx/search/cdx?"+q))
    for q in MAG_QUERIES:
        qs=urllib.parse.urlencode([("q",q),("fl[]","identifier"),("fl[]","title"),("fl[]","date"),("rows",100),("page",1),("output","json")])
        out.append(("IA_CATALOGUE",q,"https://archive.org/advancedsearch.php?"+qs))
    return out
def normalized(u):
    p=urllib.parse.urlsplit(u)
    return (p.hostname,(urllib.parse.unquote(p.path)).lower(),sorted(urllib.parse.parse_qsl(p.query,keep_blank_values=True)))
def choices(rows):
    result=[]
    for x in rows:
        if x["kind"]!="WAYBACK_CDX" or x["result"]!="METADATA_PARSED":continue
        target=x["target_or_query"]
        candidates=[r for r in x["metadata"]["rows"] if r["statuscode"]=="200" and r["mimetype"].lower()=="text/html" and len(r["timestamp"])==14 and r["timestamp"].isdigit() and normalized(r["original"])==normalized(target)]
        if not candidates:continue
        # nearest dated capture to Nov 2, distinct for official December route
        date="20041208" if target==ROUTES[1][1] else "20041102"
        from datetime import datetime
        aim=datetime.strptime(date,"%Y%m%d")
        r=min(candidates,key=lambda v:(abs((datetime.strptime(v["timestamp"][:8],"%Y%m%d")-aim).days),v["timestamp"]))
        result.append(dict(kind="PAGE",target=target,timestamp=r["timestamp"],original=r["original"],cdx_mime=r["mimetype"],cdx_digest=r["digest"],cdx_length=r["length"],replay_url="https://web.archive.org/web/"+r["timestamp"]+"id_/"+r["original"]))
    return result
def selftest():
    assert len(ROUTES)==21 and len(set(u for _,u in ROUTES))==21 and len(jobs())==25
    assert normalized("http://www.wayi.com.cn:80/down/index.asp")==normalized(ROUTES[1][1])
    assert all(urllib.parse.urlsplit(j[2]).hostname in idx.HOSTS for j in jobs())
    print("PET108_SELFTEST_OK")
def main():
    p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true");p.add_argument("--output",type=Path);a=p.parse_args();selftest()
    if a.self_test:return
    assert a.output
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:rows=list(ex.map(idx.request,jobs()))
    select=choices(rows)
    assert len(select)<=21
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:pages=list(ex.map(replay.replay,select))
    report=dict(schema="stoneage.pet108.cn75.archive_routes.r1",base_head="ade02c57a1024dddf6e9a53aaa63a45d77b94f6a",previous_receipt_blob="a803a4c05529a233bb03f1d1dfef21e33289bdf7",route_count=len(ROUTES),query_count=len(rows),routes=[dict(name=n,url=u) for n,u in ROUTES],results=rows,page_replays=pages,original_payloads=0,official_closures=0,original_assets_published=False,scope="Only public archive indexes and one bounded historical HTML replay per exact route. No live historical server, original installer, paid source, peer or tracker requested; URLs are source candidates, not retrieved files.")
    a.output.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("PET108_REPORT_SHA256="+idx.sha(a.output.read_bytes()),flush=True)
    for row in rows:
        m=row.get("metadata",{})
        print("PET108_INDEX="+json.dumps(dict(target=row["target_or_query"],result=row["result"],count=m.get("row_count",m.get("num_found"))),ensure_ascii=False),flush=True)
    for row in pages:print("PET108_PAGE="+json.dumps(row,ensure_ascii=False,sort_keys=True),flush=True)
if __name__=="__main__":main()
