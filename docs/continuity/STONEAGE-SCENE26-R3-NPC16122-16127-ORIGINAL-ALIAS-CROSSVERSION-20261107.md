# SCENE26-R3｜16122、16127原NPC图号的跨版本原资源索引（2026-11-07）

承接已验SCENE26-R2四个原导师创建点和CHAR04同RAR的真实原NPC配置，不再复画那四间房。最高新缺口是实际源角色图号16122/16127没有同载体已认证原SPR动画/像素。本轮对已保存在Git的43,632条跨版原字节派生目录逐条查询**逻辑别名**及不同命名空间的**物理位图号**，实际GitHub Action [42383014954](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42383014954) 成功，作业128434443556记录完整原数字与散列，不调用原客户端。

| 原NPC `graphicname` | 台湾1.0保留的逻辑别名 | 原CN50 | 台湾PATCH129 | 物理 `bitmapno` | 原RD尺寸/长度 | 同源RD整SHA256 |
|---|---:|---:|---:|---:|---|---|
| 16122 | 0 | 1 | 1 | 232699 | 32×87；1930B；锚点(-16,-75) | `70e97c406b2ac784a5b0e0cac7906ab8b044f6f4b9ebe14a92b4e727eb250022` |
| 16127 | 0 | 1 | 1 | 232704 | 36×96；2089B；锚点(-19,-85) | `c461402ebd18a9e87277c083f4b62218f99133380b74c26278ef916836aaaeb1` |

每号在CN50 `ORIGINAL_SNAPSHOT` 原块元数据与PATCH129 `ORIGINAL_COMPLETE_OCCURRENCE_TABLE` 中各出现一次，原RD块SHA256一致；正式物理位图号**不是**16122/16127。对物理数值16122/16127的独立查询均0条。16122原块位置748989960，16127位置749001779，只适用于其确切对应原资源载体，不能拿去索引台湾1.0的REAL。源码角色标签仍为`UNKNOWN_RESOURCE_ALIAS`，**未恢复图片或动画，也不证明后期保存版导师使用了该CN50/补丁原图，更不证明JSS1999或台湾1.0角色身份**。台湾1.0保留别名未命中也不等于更早原图必然不存在。

来源验收边界：已保存跨版本原目录 `research/recovered/logical-alias-catalog-r1/` 的原衍生43,632引用压缩SHA256 `3092102e3ee83524ccbf27414ce0cf5bc5579d9a5c8638bfa073f9e62a4db1ea`、REPORT SHA256 `e5dc7249b20a60b13fc4bf12b299d4a6f386fcb928d5d8843017ded58f9c1951`；Git原catalog报告blob `3a694c3e6dc2f8bef291381674c53667c9a60507`，源SCENE26-R2 `3446a7006478a748d2f273c85822df84ace893a0`、源CHAR04 `1c564b07e829bce8360f57e63d32866c03e225e3`。原源Actions job `128434443556`，候选仓库头 `0d70b1d0b9276487166a91615b6eb1226c1d91a3`。公开仅[来源限定结果JSON](../../research/recovered/STONEAGE-SCENE26-R3-NPC16122-16127-ORIGINAL-ALIAS-CROSSVERSION-R1.json)及[来源等价/负例回归](../../tests/test_stoneage_npc16122_alias_original_source.py)，没有上传商业RD原字节/游戏图、没有建立网游或新游戏。旧CURRENT原Git blob保持不变，Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，总体percent=null。

NEXT：只有合法取得并全SHA验证CN50对应REAL或PATCH129原REAL的这两个**确切块**后，才可私人实际解码图像；在此以前不借用TW1其他角色像素冒充导师，不把一个RD块当完整SPR动画。此分支已限定止点，缺原块时返回其他原版任务/玩法内容模块。
