# INTEGRATION113 — 寶物袋兩原配置與72條真實來源候選／正式主線 Actions 驗收（2026-11-15）

本收據僅證明此前**內容PR #409**實際完成的來源候選與正式內容main；不將本收據自己的候選PR／合併main的未來Actions預先記為success。

[原始私人資料及內容衝突邊界](STONEAGE-INTEGRATION113-TREASUREBAG-SOURCE-VARIANTS-20261115.md)／[原七文件SHA、12原CREATE逐byte窗口及NPC/任務/寵物候選](../../research/recovered/STONEAGE-INTEGRATION113-TREASUREBAG-VARIANTS-ORIGINAL-SOURCE-R1.json)／[72條逐run身份的永久機器驗收收據](../../research/recovered/STONEAGE-INTEGRATION113-PUBLICATION-ACCEPTANCE-R1.json)。

- [內容PR #409](https://github.com/chinaneedM/stoneage-rebuild/pull/409)確認squash合併。候選 `bdb49147b04dcb0901da6e57bc396d1f6cde0609` 與內容正式main `8c864e94a708d96dff817a82814cbd4d9c6dcae2` **Git tree相同 `88abad5cf499bb84fef00028bf4086fbf6ddd711`**；起點main `7cd3601bfe0fefd2861bfbc964b1e23b8a85812e`。
- 精確候選HEAD：**26 push＋19 pull_request＝45/45 completed/success**；內容正式main：**27/27 push completed/success**；合計**72個不同真實GitHub run ID**，逐一ID、workflow、事件、精確head SHA、status、conclusion、時間及URL見機器收據。72不是新物件或72個測試用例。
- 新專項候選PR [run 43673502418](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43673502418)／job `132688493865` 已完成success；正式內容main [run 43673574641](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43673574641)／job `132688714558` 已完成success。工作步驟「Verify original two treasurebag source schemes and pixel candidate boundaries」均實際success；這是對GitHub公開源衍生收據的復核，**不代表CI取得商業原NPC ZIP、原RD，亦不代表原遊戲啟動**。
- 私人mixed25原ZIP **995176B／2205 CRC**整包重讀，七源文件與舊CHAR01全原SHA吻合；`100/sb_mimi.create` 十二個原配置窗口逐字節SHA同。與既有QUEST19十個 `changeevent` 袋對照後精確**一個source坐標碰撞：floor122(162,12)**。另有原CREATE `sb_hag` 函數的跨目錄模板資格，`sb_mimi.template` 名稱並非同函數鍵；不得擅自修復或宣布原生模板選擇。
- 十次重複敵人ID1117與原模板3／SPR100252只形成後期保存資料數值關係；既存SCENE28**台灣1.0原SPR段**及實際RD像素可提供另一歷史載體的限定原圖候選，但不推成同官服部署或原人設。SCENE28私人既存觀察ZIP 347996B／3CRC整SHA回讀成功，**本輪並未重提完整372MB零售客戶端，也沒有新原RD/DAT讀取或原生行為執行**。原商業腳本/PNG/ZIP全留私人。
- `docs/CURRENT-STATE.md` **2709173B／原生Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`**不動；README僅末尾追加，來源段落與歷史訂正全保留。

Stage A **7 PARTIAL＋2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，`overall_percent=null`。

**後驗門檻**：這份收據自己的新候選及合併後main Actions，必須另外按精確HEAD真核；不能直接繼承上述72條成功。**NEXT**離開寶物袋/洞窟靜態source枚舉，尋找另一份真正能增加原始可見二維、寵物、場景或實質玩法的新來源；不做原網服、登入、引擎或現代體驗改善。
