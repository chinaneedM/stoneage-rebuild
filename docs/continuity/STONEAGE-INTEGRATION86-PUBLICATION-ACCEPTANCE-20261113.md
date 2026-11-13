# INTEGRATION86｜漆黑洞窟原NPC、事件負證與原二維像正式驗收（2026-11-13）

## 實際完成的原材料限定

由[來源原字節限定報告](STONEAGE-INTEGRATION86-SIKKOKU-ORIGINAL-QUEST-2D-20261113.md)與[公開機器來源索引](../../research/recovered/STONEAGE-INTEGRATION86-SIKKOKU-SOURCE-2D-R1.json)逐項驗證：community mixed25 原NPC私人ZIP **995,176B／2,205項 CRC**、ITEM01 原保存ZIP **5,868,386B／838項 CRC**、另一保存台灣1.0原SPR像素 PET07 HTML 完整 SHA 全部真正回讀同一。洞窟原 `sikkoku.create` 八 CREATE（五不同樓層考古家、精靈王、兩護士）與獨立 `sb_sikkoku.create` 的兩原 NPCEnemy 守護獸，逐真原CP950 CREATE byte ranges/完整SHA保持；五考古事件共 **16個來源TYPE段**。來源僅後期社群混合2.5配置、跨另一台灣1.0零售原像候選，不證 JSS1999 或認證官方同一運行部署。

**真實反例不修復**：原事件53 `EVENT:ITEM=`四 ID為2701、2707、2735、2770，卻原 `DelItem:`四 ID為2701、2702、2703、2704；兩集合只交集2701，絕不補成一致、擅稱原生成功扣獎或修任務。該段 `GetItem:20570,20571,20572` 三 ID僅保管原第二物品主表有行，不能假設第一表有；五考古腳本「16樓」註釋與實際 five CREATE floor32002/32006/32009/32014/32016各異。原精靈王確切指 `npc/777/ten.arg`，同名 `npc/giiru/event/sikkoku/ten.arg` 原SHA/長度不同，不能替換；首者二次轉生後不可騎乘只為原文本，不是原生機制實行證書。

19不同物品原ID對原兩份94欄資料 **35／35整原行CP950拼合SHA成功**；本輪真正重讀已保存台灣1.0另源**16幅物品原RD PNG＋3幅原SPR原幀 PNG，19幅已存在真原像**，圖片/像素/尺寸合格；其餘原圖號 **20241／24314／24315** 無該 TW1原索引，保持缺件。**新RD解碼0、新商業原美術0、原native遊戲運行0**。

私人 `StoneAge-INTEGRATION86-Sikkoku-original-source-2D-private.zip` **113,454B／35成員／SHA256 `1433a5638f2e7358b39a5d2955cb706a8bd48082467e5d781ba37238f1b43b70`** 已保存個人 Library `/石器时代/`，並**再次獨立從Library物化回讀**，整ZIP bytes/SHA 完全相同、**35／35 CRC＋34／34 manifest檔 SHA**相同。12份選定原CP950 NPC與參數全文、原19物品完整行選摘、19真原PNG及私人 HTML/接圖只在私人庫，**不在公開Git**。

## 兩SHA三階段 GitHub 真正後驗

[PR #362](https://github.com/chinaneedM/stoneage-rebuild/pull/362) 候選 `16911a673cbc3f67752bea33a042b832305240b3`／tree `f24ceaf204f352bdfcc51f7532a6af0fea37ff3d` 經 **27/27候選 push＋19/19 PR＝46/46實際完成success**；正式內容 main squash `3fc574ef9f53f947b8fb361d6dd4f252a5b952ff`／**同一 tree**經**27/27 main push Actions completed/success**，共**73/73**具各自真正 SHA 的成功執行。

新專項三次實際真 job 日誌：候選 push [43359088039](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43359088039)／job `131668047923`、候選 PR [43359142853](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43359142853)／job `131668229971`、正式主線 [43359260565](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43359260565)／job `131668616548`，三個都逐日誌讀見**`Ran 21 tests`／`OK`**。其公開 CI 只重放**原來源衍生數字與負證**，沒有讀私人原圖或執行原伺服器、原客戶端。

**73個真實 run ID／event／head SHA／狀態／成功、私人保管SHA及精確限制**全部放[永久機器驗收 JSON](../../research/recovered/STONEAGE-INTEGRATION86-PUBLICATION-ACCEPTANCE-R1.json)；本驗收檔和JSON自身的新主線提交的 CI **不包含**在上述73次，必須按新HEAD獨立後驗，不能借舊成功宣稱。

舊 `docs/CURRENT-STATE.md` **2,709,173B／原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 逐字保持**；README只有加法記錄，原失敗、來源版本與官方執行缺口均保留。Stage A **7 PARTIAL＋2 OPEN**、B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null不變。

**NEXT：** 這份漆黑洞窟原NPC→故事檔→19原圖源關係已到靜態有界止點。輪換另一真正未重複且有原CP950/原物品/原像素實物的2D任務或NPC/寵物內容；只有原生腳本處理器／同部署實際物品異動／精靈王操作證據才重開這組 `EVENT/DelItem` 不一致、原二次轉生騎乘文字及獎勵可得性，絕不向原版填新行為。
