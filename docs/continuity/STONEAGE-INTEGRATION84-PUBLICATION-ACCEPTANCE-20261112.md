# INTEGRATION84｜JBA 20712 原始來源／私有像素／73條Actions正式驗收（2026-11-12）

## 真正完成的有界原材料

以[來源限定報告](STONEAGE-INTEGRATION84-JBA-ORIGINAL-SHOP-2D-20261112.md)及[完整公開來源索引](../../research/recovered/STONEAGE-INTEGRATION84-JBA-ITEM-SOURCE-R1.json)為準：community mixed25 2205成員原NPC私人ZIP和838成員原物品圖表私人ZIP均按完整SHA及每成員CRC**重新真實核驗**；原 `npc/genout/shop_event2.create` 的floor20712九個CREATE逐原位元組區間與CP950重編SHA復核；六份原服務參數真讀。四店中的**三個獨立ItemList源行**總共44個物品ID出現，第四個商店原始`ItemList:`僅嵌在`itemfull_msg`文本裡的16個號不能抬成實際商店上架；兩原寵技參數各12／9，共21個源字面技能號。60個不同物品ID在兩份94欄原行源索引共**120／120項重組原字節SHA一致**，對應另一台灣1.0零售來源已真解碼並私人保存的**54個不同RD alias PNG**，原PNG SHA、圖片尺寸全部真重讀核對；**新增原RD解碼0**。來源跨版本數值候選不證初代官方服務同部署，沒有原生原服交易／授技／NPC觸發運行。

私人`StoneAge-INTEGRATION84-JBA-20712-original-items-private.zip` **112511B／57成員／SHA256 `b6ec3b9122cc9d037f68988d0b9e9875745973ad94b3ac76faa20a23349c5f4f`** 已寫個人Library `/石器时代/`，再次**獨立取回與原包整位元組相同、57／57 CRC成功**。私有觀察頁60個圖片引用可全部解析，54個實際不同真原圖候選全部可由Pillow解碼且尺寸一致，未冒稱原生瀏覽器／原遊戲運行。商業原創建原文、94欄原物品表與原PNG未進Git。

## 分SHA實際GitHub出版與Actions

[PR #360](https://github.com/chinaneedM/stoneage-rebuild/pull/360)候選分支原 HEAD `2daed99b91588491d79ef8053b605fd4e6a7a54e`／tree `b93f26fad395590f3068aaf118c1d01ac5c14563`，**27／27 push +19／19 pull_request＝46／46 Actions completed/success**。已按候選確切SHA做squash合併；正式內容main `201e9a848700f5c4054cb766b1cdd8d2e6531575`／**同tree**，**27／27 main push Actions completed/success**。三次新增專項 CI 的真實run分別為push [43229416339](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43229416339)、PR [43229468428](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43229468428)、main [43229724656](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43229724656)，均完成success；另有15項公開資料元數據檢查在本地實際運行OK，不能把這些公開CI稱為原商服測試。

實際**73條run ID、事件、HEAD、status、時間、網址**全永久保管在[本輪機器驗收JSON](../../research/recovered/STONEAGE-INTEGRATION84-PUBLICATION-ACCEPTANCE-R1.json)，PR候選與正式內容主線不混用。此驗收收據**自身之後的main Actions必須另獨立後驗**，不能借用內容commit的27／27成功率。

來源歷史`docs/CURRENT-STATE.md`完整原2,709,173B／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`保持不變；公開Git新增合法派生證據／15項新測試與CI workflow，並在README加法續接，無私版原像。

**止點／NEXT：** JBA原靜態服務到真原像候選之來源關係已核有界，禁止將`itemfull_msg`嵌字母誤讀成已可買物品。轉另一批未重複有真實來源合格的原二維寵物／物品／任務內容；若日後有原native parser或同部署執行資料才重開這個16號欄位問題。Stage A **7 PARTIAL＋2 OPEN**、B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null不變。
