# R41 原NPC三文件与现代同长异SHA实际差异

日期2026-10-27（Asia/Shanghai）。起点为本轮重新读取的main `38b7670613ec94f1d9133c229bed0bf84a4eef9f` / tree `cfae99c217d4bd4066a19d2589dd8589fc12b390`；627分支、无开放PR/活动作业，旧10-07 BecomePig queued保留。七启动文件、完整CURRENT2680510B/blob031c76a5a8e431f646853909bb2f2e11e6328cd2、路线和R40后验按原生Git字节重核。CURRENT及四历史主簿不改。

最高R41实际source40451830173/job122016102981/HEADea7baa5f58b496611664990854b2e4163f074c65 completed/success。完整7954头、184范围、12013836B，实际取得sb_kbu.arg258B、sb_geno.create573B、sb_geno.template321B，三原完整SHA与旧原件清单同一并逐CRC。原包未重拉、原代码未执行、商用脚本明文未公开。现代固定YAML3328B/blob6e066821bedd0bbef7e59cc3f020cad7783e51c5也重新核验。

异SHA查明：258B参数有114字节位置不同，换编码本身不足；三个对白字段14字符位置/9组繁简替换加GB18030编码可精确重现现代258B。所有数值、键和空字段相同，完整原对白只保留摘要，不宣称实际脚本逻辑等价。原报告“纯转码候选空”保留，候选验证改为符合实测的两层差异，不修改source来迎合假设。

原创建文件实有3配置、2模板：風的守護獸前两条floorid11208/位置26,40与42,38，引用sb_kbu；第三条floorid11214/41,36引用sb_kgi，图形100343而前两100394。现代11208文件只有前两NPC及独立3warp，第三条不在其地图范围，不能报删除或把warp归成NPC。同包R40原索引仅确认两图形整数候选313/360，不认证新NPC实际图像。

规格`docs/specs/STONEAGE-PRESERVED-NPC-DELTA-MATERIAL-R41.md`及SOURCE/LOCAL-COMPARISON/MATERIAL/CUSTODY-R41记录来源与字段。ZIP/raw独立下载哈希、CMS解密后三原全SHA、本地完整字符转换、全部45条配置赋值独立核验后持久保存派生；原件只临时私人保管，不宣称长存。

NEXT `PRESERVED_GENKOU_THIRD_GUARD_ARGUMENT_42`：实际取已观察到的第三条所引sb_kgi.arg281B/SHA61c2aefca26c9d84db061f34c66c74b980006cac915fe732394f753daddbd586，与已得sb_kbu精确比较。有限16MiB/原SHA，取得材料或精确缺口即停止本NPC支线，回其它22域。DD-028 ORIGIN_UNRESOLVED、本体认证新增0、Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、P3E阻塞、整体percent=null不变。候选/main Actions后验另记，未提前称成功。
