# INTEGRATION106｜shop_m3 真原源、30组实际2D候选与93次精确 GitHub Actions 审计验收（2026-11-14）

## 真实发布和完整前后验

- 内容 [PR #395](https://github.com/chinaneedM/stoneage-rebuild/pull/395) 已真实合并：首次候选 `decfae00eca9629015eaee953e868bebb9ebbcc6`，修正后候选 `436388d3e01a762066ad3ef1b66c9d7c50a97b3f`，正式主线 `05272d2dc6e7be3c290f388ce92102f2ffe07fb0`。**修正候选和正式 main 同 Git tree `4ce55125b6a5f319f2bcd74b68094637962027ed`**，相对旧 main `c27d7ecd45ec3ff3a9bab1afd9ba48dc79f7dc00` 仅5个公开派生文件。
- **最初候选46次 Actions：44 success、两次真实 failure**，分别是 [push 43543059692](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43543059692) 与 [PR 43543084310](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43543084310)。专项测试首次错在把布尔表达式与计数比较、错误假设每条原 CREATE 都有外参，以及查用非实际 JSON key。**原商用来源、40条CREATE、28真外参、30张原RD／索引、地图几何和本次配色候选原始摘要均未更改。旧失败 Actions 不追认成功。**
- 修正候选 exact HEAD **20/20 completed/success**：push1＋PR19，专项 [push run 43543235664](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43543235664) job `132288374784` 与 [PR run 43543238783](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43543238783) job `132288383725` 的实际 logs 均为 `Ran 10 tests`／全部成功。
- 合并后正式内容 main `05272d2d...` **27/27 completed/success**，专项 [main run 43543347325](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43543347325) job `132288735203` 实际 logs 亦为 `Ran 10 tests`／全部成功。93个来源审计 run ID、其 event/HEAD/status/conclusion、所有内容的 Git blob 和私人原件 SHA、反例在 [正式机器收据](../../research/recovered/STONEAGE-INTEGRATION106-PUBLICATION-ACCEPTANCE-R1.json) 全量永久保存。**这份新增收据本身被合并后的新主线 Actions 尚未验，不能提前预支。**

## 来源和历史限定

私人 mixed25 NPC ZIP 995,176B SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f` 2205/2205CRC、原 `npc/genout/shop_m3.create` 7139B SHA256 `ae3d1b1939e31f61f3a5273f36e90961d25d8d236ddefef2dc850e0035e5b958`、40 source byte spans/28独立handler SHA真核。12个有资格旧 DAT floor 覆盖38个来源点，另2坐标在 floor5000/6000 没有同等合格 DAT；ordinal24的 floor5105创建格(22,8)与原参数名中的(24,10)冲突永久保留，不修原字、不推行为。

另一真实台湾1.0零售 TW1 P3H ZIP372,626,292B SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` 379/379CRC；24组独立原ADRN-RD候选与6组SPR原动作0方向0首帧，全30RD实际提取、两解码器逐索引同、Palet1候选RGBA/PNG回读同。私人 Chromium 真正40卡/30不同原像加载、楼层过滤3/商店过滤13、0脚本错／0外网；受限宿主 `file://` 被阻挡，实际通过同字节 `page.set_content` 验证，并非原商业客户端渲染。原图/完整原CREATE和商业台词/HTML全部留私人。

私人 `StoneAge-INTEGRATION106-shop-m3-40-NPC-original-2D-private.zip` **215,924B／92CRC**，SHA256 `308e4a6a0cd00af200a7f9208adf9e630413ed5cb53a3cb15e1cf7b10efcb7c8` 已存个人Library并独立再次下载整 SHA/CRC通过。旧ITEM01已目录化13来源商店、旧PET07已有6组SPR等，**本次真实新增为40原NPC静态位置与30原像候选的可查询整合，不是30新原图、同官方build NPC身份或原生交易／游戏世界运行**。floor300原RAR目录有文件但旧不支持滤镜、CRC未验，仍OPEN。

原 `docs/CURRENT-STATE.md` **2,709,173B** Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 未改；Stage A7 PARTIAL＋2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall percent=null。**SOURCE_BOUNDED_ACCEPTED；NEXT** 换非重复真原二维／宠物／任务可见内容；floor300/5000/6000的原 DAT 仅因新原字节与独立CRC验收才重开。
