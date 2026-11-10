# INTEGRATION38｜主线内容、原证据边界与 GitHub Actions 验收（2026-11-10）

**后验，非原游戏行为认证。** 本轮从 GitHub 远端 main `1165a1fca7584e78d23360cd31c8169ca529482e` 开始，按连续性协议重读原 HEAD、tree、Actions、README、连续性协议、完整历史 `docs/CURRENT-STATE.md` 及源索引。原始 CURRENT 保持原生 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，恰 **2,709,173B**，**未被修改**。

## 本次真正研究到的游戏资料

重新实读私人保管的三份保存原包：
- 原 CHAR01 NPC：995,176B、SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，ZIP **2,205**成员逐 CRC 无失败。八份SBC/JBA真实关联源文件均可按精确路径实取，逐完整字节SHA/CRC一致。
- 原 ITEM01 物品表与台湾1.0零售像素候选：5,868,386B、SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`，ZIP **838**成员 CRC 无失败。原证书2479与2480在两套原物品主表对应原行SHA一致；早期跨载体原图22014/22013的私人PNG整SHA及52×44、52×42尺寸重新核验。
- 原 MAP09：46,844,444B、SHA256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a`，ZIP **4,195**成员 CRC 无失败，内嵌955个原DAT包 SHA256 `c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a`。实读原DAT20712、10913、20704及指定原格；10920缺当前保存的955 DAT档而非历史无图。

由SBC与JBA两份源 CREATE/脚本（早已见于 QUEST01 编目），登记3条独立发证 CREATE、2原脚本共4旧TYPE段；两个独立 WarpMan CREATE/同源参数对应 `ITEM=2479`→10920及`ITEM=2480`→20712。原脚本字面分别有删除对方证件再添加本组织证件的指令，**不等于商业服务器曾实际执行发证/互斥/入场**。不同载体TW1原图候选**不是**同服务器部署证明。历史起源/任务常驻或运营活动类别仍未决。本轮没有新发现先前编目过的脚本、原RD或原始商业同服部署。

## 变更与独立验收的真实后验

- 内容工作分支：`agent/stoneage-integration38-sbc-jba-20261110`，最终提交 `17aa66a39dc97888176a421b9741d6acd0cf31b2`；起点比较恰**5文件**（原版权内容零）：新增专用派生JSON、连续性来源说明、源一致性 Python 反例测试、Actions工作流4个文件，README只在尾部加法新增。
- PR [#306](https://github.com/chinaneedM/stoneage-rebuild/pull/306) 在真正 GitHub 检查后合并。候选 push **24/24** `completed/success`，其中专用 [run 42794084622](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42794084622) 成功；候选 PR 事件 **16/16** `completed/success`，其中专用 [run 42794454811](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42794454811) 成功。
- 合并后内容 `main` HEAD：`affc87f846474f3039d1262315df47037eef5f72`，原生 commit tree：`19b1a9882bbeed32b8472bb5ec520cb2c0f09de6`，完整 tree **7,691项**、`truncated=false`。**本内容 main HEAD** 自己触发的 push Actions **24/24** 实际全部 `completed/success`；专用 [run 42794670814](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42794670814) 成功。未拿旧一版CI冒充本版。
- 本包永久派生 [INTEGRATION38 JSON](../../research/recovered/STONEAGE-INTEGRATION38-SBC-JBA-CERTIFICATE-ACCESS-ORIGINAL-SOURCE-R1.json) Git blob `9263784150281778ddd98e737efd4dde89d7912b`。完整原脚本、原图、原 DAT、私人ZIP不在公开Git；完整 README 前缀保留、新blob `2e213c56d4b543d078d4f955e9e83291af168640`。原 CURRENT blob仍 `c89e0e33537990aa2132b47c40fef49a985a935c`。
- 本记录自身的后续 receipt HEAD 的 Actions **不得**从前述内容HEAD自动推定为成功；只按以后真实运行结果确认。

**Stage A 仍 7 PARTIAL＋2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体完成比例未知。** 并未进入原商业游戏可操作世界，未启动新单机游戏设计、引擎或网络服务。

**最高 NEXT：** 此源组织已经有界闭合；下一轮先从现存已取得的不同内容载体找**真正有材料差异、尚未形成实物来源关联、或可新增实际原像素**的宠物/场景/NPC/原任务/装备模块。没有新原原件或有意义新关系时立即记录欠源，不靠重复散列、空目录扩张来制造“完成度”。官方同源新版本、原生发证执行/互斥/通行见证到达后才重开此组。
