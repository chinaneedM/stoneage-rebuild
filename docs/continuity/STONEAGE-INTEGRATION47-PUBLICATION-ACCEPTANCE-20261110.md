# INTEGRATION47｜波鲁13景来源图、静态任务边及主线Actions正式验收（2026-11-10）

[实际两份私有归档复读、13原DAT/旧现代RGBA候选、78原图哈希、精确来源和限制](STONEAGE-INTEGRATION47-PORU-13-SCENE-STATIC-SOURCE-GRAPH-20261110.md)；[公开派生数值/哈希索引](../../research/recovered/STONEAGE-INTEGRATION47-PORU-13-SCENE-SOURCE-GRAPH-R1.json)；[PR #315](https://github.com/chinaneedM/stoneage-rebuild/pull/315)。

## 证据保管及闭合项

本包以真正远端`main` `fb02be2d380ff6d09e66a02d03b432e8b324e73c`、tree `105732ddbd6702651688285f92753f1148a338cb` 为起点，完整通过原生Git blob重读旧 `docs/CURRENT-STATE.md` **2,709,173B / blob `c89e0e33537990aa2132b47c40fef49a985a935c`**，完整原文保持不变。旧QUEST23、QUEST24公开源原Git blob分别`303bafb317e5d5911c4a9bc23ac4ab90066b9b80`/`c7150d08cace8da3d6b5411036818e1baacb46dc`，全字节重放。私人旧ZIP **58,171,450B/1,014成员/SHA256 `fe6eba160e9df38a4182018fb2c581d2f9cdee1f39fe5cdab3f2a8904580cf6a`** 与 **23,451,751B/578成员/SHA256 `75aad7150fe4ffd4db0da16bc5de92f8ed3c61073beb2fa709a9ad19c8ba83ac`** 本轮重读CRC全通过。

实际13张原DAT全SHA、整尺寸、所有旧现代候选合层RGBA哈希与已验来源逐一一致；59次原NPC配置成员实读SHA一致；913和490台湾1.0零售图片候选号跨两原保管ZIP重读，78个重叠PNG同编号SHA全同、0冲突、并集1,325候选号（不计新图）。已实得mixed25原5509(37,35) WarpMan参数指定5510(16,49)单向关系；5510(16,50)原ExChangeMan MESSAGE无WARP。flag63与64不同`GetPet`、`EndSetFlg`、18544/18558冲突保留。只是有源静态关系，不是原运行、同官方构建或完整世界；原商版权DAT/RD/PNG/脚本全文没有公开。

## 候选／PR／主线真实发布后验

- 候选分支 `agent/integration47-poru-source-graph-20261110` commit `6bac7913bb9c7231a194d06dbb41c47fce66168d`，Git tree `c9212ed198c8dbceecc38c26f3341d1a6c6f3193`。相对起点只有精确五处：README、INTEGRATION47连续性文档、派生JSON、12项正反验证测试、单独工作流。原CURRENT blob不变，没有改旧QUEST23/24。四份新文件Git blob分别JSON `dc349f02b65ee8a78a0a23364654cf82753ed98a`、测试 `1f61c60d5facc6035a60e1b462bde4fc53d8965f`、来源文档 `b9e10a68d0203a90dedafc54b7d6724d68727487`、workflow `699b6128bd80b65eba0f3dfa18adf6fb3c27ad0d`；全部与本地Git blob精确同值。
- 候选push Actions **27/27 completed/success**，专项[run 42824812244](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42824812244)／job `129859253006` 执行`python -m unittest discover -s tests -p 'test_stoneage_integration_module_47.py' -v`成功；PR #315 Actions **19/19 completed/success**，专项[run 42824851944](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42824851944)／job `129859391245`成功。无pending/failure。
- 复核主线仍指向原起点、PR head未移动、可合并之后，PR #315 **squash merged**到内容主线 `b43576e78c1d9da2e5e7ea157698c0a19c82c09f`，tree **`c9212ed198c8dbceecc38c26f3341d1a6c6f3193`** 与候选逐对象一致，父HEAD是起点`fb02be2...`。合并后的**主线推送Actions 27/27 completed/success**；专项[run 42824994174](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42824994174)／job `129859893129`同12项测试实际成功，Stage A审阅工作流同时成功。本验收收据本身若无匹配的新Actions，不预称其亦通过CI。
- 公开 Actions只验证派生索引、固定Blob和不可造假的契约；它**没有**私有DAT/PNG/游戏原客户端输入。真实私人ZIP CRC、NPC SHA、图块字节、DAT/旧RGBA哈希验收属于本轮独立本地操作，不把CI或现代PNG解读为官方运行。

## 止点与下一最高项

波鲁本组13张已存原DAT、1条有源静态WarpMan参数有向边、63/64两组原脚本字面关系到此关闭**本包**，不关闭整个波鲁或原版游戏；缺floor500合格原DAT、没有原服任务执行/反向warp/原官方同版资格。下一最高 **按模块队列移向有原DAT与原图候选而尚无实际来源联接的另一非波鲁区域/NPC或物品任务**，只增加实物可检的内容；若找不到则记录源缺口与停止，不为追新编号重做已闭合任务、无源画图或新引擎/账号。

Stage A仍 **7 PARTIAL + 2 OPEN**；Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，overall_percent=null；原`docs/CURRENT-STATE.md`不修改。
