# ORIGINAL-CHARACTER-CREATION-CONTENT-16｜台湾1.0人物创建原始 body 资源候选基表

2026-10-25。本包落实 CURRENT 最新 NEXT16：同版本官方零售客户端建角协议输入 → 编译身体图形字段来源 → 原SPR组号。**首次取得具备原始 exe 字节锚点的十二个连续组号候选，不是已验证十二名可选人物**。不新增后代角色名、绘画或新作规则。

## 原始载体与真实取证

- 基线：此前接受的台湾 Waei/JSS v1.0 原版零售镜像，下载存档 `CD_DIC.rar` MD5 `b37a4a47f4eb608cac67e4ddf7a1621a`、SHA1 `b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded`，只提取镜像内 `StoneAge/sa_3.exe` 并验证 425984B/SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a`。未执行程序/连接服务器/提交原版权文件。
- 原程序指令位置 `RVA 71013`：`mov esi, dword ptr [ecx*4 + 0x458e28]`；该 indexed source 物理对应原 PE 可读表字节 `RVA 364072`。附近 `RVA 71020` 计算 `5*eax`，`71036` 累加至 `esi`；`71038` 将 `esi` 写至旧建角发送 `body_image_id` 的原始全局地址。**这只是限定控制流窗口内的静态来源关系，不是全部选择路径的运行时求值。**
- 旧同版本 `CreateNewChar` 编译信封为12整数+1字符串，13项载荷的早期协议标签中 `body_image_id` 第3、`face_image_id` 第4；两者实际内存值、合法 `ecx/eax` 范围仍未获取。原 `SPR-GROUP-R1.tsv.gz` SHA256 `4db7809de4197eb90cca6dc04bda8550025e022c8232e2ebb902db0e9faf0175` 共有 **464组**。
- 来源专用 Actions <https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40195712866> / job `121175972333` / 取源分支 HEAD `9261195a0252225c8dca5d7331d748b9219fe3e6` 已实际 `completed/success`。临时ZIP artifact `12600325678` 1670B/SHA256 `368a7b3ed200f5164835e1ac68ca50c3e67eb32ac712fa0438c4f4faadfa5e6c`，唯一派生原JSON 12876B/SHA256 `03be7a2c14f71c96c8114156c7189d836d99b805895510edf453ae9f706d7a59`；原数值128B窗口 SHA256 `0e9687f40dae13f8b700426b44b8fcd1b5b462396541b0123464034fbb755d65`。
- 派生JSON全文已从真实 Actions 下载并独立验证，通过仓库 Actions `40196456122` 使用 `contents:write`、`actions:read` 将**无版权像素/程序的元数据**永久提交至 `research/recovered/STONEAGE-TW10-CREATION-BODY-WINDOW-R16.json`，原派生 Git blob `4e0d8bddf6ee9e9de372b0b484d3489796007726`，源存档提交 `5ee3a6d213ce8ca47237bc4160f80b92782c7719`。不依赖7天临时工件继续研究。

## 同版数值交叉结论

| 连续索引位置（仅采样偏移） | 原程序DWORD值 | 在原TW1 SPR组号中存在 | 能否定为可选人物 |
|---|---|---|---|
| 0—11 | `100000,100020,100040,100060,100080,100100,100120,100140,100160,100180,100200,100220` | 12/12 精确存在 | **不能**，只证数值连续和同版组号关联 |
| 12 | `198` | 不属于对应SPR组号 | 可能表示相邻非表内容；非合法表上界证明 |
| 13—31 | 19个原始后续DWORD | 该32值窗口中组号命中总数仍12 | **范围外窗口**，不推全部候选 |

对32个DWORD做小端重新编码得SHA256与原始128B源窗口一致；按独立原SPR组表重算每个成员资格，12个命中、12个在R101编译动画键有效区间内，与永久派生报告严格相同。R101只是已验SPR动画查找和帧选择的同版本规则，**没有连接这个输入表的运行时选择器**。不把画面资源编号、头像编号、形象名称、宠物种类、初代12个固定外观或JSS2001手册所述人数互相替代。

## 证据边界和停止条件

- **FACT：** 原exe的固定代码和128B表窗口逐哈希可回读；12个连续数值与464个同版SPR组号精确相交，末尾的 `198` 不是同类组号；原消息第3/4位置对应身体/脸部来源的旧编译候选。
- **HYPOTHESIS：** 前12个数值可能是人物创建的外观基表入口；也可能受另一路分支/索引约束、偏移累加与运行时状态影响。静态邻接不等于可选择的12个角色。
- **OPEN：** 原代码真正表长、索引合法值域、全局输入写入条件、后续与真正姿态/调色板及头像身份映射、同版实绘/成功创建与角色名称。重新开启必须取得其一：已认证同一exe选择上界/完整控制流、原运行轨迹、可认证同版原始角色主表或源本体可选外观截取；不得以2001晚期社区12种直接回填。
- **DESIGN：** 未作现代玩法或美术决定。原专有载体、位图、音效、ROM、完整程序及原WAV均没有进入Git。DD-028本体任务/永久增加/节日运营活动/起源待考四档仍隔离。
- **止点：** 达成所需一项原始数值—同版SPR材质关联；按连续性协议§13回到22域官方原资料实物轮转，**不再扩通用角色writer/绘制helper链**。下一包 `OFFICIAL-NAMED-CONTENT-MATERIAL-ROTATION-17`：优先有实物、可验证版别的NPC/任务/宠物具名原始记录或来源可访问性，不再做旧表旁路hash循环；无同版本体数据则精确列出缺载体并轮换。

## 重放与验收

```bash
python -m unittest tests.test_stoneage_tw10_character_creation_body_window_r16 tests.test_stoneage_tw10_character_creation_r16_join tests.test_stoneage_tw10_character_creation_r16_acceptance -v
python -m tools.stoneage_tw10_character_creation_r16_acceptance
```

独立接口验证 `40196161564` 成功；跨永久报告SHA/Git blob、原字节重建、序号、表外语义、旧CreateNewChar/R101交叉验证及多组故意篡改拒绝的候选Actions `40196651280` 实际 `completed/success`。候选/main完整项目通过与此处原客户端逐画面运行不是一回事。主线集成Actions及最终main SHA须实际后验记录，不能提前填入。

原连续性文档 `docs/CURRENT-STATE.md` 完整保留，无全体复原比例判定（`percent=null`）；Stage A仍七族PARTIAL/二族OPEN，Stage B与资料网站 GATED、R79 PAUSED_NON_BLOCKING。
