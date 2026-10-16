# 《石器时代》Stage A 九系统复原预审 R1

Date: 2026-10-16. **结论：PREFLIGHT_CLOSED_STAGE_A_NOT_ACCEPTED。** 本包是从当前主线 Portfolio R1、WORLD-01、RULES-01 和直接台湾 v1.0 客户端成果出发的有限阶段盘点，不代表历史原版游戏已完整恢复，更不能按 R 编号或测试数给“总体百分比”。Stage B（新引擎/新内容制作）仍被门禁阻止。

## 九系统族：已有可复核成果与真正的历史缺口

| 系统族 | 当前组合状态 | 有用的已有成果 | 材料/历史缺口与执行边界 |
|---|---|---|---|
| lineage | PARTIAL | Taiwan Waei/JSS v1.0 retail-client foundation file/resource/runtime boundaries are authenticated. | JSS1999 exact original bytes and first-generation commercial server content are unavailable; recovered25 data are not early-version facts. |
| world | PARTIAL | Four bounded recovered25 hometown routes, 826 later recoverable floors, versioned movement/encounter source; v1 directly proves map M/MC/cache mechanism. | Early map/NPC/encounter membership; exact original field/event payload and conditional destination inputs. |
| characters_pets | PARTIAL | V1 character/pet status layouts plus descendant-based pet capture, growth identities and a bounded captured-pet roster/save/reentry scenario. | Original captured pet current MP, initial EXP/thresholds, skills, visible AI, and 1999 growth input coefficients. |
| battle | PARTIAL | Source-derived ordinary round/attack/capture model and limited battle-local EXP attribution / terminal HP return. | Source-verified original command/rule mix, level threshold regime, natural complete encounter/settlement and original rewards. |
| inventory_economy | PARTIAL | Descendant normal shop/equipment/trade semantics; recovered25 conditional item gate; synthetic local purchase-to-dispatch/two-reload integration. | Original NPC inventory/prices, source item DROPATLOGOUT, award/consumption and original economic progression. |
| npc_quests | OPEN | Descendant create→template→NPC-function graph; later shop route distinguished from ExChangeMan two-record award surface. | 1999/JSS/TW1.0 quest scripts, NPC/event population and original story rewards; incomplete Windowman arguments. |
| graphics_audio_ui | PARTIAL | TW1.0 disc directly supplies indexed graphics/animations, 218 battle SAB scenes, 15 indexed battle palettes, 114 indexed SFX, 116 loose SFX and 11 BGM; v1 protocol field/status/UI envelope anchors. | Direct asset/state/action→visible scene controls, animation selection and original UI layout interaction semantics not yet joined in one finite crosswalk. |
| runtime_persistence | OPEN | V1 client-local savedata is separate from descendant server DATA/WORK/save/logout and modern independent local persistence; reference disk roundtrips pass. | Original commercial SAAC save format/ack/durability and matching save-state fields; client-local savedata R79 nonblocking. |
| integration | PARTIAL | Engine-neutral runtime coordinator with versioned maps, encounter, representative battle/owned item/WarpMan/save paths. | Historical canonical end-to-end original server execution, early map/quest population and source-full character defaults. |

所有九族**仍为 PARTIAL/OPEN**。一个特定晚期样本或现代测试形成可运行示例，并不将整个系统升格为早期正式复原。现有资产/协议解析、四出生点、宠物状态、ITEM 门槛和本地双读档均只在其证据和显式输入范围内有效。具体版本、输入和缺口逐族存入机器表 `research/recovered/STONEAGE-STAGE-A-NINE-FAMILY-PREFLIGHT-R1.json`，含 13 份不可变来源 Git blob/字节量校验。

## 关键取舍

历史首期 JSS1999/台湾1.0 商业服务器的地图任务、人宠默认运行态、完整 EXP 表、商店/奖励及 SAAC 存档仍缺少同版源资料。重复下钻旧 Windows/CRT 函数不能自动提供这些内容；这类工作保持明确的 OPEN 与重开条件。

**下一实际复原包优先 UI-SEMANTICS-01。** 因为已经验收的台湾 1.0 客户端直接包含 REAL/ADRN 图形、SPR/SPRADRN 动画、战斗 SAB 布局/调色板、音频资源及多个原始游戏状态/动作消息结构。较有价值而仍未闭合的是：原始状态与操作如何选择对应画面、图形/动画和反馈语义，而非是否有一个现代渲染引擎。先做五个有界源证据槽，再判断是否需要更小的原版可执行文件定位；不允许凭资源存在推测一定显示在哪个界面，也不提前制作美术。

