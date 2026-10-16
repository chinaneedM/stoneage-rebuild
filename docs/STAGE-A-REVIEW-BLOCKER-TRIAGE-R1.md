# Stage A 九系统联合复原阻塞分级 — STAGE-A-REVIEW-BLOCKER-TRIAGE-01

日期：2026-10-16。远端基础 `05196c8bf2708d6841439835ea97180c6bb9337b` / tree `b503608086893f84dc449d80e48855891acac597`。**性质：已有证据联合审查，不是最终Stage A验收、不是完整初代可玩复原，也不启动Stage B。**

## 目标、证据范围与停止条件

本包确认一个玩家从出现→移动→遇敌/战斗→捕获宠物/购买道具→NPC条件/奖励→退出重登的实际玩法，哪些接口/资料在原版台湾1.0直接可证，哪些只能在后期 recovered25 / 固定后代参考模型有条件可复现，哪些必须依赖缺失的最初商业服务器。仅整理已验证源资料；没有新增原版商业服务端、原始NPC、任务、关卡数据或新作制作。

完成条件：九族门禁不冒进、至少六条代表体验证据范围逐条列明、所有高影响缺口有明确「证据何时重开」标准、旧R79非阻塞；全部记录由可检验Git blob锚定。重要数据详见 `research/recovered/STONEAGE-STAGE-A-BLOCKER-TRIAGE-R1.json`。

## 九个系统族与实质阻塞

| 系统族 | 阶段门禁 | 对原始游戏复原的关键边界 |
|---|---|---|
| lineage | PARTIAL | JSS1999 exact original bytes and first-generation commercial server content are unavailable; recovered25 data are not early-version facts. |
| world | PARTIAL | Early map/NPC/encounter membership; exact original field/event payload and conditional destination inputs. |
| characters_pets | PARTIAL | Original captured pet current MP, initial EXP/thresholds, skills, visible AI, and 1999 growth input coefficients. |
| battle | PARTIAL | Source-verified original command/rule mix, level threshold regime, natural complete encounter/settlement and original rewards. |
| inventory_economy | PARTIAL | Original NPC inventory/prices, source item DROPATLOGOUT, award/consumption and original economic progression. |
| npc_quests | OPEN | 1999/JSS/TW1.0 quest scripts, NPC/event population and original story rewards; incomplete Windowman arguments. |
| graphics_audio_ui | PARTIAL | Direct asset/state/action→visible scene controls, animation selection and original UI layout interaction semantics not yet joined in one finite crosswalk. |
| runtime_persistence | OPEN | Original commercial SAAC save format/ack/durability and matching save-state fields; client-local savedata R79 nonblocking. |
| integration | PARTIAL | Historical canonical end-to-end original server execution, early map/quest population and source-full character defaults. |

任何局部契约、测试数、模型版本「闭合」均不提升九族整体为已验收。依赖原始服务器剧情/奖励数据的两族仍为 OPEN，其余为 PARTIAL，Stage B GATED。

## 七条典型玩法链：可复现≠初代被证实

| 玩家经历 / 证据链 | 已支持的**限定范围** | 原始版还缺什么 |
|---|---|---|
| ORIGINAL_TW10_CLIENT_ENTRY | Original retail client has version-pinned field/status/owned-item/pet protocol shapes, NPC WN and resource address records; these expose an input/output contract only. | First-generation commercial server map, NPC population/quest dialogue, items, rewards and authoritative running state; original live end-to-end play not demonstrated. |
| RECOVERED25_HOMETOWN_FOUR | Four source-qualified later hometown route existential/conditional witnesses from WORLD-01; routes 1/2 COMBAT, route 3 COMBAT>SHOP>WARPMAN, route 4 SHOP>COMBAT>WARPMAN. | Historical TW1.0 route ownership, actual original destination/event/NPC data, server settlement and global outcomes. |
| CAPTURE_OWNED_PET_REENTRY_GROWTH | A finite captured-pet/roster/disk reentry/growth reference lifecycle accepts explicitly supplied current pet state; source-bound known fields are not silently invented. | Original current MP, initial EXP/maxEXP and version threshold, owned skills, status, rename/free-name and AI binding, first-generation server save. |
| BATTLE_EXP_SETTLEMENT | Ordinary battle/capture/EXP and settlement source contracts and regression evidence exist for scoped profiles. | First-generation complete battle command, level threshold regime and realized commercial reward/EXP outcomes are unverified. |
| SHOP_OWNED_ITEM_WARPMAN_LOCAL_RELOAD | Later ordinary ItemShop purchase/owned item/ITEM-FREE WarpMan predicate/local coordinator two reloads compose under explicit inputs; separate ExChangeMan GetItem source witnesses must not be conflated. | Original item identity/price/award/consumption, original quest event and authoritative logout/relogin durability. |
| V1_UI_GRAPHICS_RESOURCE_SELECTION | Five original-client message crosswalks, 218 battle SAB scene identities and 15 indexed palettes are source-specified; candidate grid decoder is not actual original render proof. | Original pet animation selection, battle palette/scene selection and visible interaction/layout runtime trace. |
| ORIGINAL_QUEST_AND_RELOGIN | WN original client envelope plus independent later NPC dialogue, NPCEnemy, WarpMan and ExChangeMan structures show relevant possible functions. | First-generation story dialogue, NPC/quest script, rewards, event flags, item persistence, SAAC ACK and matching original re-login result. |

