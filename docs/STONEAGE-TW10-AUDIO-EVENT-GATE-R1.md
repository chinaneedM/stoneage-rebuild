# TW10-AUDIO-EVENT-SOURCE-GATE-01 — 原台湾1.0播放接口与音频原盘源关联

2026-10-18。唯一历史事实源为远端main `1e5b2470da55e99e662b7c15cef3e2db45e3be72` / tree `c6445725d41d6737aae039ecb904c4dafa3fc9ae`；地图内容T03已经完成主线归档验收。此次是**原始编译客户端实际音频接口入口的有限技术核查**，不是“音乐应该对应什么村庄”的设计，也不是再录一遍114+116+11音频文件表。

## 已在本仓库存在的物理声音源，不当作本次新增

`research/recovered/STONEAGE-TW10-AUDIO-DATASET-R1.txt` 源Git blob `094becbc92397ee8abf72a014deffffabc97a316` 来源于接受的Waei/JSS台湾1.0原零售盘：`soundaddr_1.txt` 索引114段、`sound_1.bin` 长3695418字节，独立`data/se`目录116个SFX WAV和`data/bgm`目录11个BGM WAV。114段中107与独立同名WAV逐字节相同、1个声音PCM相同但容器元信息有差异、6个PCM不同；另两个非索引wav 91/92与容器01/02记录逐字节一致，早在2026-09-19已经识别并存档。**不得将这些旧事实算本轮新音效发现**。

另有原编译运行体导出的`STONEAGE-TW10-RUNTIME-SOUND-R1.txt`，已观察`sa_3.exe`从`WINMM.dll`导入`mmioOpenA/mmioRead/mmioAscend/mmioDescend/mmioClose/mciSendCommandA` 6项，并从`DSOUND.dll`导入一个ordinal #1。这只证明静态导入，不证明具体播放对象和发生场合。

## 本次新实证任务

工具`tools/stoneage_tw10_audio_event_gate.py`以原零售盘`STONEAGE.bin`（经过指定原发行archive的MD5/SHA1认证）暂时提取原文件`StoneAge/sa_3.exe`，再次验证已固定的原exe SHA256，然后解析PE导入表、用Capstone扫描实际 `.text`内CALL/JMP到WinMM/DirectSound IAT条目的地址，以及通过直接转移连接这些导入跳板的调用者。每条仅输出 RVA / API 名称 / 入口种类 / 出边，绝不上传原可执行文件字节或反汇编正文。并记录少数原盘声音路径字符串的已见位置，**文件名存在并不等于该段代码实际将某文件绑定到哪个事件**。

验收标准：真实源动作、链接范围及其指纹经独立Actions运行并将派生JSON永久归档；若找不到任何原实参链，则只接受 **原客户端播放API结构存在**，不得按论坛猜测指派“某首村庄BGM”“某只宠物攻击声”“登录音效”。人类记忆可供未来设计，但不是编译可认证选择链。

**缺失的同版证据**：音效文件索引→音源编号→播放函数传入值→事件触发条件（场景、宠物、战斗、登录）及游戏实际运行时的显示/声音行为。本次审查不生成完整音频重现、不拷贝音频文件、不开始单机新作，也不改变Stage A九族7 PARTIAL+2 OPEN／Stage B GATED／R79 PAUSED。

**下一有界任务** `PREPRODUCTION-CROSS-DOMAIN-MATERIAL-EVIDENCE-REVIEW-03`：在T01～T04原资源项目完成后，核对真正可用的地图/人物/宠物/NPC/剧情/外挂/资料站等域的实体来源缺口，优先只做能改变历史内容恢复结果的工作，不再无限拉长源代码API树。
