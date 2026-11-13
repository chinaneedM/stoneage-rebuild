# INTEGRATION88｜原隊伍營地99 CREATE、三守門通行條件、44 Warp與真正原2D私人觀察（2026-11-13）

## 啟動、來源資格和新遊戲內容

從遠端 main `a1a0ac451d61fd23ee70b4cd3c5d0c3d3e763c95`／tree `e9e7ba46782002c071138aa0c4d28b8fd54afabd` 啟動，當時最新HEAD26/26 Actions實際成功、0開放PR；重新讀 README、協議、設計、時間線、來源登記、路線、模組順序及INTEGRATION87驗收。完整`CURRENT-STATE.md`按**2,709,173字節、blob`c89e0e33537990aa2132b47c40fef49a985a935c`**從原始Git blob取得，未變更舊歷史。

**恢復的原遊戲內容：** 保存版 `npc/genout/500npc_m.create` 是一組島上隊伍／營地 NPC、門衛、對話、商店與數字傳送配置；這次不重做已完成的36組GetPet，也不是已完成的波魯龍王5509–5511三原地圖。材料是**後期社群mixed25保存的原始NPC原檔**；另外採用已保存、不同來源的臺灣Waei/JSS零售1.0原SPR素材。兩個來源並未證明官方同服／初代1.82部署，也沒有原生遊戲運作證據。

## 來源實讀與計數守恆

原 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`：995176B、SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`、全2205成員ZIP CRC PASS。實際重新逐原CP950讀 `npc/genout/500npc_m.create` 14674B／SHA256 `587e264d484fa74f4c615b2c63e2b7cb522061bf60602b30ac6456c98752cb46`，對照既有CHAR01 Git原源派生索引，**99/99個原CREATE塊的原位元組span和SHA完整吻合**。其中55個有圖形編號、44個無圖Warp，分布11個原floor值；原函數有npcgen_man50、npcgen_warpman3、npcgen_shop1、npcgen_signboard1、npcgen_warp44。原`file:`直接目標46/46同ZIP存在，逐原件SHA成功，不推為46個新NPC或46項遊戲事件。

完整99筆原位元組界限／SHA、來源地圖與座標／功能／圖號、46個來源目標與SHA、44個直接傳送數值、跨來源原像SHA見[公開原來源限定索引](../../research/recovered/STONEAGE-INTEGRATION88-TEAM-CAMP-GATE-WARP-ORIGINAL-2D-R1.json)。**源重複座標保留**：floor5533的(34,47)來自第32/33塊；floor500的(226,328)來自第81/87塊。第55塊`npcgen_warp`原字面另有`N`，其餘原數字照錄，未規範化為已可走的遊戲連通路網。原註解提及生成材料`data/npc/poru/500npc_m.gen`，但本保存NPC子樹沒有該原GEN，不能捏造其原位元組。

## 三份原門衛門票條件（原文參數非實際放行）

從同原保存ZIP三份不同完整原參數字節，以原`npcgen_warpman|file:...`直接來源連接：
- 原floor500 (450,391)，原`WARP:5532,0,22`、`FREE:ITEM=18553`、`MONEY:-1`，來源檔`genout/wpm_500_450_391` SHA256 `6a07078ac3523de6053a64d8cb4e8df4f5e5bbbf4321e09d9155d07cf5030359`。
- 原floor500 (410,622)，原`WARP:5536,30,13`、`FREE:ITEM=18554`、`MONEY:-1`，來源檔`genout/wpm_500_410_622` SHA256 `c3bbd14de86ddcc3813760b88dd5001949bb054bbc2a9a543724b98fc51371b6`。
- 原floor500 (225,430)，原`WARP:5533,30,11`、`FREE:ITEM=18555`、`MONEY:-1`，來源檔`genout/wpm_500_225_430` SHA256 `a214c38b1a94c1eea0b3464e2c95982e8864f78bb2ebf3209afb9bdba2d1893b`。

另外44筆`npcgen_warp`的原配置來源有42筆floor500、2筆floor5530，部分目標數值/入口相同，**保留每次原出現**。這是靜態條件、方向及目標字面；不證明執行了傳送、消耗了物品、扣金、原服開門或曾在該圖角色可見。

## 來源限定的三張守門證與既存原物品圖像候選

再查同社群保存RAR中已存 ITEM01 原始兩份94欄物品主表的**公開逐ID完整源行SHA索引**（Git blob `dbb958e77aed796faf86570c7523d3f0dc5748fd`），三個原 `FREE:ITEM` 物品ID 18553／18554／18555皆存在**兩個候選主表**，且各ID兩原94欄完整行SHA相同、原欄30/31等無變更。其原原圖別名順序為 **24124／24126／24127**；原B表cost原值字串0、type原值16、level原值0，只表明存檔欄位，不推免費商業交易或官方有效設定。舊ITEM01已把三個別名列為 **臺灣1.0零售原RD已取得／原PNG可解候選**；這是跨來源相同圖號的圖像線索，不是本輪重新讀取三張像素、更不是該原初版有這三門票。原兩主表雖同保存RAR，**未證哪一份被真實伺服器使用**，也未在本輪重新取得私人itemset原文。原物品名／94欄商業正文仍留在私人材料，Git只發可驗SHA及原始數值。

## 真原二維像素、現代私有資料查閱與負例

重新實際讀私人原PET07頁`15,123,277B/SHA 58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`及私人RD報告`1,617,404B/SHA b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`；29筆mixed25圖形數字與**另一版TW1**保存SPR4組候選`100259/100379/100401/100432`相同，現有真正原RD派生PNG中取**57個不同圖塊**、57/57全PNG SHA及圖寬高逐一對原報告。臺灣1.0公開PET07原索引有這四組共**12條原動作/方向0序列、101個幀出現**；但圖號100401的原動作0方向0含bitmap82729原嚴格RLE解碼溢位，**該26幀位置在私人頁不能完整顯示**，只保留可見的動作2/1兩段。本私人頁可見合計11段、75幀位置、57幅不同真原PNG。10筆保存NPC原圖號100406不在PET07被抽取的130圖號子集中，不能宣稱TW1整個客戶端不存在此圖。

新私人離線HTML將99來源配置、三個門衛、原可見SPR/PNG源幀接成可按原floor與功能查的資料觀察頁，**沒有補造或新解碼任何原RD**，不是原商業客戶端截圖／原遊戲。已在本輪Chromium真運行切四個測試角色、篩floor500得到46筆、篩純Warp得42筆／全Warp44筆；原PNG成功顯示，0 JS異常、0外部HTTP請求。私人ZIP `StoneAge-INTEGRATION88-500-team-camps-original-2D-private.zip` 349552B、SHA256 `e2c6b6f051835d668a3d1646a021300819bd5dc1043076d3d14b5f9e551c9fa7`、2 ZIP成員CRC合格，個人Library `/石器时代/` 已成功上傳及獨立重取同整SHA。

**版權資料界限：** 原PNG、原商業NPC原文、私人HTML、完整原ZIP都只在私有交付，公開Git只放數值、原SHA、來源範圍、負證與自動測試；公開Actions不能冒作私人原位圖重解碼或原服執行。Stage A7 PARTIAL+2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；overall_percent=null。止點為本群99筆與57真像已驗；下輪選另一不同有真正原文件的原2D內容，不造原版玩法、不做新引擎。
