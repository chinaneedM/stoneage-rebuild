# PET-HIGH-FIRST-33：逐条字段缺件与恢复队列

沿 R32 的25份固定源对象生成可查询、逐条来源定位的缺件队列，不复制原商业素材，不把同名或图号变成官方身份。每项记录名称/原源位置、现存证据、11项尚未同部署验明的正式字段及具体再取证优先类。按源位置而非物种统计。

| 来源 | 记录位置 | 实质证据 |
| --- | ---: | --- |
| 台湾1.0 | 124 | 120原头像、4原姿态替代；124原动作索引 |
| 保存大陆5.0 | 305 | 全部有原RD散列和SPR组引用；早版不匹配181不作早版缺失 |
| 保存台湾8.5 | 1889 | 四程序分轨，额外SPR范围内685个具名槽与1696条图号路线精确原行散列关联 |
| 声称台湾7.5 | 467 | 条件初值、成长、技能槽、后期遇敌比较；不作官方数值 |
| 后期年兽、日韩具名 | 45 | 8后期年兽、29日韩早期资料、8独立取得档 |
| 2011—2025历史具名候选 | 156 | 41+43+18+54来源位置；保留来源角色，不计物品或泛称 |
| 合计 | 2986 | 非物种数，非全历史名录 |

TW85额外SPR仅550图号的专项取证，四程序分别覆盖207/190/106/182个具名槽，头像补丁候选182/182/106/182；每轨另301个槽不在该专项内，标记 NOT_ASSESSED_IN_EXTRA_SUBSET 而不是缺原图/动作。既有原像素取证仍保留。

## 使用

```bash
python3 tools/stoneage_pet_gap_queue.py --verify
python3 tools/stoneage_pet_gap_queue.py --query 蒙奇
python3 tools/stoneage_pet_gap_queue.py --source tw85_grid
python3 tools/stoneage_pet_gap_queue.py --priority P1_FREE_LATER_ORIGINAL_CLIENT
python3 tools/stoneage_pet_gap_queue.py --all > pet-source-gaps.json
```

优先寻找真正可免费取得的后期经典PC原客户端/补丁和同部署主档，保留日韩本地原名；有同源实物才恢复缺字段。条件数值、现存原图索引、同期见闻不必重复搜集，除非能解决冲突。不得把未评估子集误判为缺资产；不得将宣传奖励、玩家数值、跨版名称对应等同官方实际取得。历史名录尚未达到官方全字段结项门槛。


## R34 增量

[大陆2011—2012同期字段](CN-2011-2012-PERIOD-FIELD-WITNESSES.md)追加16个独立来源位置，队列共3002。原R33的2986为其历史验收口径；全字段同部署仍未验明。


## R35 增量

[2013大陆状态面板、取得与成长封印](CN-2013-PERIOD-FIELD-WITNESSES.md)：13独立补缺位置，阿玛兰斯对话候选仅在R32查询保留，队列3015。三份Lv1样本非初值范围。

## R37 台湾1.0原名档逐项对照

现有124项均附 `source_evidence.field_reference`。可按 PET 档号核对2001投稿和后期模板的属性是否一致、存在异组、互不吻合或缺资料，并追出处。史料中的获取描述可随同查看。同部署正式字段仍等待原服证据。[逐项判断依据](../continuity/STONEAGE-PET-HIGH-FIRST-37-TW10-FIELD-REFERENCES-20261124.md)。


## R46 高版本取得补缺分流

349条无保存版双宠标记遇敌路径的既有TW75记录按来源资格分流，13有原任务奖励配置、234有其他来源参考、102本批无合格取得参考。没有新增队列位置，也未宣称任何官方取得字段关闭。[逐条矩阵与续接](../continuity/STONEAGE-PET-HIGH-FIRST-46-PC-ACQUISITION-GAP-20261124.md)。


## R47 同期取得补证

对102条R46缺件补充19条同期名称元素相容的玩家取得记载，2条异元素冲突、8个仅上下文关联，余83条无相容记载；不改变正式字段、总位置或历史R46口径。[续接](../continuity/STONEAGE-PET-HIGH-FIRST-47-PC-PERIOD-ACQUISITION-GAP-20261124.md)。


## R48 旧PC图鉴取得关联（候选）

83项余缺中9项名称元素相容的旧图鉴/攻略参考，余74；原R47及正式字段不变。见[续接](../continuity/STONEAGE-PET-HIGH-FIRST-48-LEGACY-PC-ACQUISITION-GAP-20261124.md)。


## R49 同期PC取得补证（候选）

74余缺位置增7个相容参考（6原名，布尔摩两个模板共享一条报刊证据），余67；15个上下文位置未升级。见[续接](../continuity/STONEAGE-PET-HIGH-FIRST-49-DATED-PC-ACQUISITION-GAP-20261124.md)。

## 当前覆盖

```bash
python3 -m tools.stoneage_pet_high_first_64_coverage --current
python3 -m tools.stoneage_pet_high_first_64_coverage --current --source tw85_grid
python3 -m tools.stoneage_pet_high_first_64_coverage --current --source tw75
```

当前视图在原 3,015 个待核位置中接入 2,785 个可追溯的 PET74 视觉引用。保存台湾 8.5 的 1,889 个具名位置均有严格肖像凭证，1,883 个位置的所有关联图组有完整动作画布凭证。标称台湾 7.5 的 467 个模板可按图号查到严格或有界的台湾 8.5 动作候选，模板与官服身份仍需同部署证明。台湾 1.0、大陆 5.0 的原件观察与跨载体对应分别显示。原 PET64 命令仍可重放当时发布的摘要。[覆盖与正式字段缺口](../continuity/STONEAGE-PET-HIGH-FIRST-75-CURRENT-COVERAGE-20261126.md)
