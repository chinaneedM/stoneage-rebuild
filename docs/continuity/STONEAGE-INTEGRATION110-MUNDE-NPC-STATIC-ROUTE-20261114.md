# INTEGRATION110｜夢德族據點的原NPC短對白、七層靜態路由與入口一格差異

日期：2026-11-14。**Stage A 原始遊戲歷史材料**，不是新遊戲設計，不是原商業客户端運行證據。本次源載體為後期**community preserved mixed25**，不歸屬台灣1.0或JSS1999正式同服。

## 續接與查重

起點遠端 `main=422a5d067b61997c92d534c0687eca4262a5dbba`、Git tree `879780e89bf45122256283a78629803688927e0b`；精確 HEAD 的26條 push Actions 全部 `completed/success`、沒有開放PR。原 `docs/CURRENT-STATE.md` 為2,709,173B，Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，**全歷史原樣保留**。本次實際重新讀取 Git 原協議、README、CURRENT 原Git blob索引和舊材料範圍；INTEGRATION109 已正式收據閉環，故不重做其309條 `kingwarp`。既有INTEGRATION38證書、O79寵物對話、INTEGRATION51百人道場、QUEST23波拉島等已驗項不得當新發現。本包專選尚無同名整合的原 `genout/11100npc.create`、`genout/11101d.create`。

## 原始源檔實物與可公佈的派生資料

私人 Library 保管的原 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 995,176B、完整 SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，本次 **2,205/2,205 ZIP CRC** 成功。真正重讀的兩CREATE：`genout/11100npc.create` 1,481B/SHA `bf0b094b588a60be6f87fc79536fc795f5f589e5dd50beb85a35ee5426ad2f85`；`genout/11101d.create` 1,737B/SHA `4a57c2ece8d7476ee10660d0713caab7d211dc64b7bb972c223335baef869a21`。二檔合 **22個原字節段**，逐段Byte-offset（半開）、SHA、NPC樓層、坐標及原功能保留於[公開數值收據](../../research/recovered/STONEAGE-INTEGRATION110-MUNDE-TRIBE-ORIGINAL-NPC-STATIC-ROUTE-R1.json)，可直接與舊[CHAR01全源段索引](../../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-FULL-SOURCE-ROWS-R1.json)按段比對；它們**不是新發現的22原文件**。

`11100npc` 有8個源配置：5 `npcgen_man`，1 `npcgen_dengon` 留言版，1 `npcgen_warpman`，1 `npcgen_signboard`。原短名含「夢德族的人民」「女盜賊」「盜賊」及「秘密的留言版」；其中6個源配置在樓層11107，另外2個在floor100。7份真原外參/短對白/標牌檔均已依原ZIP讀取，逐字節尺寸、CRC、完整SHA與舊CHAR01同源索引一致；5個短對話檔只提取來源身份，未在公開Git展示其完整商業原文。短對話有族長、盜賊團和昔日對手的文字線索，屬**來源文本語義**，不能據此補造NPC對話分支、戰勝記錄、具體Boss身份或事件觸發。

`11101d` 有14個 `npcgen_warp` 靜態配置：11101—11107七floor之間12條分成6個精確反向對、11101→floor100和11107→floor100另各一條在此單檔無精確反向配置。**這是文件內相互倒向的字面靜態數值關係，並不等於原玩家實走往返。** 源入口另一原 `wpm_100_443_127` 寫入：floor100 `(443,127)` 的字面 `WARP:11101,33,29`、`FREE:LV>0`。但11101的原靜態出口源格是 `(33,28)` → floor100 `(442,127)`，入口到達點和出口源格、出口到達點和入口來源格均各有一格偏差；**不可擅改為完全雙向對稱或認證原碰撞**。

## 已驗DAT尺寸的正反核查

僅復用既有[後期原世界來源覆蓋檔](../../research/recovered/STONEAGE-25-STABLE-WORLD-CONTENT-COVERAGE-R1.txt)的原DAT來源 metadata（Git blob `455fa7abef06ffefec6b7e46f87ac12c9ee83972`），七floor `11101`為70×70、`11102`—`11107`各50×50；七個原DAT源SHA逐項存收據。22原建立源位置中**20/20**在這七已驗的尺寸內，另2個源floor100不在所選覆蓋清單；14靜態目的地中**12/12**在已驗尺寸內，另2個目的floor100在同所選清單缺資格。**已資格坐標越界0；無資格不等於原世界不存在該DAT。** 這一單元沒有新讀原DAT三平面、原bitmap RD/SPR像素，故仍不可證碰撞/通行或原2D畫面。

## 驗收與證據止點

公開 test `test_stoneage_integration110_munde.py` 只讀派生JSON與既有CHAR01完整來源段索引、既有來源覆蓋表：逐22原窗SHA/位置反證、9源檔尺寸SHA/CRC、七地圖摘要、12精確反向/2源檔未成對、入口一格不對稱及版權/執行否定欄位；並以改一段SHA、改一端offset和改floor的三個非原值測例確實拒絕。新GitHub Actions在候選/PR及正式main的真實狀態必須分開後驗，不預寫成功或原生玩法恢復。

**已觀測：** 後期來源原短名、原配置、原短文本文件、七張舊原DAT metadata的有界數值關聯。**仍 OPEN：** 原商業世界可達性、原主角與NPC畫面/實際對話執行、動作配色、原來的發行版本與初代同源、任何運行時觸發。原文字/商業二維圖/原DAT/私人ZIP不入公有Git。

Stage A保持 **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，總體完成率 `null/UNKNOWN`。**NEXT** 切換獨立有真新原字節或可觀測2D像素的非重複寵物、任務、場景內容；若只有相同靜態傳送檔則止步。不延伸本族成通用路由助手或虛構NPC行為。`CURRENT-STATE.md` 原文件不修改，README以追加方式指向本日期收據。