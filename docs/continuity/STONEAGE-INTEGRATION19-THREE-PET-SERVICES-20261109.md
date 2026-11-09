# INTEGRATION19｜三間寵物店原服務、十一條有向門點、4003 原格與來源候選畫面

## 新鮮遠端與歷史前綴

按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重新讀取 GitHub 原遠端：起點 `main` HEAD `0df67b01fbba90d0792c8b75ffc09667e3776e27`／tree `a38cc8e78d39839e1f5b6ecc06c2a844acf519b1`，同 HEAD 11 項主線 Actions 均完成／success。歷史 `docs/CURRENT-STATE.md` 從完整 Git blob 讀回，尺寸 2,709,173 bytes，blob `c89e0e33537990aa2132b47c40fef49a985a935c`。**完整歷史原樣保留，本檔與 README 是日期追加，絕非覆寫 CURRENT。**

本工作屬 Stage A 原版內容復原，不是新遊戲／原伺服器重建。CREATE、服務參數、mapwarp、DAT 為後期社群保存 mixed25 原件；4003 可見圖塊是另存的臺灣 1.0 零售原圖候選。兩組來源**不能合稱 JSS1999 或臺灣 1.0 同服**，任何源字段只報原字面，不代表原版交易或教學有運行。

## 六條原 CREATE、原參數與版本來源

