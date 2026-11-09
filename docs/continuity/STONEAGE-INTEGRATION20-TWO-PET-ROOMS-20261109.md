# INTEGRATION20｜3303、3403 原 DAT 房間實際補回，3400 源件邊界釐清

## 遠端起點與實物

從 GitHub `main` `59a8b2a837c38a7077790aba62bd84bdd346c70b` / tree `d1fa75e34fa13a1e11b16587379ede12a0213cc4` 依連續性協議重新啟動。同 HEAD 的 11 項 Actions 全部完成成功；PR #287 已合併。重新經 Git blob 取回 `docs/CURRENT-STATE.md`，完整 2,709,173 B／blob `c89e0e33537990aa2132b47c40fef49a985a935c`。**本次只加新來源記錄與 README 指針，不截短也不改寫歷史 CURRENT。**

真正取回私人 Library 根目錄兩份原封裝：`StoneAge-MAP09-691-source-ready-map-catalog-private.zip` 46,844,444 B／SHA-256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a`，4195 成員全部 CRC 通過；原社群保存混合 2.5 RAR 361,255,180 B／SHA-256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，整檔符合 MAP01／R18。從 MAP09 內層 955 份完整原 DAT ZIP（SHA-256 `c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a`）實取 `3303.dat`、`3403.dat`、`3300.dat`，各整 SHA 與 MAP04／MAP09 完全相符。此前 INTEGRATION19 的「本輪只有索引」不再適用於 **3303／3403 本次私人來源實讀**，原舊收據本身不改。

從同一原 RAR 另以 libarchive 抽取 `jyaruga/ururi/3303` 與 `jyaruga/kikuku/3403` 的 **原 LS2MAP 各 3644 B**，分別整 SHA `df8405a9f2552c1a21983256e65054eb368994a9dfe7419ad9878ea9e13f9b3e`、`0a09df92ca18eee6f88020e8f93e72182a449d8621ca9a31c728ed8dd0c65618`，原 RAR 目錄 CRC 與原頭、CP950 房名、30×30 及兩層大端 u16 均核實。

## 兩間原室內的圖像／NPC／門點整合（來源限定 FACT）

| 原房間 | 來源 DAT SHA-256 | 原像素候選繪製位置／不同圖塊 | LS2MAP vs DAT 第一／第二層差值 |
| --- | --- | --- | --- |
| 3303 烏魯力的寵物店 | `785799faa3e1cf9de1b92809e8688e172e47b37ab72eb10924e00cddd98e473b` | 101／44 | 0／256 |
| 3403 奇喀喀的寵物店 | `0f6ecf597a7bf969d6e4e769081467ac1228e01ed6583c8d5ae50d031f8dad95` | 162／45 | 0／32 |

第一層 900 格全同，第二層所有差格皆為原服務端 u16 `2`、原客戶端 u16 `0`。只保存**兩來源原值不同**，不直接宣稱原碰撞／遮擋／可通行含義。由完整原 DAT 的數字引用及 MAP09 已驗台灣 1.0 RD 像素候選重建兩間 1889×1425 全畫布，每間第一層／第二層／合層三幅。Pillow 與 NumPy **獨立繪製全 RGBA 像素逐字節相等**，亦各自對 MAP09 舊收據三個 SHA 同值；既非新發明的原圖，也非原客戶端原生圖像路徑。

重新讀取原四筆 `genout/shop_m2.create` CREATE (#56、#59、#69、#72) 與四份 CP950 原參數，逐建立區塊 SHA／源圖號／角色／原座標，與 GAMEPLAY03／05 和 INTEGRATION19 公開數值索引一致。本輪另外實讀原三平面格：

- 3303 PetShop (16,14) `[5002,0,49152]`；PetSkillShop (13,14) `[5000,12631,49152]`；(15,20) `[5115,0,49155]`、(16,20) `[5116,0,49155]`。
- 3403 PetShop (18,18) `[5019,0,49152]`；PetSkillShop (18,14) `[5001,0,49152]`；(15,21) `[5025,0,49155]`、(16,21) `[5026,0,49155]`。
- 3300 已驗原 DAT 的 3303 出店目標 (51,60) 是 `[2023,0,49155]`，不等於門點實際傳送成功。

重讀對應原 mapwarp 和獨立 `Warp` CREATE：3303 有 3 條有向、3403 有 4 條；3303 (16,20) → 3300 (51,60) **明列出店而未列此點的反向進店**。3400 室外目標 DAT 缺完整校驗，不擅補其格數值。

3403 寵物店 CREATE 圖號 `16033` 有同保存混合 2.5 原 RD／PNG／RGBA SHA、36×81 及 ADRN 偏移 `(-16,-73)`，本輪第一次在**3403 完整私人候選場景**上放入該真原靜態圖，並附顯式可關開關。3303 的 16218／16212 和 3403 的 16018 真圖缺件，不畫假 NPC。本次按數字同號與不同載體來源建立的是**現代私有候選叠圖**，不能證明原客戶端當時正確選擇、層序、色盤或官方同部署。

## 3400：原 RAR 有 DAT 條目，不等於目前取得合格 DAT

MAP09 955 份驗證原 DAT **不含** `3400.dat`。追查完整 RAR 目錄確認確有 `stoneage2.5/map/3400.DAT` 這個 86,408 B 原成員，RAR 頭 CRC `7e5f34db`，但本環境 libarchive 在該段回報 CRC/讀取錯誤，**不能宣稱已得完整可靠三平面 DAT，更不能據此斷言原 RAR 全體物理損壞**。

另在同原 RAR 的 `SACH-MX0.30/MAP/3400.MAP` 成功提取**獨立原 .MAP**：28,808 B／SHA-256 `5145335b11bf8b0ae03c7634b6dacc471220c42946da76a17016fb7a95d46bbd`／CRC `8b6c3b59`，其頭是 120×120，後面只有 14,400 個 u16 位置（單平面形式）。**該 .MAP 與三平面 .DAT 是不同來源類型**，不可把它偷補為 3400 走圖、出口格或碰撞。上輪「3400 不在 MAP09」的限定仍真；更準確的新表述是「母 RAR 有未通過驗收的 DAT 成員，另有可驗單平面 MAP」。

有限檢查原 RAR 巨大的 `adrn_15.bin`／`real_15.bin` 時，本環境 libarchive 對某段報 `Parsing filters is unsupported`；未取得新原人物原 RD，不把解壓器受限當成歷史資產缺失或再擴展 RAR 工具工程。

## 私人觀察與驗收

新私人 ZIP：`StoneAge-INTEGRATION20-3303-3403-ORIGINAL-SCENES-PRIVATE.zip`，2,585,668 B／SHA-256 `2403ea2ee5928fba93de8b8913859b403d20e449049cfbba19a28ca237f31abb`，101 成員 CRC 全通。內含兩間房各三幅原來源候選畫面、原 DAT/LS2MAP、驗證過的有限原 NPC／傳送原文、16033 原圖／RD、3400.MAP 輔助材料以及離線 HTML。**原商業字節只在私人 Library** `/石器时代/StoneAge-INTEGRATION20-3303-3403-ORIGINAL-SCENES-PRIVATE.zip`，已上傳並獨立重取全 ZIP 逐字節／SHA／101 CRC 一致；公開 Git 僅保存哈希、數字、来源邊界與測試。

本機 Chromium 直接 `file://` 受 `ERR_BLOCKED_BY_ADMINISTRATOR` 阻止，不假報成功；改用 **HTML 原結構與真 PNG 原字節以 data URI 代入的內存副本** 驗六個圖層、3403 真圖開關、兩房標記開關，0 JS 錯誤、0 外部 HTTP/失敗請求。此測試**不是原商業原客戶端執行**，也未驗買賣、學技、碰撞或原生傳送。

[公開來源派生收據](../../research/recovered/STONEAGE-INTEGRATION20-TWO-PET-ROOMS-ORIGINAL-SOURCE-R1.json)及原資料反例契約 `tests/test_stoneage_integration_module_20.py`：GitHub CI 僅重放可公開的源哈希／數值與反例，不宣稱執行私有素材。

**止點／NEXT：** 3303／3403 原 DAT、原 LS2MAP、整圖像候選與源功能／門點本輪 SOURCE_BOUNDED_PARTIAL 收斂，不再反覆重畫。只在新取得能完整解壓且 CRC/整 SHA 驗證的 **3400 原 .DAT**、同來源 16218/16212/16018 等 NPC 真 RD，或其他具來源的新原像素實物時，增量重開缺件。否則轉下一個有材料且尚未整合的 Stage A 內容家族；不做網服、賬號、引擎、體驗優化。Stage A 仍 7 PARTIAL + 2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；overall_percent=null。
