# 2026-10-27｜最高优先级改为「进入并观察真正的原版世界」

类型：用户明确重排工作顺序、加法连续性覆层。**这是执行优先级与一个有限兼容环境实验，不是已进入游戏的证书。**

## 新的工作次序与目标

用户指出：真正进入原版，观察人物、地图、宠物、界面、战斗、音效，才能可靠地建立后续缺资源表，也能作为未来新游戏设计的体验参考。此前R20→R46偏向原文件/论坛和静态内容主表恢复；从此**原版真实游玩观察是全项目最高优先级**。22-domain历史取证保留为「为进入、表现和确认真实游戏场景所需的有界依赖」，不再自动因最新NPC/技能文本NEXT抢先。

事实分层：
1. REAL_ORIGINAL_EXE_EXECUTED：TW1零售盘原`sa_3.exe` 425984B、SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a` 已在Wine32 / ACP950 / Xvfb8bpp隔离执行；原登录面板单帧已私人解密、人眼实际观察。见P3源40244430667。
2. ORIGINAL_LOGIN_VISUAL_PARTIAL：窗口、自身colormap、悬停高亮已记录，但原色仍失真，QUIT短按/200ms没有观察到有效退出；无windowmode的全屏路径在输入前已崩溃，见P3C。
3. SYNTHETIC_DISPLAY_AND_INPUT_ONLY：Windows2022自编x86程序在256COLOR下GDI/DirectDraw真实8bpp颜色及输入通过，但GetACP1252；没有相同进程ACP950验证，更没有在该Windows环境运行原客户端，见P3D/P3E。
4. WORLD_ENTRY、NPC/PET/FIGHT/MAP/AUDIO_IN_CLIENT：全部OPEN。此前原音频段WAV经解码保存不代表游戏中已听到；已有世界地图模型不是客户端真实场景。后代2.5原始数据不能提升为TW1原游戏画面。

## 眼前唯一实验P3F：Windows Server2022进程代码页

可证伪技术假设：Microsoft解释Windows Server 2022及Windows11的unpackaged应用可由Fusion manifest的`activeCodePage=zh-TW`选择地区代码页；本地先不动商业程序，只编译**两个相同的自编x86二进制**，仅给后一份嵌入该清单，同一Windows2022 runner的DEFAULT、256COLOR、WINXPSP3 256COLOR三设置各独立运行，记录各自`GetACP`、GDI实际bpp、DirectDraw GetDisplayMode，作为对P3E「1252」障碍的一次严格有限复测。<https://devblogs.microsoft.com/oldnewthing/20220531-00/?p=106697>，<https://learn.microsoft.com/en-us/windows/win32/sbscs/application-manifests>。

交付：`tools/stoneage_p3f_zh_tw.manifest`、`tools/stoneage_p3f_manifest_probe.py`、`tests/test_stoneage_p3f_manifest.py`、`.github/workflows/probe-stoneage-original-world-p3f.yml`。源工件仅为自编程序的数值JSON、无商业字节；独立负控阻止将设置字符串/命令返回、合成32位编码及环境测试误当原游戏成功。

只有**同一自编x86进程**同时观察到GetACP950、GDI8bpp和DirectDraw8bpp，才算P3F受限候选；仍需P3G将原P3E的精确RGB/截图像素、Win32输入消息接收与进程隔离在相同繁体代码页条件下联合认证。若不通过，在一次有界失败结果后停止Windows清单分支，明确需要可管理的ACP950开机虚拟机环境；不得重复盲测或反复下载0.84GB旧光盘。

## 真正的原世界体验验收顺序

1. **P3G同进程兼容资格**：显示真实RGB、聚焦、点击down/up与长按、DirectDraw、ACP950、无外连/只许本地回环；受限沙箱。现有P3E只分别证明部分功能，不能拼成一例。
2. **P3H原客户端可操作登录/选角**：取得SHA一致原exe、375个原运行文件，核无篡改、封闭外网、可看正确颜色，记录原启动窗口及按钮确实响应；不用真实历史账号/密码。
3. **P4原版客户端的本地离线世界**：先从原客户端协议的已认证字段找出本地测试回环最小链。只用隔离`127.0.0.1`自编演示服务；不能联网连不明商业服务器/私服。没有经证实的包字段或起始地图不得自称历史服务器复活。能实现则认证角色选择→原地图实际出帧→操控移动→原NPC/宠物画面→遇敌/战斗→音效实际触发。每一步用原程序自身画面、源身份、动作时间、声音观测和不可伪造的程序/报告SHA验收。
4. **观察驱动资源清单**：仅当亲眼观察得到新问题时，有目标地提取TW1同版图块、SPR/RD、BGM/SFX、NPC/物品/任务；后来版本一律明确后代来源。原版世界没进去之前不得将现代离线播放器画面标为游戏实拍。
5. **设计借鉴单独列账**：本次任务是原版观察，不开始生产新游戏；未来体验拆解保留「实际原版观察」「后来版本补充」「设计构想」三种标签，避免将推断写成童年原版事实。

当前阻断：不存在已验证的可用8bpp+ACP950+完整网络隔离、输入与颜色同环境，以及原TW1历史商业登录服务不可用；私人原盘持久保存也未配置。无可靠总体恢复百分比，Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、DD-028本体/运营活动任务分立均不因用户重排而假称已关闭。**下一最高：P3F实际源Actions评估；通过则P3G；失败则集中建立可启动ACP950的隔离虚拟机，不返回低收益任意NPC/宠物资料轮转。**
