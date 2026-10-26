# R38 原混合保存客户端 REAL 实物文件头与相册三图索引边界

日期2026-10-27（Asia/Shanghai）。FACT只属于已有社区混合2.5保存包，未证明官方干净发行或原程序实际部署；本包以真实原RAR4文件头补足R37三项静态资源索引的容量归属，不提取图像。

## 新原始证据与保管

取证源码分支`agent/album-real-header-r38-20261027` commit`1c58edffe3a299466373f1c5d4e3713a4ac751ac`。原source Actions [40422947999](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40422947999) / job121921573780已实际completed/success，报告状态`SINGLE_REAL_HEADER_PRESENT_PIXELS_NOT_ACQUIRED`。整段RAR目录由rarfile4.2原生扫描完整7954头；184次严格HTTP206 Range请求，实取12,013,836B，原16MiB上限未提高，没有读下面的大图压缩数据。

同目录实际唯一`stoneage2.5/data/real_15.bin`原RAR头声明：解压后763,908,374B、压缩载荷338,458,942B、RAR4 method53（压缩，非stored）、flags33472、原CRC32 3180047245；header_offset5107864、data_offset5108046。此为文件头**声明**的未压缩大小及原CRC字段，**没有下载/哈希/校验整份原REAL像素文件**；不要把未读原文件声明为完成SHA/CRC验证。

| 相册名（R36） | R37源face逻辑 | R37物理编号 | ADRN在该REAL声称的解压字节offset | 大小 | exclusive end |
|---|---:|---:|---:|---:|---:|
| 乌力 | 28001 | 7246 | 26,119,737 | 9,521 | 26,129,258 |
| 乌力乌力 | 28002 | 7247 | 26,129,258 | 9,678 | 26,138,936 |
| 乌力斯坦 | 28003 | 7248 | 26,138,936 | 9,304 | 26,148,240 |

三位置连续且均处于原RAR头声明的解压大小763,908,374B内，为**结构一致性的同子树目录线索**；还没有读取这三处RD头、块SHA、像素或原图显示。不能使用HTTP Range的原RAR压缩文件偏移直接冒充解压REAL的地址，method53压缩载荷338MB超出原16MiB证据包限制且未发现独立可验证随机解压索引。原容器单成员不依赖split/solid不等于可以任意偏移随机解压，也不能从大小等式推宠物/图像身份、版本首发、运行时渲染。

所有184范围元数据与来源身份/文件头字段持久保存在`research/recovered/STONEAGE-ALBUM-REAL-HEADER-SOURCE-R38.json`，有限源派生摘要见`STONEAGE-ALBUM-REAL-HEADER-MATERIAL-R38.json`；未保管原件，不发布图像/执行程序。短期GitHub artifact ZIP SHA仅API报出，未独立拉取核验ZIP。来源边界与R37首次取件失败历史原样保存。

## 有界停止与22域重排

R38止于“原压缩档案有该唯一REAL头、三段ADR N偏移容纳于未压缩大小”，不提升到实际位图配对。没有经核验的独立原REAL局部解压能力或足够且可校验的私人长存目的地时，不为三图下载338MB压缩/764MB未压缩源，不构造假RD头或图像。将最高转向22域原始具名宠物/NPC/本体任务一手同版材料；有**具体可验证同源REAL提取/私人长期保管**时才重开三图实际内容。原官方客户端新增0，DD-028任务四档、Stage A7PARTIAL+2OPEN、Stage B/wiki GATED、R79暂停、总体百分比null不变。
