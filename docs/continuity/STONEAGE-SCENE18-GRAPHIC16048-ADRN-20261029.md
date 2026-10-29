# 2026-10-29 — SCENE18 原NPC图形键16048同包ADRN实物查询

本轮从fresh main `bfd6394cbc4b998a6cedfd732b8048da82360501` 起步，先核SCENE17实物、R15既有真实私人图像及其未解决原本体运行边界，再决定最小新证据范围：只在原RAR里寻找同保存客户端`adrn_15.bin`，完整鉴真18,765,120B/SHA `92d0137590d35a7a1f4fb11af3ad13bbc585813a4b0e1e3f933c397007fbff74`，对R17新增的图形键16048找原80B属性记录的物理bitmap/REAL偏移及尺寸。原`real_15.bin`760MB以上，仅检查RAR header而**不读取其图像内容**。本包不能认证原NPC实际像素，也不能把近邻NPC反推为台湾1.0官方原服。

定点HTTP206仍复用同R36/R46来源，自定≤64MiB/1024范围请求、RAR头≤10000，压缩ADRN包≤24MiB，必须原成员全SHA/CRC、unar与libarchive字节相同。不提前称源任务通过，不将原件或图片传公开Git；失败诚实留档。来源和同部署依然只是混合2.5保管，原世界尚未进入。

## 原件来源任务失败及有限修正历史（不可抹除）

- 源运行 [40790203309](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40790203309)：错误目录层级（漏`data/`）导致原RAR全7954头遍历后缺匹配；实得HTTP206 12,013,836B/184请求，真实failure；这不证明原ADRN不存在。修复由仓库原始完整文件目录 blob `78e8260e89928df76513799511d45c14a9e24dfc` 精确指向 `stoneage2.5/data/adrn_15.bin`。
- 源运行 [40790264401](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40790264401)：更正路径后命中RAR原件，但试图一次读取超过已验稀疏读取器每次2MiB限制；实得12,013,836B/184请求，真实failure；修订分段读取。
- 源运行 [40790416308](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40790416308)：修正分段后实际HTTP206 14,242,060B/218请求、已进入原索引解压；独立libarchive读隔离RAR返回明确`ArchiveError: Parsing filters is unsupported`，真实failure。与历史R7记录一致，不推广成双解包器已通过；原文件在错误前已由unar整文件SHA/CRC校验，未在这一失败报告中输出图形记录。

第四次有限试验只在原unar解压整文件尺寸+SHA、RAR CRC通过后，使用原80字节记录查看16048。保留独立libarchive不支持的失败记录，不尝试另一组通用解压器/驱动/原进程，也不将其称为已验证实际RD像素。若最后无资料增量则止点回22域，不继续空转。源工件仅派生元数据、不得包含商业图像或原数据。


## SCENE18 实际来源验收与跨版本取图候选（2026-10-29）

本轮从远端主线 bfd6394cbc4b998a6cedfd732b8048da82360501/tree92dd8a649e8045138b95fd77ebd4c02fed4697f2启动；666远端分支、0开放PR、七启动文件及完整CURRENT 2685765B已核。续接既有未合并SCENE18分支c571fc2，未重跑或虚构源执行。成功source run40790680489/HEAD81578679/job123174841510已实际completed/success；工件12860514878 ZIP12508B独立下载SHA256 0cea2baa749a483798099ab5899f2e6c14871f150417bec8ed01e340448023b4与API相同，原JSON42747B/SHA f53d3630ed49dd06c3822972a2620001d1781bf232b1c9e8db21c3ab1b7c4213永久归档。

**FACT（原创建配置→同载体索引）**：218次HTTP206/14242060B、7954原头；unar整ADRN18765120B SHA/CRC通过后，原图形键16048恰一80B记录：index/bitmap5894、REAL偏移25018537/长度1668、尺寸36×79、原偏移-18/-70，记录SHA2273a098fa5e5f701c44ead12757cbb159570c43ceb5cf0120d32b1a71e5f524。libarchive3.7.2明确Parsing filters is unsupported；不能称双解包器成功，前三次failure保持不变。上文原双实现要求由这个有界单解包器+既定整SHA/CRC结果明确降级，不追认成双实现。

