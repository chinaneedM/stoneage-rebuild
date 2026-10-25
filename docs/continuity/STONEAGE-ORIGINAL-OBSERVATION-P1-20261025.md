# 2026-10-25 原版观察台 P1 真实字节源验证

**加法连续性覆层**。本轮启动远端main `21b14d6b0c50245f1dd607a48113563cef61a243` / tree `5b0e47521d8efd82078922ff5a859a067729d20d`，主线最近R19收据与已通过的R16/R17/R18/R19/StageA Actions重新核验；完整 `docs/CURRENT-STATE.md` 原Git blob `031c76a5a8e431f646853909bb2f2e11e6328cd2` 已真实回读，历年材料与ROADMAPP均保留，原文件未覆盖。用户现明确增加“亲眼看到、听到并可操作原版”复原目标，不意味着用户要求立即推新作。详见 `docs/STONEAGE-ORIGINAL-OBSERVATION-LAB-R1.md`。

P1内容新增来源身份钉牢的只读工具 `tools/stoneage_original_observation_lab.py`、本地零网络HTML图像/音频观察页、合成回归与CI。**不是已运行老版游戏**。离线候选source-contract run40205884525/job121206596309 10项新测试+既有4 RD测试实际success。后续真实source run **40206034214/job121207050316**、原HEAD `898dfea3cd33ca3f99afc94f4c23f29b80daf203` 实际completed/success：为首次真实索引像素生成而新一次重取既经认证TW1零售源 `CD_DIC.rar` (842125501B、原MD5/SHA1匹配)、实际临时提取 `STONEAGE.bin` (523449360B)，只读提取原 `adrn_1.bin`/ `real_1.bin`/ `sas_20.wav`，用程序验证前两全文件原SHA。原盘无永久私有保管，并非新增官方版本。

原版`bitmapno=5846`：ADRN索引5846、52×72、RD原块SHA256 `f4880a27d5aa6fb617a308703ea81bd6db3b67fa7a77436183e0b24667ce1911`、输出索引字节SHA256 `701a3bb13ec61eadc2531e770d90b1b8744abb682327396eb98e6b351ac0769e`、私有临时灰度PNG SHA256 `14378bfb36388dd4c96b173966126e9f7dcb285b5d82199fcbbd5458e42a763c`。 `bitmapno=5847`：索引5847、40×72、原RD SHA256 `9575da7cf85d7324def2e7502493d229f50bd07514f2933d3352029e1eaec70839cc1??`、解码像素SHA256 `e4efb9a660aa96ba266a6d6229e156511d6287b476e8b84fd267fedd537c0bc1`、灰度PNG SHA256 `056bf10474ca155bd7ae6c032795b21ae71107176247fc8e1b4e9e85e8e9b8ac`。注意5847 RD SHA以**机读JSON与旧R99逐哈希为准**，本段不可用复制错误短写覆盖来源。公开Git只保留JSON/指纹、不保留图像本身，也未观察真实色彩或宠物身份。
 
原音频 `StoneAge/data/se/sas_20.wav` 原文件3938B、SHA256 `6e8e7b6fcfb0409583b471866b7f3e5b8b9d698afa16d888ace5af38722e6e00`；实际PCM元数据单声道、11025Hz、16-bit、1939帧、0.17587302秒，未播放、未绑定某动作或宠物。
 
本轮原始 PNG 与 WAV 均在Actions临时目录中生成/读取并于最后清理，没有将任何版权图像、声音、游戏程序和私有包写到公开Git或长期存储。数据定义仅证明TW1同版RD的**索引结构可解码为灰度图**，而非验证完整调色板、图像色彩、原版角色选择、服务器NPC名称、游戏世界或实际玩家操作。下一观察门槛P2是**真实原调色板与原SPR动画可视化**；内容主任务 `EARLY-OFFICIAL-WORLD-ENTITY-SOURCE-20` 保持单独OPEN。本项目 Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、overall percent=null不变。
