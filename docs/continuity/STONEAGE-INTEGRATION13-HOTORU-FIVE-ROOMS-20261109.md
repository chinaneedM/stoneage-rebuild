# INTEGRATION13｜霍特爾五間室內的原房名、門點與配置

從 GitHub main `8ff246e5cccc08599314472e3aaa52b8dd197a9f` / tree `3e88d9f37f56cebea68a931bc5fd3d9449345e1a` 續接。當時遠端 932 分支、7,548 檔案、零開放 PR，同 HEAD 的 INTEGRATION12 [專項 Actions](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42560625726) 成功。讀取並驗證完整 CURRENT 歷史 2,709,173 B、Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`。本增量接續 README 已採用的日期覆層，保留 CURRENT 歷史全文。

## 原始資料與五間房

重讀後期社群混合 2.5 保存 RAR，361,255,180 B，SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。RAR4 獨立掃描 7,952 個文件標頭並驗 CRC，libarchive 取出 22 個目標成員，再逐成員對原大小/CRC。NPC、模板、參數另對 CHAR01 與 R18 的 SHA。五原 DAT 從 MAP07 與 INTEGRATION11 的兩份私人歸檔逐字節核同，20 條原傳送記錄逐行核 SHA、方向與雙端 DAT 格值，與 INTEGRATION11 既有證據一致。

| 地圖 | LS2MAP 原名 | CREATE | MAP07 候選圖引用 | 具體來源 |
| --- | --- | ---: | ---: | --- |
| 1301 | 霍特爾的武器店\|0 | 4 | 156 | 兩個 ItemShop、兩個離開門點 |
| 1302 | 霍特爾的道具店\|0 | 6 | 157 | 四個商人配置出現位置，含兩份配置的同格記錄 |
| 1303 | 霍特爾的寵物店\|0 | 11 | 165 | PetShop、PetSkillShop、TownPeople 及六個 `npcgen_mugon` 配置 |
| 1304 | 霍特爾的肉店\|0 | 3 | 141 | 限制商店模板指向 ItemShop；物件層有 60 格差值 |
| 1305 | 霍特爾的醫院\|0 | 5 | 209 | WindowHealer、ItemShop、TownPeople 及兩個離開門點 |

五份原地圖均 30×30。1302 的 `(12,15)` 由 `shop_m.create#106` 和 `shop_m2.create#118` 各指定一次，兩個原塊 SHA 不同，圖號與原參數檔相同。保留二者，實際載入哪份配置待驗。1303 的六條 `npcgen_mugon` 模板功能欄為空，保留原圖號及位置。1305 醫療配置的尾部數值為 `10|1.3|2.6|2`，首輪通用檢查把它當作只接受文件參數而停下，核原字面後按數字格式保存，數值語義仍待證。

五張 DAT 與同保存載體 LS2MAP 的首層逐格相同。1304 第二層 60 格為伺服器值 2、客戶端值 0，其餘四張第二層逐格相同。LS2MAP 為兩平面大端 u16，DAT 為三平面小端 u16。兩層差值僅描述原文件。

## 私人觀察與公開驗收

五張原 MAP07 候選底圖保持 PNG 字節和解碼 RGBA 完全一致，共 828 次既有候選引用，新增原 RD 解碼與底圖重繪均為零。私人離線頁加入五間原房名、28 個座標標記和 29 條逐配置查閱列，同格顯示兩個序號。來源是後期社群保存資料與另存臺灣 1.0 候選像素。原生 NPC 外觀、原生碰撞、門點執行、成交和官方同部署待證。

私人 ZIP 2,867,302 B，SHA256 `c4cb208810a8ae0ad1ad76f59f3569f2f19b8bfd0389fe71aa6d3ffa91ff44eb`。保存後另行取回，獨立驗整檔 SHA、34 成員 CRC、27 原成員大小/CRC/SHA、五張 MAP07 PNG/RGBA 和 29 條配置源格。私人 HTML 結構與標記數已獨立驗證，未以原客戶端或瀏覽器重放。公開只收[派生源資料](../../research/recovered/STONEAGE-INTEGRATION13-HOTORU-FIVE-ROOMS-SOURCE-R1.json)、生成工具與六項資料測試。原商業字節與私人觀察包分開保管。

**NEXT INTEGRATION14**：霍特爾本組七間室內已具來源限定資料。沿 1301/1302/1304/1305/1310 原 ItemShop 參數，優先核主表、備用表和既存 ITEM05 所見的同一項實際物品差異。只接可證配置、物品表和已驗候選圖，對既有資料查重，保留哪份表實際生效與交易未證的界限。Stage A 為 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 暫停，總體百分比未知。