**新增跨版取图候选**：独立从已有官方patch数值属性重建整80B记录，其SHA与本次混合2.5索引完全一致；TW8.5 native完整记录也同SHA，TW1/CN5已有完整表的头部/属性SHA一致。后三个历史样本原RD摘要均ce21e49856dde81b79afa5854f400df31393b1d87a08e6357b0eb8fd2e5ad252。这只给后续读取旧已保管原图的准确候选；本次mixed25 REAL读出0B，其RD摘要仍null，**相同索引不能证明未读像素相同**，也不证明初代官方NPC身份/同服/对白/原图渲染。

源报告、完整range链、跨版候选、ZIP/JSON/Git blob保管收据以及17条新正反测试永久入Git；与既有门槛合计51测试本地通过。候选/主线CI按后验另记，不能以公开元数据CI冒作原图解码或源重跑。原数据/图像/程序未公开。

**最高NEXT：SCENE19-EXISTING-PRIVATE-NPC-BITMAP-OR-CONTENT-ROTATION**。先在已有私人TW1/mixed25保管包或图像子集中找准确原RD(5894/1668B)；完整原成员SHA或既已认证的块SHA成立才解码，并独立核索引/像素再接现代观察器。若只能取得索引或需要重拉338MB压缩REAL，有限缺件止点回22域材料队列，不再扩大RAR/解包/驱动辅助链。NPC63,103位于R15旧7×7窗口之外（y最大102），不得为显示NPC把旧画布伪称已覆盖；新观察须显式扩窗/重取地图范围或单独候选图检视。原版世界仍未进入，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、总体percent=null保持。


## SCENE18 主线终验及相邻SCENE19真实原图复用（2026-10-29）

PR34已合并为40542736b9db3b20aa9525e093bf7aa183063ce9，完整tree1904874d025ee1d1eae9febf71699660a4e4f8ce与本地已验tree相同；候选66adf209的21项、主线21项Actions全部实际completed/success。主线专用40815745599/job123256252294原日志确认51测试，公开CI仅读元数据，未读原图。全21运行ID/源工件/原报告blob在STONEAGE-SCENE18-PUBLICATION-R1.json永久保存。原生git push无凭证失败，曾有head不存在的PR422失败；随后使用已连接GitHub Git数据接口上传11完整blob并逐SHA匹配，远端整tree一致后正常PR合并，未截断大CURRENT。

相邻SCENE19不是重拉原盘：实取已保存P3H原件包372626292B并核SHA3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24，完整TW1 ADRN10079680B/SHA47254c0ff904d363fb5c3c5297edf553c8eaf24cd933f346d8ce7aabed4155c8及REAL315842228B/SHA408e6ee05c83354349691937da2ad8f7488ac10f65f07e6681b7d92cb1c9ed13重新认证。原5894整80B记录SHA与SCENE18完全相同，实际1668B RD/SHAce21e49856dde81b79afa5854f400df31393b1d87a08e6357b0eb8fd2e5ad252解得36×79/2844索引；两个不同实现全部索引同一，索引SHA d5d2cc7806f814d64bf5c27f0b557c7846c71c08e2dd87af1f2078af3548c119，Pillow PNG回读RGBA及整数4x全部精确相同，并实际目视一幅有帽饰的人形候选。原灰度只是索引数值，Palet0配色/倒行/透明仍候选，不能称真实游戏当时颜色或原屏幕截图。

小私人候选包16155B已保存成功（保存后未再次回读，不伪称耐久二次SHA）。公开Git只有2249B派生元数据，原RD/SAP/PNG未公开；source_ci_run_id=null明确本地复用与双解码器，不虚构GitHub source任务。mixed25 REAL仍读0B，未证明它与TW1该块相同；台湾1.0中该图存在也不证明TW1官方服有1000(63,103)的NPC、同名对白/交互或纯净2.5发行身份。浏览器场景/原客户端世界都没有新认证。

最高NEXT改为 **SCENE20-MATERIAL-ROTATION-REVIEW**：先按22域已有材料作一次有限查重/重新排序，再选择有原实物的交互/音频/场景集成结果；不要继续RAR过滤器、原EXE或相同5894摘要空转。若选择现有R15观察器，只能将已取得TW1候选图作为明确跨样本参考，不能冒充同源NPC实际像素；NPC坐标y103在旧7×7窗外，扩窗须原DAT/每个原图来源单独资格。保持原世界未进入、Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停和总体百分比null。该后验提交自身CI另据实际记录，不能追认成已运行。
