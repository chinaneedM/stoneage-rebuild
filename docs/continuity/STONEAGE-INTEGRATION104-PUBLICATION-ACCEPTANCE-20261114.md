# INTEGRATION104｜31900原NPC來源及全部73次實際Actions永久驗收（2026-11-14）

## 已發生、可精確回查的GitHub驗收

- 內容 [PR #391](https://github.com/chinaneedM/stoneage-rebuild/pull/391) 已合併；候選 `f6b81d44aea0134cbb75000e52d7962ab08348da`，正式 main `fccd89872eb82f3c749baa45dce4876366a8bdc0`，兩者同 Git tree `ecdbd7f9162329672c9d433c6ca987d5c8b3d6e3`，相對舊 main `dc98be953b6a6c5ee114bef6e5904c2db5e05d62` 僅5個派生資料/測試/README變更。
- 候選exact HEAD完整 **46/46 completed/success**（push27，PR19）；[專用push run 43529583721](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43529583721) job 132243654762、[專用 PR run 43529626128](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43529626128) job132243802327，都有真實 `Ran 12 tests / OK`。
- 合併後**獨立正式main** exact HEAD完整 **27/27 completed/success**；[專用main run 43529739602](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43529739602) job132244179881，亦由真日誌查 `Ran 12 tests / OK`。
- [永久機器收據](../../research/recovered/STONEAGE-INTEGRATION104-PUBLICATION-ACCEPTANCE-R1.json) 保存以上 **73條** 真實run ID/event/HEAD/status、五個公有 Git blob SHA、來源/私包 SHA/負證。**本驗收收據自身新提交的 Actions 尚未取得，不能提前聲稱成功；須對收據精確 HEAD 另外驗證。**

## 來源的實物保管鏈與未決邊界

- 後期 community mixed25 保存 NPC ZIP **995,176B** / 2205/2205 CRC；真原 `npc/genout/31900npc.create` **7,121B** / SHA256 `6efe8306e0fc4fae6cf4d76af438c98e624d8637e1429d970efe77692ff6aa9f`，本輪全47逐原SHA；真原18 handler共4,249B逐個SHA和 CP950 完成。原文不入公開Git。
- 已核舊 MAP04 九個 DAT header 但**無新DAT原字節讀取**。原 source 16靜態傳送，31910有13個`FREE:ITEM=2548`和`DelItem:2548*1`、31903有一個`FREE:ITEM=2549`而無DelItem； **31902 (9,67) 與15×10原 DAT 尺寸衝突**永久保留，不強行修 source，也不認證實際運行的交易和傳送。
- ITEM01原兩表 ID2548/2549整行SHA相同；獨立TW1零售原RD已解碼舊候選圖24051/24058/24112本輪只重新校驗已存PNG SHA，不跨版認作同服身份，無新RD解碼。
- 19份商業原小文件＋3張舊驗真零售原PNG＋1現代離線31910靜態點選HTML＋SHA清單的私人ZIP **18,408B** SHA256 `92b3721f0882f37d87698de0c729adb7fcf066ed55c1193b3d787352b6e0f626`，已存私人個人Library、從Library獨立下載**整字節一致、24/24 CRC、23份內容SHA全一致**。現代HTML不是原生遊戲畫面。
- 舊完整 `docs/CURRENT-STATE.md` **2,709,173B** Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未變。Stage A 7 PARTIAL＋2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null。

**SOURCE_BOUNDED_ACCEPTED，非 GAMEPLAY_VERIFIED。NEXT** 尋找另一組未重複的原實物可視2D/寵物/NPC/任務來源，不延伸沒有原字節新證據的虛構玩法。
