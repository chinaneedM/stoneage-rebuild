# 台湾1.0原地图编号与地形碰撞属性的可认证来源边界

2026-10-18，`TW10-MAP-CONTENT-ORIGINAL-RESOURCE-BOUNDARY-01`。此工作包**不是地图恢复成功证明**：原台湾1.0零售盘 field_map_disc_files=0，地图场景数据通过原客户端 `M/MC` 服务器协议进入 `map\\%d.dat` 本地缓存。源字节的相关调用链、缓存读写动作已经在 `research/clients/STONEAGE-TW10-RECEIVE-MAP-LINEAGE-R1.md`、`STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt` 证明，今轮复核而不另称新发现。

新可执行任务基于真正同构建原盘 `COLLISION-ATTR-R1.tsv.gz`，它是原 `adrn_1.bin`（每记录80字节）导出的map_number、bitmapno、hit_raw、atari_x、atari_y、height_flag等元数据；9286个独立非0地图号，3处原文件的重复map number以源顺序最后一条为准（已去重的导出表不再能复算那三个碰撞来源）。

**本轮新增关系**：玩家2001年文献中对位图号1—4574“小地形格”、4575—5845“大地形物件”、5846—5946“NPC”等分类，仅作为来源级别C的候选**位图号区间**。原脚本 `tools/stoneage_tw10_map_content_collision_crosswalk.py` 用真正原版map_number→bitmapno行与这些候选区间作精确关联，按原字段输出hit/priority/height/碰撞占格分布及可复查的原始map_number。未落在这三段内的原碰撞条目保持“其他”，不将其丢弃或改判为新NPC身份。

由此可恢复的是**原资源的地图编号与碰撞元属性**，绝不能由一个map_number说明“玛丽娜斯/萨姆吉尔属于首版”或“某NPC就在此格”。地图DAT宽/高+tile/parts/event三层客户端解析器已有，但无本次承诺的原版地图payload；后代2.5/2003共995个地图路径，980个同路径同SHA，兼容台湾1.0资源的数量仅为跨版本**画图资源可兼容性**，不能证明台湾1.0确实具有这些场景。

停止标准：`TW10_ORIGINAL_COLLISION_MAP_NUMBER_ATTRIBUTE_CROSSWALK_COMPLETE`只在新脚本实际针对完整原数据通过独立CI后关闭资源层交集；野外地图全图、完整村庄、NPC刷新、任务对白/条件、遭遇区域继续`OPEN_SAME_BUILD_SERVER_PAYLOAD`。下一项`TW10-AUDIO-EVENT-SOURCE-GATE-01`：优先音乐音效原盘源和事件调用路径，而不是无边界反编译。现阶段仍为历史复原准备，7 PARTIAL+2 OPEN，Stage B生产/资料站GATED，R79暂停。

 
## 原盘实算结果与源字节保管

GitHub Actions`39078746682`成功运行完整台湾1.0原碰撞来源与2001玩家分类的区间对照，原归档Action`39079097177`又成功逐字节重放。9286条原map_number→bitmapno资源属性并不表示9286个地图场景；原文件重复map_number 3例已在派生原数据采用末条覆盖，因此本独立交叉分析不冒充又恢复了冲突前序记录。

| 玩家图号候选分类 | 原始map_number映射条目 | hit0 | hit1 | hit2 |
|---|---:|---:|---:|---:|
| 小地形 1–4574 | 4571 | 1539 | 3032 | 0 |
| 大物件 4575–5845 | 1271 | 972 | 237 | 62 |
| NPC静态资源 5846–5946 | 101 | 101 | 0 | 0 |
| 其余编号 | 3343 | 3317 | 26 | 0 |
| **全部** | **9286** | **5929** | **3295** | **62** |

这只是原ADRN bitmap碰撞资源/地图编号属性，不能用属性hit0就判定某个世界坐标不可移动；真实floor地图DAT的tile/parts/event三层场景没有取得。同版地图/村庄/NPC内容继续OPEN。

源 artifact`12117946984` ZIP1795B SHA256`8d48e37f0eae58b7659e7315ef83ccffe95c36d8728b6fe76d68d7d0d1dab5a4`；raw JSON8494B SHA256`5efa5972fe68d38d0e85aad3c7e13d6c4cd588c0f1b81a5900ba79e8a6711dd9`；Git blob`7d4d5d2cae224c093b3e85e8ef1bfc49b54c5981`。只永久归档元数据及验收回执，原版权地图与图像没有入库。
