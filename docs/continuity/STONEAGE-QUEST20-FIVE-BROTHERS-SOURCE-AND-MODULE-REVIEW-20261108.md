# QUEST20 — 五兄弟地下城，五组选择道具、六层原MAP与领宠来源关系（2026-11-08）

## 远端与任务组合审计

从GitHub远端 `12c1bd336ff2e98507bfa708553675f85290fa5d` / tree `835619b34de6927e6a8e76fcf25b6b656d5c42db` 重新读取主线、提交、11项成功Actions、协议、README、历史/来源、模块路线，以及完整 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 2,709,173B，**不改动原巨大历史文件**。QUEST19已验收，QUEST20优先模块去重后处理有实际材料的剩余任务族。

原 QUEST01 具已有 315条活动CREATE引用、295份不同脚本、1349个TYPE源段。QUEST08–19十二个专项脚本来源路径合计80份、相互路径无重复，其中78份已经属于QUEST01（403已知段）；另外2份 `giiru/event/event30_5` 和 `.old` 是保存目录变体，在该QUEST01 CREATE索引中没有活动引用。**217份QUEST01脚本尚无这十二包的逐族专项，不等于缺源或游戏未还原百分比**。本轮不能把原索引已经覆盖的旧段重复算作新增任务。

## 五兄弟的地下城：原字节与地图

源属于后期社区混合2.5保存本，并非 JSS1999、台湾1.0、大陆初代1.82认证部署。私人原 NPC ZIP 995,176B/SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 本轮实际 SHA/2205条成员CRC全部通过；原 `giiru/event/ev28.create` 5199B/SHA `35616eedb62b5fe5fa8c04a9d978bee7c0808ed092ce3fb6040f78e076ad74ce`，30份活动引用脚本合计30,333B，严格CP950往返与QUEST01原SHA/CRC均同。ITEM01私有双表行和台湾1.0原RD图候选 ZIP 5,868,386B/SHA `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa` 的838条成员CRC亦通过。父361MB RAR和两份完整物品表原文本**本轮未重新提取**；仅复用已认证行SHA，不虚称整个父包新验。

本族原CREATE有30个NPC配置/30份不同脚本/85个已被QUEST01登记的TYPE段。分布：31701 floor 6配置/50×50；31702 3配置/50×50；31703 5配置/50×50；31704 5配置/50×50；31705 6配置/50×70；31706 5配置/50×80。全部30个原创建坐标在MAP09已验6份DAT的宽高范围内；**没有此轮新读DAT格、没有进入原游戏或验证碰撞/楼层路线**。来源路径含giiru并不直接证明台湾1.0原世界地域分类。

## 玩家可感知的选择谜题与有界控制

注意只有**23个选择NPC**，不是24个；另有1个起始、1个中间交付终点及第六层5个奖励NPC。按源脚本中唯一的GetItem数值分组：

| 源楼层 | 选择脚本后缀 | 终点要求的道具 | 同层另一道具 | 获得要求道具的后缀 |
|---|---|---|---|---|
|31701|1–5|2507|2508|5|
|31702|6–8|2509|2510|8|
|31703|9–13|2511|2512|12|
|31704|14–18|2513|2514|15|
|31705|19–23|2515|2516|19|

终点 `ev28_end` 的一个原EVENT条件要求五件2507、2509、2511、2513、2515并出现 `DelItem` 这些数字、`GetItem:2517`、`EndSetFlg:28`；其它脚本段还包含另一个10道具DelItem和 `ENDEV=28&ITEM!=2517` 重新获取候选，不能擅自判定这些段在原生游戏何时被选择或是否全数执行。

全部85源段有 `GetItem=75`、`DelItem=52`、`GetPet=5`、`EndSetFlg=6` 条原字面命令。**保留异常**：同组 `ev28_21` 只有2条 GetItem（通常3条），`ev28_23` 只有1条DelItem（通常2条）；原来源未证明这是bug、路径优先级或重复操作后果，不模拟或补写。前五层10种道具ID2507–2516不同，但两份原94栏物品表都给同一个图别名24222；16个关联ID有16份两表成对相同原行SHA、另一个台湾1.0原RD来源有16个跨版本候选，合计仅7个不同图别名。不能凭图像同一把10件任务道具合并，也不能宣布跨来源是早期官方同服。

## 第六层五奖励和宠物属性的真实数字关系

