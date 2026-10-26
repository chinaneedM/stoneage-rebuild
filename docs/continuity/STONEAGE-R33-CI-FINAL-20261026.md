# R33 最终验收：16份原SAP跨保存样本全SHA相同，八帧原索引来源固定

2026-10-26 连续性协议§14追加验收记录，不覆盖原2,680,510B CURRENT 和历史主簿。实际内容main 8f5dd90839c6c866bcd82943f37be00edcd75ecc，tree 36a50a1fd16dcddb44736f99485ca36f9cf3eb31；全部原始CURRENT blob 031c76a5a8e431f646853909bb2f2e11e6328cd2 未变。

本次一项实质跨版本来源联接：TW1.0 authenticated 原 Redump 文件与尚未官方纯净鉴真的台8.5保存样本的 16/16 原SAP文件大小708B、逐号SHA256全部相同，R30原八帧索引原RD SHA与原记录SHA八项再校。TW1.0的Palet_0原指令初始化RGB证据不能回填成TW8.5实际场景选色。

候选分支 agent/r33-palette-same-carrier-20261026 专用运行 https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40341126302 ，job121635791250，实际 completed/success；经fresh主线保护检查后非强制快进内容main，同内容独立运行 https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40341261031 ，job121636266619，实际 completed/success。两者均通过五份source Git blob固定、16套对应关系/八帧对照、反例测试及版权泄漏拒绝。

原程序/原SAP/Pixels未新取或进Git。旧R32一次失败、较早研究原文/并发历史全部保留。R33新增报告 research/recovered/STONEAGE-TW85-PALETTE-SAME-CARRIER-R33.json，最终机器验收 research/recovered/STONEAGE-R33-PUBLICATION-20261026.json。只有确证TW8.5同构建场景调色板loader/选择证据才重开彩色画面归属；现不称原色已恢复、不称具名物种或原服进入世界。

最高NEXT ORIGINAL_WORLD_PLAYER_VISIBLE_CONTENT_PRIMARY_MATERIAL_34：轮转22域玩家可见原实物，优先可验的原世界内容，若无同源主表或具体原件则准确定界止点。任务DD-028本体/永久/运营活动/起源未定四分。P3E BLOCKED；Stage A仍7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79暂停，总体percent=null。此终验收据新提交本身不预称相同HEAD CI已通过。
