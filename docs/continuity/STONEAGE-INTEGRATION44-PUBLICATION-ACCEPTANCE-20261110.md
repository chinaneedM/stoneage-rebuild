# INTEGRATION44｜加鲁卡 A1 原图来源与主线验收（2026-11-10）

[原文件取证与历史界限](STONEAGE-INTEGRATION44-JARUGA-A1-ACTUAL-ORIGINAL-SOURCE-PIXELS-20261110.md)、[公开安全派生数据](../../research/recovered/STONEAGE-INTEGRATION44-JARUGA-A1-ORIGINAL-SOURCE-PIXELS-R1.json)、[PR #312](https://github.com/chinaneedM/stoneage-rebuild/pull/312)。

## 真实恢复范围

按仓库协议从 remote main `64eee7feb45e44b76c50d2cce16e0e7b40acf15b`／tree `2f5808dd5b643c3ea9fa5f8d2035bad217b60dca` 启动。历史 `docs/CURRENT-STATE.md` 全部 2,709,173 字节、Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保留、不覆盖。找不到同 SHA 的地图4000原DAT，故明确保留缺口并换用已有真源地图3000；这不是放弃旧原件。

从五份私人保存归档真实核各整SHA、ZIP各成员CRC，另对 TW1 原 `real_1.bin` 315842228B 与 `adrn_1.bin`、`Palet_1.sap` 重读全SHA。混合2.5 `3000.dat` 135008B SHA `3337fb536f3e0938527ac3f6a650427424c20e3a824aae0eb17192fdd177013e`。A1 `jaruga/event/oev.create#1`／地图(99,64)／原 `oev_1`、物品2552→2553。121 原格、132 次高值出现使用73种具有原来源资格的TW1候选RD（原私人I41已有52、MAP04已有20、本轮从纯净零售TW1原REAL实解8335一幅），24低数字仍未知。原人物候选16068同样从TW1原RD新读并双解码，不推原NPC原生姿势/同正式部署。

三幅736×745私人现代场景候选按真实原数值与已验RD透明候选合成，Pillow/NumPy独立全部RGBA匹配并目视；另外现代合成标记、跨保存源人物叠加不代表原生显示。完整私人 85 成员 ZIP `StoneAge-INTEGRATION44-Jaruga-A1-original-source-scene-private.zip` 为 2,035,837B/SHA256 `330e3568d9cba88ed8f42ffa410a29b7f40021aa3860e003fbc6ddc400114df1`；已上传个人 Library `/石器时代/` 并重新完整下载回读，同SHA和85 CRC。私有原DAT、RD、图、任务原文没有入 Git；公开 CI只对有SHA的派生记录/旧 Git blob做回归，不能冒作商业原程序或原服务器执行。原图跨源资格、原调色/层序/碰撞/任务交互未证。

## Actions、修复与真实发布链

1. 首次候选提交 `0d48667ef08b606f699839c60deeced6c462b3f2`、原5个预期文件。首次 **push 26/27 成功、PR 18/19 成功**；专项原失败 [push run 42814050054](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42814050054)、[PR run 42814088330](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42814088330) 各在八项测试中的一项 `KeyError: original_NPC_actor_direction_verified`。原因是**公开专项测试字段名拼错**，实际派生JSON及其证据界限字段为 `native_NPC_actor_direction_verified`；不是原图源读取失败。保留失败历史，未将失败动作追认成功。
2. 第二次修正提交 `b1e96da0db8e049d254c2c2e0fea43dfae4d31de` 只更新 `tests/test_stoneage_integration_module_44.py` 的一个字段名称，派生数据、原源、私人归档及四其它文件全不变。新提交 **19/19 pull_request Actions** 完成成功，专项 [run 42814661311](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42814661311)、job `129824559252` 实际成功；该修正提交因路径过滤只触发 **1/1 push Actions**，专项 [run 42814654036](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42814654036)、job `129824533928` 成功。不得虚称修正提交单独跑了27项push。
3. PR #312 确认基线不变、候选可合并后 squash 合并至 main 内容 HEAD `f371ebcc7b1366a165ca2dfc58b961f3bfd31971`，tree `d72ef15ab69a6cd48cd03b53b8890f146cccebc2` 精确等于修正候选 tree，父提交 `64eee7feb45e44b76c50d2cce16e0e7b40acf15b`。公开派生报告 Git blob `1d2e60acf4613e2b1d44041f3a97697bff0d3fdf`；原历史CURRENT blob仍精确 `c89e0e33537990aa2132b47c40fef49a985a935c`。
4. 该内容主线 `f371eb...` 的 **27/27 push Actions 全部 completed/success**，专项 [main run 42814838629](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42814838629)／job `129825180143` 的八项公有回归真实通过。此验收收据内容尚未在新主线触发测试，不预支收据提交自己的 CI。

## 阶段边界与新 NEXT

本次确实完成一个新的有原来源坐标的 A 路线场景像素+静态任务串接，而非将旧52+20幅重新命名为新发现；当前新地图像素别名**8335一幅**，原人物RD图16068另行新解。地图4000原DAT与原生运行依然 OPEN。

**NEXT：** 延续来源充足且尚未完整可视的 A 路线地图节点，优先原 DAT 真读 + 原图像 + 原任务来源的一组节点，不反复重建源关系。连续两轮无新原内容则停止环岛支线、转其它可取原件的模块。地图库原索引、原生画面行为、官方部署版本与商业原服状态不被现代观察器替代。Stage A **7 PARTIAL＋2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**，总体完成率 null；仅继续 Stage A 历史复原，不进入正式新单机开发。
