# INTEGRATION69｜被盜三件家寶：兩名原NPC、五件道具與臺灣1.0七幅真原像（2026-11-11）

## 新起點／有界目標

從 fresh GitHub `main=899c69e573e349ed404b8a3d1362c499cfad73f2` / tree `083cf8dc657c8f83bbc360c8890da2132b172436` 依連續性協議重新讀遠端分支、最新提交、全部26/26已完成成功Actions、README、原生 `docs/CURRENT-STATE.md` Git blob、歷史/來源/設計、路線/模組及INTEGRATION68正式驗收。原 `CURRENT` 是 **2,709,173B／blob `c89e0e33537990aa2132b47c40fef49a985a935c`**，本輪全字節保留。最新NEXT是換不同來源就緒、可恢復真正原版2D可見內容的地圖／寵物／道具／NPC，不重跑四村NPC原像。

此次切換為**後期保存來源的 event13「被盜家寶」整件任務的跨模組證據**：補齊此前未專題的兩原NPC配置、其同源原事件段與5原物品行，再把相應的**兩原NPC和五件物品**準確映射到認證**不同載體**臺灣1.0零售原ADRN/REAL真正原像。交付的是可查原版內容來源，不是猜情節、原場景遊戲或新單機引擎。QUEST01已有兩原腳本及5原TYPE的基礎索引，所以新增來源原腳本／TYPE發現**0/0**；新的是跨來源可見圖形及完整原關係的有界聯接。

## 真實復核原件、來源區分

- 私人保存後期社群 mixed25 原 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`：**995,176B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`**，2205/2205 ZIP CRC；真正抽取 `sainasu/event/event13n.create` (580B, SHA256 `05a2d1f95cdba5c2fba2918d3a11afe7375109a4af07d01e77a5a572ffb10bdf`)、`event13_1`、`event13_2` 及原 `jaruga/event/event.template` 全原CP950。所有原SHA、CREATE範圍、事件物理行和舊QUEST01/CHAR01固定索引核同。`changeevent→ExChangeMan` 是同保存原模板函數名，未執行原服。
- 私人原 ITEM01 兩套94欄原物品表研究包：**5,868,386B / SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa` /838成員CRC通過**。本輪依保存的私有94欄原行目錄逐項核五ID兩行的完整原行SHA、原圖號，未重開361MB混合2.5父RAR，**不得稱本輪重取父RAR原文行**。
- 私人原認證TW Waei/JSS1.0零售 `P3H.zip` **372,626,292B /SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`**；實際重新讀取全 `adrn_1.bin` **10,079,680B / SHA `47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8`**、`real_1.bin` **315,842,228B / SHA `408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13`**、Palet1原字節SHA `32870080c47537a59beaf770b6df7bd79820fd52a23825058460900494f0b4b0`。每圖按全索引 **原80字節ADRN最後+76的別名** 唯一候選，從真REAL指定原位置按原RD大小讀出；七圖均由兩套獨立RLE程序全索引逐像素完全同，現代候選PNG已目視，非原生調色板/選圖證明。

**資料邊界**：後期社群mixed25原NPC／物品資料與臺灣1.0官方零售圖像不能因此變成同一官服部署、1999 JSS首版或1.82初代任務。相同數字是已核源別名候選，不是實測原客戶端 `graphicname→bitmapno` 函數；原圖可見不等於原NPC真的以該外觀出現在該樓層。

## 這次真正接起的原遊戲內容

後期源 `sainasu/event/event13n.create` **兩條不同原CREATE**：

| 原配置 | 樓層/出生座標 | 圖號 | 原腳本 | 原資料動作 |
|---|---|---:|---|---|
| 老人薩頓 | 1112 (16,15) | 16000 | `event13_1` | 一條ACCEPT、一條REQUEST、兩條MESSAGE |
| 關懷老人的年輕人 | 1100 (86,99) | 16048 | `event13_2` | 一條CLEAN |

老人源ACCEPT事件13要求 **`NOWEV=13&ITEM=2428&ITEM=2429&ITEM=2430`**，原命令字面為 `GetItem:2450`、`DelItem:2428,2429,2430,2431`、`EndSetFlg:13`。老人REQUEST原等級門檻 `LV>15`、給原線索道具 `GetItem:2431*1`；另有 `NOWEV=13&ITEM!=2431` 取回線索的MESSAGE。**年輕人**另有原CLEAN條件 **`ENDEV=13`**／命令 **`CleanFlg:13`**。兩者同一事件號的互動優先級、清旗標時機、逗號DelItem含義、再次觸發和交易狀態都沒有原生實驗，不能因為看到CLEAN原命令就稱完成後一定清空、甚至陷入迴圈。原腳本條件、物理行、原段SHA和命令次序全保留機器收據。

