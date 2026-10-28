# 2026-10-29 — SCENE17 两个原 NPC 文件定点取证

依据最新main `cf9b7f261348313e452045da747a74ba06922265` / tree `f472e198732faa13e153c362d66004d48e3b651b`，远端协议/完整 CURRENT/README/路线和SCENE16已复查；R18 全文件目录证实要找的两个原成员存在且 SHA 固定，但SCENE16此前只证明文件清单，未读原文件。

**目标**：仅在已知社区保存 mixed2.5 原RAR中通过约束 HTTP206 范围取 `npc/genout/1000npc_m.create` (4413B) 与 `npc/genout/npcgen.template` (4950B)，真实读出出生矩形与模板函数；不下载361MB完整包，原版权脚本原文/人物像素不进公开Git。运行场景不是台湾1.0官方原服务器。

**链路**：复用已有R36/R46已在真实源任务验证过的Mediafire分卷、稀疏RAR头扫描与隔离成员提取。整原文件长度+SHA256、RAR CRC、unar 与libarchive逐字节同一才交给 SCENE16 真正解析。目标floor1000/(63,103)的条数可为0/1/多条，所有分支都必须保留；没有可验结果前不预填NPC身份/中文名/互动/原地图帧。范围上限32MiB/512请求、10000头。原件、原对白、声音、图像禁止作为Actions工件上传；仅源派生 JSON、原range/文件哈希及负例检查。失败必须保留原因，不转成已取原件。

**止点**：完成一次真实 source Action，并独立读取报告和运行日志，决定图像实物联接或按协议13轮换22域。有原件同包数值键也不能替代原生图片或同官方服证明。当前 Stage A7PARTIAL+2OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、总百分比null。真正原版客户端世界尚未进入。

## 实际来源执行后新增证据（源报表永久化前的有据事实）

来源Action [40789416440](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40789416440) / job123170623106实际 `completed/success`；原件稀疏请求184个/12,013,836B、扫描7,954头，RAR来源两成员逐完整SHA/CRC及unar/libarchive字节一致：创建文件4413B/SHA `c9b000a836b0aae3d88358097039f1beea020d92ba84f6ccc338bb54bc478240` /CRC2981039746；模板4950B/SHA `0c5a58d5e31cafd3b58ccc1fa88fee7d1f95d12c0b87b04db9f06fea3b2a4df3` /CRC1448375672。读取的是原**社区混合2.5保存包成员**，不是台湾1.0或商业服务器同部署验证，未重新核全RAR SHA。

原 `1000npc_m.create` 共25块、`npcgen.template` 共41块；唯一目标创建块 ordinal1/字节[287,450)，块SHA `bbc86e2ab64fa20e8f6702ee11e97c9ff659041c62fcf257bb8d16b2f06a4ce7`，floor1000、borncorner(63,103,63,103)、graphicname16048、dir4、createnum1、time0；其`enemy`引用的准确模板token `npcgen_man`在实得模板唯一命中`TownPeople`，模板块SHA `5f24ae6f815471af9439ed4b824ae494006a8ba6fb7e4bac43b44b8ae5a89b29`。姓名原值只保留8B/SHA `b66523220d17805c9e6b91cff10209eef1b1a4161fa2c3c17c09c6efa7a89959`；未公开原NPC对白或脚本。目标位置与SCENE15现代落点1000(63,99)位于同地图，但不能推原游戏可达/碰撞/遮挡/互动或官方身份。

源Action上传了仅派生 `scene17-derived-original-source-only` 工件id12861201262，API报告ZIP sha256 `81af6d0d12d816bf39630516d84dc96050927c4077325130d25d100b2dd966db` /大小11,979B；**本轮未独立下载工件ZIP，不冒称本地重哈希**。现将源日志里完整JSON范围哈希、原件偏移、CRC、独立解包见证存档 `research/recovered/STONEAGE-SCENE17-ORIGINAL-NPC-SOURCE-R1.json`，并添加15条正反例专用校验。候选/main CI及Git blob后验必须按实际观察另记。本报告是实物新增NPC创建**配置**，不是原客户端人物画面、真实聊天或进入原版世界；总体复原进度仍null。

## SCENE17 主线合并与真实验收后验

[PR #33](https://github.com/chinaneedM/stoneage-rebuild/pull/33) 正常合并主线 `e418e15e459192f64216539d642f774f3febe670` / tree `e5483a0e8ea547f8a31c542ae79966d65961a73b`。原源码候选 b642458、报告候选2ec11085、最终README增补候选8f3a8a逐段保存；最终候选11项 Actions 实际completed/success，主线同一内容11项 Actions 全部 completed/success；主线专用源派生验证运行ID40789937189。候选源派生校验实测35项通过；无原脚本运行/登录/官方身份晋升。

独立从源运行日志的JSON重新解析、与主线已归档报告结构逐字段一致。完整派生报告Git blob `1b8b82f4f0df5b69c2af14f538164399efc7b473`；临时ZIP仅GitHub API报告SHA（未本地独立下载）。详细source/candidate/main run IDs、CRC、审计边界、五份未改历史blob见 `research/recovered/STONEAGE-SCENE17-PUBLICATION-R1.json`。本后验提交自身 Actions 未观察前不得宣称成功。最高后续任务为同载体16048图形原像素的有限资格证明，缺原素材应明确停止转22域，绝不反向虚构官方NPC名字或对话。原本体世界未进入，Stage A/B/wiki/R79和完成率null不变。
