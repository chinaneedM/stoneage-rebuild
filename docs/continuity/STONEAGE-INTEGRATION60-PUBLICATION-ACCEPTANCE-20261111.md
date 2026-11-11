# INTEGRATION60｜五间诊疗室原药师／护士／药品及TW1原图：正式发布与原件验收（2026-11-11）

## 远端开工及来源限界

本轮从实时 GitHub `main=b5aaf4cc964aa12a48bcb7be7dda9d3e3bc3daf2`、tree `485864f4e699d9abed8a2172964fe3c4ad7f274e` 重新读取分支、最近提交、Actions、无开放PR、协议、完整原`docs/CURRENT-STATE.md` Git blob、README、设计/历史/来源/路线与模块工作单及INTEGRATION59的最新验收。最新优先级要求停止重复四村武具清单，继续不同的原物品/技能/配方/任务与真实场景NPC的有据联接。

[INTEGRATION60源限定内容](STONEAGE-INTEGRATION60-FIVE-CLINICS-MEDICINES-20261111.md)与[公开数字／SHA报告](../../research/recovered/STONEAGE-INTEGRATION60-FIVE-ORIGINAL-CLINICS-NURSE-MEDICINE-ITEM-HANDLER-PIXEL-SOURCE-R1.json)接合已验证的后期社区mixed25原地图1105／1205／1305／2005／3005；每间一条护士`WindowHealer`和一条药师`ItemShop`真实原CREATE，共10条源创建关系（不是新发现的10个人物）。源护士四个原内联值、五份药师参数 SHA、五份原DAT SHA、坐标、图号均按源档与旧I49/I50/GAMEPLAY05互相确认。五药师各原ItemList同样12条数字，**60个原数字引用、12不同原物品ID、11个独立TW1零售已解原图别名**；原物品表使用回调分为5`ITEM_useRecovery`、2`ITEM_useRessurect`、5`ITEM_useStatusRecovery`，保留原拼写/使用参数/场景/目标、价格原值及A/B整行SHA。同房关联和原具体药物用途字段才是本包新增的跨模块材料；不重复声称新原地图/原物种/原动画。

## 私人原始材料真实回读、保存和限制

- 私人原mixed25保存NPC ZIP 995176B / SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` **2205/2205 ZIP成员CRC**重新合格；所选10个CREATE块、5份药师参数的原内容与相应I49/I50/GAMEPLAY05公开源SHA一致。
- ITEM01私人原表/先前真正解出的TW1零售RD原像素研究ZIP 5868386B / SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa` **838/838成员CRC**重新合格；两套94栏原物品表中12选定原行实际重读、源整行SHA与既有目录一致；11张已存原TW1 PNG逐SHA/尺寸与既存原RD收据相符。新原RD二进制解码0。
- 新私人有限源证包 `StoneAge-INTEGRATION60-five-clinics-twelve-original-medicines-private.zip` 52450B / SHA256 `940617f696b2dc45f8b2e8009e0e4286a764fea24a0c979dd5843306be84e280`，28成员 CRC 全过。已上传个人Library `/石器时代/` 并从新副本独立再下载，比对整ZIP SHA、28成员CRC均成功；原NPC片段／物品原文／PNG／私人图册**不进Git**。
- 没有新打开完整361MB混合原RAR、没有本次重读原DAT二进制、没有新的原RD二进制解码或原客户端／原服务器原生运行。跨晚期社区mixed25静态源和早期TW1原图，只能作带源的候选，不能宣传为同一历史官方部署、原生配色选择、真治疗／复活／交易效果。护士原四值与药师不同的buy_rate保留字面，不虚构收费公式。

## 必须保留的失败与真实修复、候选／主线验收

| 阶段 | GitHub实际结果 |
|---|---|
| 首次候选 | `21518242e4a6c121ded47a5bfa78eb33c36e5101`；[专项push run42960416190](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42960416190) / job130325352158 **failure**：8项测试中7通过，1项因新派生JSON漏五个`source_CREATE_ordinal`字段而KeyError；未改变原游戏数据。失败历史不覆盖、不冒称成功。 |
| 精确修复候选 | 基于旧GAMEPLAY05对应来源原CREATE序号补入32／47／63／89／9，候选HEAD `b55dfe7ebe6f2158e70d0aef81532bc55b099587`，tree `3ef06e5ddd367d28999d305672f4d1a4b3d86a87`；仅改派生JSON，不改私有原件。 |
| 修复候选CI | **20/20 completed/success**（该候选仅触发push1+PR19）；[专项push run42960720619](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42960720619) / job130326342901、[PR run42960724160](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42960724160) / job130326353693，八项专项测试成功。 |
| PR／合并 | [PR #328](https://github.com/chinaneedM/stoneage-rebuild/pull/328)在HEAD固定、main不变、mergeable clean后正式squash。内容main **`eaf7df46d4fd66f172b91ab3f79312c22da14d7c`**，tree **`3ef06e5ddd367d28999d305672f4d1a4b3d86a87`** 与修正候选完全一致。 |
| 正式main Actions | **27/27 completed/success**；[INTEGRATION60专项 run42960914737](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42960914737) / job130326971522 实际执行成功，8项测试通过。 |
| 历史CURRENT | 正式内容main树仍指向`docs/CURRENT-STATE.md`原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`／2,709,173字节，全部原样保留。 |

本页只在内容main真实27/27成功后发布，**当前验收收据自身HEAD不在这里提前宣称另一轮Actions成功**。公开CI只验证固定Git派生数字/来源关系，不能替代私人原件取源或旧游戏本机运行。

## 未证事实、阶段边界与后续最高NEXT

**OPEN：** 原护士四个参数的实服计算含义、真实药价/扣款、物品生效的战斗/场外目标、交易/复活/解状态事务、原生交互与同服客户端的选图、官方早期JSS1999/TW1/CN1.82任务/道具身份；仍无法据此宣称已恢复五间真正可玩诊疗室。后续若取得同部署原文件或原版执行证据再重新判定。

Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null，均未改变。**最高NEXT**：五诊疗室和12物品关系来源限定已闭合；下批优先一条真实未接合、具有可重新取得原文件的宠物技能／配方／任务道具或其它可见游戏服务联系，严格查重既有目录；没有新的实质原字节／关系则记清止点轮换。不得扩展医疗计算模拟、新引擎、账号或网络原服基础设施。
