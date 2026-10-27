# 2026-10-27｜SCENE-RESOURCE-JOIN-01：真实地图编号至源图像字节的有限联接

性质：**有界研究工具候选；不是原版进入世界或完整场景出帧**。

## 远端启动依据
最新主线 HEAD 565cec85e9dd8139e97b2df4b1d754d103930491 / tree 6da3843732494d8a4696e372bf6ab603d8611404。CURRENT-STATE.md原Git blob 031c76a5a8e431f646853909bb2f2e11e6328cd2，Git原文件2680510字节；完整读取，不裁切、不覆盖。原现代观察工作分支 a8fbef9c694bc60d73360eafd10fac6b99be33cc 起步，Actions未有完成/成功验收时，不提前写入main。DD-030仍规定未来作品简体中文UTF-8，历史原文字节保持各版本独立。

## 第一性来源事实
- 现有 tools/stoneage_recovered25_region_payload.py 可按已固定来源SHA重现后期761张DAT（三层tile/object/event）及65张LS2MAP（两层tile/object，事件为真正缺失None），不等于复活台湾1.0服务器。
- research/recovered/STONEAGE-25-CLIENT-ADRN-COLLISION-COVERAGE-R1.txt 仅证实191张缺服务器碰撞源的稳定DAT地图在 *碰撞ADRN需求* 下所需ID没有漏映射（unresolved=0），不证明所有826张场景已经具备原图、色板或渲染顺序。
- recovered25原图索引 adrn_15.bin 为18765120字节，SHA256 92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74，234564条80字节；10159个不同map_number、514次重复编号。对应 real_15.bin 763908374字节，SHA256 c7640643804d550bc07e33661103fb7b5f557ee01e68a5a5d92382c5305c2b0d；来源以 research/recovered/STONEAGE-25-RESOURCE-PROBE-R1.txt 为据。总体保存包SHA256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5；此包不是经认证的干净官方发行版本。
- tools/stoneage_dat_probe.py::load_adrn 证明 map_number 在80字节记录第76字节（little-endian uint32）；记录起始 bitmapno 与这个值不等价。同名编号必须保留所有出现，不能把碰撞代码中可能存在的末条规则擅自升级为图像显示规则。

## 本次代码与独立回归
新增 tools/stoneage_private_scene_graphic_join_r1.py 和 tests/test_stoneage_private_scene_graphic_join_r1.py，更新现代观察器原有CI工作流。CLI先复用已鉴真的后期区域载荷物化功能，再对同保存来源的 AD RN/REAL **整文件尺寸+SHA256**进行严格检查；最多64×64地图格、最多16个候选图号，超出拒绝。来源为后代 LATER_RECOVERED，不得写成TW1_DIRECT。DAT必须保留事件层，LS2MAP事件层不能用零补造。

每个来源ID将按真实ADRN第76字节map_number查表；仅单一记录、图像尺寸正常、REAL区间有效、RD像素可解码时，向仓库外空的私人目录生成编号PNG。所出图像是**索引像素灰度预览**，没有原场景调色板、透明规则、等距地图坐标投影或真实绘制顺序。重复编号、无映射、特殊尺寸分别显式登记不擅选取、不虚构图像；目录已有文件拒绝写入。公开Git只保留源码、合成测试及有界文档，不上传商业PNG、REAL、声音或游戏原件。

本地等价工程实现已有13项合成Python正负测试通过：包含来源SHA错配、重复编号保真、缺映射、特殊查询ID、ADRN偏移与REAL越界、DAT/LS2MAP事件差异、历史归属不得提升和私人路径拒绝。远端候选CI须实际完成才可声明它通过；不能把本地小测试写成真正从保存包获取源图。

## 本机私人使用契约
完整私人数据已存在且满足固定来源SHA时，从仓库根目录执行（路径只是示例；特定floor/视口不保证满足图号限制）：

    mkdir -p /private/observations/scene-id-art
    python -m tools.stoneage_private_scene_graphic_join_r1 \
      --client-dat-dir /private/recovered25/client-map \
      --server-map-root /private/recovered25/server-maps \
      --adrn /private/recovered25/data/adrn_15.bin \
      --real /private/recovered25/data/real_15.bin \
      --floor 100 --x1 0 --y1 0 --x2 1 --y2 1 \
      --output-dir /private/observations/scene-id-art

输出 source-manifest.json 与最多16张私人map-ID灰度PNG，每张有真实ADRN记录和RD字节SHA见证。图像只有用户实际加载查看后才可称为观察过；本次尚未实际持有/查看相应版权原图。现代研究观察台和原EXE真正可玩世界不可混认。

## 当前止点与下一最高
- 目前是“地图来源实际值 -> 图像容器来源记录 -> 可解码索引像素”的**研究工具接缝**，并非“实际游戏tile渲染”。碰撞属性的map_number分类不能当成历史draw选择规则。
- NEXT SCENE-RESOURCE-OBSERVATION-02：从已保存的**同构建**绘制调用/原程序源证据中，验证一个tile/parts图号如何选择绘制的bitmap、图层、屏幕投影/透明/颜色；若缺同建证据就保留UNKNOWN，不从后代混包回填TW1。然后才在私人原盘可访问环境中实际生成一小片有真实图像的可视观察样本。
- 本聊天公共容器没有已持续保管的0.76GB REAL原件，也没有运行中的原客户端或真实原服务；不得宣称已进入游戏。早先P3只目视原登录面板。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、DD-028任务本体/运营活动四档与整体恢复百分比null都未改变。
