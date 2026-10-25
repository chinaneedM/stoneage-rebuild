# 《石器时代》R19：台湾 1.0 原程序繁体短文本原字节取证（2026-10-25）

## 启动校验与连续性

本轮启动时重新核对远端主分支 HEAD `33931b2b9dc9b02f2cba4a6dd6499141bf24c7fd`，tree `2858c6a4b4ba945b383e4d645c342682976c9a22`，最近提交及R18主线实际成功Action `40202008184`，完整连续性协议、README、路线与22域作品集。原 `docs/CURRENT-STATE.md` 完整Git blob `031c76a5a8e431f646853909bb2f2e11e6328cd2` 已重新读取并保持原样；本记录是协议第14节要求的**加法连续性补记**，不是CURRENT正文替代，也不覆盖R16–R18先前事实。

## 这次取得什么真实物件

已接受的台湾 Waei/JSS 1.0 Redump 104630历史客户端，来源作业 [40203596474](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40203596474)（源HEAD `03572bbec4b80660a244dcc9fe4f2ad7370ccf57`）完成从经验证的历史 `CD_DIC.rar` 实际取源，先核对源包既有原哈希、`STONEAGE.bin` 长度，再从只读原客户端抽取两个文件：

- `StoneAge/sa_3.exe`：425984B，SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`；
- `StoneAge/StoneAge.exe`：409600B，SHA256 `9b280068063b4398e5c8901b881daa1f13576201e475efede3127b59cdad2867`。

这两条原身份与原台湾1.0客户光盘 `research/recovered/STONEAGE-TW10-CLIENT-INVENTORY-R1.txt` 一致。原程序、图像和整个原商业包不入Git；Action最终销毁临时包。严格扫描PE的非执行、文件字节落地 `.rdata/.data`，不再把 `.text` 指令当汉字串；只记录NUL终止、严格汉字且不长于12字的cp950/gb18030/cp932候选。启动器13次纯汉字候选解码（其中cp950 10），主游戏181次（其中cp950 172），后者仅保留首24条，**绝不算13或181个游戏实体/菜单全集**。有些gb18030对同一原字节的替代解码是乱码；只有明确验证的CP950短标签可以作为下面的原字节例证。

### 可重放源字节见证

| 原文件（文件内十进制偏移） | 原短文本（cp950解码） | 原字串SHA256 |
|---|---|---|
| StoneAge.exe 205156 | 下載失敗 | `aa1bef9edd02ece4033cebca06a18bd208ca0cc52358bda2563ff6cdd65bc1d9` |
| StoneAge.exe 205908 | 啟動石器時代 | `0edf869b6def5df7145ec868a8db608ee752270d3d85de4616a9ccc8df2a1baf` |
| StoneAge.exe 206416 | 連線發生錯誤 | `614013b7a9c88048092f58a2dcb42c4a9891009a818719d4a2030f3c71441830` |
| sa_3.exe 351900 | 戰場地圖錯誤 | `f0c8c6b9e7ac2ef55baf93dc9f924ace68c21bc33941a05e3cc6781a8b2db02e` |
| sa_3.exe 352068 | 沒有參戰的寵物 | `ddcaf5c913d56debb45c1ec79fa72166d9c6663342c702a6ba5d3641e5980865` |
| sa_3.exe 352260 | 出其不意的攻擊 | `33832b28c9e6b99133f5cb1777998fb18b80f18014f9f72cfdda1b2c9615ad38` |
| sa_3.exe 353636 | 關閉動作視窗 | `f23bd0cd1c963ebfbaabf73336218c2a4ddae62e67ba8d0b7ca6159aead4b38a` |

每项原文件偏移、来源PE段、字节长度、短字串SHA以及双解码身份保存在 `research/recovered/STONEAGE-TW10-ORIGINAL-EXE-TEXT-CANDIDATES-R19.json`。原来源作业格式标准JSON的SHA256固定为 `66bef73e28bfc8c2cda25d8a1b3a48c62dc1d90a7dc20be452931e03ab7d161c`。独立Guard还要求CP950重新编码与上述SHA逐条吻合，并与原客户端原文件清单相互核验。**这证明原可执行程序数据段存在这些繁体字串，不保证原UI实际何时显示。**

## 失败历史、证据边界与最高NEXT

源分支首跑 [40203057866](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40203057866) 原档案及两EXE鉴真和7离线测试成功，但输出超50KB硬上限而**失败**，未形成产物。第二跑 [40203254181](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40203254181) 修订大小后成功，然而误扫机器码产生2592次看似汉字的解码，人工复核明显混杂乱码，故未认可实体或界面。第三跑 [40203596474](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40203596474) 通过真实PE非执行段筛选而成功。失败不隐藏，也不能把候选数当游戏内容总量或恢复百分比。

已恢复的是台湾1.0原程序**短文本字节证据**，不是原服务器主表、NPC名字、具名宠物、成长值、宠物模型关系、已部署场景/地图缓存、完整任务、实际登录界面或完整战斗规则。四类任务边界 `BASE_GAME_QUEST`、`PERMANENT_VERSION_QUEST`、`OPERATOR_EVENT_QUEST`、`ORIGIN_UNRESOLVED` 不变。Stage A仍为7 PARTIAL/2 OPEN；Stage B与百科GATED；TW1本地savedata R79暂停；原大包持久保管暂停；总体百分比未知。公共Git只载元数据与极短例证，绝不载版权二进制/原对白语料。

最高下轮任务 **`EARLY-OFFICIAL-WORLD-ENTITY-SOURCE-20`**：寻找实际可取回、可哈希鉴真且有同版原始载体的早期官方NPC/宠物/游戏本体任务主表、原服投递或原版地图缓存，尝试唯一名字→实体ID→原图/SPR组号的可重放联接。没有真实原件即保持OPEN/null；先审已有归档排重，不反复下载同原程序/社区混合2.5/论坛断链，不延长字符串helper链。下一会话必须再次先读远端实际HEAD/tree/Actions、整个CURRENT及本补记后再行动。
