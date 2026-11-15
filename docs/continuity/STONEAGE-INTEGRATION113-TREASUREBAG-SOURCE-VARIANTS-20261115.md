# INTEGRATION113｜迷宮「寶物袋」兩套原NPC來源、同位衝突與真實寵物動畫候選（2026-11-15）

## 精確續接／新研究對象

按連續性協議重新讀 GitHub 遠端 main `7cd3601bfe0fefd2861bfbc964b1e23b8a85812e`／tree `d6700ad0bbea95cbcac013915581ddd6c03e11b8`，精確HEAD 26/26 Actions 完成成功、零開放PR；連續性文件與完整歷史 CURRENT 原生 Git blob **2,709,173B／`c89e0e33537990aa2132b47c40fef49a985a935c`** 保留不改。上輪 INTEGRATION112 已驗收，不再擴其三條盜賊來源。

本次**真正新增的業務關係**：舊 QUEST19 已記錄 `extra/event/marju.create` 中 **10個以 `changeevent` 連動切繩石2697、`NpcWarp` 和 `GetRandItem` 的寶物袋**；現在從同一後期社群保管 `mixed25` 的另一個**獨立原配置檔** `100/sb_mimi.create` 真正核出**另外12條 `NPCEnemy` 來源配置**，並識別兩套原配置在同一座標的源衝突。**這絕不表示原遊戲同時出現22個袋子**，也不證明兩套都曾載入同一伺服器。

## 真原件、源對照與重要異文

重新回讀私人 `StoneAge-CHAR01-mixed25-all-npc-original-private.zip`，**995,176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`、2,205/2,205 ZIP CRC**；實取 `100/sb_mimi.create`、`100/sb_mimi.template`、`100/sb_mimi.arg`、`300/sb_hag.template`、`300/sb_hag.create`、`300/sb_hag.arg` 及 `extra/event/marju.create` 共**七原文件**，尺寸／完整源SHA／原成員CRC對既有CHAR01逐文件一致。12段 CREATE **依實際原二進位位移切片**重算完整原塊SHA，12/12對既有源索引相同。 `300/sb_hag.create` 的一段原註釋／名稱含不能嚴格CP950往返字節，原位元組與原SHA不改、不用修復後文字作證；`100/sb_mimi.arg` 的條件參數可CP950無損回編。

12配置中，**floor122六處**： (78,102)、(78,96)、(93,152)、(45,152)、(120,145)、(162,12)；**floor118六處**：(75,9)、(129,165)、(207,99)、(189,69)、(99,15)、(81,15)。圖號字面全部 `16073`，原短名「寶物袋」，原來源內各只有一個 `100/sb_mimi.arg` 精確引用。原ARG有 `entype:2`、`item:2697`、`time:60`、`dieact:0`、十次重複 `enemyno:1117`；原短句提及切繩石與袋中恐龍，**不證實原native切袋、真正消耗、掉落物、機率或戰鬥結果**。

最需保留的原文字段差異：12段 `enemy` 的**函數名都為 `sb_hag`**，其原模板唯一命中 **`300/sb_hag.template`**，而同目錄另有 `100/sb_mimi.template`、模板名 `sb_mimi`，在CHAR01全4985有效CREATE中該 `sb_mimi` 函數名**零引用**。對應 `sb_hag` 函數名則共13筆（本12筆及300目錄1筆）。12段原 `graphicname=16073`，跨目錄 `sb_hag` 模板原 `type=100329`，不能私自聲稱原native選擇哪個繪製欄位、源關係為錯碼或有修正優先級；CHAR09舊索引已正確保留跨目錄匹配，**並非推翻CHAR09**。

與[舊QUEST19](STONEAGE-QUEST19-MARJU-POST-TREASUREBAG-SOURCE-20261108.md)原十袋逐座標比較，**唯一精確重點**是 `floor122 (162,12)`：本組原CREATE第5塊與原腳本 `extra/event/marju04a` 在同一出生座標、同圖號 `16073`，卻是不同的 `NPCEnemy` 與 `changeevent` 靜態來源。其餘位置不同。舊 QUEST19 使用原 `ITEM=2697`、`GetRandItem`／`NpcWarp` 等條件；本組 `item:2697` 是不同ARG語法，不能假設兩者等價或同時生效。已保存 MAP09 118(250×180)／122(300×200) 原DAT SHA足夠核位置界限，**本輪新讀原DAT=0**，不執行碰撞或場景。

## 新的寵物／敵人來源關聯，與原像素的分界

既有同社群存檔CHAR09原敵人表證明 `enemyno 1117` 可數值連到**敵人模板3／圖號100252／同源SPR索引242／原頭動畫數56**；但此敵人ID於原兩套敵人實例表的原完整行SHA**不相同**，兩原模板行SHA亦不相同，不能擇一宣稱為唯一運行參數。先前 SCENE28 私人原像研究獨立取自**正規台灣1.0零售客戶端**的SPR組100252：整SPR段SHA `eeb2ec4546277c2acdf1b43fff7967c4c0fe5ac5c019bb7d68a901e134691b0a`，8方向action1／16幀位置和相關真原RD像素已被獨立驗真。這個SPR段已與先前保存社群源對照為**段位元組相同**，但不表示跨版本真像素、配色、召喚角色、敵人名字、伺服器同部署或「袋中恐龍」物種已證成。

本輪另直接回讀私人 `SCENE28-private-original-TW10-pet-action1-observer.zip` **347,996B／SHA256 `f707d196acb6c449e2b6b11345a02db36ac6726131ce51f9a93587b32c3ad492`／3/3CRC** 並核SPR100252保存源收據；**未重新取得整個372MB P3H零售原包，亦未再讀新原RD像素**。原圖、動畫、完整原商業腳本和私人HTML不入公開Git，不創造第二套查看器。

## 來源結論與下一個止點

[可機讀原文件 SHA、12原字節段、兩方案座標比對、原敵人數值與負證](../../research/recovered/STONEAGE-INTEGRATION113-TREASUREBAG-VARIANTS-ORIGINAL-SOURCE-R1.json) 與相應正反測試只要求公開已固定的CHAR01／CHAR09／QUEST19／SCENE28來源收據，CI不能取代私人原件復讀。這是兩個來源配置族的**實際互斥可能／重合風險**，不是已證同時生效、二選一機制，亦不是早期台灣1.0或1999商業玩法。

Stage A **7 PARTIAL＋2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，整體`overall_percent=null`；歷史CURRENT完全未改。PR合併與候選/主線Actions必須依其各自精確SHA真正後驗，不能預支。

**NEXT：** 此寶袋雙配置族止於來源衝突和有限可見圖像候選；改找不同來源、真正新增且獨立合格原二維、寵物、場景或實質玩法規則。缺資料即保留UNKNOWN，不建新引擎/帳號/原網服。
