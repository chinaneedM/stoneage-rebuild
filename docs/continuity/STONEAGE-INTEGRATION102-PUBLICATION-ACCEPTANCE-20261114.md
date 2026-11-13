# INTEGRATION102｜原 meiro 迷宮來源與主線 CI 正式驗收（2026-11-14）

## 精確候選、主線與真實 Actions

- [內容 PR #387](https://github.com/chinaneedM/stoneage-rebuild/pull/387) 已 **squash merge**。候選 `8e84004dda3ce5059f87ae84da02fd17a632cafe`／Git tree `9ef5013dc5e55b332f43ea68d98338f346bb749c`，原 main `0c9bc5da57edfec64deced0af299bb03cbc11387`，合併後 main `b84675030836dc1da897a3660ebea0c7ce14022e`／**與候選完全相同的 tree**。
- 候選精確 HEAD 的 **46/46 Actions completed/success**（push 27、pull_request 19）；本批專用 push [43467122794](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43467122794) job `132029117982` 和 PR [43467173830](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43467173830) job `132029293433` 真正日誌均 `Ran 6 tests / OK`。
- 合併後主線精確 HEAD **27/27 Actions completed/success**；本批專用 main push [43467415233](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43467415233) job `132030124762` 真正日誌 `Ran 6 tests / OK`。未拿候選成功替代正式主線。
- [永久機器收據](../../research/recovered/STONEAGE-INTEGRATION102-PUBLICATION-ACCEPTANCE-R1.json) 保存 73 條各自的 run ID、觸發事件、實際結果、精確 SHA，以及五個本次內容 Git blob／兩個不變的來源索引 blob。**此驗收收據自身新提交的 Actions 尚未後驗，不預支。**

## 原始遊戲內容、原物保管與負證

原資料為後期社群 mixed25 私人已保管 995,176B ZIP，完整 SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`、**2,205/2,205 CRC** 成功，重讀 `npc/genout/meiro.create` 2,246B SHA256 `4aac9ba239351b9bdb932fb1f47d58854023afd17d371119718684103c241574`、17/17 原段逐 SHA，以及三份原 handler 完整 SHA/CP950，共 425B。

在來源範圍內：14 個 `npcgen_warp` 數字配置有六對嚴格反向、兩條無嚴格反向，同時有 1 原 `npcgen_warpman`、1 告示、1 居民；原一 handler 字面 `FREE:LV>49`、`WARP:122,6,5`、`MONEY:-1` 不能升格成原服實際觸發／扣款。舊 MAP04 的四原 DAT（118/120/121/122）已有整 SHA 和尺寸證據，10 NPC 配置座標在尺寸內；100/119 原 DAT 此來源未有合格記錄，另七配置不假填。本輪新增實讀 DAT 0 字節、解碼原 RD 0 幅，未觀察原世界原生碰撞／對話／傳送，也不證官方 TW1.0／1999／1.82 同服版本。

商用原 CREATE／handler 原文、專有圖與 DAT 沒有公開；只發無版權正文的數字/來源 SHA、公有負例和測試。完整 `docs/CURRENT-STATE.md` 保留 **2,709,173B**／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，前史未截斷。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent `null`。

**SOURCE_BOUNDED_ACCEPTED，不是 GAMEPLAY_VERIFIED。NEXT** 另選未重複而實際能取得原字節/原 2D 的遊戲內容族；本批止於迷宮靜態源，需新同源 DAT 或原生實行證據才重新開放，不能改做 MMO 網絡或新引擎。
