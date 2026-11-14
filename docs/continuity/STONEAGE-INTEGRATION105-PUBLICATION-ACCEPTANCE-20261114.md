# INTEGRATION105｜原dungeon02來源與73條實際 GitHub Actions 永久驗收（2026-11-14）

## 已完成的精確 HEAD CI / 主線閉環

- 內容 [PR #393](https://github.com/chinaneedM/stoneage-rebuild/pull/393) 已實際合併。候選 `dd1ea58a632842dd9b7b8e63a19d3cd6abc0c380`，正式 `main` `6bfb5a13ca8955eb76ad475687317e5275a0722f`，**兩者同 tree `4ae60f86c6ed4ed9399cda8d40df8243e2b2f41f`**。對舊 main `86d83465745283bf42ebc4384a455eb3025ddc1f` 共改5個派生文件（README、來源報告、數值 JSON、單測、專用工作流）。
- 候選精確 HEAD **46/46 completed/success**：push **27**，PR **19**。專用 [push run 43539493768](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43539493768) job `132276441969` 和 [PR run 43539514466](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43539514466) job `132276507363`，均在實際 job logs 出現 `Ran 9 tests / OK`。
- 正式主線獨立新 HEAD **27/27 completed/success**；[正式 main run 43539619083](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43539619083) job `132276850099` 亦已從原日誌實核 `Ran 9 tests / OK`。全部 **73條真實 run ID、event、HEAD、完成狀態和5個內容 blob** 收錄於[永久機器收據](../../research/recovered/STONEAGE-INTEGRATION105-PUBLICATION-ACCEPTANCE-R1.json)。
- **此新驗收收據自己的新 HEAD Actions 尚未核定**；不可把上面73條歸到本驗收提交的 CI 成績，也不能把無匹配 run 說成0/0成功。

## 原源真實資格及不可抹去缺口

私人個人 Library 中既存 community mixed25 原 NPC ZIP 995,176B SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 已本輪真重讀 **2205/2205 CRC**；真正原 CREATE `npc/genout/dungeon02.create` **18,174B** SHA256 `bf047be69b5b1d3f6fda836cac4174e69868031b4e3e57f71c2f7da2b02636b6`，151條 byte span 完整對舊 CHAR01 原 SHA 索引。7真 handler **720B** 各逐 SHA / CP950 可讀，但原文字不公開。

原 **144** 靜態 `npcgen_warp`：**132**具有精確來源反向，**12**沒有；其餘7源為 `npcgen_man`。出現65個源 floor 中只有64具既核合格 DAT 尺寸，**floor300無匹配 DAT**；舊 DAT 內源點135及目標128全在界內，其他16源點/16目標為缺DAT，而非已證越界；舊 INTEGRATION104 另一 `31902(9,67)` 歷史反例原樣不修。這些只屬後期社群來源與另一既核同來源族 DAT 的歷史靜態資料資格，**不證官方臺灣1.0/JSS1999同一部署、原native傳送、碰撞、對話執行或原世界可玩**。本輪新 DAT 原字節讀取0，新增 RD 解碼0；原商業文字、像素、執行檔未公開。

已保留整個 `docs/CURRENT-STATE.md` **2,709,173B** Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`；Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null。

**來源有界驗收完成，不是玩法驗收。NEXT** 若取到可信 `300.dat` 同載體原件，有限復驗相關坐標/2D來源；否則輪換別的未重複、具原字節/原像素的歷史 NPC、寵物或任務組，不擴張虛構玩法或新引擎。
