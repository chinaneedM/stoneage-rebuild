# INTEGRATION90｜波魯龍王殿 24 原 NPC 配置／原 DAT 座標／真實 TW1 二維動畫候選（2026-11-13）

## 任務與新增範圍

fresh `main=19e81df26af2b8dc2883573109d29065e8fc0f42` / `tree=29bc247ff4f73523076dec714ed37d7ed5237f1b`，起始 26/26 同 HEAD Actions 完成且成功、開放 PR=0；已重新讀取完整 `docs/CURRENT-STATE.md` 原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` (2,709,173B)、continuity §9–18、路線／模組、最新 INTEGRATION89。**原 CURRENT 不改字節。** 因 INTEGRATION89 已完成洞窟通行／店務，此輪選尚未作整廳來源—可視二維連接的波魯龍王殿，不重複已驗龍王原 EVENT63 的語義。

**原實物**：後期社群 mixed25 私有 NPC ZIP 995176B／全 SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`；2205/2205 ZIP 成員 CRC 通過。原 `npc/poru/boss.create` 3771B／SHA `be204fb18123356bd6c3cd0a1e70e0552c77138ccbbbb0b03a91d351de4edbb5` 的 **24/24 原 CREATE 起止位元組窗和 SHA**已通過；公共 CHAR01 全員行索引保留原序，原 floor 5511 **23** 條，floor 5510 **1** 條，只有 **6** 個不同 `graphicname` 數值（不是 NPC／物種總數）。原函數 22 `npcgen_man`、1 `changeevent`、1 `sb_ganzo`，五個真正不同 `file:` 參照全部實取並核 SHA。三份 13B 短原文本在不同原路徑但**完整 SHA 相同**，不能當成三段獨立對話。

## 圖層實物而不是虛構站位

從之前私人 INTEGRATION58 保管 ZIP 真讀兩份原始 DAT：floor 5511 `30×30`、5408B SHA `5d44ea8c70c2537447926714fc0f84f5900c63e4008917fabcd3885d73dc0884`；floor 5510 `60×60`、21608B SHA `a7be854d0767203b547984269e34e72c2c443c011c35027d727d7fd192c00cfc`。24/24 原創建 `borncenter` 坐標在各自 DAT 界內，依 8B 頭與三個連續 u16 平面逐位置真讀。5511 的 23 條第三原數值均 49152；5510 (53,17) 的一條為 49154。**不從該第三欄自行命名障礙／事件／通路**，更未證原版運行站位。

新有界觀察：floor 5510 (53,17) 原 `sb_ganzo` 所指獨立 `poru/boss.arg` SHA `783dc96dd201bbede74049d375dbf776d62ab9b5aecc6a2b257e448fdb4f5f3f` 的原字面 `entype:2`、`dieact:1`、10 個 `enemyno`、`warpfl:5511`、`warpx:6`、`warpy:24`。這是**原配置候選**，不是原生戰鬥、勝利傳送或可達性驗證。floor 5511 (17,12) `changeevent` 對應 `boy04` 及事件 63 是 INTEGRATION58 先前已查，未算作新觸發規則。

## 另一來源臺灣 1.0 原 SPR 與實際原 PNG

對獨立原 TW1 零售 PET07 原素材，6 圖形號 `100351/100353/100354/100371/100373/100396`，原 SPR 全段 SHA 與現存 PET07 收據逐組相同，動作 0/2/1 方向 0 共 **18 個真正原動畫序列、187 原有序幀位置、92 個互不重複的源 bitmap 數字**。私人舊 PET07 畫廊真取上述 **92 張現存 PNG 原候選**、逐張重算 SHA256 與尺寸，全部 **92/92** 和分開的 TW1 原 RD 候選 `Palet_1` 公私來源 SHA **逐字相同**；不同 0、缺 PET07 來源核驗 0。此次新增原 RD 解碼 0、並未重新整包下載 TW1，絕不稱 92 張新發現的官方美術或六種早期官方寵物。與 INTEGRATION89 的另一三組調色板不一致是**不同圖形組與不同選取範圍**，不得以此 92/92 修正或抹去先前反例。

## 私人真正二維觀察實測／公私邊界

私有 10 成員觀察 ZIP **3,391,913B、SHA256 `a59c516ae39683c9a74abb1deb795328b892524fea0f7d8e29747155a3d553ad`**：含真正原 CP950 CREATE/5 arg、5510/5511 原 DAT、92 張已驗 TW1 舊原像內嵌的現代純離線觀察頁、先前 DAT 現代原圖觀察及私有源收據；存個人 Library `/石器时代/StoneAge-INTEGRATION90-Poru-Dragon-Hall-original-2D-private.zip` 並**獨立取回**完整 ZIP SHA/10 成員 CRC 無誤。Chromium 原私有離線頁實際 **24 條切換、72 次動作／翻幀、兩份地圖圖片載入、0 JS 錯誤／0 外部 HTTP 請求**。座標示意與原 DAT 圖像**分開、未配準**；頁面是現代證據觀察器，不是商業遊戲原生畫面或原生動作 FPS。任何商業原圖、原 DAT、原完整文案未加入 Git。

[完整逐 24 建立窗、DAT 原格、五參數 SHA、6 原 SPR／92 PNG SHA 公開無原圖衍生索引](../../research/recovered/STONEAGE-INTEGRATION90-PORU-DRAGON-HALL-SOURCE-2D-R1.json)。 Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki GATED、R79 暫停、overall_percent=null 不變。下一包換另一有獨立實物且未重複的原二維內容家族；無原遊戲運行輸入不重開守衛／事件執行推論。
