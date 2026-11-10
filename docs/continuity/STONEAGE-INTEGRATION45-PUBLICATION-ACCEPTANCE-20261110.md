# INTEGRATION45｜环岛A3/A7/A11原场景公开派生证据与主线验收（2026-11-10）

关联：[实际原数据、像素、负证范围](STONEAGE-INTEGRATION45-JARUGA-A3-A7-A11-ORIGINAL-SOURCE-SCENES-20261110.md)、[只含数字及SHA的派生索引](../../research/recovered/STONEAGE-INTEGRATION45-JARUGA-A3-A7-A11-ORIGINAL-SOURCE-SCENES-R1.json)、[PR #313](https://github.com/chinaneedM/stoneage-rebuild/pull/313)。

## 远端与材料验收

远端起点 main `182ccf89632cf9f800bc70dd6c2c6e151e91dce4`，完整 tree `f66f7fb28e996b2d3c549f2edf32d68804bba3f8`，历史 `CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`（2,709,173字节），**未修改**。重新整包 SHA/CRC 读取 I41、MAP04、QUEST25、原 TW1 P3H 与 I44 共5个私人源包；原TW1 ADRN/REAL/Palet1三个成员整 SHA 实读，三份 mixed25 目标原 DAT 与任务CREATE／脚本原成员分别实读并按旧Git来源索引逐 SHA 匹配。

新增三个真实原DAT坐标场景：A3 `20105/(25,49)`、A7 `20301/(238,118)`、A11 `20601/(5,11)`；**363个原格、264次高值图引用全部有源、跨窗108个不同原图号、215次1–99原低值不解释**，不是264/108个新美术资源。三处原script `oev_3/7/11` 的任务字面2554→2555、2558→2559、2562→2563与各自CREATE具体 SHA/TYPE段索引一并可回归。原 TW1 `16067` 人物RD新实读双解码与保留原 `16068`再次逐来源SHA复核；二者只作跨版本同编号图像的静态候选，不认证原角色实际动作/表情/部署身份。

三张场景各层0/层1/合层共9幅现代像素画布实际由原数值与原像素候选拼合，主方法Pillow与独立NumPy位图重叠精确一致；再用第二个独立 Python 程序从交付ZIP内三原DAT与108种源图重读、不同对角线枚举顺序逐位置合成，**9幅RGBA SHA与已记录候选完全一致**，另有3种坐标标记和跨版本人物叠加私人候选。实际已目视A3高崖、A7岩地/植物、A11洞窟岩场景，但合成透明背景、层次和原始客户端实际画面不是同一事实。

私人归档 `StoneAge-INTEGRATION45-Jaruga-A3-A7-A11-three-original-scenes-private.zip` 实际大小 **5,098,689B**、**132项**、SHA256 `a705e963612ce24177940feebe9f7d4225a4bbc83af2197624af31bb5350d018`，私人源报告序列化SHA `f054f24869c107566c33eda3487bf5b56e586a4adb9535ede84a35741cf90312`，保存个人 Library 的 `/石器时代/` 后重新取得全ZIP，整字节相同且所有成员CRC成功。**原商业DAT、RD、PNG、原事件正文不进入公开仓库**，只发布来源数字/散列、回归测试、工作流与连续性记录。

## 真实 GitHub 提交、Actions 和独立验收

- PR #313 的候选HEAD `0f549fd2ce6a95708ad400311b551511c350ffd3`，tree `555cd15144148fa57cf47bfd050cf96c3ae8e7e9`；仅5个预期路径：README、docs加法连续性、research派生JSON、tests专项Python、.github专项工作流，没有对旧原件/历史文档删除覆盖。
- 候选HEAD **27/27 push Actions completed/success**，包含 [专项run 42818452933](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42818452933)／job `129837486224`，实际执行专项unittest成功；**19/19 PR Actions completed/success**，包含 [专项run 42818505849](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42818505849)／job `129837667648`，专项unittest成功。此次没有失败动作需要回写为成功。
- PR #313 验证 main 没变化与 mergeable=true 后采用 squash 合并。内容 main HEAD `3dca3da1305f8551dcd8b91dd13da18610155fd3`，tree `555cd15144148fa57cf47bfd050cf96c3ae8e7e9` 与候选一致，父提交即开始时旧main `182ccf89632cf9f800bc70dd6c2c6e151e91dce4`。公开派生报告 blob `776810890b1f6f4941c827eedd37252344af40cd`，历史 CURRENT blob核实仍精确 `c89e0e33537990aa2132b47c40fef49a985a935c`。
- 合并后此**内容**主线 `3dca3da...` 的 **27/27 push Actions 全部 completed/success**；[专项run 42818634340](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42818634340)／job `129838108611`实际执行专项测试成功。本收据追加 HEAD 自身不预支CI，即使没有新匹配Actions也不称其已独立验收。

## 下一真实源目标与严格界限

同保存的 INTEGRATION10 ZIP（5,759,006B SHA `7a4b74af4ca4b0cca3108dcdec55bb9f1892a2edf17b73d400aab4c041fa6b96`）已真读地图 `source/3400.dat` 86,408B/SHA `a3c6918ba21c909e6312329c936615aa6b6d8800d7967ed85a2146d55ca263c4`，原 A12 (69,61) 的 **135次高值引用／69种图号／21次低值**仅初筛原图候选没有缺号。本轮尚未实绘 A12，更没有原生客户端运行认证。

**最高 NEXT：INTEGRATION46 / A12原DAT＋静态原任务与实际2D画面独立核验。** 地图4000及A2/A8/A9缺本轮原件仍 OPEN；请勿以某图的坐标、逻辑图号、现代图集或脚本名称假定早期官方同服、原程序交互、原游世界已可运行。Stage A **7 PARTIAL＋2 OPEN**，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null，项目尚未转入新单机开发。
