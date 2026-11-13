# INTEGRATION103｜四村長毛象貨運原貨物 ID、雙服務參數、歷史 2D 候選（2026-11-14）

## 啟動與查重後的實質復原

本輪以已驗收 PR #388 的新遠端 main `747396b15f374f0c1fee10301e2cc121359709c3`、tree `92cd773cc83474837926bf046985b21e3f9b9296` 重啟，閱讀協議與完整原 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B）及最新來源、roadmap 與模組優先序。原 CURRENT 原封不動。本題與以前 **QUEST06/INTEGRATION48** 的 `sa60/newbie/newbie2.create`／四份 `worksell_*.conf`（新手貨運任務提示）、**INTEGRATION91** 的 `chatroom/bus.create` 原巴士/路線（客運）分開；本輪是尚未單獨復原的 **`npc/genout/unsoya_1.create` 貨運服务來源**，不重複宣稱原任務/車輛首次發現。

私人已保管的後期社群 **mixed25 NPC ZIP** `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` 995,176B／完整 SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，實際再讀、2,205/2,205 CRC 合格；`npc/genout/unsoya_1.create` **4,397 原字節** SHA256 `2fb4ab28ab89452ebe89e8fcc72c2d942c6d6460b24efb8bdb2278317caf7c5e`，26/26 個原 CREATE 原字節窗逐 SHA 完全等於原 CHAR01 Git blob `a088b61a3212f7049e7793f587123ffb29bebad7`，且 CP950 往返成立。源直接引到的**12 個不同參數原文件全部實際重讀**、完整 SHA 與 CHAR01 索引逐項一致，12/12 CP950 往返；4 `EXPRESSMAN`、4 `LIMITSHOP`、4 `NEWWARPMAN`，原 handler 完整正文不公開。原 CREATE 中另有10條 `npcgen_mugon` 長毛象數值配置、8條向導/夥計、4個 `npcgen_shop`、4個 `npcgen_limitshop`；**26是創建配置而非26個不同人物/動物。**

## 原貨物的可重放 12 對數字與來源標籤

原四服務位置各自有 `EXPRESSMAN.ItemList` 與 `LIMITSHOP.LimitItemNo`，分別位於四組 XXX11/XXX14。另以過去 ITEM01 兩份原 itemset 全行認證後保管的私人目錄再讀 ID2402–2413，對照 Git 公開 `research/recovered/item-module-01/STONEAGE-ITEM01-ORIGINAL-ITEM-ID-DERIVED-INDEX-02-R1.json` 的 **12條原 94欄整行 SHA**，12/12 與私人目錄完全一致，**兩 itemset 源行全部逐字節 SHA 相同**。本輪**沒有再次實讀原 itemset 3.39MB/3.67MB 全文件字節**，不能冒稱新的主表解包；這是原來源已驗目錄與原 NPC 參數的新增跨模組連接。

| 源短地名（只來自原 itemset 說明欄） | 出貨參數原樓層 | 收貨限額參數原樓層 | 出貨原 `ItemList` 數字 | 收貨原 `LimitItemNo` 數字 |
|---|---:|---:|---|---|
| 薩姆吉爾 | 1011 | 1014 | 2405／2408／2411 | 2402／2403／2404 |
| 瑪麗娜絲 | 2011 | 2014 | 2402／2409／2412 | 2405／2406／2407 |
| 加加 | 3011 | 3014 | 2404／2407／2410 | 2411／2412／2413 |
| 卡魯它那 | 4011 | 4014 | 2403／2406／2413 | 2408／2409／2410 |

每個 ID 只出現在**一個**出貨 `ItemList` 與**一個不同村**的收貨 `LimitItemNo`；同源物品行說明的兩個短地名完全吻合這兩端。四地共 **12 個唯一的有向貨物候選，四地相互各有三個、無自環**，是**源字節 / 原貨物說明靜態證據**，不能宣稱遊戲實際有12條可以營運的航線、貨運成功、交易結算或扣除保證金。物品表原價欄只是原行數值，不能拿它等同原服運費/報酬。十二件原道具圖號數值全部是 **16071**，非十二幅獨立圖；名稱、價格、真實原商業原行不公開。