同保存版兩原物品表中五ID **2428、2429、2430、2431、2450**，原短名分別為「薩頓家的衣服」「薩頓家的斧頭」「薩頓家的頭盔」「盜賊們的足跡」「薩頓家的秘藥」；十原行各ID雙表完整SHA相同，但**五是五個來源物品號**，不代表遊戲原本物品總數。完整私人原物品正文不公開。

| 保存版原來源別名 | 臺灣1.0原ADRN物理圖塊 | 原圖尺寸 | 源角色 |
|---:|---:|---:|---|
| 16000 | 5846 | 52×72 | 老人NPC候選 |
| 16048 | 5894 | 36×79 | 年輕人NPC候選 |
| 21028 | 6329 | 32×47 | 道具2428 |
| 20018 | 5991 | 36×38 | 道具2429 |
| 21540 | 6405 | 28×29 | 道具2430 |
| 24222 | 6716 | 28×39 | 線索2431 |
| 24169 | 6995 | 16×19 | 獎勵2450 |

**七幅全部是真正來源RD解碼重放**：兩NPC本輪重新讀原RD，五道具原本已由ITEM01源資格解碼，本輪從臺灣1.0全REAL再重解並與私有ITEM01先前保存的五PNG逐RGBA像素、原索引SHA、RD SHA、原ADRN逐80B SHA全部吻合（**5/5**）。PNG寫入方式可能造成檔案SHA差異，不能以新PNG序列化的字節不等誤判原像不一致；私有包保留五份舊已驗PNG字節。原圖候選Palet1不認證商服實際調色板。特別保留錯誤反例：實際物理圖塊16000/16048都存在，但與後期源 `graphicname=16000/16048` 對應的+76別名物理5846/5894不是同一RD，不能直接按數字取物理圖。

原樓層1112舊MAP09已有 30×30原DAT來源候選，整 SHA `e48585b8b02d646e53c3fa181175ba4b5b8954e1a341c9f72f66f50bececa840`；**1100在本955 DAT來源批次沒有匹配**，不能說原遊戲不存在1100；此次不重讀兩處原DAT、不畫可達路線、不冒稱人物已原生顯示／對話。

## 私人保管與公開停止條件

私有 `StoneAge-INTEGRATION69-event13-two-NPC-five-items-original-source-private.zip` **75,935B / SHA256 `054f01290d92f70fa36783c0273e99064d6e699a67fa098e7f141c70b893df47` / 31成員**，有原NPC/腳本、私有94欄源字段保存、七份原RD／原像候選、現代參照圖與純離線查閱HTML。已保存個人Library `/石器时代/`，又從另一工作目錄完整回取，原ZIP每字節及**31/31成員CRC全一致**。私有94欄行由先前驗證的源目錄重建，**非本輪從父RAR重提的原CP950行**；不混淆證據層級。原NPC全文、私有行字段、圖片、RD和HTML不進公開Git。

公開只交[數值／逐原件SHA／原像標識／反例與限制](../../research/recovered/STONEAGE-INTEGRATION69-HEIRLOOM-EVENT13-NPC-ITEM-TW1-PIXEL-SOURCE-R1.json)及可執行回歸；GitHub CI能驗已存公開來源目錄與數值，不取代私人原圖重放，也不能證明原商服玩法執行。此來源包達到 `SOURCE_BOUNDED_STATIC_VISUAL_JOIN` 止點，不擴任務模擬器或造商服地圖。

**狀態不變**：Stage A **7 PARTIAL＋2 OPEN**；Stage B/wiki **GATED**；R79 **PAUSED_NON_BLOCKING**，`overall_percent=null`。**NEXT：** 離開 event13 和已完成INTEGRATION68四NPC，選其他實物支持、未重複的原寵物／技能／道具／地圖及跨模組內容；無合格原件才明確停，不能做賬號/網服/新引擎或體驗優化。候選／PR／main Actions結果只能依其真實運行後另行驗收，本文不預支成功。
