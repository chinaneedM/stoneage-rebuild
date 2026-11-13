# INTEGRATION87｜36條GetPet→台灣1.0原SPR候選全量數值鏈主線與Actions終驗（2026-11-13）

## 合併與樹內容守恆

源開始 main `40e857168d5a8650b6f6f803dba0aad63f90933c`／tree `f47fcb0a92e99e6cbbe73a0fe94785a3861610ee`。該 HEAD 本輪開始已驗26/26 Actions成功、0開放PR。原巨型 `CURRENT-STATE.md` **2,709,173B／Git blob c89e0e33537990aa2132b47c40fef49a985a935c** 真由遠端 blob 全文讀出；本次無修改、不覆蓋、不抹歷史。五份規範啟動原文、roadmap、模組次序已核，實際作業清單獨立見 [INTEGRATION87來源範圍](STONEAGE-INTEGRATION87-36-GETPET-TW10-2D-CENSUS-20261113.md)。

[PR #363](https://github.com/chinaneedM/stoneage-rebuild/pull/363) 候選初稿 `b84ebcae`；修正後候選 `a5780b7b`，固定內容tree `c0f5481eab88bb3ae245e3862cbc180cddd10ee1`；正式 squash main 內容提交 `aebb5405fbedff10a5705ff32bf2f658af728f0f`／**同tree**。報告／測試／工作流／來源文檔各路徑 Git blob 精確保存在 [永久機器收據](../../research/recovered/STONEAGE-INTEGRATION87-PUBLICATION-ACCEPTANCE-R1.json)。

## GitHub Actions 實際後驗，保留兩條失敗

第一次候選 `b84ebcae` 的 push run `43362856070`、PR run `43362886913` 都實際 failure；6項中5項通過，測試把「原腳本不等於原NPC執行」的正面限制句誤要求是 `false`。**這兩次失敗不追認為成功、不刪歷史**。修正僅調整測試斷言的正反極性，來源JSON、證據及36條數字不變。

修正後同候選 `a5780b7b`：
- **專項 push run 43362998905** completed/success，6/6 tests OK。
- **專項 PR run 43363002385** completed/success，6/6 tests OK。
- 其他原有 **O11 PR run 43363002372、O12 PR run 43363002437** 亦各 completed/success，合計候選本次SHA **4/4**；不能把其算成四次INTEGRATION87專項。
- 正式 main 內容 `aebb5405fbedff10a5705ff32bf2f658af728f0f` 的唯一有條件被觸發 **run 43363096290/job 131680981107** completed/success，實際原日誌 `Ran 6 tests / OK`。此HEAD本次共1項run，不捏造此前26個workflow皆再次運行。

## 實物資格、增量與持續OPEN

已有私人來源 PET10原 CP950 4,100,822B 整 SHA `640506ad…`、PET07原像派生1,617,404B `b5ad2e58…`、私人源原圖HTML15,123,277B `58e8ee4f…` 實際在本工作環境獨立核整 SHA；36條按原欄位 numeric enemy instance→template→graphic 值全數一一吻合。**本輪沒有重獲完整原RAR，也沒有新原RD解碼，任何商品原圖、原音像、原腳本正文均不進公開Git**。公開CI只重核已存派生原數值／位元序列SHA和負證，不能冒充私有原碼的重新源執行。

44條源腳本 `GetPet` 字面出現，36個不同源實例，36個原數值模板圖號，在**不同保存來源**的台灣1.0原SPR中均有單獨數字候選；早已有PET07原始2D來源，不代表本次新發現36種寵物、原服發獎或官方同部署。最重要反例：`GetPet1481` → `graphic100401` 的動作0/方向0原RD圖`82729`嚴格解碼越界，未以猜測補圖。舊INTEGRATION62/66/67專項已知20原實例候選留標識，統一索引增量不得重報為20個新獎勵。

**Stage A=7 PARTIAL+2 OPEN；Stage B/wiki=GATED；R79=PAUSED_NON_BLOCKING；overall_percent=null**。本驗收收據自身新HEAD的Actions必須以重新讀取為準，不預支成功。**最高NEXT** 退出本輪36數字聯接，選另一尚未重複且有真實新可查來源的原2D寵物／物品／任務內容批次；只有新同構建原主表、原source實物或原native執行才能重開此批不確定性，不能改為新單機遊戲開發。