## 原樓層、早期原圖與「已見」/「未見」邊界

源 26 條 CREATE 坐標分布在原 **1011/1014/2011/2014/3011/3014/4011/4014** 共8個樓層數值；依此前已驗 MAP04 原 DAT 目錄，8/8 均有來源文件完整 SHA、30×30 頭部與創建坐標核驗，26/26 座標落在已驗頭部邊界內。1011/1014 **同 SHA / 同來源內容**，實際只有**7份不同原 DAT 字節身份**。本輪 DAT 原字節重新解包0B，尚未觀察原 native 地圖與碰撞、NPC創建及道具互動。

從已驗私人 **ITEM01** 原圖觀察包重新讀出台灣零售1.0 對應物品圖號 **16071** 的單張歷史 RD 候選彩色 PNG（48×50，3,824B；完整 PNG SHA256 `602c03644de8acbe126d25ea08c60d3179e149ee17228d71c8d335d6e8b641df`），與原既有 RD/SHA 保管收據相同；又從已保存 **INTEGRATION91** 包重新回讀圖號100355的已驗源第一幀候選 PNG（物理圖118955，SHA256 `3aafe8871c60ae0e13589bf21b72508716bc6d8059bf4f3a36932ec56cfbf1a1`）。本輪兩圖實物經來源 ZIP 全 SHA、PNG SHA 重新驗證並私有檢視，**新增原 RD 解碼0**，不假稱新圖、新動作、客貨兩來源同官方服、原版 Palet 與畫面；二者獨立於後期 mixed25 NPC 原文件。私人離線 HTML 僅顯示兩幅舊來源原圖候選與12原貨物源對應，沒有交易、導航、移動或完整世界模擬。

此外，四份 `NEWWARPMAN` 原腳本各有**7個按原字面編號的 `TALKEVENT`**（本輪讀出14以外的完整段），均有一個 `AddItem` 數值2622／2623／2624／2625；這些源文件和 QUEST06 `worksell` 不是同一原文件，哪怕數字相交也不能推斷彼此同時部署、執行次序或實際獎勵。原始腳本/圖案不入公開 Git。

## 可交付與止點

**私人保管驗收：** `/石器时代/StoneAge-INTEGRATION103-four-village-express-cargo-source-original-2D-private.zip`，ZIP **28,396B**、SHA256 `22bc5b2926753926a40530380742baaed3bdd081a0dfada8f8981c477350a441`，含13份後期原小腳本、2幅舊已驗台灣零售原2D候選PNG、1份只讀HTML和1份完整SHA保管清單，**17/17 CRC**與16個內部成員SHA合格，個人 Library 上傳後**獨立重新下載整字節/全SHA一致**，不流入公有Git。

公開 [來源限定完整逐 SHA 數值 JSON](../../research/recovered/STONEAGE-INTEGRATION103-FOUR-VILLAGE-EXPRESS-CARGO-ORIGINAL-2D-R1.json) 保留 26 CREATE 的原 byte-span / handler SHA、四村12有向候選與原12物品行 SHA、8樓層的 DAT 原 SHA/幾何、獨立TW1舊候選圖片 SHA、全部來源負證。10項公有正負契約本地通過；遠端正式 Actions 與合併必須逐精確 SHA 後驗。私人原13檔/兩幅真正原圖片候選與單HTML打包進個人 Library，版權源不公開。

**SOURCE_BOUNDED_PARTIAL**，不是運行原服/已證貨運機制，更非可玩的單機新遊戲。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent `null`。**NEXT**在此可重放新增關係成立後停止同源貨運補 helper，選不同的、尚未實際整合的原遊戲人物/任務/地圖2D原件；僅取得新原生觸發/同源資料時重開此機制。
