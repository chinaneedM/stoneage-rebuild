# PET-HIGH-FIRST-09｜台湾保存8.5原PC图组的可视与动作来源索引（2026-11-23）

## 研究目标与源资格

仅经典2D PC宠物模块。承接[PET08四轨原程序选择路径](STONEAGE-PET-HIGH-FIRST-08-TW85-NATIVE-SPR-NAME-BRIDGE-20261123.md)，使用同一保存安装包中已永久归档的SPR/R28帧引用、R29同包ADRN/REAL映射结果、华义补丁原记录及TW85原RD配对，建立可复核的**原帧来源和头像RD候选**；不把客户端本地编译记录冒充官方实际发放/原服Pet ID。

- [逐SPR图号、物理组、原始动作索引和头像候选机读报告](../../research/pets/PET-HIGH-FIRST-TW85-VISUAL-ACTION-REFERENCES-R1.json)
- [源派生脚本及精确Git blob输入锁定](../../tools/stoneage_pet_high_first_tw85_material.py)；`python -m tools.stoneage_pet_high_first_tw85_material --mode generate`产生JSON，`--mode verify`对派生JSON逐字节复算。
- [可复用的原生选择源报告](../../research/pets/PET-HIGH-FIRST-TW85-NATIVE-SPR-ALBUM-R1.json)以及[PET09字段/负面断言回归](../../tests/test_stoneage_pet_high_first_tw85_material.py)。

## 实际恢复范围

| 量度 | 原版本保存载体证实值 | 口径 |
|---|---:|---|
| TW85相对CN50的额外SPR图号 | 550 | 图形编号，**不是**550只宠物 |
| 原物理SPR组（含同号复本） | 554 | 原整段SHA与原索引保留 |
| 至少一轨本地具名的图号 | 514 | 余36在四轨均无有效具名来源 |
| 四轨本地具名图号 | 508 / 497 / 227 / 464 | 分别对应sa/sb/sc/sd，**不可相加** |
| 同一图号跨轨不同姓名 | 41 | 各程序姓名/别名/原行SHA独立保留 |
| 不同原逻辑头像别名 | 207 | 其中203不在CN50原305行的别名集合 |
| 通过华义补丁原行及保存TW85原RD精确配对的别名 | **182** | 各有原生物理RD号、SHA及原尺寸 |
| 原补丁中没有命中记录的别名 | **25** | **OPEN：不能推断客户端本地没有头像** |
| 原始SPR帧引用位置 | 137,211 | 137,192有源RD映射，19原空帧 |
| 未找到同包RD映射的非空帧位置 | **0** | 仅表示资源索引可配对，非实际播放 |
| 官方实服新增物种/本轮私有像素解码 | **0 / 0** | 证据缺失，不表示游戏历史不存在 |

帧引用还留有**111,960个物理图像ID的逐组非去重计数**、110,124个已配对RD内容SHA的逐组非去重计数和7,683个非零原声效字引用（均按554组累加，不能称独立位图总数）。每组保存原SPR整段SHA、原动画表头数、原始`anim_index`每桶帧数、逐帧顺序哈希及原R29映射计数。原始动画序号**没有**被擅自命名为攻击、待机、行走或八方向；本轮未运行商业客户端、未解码并目视原像素、未发布原版权字节。

### 代表性逐条查验

- 原SPR`101501`的四程序本地名均为**雷帝斯洛**，逻辑头像别名`28429`；通过原补丁精确配对保存TW85物理位图`303372`、原RD SHA `fa9ddb2acabd1a5bf03be3d6b08ee079ccf36badaaf70558d8d817aafc04523c`，尺寸96×104。该物理组有56个原动画表头、448个原帧位置，未实际执行动画。
- 原SPR`101669`在sa/sb为**利則諾頓**、sd为**地人龍**、sc没有合格姓名；跨轨冲突没有强行统一成一种宠物。
- 原SPR`101866`保存3处不同原物理组记录；未按图号去重丢掉原件。

### 25个没有补丁匹配的头像别名：实际止点

本轮试图额外读取已归档的`research/recovered/adrn129-tw85-real-pair/NATIVE-R1.tsv.gz`，发现它仅保留原ADRN头字段和记录/属性哈希、RD位置与SHA，并**未保留原80字节记录的`map_number`字段**；不能从该派生文件单独恢复“逻辑头像别名→物理RD”的新关联。扩展尝试在[失败Actions 45180990056](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45180990056)中以`KeyError: map_number`明确止步；已撤回这一不可重演的扩展，不掩盖失败，也没有发布伪造25项。最初[成功验收45180613385](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45180613385)，回退后[成功验收45181178912](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45181178912)。25项只能待再取得允许公开保存的原80B别名字段映射/原ADRN私下复读后关闭，无需无意义反复查询既有缺字段的派生表。

## 未证明的原版事实与接续

保存安装器出自第三方归档，尚未独立证实为运营商原始纯净零售安装版本。四原程序是静态有界路径，非原实机演出；头像逻辑别名不是物理位图号，撞号候选不能指定默认运行胜者；SPR动作序号不等于官方动作语义。尚无该运营部署PetMaster、正式宠物ID、Lv1属性/出生区间/成长、技能、抓捕/领取、真实发行及活动日期，故**不新增官方物种计数**。

**PET依旧为唯一活动模块**；保留Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、总体百分比UNKNOWN。原始`docs/CURRENT-STATE.md`完整Git blob`c89e0e33537990aa2132b47c40fef49a985a935c`原样保留。

**NEXT PET-HIGH-FIRST-10：** 以本图号/物理RD/帧引用索引为入口，优先在可合法取回的现有已认证PC保存载体中私有解码代表性头像和逐动作帧，形成真正可观看的原像素观察；与此同时补寻当期官方PC实服投放公告及同运营部署PetMaster。无对应源则标为MISSING_SOURCE，不能转去手游/私服/收费介质，也不切换出PET模块。
