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
新增 tools/stoneage_private_scene_graphic_join_r1.py 和 tests/test_stoneage_private_scene_graphic_join_r1.py，更新现代观察器原有CI工作流。CLI先复用已鉴真的后期区域载荷物化功能，再对同保存来源的 ADRN/REAL **整文件尺寸+SHA256**进行严格检查；最多64×64地图格、最多16个候选图号，超出拒绝。来源为后代 LATER_RECOVERED，不得写成TW1_DIRECT。DAT必须保留事件层，LS2MAP事件层不能用零补造。

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


## 2026-10-27｜后代源码独立审查：绘制候选与碰撞候选不能合并

独立复核另一个早已在项目 SOURCE-REGISTRY-RESOURCE-CONTAINERS-R1.md 登记为 C/LINEAGE 的后代公开源码存档：BismarckDD/stoneage Git commit 999ffdf1d220ec6666eb65339180689c9caf1876（并不是台湾1.0实际程序的同SHA源代码，也未证明为本次mixed25二进制对应build）。

- client/stoneage/system/map.cpp 行约916–984的 drawMap 分支：tile和parts只有在编号大于 CG_INVISIBLE 时才进入图像显示路径；较小的20–39以及40–59分别落在环境音与BGM触发逻辑，而非普通地形PNG。
- client/stoneage/system/map.cpp 行约894–895及917起：使用 SURFACE_WIDTH/SURFACE_HEIGHT 的斜向坐标与对角顺序推进，parts通过 realGetNo 取物理图号，再查图尺寸、偏移并走 setPartsPrio。不足以证明现代视口里的具体投影、遮挡或透明像素复现。
- client/stoneage/system/loadrealbin.cpp 行约188–209及336–354：在该源码配置中ADRN属性 bmpnumber（与恢复的map_number字段同型）映射到物理 bitmapno；映射表赋值可能遇到同键更新，也存在特定后期宏/编号例外。因此仅是**后代源代码中的候选选图语义**，不能将本包514次重复图号全部按末条规则自动认证。

据此已把新增探针收紧：**只对大于99的tile/parts编号实际导出索引图像**；碰撞属性另含60–79，但专列 special_collision_ids_not_drawn，不再将其误作已经被原地图绘制的贴图。报告的draw_rule_grade为 DESCENDANT_SOURCE_LINEAGE_NOT_RECOVERED25_SAME_BUILD，物理draw选择、原版色板/透明/景深依然OPEN。新增反例测试断言60/79不能作为直接绘制候选，同时保留此前map number覆盖与重复记录事实。

来源指针：
- https://github.com/BismarckDD/stoneage/blob/999ffdf1d220ec6666eb65339180689c9caf1876/client/stoneage/system/map.cpp
- https://github.com/BismarckDD/stoneage/blob/999ffdf1d220ec6666eb65339180689c9caf1876/client/stoneage/system/loadrealbin.cpp
- https://github.com/BismarckDD/stoneage/blob/999ffdf1d220ec6666eb65339180689c9caf1876/client/stoneage/systeminc/map.h

本次新版等价合成单测再次13项通过；真实保存包来源像素、实际浏览器观察和GitHub Actions完成状态仍按实际单独标注，不预报成功。
