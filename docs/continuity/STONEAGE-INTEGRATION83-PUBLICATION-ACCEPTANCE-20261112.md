# INTEGRATION83｜兩處原素材市場：正式GitHub Actions與私人原件保管驗收（2026-11-12）

## 有界原內容交付

[來源限定原報告](STONEAGE-INTEGRATION83-1009-4009-MATERIAL-MARKET-20261112.md) 與 [公開機器派生索引](../../research/recovered/STONEAGE-INTEGRATION83-1009-4009-ORIGINAL-MATERIAL-SHOP-2D-SOURCE-R1.json) 已永久接入主線。依私人已保存 community mixed25原NPC ZIP 995,176B／2,205成員、原ITEM01 ZIP 5,868,386B／838成員的**真實來源CRC、SHA與逐段原文重核**，有 `floorid=1009`、`4009` 各五個共10個原`shop_m/shop_m2` NPC CREATE、10份完整原參數。同對應的五組 `ItemList` 原文字串一致，**不是**十個商店SHA相同，也不證原服務端選貨執行一致。物品原文直接列ID **6次**，另外**32個區間表達式**只有依「含兩端」假設可展開 **256候選出現**，不把262次混成原版實際商品數；去重為123個原物品ID，皆兩份同保存載體原物品表的完整94欄原行SHA逐項同一。不同載體TW1.0零售過去真正解碼的45種原RD圖PNG現存、逐原像SHA/RGBA重新核驗，支援117個物品ID來源限定可見候選；6 ID圖缺口保留（4屬2個原RD解碼失敗alias，2屬2個TW1索引未找到alias），新增原RD解碼數**0**。第一輪原CP950位元組 `}` 切塊誤失兩CREATE，最終改為 CP950 解碼後以原位元組精確回算而10/10成立；首次方法錯誤不追認為通過。沒有證明原生選貨、交易、官方同版或原客戶端行為。

## GitHub實際驗收

[PR #359](https://github.com/chinaneedM/stoneage-rebuild/pull/359) 候選 HEAD `1960688af3020cf3bfe8974d93a43b8801bb8c24`／tree `69064a00e97d59027f0bb40edb7aee28a2582ab8`，**27/27 push**＋**19/19 pull_request**共 **46/46條**Actions completed/success。按預定SHA經squash合併正式內容主線 `60f8650628ae19d9e5fba97408e11d4579a4d7b9`／**同tree**，正式**27/27 push Actions**亦completed/success。新增專項 push [run 43223850860](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43223850860)／job `131201885866`、PR [run 43223913227](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43223913227)／job `131202086662`、main [run 43224093163](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43224093163)／job `131202679486` 的實際日誌分別為**Ran 13 tests／OK**。這三個專項成功不替代原商店 native 執行；主線原R28較慢工作流完成後才採集最終27/27，不提前代稱成功。

**73條成功Actions**按其真正的候選／主線HEAD、事件、時間、run ID、workflow名稱逐條存入 [驗收機器回執](../../research/recovered/STONEAGE-INTEGRATION83-PUBLICATION-ACTIONS-R1.json)，將PR候選成功與正式內容成功分離。此驗收收據新提交自身的後續Actions**不在73條內**，必須另查，不能將之前成功冒作最新SHA成功。遠端相比起始 main 僅增 workflow、README續接、本文前一版來源報告、源JSON和測試五處，沒有原件或舊歷史刪改。

## 私人永久保管／止點

私人 `StoneAge-INTEGRATION83-1009-4009-original-material-market-private.zip` **156,739B**／SHA256 `cb101b40000e631e028ea50eb0aaa1689c58b35524594fa24efc1a4991566eda`，已上傳個人Library `/石器时代/`，再**獨立自Library取回、逐整包SHA相同、69/69 ZIP CRC與68/68非manifest內容SHA驗證相同**。包含原參數與原物品行選摘、45份已驗真原圖候選、現代私人二維查閱；原有版權圖／原配置全文／完整原物品表沒有進GitHub。公開只留合法派生原值／來源SHA／測試，不以台灣1.0的圖片宣稱community mixed25或JSS1999同一官方運行部署。

`docs/CURRENT-STATE.md` **2,709,173B**、原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 完整保留，不更新其巨大歷史正文。Stage A **7 PARTIAL＋2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent仍未知。

**NEXT：** 本市場10商店／123物品／45既存原候選圖已來源限定閉合。轉另一真正未重複、有同源原物可核的寵物／物品／任務二維內容；本批6原RD缺口只有得到真正可讀原位元組時才重開，不虛構缺圖或擴交易引擎。
