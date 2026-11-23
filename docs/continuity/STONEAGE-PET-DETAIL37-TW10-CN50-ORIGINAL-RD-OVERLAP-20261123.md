# PET-DETAIL37｜台湾1.0与保存大陆5.0 PC原头像RD字节复用逐只闭合（2026-11-23）

## 工作目标与真实新结果

从最新主线 `5e0c01f0c854af7aefa75fd0485ddf728d069168`、tree `58bec514bacb6eaec545f71f7de03c0185d8b404` 读取四份源锁定机读原件，**将台湾1.0具名原SPR身份与保存大陆5.0的同包相簿原名、原ADRN末条投影、原RD完整SHA逐只交叉**。原始大型 `docs/CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保留。

* **120** 条台湾1.0本地原相簿头像：先经两端原SPR完整段指纹和名称校准为同一源级身份，再核各自原RD块完整SHA-256 **120/120精确一致**，不只是图号或字形相同。
* **4** 条台湾1.0原头像缺失：洛克斯、阿伊薩、格洛格魯、朵洛將恩，分别有后期 PC 源已验双RD候选（126066—126069及126222—126225），但台湾1.0原生相簿仍未有这四张头像；这4条绝不能称为台湾1.0 RD复用成功。
* 保存大陆5.0 **另181条具名槽位**不在原台湾1.0这124条已证具名SPR身份配对内；未构成“181只新版物种”或者“181只已实装”的官方数量。全305个原相簿名和末条图像RD SHA各可定位，分区严格 **120+4+181=305**。
* 全305个末条投影RD哈希均不重复；这只说明这份保存文件末条候选不同，**不**说明完整原ADRN没有撞号、全图片唯一在其他版本中不存在、游戏原生默认用末条或真实服务器有305只可获得宠物。

## 证据来源

1. [台湾1.0认证零售原相簿124条与原SPR/RD](../../research/recovered/STONEAGE-PET39-TW10-RETAIL-CLIENT-ALBUM-R1.json)，保留原EXE/SPR/头像RD精确 SHA。
2. [台湾1.0与保存大陆5.0已核124条原SPR具名桥](../../research/recovered/STONEAGE-PET126W-TW10-CN50-ALL-124-ORIGINAL-PC-NAME-VARIANTS-R1.json)；允许简繁及已验证异名，但**不**对全305行做仅凭名字猜配。
3. [保存大陆5.0编译名到同CAB原ADRN末条及RD索引](../../research/pets/PET-DETAIL-EVIDENCE36-CN50-ALBUM-ADRN-RD-PROJECTION-R1.json)，属于**第三方保存PC安装包**，原始官服当年纯净发行压盘资格仍未独立证明。
4. [四个头像缺项的后期原RD两个不同候选、真实实读证据](../../research/pets/PET-DETAIL-EVIDENCE33-FOUR-PC-PORTRAIT-PIXEL-PAIRS-R1.json)。本次**重新组合并核算已存元数据**，没有重新取得或解码原商业图像字节。

完整305条结构化结果：[PET-DETAIL37机读逐条来源分层](../../research/pets/PET-DETAIL-EVIDENCE37-TW10-CN50-ORIGINAL-RD-OVERLAP-R1.json)；独立可复算程序 `tools/stoneage_pet_detail37_tw10_cn50_rd_overlap.py` 与测试 `tests/test_stoneage_pet_detail37_tw10_cn50_rd_overlap.py`，四份输入均被 Git blob SHA 锁定。沿用PET33/PET36证明，并不是发明一个新的原客户端或已确认305个真宠种群。

## 历史边界与NEXT

**FACT**：原台湾1.0本地原SPR具名配对124条，其中120具有与保存大陆5.0逐字节哈希一致的原头像RD；另4只早期缺头像在后期找到两套不同图像。**OPEN**：原大陆5.0完整ADRN中这305个别名是否还存在其他重复记录、原生渲染选择器、早期官方服端Pet ID/出生属性/成长/技能/捕捉/发行、保存PC版本的原始发行资格。**DESIGN**：仅以字段级版本标签记录；不得把来源索引当成新游戏已实施方案。

**NEXT PET-DETAIL38**：若合法可读的已保存大陆5.0 `adrn_31.bin` 可用，直接针对305个别名扫描**原303197条全量+76字段**并保留按源文件顺序的全部匹配（覆盖PET33已知28085—28088双变体）；同时定点检查已保存台湾8.5同版原图/可取官方PC补丁的原生选择器和服务端宠物表。若原商业字节当前不可取，明确止点，不拿末条派生表冒充原全表、不追付费卖盘、不扩社区私服公式。

PET仍唯一活动模块；仅经典原PC；Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING；全游戏完成率 UNKNOWN。无原商业客户端、服务端主档、像素上传。
