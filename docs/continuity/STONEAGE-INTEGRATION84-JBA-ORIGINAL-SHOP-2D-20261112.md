# INTEGRATION84｜JBA 20712 九筆原NPC、44筆獨立ItemList、16筆嵌字串候選與54幅既存原RD像素（2026-11-12）

## 啟動、原來源與查重

本輪按遠端 `main=fb5ce1db69fe2b288135dc81e729756f97d9e9c5`／tree `8dbb756894df4a50fc59b0ee904f84f896044fb6` 啟動，重新讀取 protocol、README、DESIGN／TIMELINE／SOURCE、roadmap／module order，並從 Git blob 真正讀出完整未改寫的 `docs/CURRENT-STATE.md`（2,709,173 原位元組／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`）。本輪開始時 main 該 HEAD 26/26 push Actions completed/success、0 開放 PR。前一包 INTEGRATION83 的 floor1009/4009 十素材商店已閉合；此包**不重做**它、舊 INTEGRATION38 的 JBA/SBC 證書條件、也不重做原 ITEM01 的224 `ItemList` 目錄。本包專門恢復保存資料中另一組 `floorid=20712` 原NPC/服務配置至有來源合格原二维物品圖的關係，與先前既有目錄做差異審核。

**實際私人原始資料重新回讀：** `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`，995176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`／2205成員CRC全部成功；`StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip`，5868386B／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`／838成員CRC全部成功。原 `npc/genout/shop_event2.create` 2883B／SHA256 `ac3eb1246f29158d6851f78d2a01320aaa9272d34457aee8a4b694982168775c`。CP950 嚴格解碼往返與每一原CREATE位元組區間／SHA相同；沒有改原文。

## 同一社群 mixed25 保存載體：九 CREATE → 六原參數

原 `shop_event2.create` 共16個源 CREATE，其中**索引2至10**為 `floorid=20712` 九條。其原 `borncorner`、圖號、功能及名稱原字面分別是：武器店 `(45,32)`／16033／`npcgen_shop`、防具店 `(45,36)`／16017／`npcgen_shop`、道具屋 `(25,4)`／16069／`npcgen_shop`、高級飼育員 `(22,4)`／16202 和 `(20,4)`／16203／`npcgen_petskillshop`、克雷爾 `(18,4)`／100291 與昆伊 `(17,4)`／100297／`npcgen_mugon`、護士 `(45,15)`／16058／`npcgen_winhealer`、藥劑師 `(45,19)`／16059／`npcgen_shop`。九項是原配置建立記錄，**不是九名已在原生世界見到的NPC**；沒有原服建立、行走、對話或交易執行。

六份直接 `file:` 指向的原參數全在 NPC 保存 ZIP 中：四份 `ss_20712_*` 商店參數和兩份 `psks_20712_*` 寵技參數，全部真讀且整份 SHA／長度已放公開派生JSON。其可證直接原字面：

- `ss_20712_45_32` 武器店：獨立原行 `ItemList:` 明列16個ID，`LimitItemType:OFFENCE`，`buy_rate:1.0`、`sell_rate:0.15`。
- `ss_20712_45_36` 防具店：獨立原行 `ItemList:` 明列15個ID，`LimitItemType:DEFENCE`，`buy_rate:1.0`、`sell_rate:0.15`。
- `ss_20712_45_19` 藥劑師：獨立原行 `ItemList:` 明列13個ID，`LimitItemNo:1500-1550,2568`，`buy_rate:2.0`、`sell_rate:0.2`。
- **`ss_20712_25_4` 道具屋關鍵負證：** 原檔 `itemfull_msg:` 內容末尾直接緊接 `ItemList:1212,...,1468`，**不存在任何行首 `ItemList:` 鍵**。這16個數字是真實原文字串、但只是 `itemfull_msg` 內嵌候選，不可擅自補換行或算作原 `npcgen_shop` 已證的售貨清單。原 `LimitItemType:ACCESSORY` 確實存在，單獨保留，不可用它反推 16 件已上架。
- `psks_20712_22_4`／`psks_20712_20_4` 分別獨立 `pet_skill:` 列出12／9個原技能號，兩者原 `skill_rate:1.0`。字面服務參數不等於原引擎成功學技能或計價結果。

真正獨立 `ItemList` 只有 **3份／44個原ID出現**；嵌在另一字段中的 **1份／16個文本候選** 明確區分，合併只為查原物品來源，去重後共60不同原物品ID。60 個在已保存兩套94欄 `itemset.txt`/`itemset0710.txt` 原行索引可追逐來源SHA，非新增60件裝備或首次發現60個物品種類。每原ID逐源94欄原行SHA與原 `ImageNumber` 已分來源保存；公開只含原數值／名稱／位置／完整SHA，不公開原94欄正文。

## 跨來源原二維像素及私人可見輸出

以60原ID的來源 `ImageNumber` 對照**另一載體**台灣1.0零售先前已保管真正解碼的原ADRN/REAL/RD PNG，共有**54個不同來源合格原RD alias**，覆蓋60／60個ID。這54幅原圖本輪逐PNG位元組SHA從私人 ITEM01 包**實際重新核對**，並不代表本輪新增解碼54幅；**新RD解碼0、新原美術0**。部分物品共用原圖別名，不能把54當54件物品或54張新畫。所有同號關係只作跨來源的私人可見候選，不證台灣1.0與社群2.5原伺服器同部署，也不證初代官方JBA店面、原UI、實際選圖。

私人離線索引 HTML 已把44個**原獨立行**與16個**內嵌文本候選**分欄逐ID展示，并提供九個源NPC原座標／功能，旁列54幅已驗台灣1.0真原像候選 PNG。私人 `StoneAge-INTEGRATION84-JBA-20712-original-items-private.zip` **112511B／57成員**／SHA256 `b6ec3b9122cc9d037f68988d0b9e9875745973ad94b3ac76faa20a23349c5f4f` 已保存個人 Library `/石器时代/`；全原圖只在私人資料庫，**未上傳公開Git**。HTML屬現代離線查閱頁，非原客戶端視窗；未宣稱本輪瀏覽器互動驗證。

## 驗收邊界、接續

[公開來源限定 JSON](../../research/recovered/STONEAGE-INTEGRATION84-JBA-ITEM-SOURCE-R1.json) 逐原CREATE區間、九原功能/數字、六原參數完整SHA、三項獨立清單、16內嵌負證、21寵技數值及60物品雙表行SHA／54原RD+PNG SHA分層記錄。[靜態正反測試](../../tests/test_stoneage_integration84_jba_source.py) 只在公開派生元數據上驗源鏈一致、絕不假冒於GitHub Actions重讀私人原檔／圖。專項CI與正式PR/main結果按實際運行另記，不先推定。

保留 Stage A **7 PARTIAL＋2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null。大 CURRENT 原 blob 不改，保留過去失敗。**NEXT：** 本JBA原9 NPC／6參數／44真正ItemList／16嵌字候選／21寵技／54已保存TW1像已到來源有界止點；轉真正另一個未重複原二維寵物／任務／物品材料。只在得到原native parser或同部署執行時才重審「嵌在 `itemfull_msg` 裡的 `ItemList`」是否會被引擎視為貨品，不為修格式臆造購買成功。
