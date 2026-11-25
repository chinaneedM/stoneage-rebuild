# PET-HIGH-FIRST-66｜全467模板动作继承与逐帧像素覆盖（候选）

基于 main `bfffded395e548352026e06235b128aa64c7311e` / tree `a643edab2191b857ca37406c6cede6da4f9ad6ff`，PET65 候选5/5和合并后1/1 Actions通过，原历史CURRENT blob保留。本轮承接PET65的427个物理组，按完整SPR动作和帧表、R29原RD绑定逐帧核查；对照原TW10 PET15（131组、32150严格位图、5个边界例外）、CN50 R11实读像素及TW85 R12/R13/R60实读像素。TW10由固定聚合凭证、原容器散列及完整源索引重建严格覆盖集合，不声称已复读私人逐图像散列。仅完整RD块散列、长度、宽高一致方可跨载体继承；同一目标SPR序列可以由不同来源精确像素共同覆盖，不推断源版名称或实际动作语义。目标图号与原早期SPR段同摘要时额外逐项复核原方向、动作、时长、帧编号、偏移及音效字。哨兵帧独立保留，原未严格解码的5个边界位图不凭TW10凭证升级。

执行 `python -m tools.stoneage_pet_high_first_66_motion_inheritance --output /tmp/pet66.json`。逐组、逐动作、逐模板和逐位图机读矩阵，严格区分全序列、部分序列、无完整序列，并生成真正需补读的位图集合。待候选CI产出实测统计后保全摘要；避免重复下载相同RD字节。未新增原件或官服实际取得，PET仍为唯一活动模块。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79暂停，总体UNKNOWN。
