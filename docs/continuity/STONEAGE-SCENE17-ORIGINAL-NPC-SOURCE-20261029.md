# 2026-10-29 — SCENE17 两个原 NPC 文件定点取证

依据最新main `cf9b7f261348313e452045da747a74ba06922265` / tree `f472e198732faa13e153c362d66004d48e3b651b`，远端协议/完整 CURRENT/README/路线和SCENE16已复查；R18 全文件目录证实要找的两个原成员存在且 SHA 固定，但SCENE16此前只证明文件清单，未读原文件。

**目标**：仅在已知社区保存 mixed2.5 原RAR中通过约束 HTTP206 范围取 `npc/genout/1000npc_m.create` (4413B) 与 `npc/genout/npcgen.template` (4950B)，真实读出出生矩形与模板函数；不下载361MB完整包，原版权脚本原文/人物像素不进公开Git。运行场景不是台湾1.0官方原服务器。

**链路**：复用已有R36/R46已在真实源任务验证过的Mediafire分卷、稀疏RAR头扫描与隔离成员提取。整原文件长度+SHA256、RAR CRC、unar 与libarchive逐字节同一才交给 SCENE16 真正解析。目标floor1000/(63,103)的条数可为0/1/多条，所有分支都必须保留；没有可验结果前不预填NPC身份/中文名/互动/原地图帧。范围上限32MiB/512请求、10000头。原件、原对白、声音、图像禁止作为Actions工件上传；仅源派生 JSON、原range/文件哈希及负例检查。失败必须保留原因，不转成已取原件。

**止点**：完成一次真实 source Action，并独立读取报告和运行日志，决定图像实物联接或按协议13轮换22域。有原件同包数值键也不能替代原生图片或同官方服证明。当前 Stage A7PARTIAL+2OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、总百分比null。真正原版客户端世界尚未进入。
