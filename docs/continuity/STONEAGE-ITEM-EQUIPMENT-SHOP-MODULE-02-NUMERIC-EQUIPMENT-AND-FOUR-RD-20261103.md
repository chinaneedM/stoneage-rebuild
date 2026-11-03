# ITEM02｜原物品数值分型及台湾1.0四幅RD异常溯源（2026-11-03）

**阶段：原版《石器时代》历史复原，而非新石器引擎、平衡或体验开发。** 从远端main HEAD `c2c6aa8fccd10ec3feaa0817a8740126c8fa345c` 和tree `a5de971767f56a1136f5851f1ea70f03f31d755d` 启动，最近11项Actions成功、无开放PR。连续性协议、README及源状态已读；巨大历史 `docs/CURRENT-STATE.md` 的真实blob `c89e0e33537990aa2132b47c40fef49a985a935c` 保持原字节，不覆盖。

## 本批真实原件
实际从用户私人Library下载原社区混合2.5 RAR 361255180B/SHA `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`、TW1原零售P3H 372626292B/SHA `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` 和ITEM01图文私有收据。两份原主表 `itemset.txt` 13254与 `itemset0710.txt` 13915行实际真解压、全SHA重验、每行94字段CP950无解码问题；两表原SHA、TW1原ADRN/REAL整文件SHA及所有无版权衍生值已归档在[ITEM02数字来源目录](../../research/recovered/STONEAGE-ITEM02-ORIGINAL-NUMERIC-EQUIPMENT-AND-TW1-RD-BOUNDARY-R1.json)。

**本轮新发现：** 后一源表包含32类原始type整数（不证明官方装备槽分类）；有10036/13915行在零基37～42原攻/防/敏六静态数值中至少一列非零。13254共同ID的这六列原数值**没有变化**，其他零基57列有206项变化，不能把ITEM01的8951行内容差异误说成8951项装备攻防敏重平衡。32类逐类型件数、新旧表ID资格、TW1图候选资格已关联到全13915行源记录。两源文件属社区混合载体，不根据0710文件名断代或提升为初版官方装备表。

**四原RD异常的具体止点：** TW1的图号24077、24137、24138、24140已按原ADRN指向实际原REAL完整字节，原RD长度449/481/472/511B。全部在严格RLE最后一条`0xC2`（零填充2像素）产生**正好多1像素**，此前832成功/4失败的资格不变；不能由此认定原字节损坏，也不能悄悄截去一像素冒充真实运行画面。四原ADRN SHA、RD SHA与首个越界偏移432/464/455/494入公开数字收据，原美术仍私人保存。

**831缺原TW1索引的物品图号：** 本轮没有擅自补图。实际尝试从混合2.5 RAR提取后期`data/adrn_15.bin`，libarchive报告`Parsing filters is unsupported`、有效字节0；解包工具失败不是原包坏。没有同载体原ADRN+REAL时，不提升后期图号为已真解码。原商业客户端、服务器、商店没有执行。GitHub CI只从已有ITEM01七份逐ID派生目录重放本轮的32类/13915行和负例，不重新读取私人商用原件。

Stage A7PARTIAL+2OPEN、B/wiki GATED、R79暂停、overall_percent=null。**最高NEXT ITEM-EQUIPMENT-SHOP-MODULE-03**：有真实后期原索引及原REAL才批量补831缺口；其余时间集中装备其他原字段、配方及商店实证或记录硬缺口后有界转任务模块。禁止新游戏体验优化和无效解码脚手架。
