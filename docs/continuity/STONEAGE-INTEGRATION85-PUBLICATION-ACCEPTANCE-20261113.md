# INTEGRATION85｜四方守護者、四勾玉與兩石像來源限定正式驗收（2026-11-13）

## 來源有界的真正原材料

依[逐字節來源／可見原二維候選報告](STONEAGE-INTEGRATION85-FOUR-GUARDIAN-SHRINE-2D-20261113.md)、[公開源數值與 SHA 派生 JSON](../../research/recovered/STONEAGE-INTEGRATION85-FOUR-GUARDIAN-SHRINE-ORIGINAL-2D-R1.json)，私人原 community mixed25 NPC ZIP **995,176B／2,205 成員**及 ITEM01 ZIP **5,868,386B／838 成員**已實讀完整 SHA／逐成員 CRC；私人另存 TW1 PET07 原像素 HTML 完整 SHA 也吻合舊原來源。

同一社群混合 2.5 來源的 `sb_4sin.create` 在 floor31603／31606／31609 各四份，合計 **12份 NPCEnemy CREATE**；其十二份 `.arg` 與四模板均實讀。另一 `nev1_1.create` 在 31609 的四守護者雖同四個圖號、但座標與 `changeevent` 功能不同，**另四份 CREATE**；31610 兩石像 **兩 CREATE 共用一份 `nev1_5` 原事件**，並非兩份獨立獎勵腳本。四個事件 `GetItem` 原字面為地2528／水2529／火2530／風2531；石像原文條件四勾玉及四 `DelItem`，另 **16個 `GetRandItem` 候選**。沒有原生事件 parser、NPC 創建、戰鬥觸發、通關路徑、獎勵分佈或官方同部署證據。

20個原物品 ID 的兩份社群物品表 **40／40筆原94欄 CP950 原字節行 SHA**真實重構核同，其中六個獎勵 ID 的原第30／31欄值有版本差異，原樣保留。跨**另一來源**台灣1.0已解碼保管圖像真重讀：**18份原物品 RD PNG＋四幅既存守護者 SPR 首幀 PNG＝22幅真原像候選**，圖片檔／RGBA／尺寸逐項核同。**新增原 RD 解碼數0，官方初代NPC名稱／實際原遊戲畫面／原色板／原動畫時間均未獲認證。**

私人 `StoneAge-INTEGRATION85-four-guardian-shrine-original-2D-private.zip` **137,532B、46成員、SHA256 `7edac69d609363cde14aaa9a2b8cfb7c1d633fb5f41a34d79399fdf8b497c60f`** 已保存個人 Library `/石器时代/`，另獨立回讀整ZIP全SHA相同、**46／46 CRC、45／45 非 manifest 成員 SHA**相同。20份原NPC文本、原物品全文摘錄、22份原圖、現代離線查閱HTML及原圖候選接圖仍**只在私人資料庫**，未上傳公開 Git。離線頁不是原客戶端也不代表原遊戲可運行。

## GitHub 真實 Actions／PR／主線

[PR #361](https://github.com/chinaneedM/stoneage-rebuild/pull/361) 候選 HEAD `f980cc0448900c5c4f2d80ec6d3e0b756a9fa51d`／tree `145f498eeaea43f1197cd2c6b38b7450d974f63b`，**27／27 push、19／19 pull_request＝46／46條實際 completed/success**，無失敗。按來源 HEAD 正常 squash 合入正式內容主線 `ed58e02ceaca24891e229e66625c2efcd47c062f`，**同 tree**，本內容正式 main **27／27 push Actions**亦已全部實際 completed/success。三次新增專項的 push [43293726095](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43293726095)（job 131446350990）、PR [43293804955](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43293804955)（job 131446629350）、main [43293965248](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43293965248)（job 131447189896）已分別實際取得 job 日誌，均清楚顯示 `Ran 21 tests`／`OK`。

全部 **73條 Action 真正的 run ID、SHA、event、job 所在主源與時間、status／conclusion**已按來源固定在[永久機器驗收 JSON](../../research/recovered/STONEAGE-INTEGRATION85-PUBLICATION-ACCEPTANCE-R1.json)。這只驗證**公開派生數值契約**，不得報成原圖片在公開 Actions 中解碼或原商業客戶端／伺服器成功執行。本文／JSON 的新驗收收據提交**自身的 Actions 不包含於上述73條**，必須另按該新 HEAD 後驗。

公開內容對上游 main 僅五處增量（workflow、測試、源派生 JSON、日期來源記錄及 README 復原續接），本文及機器收據再加法追加；不改寫舊失敗、原版史料或大歷史檔案。歷史 `docs/CURRENT-STATE.md` **完整2,709,173B／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原樣保留**，未縮短／覆蓋。Stage A **7 PARTIAL＋2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null 不變。

**最高 NEXT：** 本守護者→原勾玉→原石像候選物品／原二維像素關係已源限定閉合。輪換別組真正未重複且有原件與真原2D像素可核的寵物、物品或任務內容；只有拿到對應原生程式處理器、原伺服器實際載入／客戶端操作證據時才增量重開 `NPCEnemy`／`changeevent`／`GetRandItem` 原始運行語義，不虛構原生隨機率、觸發順序或玩通任務。
