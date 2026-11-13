# INTEGRATION89｜恐龍牧場洞窟、等級／紅藍手環傳送、肉品收購與已有真正原二維候選（2026-11-13）

## Fresh source, no duplicate of prior covered family

重新從遠端 main `324c303afa6209fb4da8e665720b7697a6897798` / tree `fcbf782adf1270ce9b52536eed306c2c65b67a0c` 啟動，重新核實本HEAD **26/26 GitHub Actions completed/success**、0 PR、完整原 `CURRENT-STATE.md` **2,709,173B** blob `c89e0e33537990aa2132b47c40fef49a985a935c` 真讀而不改。讀協議、README/INTEGRATION88永久驗收、設計、時序、來源登記、路線與模組優先。INTEGRATION88 三隊營地99配置已結束；此輪不重複之前QUEST17/INTEGRATION55已整理的**三種牧場寵物條件/領寵**，而是真實補上同保存來源的洞窟管家三門、洞窟現場35 CREATE、商店肉品來源及可見二維候選。圖/源來自兩個不同保存版本，絕不晉升為1999/JSS原作或TW1早期官方同服。

## Original private source and three literal cave access conditions

原 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B**，完整SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 實重新讀取、2,205/2,205 ZIP CRC成功；原真正 `npc/genout/bait_01.create` **5,743B／SHA256 `d98e0863def90f5c99240308312c8475aba05ceb329e7efae93f42ca7e49d570`**，原35 CREATE逐原bytes窗口SHA全部吻合既有CHAR01 Git原始派生。來源原floor共 **200、201、20901、20902、20903** 五數字（不是已證同構建本原版通路），原函數分布20個`npcgen_man`、7個`npcgen_signboard`、3個`npcgen_warpman`、3個`npcgen_limitshop`、1個`npcgen_shop`、1個`npcgen_dengon`。16份直接 `file:` 原目標全在同ZIP實存在、實讀CP950原字節SHA一一合原來源索引。35 CREATE不等於35隻不同寵物或35位已真正出現的官方NPC。

三個原守門 `npcgen_warpman` 引用三份不同原保管文本（各完整源SHA/原CREATE byte span在[公開來源索引](../../research/recovered/STONEAGE-INTEGRATION89-DINO-CAVE-GATES-SHOPS-ORIGINAL-2D-R1.json)）：
- 原floor200 `(337,653)`：字面 `FREE:LV>4`、`WARP:20901,0,8`、`MONEY:-1`，來源 `genout/wpm_200_337_653`，不是驗證原生通行；
- 原floor20901 `(21,13)`：字面 `FREE:ITEM=2595`（原保存對話為**紅手環**）、`WARP:20902,53,51`、`MONEY:-1`；
- 原floor20901 `(16,17)`：字面 `FREE:ITEM=2596`（原保存對話為**藍手環**）、`WARP:20903,5,5`、`MONEY:-1`。

兩件手環在**同一 mixed25 保存RAR的兩套94欄原物品主表**皆可由ITEM01完整原行SHA找到，兩主表各自同ID原行 SHA 一致；原商品圖號數字分別 **22114／22118**。不推哪一份原服啟用，也不能把TW1客戶端不同來源同數字視為原服已跑通。在最深層的實際可達、傳送、道具扣除、隊伍進出／等級門檻執行上，本輪仍沒有原程式證據。

## Four original cave shops and distinct meat-purchase rates

同ZIP原已證 `genout/ss_20901_8_19`：floor20901 (8,19) 原字面 `ItemList:12856`、`LimitItemNo:12856`、`special_rate:0.6`、`sell_rate:0.6`。原物品ID12856在兩份同保存的94欄原物品行SHA相同，原圖號數值 **24045**，舊ITEM01列為TW1另一原件可解RD候選。原私人對話是洞窟用**胡椒**提示，不代表實際捕捉成功或加成確切數值。

另外三間原`npcgen_limitshop` 肉品收購參數：
- floor20901 (44,22) 源`genout/lbis_20901_44_22`：`LimitItemNo:1234-1249`、`sell_rate:0.8`、`special_rate:1.0`；
- floor20902 (11,4) 源`genout/lbis_20902_11_4`：同 `LimitItemNo`，`sell_rate:0.7`；
- floor20903 (18,19) 源`genout/lbis_20903_18_19`：同 `LimitItemNo`，`sell_rate:0.6`。

上述僅**原配置中的文字數值**；`1234-1249` 不擅自計為實際已收購16種肉、`sell_rate` 不當實際結算價格或官方固定率。全商業原對話仍在私有原文件，公有只存源字節SHA與必要原數字／負證。

## Two-source genuine 2D candidate, independently discovered palette difference

真實原另一來源臺灣 Waei/JSS **零售1.0** 已保存PET07原SPR/ADRN/REAL資料：私人畫廊HTML **15,123,277B** SHA256`58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`，原RD獨立來源報告 **1,617,404B** SHA256`b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`。35源原CREATE中 **18條圖形數字**落在PET07真正原SPR的10組 `100250/100251/100252/100271/100275/100276/100278/100335/100368/100393`；現有公開SPR段SHA、方向0動作0/2/1各 **30段 / 250原有序幀位置 / 168個不同原bitmap**，10圖號均各存真正原SPR SHA。這是跨版本候選數值，不是官方原遊戲同一部署的18個動畫NPC已實現。

本輪從私人原图库可實拿 **532張既有PNG**，共93原方向／動作序列、852源幀出現，所有532張嵌入PNG均實計各自完整SHA、逐PNG實際讀尺寸。但**重點反例**：與較新的PET07原RD逐PNG來源表對照，168個當前表抽樣的源bitmap中：
- **116張**私人老畫廊PNG SHA與較新原RD同bitmap的調色板1候選PNG SHA**逐字一致**（7個圖形組）；
- **52張**老畫廊與新原RD候選**PNG SHA不一致**，全屬三個人物圖形組`100250/100251/100252`，是老庫調色板/圖像候選差異，**不得虛稱已通過新來源像素同一**；
- 另外 **364張**私人畫廊PNG不在較新來源報告本次選取的位圖核驗範圍，不能推它們有錯、或假充本次原RD重新驗證。

因此真正「本輪與兩來源原RD候選SHA完全吻合的可見老畫廊PNG」嚴格只報**116**，另52/364分別 OPEN/NOT_IN_CURRENT_SOURCE_RECEIPT。沒有新的RD區塊解碼、沒有發現新的官方原美術。

私人資料查看包 `StoneAge-INTEGRATION89-DINO-RANCH-CAVE-original-2D-private.zip` **1,482,192B**，原完整 SHA256 `a43da4967959afbf593bf3e9319421d13b752c1082fd4d103ab94ace8d4e9090`，2 ZIP成員CRC成功；已存私人個人Library `/石器时代/` 並獨立重新取回完整SHA一致。私有HTML完整含35來源NPC原姓名、16份原參數文字與老图库可手動觀察的532PNG候選，不公開任何商業原文本/圖像。已用Node `--check`實際驗內嵌JavaScript**語法成功**；本工作環境Playwright預設Chromium缺下載binary，另一系統Chromium試跑逾時，**沒有成功瀏覽器實際UI驗收**，不可冒稱0 JS或0網絡請求實際瀏覽器通過。相同圖號不代表原客戶端當時就是這個角色/配色。

**狀態不變：** Stage A 7 PARTIAL+2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；overall_percent=null。下一NEXT必須轉另一真正不同且已有資料的歷史原2D內容族，除非取得新同構建地圖DAT／原始客戶端／原程序才重開傳送/商店執行級別證據。
