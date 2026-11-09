# INTEGRATION18 / SCENE26-R4｜四間寵物常識解說員房間的來源限定復核

## 啟動與歷史前綴

本輪按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 從 GitHub 重新讀取主線。開始時 `main` HEAD `6f7e79f66643201b9164c6bd6c235d6e9f022824`，Git tree `43995d568b1f8476beadd5d7056ab3e284ffcd8f`，PR #285 已合併、同 HEAD 的 11 個主線 Actions 完成並成功。並確實從 Git blob 接口讀回 **`docs/CURRENT-STATE.md` 2,709,173 B**，其 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，普通 file interface 返回空值的情況未作為文件為空的依據。本輪不改寫該多兆位元組歷史前綴；本記錄與 README 是追加續接，不是替代 CURRENT。

## 本次可核的原內容聯接（FACT：限定於注明的來源）

與前一筆 [INTEGRATION17](STONEAGE-INTEGRATION17-THREE-PET-ROOMS-20261109.md) 相接，從現存原保存社群混合 2.5 的四筆 `sa60/newbie/newbie.create`、原 `sa60/newbie/petmaster`、MAP09 的四張原 DAT 與獨立保存的原圖來源收據交叉對照。這不是已認證臺灣 1.0 / JSS 1999 原始同服配置。

| 房間 DAT floor | 原建立座標 | 建立圖號 | 現代同距投影標記 | 原 AD​​RN 候選靜態圖左上角 | 原圖尺寸 |
| --- | --- | --- | --- | --- | --- |
| 1003 薩姆 | (19,15) | 16122 | (1104,616) | (1088,541) | 32×87 |
| 2003 漁村 | (11,12) | 16127 | (752,736) | (733,651) | 36×96 |
| 3003 加加 | (16,19) | 16122 | (1136,784) | (1120,709) | 32×87 |
| 4003 加魯卡 | (14,17) | 16122 | (1008,784) | (992,709) | 32×87 |

四個原 CREATE 各自獨立，不能把三處共用圖號 16122 合併為同一 NPC。四間在 MAP09 已取回原 DAT，候選合層 canvas 均為 1889×1425。原 16122 的 RD SHA-256 為 `70e97c406b2ac784a5b0e0cac7906ab8b044f6f4b9ebe14a92b4e727eb250022`；16127 為 `c461402ebd18a9e87277c083f4b62218f99133380b74c26278ef916836aaaeb1`。兩個原壓縮 RD 均已由 INTEGRATION17 實讀、雙解碼，並與獨立 CN50/PATCH129 候選塊 SHA 相符；本輪沒有重新取得該兩份 RD 的實際字節，不能冒稱重新解碼。

實際取回原私人 `StoneAge-SCENE26-R2-four-original-pet-tutor-rooms-private.zip`：2,532,646 B，SHA-256 `cf7d0d6dbb34fc77e64740f2d4990a0012a15a347bfb683e3cd1dc97eb02ca4c`。原 CREATE 與原 `petmaster` 文本由內部已存封裝直接回讀、完整 CRC 與 SHA 核對；`petmaster` 1,365 B / SHA `04ba49ba514eb469b4c12085c6733cd73c281c6ca682c813c2e35748ab6ac1db`。私人 HTML 只作**靜態教學資料查閱**，原 CP950 逐字保存，含 10 段原文字窗資料；原本的 `MESSAGE` / `LV>0` 設定不是我們實行過的原生互動。原字串不公開入 Git。

## 私人有限觀察：真正完成與仍缺的原像素

重用四張已驗來源限定房間圖，產生四間可直接查閱的私人離線觀察頁；取原配置的標記位置與 ADRN signed offsets，各畫出尺寸經 SHA 收據限定的**空心候選佔位框**。沒有把任意方框/剪影冒作原始 NPC 造型。最新能讀取的 R2、INTEGRATION17 和 WORLD11 私人 ZIP 都沒有解說員原圖號 `16122.png` / `16127.png`（或等價原 RD 真正圖片字節）。所以：

- **原像素解說員本輪實際放置數 = 0**；候選原圖 bounding box 四處，皆標註尚缺真 PNG。
- 可選來源檢查要求 **兩份**原 PNG 同時取得，逐 PNG SHA-256、完整解碼尺寸、RGBA SHA-256 對 INTEGRATION17，單件/錯件拒絕後才容許真圖私有疊加。
- 生成了私人 `StoneAge-INTEGRATION18-SCENE26-R4-PRIVATE-PARTIAL.zip`：3,753,771 B，SHA-256 `64eeff437d245a2bf7f40ac781c4a6279fc065de9bbd8acbe8a5ff904e645d56`，14 成員 CRC 全過，兩次生成逐字節一致。
- 已在 Chromium 用 `page.set_content` 加載同一 HTML 與四張原場景 PNG 的內存副本，四張 1889×1425 圖載入、十個文本項可查，0 JS 錯誤、0 外部 HTTP 請求。此環境直接導航 `file://` 被 `ERR_BLOCKED_BY_ADMINISTRATOR` 禁止，**不能聲稱本輪成功直接打開本地 file URL**。本輪私人 ZIP 已在會話容器保存，**已成功上傳個人 Library，並重新下載整 ZIP 驗 SHA-256 與全部 14 個 CRC**。

公開 JSON `research/recovered/STONEAGE-INTEGRATION18-SCENE26-R4-BOUNDED-TUTOR-LAYOUT-R1.json` 將上述四行和五個前置 Git blob 實際串起；`tests/test_stoneage_integration_module_18.py` 除來源 SHA/原座標/原圖幾何/原 DAT 外，會拒絕偷換圖號、位移、替換 RD 和場景指紋，也否定在缺圖時的原像素放置宣稱。公開 Action 驗證是**派生數據、非原圖私人重演**。原商業素材、完整對話、原 RD 和原 PNG 均不入 Git。

## 狀態、止點與下個有材料工作

**SCENE26-R4 = SOURCE_BOUNDED_PARTIAL（非原像素全部完成）**。下次只有取得來源可核、與上列 PNG/RGBA/RD SHA 逐項相符的 `16122` 與 `16127` 真正圖片字節時，才完成原造型接入。已有原畫面的其他三間 `3303/3403/4003` 寵物服務關聯可在原 DAT、MAP09 像素、CREATE、參數和傳送證據可復核時接續；3400 室外 DAT 缺件要明示而非造圖。優先做有實物的下一組，不為同一缺圖反覆擴大解碼工具。

原生對話觸發、原生 NPC 繪製層序/色盤/碰撞、原版商店或技能操作、官方同服部署及原生遊戲可玩仍是 OPEN。Stage A **7 PARTIAL + 2 OPEN**；Stage B 與 wiki **GATED**；R79 **PAUSED_NON_BLOCKING**；全體完成百分比仍為 **null**。Stage A 歷史忠實復原，不開始新引擎、網絡服務或現代遊玩優化。