重新從三份已存私人 ZIP 逐完整 SHA 與全部成員 CRC 復驗：CHAR01（995,176 B／SHA-256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`）、INTEGRATION17（2,546,139 B／`c98770de851d0ba704e1a4c8f18d364c4f2a87c3746ec717953fd88c4930c93f`）、SCENE26-R2（2,532,646 B／`cf7d0d6dbb34fc77e64740f2d4990a0012a15a347bfb683e3cd1dc97eb02ca4c`）。原 `genout/shop_m2.create`（20,544 B／SHA-256 `ef0447f668939f9257f62467d1a6194d34955e22ab7e334aa232865127905651`）中的六個區塊逐原 ordinal / SHA 比較 GAMEPLAY03/05；原參數六份逐件 SHA 對照，原 CP950 字節只私人保存。

| floor | PetShop 原 CREATE：座標／圖號 | PetSkillShop 原 CREATE：座標／圖號 | 原技能 ID 順序 | PetShop 欄差別 |
|---|---|---|---|---|
| 3303 | #56：烏魯力的寵物店 (16,14)／16218 | #59：飼育員 (13,14)／16212 | 0,1,2,3,50,80,100 | `pool_flg`、`pool_cost` 未列 |
| 3403 | #69：奇喀喀的寵物店 (18,18)／16033 | #72：飼育員 (18,14)／16018 | 0,1,2,3,50,61,130 | `pool_flg`、`pool_cost` 未列 |
| 4003 | #82：寵物店 (13,13)／16038 | #85：飼育員 (18,15)／16207 | 0,1,2,3,10,50,100,200,201 | `pool_flg=1`、`pool_cost=200` |

三 PetShop 原拼字均為 `nomal_rate=1.0`，`special_rate=1.5`，`special_pet` 欄存在但空白。三技能店 `skill_rate` 原字面依序為 `1.1`、`1.2`、`1.0`。原文件名、欄位缺席、原字串均保留；**不推出金額單位、實際費率、教學成功或 NPC 可操作性**。

## 有向傳送：mapwarp 與獨立 CREATE 雙來源核對

在 SHA-256 `b7b50f42efa8e5a3f740d49a8d0c01cbf994d1bb66151b16ff5b5e7c14e7595c` 的 `mapwarp.txt` 精確重取行 664–667、735–737、752–755 共十一條，並對 `genout/warp_y2.create`（19,522 B／SHA `a2e60d39af1d008b1f1d3c8d084cfdf36ad275c896a83895b4c295531a361352`）獨立各 CREATE 區塊原坐標、方向及 SHA；**11/11 一一相符**，不是把文字中的 `↔` 自動展開。

- 4003 (10,15)/(10,16) 與 4000 (99,72)/(99,73)：兩組各雙向原記錄，共四方向。
- 3300 (51,60) → 3303 (15,20) 與逆向；另 3303 (16,20) → 3300 (51,60) 有獨立原記錄，**從 3300 (51,60) → 3303 (16,20) 的逆向未列**。一方向不能憑鄰格補造。
- 3403 (15,21)/(16,21) 與 3400 (53,49)/(54,49)：兩組各雙向原記錄，共四方向。

原 Warp 記錄不等於原客戶端碰撞、進門觸發已實測；3400 室外 DAT 在本次可取私人包沒有原字節，不能宣稱原生走圖可行。

## 4003 全原 DAT 取格和有據離線可見畫面

原 4003 DAT 實讀 5,408 bytes／SHA `0a9fa2a089b6936e86eea458bca464038b8d5cb7fee057b9d2b393ffc6c6d6d4`，原三平面 u16：PetShop (13,13) 是 `[5002,0,49152]`，PetSkillShop (18,15) 是 `[5000,0,49152]`，獨立常識解說員 (14,17) 是 `[5002,12802,49152]`，兩個房內門點 (10,15)/(10,16) 分別是 `[5024,0,49155]` / `[5013,0,49155]`。這是**原格值，非碰撞定義**。三個角色有三條獨立原 CREATE，不能因同房而合併。

從 SCENE26-R2 私人原包核 1889×1425 候選底圖 PNG，完整原來源候選 RGBA SHA `4512cdc85c6973d775efcd1d53ada6732bf023ef559f1baa6182a7b146d3722e` 與 MAP09 匹配。現代資料標記可切換，原 NPC 16038/16207/16122 實際像素**沒有**放入此圖；不得說成原客戶端已顯示。從 INTEGRATION17 真正取回 16033 的原 PNG／RD 索引候選，PNG SHA `db1398accb72f8423f0333f7111d78b99e936e1aa1ca3395e58bcbf809bb10a3`、36×81、RGBA SHA `17588f01cf524ed3eb5631884d6779c91685cce75c773563a80294167ce8b652`；它僅在 3403 **資料卡**獨立顯示，**未**偽造 3403 房內合層。

公開 MAP09 已對 3303/3403 各有源 DAT 全 SHA、三平面影像候選 RGBA 指紋；但本輪個人私人原件**只有 4003 原 DAT／全候選圖可重新讀取**，未重新讀取 3303/3403 兩個原 DAT 的完整字節及原完整畫面。明示這兩間為 **INDEX_AND_PARAMETER_ONLY_THIS_UNIT**，不造背景、缺失的其他五張 NPC 原像素亦不補畫。

## 私人交付與止點

新 `StoneAge-INTEGRATION19-THREE-PET-SERVICES-PRIVATE-PARTIAL.zip` 534,764 B／SHA-256 `2ac6d2e3502f25c87a06520287f41b971212e4850636acec5e644102c4d1c91b`，16 成員完整 CRC；原腳本/參數、DAT、私人 PNG、離線 HTML 只在此包。原字節重放兩次整 ZIP 一致；HTML 引用的兩張圖都在包內。已存個人 Library `/石器时代/StoneAge-INTEGRATION19-THREE-PET-SERVICES-PRIVATE-PARTIAL.zip`，獨立取回整包 SHA/CRC 同值。當前環境 Playwright **缺 Chromium 二進位**，沒有做真瀏覽器執行，不能聲稱 JS 在瀏覽器中已驗；已做源素材、解碼圖、靜態 HTML 引用及整包測試。

公開 Git 只存 [來源限定數值索引](../../research/recovered/STONEAGE-INTEGRATION19-THREE-PET-SERVICES-SOURCE-R1.json)、專項反例契約、此日期續接及 README 指針；不放受版權約束的原圖、原 DAT 或全文。CI 也只檢查公開派生資料，不能冒稱本地私人重放或原遊戲運行。

**NEXT：** INTEGRATION19 本批達到來源限定止點。僅取得可按來源 SHA 驗真的 3303／3403 原 DAT、完整可見畫面、3400 室外 DAT、其它缺失 NPC 圖像時再增量重開；若不可得，按最新整體內容佇列選擇下一個有實物的 Stage A 模組，不擴泛用 RAR/動畫/網服 helper。Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null，單機離線復原方向不變。