| 待核界面/交互 | 原版消息/资源起点 | 下一包只需补的语义 |
|---|---|---|
| FIELD_AND_POSITION_STATUS | S:C floor/position and related S:D/E status branches; M/MC map delivery; v1 graphics-address namespace | Locate exact field view state-to-render/interaction mapping and which resource/animation IDs are invoked. |
| CHARACTER_STATUS_AND_HUD | S:P full player status and S:M compact HP/MP/EXP; v1 REAL/ADRN resource address namespace | Join original incoming state positions to the displayed field/status screens and controls. |
| INVENTORY_AND_ITEMS | S:I full item records / incremental I + item operation results; original sprite/graphics containers | Item slot, item view and UI action/response ownership, not a new economy rule. |
| PET_STATUS_SKILLS | S:K owned pet status and S:W skill view, KS/PS requests/results; SPR/SPRADRN animations | Original pet view/select/skill command presentation semantics with explicit unknown art/animation crosswalk. |
| BATTLE_AND_NPC_WINDOWS | B battle messages, 218 SAB battle-map entries, 15 indexed palettes + Palet_0 separate; WN window envelope | Battle scene/command/NPC window visible state and response mapping; Windowman later configs are not launch-era screens. |

### 五槽验收边界

每槽记录原版来源角色、已知字段/动作、资源索引（若有直接绑定）、运行前提、未证实画面映射、后期版本冲突及无法复核之影响。必须避免用后来 2015 年教程界面、再发行版本界面或其他《石器》衍生游戏截图来冒充 1999/台湾1.0 的直证。可以另作为有日期的对比史料，但与 `V1_DIRECT` 隔离。

特别注意：台湾1.0 `S:P` 与 `S:K` 的字段界限直接可验，不能混入后期骑乘/转生/融合扩展。NPC Windowman 后代 `takeitem/giveitem/warp/battle` 占位字段未证明会执行；四份恢复 2.5 Windowman conff 缺失，不能虚构原版窗口结构。218 战斗 SAB 与 15 已索引战斗调色板、未索引 `Palet_0.sap` 保持区别，不能把233项误认成233张地图；114条容器音效与116份松散 WAV 和11份 BGM 也不能合并为一个 ID 空间。

## 退出条件、阶段安全与下一步

UI-SEMANTICS-01 只交付五槽有版本/原始消息/资源/交互/缺口的规格表。任何无法复核的历史渲染行为保留 OPEN，不能按设计常识填默认值。此任务完成后再审其他八族，若新证据直接改善人宠战斗/首骑情绪节点或原始剧情归属，则重新排序；此前没有可证据支持的历史总完成百分比。

需要重新打开别族工作包时，必须有对应同版可下载源、明确的规则矛盾或直接妨碍代表性玩法的业务字段。R79 继续暂缓；不重做826图与NPC全量清单，不挑选最终引擎、不制作新游戏。

## 可复核出处

- portfolio: `research/recovered/STONEAGE-RESTORATION-PORTFOLIO-R1.json` (`696be2bdc360e066abe92f95255b912eae3e90de`)
- foundation: `research/clients/STONEAGE-TW10-FOUNDATION-BASELINE-ACCEPTANCE-R1.md` (`07267e55aabd181c574be7b5d3bd88402d766f11`)
- client_boundary: `research/clients/STONEAGE-TW10-CLIENT-DATA-BOUNDARY-R1.md` (`11e2b77bce2febfef37c3a0c87dec878a6f289ee`)
- gameplay_matrix: `research/clients/STONEAGE-TW10-GAMEPLAY-DATA-MATRIX-R1.md` (`ddbef0ebd37d1a86554f7ac64f63f3ca4776e75e`)
- audio: `research/clients/STONEAGE-TW10-AUDIO-PROVENANCE-R1.md` (`b4e7746b4a6b1b2db2fd7a5633c01fdbdc6e4c55`)
- windowman: `research/mechanics/STONEAGE-WINDOWMAN-CORE-R1.md` (`92a318d3e37c0dfa48789391192e4198b3dd379c`)
- battle: `research/mechanics/STONEAGE-ORDINARY-BATTLE-ROUND-R1.md` (`f1ff84f3bbf99a0a5a973981f4ec86f777dc6eb0`)
- capture: `research/mechanics/STONEAGE-PET-CAPTURE-CORE-R1.md` (`c44ba2ce47c66f9036f4cbdec9faf20c2bf20e3c`)
- historical_save: `research/mechanics/STONEAGE-SAVE-LOGOUT-PERSISTENCE-CORE-R1.md` (`324d951341d7e0ac1b1996659857614a08b72f12`)
- world: `research/recovered/STONEAGE-WORLD01-FOUR-HOMETOWN-ACCEPTANCE-R1.json` (`5b7abe7e05bd6c9074c556cb4cf105d371bfa26e`)
- rules_preflight: `research/recovered/STONEAGE-RULES01-CROSSSYSTEM-PREFLIGHT-R1.json` (`d5990b2b617f586403e8c881ed900b5c58fbf5be`)
- award: `research/recovered/STONEAGE-RULES01-KEYITEM-AWARD-BOUNDARY-R1.json` (`dc5923920bfc728be3cbe51802ed48c1c78fb34d`)
- coordinator_reentry: `research/recovered/STONEAGE-RULES01-COORDINATOR-GATE-RELOAD-ACCEPTANCE-R1.json` (`027df051030a7deaea93a516e7f6821938a321f7`)
