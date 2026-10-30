# O10 远端主线验收及私人保管限制收据 — 2026-10-31

## 真实 GitHub 身份与主线 Actions
- 合并PR：https://github.com/chinaneedM/stoneage-rebuild/pull/68；candidate `a2019aa6c492440d0bdf2f9462ca866ba2d33a97`，候选**12/12** check-runs completed/success。
- 远端实际merge HEAD `2d0c201e180b105371817b357985e4d7f9304215`，tree `c9bb3ca2c470e5a7c30151b343c2dfff7fff263b`，父提交 `699f530c9452a869b8ec1458a947bb45eb51c441` 与 `a2019aa6c492440d0bdf2f9462ca866ba2d33a97`。
- 合并后main在该HEAD的**11/11** Actions都实际 completed/success，以下逐ID保留；O10公开CI不拥有也没有执行私人RD/原PNG。
- `41139606547` `Verify original same-build named-entity source gate R31` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606547
- `41139606555` `Validate Stage A evidence-limited review acceptance` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606555
- `41139606566` `Verify StoneAge O10 bounded expanded village original source (no private assets)` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606566
- `41139606580` `Verify original dated map110 three actual cell values R32` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606580
- `41139606587` `Verify original four village interior materials R34` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606587
- `41139606713` `Verify StoneAge R17 original battle SAB crossversion occurrence conservation` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606713
- `41139606735` `Verify preserved mixed25 full server source conservation R18` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606735
- `41139606739` `Accept preserved original TW85 SPR137 full animation material R28` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606739
- `41139606763` `Verify original local album name material and no master promotion R35` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606763
- `41139606796` `Accept primary-source TW1.0 character creation numeric join R16` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606796
- `41139606832` `Verify original native album table and saved-name joins R36` — `completed/success` — https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41139606832

## 本轮确实恢复的原始内容（严格边界）
- 私人保存混合2.5原1000.DAT（160×160，153608B/SHA 94b19cb59d72b7b48da70d2741ba68516caad970297fd48ed11ef720fa3ea97e），在(55..73,89..113)的475格恢复492原地面/构件布置，183个不同数值图号均找到唯一TW1已认证ADRN+76别名，整TW1 REAL315842228B真实重算SHA后取得183个原RD。第二解码算法、原PNG回读和NumPy/Pillow独立全图像素核对成功。相对旧O4 85图块/55图号覆盖，新增407外部布置/128原图号；不是128种新宠物或NPC。
- 本轮图形可视候选1408×1055，全候选RGBA SHA256 098f369a7c926e6d676abce65c0c6e8407fedf4ff751a0d96689936b64794532。等角排序、Palet_1采色、透明仅有源候选，不保证原游戏当年绘制选择。
- 原1000(63,99)到1001(10,15)以及静态NPC1000(63,103)仍仅是旧保存版配置证据；现代离线页可显示/查源，不是进入原版世界、原碰撞/行走/对话/交易或官方同一构建的实证。

## 真正私人ZIP，公开与保管失败如实记录
- 私人**当前会话内**文件 `StoneAge-O10-private-expanded-village-original-source-20261031.zip`：7764347B / SHA256 `b3f04b571b4b64b654ee4f314a33d6ab1a85e2d8a8ddaf21b2c102fc5a45c197`，888成员，包含183张源PNG、原183RD、183×80B源ADRN记录及整原DAT/原SAP的私人可复核范围；O9原328成员逐文件完整字节相同。独立在最终ZIP里重新解码全部RD摘要/PNG RGBA、源DAT492布置/候选整画面并查ZIP全部CRC，PASS。
- **持久Library写入本轮未成功**：实际files.manage_library 两次都返回 `CONTAINER_SESSION_EXPIRED`，不可把生成会话附件/用户可用下载链接伪称已保存到私人Library。下一轮需用户侧保留该会话附件，或有可用工具时再次从当前私人文件校SHA后上传。
- Chromium对真实 `file://` 原HTML导航有 `ERR_BLOCKED_BY_ADMINISTRATOR`，保存失败；以相同原PNG字节内存浏览器8个实际交互检查成功，0 JS错误、0外部HTTP请求。未证用户机器直接双击一定能打开。
- 公开Git对比PR只有六条文字/测试/工作流/派生JSON文件，**没有原PNG/DAT/RD/商业EXE或完整私人包**。公开CI不会验证图像真实性的原始字节运行，只验证本轮已归档源派生收据和严禁提升的历史边界。

## Continuity 与下一项
- 完整旧 `docs/CURRENT-STATE.md` 精确Git blob `20050acf279a01555ab06a381dfcdc936bd381a6`、2708031B，在主线新tree实际保留不变。本收据为 §14 加法归档，绝非截短替换。
- O10 图块来源已有限闭合。下一最高 O11：回22域寻找确切**同一版本的实体/宠物形态→SPR动作→游戏事件/音效/任务NPC联接**；缺同版主表不能用图片外观或晚版混合服务器猜官方初代的物种/任务/交易。不要继续无界扩大地图截图或旧联网驱动辅助。
- Stage A维持7 PARTIAL+2 OPEN，Stage B及wiki GATED，R79 PAUSED_NON_BLOCKING，原客户端真正进入世界OPEN，overall_percent=null。后验收据自己的新增commit Actions结果必须再次检查，不得提前宣称11项也适用于它。
