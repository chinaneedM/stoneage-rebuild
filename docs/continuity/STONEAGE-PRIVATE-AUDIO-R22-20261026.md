# 2026-10-26 — 单段原WAV私人交付R22，模型听觉仍受限

协议14加法连续性覆层。fresh main `e44754afab9054383debb992ee6b83c7b62a9454` / tree
`8ca806b0bd54211f4354874e9b056a4f75880a46`，599分支完整分页、5911项未截断tree、
无AGENTS、0开放PR/运行中；最新R21收据40277086242实际success。10-07无关旧queued
37642417333保留。七启动文件完整Git字节重新读取，逐blob与远端tree核对，另读路线/
R102材料portfolio及最新R20/R21覆层；不依据旧聊天SHA。CURRENT2680510B、blob
`031c76a5a8e431f646853909bb2f2e11e6328cd2`、SHA256
`f02f85b837fc09973cb2eca33f7daf4db547a77cb35a81a9576c6308f70142c0`及另外四大历史
文件完整原样保留。CUSTODY保留全部启动指纹。独立工作树保护原目录已有不相关修改。

## 本包目标和止点

最高ORIGINAL-AUDIO-PRIVATE-AUDITION-22：只取一段已有来源、哈希和PCM记录的原WAV，
验证私人持久保存、独立完整回读、真实可解码及试听能力。没有完整可用能力就记录具体
阻塞，不扩声卡/驱动helper、不重拉TW1整盘，不把文件结构当“已听到原游戏声音”。
结果有两个层级：**一份可下载试听的原样私人WAV已交付；助手实际收听仍未成立。**

## 真实原来源：一次有界取源，不是新版本

源HEAD `17be8ff3b712b9f4c0c6d4c2bb4a46abd4d796fe`、tree
`a87bf2cee5dd3962b02ea550a92a178bbdb78abe`，Action
[40309396706](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40309396706)、
job121526494995实际completed/success。复用已验证Stoneage-5网上保存载体，仅读取
8MiB逻辑CAB前缀（原扇区范围65856–9699647/733057248），不是完整733MB盘或612MB CAB。
前缀SHA87973df3…与既验固定值相同；cabextract只静态提取soundaddr_3.txt和sound_3.bin。
691B表SHA5afc6a80…、2696934B容器SHAf5c0b5b0…均完整一致，重新生成的27表项/三重
相同段报告与R15永久报告语义完全相等，旧波形结构不是本轮新发现。

它仍是保存的CN5载体样本，未认证纯净官方发行/原部署build，也不是TW1原声音。
R15证明此容器内容与TW8.5保存包等有关系，不因此混成同版场景/宠物事件。
原游戏程序执行0、原游戏音频设备播放0。

固定选择表index0/offset0的`saam_01.wav`，没有从文件名猜声音用途：

| 原样字段 | 实测值 |
|---|---|
| WAV完整长度 | 27180B |
| WAV SHA256 | 58b036717914ad27682dde9c5e797d8a043381a9000154ac4bcbf6b84fd09454 |
| PCM格式 | 单声道、unsigned8、22050Hz |
| PCM样本数/字节 | 27136 /27136B |
| 时长 | 27136/22050，即1.230657596371882秒 |
| PCM SHA256 | afa24f1f1b94806a6717962d7cfedf64de7985fb2c672f5437eb3e0ccfbab0e3 |
| unsigned样本范围 | 73–190，22752个样本不等于128 |

范围/非中点计数只是信号测量，不作“动物叫声”“人物/攻击音效”或主观听感描述。
没有拼接、归一化、重采样或更改原WAV头。

## 私人传回、保存和独立回读

新增窄范围WAV传输，独立于原PNG专用守卫，后者没有放宽。源runner以本轮公钥使用
X25519/HKDF-SHA256/AES-256-GCM加密单段WAV，AAD认证媒体类型/原长度/SHA/接收公钥。
私钥只在私人工作目录，公开Git只有公钥、代码及派生元数据。runner先清理原表、容器
与稀疏CAB，再上传派生JSON和密文JSON。没有明文WAV进入公开Actions工件或Git。

工件12643539813，ZIP29221B，实下SHA256
`89b2cebf90956b7bb159c84fa812183227e7eaea6a8724e8ed97bae51fee5952`与API一致；恰
r22-audio-derived.json/r22-audio-sealed.json两成员。原样派生2555B、SHA256
`453f473aa366e2fce4be1fa841d0d19e5d5ed19f7e50fbe19a7ff3e0c7147482`永久入Git。
密文完整摘要/接收公钥摘要/源run-job-steps保留在
[CUSTODY](../../research/recovered/STONEAGE-PRIVATE-AUDIO-R22-CUSTODY-R1.json)，密文及
私钥本身不进Git。解密成功后WAV/PCM摘要均与源报告和旧27项报告一致。

