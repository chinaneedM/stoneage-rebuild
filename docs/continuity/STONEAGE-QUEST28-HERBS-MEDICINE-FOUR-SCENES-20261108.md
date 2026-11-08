# QUEST28｜药草／药粉、骨头交换与四张原 DAT 场景（2026-11-08）

本包依据 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`，从**本次重新核验**的远端 `main` HEAD `d3181164d8cdf47a8d293c21da375f530960a3e3`／tree `04c679ea419249d6323064f5dfeaeabbb17d73bd` 承接 QUEST27 的最高 NEXT。已重新读取远端主线、11 项已列出的 successful Actions、完整巨型 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 和连续性及模块优先级文档。原 CURRENT 全历史不改；本记录是增量接力而非覆盖。

## 去重与资料资格

处理 `jaruga/event/event01_1/2`、`sainasu/event/nevent02_2/3/4` 五份原脚本，及准确指向它们的两份 CREATE、`jaruga/event/event.template`。五原脚本、15 个 TYPE 段**都已属于 QUEST01**；原始脚本新增数 **0**，本轮新增的是跨脚本控制关系、原材料数值、原 CREATE 地址及地图原图的统一可核查资料包。WORLD14 是 `sainasu/event/nevent01_*` 钓竿组合，QUEST11 是 `giiru/event/garunaev*` 两族任务；二者的内容不能因为同村落或同功能模板而混入本组。WORLD23 的跨任务记录仅用于查重。以下关系均是后期社区 mixed25 保存载体中的静态来源，**非** JSS1999／台湾1.0／大陆1.82 已认证的官方同服部署。

用户私人 Library 的 `StoneAge-QUEST28-herb-medicine-four-scenes-private.zip` 本轮已实际取出并独立校验：**17,761,242 字节／SHA256 `ac3fc06fe4753b2f157df05c3c3d46704157f819f95e9e92aecbe49890c30f88`／489 ZIP 成员全部 CRC 可读**。两份 CREATE、五原脚本和一份模板，共 8 文件逐全 SHA256/CRC 与既有原 NPC 目录复核；五脚本的 15 段由 CP950 原文独立重新切段，段级 UTF8 SHA 均同报告；两原物品表对应 9 ID／18 原行各94栏逐 SHA 通过。旧 NPC、ITEM、MAP09 原始私人父包通过既有来源保管收据确认，本轮没有重下原 mixed25 RAR，不称重新执行旧服务端。

## 新确认的静态交付关系

| 来源脚本／段序 | 原条件字面 | 原输出／输入数字 |
|---|---|---|
| `jaruga/event/event01_1` #0 | `NOWEV=1&ITEM=2401` | DelItem 2401 → GetItem 2427，EndSetFlg 1 |
| `jaruga/event/event01_2` #2 | `LV>0&ITEM=1983&ITEM=1982` | DelItem `1983*1` → GetItem 1984；**本段未删除1982** |
| `jaruga/event/event01_2` #3 | `NOWEV=1&ITEM!=2401,NOWEV=87&ITEM!=2401,ENDEV=87&ITEM!=2401` | GetItem 2401；三原逗号分支保留，不能只归入事件1 |
| `sainasu/event/nevent02_2` #0 | `LV>0&ITEM=2446*10` | GetItem 2449，DelItem `2446`（**原删除未写*10**） |
| `sainasu/event/nevent02_3` #0 | `LV>0&ITEM=2449` | GetItem 1264，DelItem `2449*1` |
| `sainasu/event/nevent02_4` #0 | `LV>0&ITEM!=2447` | GetItem 2447 |

这是原脚本引用关系的阅读顺序，不是已实测的任务可运行路径。尤其 `ITEM=2446*10` **不授权**将 `DelItem:2446` 改成 `DelItem:2446*10`；`ITEM=1982` **不证明**它在原混药后被消费。省略数量、逗号、原 TYPE 顺序均按字节来源保存。`nevent02_4` 的静态关键词 SHA 已记，但 `nevent02_1` 缺本原 NPC 子树对应脚本，**不能推断**原触发、骨头掉落、弹琴战斗或真正药品效果。

## 道具与四处原地图实物

9 个道具数字 ID：1264、1982、1983、1984、2401、2427、2446、2447、2449；两原94栏物品表共18原行已核。对应台湾1.0原客户端候选图实物中，只有 **7 个**有经旧来源认证的原 RD→PNG 像素；1982、1984 不在该零售索引合格候选范围，**不得补造图像、断言物品不存在或把后期道具归于初代**。后代94栏中 `usefunc` 空白、`vanishatdrop` 数字仅是原表物理列与已知后代字段名的并列，原生使用／丢弃效果仍未验证。

从既已保存的原 DAT／候选 PNG 严格复验四场景：floor 3110（30×30）、20105（50×70）、3305（30×30）、3105（30×30）；共 6 个对应原 CREATE 坐标、三平面 u16 均由 DAT 原字节独立重新计算。实际整理 **439 幅互异来源候选 PNG**，每幅完整 SHA 同私人凭据；现场四个现代 2D 场景画面／标记仅为源资料观察工具，**不是原客户端进图或 NPC 原生绘制**。floor 3200 的部分原 CREATE 有来源数值，但相应完整像素受 `MAP10_GT99_RD_SOURCE_BOUND_LOW_VALUES_OPEN` 限制，本包不冒充它也已完整绘制。没有新 RD 解码。

私有包只在用户个人 Library；原 NPC 原文、对白、原 DAT、美术候选 PNG、原观察 HTML 均**不进入公开 Git**。公开 `research/recovered/STONEAGE-QUEST28-HERB-MEDICINE-FOUR-SCENES-SOURCE-R1.json` 只保存派生数字、短字段、SHA/CRC、精确引用、限定结论与停点；配套 `tests/test_stoneage_quest28_herb_medicine_source.py` 将公开衍生记录与仓库既有 QUEST01、CHAR01 和 ITEM01 的散列及异常边界交叉检查。独立私人复验结果不冒作公开 CI 重新执行原商业字节。

## 结论与接力

本组达成了 6 条可复查的静态任务材料关系、7 个原 NPC 创建配置点、9 个道具候选及 4 张有原 DAT 依据的地图观察的来源止点；**仍没有**认证后期社区保存包是初代官方原服、原版原生任务执行、掉落、药效、NPC 实际显示或全局任务总完成率。

**最高 NEXT：`QUEST29_MODULE_SOURCE_REVIEW_AFTER_MEDICINE_BATCH_STOP`**。先按 QUEST01 的 295 原脚本索引、已经专门覆盖的 QUEST08–28 批次及 22 模块材料全面查重，再选另一组有实物、能产生新玩家可见内容整合的任务批次。若无同版新原件，记录精确受限缺口并换模块；不要继续扩散这几份药草脚本、发明条件执行器或恢复网服。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、整体百分比 **未知**不变。

## 合并后验收回执

[PR #268](https://github.com/chinaneedM/stoneage-rebuild/pull/268) 已在真实远端合并至 main `f15f31e5f0053f486da39481db1ce20190d93d86`，完整 tree `26e63c613c74b4f560861c9ae44dd7dbea248e3c`。候选 14 项、合并后主线 11 项 Actions 均实测 `completed/success`，含 QUEST28 专项；旧巨型 `CURRENT-STATE.md` 的 blob `c89e0e33537990aa2132b47c40fef49a985a935c` 再次确认未变。逐项运行ID、候选与主线边界及原 ZIP 散列已保留于[验收收据](../../research/recovered/STONEAGE-QUEST28-PUBLICATION-ACCEPTANCE-R1.json)。本后验提交自身 Actions 应另据真实结果判断，不预支。最高 NEXT 仍为 QUEST29 全模块查重及实物内容增量选择。
