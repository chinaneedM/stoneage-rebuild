# INTEGRATION102｜迷宮原 NPC/傳送數字、條件與四張既驗 DAT 來源（2026-11-14）

## 實取原件與去重

本輪從最新遠端 `main` `0c9bc5da57edfec64deced0af299bb03cbc11387`、tree `1b9dacb5167297b4cfc661151b2af5832ea2ed04` 重新啟動。依協議讀取完整 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，原 **2,709,173 字節**全部保留；INTEGRATION101 已驗收，不重做其兩村居民。新材料是尚未獨立彙整的後期社群 mixed25 `npc/genout/meiro.create`，不是將 95–99 的地下城或 101 的礦村舊成果重新計數。

私人已存 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip` **995,176 字節**，全 SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，全部 **2,205/2,205** 成員 CRC 實測通過。真正實讀原 CREATE **2,246 字節／SHA256 `4aac9ba239351b9bdb932fb1f47d58854023afd17d371119718684103c241574`**，以 byte offset/長度/CP950 往返重新核驗 **17/17** 個原設定窗 SHA，與遠端舊 CHAR01 來源索引逐項相同。三份直接 handler 來源也真實讀回、驗完整 SHA/CP950，原始共 **425 字節**，不是三份推測的流程。

## 原版數值配置與新可見內容的證據邊界

- 原 CREATE 共 **17 條**：14 條 `npcgen_warp`、1 告示牌、1 居民、1 `npcgen_warpman`。6 個不同的 floor 數字 **100／118／119／120／121／122**，配置分布 **4／2／3／3／3／2**；並非六個已證可到達場景。
- 14 條直接 `npcgen_warp` 文字目標關係中，**12 條構成六對嚴格坐標互逆**，另外 **2 條（序號 4、9）在同一 CREATE 內沒有對位的數字直反向配置**。這並不證明遊戲單行道；另有來源獨立的 `npcgen_warpman`，不能用不同 handler 類別冒充 `npcgen_warp` 互逆。
- 真讀一份 **309 字節** handler（SHA256 `03f96263b3cbc36d3cbe54f7002d5634c4dfcb52c1e57ddb33e7dec8a9c166e1`），其原始**數值/條件字面**為 `WARP:122,6,5`、`FREE:LV>49`、`MONEY:-1`；是源腳本的字面值，**不是原服務端確實執行等級門檻或收費的證明**。私人原始長對話與其他兩份 handler 的原文不公開。
- 接上先前 MAP04 公開原 DAT 目錄：**118=250×180、120=30×30、121=30×30、122=300×200**，四份原 DAT 的 SHA 全都有前輪實物證據，本批涉及 **10/17** 出生配置坐標，全部在舊尺寸內。**100、119 沒有此前 MAP04 的同 ID 已驗 DAT**，其餘 **7/17** 只限原 CREATE 配置；本批實際讀 DAT 原始字節 **0**，原圖 RD 新解碼 **0**。

[可公開、無商業原文的逐17設定／原 handler SHA／靜態關係／負證 JSON](../../research/recovered/STONEAGE-INTEGRATION102-MEIRO-17-ORIGINAL-SOURCE-MAP-R1.json)保留來源與舊公開索引 blob 交叉。公開 CI 的正負例僅驗原**已歸檔來源 metadata**與本輪可核資料的相互一致；它不會讀私人原始 CREATE／handler／DAT，也不構成重新執行原遊戲。原始私有 ZIP 未增發、不入 Git；本次只讀復用，未取得新的早期官方客戶端或原商服來源。

## 範圍、止點與下一步

原社群 mixed25 不可提升為台湾 Waei/JSS 1.0、JSS1999、或大陆 1.82 的官方同部署事實。`npcgen_warp` 配置不是實際踏入迷宮的運行軌跡，源文字不推斷碰撞/觸發/地圖顏色/原生對話分支，且早期玩家可操作世界仍未進入。沿用 Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent `null`。

**SOURCE_BOUNDED_PARTIAL 止點**：17 項原件已實讀並可公開重驗 SHA/參照關係，100/119 原 DAT 及原服實行機制維持 OPEN。有取得新同源原 DAT/handler 實行或同版原生測試才重開；下一優先轉不同尚未單獨整理、可取得真原始字節或 2D 像素的內容家族，不把 14 條來源數字配置當作已完成真迷宮可玩復原。正式候選/main Actions 與合併**只依真實後驗**，不能預寫成功。
