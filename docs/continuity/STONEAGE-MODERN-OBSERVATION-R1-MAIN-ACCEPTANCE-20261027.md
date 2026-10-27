# 2026-10-27｜现代离线原始素材观察 R1 主线合并及验收回执

## 目的与范围
本回执仅将《石器时代》历史资源的**现代离线观察工具链**接入主线。用户已明确优先真实进入/观察老游戏，不继续无限补网页NPC文本；当持久隔离 Windows 原客户端环境尚不可用时，现代浏览器有界显示已核对的原始资源像素/帧，并保留繁体台湾、日本、韩国与大陆各版本的独立源身份。未来新游戏默认简体中文UTF-8的DD-030不变。

## 不可修改的来源与Git关系
- 合并前 main HEAD：`565cec85e9dd8139e97b2df4b1d754d103930491`；tree：`6da3843732494d8a4696e372bf6ab603d8611404`。
- 合并源工作分支：`agent/modern-observation-zhcn-r1-20261027`，验收 HEAD：`91214023f9b6dc9d12501cdd5d1d04c0f94fe38e`。
- PR：<https://github.com/chinaneedM/stoneage-rebuild/pull/13>；实际 merged=true。
- 主线合并 HEAD：`573046d14597c6b127b0a529fc66d4e8737169c9`，tree：`1b444d48368586e6b7ee8cd62cb5ed456a558598`。Git父提交恰为上述合并前main和源工作分支；合并不是覆盖旧历史。
- main原始大型 `docs/CURRENT-STATE.md`：Git blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`、tree原字节数2680510，读取完整Git Blob，**合并未改写该文件**。本回执属于协议14约定的日期加法checkpoint，不修改既有历史报告。
- 接受代码变更涉及17路径，核心文件在 `tools/modern-observation-viewer.html`、`tools/scene-original-graphic-contact-sheet.html`、`tools/stoneage_private_sprite_frame_export_r1.py`、`tools/stoneage_private_region_diagnostic_r1.py`、`tools/stoneage_private_scene_graphic_join_r1.py`。

## 实际远端CI证据与失败记录
1. 原工作分支最近严格源验收：GitHub Actions run [40522049076](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40522049076) / job `122251448039`，status=completed, conclusion=success。解码日志明确 Python **41 tests / OK**；Node离线模拟浏览器接收正确来源、拒绝改SHA/误称场景资格/错事件层/解码失败，`SCENE_ORIGINAL_GRAPHIC_CONTACT_SHEET_SYNTHETIC_BROWSER=PASS`；本地图CSP/无网络引用检查 PASS。
2. 较早候选 run [40520326509](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40520326509) / job `122245345236` 曾 **failure**：原新增map探针对60–79碰撞属性特殊编号与后来客户端`>99`显示域的测试边界不一致，41项中3项断言失败。之后分别修正来源工具和单测，run [40520715670](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40520715670) 及最终40522049076已success；**保留早期失败与纠正原因**。
3. 合并后main的同一现代观察专用工作流 run [40522528120](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40522528120) / job `offline-observer` 的jobs实际读取为 completed/success，包含 Python 资源/历史主张限界、Node假浏览器和离线安全三个步骤。其他因合并触发的独立历史工作流不得借此单个工作流的成功预支验收，分别按最新实际Actions状态判断。
4. 所有上述Python与Node都只使用**合成数据**，不是此会话再次下载/执行老客户端、读取后代763908374字节REAL原件或亲眼观察真实村庄。独立源文件与PNG的实际私人视觉资格**仍OPEN**，不把成功的合成CI写成成功进入老游戏。

## 交付能力及严守的边界
- 使用 SHA 引证的TW1原帧时，浏览器逐PNG SHA核对导出清单及台湾原盘四文件固定指纹，混入后代资源时标记人工拼接；默认UI使用简体中文。
- 后代地图DAT(761)/LS2MAP(65)分离，事件层不造假。私有地图按`map_number`读取同保存材料`adrn_15.bin`→`real_15.bin` 的RD图像块，只导出最多16个非特殊候选ID的灰度索引图；缺映射、重复编号、图像尺寸异常必须显式OPEN。
- 现代原图观察册只能从本地文件选择框载入由此工具形成的清单与PNG，检查固定原始资源SHA、逐图像SHA和实际浏览器解码后并排展示。它**不是同构建已认证的地图原绘制语义、调色板、遮挡、坐标投影或游戏实拍**。
- 公开Git不储存原商业EXE、地图原payload、REAL容器、原宠物图、BGM/WAV和他人版权原图。播放器没有自动外连或后台商服连接。

## 明确未完成与下一最高优先级
**原客户端真实世界进入仍未完成**：此前真实TW1 `sa_3.exe`在Wine32/ACP950/Xvfb8bpp环境只观察到登录画面，尚无选角、移动、NPC/宠物、战斗、声音在游戏内触发的见证。Windows2022 P3F的ACP1252负面结果不因现代观察工具主线通过而改变。

`SCENE-RESOURCE-OBSERVATION-02`：取得可持久访问的已SHA固定后代地图和ADRN/REAL真实字节，在私有目录实际生成**一个**小视口的候选原图并由观察者真正查看；若缺持久原载体、同版绘图选择、调色板与透明语义，分别标OPEN，不得让合成清单代替源事实。同时不放弃原版客户端在独立ACP950/8bpp/输入/无外网+回环虚拟机中实现可操作原画面的最终目标。不得回退无限制搜集NPC文章，也不将地图号码覆盖看作已恢复826张原图场景。

保持Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、DD-028本体/活动任务分离、DD-030默认简体，以及整体复原百分比null。
