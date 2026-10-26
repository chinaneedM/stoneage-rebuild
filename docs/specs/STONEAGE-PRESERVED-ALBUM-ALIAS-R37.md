# 相册图号到同一保存客户端ADRN物理记录（R37）

日期2026-10-27。性质：有源静态研究规格；不是复原游戏运行画面或鉴真官方版本。

**范围/原始来源**：R36保存包原程序两份相同相册281行表（224有效槽）；同社区混合2.5保存子树之`data/adrn_15.bin`。实际R37原成员18,765,120字节、80B×234,564记录，SHA256 `92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74`，完整SHA与原RAR CRC823378952匹配。不是同官方编译/安装认证，也不能推广台湾1.0/JSS1999。

| 原程序相册名称 | 槽 | 表内face逻辑值 | 同源ADRN字段+76逻辑值 | ADRN原物理bitmapno/行号 | 尺寸 |
|---|---:|---:|---:|---:|---|
| 乌力 | 0 | 28001 | 28001 | 7246 | 96×104 |
| 乌力乌力 | 1 | 28002 | 28002 | 7247 | 96×104 |
| 乌力斯坦 | 2 | 28003 | 28003 | 7248 | 96×104 |

**同号反例（必需）**：原物理bitmapno=28001/28002/28003各自还存在一条独立记录，逻辑+76均为0，尺寸36×79/36×77/48×77，和上述7246–7248不同SHA、偏移和记录尺寸。不得把相册face=28001直接读取物理28001；此处建立逻辑→物理记录的同源静态关系，而非RGB像素/动画/物种身份结论。原全表非零alias存在514次重复额外出现；仅上面三个逻辑键在本原件各出现一次，其他键不套用first/last-wins。

**来源失败与修正**：第一次run [40419864727](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40419864727) job 121911312484 的CI作业标success，但源状态实为NOT_ACQUIRED（单次2.28MB超出单段预算，finite sparse read required）。第二次run [40420077051](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40420077051) job121912033214采取有限1MiB分块，71次HTTP206 Range累计4653056B，unar=0，源状态为ORIGINAL_ADRN_FULL_HASH_MATCH。保留两次原始派生源报告的所有范围校验元数据；不涂改前一次错误。

**内容可用边界**：R36表内face值由同原程序保存拍照路径静态赋值；R37同源ADRN定位正确物理bitmapno以及对应offset/size；尚未读/解码原REAL像素、验证SPR、执行原程序、证明运行选择器使用该条、同部署build及原服务器具体物种/捕获成长。证明的是静态证据链，不是画面可运行。原REAL、原程序、密文、私钥都不入Git。source artifact ZIP digest仅GitHub API记录，此轮未声称再下载独立校验ZIP。本包离线正负验收从Git两个已存派生报告及R36原281行运行，不重取原客户端。

**下一止点**：若已有同源REAL可在有限预算合法取件，则仅对三幅原bitmap号7246–7248的offset/size/头/块SHA做匹配；若不可得，明确材料缺口，按22域队列切换，不为解码helper重复下整包/763MB REAL。新认证官方客户端0、Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、DD-028四任务档、总体恢复比例null不变。
