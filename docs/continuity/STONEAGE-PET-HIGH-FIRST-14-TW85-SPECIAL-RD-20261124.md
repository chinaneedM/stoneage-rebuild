# PET-HIGH-FIRST-14｜TW85 特殊 RD 与原客户端主表盘点（待验收）

起点 main 789a69963b09fe33538681ebbe4f943789aa71a6，tree b8febdcfc742d903a451957d3a1a663363380107，PET13 PR #624 61/61 通过并合并。历史 CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c 原样。读取 PET12/PET13 两份真实来源回执，失败记录合并去重10块，8个物理组未闭合。重新实读其完整块、独立按位掩码解析 RLE；只记完整流和尺寸前缀散列，不把前缀当原生像素。静态检查原 sa.exe 的 RD magic 候选路径；另用已认证 MSI 文件目录查宠物主档候选，不以文件名扫描证明二进制无嵌入表。来源参照为后期社区保存 BismarckDD/stoneage 固定提交 2f736808ff4361f5429ee919b718c88fabb60346，unpack.cpp blob 11d3438699891a03c940b0a8d76d658293a4e04b，不当同部署。源作业和正式回执未验证前不合并。

NEXT：读取实际源回执；再决定可证的特殊资源解释与真实同版宠物数据。PET锁、PC-only、Stage A、B/wiki和R79状态不变。

## 2026-11-24 实物验证（待PR验收）
源作业 [45348429899](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45348429899) / job 138288607655 SUCCESS，源回执提交 f8dc71f728e957cfa458703fd17e8a8752170ac3。重新认证六分卷、提取MSI并核验原始ADRN/REAL及解包原sa.exe。10个异常块：8个由两种解析方法得到完全一致的 RLE 流，长度均为宽×高+1，额外字节全为0，末条重复指令 count=2；另2个仅16字节头，无像素正文，宽4、高分别-263/-307。前缀SHA只为候选，不是原生解码闭合。sa.exe发现1个RD magic候选RVA 586653，尚未证明完整解码路径。557份MSI清单中0个文件名匹配宠物主表候选，不排除嵌入表。现有207头像、510/518物理组完整取样；新增原生闭合0。8组对应7个具名客户端候选：魯貝萊歐、布林特（2组）、黑烏力王、弗奇肯、卡沃寇恩、裘尼、艾克夫。查询工具保留PET12原样本并另附PET13样本及完整状态，不合并原程序身份。
 
新增同期史料：[2004-08-19活动报道](https://gnn.gamer.com.tw/detail.php?sn=16483)记计划每场抽奖10只暗黑烏利王，不能证其等同黑烏力王或实际发放；[2004-12-25报道](https://www.games.idv.tw/news.php?nid=249)称红火蚁、绿蚁近日上线（2005元旦前），不证布林特精确对应及首发日期；[2005-04-24编辑的玩家技能资料](https://forum.gamer.com.tw/G2.php?bsn=1571&lorder=19&parent=3415&sn=1338)记黑烏力王／黑烏力化、卡沃寇恩及卡沃裴特／擒拿，不证明出生配招或原服公式。后两为可检索正文／片段，原网页完整快照未得。独立记录于 `research/pets/PET-HIGH-FIRST-14-TW85-PERIOD-CLAIMS-R1.json`，不增加永久PET号或官服实发确证数。
 
NEXT PET-HIGH-FIRST-15：有限复核原sa.exe候选RVA 586653的尺寸处理、尾零及无正文块分支；若无法证明则保留候选并优先同版宠物主表、同期官服发行、属性成长技能捕捉史料。PET唯一，PC-only，Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，overall UNKNOWN，历史CURRENT不动。
