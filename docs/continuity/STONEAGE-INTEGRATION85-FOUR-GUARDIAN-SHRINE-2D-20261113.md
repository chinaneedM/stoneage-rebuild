# INTEGRATION85｜四方守護者：十二原戰鬥 NPC、四原勾玉 NPC、兩石像及 22 幅已保存原二維候選（2026-11-13）

## 實際起點、目標與查重

本包在重新查詢 `chinaneedM/stoneage-rebuild` 遠端 `main=cb0626c866186b2906e33315bc860f2e993230bf`／tree `18dab1d064022f3da91e9096ac8bb75d32580b91`、同 SHA **26/26 Actions completed/success**、0 開放 PR 後啟動。完整讀取遠端 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`、README、DESIGN-DECISIONS、HISTORICAL-TIMELINE、SOURCE-REGISTRY、RESTORATION-ROADMAP-R2、模組工作次序和未修改的 `docs/CURRENT-STATE.md` 原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B）。之前的 `INTEGRATION84` JBA 商店已止點，**本包不再重複商店或原物品全集枚舉**。

本次要恢復的具體遊戲內容：在來源相同的社群 mixed25 NPC 原配置中，核出四方守護者的**戰鬥型與任務型兩套原 NPC**、四勾玉的原獲取字面和雙石像共同的原交換/候選物品腳本，再接到**另一個分開保管的台灣 1.0 零售客戶端**以前確實解碼的原 2D SPR/RD PNG。交付有來源與原字節 SHA 的公開靜態內容合同及私人離線圖像查閱；不是原版玩法、原服戰鬥或現代新遊戲引擎。此前 QUEST20 的五兄弟領寵/迷宮資料和 ITEM01/PET07 既有原圖不重算為新發現。

## 私人原件實讀與來源分界

直接從個人 Library 已保存原件重新真讀：

- `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B**，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，**2,205/2,205 成員 CRC**。
- `StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip` **5,868,386B**，SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`，**838/838 成員 CRC**。
- `StoneAge-PET07-original-sprite-private-catalog.html` **15,123,277B**，SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`，包含先前從**台灣1.0原 SPR/ADRN/REAL**真實提取的候選 PNG；4個圖號另與先前公開 PET07 原完整 SPR 段摘要對照。

20份實際涉及的社群 NPC 原 CREATE／模板／參數／事件檔均嚴格 CP950 解碼與回編完整原 SHA 並逐來源 CRC；CREATE 先在解碼後的完整字串定位原區塊，再回編核**原位元組區間/散列**，不以 UTF-8 字元索引當原 byte offset、不受 CP950 尾隨符號誤切影響。20份包括 `npc/300/sb_4sin.create`、`npc/300/sb_4sin.template`、12份對應 `sb_4sin*.arg`、`npc/giiru/event/nev1_1.create` 及5份真正 `nev1_1` 至 `nev1_5` 事件檔；相同事件被不同 CREATE 重用，不重複算獨立檔。

## 有來源的兩種守護者，絕不能因同 floor/圖號合併

### A. 十二 `NPCEnemy` 原 CREATE

原 `npc/300/sb_4sin.create` 長 **2,449B**／SHA256 `36f81d50f2811be6ef1a312552a1cef941f4bbc0f4f368426f8c8651a00eaff8`，包含樓層 **31603／31606／31609** 各四項，合計12個原 CREATE。四種原 `graphicname` 對照：水 **100379**、火 **100370**、風 **100328**、地 **100274**。同來源原 `sb_4sin.template` 長 588B、四個 `templatename` 都是 `functionset=NPCEnemy`；十二個 CREATE 都各自指向一份實存原 `.arg`，其中 `entype:2`、`dieact:1`、五個 `enemyno` 數字、原 `warpfl/warpx/warpy` 全逐檔 SHA 保留。3F/6F 首位敵人 ID 來源分別為1031–1034，9F 的首位為1048–1051；不把兩組數字抹平。來源的 `warpfl` 此處是**同 floor**，而非可自行擅補的「到下一層」。原 `time=60000`、`borncenter` 和 `movecenter` 都維持原值；沒有證明原版生成時間、移動路徑、戰鬥實際編隊、戰後傳送或可達性。

### B. 同層四 `changeevent` 任務 CREATE

另一原 `npc/giiru/event/nev1_1.create` 長 **1,194B**／SHA256 `bde421eff8f67ebba9b917398cd0c8d9cff44a842fab730f316d80f4ec161fa3`，在 `floorid=31609` 還有**四份任務 `changeevent` 守護者 CREATE**：風 `(79,79)`、火 `(79,22)`、地 `(20,22)`、水 `(20,78)`，每處同圖形數字卻與 A 類 NPCEnemy 的原 `borncenter` 各不相同，且其原檔指向不同的 `giiru/event/nev1_1` 至 `nev1_4`。四份完整原 CP950 事件各有兩個 `TYPE:MESSAGE` 來源段：原 `LV>0&ITEM=...` 的持有檢查及另一段 `GetItem` 分別為 **地2528／水2529／火2530／風2531**。這是**原文本的來源條件與指令**，不證明原生 interpreter 的分支優先序、玩家實際領取或與 A 類戰鬥 NPC 同時部署。

