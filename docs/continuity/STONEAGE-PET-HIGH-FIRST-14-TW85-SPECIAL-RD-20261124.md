# PET-HIGH-FIRST-14｜TW85 特殊 RD 与原客户端主表盘点（待验收）

起点 main 789a69963b09fe33538681ebbe4f943789aa71a6，tree b8febdcfc742d903a451957d3a1a663363380107，PET13 PR #624 61/61 通过并合并。历史 CURRENT blob c89e0e33537990aa2132b47c40fef49a985a935c 原样。读取 PET12/PET13 两份真实来源回执，失败记录合并去重10块，8个物理组未闭合。重新实读其完整块、独立按位掩码解析 RLE；只记完整流和尺寸前缀散列，不把前缀当原生像素。静态检查原 sa.exe 的 RD magic 候选路径；另用已认证 MSI 文件目录查宠物主档候选，不以文件名扫描证明二进制无嵌入表。来源参照为后期社区保存 BismarckDD/stoneage 固定提交 2f736808ff4361f5429ee919b718c88fabb60346，unpack.cpp blob 11d3438699891a03c940b0a8d76d658293a4e04b，不当同部署。源作业和正式回执未验证前不合并。

NEXT：读取实际源回执；再决定可证的特殊资源解释与真实同版宠物数据。PET锁、PC-only、Stage A、B/wiki和R79状态不变。
