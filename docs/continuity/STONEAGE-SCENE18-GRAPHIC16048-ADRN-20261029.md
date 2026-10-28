# 2026-10-29 — SCENE18 原NPC图形键16048同包ADRN实物查询

本轮从fresh main `bfd6394cbc4b998a6cedfd732b8048da82360501` 起步，先核SCENE17实物、R15既有真实私人图像及其未解决原本体运行边界，再决定最小新证据范围：只在原RAR里寻找同保存客户端`adrn_15.bin`，完整鉴真18,765,120B/SHA `92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74`，对R17新增的图形键16048找原80B属性记录的物理bitmap/REAL偏移及尺寸。原`real_15.bin`760MB以上，仅检查RAR header而**不读取其图像内容**。本包不能认证原NPC实际像素，也不能把近邻NPC反推为台湾1.0官方原服。

定点HTTP206仍复用同R36/R46来源，自定≤64MiB/1024范围请求、RAR头≤10000，压缩ADRN包≤24MiB，必须原成员全SHA/CRC、unar与libarchive字节相同。不提前称源任务通过，不将原件或图片传公开Git；失败诚实留档。来源和同部署依然只是混合2.5保管，原世界尚未进入。

## 原件来源任务失败及有限修正历史（不可抹除）

- 源运行 [40790203309](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40790203309)：错误目录层级（漏`data/`）导致原RAR全7954头遍历后缺匹配；实得HTTP206 12,013,836B/184请求，真实failure；这不证明原ADRN不存在。修复由仓库原始完整文件目录 blob `78e8260e89928df76513799511d45c14a9e24dfc` 精确指向 `stoneage2.5/data/adrn_15.bin`。
- 源运行 [40790264401](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40790264401)：更正路径后命中RAR原件，但试图一次读取超过已验稀疏读取器每次2MiB限制；实得12,013,836B/184请求，真实failure；修订分段读取。
- 源运行 [40790416308](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40790416308)：修正分段后实际HTTP206 14,242,060B/218请求、已进入原索引解压；独立libarchive读隔离RAR返回明确`ArchiveError: Parsing filters is unsupported`，真实failure。与历史R7记录一致，不推广成双解包器已通过；原文件在错误前已由unar整文件SHA/CRC校验，未在这一失败报告中输出图形记录。

第四次有限试验只在原unar解压整文件尺寸+SHA、RAR CRC通过后，使用原80字节记录查看16048。保留独立libarchive不支持的失败记录，不尝试另一组通用解压器/驱动/原进程，也不将其称为已验证实际RD像素。若最后无资料增量则止点回22域，不继续空转。源工件仅派生元数据、不得包含商业图像或原数据。
