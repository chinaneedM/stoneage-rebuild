# INTEGRATION66｜四岛环岛终点原GetPet和台湾1.0宠物原像候选（2026-11-11）

## 起点、任务和来源身份

本轮严格从**当时实取** GitHub `main=a01ff1fb6b616beb8e831dfc9a9d5c5ce9c6ace2`／tree `e9735d8eef0f6e4c1b3eabdfd830ff34b4fabc8d` 启动；完整原 `docs/CURRENT-STATE.md` **2,709,173B**／Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不变。INTEGRATION65玄黄洞窟已止点，依据最新README/NEXT选择尚未专项原像接合的QUEST25四条环岛终点宠物奖励。本工作是**历史原游戏内容静态来源复原**，不是单机新游戏或原服启动。

NPC任务脚本、宠物实例/模板来自后期社区**mixed25保存版**；SPR、ADRN、REAL真实源和已有候选PNG来自**另外一个经过来源核查的台湾Waei/JSS 1.0零售客户端PET07**。同数字图号仅跨载体候选，绝不升级为早期官方同服、官方物种名称或奖励实测。

## 实际读取与四条原源列表

私人QUEST25原ZIP **172,328B/SHA256 `543cf62ec2b1f5a36a929c7714e86510f1382430039ebf6e7a487d165acffbb2`**：全部173成员ZIP CRC通过，4份终点原脚本真实读取／CP950解码／整SHA及GetPet原文字面与已公开QUEST25目录完全相同；新增原脚本0，不重复当成任务发现。

| 终点 | 原脚本 | 原GetPet有序整数（不去重） |
|---|---|---|
| A | `jaruga/event/oev_ed1` | 358,96,328,309,365 |
| B | `jaruga/event/oev_edb` | 338,360,366,**482,482**,78 |
| C | `sainasu/event/oev_edc` | 48,94,350,482 |
| D | `sainasu/event/oev_edd` | 76,309,361,96 |

合计**19原数字位置／15不同后期实例**。每一个源实例沿已验社区mixed25 `enemy1→enemybase1`的**同载体原行SHA、模板号和原图形号**连接，最后与不同载体TW1 SPR组的**相同数字图号候选**关联。B的482重复两次、跨路线重复实例均保留，出现次数**不构成随机抽奖概率**。

从私人台湾1.0 PET07离线页 **15,123,277B/SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`** 和原RD独立数值收据 **1,617,404B/SHA256 `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`** 重新读取，核出**15个原SPR组，45条原动作0/2/1、方向0序列，347个源有序帧位置与236张不同已保存原PNG候选**。逐序原位图号以u32 little-endian复算SHA，和源SPR记录相同；逐图完整SHA/RGBA/尺寸与原RD报告交叉。**本轮重新解码原RD二进制0，新原版权图片0、原客户端/服务端实际运行0。**

**真实六图差异不隐藏：** 本保存的bitmap `113515–113520`（图形号100329）沿用了先前PET06观察页的PNG候选，六幅当前PNG SHA与PET07的*首选*PNG SHA不同，但逐项完全等于PET07原报告已明确保存的`previous_png_candidate_differences.prior_private_png_sha256`。其余**230/236**图片等于PET07当批首选SHA，**6/236**等于历史既存PET06候选SHA；这不等于“236张同一配色全部验证”，不自动覆盖任一版本，更不推断真实游戏颜色选择。全部236张均有原RD SHA、位图ID、已验来源序列及尺寸。

## 私人交付、公开范围与下一步

私人 `StoneAge-INTEGRATION66-four-island-tour-pet-original-pixels-private.zip`：**1,182,803B/SHA256 `a4d84eea13ee9cc3d97a57359112612b1ed6ff06ed523d3fdf956840e79fd961`／242成员**（4份原终点脚本、236原PNG、1私人数字源报告、1离线路线/动作/逐帧观察HTML），已存用户个人Library `/石器时代/`，又独立下载到另一路径逐字节/全SHA/242CRC全部匹配。私人观察HTML未运行浏览器，不虚报观察器运行或原游戏运行。

公开仅保存[完整源编号、原事件段SHA、15 SPR候选与236 PNG来源散列](../../research/recovered/STONEAGE-INTEGRATION66-FOUR-ISLAND-TOUR-15-PET-TW1-ORIGINAL-PIXELS-R1.json)及公开派生数值回归测试；**无原版权脚本全文、原PNG、原HTML、原商用程序**进入Git。GitHub Actions只能验证公开数字/相互关系，私人原字节实读由以上单独核查负责。候选CI和主线CI仅能以后验实际结果记录，不预支成功。

止点已到；**NEXT**转其它尚未专项、可真正取到原文件的地图／NPC／宠物／道具／任务组合，重实体复原，不扩无内容框架、原网服/账号或新游戏引擎。Stage A **7 PARTIAL＋2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、`overall_percent=null`保持。
