# PET-HIGH-FIRST-09｜台湾保存8.5原PC图组的可视与动作来源索引

本工作包锁定经典2D PC宠物模块，在PET08原四程序选择路径基础上连接**同保存载体**原SPR帧引用、R29原ADRN/REAL映射结果，以及经华义补丁原记录与保存TW85原RD配对验证的头像逻辑别名。

- [原程序图组到各轨姓名](../../research/pets/PET-HIGH-FIRST-TW85-NATIVE-SPR-ALBUM-R1.json)：550个额外图号／554个原SPR物理组。514个图号至少在一轨具名，另36个无有效姓名；跨轨41处姓名冲突必须保留。
- [可重演建档程序](../../tools/stoneage_pet_high_first_tw85_material.py)严格锁定原源文件Git blob。运行\`python -m tools.stoneage_pet_high_first_tw85_material --mode generate\`后生成[逐SPR物理来源／帧序哈希／头像RD候选](../../research/pets/PET-HIGH-FIRST-TW85-VISUAL-ACTION-REFERENCES-R1.json)；\`--mode verify\`逐字节复算，不伪造原图像。四轨名称保留繁体原字形。
- 每个相簿头像别名独立列出补丁原行、原物理位图号、TW85保存本机原ADRN索引、原RD SHA和尺寸。**别名不等于物理位图号**；重复记录没有默认胜者。跨版本同名/同号不自动代表正式发行宠物。
- 每个原SPR物理组保留全段SHA、原动画表头数、原始anim_index桶计数、按原顺序计算的帧引用SHA、总帧数/空帧数、同保存载体RD映射完整性。**anim_index不能直接命名为攻击/待机/行走/八方向**，更不能冒充实机播放或已渲染的原像素。

**历史证据边界：**该安装器为第三方保存且未独立认证为运营商原始纯净安装发行包；四程序路径是静态有界来源而非本轮原游戏执行。图片源RD哈希／动画帧引用可追溯，不等于已私人解码显示像素或原实服动作。未获得原部署服务器PetMaster、官方宠物ID、初始区间、成长、技能、捕获/投放日期。PET仍唯一活动模块，Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停，整体完成率UNKNOWN。

**NEXT：**以本索引中已确认物理头像和帧引用为实际目标，私人源字节条件允许时解码具体原RD帧并建立可视动作预览；并行有限查证PC原运营商当期公开发行/活动和同部署服务端主表。资料缺失即记录止点，不因图组或编译姓名推断新增官方物种。
