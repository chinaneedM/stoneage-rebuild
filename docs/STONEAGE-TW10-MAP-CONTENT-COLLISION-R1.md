# 台湾1.0原地图编号与地形碰撞属性的可认证来源边界

2026-10-18，`TW10-MAP-CONTENT-ORIGINAL-RESOURCE-BOUNDARY-01`。此工作包**不是地图恢复成功证明**：原台湾1.0零售盘 field_map_disc_files=0，地图场景数据通过原客户端 `M/MC` 服务器协议进入 `map\\%d.dat` 本地缓存。源字节的相关调用链、缓存读写动作已经在 `research/clients/STONEAGE-TW10-RECEIVE-MAP-LINEAGE-R1.md`、`STONEAGE-TW10-RECEIVE-MAP-JOIN-R1.txt` 证明，今轮复核而不另称新发现。

新可执行任务基于真正同构建原盘 `COLLISION-ATTR-R1.tsv.gz`，它是原 `adrn_1.bin`（每记录80字节）导出的map_number、bitmapno、hit_raw、atari_x、atari_y、height_flag等元数据；9286个独立非0地图号，3处原文件的重复map number以源顺序最后一条为准（已去重的导出表不再能复算那三个碰撞来源）。

**本轮新增关系**：玩家2001年文献中对位图号1—4574“小地形格”、4575—5845“大地形物件”、5846—5946“NPC”等分类，仅作为来源级别C的候选**位图号区间**。原脚本 `tools/stoneage_tw10_map_content_collision_crosswalk.py` 用真正原版map_number→bitmapno行与这些候选区间作精确关联，按原字段输出hit/priority/height/碰撞占格分布及可复查的原始map_number。未落在这三段内的原碰撞条目保持“其他”，不将其丢弃或改判为新NPC身份。

由此可恢复的是**原资源的地图编号与碰撞元属性**，绝不能由一个map_number说明“玛丽娜斯/萨姆吉尔属于首版”或“某NPC就在此格”。地图DAT宽/高+tile/parts/event三层客户端解析器已有，但无本次承诺的原版地图payload；后代2.5/2003共995个地图路径，980个同路径同SHA，兼容台湾1.0资源的数量仅为跨版本**画图资源可兼容性**，不能证明台湾1.0确实具有这些场景。

停止标准：`TW10_ORIGINAL_COLLISION_MAP_NUMBER_ATTRIBUTE_CROSSWALK_COMPLETE`只在新脚本实际针对完整原数据通过独立CI后关闭资源层交集；野外地图全图、完整村庄、NPC刷新、任务对白/条件、遭遇区域继续`OPEN_SAME_BUILD_SERVER_PAYLOAD`。下一项`TW10-AUDIO-EVENT-SOURCE-GATE-01`：优先音乐音效原盘源和事件调用路径，而不是无边界反编译。现阶段仍为历史复原准备，7 PARTIAL+2 OPEN，Stage B生产/资料站GATED，R79暂停。
