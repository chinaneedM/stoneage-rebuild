# O11 主线 Actions 完成的最终验收回执 — 2026-10-31

## 远端后验
- GitHub 仓库 `chinaneedM/stoneage-rebuild`、[PR #69](https://github.com/chinaneedM/stoneage-rebuild/pull/69) 真实合并。
- 候选 HEAD `32134b0e207595a2d878e5474e85dea5e3056835` 的 12/12 GitHub check-runs **completed/success**；包含专门 O11 的24项合成来源反例和常规原数据边界。
- 主线合并 HEAD `2fad0a9a1001a2ac6e0244d82417473190c9fe6a` 的 11/11 GitHub workflow runs **completed/success**，包括 O11 专项工作流；不是从候选结果推断。
- 合并树 `c468ca4735acec1b9d0f6c687076c1aba7dd2f6a`；前序保留的排队快照 HEAD `fcd2196fae41262f8d95bf88fa298025a7f3c311`/tree `0ce3f1472300e0f04cac3d80ebe426aff5566932`。队列曾全部queued，其历史准确保留在 `docs/continuity/STONEAGE-O11-POSTMERGE-QUEUED-20261031.md`，本收据是**后来的真实后验**而非修改旧记录。
- 远端 `docs/CURRENT-STATE.md` 原完整 blob `20050acf279a01555ab06a381dfcdc936bd381a6` 保留，未截断。

## O11来源、实物与未证语义
- 原TW1 `spr_1.bin` 编译资源：464组、39065动画、242085帧位置；有据三个数字组 action0 24条动画、352帧与mixed25保存帧全字节逐段一致，24个字段73、24个字段10000，304个0。208幅RD源图片经独立TW1原ADRN/REAL解码及候选色表RGBA重播，208/208与此前保存的同数值原PNG逐像素同一。
- 73究竟是否音频编号、零基/一基选择、10000的意义、具体宠物实体名称、实际游戏动作/战斗技能、碰撞及原初代官方部署身份仍**OPEN**。两原SFX候选 `sam_18.wav`/ `sam_17.wav` 只能在私人页手动比较，**没有自动绑定/原始程序执行/真正世界进入**。
- 私人216成员 ZIP 1145869B、SHA256 `a972f91257bef896a07e436727072d8341940c570386b6e9282b4e8d2892f811`，私人 Library 路径 `/石器时代/StoneAge-O11-private-sprite-frame-sound-candidate-20261031.zip`，上传成功且Library二次完整SHA回读一致。原PNG/WAV/RD/商业EXE不进入公开仓库，现代HTML非原游戏程序。
- Chromium以相同原PNG/WAV内存页面验证24序列/48非零字段操作、两WAV手动AudioContext解码、0 JS错误/0外网；`file://` 管理员阻断保留，不能认作用户本机一键原游戏启动。
- 公开 SOURCE 账本 `research/recovered/STONEAGE-O11-NATIVE-FRAME-SOUND-SOURCE-R1.json` 和 `STONEAGE-O11-TW1-208RD-PIXEL-AUDIT-R1.json` 只含派生数值、摘要及严谨反例；公开CI不会读取私人原源。

## 已实际通过的主线运行（原HEAD 2fad0a9a1001a2ac6e0244d82417473190c9fe6a）
- [41144089539](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089539) — Verify original same-build named-entity source gate R31 — completed/success
- [41144089478](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089478) — Verify original dated map110 three actual cell values R32 — completed/success
- [41144089470](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089470) — Validate Stage A evidence-limited review acceptance — completed/success
- [41144089464](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089464) — Accept primary-source TW1.0 character creation numeric join R16 — completed/success
- [41144089445](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089445) — Accept preserved original TW85 SPR137 full animation material R28 — completed/success
- [41144089439](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089439) — Verify original four village interior materials R34 — completed/success
- [41144089438](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089438) — Verify StoneAge R17 original battle SAB crossversion occurrence conservation — completed/success
- [41144089407](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089407) — Verify preserved mixed25 full server source conservation R18 — completed/success
- [41144089399](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089399) — Verify original local album name material and no master promotion R35 — completed/success
- [41144089392](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089392) — Verify original native album table and saved-name joins R36 — completed/success
- [41144089389](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089389) — Verify StoneAge O11 native source animation and bounded sound-word candidates — completed/success

## 延续条件
Stage A **7 PARTIAL+2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，`overall_percent=null`、原可操作游戏世界未进入。下一最高 **O12**：优先有同版本实体→动作→音效/技能/任务事件触发实参或主表的原字节来源，缺件必须有界止点再转22域其它真正游戏内容，不要反复加地图截图或泛用驱动。未来新游戏简体中文单机需求不等同于原素材可以未经许可商用或公开分发。

本最终收据新增提交本身的 Actions 状态须再核，不能提前称其已跑11项。
