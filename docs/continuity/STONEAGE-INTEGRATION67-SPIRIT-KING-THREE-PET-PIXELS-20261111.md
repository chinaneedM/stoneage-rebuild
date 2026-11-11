# INTEGRATION67｜精灵王原GetPet三候选与台湾1.0宠物二维原像（2026-11-11）

## 起点、目标和源身份

按连续性协议，从新查远端 `main=b652ed2cd7479f1530d232b2dd07b3f07f1f03a8` / tree `06f7d05b3372fe32f5ccda350658c7462854a651` 启动，重读README、协议、原 `docs/CURRENT-STATE.md` 的完整原生blob、历史/设计/来源、路线、模块指令、最新INTEGRATION66验收。原CURRENT始终是2,709,173B / Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，不截断、不改写。上一批四岛奖励图号已闭合，本轮转至未专项联接的**精灵王事件真实原脚本中3处GetPet与已保存原图**；不是新增3种物种或3份新脚本。

使用后期**社区mixed25保存本**精灵王脚本及同源enemy1/enemybase1静态表；使用**不同载体**认证的台湾Waei/JSS v1.0原SPR、ADRN和已解原RD候选PNG（PET07）。不同版本相同图号仅是有来源的数值候选，不证明两源在同一官方部署使用。

## 本次真正复核的原始字节及源控制

私人QUEST29 ZIP 91,171B / SHA256 `e710f97dfc165e06680f3b016b19313c6a5569558cfc700759da1cc2f0f28407`，138/138 成员CRC逐原字节验证；三份原CP950脚本整SHA、原物理行与GetPet行UTF8 SHA均与QUEST29和WORLD21旧数字目录相同。本轮原脚本发现数0；原指令及静态门槛：

| 原脚本 | 物理行 | 原GetPet | 同源enemy→template | 独立TW1同数字图候选 |
|---|---:|---:|---|---:|
| `king/event69_1` | 34 | 355 | 312 | 100376 |
| `king/event69_24` | 18 | 484 | 315 | 100430 |
| `king/event69_7` | 120 | 1479 | 718 | 100451 |

条件原文分别包含 `ENDEV=4&ENDEV=29&ENDEV=30&NOWEV=54&ITEM=2547`、`ENDEV=4&ENDEV=69&ENDEV=70&ENDEV=71&NOWEV=72`、`ENDEV=4&ENDEV=69&NOWEV=70`。另首脚本有字面DelItem2547与EndSetFlg54；第三脚本另有GetItem19624/EndSetFlg70。只核静态原条件和数字；**不**解释为原生分支实际触发、奖励、旗标写入、随机概率或实际物种身份。

## 台湾1.0真实原图来源与限度

私人PET07原HTML **15,123,277B** / SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76` 与原RD报告 **1,617,404B** / SHA256 `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4` 全SHA重读。筛选图号100376、100430、100451的原SPR动作码0、2、1，方向0共9段：对应**16、20、38帧位置（合计74）**，每段原u32le位图顺序SHA与源收据一致。三组各16张不同bitmap、共**48张不重复的原RD→PNG候选**；48/48逐PNG字节SHA、原RD SHA、尺寸、RGBA解码复核，与PET07当前保存配色全部一致，*没有*先前INTEGRATION66的6张旧PET06配色冲突。注意该结论只限当前48张，不证明游戏运行时调色板选择。本轮新原RD二进制重解码0，原生客户端/服务端执行0。

原图私人研究交付包含每组实际原像的静态有序序列和现代排列图；它们**不是**原客户端动画播放速度、原NPC与宠物相同身份、游戏场景或玩家领奖截图。不能把帧位置数或图号数当成历史宠物种数。

## 私人保管与公共可核性

新私人 `StoneAge-INTEGRATION67-spirit-king-three-GetPet-TW1-original-pixels-private.zip`：**437,505B / SHA256 `f30e9995697030be3c16bb98075b22ca708d35f3ed61abffc9cf1ada8ff10619` / 56成员**（三份原脚本、48张真实已保存候选PNG、3幅现代排列参照图、HTML和私人核验收据），成功存个人Library `/石器时代/` 后，从另一新副本读取，字节、整SHA及**56/56 CRC一致**。原商业原文、RD/PNG、对照图片和私人HTML全部不进入公开仓库。

公开仅[数字、原事件与行SHA、原模板关系、SPR动作位图顺序SHA、48个RD/PNG原件散列及尺寸](../../research/recovered/STONEAGE-INTEGRATION67-SPIRIT-KING-THREE-GETPET-TW1-ORIGINAL-PIXELS-R1.json)，辅以可重放的公开负例测试。公开CI无法重解私人原图，私人实物核验与公开数字验收不可偷换。

本源限定支线到此止点。**NEXT：** 调转未专项的、确有原始字节且可以恢复可见二维内容的另一地图/NPC/宠物/道具关系，先查重，不叠加重复同号、不扩网服、账号、引擎或未来重设计。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、`overall_percent=null`；原版实际任务执行/同部署仍 OPEN。候选和正式主线Actions只能在真正完成后另行记录，**不预支成功**。