**有界后期世界案例**：WORLD-01仅支持 recovered25 四条出生点路线，24格是来源/输入/缺口审查，**不是**24格史实复原。1、2号有 COMBAT 经典路径；3号 COMBAT→SHOP→WARPMAN；4号 SHOP→COMBAT→WARPMAN。后两条经典坐标路径不通，须满足普通购买与有条件WarpMan权限。路线中的战斗与传送是存在性测试输入，不能推成无条件保证；不属于已证实台湾1.0出生地。

**宠物/成长**：最小可执行现代参考有捕获、拥有、入栏、读档和受控成长；初代 MP、技能、EXP阈值、可见AI与匹配服务器结果未可证，不能用野生敌人EXP或随机猜测补齐。

**NPC/任务与经济**：原始 v1 WN 通信仅证明窗口数据交换；recovered25 NPCEnemy、TownPeople、Windowman、ExChangeMan、WarpMan属于后期证据。ExChangeMan事件赠送与ItemShop商店购买不同；有道具不等于已证明历史服务器事件持久化/任务完成。

**画面与保存**：真实 v1 战斗SAB索引与调色板可做可消费规格，实际场景选择/角色动画/窗口位置无直接运行链。现代本地存盘≠原始商业SAAC写入；原客户端本地savedata又是单独一层。

## 决策分级与下一步

- **P0_EVIDENCE / B0_ORIGINAL_SERVER_CONTENT**：TW1.0/JSS1999 original NPC, quest scripts, master items and original map/events unavailable; client interfaces do not determine server world content.。当前处理：RECORD_UNAVAILABLE_WITH_REOPEN_TRIGGER；重开条件：Authenticated matching first-generation server release, data files or client/server capture.
- **P1_GAME_RULE / B1_ORIGINAL_PLAYER_PET_AND_EXP**：Captured pet current MP/EXP/status and mutually incompatible descendant EXP threshold regimes cannot be selected for original first generation.。当前处理：EXPLICIT_INPUT_VERSIONED；重开条件：Source-version-selected original runtime capture/EXP threshold data.
- **P1_GAME_RULE / B2_ORIGINAL_QUEST_ITEM_DURABILITY**：No source-aligned ITEM_DROPATLOGOUT/quest EventNo/SAAC durable write and original re-login result.。当前处理：SEPARATE_MODERN_DISK_FROM_HISTORICAL_SAVE；重开条件：Matching source item/event persistence and original save ACK/relogin trace.
- **P2_PRESENTATION / B3_ORIGINAL_UI_VISUAL_BINDING**：v1 asset/message identities known, actual graphic/SAB/palette selectors and on-screen placement not observed.。当前处理：KEEP_OPEN_NOT_PREPRODUCTION；重开条件：Original v1 renderer callsites or authenticated visual/runtime trace.
- **PAUSED_NON_BLOCKING / B4_ORIGINAL_LOCAL_SAVEDATA_R79**：Client-local savedata helper ABI and realized IO effects not fully reconstructed; not a cause to defer content review absent material state dependency.。当前处理：DO_NOT_REOPEN_FOR_GENERIC_STATIC_GAPS；重开条件：Named game-rule/state dependency or new primary evidence demanding that helper's semantics.

最严重的是早期商业服原始世界/NPC/任务与奖励内容的**来源缺失**，而不是程序必须解完每个旧辅助函数。对无法恢复的证据保留 OPEN 与触发条件，不杜撰数据填空；不要求实体购买、收集原图资产或重枚举完整826层地图/数千NPC。

**下一交付 `STAGE-A-CONSOLIDATED-REVIEW-PACKET-01`**：生成面向用户联合审阅的九族阶段验收表，按「可复核规格」「带输入的参考体验」「缺原商服内容」「将来设计可借鉴」分级，标注来源和重开条件；完成正式审阅之前 Stage A 不标完成、Stage B 不启动，不做新引擎/美术/剧情生产。

## 独立验证与历史保留

本次审查分支 `785524806ee3ddc37826614f7916123f37d9b3d3` / source tree `a85d2633ade6791690594d376a5251301fe4d0c0` 对应独立 GitHub Action `38922063102`、job `117044218968` SUCCESS，共5项回归核对11份现有不可变Git源指纹；下一提交只追加验收凭据/完整历史连续性，不将原始任务/奖励复原声称为完成。阶段总验收与用户共同审阅均尚未进行。
