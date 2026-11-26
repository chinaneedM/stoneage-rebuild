# PET114｜大陆胜思8.5 2011-06-22 ZOL分发记录（候选）
2026-11-26。fresh main 5ab3d7a9afba0156aa18d4eb6d041585237b1104/tree dd7a70fa6e32e9a1d430ae11b9657177177d2eb3，PR715已合并，精确候选c2312d259c2d73ce4a7e4f44cf753e57e850b909 5/5 Actions success，最终收据run45818127020/job139903032147 success，日志PET113_FINAL_RECEIPT_OK bec4bf24c737ac0e2510a010ac50e5c65a83f015。主线精确新HEAD检查初次未见run，不能称通过；开放PR0。历史CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c/2709173B未变。CN7.5集中分发取证结束、非阻塞，仅新独立原件线索重开。
依据已验PET113最终续接记录：ZOL 2011-06-22更新/1.15GB魔域大冒险客户端，页面 /ol/13450/download.html 与 softId=357206 及实际分发入口 /down.php?site=11&softid=357206&subcatid=62（先前现站HTTP403）。2010首测1.19G/MD5与2012 V1.200.012 1.34GB/MD5不是此记录的哈希，不合并。只查三确切入口HTTP/HTTPS六种历史索引，2010–2015有界，每入口最多2个去重摘要成功/重定向捕获，总计最多6次。重定向禁止自动跟随，只读存档响应头中原Location/档案包装Location，区分其证据等级；若HTML仅提取文件候选、记录ID、版本关键词/日期/大小标识，限制256KiB，不自动下载商业载体或运行脚本、程序。无源报告前不填实际结果。
NEXT：核PET114实跑及工件；如得具名新历史原文件地址，定向索引/有限完整性预检；否则仅重开真正独立的8.5分发记录（如当期官方历史页面而非重复现站已失败入口），仍无原件则转可验证同期具名宠物补证。PET唯一，3015位置/67严格取得缺件，Stage A7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，overall UNKNOWN。

## PET114A 修复
首次run45818600109/job139904680773真实failure：norm返回含list的tuple，作为set/dict键不可哈希，self-test即中止，未进行档案查询。改为嵌套tuple，并新增非空CDX样本、跨协议去重和查询参数重排测试。保留失败记录，不降低验收门槛。待新精确提交实际运行。
