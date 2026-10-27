# R46 社区原保存包家族治疗 NPC 创建配置 — 原字节限定取证

日期：2026-10-27。包名：`PRESERVED_HEALING_NPC_NAMED_MATERIAL_46`。限定一份已索引的原始创建配置文件，不扩大治疗机制或早期四村线路。依据源报 Git blob `a0e5391ab70d5636fe55e196ec5b6081d4825ddc`；并非台湾1.0、日本JSS1999或官方同一部署构建的证明。

## 实际取得的原源及保全

- 原保存父包：社区混合2.5保留材料，声称父包361255180B；已有 R18 父包SHA 与静态成员目录为索引依据，未将社区“2.5”标题当官方build。
- 精确成员 `gmsv/data/npc/family/fmhealer.create`，649B，原完整 SHA256 `1d7d71960958cc60c5e6ba686fede736b5d66ec15f5d58300041a8a2de893847`，RAR CRC `3313982981`。两种解码器（unar/libarchive）对同一次HTTP源的完整原字节一致；两种编码(CP950/Big5)严格解析相同。
- 真正源 GitHub Actions [run40502401619](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40502401619) / job122183066222 / HEAD `0cea990336ff52699b4faa3212bb59fb3dbd8a3f` completed/success；遍历7954个RAR头，184次严格HTTP206范围、合计12013836B。未拉361MB整包、未运行商用服务端。
- 源报告52867字节/SHA256 `c14788fe3bbe854b4de0e84aa1abbb6f81a6189ef6aca7c77701cac8cc2a036a`/Git blob `a0e5391ab70d5636fe55e196ec5b6081d4825ddc` 原样永久入库；短期工件ZIP artifact12732389728 的 `1962baed3c42e7dbf23afe15b0caa11b42caeb6a1e970f2d1847024ee3e31416` 是GitHub API所报SHA，**未独立下载校验ZIP**，不能声称二次取源。原脚本、对话文本、其它未选块正文不入公开Git。

## 原配置实际见证（仅前三条）

原文件共**四个** `NPCCREATE`块；本包按既定有限规模仅投影前三个，不宣称四个都已经逐字段考据。

| 源块序号 | 原物理开行 | name原名 | floorid | borncorner 四整数 | graphicname | enemy声明引用 |
|---:|---:|---|---:|---|---:|---|
| 0 | 3 | 家族小護士 | 1041 | 4,8,4,8 | 16023 | npcgen_fmhealer\|1 |
| 1 | 16 | 家族小護士 | 2031 | 13,8,13,8 | 16023 | npcgen_fmhealer\|1 |
| 2 | 30 | 家族小護士 | 3031 | 2,9,2,9 | 16023 | npcgen_fmhealer\|1 |

共同原整数：`dir=4`、`createnum=1`、`time=0`、`ignoreinvincible=1`。只是存档中的声明字段，不能据此认定真实生成次数、刷新单位、地图范围、玩家可达性或实际治疗行为。尤其原列名是`borncorner`，不是先前守护兽的`borncenter`；不自动换名或补语义。三个同名字串仍是三条独立位置与原创建块，不按名称去重。

`enemy=npcgen_fmhealer|1`仅为原配置的静态模板/服务标记；尚缺原模板/函数注册的同构建完整链，不能把它等同`NPC_HealerAllHeal`或`NPC_WindowHealer`的实际执行。既有后代治疗模型证明一定作用域内的HP/MP/宠物恢复行为，但**不证明本原文件某个家族护士的服务价格、治疗范围或可用时间**。既有四出生点/后期地图故事，不允许倒推此社区源作为台湾1.0初始NPC。

## 分类与后续边界

- **FACT（来源限定）**：社区保存文件的原始SHA、四块配置总数与上表三个原条目、同一字节的独立解码和日期记录。
- **HYPOTHESIS / OPEN**：原服务 token 对应程序函数、同部署证据、实际NPC生成/治疗、地区时期、原图像内容、第四条详情；全部保持OPEN。
- **任务分类**：`ORIGIN_UNRESOLVED`，新增已认证本体任务0；不混入运营活动任务、也不把“家族小護士”叫已核原生任务。
- **NEXT**：本包到此止点，轮回22域材料队列，只选择能带来新可归属具名宠物/NPC/原游戏本体任务或具体物品内容的原源。优先早期可追溯发行商/原版主表；若无，登记精确缺口再轮转。不回头扩治疗 helper、洞窟脚本或重下原大包。
- Stage A 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、大包私人持久保管外部依赖未解决、整体复原百分比未知，原先证据和失败记录均保留。