文件`stoneage-cn5-saam_01-original.wav`已保存为用户私人文件，随后通过独立读取路线
取得新副本，27180B逐字节等于解密后的原样WAV；完整SHA/PCM再次相等。私人文件ID、
权限传输参数及私钥不写公开库。一次小文件的实际持久保存不代表商业大包存储容量/
限制已解决，原大包私人保管门槛继续保留。

FFmpeg6.1.1独立读取回读文件，成功解码为54272B signed16 PCM；逐样本恰等于标准库
wave所读unsigned8经`(sample-128)*256`的对应整数，完整SHA为
`a0a81907a4f04155c295b0ea8487f92011f7d38bf3015cb983e3e1c4e95fe8dd`。
这是全部27136个样本的解码比较，不是播放器或耳朵听过的证据。

## 实际试听能力限制，不能被解码成功抹去

确实将同一原样WAV送到当前会话音频输入/呈现接口。返回原文：
`audio content omitted because you do not support audio input`。
所以本会话**没有取得模型可听的音频输入**，助手未声称已听到、识别或评述此音色。
文件链接可供用户下载后试听；未收到用户播放确认，也未验证当前客户端播放器实际
开始播放，三者分开保存：

- 私人原样文件保存/全量回读/独立解码：已验证。
- 模型实际收听：受当前输入能力阻塞，未验证。
- 用户实际播放、原游戏设备/事件/场景联合播放：均未确认。

源报告仍原样保留private_storage=false等**源runner当时**状态；本地后续成功保存与
模型输入阻塞另记在[交付报告](../../research/recovered/STONEAGE-PRIVATE-AUDIO-R22-DELIVERY-R1.json)，
没有改旧报告把源执行写成已播放。最终状态
`PRIVATE_ORIGINAL_WAV_AVAILABLE_ASSISTANT_AUDIO_INPUT_UNSUPPORTED`。

## 验收和最高NEXT

7项合成传输测试及9项来源/交付负例共16项本地通过；错钥、AAD/密文篡改、错误格式/
RIFF截断、公开输出路径、假PCM/时长、仅保存未回读、以解码冒听觉/播放、虚构事件名
均拒绝。离线保管重放只验证永久派生，不在候选/main访问私人音频或重取原容器。
source/私人文件回读与离线CI是不同证据，不把测试数当复原百分比。候选/main须据实际
发布后结果追加，当前不预写成功。

本有限包到此止点，不因模型不能听就连扩音频/播放驱动。最高NEXT
**POST-ORIGINAL-OBSERVATION-MATERIAL-PORTFOLIO-23**：用R102全22域基线与本阶段真正取得的
原文件/别名/地图/彩色动画/单WAV结果做一次增量材料复核，明确每域的实物、可见/可听
交付、原版执行、身份和缺件四层，再选一项新的实质取源/内容联接。不得重复880文件
原审计、只填计划或把地图/音频候选数当实体恢复；R20仅新同版原源可重开，P3E仅新
完整编码/显示/隔离环境可重开。复核止于一个可执行材料包，不连续做管理索引。

原版完整登录/QUIT/声画联动与世界仍未验收；具名NPC/宠物/本体任务身份没有因此增加。
Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、DD-028四类任务、overall percent=null不变。


## 实际主线终验

内容main `0639801ea6ca79204d642233cb5ab4cf31a2490a` / tree
`570397a8a07fbc5a160c77d55ac2272a8ed91b51` 已非强制快进发布。候选五项、同HEAD主线
六项Actions实际completed/success。主线专用40310312185日志确认16项测试及原样来源/
私人回读/解码与听觉边界重放通过；另P1、Stage A、R16/R17/R18兼容成功。14内容路径
与远端逐字节相等；五大历史文件和协议原样、两既有文档精确历史前缀保留。
[永久发布收据](../../research/recovered/STONEAGE-PRIVATE-AUDIO-R22-PUBLICATION-R1.json)
保存所有候选/main运行作业步骤、源链及内容blob；收据自身CI发布后实际观察，不预写
成功。单段私人文件不公开；模型无法接收音频、用户/游戏播放未确认、事件身份未知等
限制完整保留。最高NEXT仍增量材料复核23，不因验收通过而称助手已听到原游戏。