五份 `ev28_ed1–ed5` 原脚本以2517作为道具交付字面，分别 `GetItem` 2518、2519、2520、2526、2525以及 `GetPet` **54、57、55、56、481**，并列有 `EndSetFlg:31`。**这些五条GetPet早在WORLD21就已实读并联接原enemy实例与模板，不能算QUEST20新增5项宠物。** 此次新增的是五份NPC CREATE原 `graphicname` 与同一后期保存包 `enemy.txt`→`enemybase.txt` 模板 `IMGNUMBER` 的五组精确同数值联接：\
实例54→模板91→图100287；57→94→100290；55→92→100288；56→93→100289；481→95→100394。NPC配置恰是同列图号。

`GetPet` 参数是敌人实例数字而非模板数字，例如54不是模板54。源脚本 `PET>0-91` 等字面不允许省略命名空间直接认作同一实体；原生对话条件、成功发宠、宠物名称/形态、奖励满格与该层真实可走性仍OPEN。同源关联不是全历史版本判定，更不是未来单机新作功能实现。

## 交付、可重复验收与NEXT

公开仅派生数字/SHA：`research/recovered/STONEAGE-QUEST20-FIVE-BROTHERS-MODULE-REVIEW-R1.json`；公开单测 `tests/test_stoneage_quest20_five_brothers_source.py`，复用 QUEST05 统一 CI。原脚本/原图/私人ZIP不公开。原本 WORLD21/QUEST01 的证明不被覆盖或改写；遇到后期新增真实原件再增量关联。

当前Stage A仍7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总体百分比null。QUEST20 CI后验未确认前为 SOURCE_BOUNDED_CANDIDATE。**NEXT QUEST21**优先另一族不同的原始玩法内容，或转为能实际观察的宠物/回合战斗/地图机制，不继续把已索引的SOURCE TYPE行当“新任务数”，不做账号、联网、服务器服务或新游戏引擎。

## 候选失败与后验验收事实（2026-11-08）

- 起始候选 Git commit `fdd0c7ed9f16bec69953dadc28500c00e0affb2b`，tree `fd8cd62d18be8041030829518de6c17bac4576d9`，只提交四项派生/测试/文档/现有CI注册；没有私有商业脚本正文、原MAP/DAT、真实RD像素、ZIP、原EXE等。
- 第一次候选 push [#42468725466](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42468725466) 与 PR [#42468766647](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42468766647) 的 QUEST 专项 **completed/failure**；八个 QUEST20 测试中其余七个通过，`test_04_30_spawns_inside_six_original_qualified_map_sizes` 错误访问不存在的 `uncertainties.original_NPC_route_entered` 键，原JSON正确键为 `uncertainties.actual_game_dungeon_entered`，属于**测试字段名笔误，并非源文件SHA或地图几何冲突**。失败事实永久保留。
- 修正候选 `71bafc20f3089bf956ed46c4e8f7e835f5768c9c`，只更正此一测试字段名；候选 push [#42468876689](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42468876689)、PR Quest [#42468879735](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42468879735) 及另两项PR [#42468879764](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42468879764)、[#42468879744](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42468879744) 全部 **completed/success**。
- [PR #260](https://github.com/chinaneedM/stoneage-rebuild/pull/260) 已合并，主线 squash SHA `92e8765ec209ac9896f7628b967aa184f36caea0`，tree `4b9d14aaeb5da9c3d2b590c10f97d073a829bf2c`。合并后主线 QUEST05–20 专项 [#42468934142](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42468934142) **completed/success**。这证明公开派生数据／断言和来源边界可重放，**不证明**原客户端、原服务器、迷宫谜题或领宠执行。
- 本报告初稿的「CI后验未确认前为候选」被实际结果追认，正式 `QUEST20=ACCEPTED_SOURCE_BOUNDED`；但 `GetPet`五值属于WORLD21既有证据、85段属于QUEST01既有脚本，单机可玩闭环、历史官方同版身份及真地图NPC/战斗仍 OPEN。Stage A维持 **7 PARTIAL+2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null。
- 原 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173B）未触碰；下一最高 `QUEST21_SOURCE_READY_DISTINCT_FAMILY_OR_GAMEPLAY_CONTENT_MATERIAL_REVIEW`：先比对实际还未专项复核但已在QUEST01内的族，优先能真实增加任务→宠物/地图/物品或玩法机制联接的有源材料；连续只复算旧TYPE数值就转宠物、回合战斗或地图的可见实物，不造原版行为、不转联网帐号/服务器、不启动新作引擎。
