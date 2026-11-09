# INTEGRATION26｜第2009市場十二種缺台灣1.0索引的商品：同保存來源三幅原 RD 候選像素回接

## 真正的新整合，不重複舊原件

2026-11-09 從遠端 `main` HEAD `65444b93df5f92ddffb5915883848cc516d25dd7`／tree `c8c999ca20685cc9ed46effd4f56d99eca4faf1a` 開始；依協議確認全量 `CURRENT-STATE.md` 原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`、2,709,173B 完全保留。前包 INTEGRATION25 已合併、PR 八項與主線十六項 Actions 實際成功，原始商店七個與181個不同商品ID皆不重造。

此包要填補**INTEGRATION25 特定來源資格缺口**：12種混合2.5原市場 ItemList 關聯 ID `12218-12229` 在已選擇的台灣1.0零售原 `ADRN/REAL` 索引**找不到圖號**；這不等於其他版本沒有原像素。重新查核倉庫已驗的 [ITEM06 後期社群原 RD 來源報告](../../research/recovered/STONEAGE-ITEM06-MIXED25-MISSING-TW1-ITEM-ALIAS-PIXELS-R1.json) 後，這12種 ID 正好全部落在**三個早已真正原 RD 解碼並持久化的 mixed25 候選圖像別名**，不需要再解包原338MB以上商業REAL，也不應假造圖像。

## 私人原像素保管重新讀取

本次從私人 Library **實取並驗 SHA** `StoneAge-ITEM06-private-mixed25-item-pixels.html`，1,242,805B、SHA256 `ff901220af1484a3367ef52014fe561b25bd6ee9d270b4b6d3fb220ff1f8a700`；原HTML所含三段現存、離線內嵌 PNG 經真正 base64 解出，再以每份 PNG **整文件 SHA256 與 PNG 原頭寬高**獨立核對先前公開 ITEM06 永久原像素收據：

| 同 mixed25 原 `ADRN` 別名 | 原保管對應不同商品 ID | 私人 PNG bytes | 原圖尺寸 | 完整 PNG SHA256 |
| ---: | --- | ---: | --- | --- |
| 24553 | 12218–12221 | 1,204 | 32×28 | `d063b00dc3cf088ec94fd7f741457cbe723889ca44aebded27d89c9d504a0223` |
| 24560 | 12222–12225 | 1,322 | 36×36 | `783f5ed58b050fb278efa141a748b4107b68e27dcb180b3320c05fb0feade7ac` |
| 24552 | 12226–12229 | 1,352 | 32×33 | `ffcd24fbf6bafd4042b4983cb5ae650813dc9bea40ade242e9d4bac920d08acc` |

三圖具 ITEM06 **同保存後期混合2.5原** `adrn_15.bin`／`real_15.bin` 固定源文件整 SHA、原 80B 記錄 SHA、真 RD 壓縮塊 SHA、真索引像素 SHA及先前二種獨立解碼收據。本次只**重新讀取先前原 RD 解碼所保存的真 PNG 全文件**，**沒有重新讀取原 AD RN/REAL 商業檔，也沒有新增原 RD 解碼成果**；不能將私人 HTML 裡的 PNG 直接冒稱新從原 REAL 實解的證據。所有私人原圖與 HTML 仍僅私有，不上公開Git。

## 統一來源關聯、證據上限

逐一接[INTEGRATION25 181物品市場 ItemList 來源](../../research/recovered/STONEAGE-INTEGRATION25-ORIGINAL-2009-MARKET-SEVEN-SHOPS-SOURCE-R1.json)的12個 `TW1_INDEX_NOT_FOUND`，以**原物品表實際 ImageNumber**精確找到同後期社群保存載體 ITEM06 三個原 RD 資源號；十二種不同 ID 在七個原 ItemList 的**來源出現位置共13次**，其中 12221 既是蔬菜店的區間候選又是特產店明列值，兩種原依據不能去重抹平。

在**兩個嚴格分開的來源範圍**內，本市場原不同商品有圖像候選的資料關聯由原有的 **169個台灣1.0零售跨載體原 RD 候選**，再加上**12個這份混合2.5原 RD 候選**，而達到 **181/181 個市場原商品ID具至少一條來源限定原 RD 圖像候選**。這**不是**181幅不同原圖，不是原版可購買181種商品，不代表原版 1.0 圖索引原來就有這12個，也不證明它們在原商業市場 UI 真正被選用。

本輪原 `CURRENT` 完全不動，公開新物只有[十二項市場商品→三個真混合原圖源橋接](../../research/recovered/STONEAGE-INTEGRATION26-MARKET-12-MIXED25-ORIGINAL-PIXEL-BRIDGE-R1.json)、公開固定原來源 Git blob 重放與負例測試及 README 指標。真正的原生地圖繪製、調色板選擇、交易／價格、道具用途及跨版官方同部署仍 OPEN；先前 ITEM06 原415個 RD 不是此輪重復發現的新415個。

## 項目順序更正與 NEXT

本輪補做全倉查重後，確定**O70（四地47個原委託 ACCEPT 區段）與 O74（四地23個原寵物委託書商人、原 NPC 圖）早已完成來源受限整合**；先前 INTEGRATION25 驗收收據指向再次整合 `mission.create` 的文字 NEXT 應**被本條明確取代**，舊收據保留歷史，不覆寫或假稱新發現。四市場 `工作介紹中心` 的 ItemList `18563–18566` 亦早在 O74 列為分離來源，沒有證據足以重新發明原任務執行語義。**新的最高NEXT：停止市場與委託舊來源重掃，從模組全局選另一份真正尚未整合而有原件的原遊戲內容；只有取得新同版原運行選圖、交易實證或新來源缺圖，才重開這12件的實際選擇語義。**

Stage A仍 **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent仍 `null`。所有內容是 Stage A 來源保全／模組整合，不建新引擎、登入、商服或原版玩法虛構。