### C. 原31610雙石像共用一份事件檔

同一 `nev1_1.create` 在 `floorid=31610` 另有兩個 `changeevent` 靜態 CREATE，座標 `(24,24)`／`(25,24)`、圖號 **10939／5075**，共同指向唯一 `giiru/event/nev1_5`；**兩個圖號不是兩份獨立腳本**。其原 `EVENT` 字面條件包含四個 `ITEM=2528*1...2531*1`，`DelItem` 列出四個勾玉，`GetRandItem` 字面列出 **16個不同 ID**，原順序為 `51,52,71,148,171,241,271,375,11424,1125,684,11433,11443,11454,11463,11475`。不能從指令名稱擅推真正獎品隨機分佈、操作順序、物品領取成功、原式樣 UI 或歷史「必經」機制。

## 四勾玉＋16候選物品與真正已有原二維像素

四勾玉各一件，兩份社群原物品表 `itemset.txt` 和 `itemset0710.txt` 的完整94欄原行 SHA 逐字節相同，原圖別名依次**地24065、水24066、火24064、風24067**。石像16個字面獎勵候選也全部有兩份原94欄行 SHA 並逐行 CP950 重組驗過；總共 **20不同原 ID ×兩表＝40完整行 SHA**，其中 **6個 ID（11424、11433、11443、11454、11463、11475）兩表只在原 zero-based 欄30/31不同**，不能當作同一原數值或證明裝備效果。其餘14 ID兩表整行字節相同。

20 ID 的來源 `ImageNumber` 去重有**18個不同別名**，在台灣1.0先前真解碼的 ITEM01 保管包中全部有原 RD 候選 PNG，本輪逐個完整 SHA、RGBA bytes SHA及原尺寸**實讀核對18/18**。另從已保存 PET07 來源 HTML 的130圖形候選中，直接實取水100379／火100370／風100328／地100274四組原有序 SPR 的**4個真原 PNG 帧**，各 PNG SHA與相同來源已存原 SPR/RD 派生收據核對（風用動作2原方向0第一帧，避免將O65不同候選配色 PNG冒充PET07動作0同一PNG）。**4+18=22幅實際原像候選**，非本輪新解RD（**新RD=0**），不等於22個新美術或原版物種數；同號是跨載體參考，不證早期與混合後期同服。

已製作一份**私人靜態 HTML**和一張現代接圖預覽：四守護者／四勾玉原圖、12份戰鬥參數、四任務配置、雙石像、16獎勵候選的名稱/數字/原圖可在離線查閱；嚴格保留原PNG位元組，現代卡片版面不是遊戲原畫面，整頁無網路請求、無遊戲行為與新引擎。私人包 `StoneAge-INTEGRATION85-four-guardian-shrine-original-2D-private.zip` **137,532B／46成員／SHA256 `7edac69d609363cde14aaa9a2b8cfb7c1d633fb5f41a34d79399fdf8b497c60f`**，已存使用者私人 Library `/石器时代/` 並**獨立從 Library 再取回、整ZIP逐位元組同一／SHA同一、46/46 CRC及45個非manifest成員逐SHA同一**。完整原 NPC 文件、原94欄物品行、原PNG、HTML／私有圖卡**全部不入公開Git**。

## 驗收、精確止點與NEXT

[公開合法派生數值/SHA](../../research/recovered/STONEAGE-INTEGRATION85-FOUR-GUARDIAN-SHRINE-ORIGINAL-2D-R1.json)記錄每一原CREATE byte起止和原區塊SHA、12 arg+四模板、四任務及兩石像、四ITEM/16GetRandItem、兩表94欄行 SHA差異、台灣1.0原RD及候選PNG SHA，並明示跨版本否定證據。新增 **21項公共正反契約測試本地實際PASS**；GitHub Actions/PR/main不得提前聲稱成功，待各自確切新SHA後驗。公共CI不會讀原私有圖或執行原程序。

目前仍為 Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null。原 `docs/CURRENT-STATE.md` **2,709,173B**完整 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`不改寫。本源族已達有界靜態復原止點，**NEXT** 轉不同且不重複、有原件與原像素可核的寵物／物品／任務二維內容；只有取得對應原生 script interpreter、實際載入或原世界執行證據才重開戰鬥／勾玉／石像的真正可達性與狀態轉移，不能以測試數、圖號或回合模擬冒稱原版可玩。
