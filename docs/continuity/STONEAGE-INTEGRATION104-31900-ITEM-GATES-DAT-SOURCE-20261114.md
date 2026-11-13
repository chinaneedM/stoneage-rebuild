# INTEGRATION104｜31900 原 NPC 六樓層與 16 條靜態傳送、雙道具條件、原 DAT 反例（2026-11-14）

## 重新啟動及查重

本輪按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重新讀 GitHub 遠端 main `dc98be953b6a6c5ee114bef6e5904c2db5e05d62`／tree `d443a79b2e337911e201bb3b61aee2562203c8f9`、最後正式提交、exact-head Actions **0 條**、開放 PR **0**、README、協議及指定模組和來源邊界檔。`docs/CURRENT-STATE.md` 一般文字讀取為空，**轉用原生 Git blob** `c89e0e33537990aa2132b47c40fef49a985a935c` 完整重讀（2,709,173B；UTF-8解碼長度與原字節不等），不得空覆蓋。上輪 INTEGRATION103 收據完成但它自身主線提交沒有新 Actions，不能虛稱「0/0成功」。

本次換新內容族：`npc/genout/31900npc.create`，有真來源但尚未於 README 單獨整合，不重做 INTEGRATION102 `meiro.create`、INTEGRATION103 `unsoya_1.create`、舊長毛象客運/新手送貨或已完成的完整 CHAR01 靜態 NPC 目錄。本次成果是在原 CHAR01 的已有全文索引之外，重新**實讀並驗 SHA 的指定原 CREATE、真 handler 文本、原道具雙表及 DAT來源對照**，新增可被反證測試的具體源關聯與矛盾。

## 實際原始資料和完整保管

- 後期社群保存 mixed25 私人原 NPC ZIP `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176B**，SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，本輪 **2,205/2,205 CRC**。原 `npc/genout/31900npc.create` **7,121B** SHA256 `6efe8306e0fc4fae6cf4d76af438c98e624d8637e1429d970efe77692ff6aa9f`，**47/47** 原始 byte start/end 和 SHA256 均與既存 CHAR01 公共原來源索引 blob `a088b61a3212f7049e7793f587123ffb29bebad7` 完全吻合。
- 真正重新讀出 **18/18 個被 CREATE 直接引用的原 handler**，共 **4,249B**，全部以 CP950 往返、逐原全 SHA 對舊索引成功。原 CREATE 包括 **27** 條 `npcgen_mugon`（圖形號24051）、**14** `npcgen_warpman`、**3** `npcgen_man`、**2** `npcgen_warp`、**1** `npcgen_signboard`。這些是原配置而不是47個已在運行的NPC，也不能直接將 `graphicname=24051` 證成某個怪物/圖像的正式身份。
- 上輪原 MAP04 資格索引 blob `1ef8c004179128ea44ffa4fb4259748bc8c83911` 真實保存所需 **9個不同樓層 31901–31907、31910、31911** 的原 DAT 完整 SHA、字節和尺寸（本輪沒有重新取回 DAT 原字節）；其中原 CREATE 覆蓋6個樓層，傳送目的補齊另3個。所有16條**傳送目標**按先前合格 DAT header 均在界內。
- 已保存 ITEM01 兩個原 itemset 完整行 SHA 的公有原索引分片02 blob `b91bc8335db508998f4595144ce371979ea8c849`：**ID 2548** 兩表整行相同，原圖號 **24058**，**ID 2549** 兩表整行相同，原圖號 **24112**；這是社群後期來源兩表一致，不證臺灣1.0同服資料。原 ITEM01 私有 PNG 載體 ZIP **5,868,386B** SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`，全 **838 CRC**，本輪真正重讀 TW1 零售**已解碼的舊候選** `24051/24058/24112` 三張 PNG 全 SHA／圖像尺寸，**新 RD 解碼=0**。其中 24051 僅與27條 `graphicname` 具有數字交集，不能因此宣稱是社群後期 NPC 的同版正式圖形。

## 新恢復的靜態遊戲內容規格

| 靜態源配置 | 原文字面條件/目標 | 觀察數 | 證據資格 |
|---|---|---:|---|
| 31910 十三個 `npcgen_warpman` | 同一 `FREE:ITEM=2548`、逐個 `DelItem:2548*1`、`MONEY:-1`、各自原 WARP 目的點 | 13 | 實際讀原13 handler 全SHA，目標 DAT header 內；不證交易、扣除、可到達或實際WARP執行 |
| 31903 一個 `npcgen_warpman` | `FREE:ITEM=2549`、`MONEY:-1`、`WARP:31904,7,3`，**沒有 DelItem 源欄位** | 1 | 不能把2549假設為會扣除 |
| 31904 / 31911 原 `npcgen_warp` | 無外參文件，原內聯目標分別31903 `(38,4)`、31902 `(8,7)` | 2 | 靜態入口/出口字面，不證雙向通關 |
| 原本 31901–04、31910、31911 出生點 | 原 CREATE 共47個點；按以前已核DAT資料尺寸 46在界內、**1在界外** | 47 | 靜態資格，原地圖碰撞/朝向/實走仍未證 |

**重要原源矛盾，不得「修復」：** 原 CREATE 第4段（0-based index **3**）寫樓層 **31902**、出生點 **(9,67)**；既存已驗 `31902.dat` 是 **15×10**（908B，SHA256 `27bc3d9573207552813469ba197ed4da5b8ad3de8e3f3a94219fc09ff389ad49`），因此 source y=67 明確不在該 DAT header 範圍。另一 `31911` 來源直傳 `31902,(8,7)` 則在界內。不能因此擅自把前一坐標改為 (9,7)、臆測載入器自動糾正、宣稱遊戲BUG或聲稱跨版原 DAT 一定適用：社群 NPC 保存包／原 DAT 索引雖相同大來源族，未驗運行載入順序。

同一性與身份邊界：後期保存版 mixed25 原 NPC/script、後期保存 DAT、另一認證的臺灣 Waei/JSS 零售1.0 RD 候選圖，未證同一次正式服端部署。原圖像雖為已保存真像素，私人**靜態 HTML 圖層與數字點選**是現代研究介面，沒有任何 `31910.dat` 原始像素畫布，也不是遊戲截圖。未讀到新的原商業EXE或實測遊戲事件。原全文/PNG/原源檔不入公開Git，只儲源SHA及數字候選。

## 私有研究包、公開驗收與止點

私人觀察包 `StoneAge-INTEGRATION104-31900-source-map-items-2D-private.zip` 含原 CREATE、18份真正原handler、三張之前已驗的零售原候選PNG、現代離線靜態可點選 `31910` 來源點HTML及私有SHA清單。包大小及SHA以本輪驗收收據的真驗為準；須上傳私人Library後獨立下載 CRC/SHA，不能在未做到前宣稱永久保管完成。

公開 [逐原窗口與數字負證JSON](../../research/recovered/STONEAGE-INTEGRATION104-31900-ITEM-GATE-DAT-SOURCE-R1.json) + **12項**本地可重放正反測試 + 專項GitHub Actions，均不復制原商業文本或原像素。正式 GitHub PR/候選 Actions／主線精確 HEAD 驗收需在發佈後根據真實結果另記，不預支。

保留 Stage A **7 PARTIAL＋2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent **null**。**NEXT** 與本組不同的真實原地圖、NPC或寵物2D可觀察資料；31902唯一越界需同載體更新DAT或原生行為才能解開，不用現代推測改原歷史。
