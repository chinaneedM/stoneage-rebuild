# INTEGRATION63｜吉鲁巴那姆水壶11种原物品状态与16种源脚本边：正式验收（2026-11-11）

## 起始远端与内容来源

按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 重新读取真实 `main` HEAD `3b5e9be141225feea79e0cd94fb4d1ef2290f2c7` / tree `59186f788a3ac2a8630cf9608c5b73fe73044487`、最近提交、Actions、未结PR、README、协议、原 `docs/CURRENT-STATE.md`完整Git blob、设计决策、历史时间/来源记录、路线/模块/离线优先级，承接INTEGRATION62的不同可见内容NEXT。查重已报道的宠物技能店、五诊疗室、主厨菜单和QUEST30两奖励后，选择QUEST18原吉鲁水壶任务中的原ID-原脚本转换缺口，完成不重复料理/宠物图的多场景任务物品状态源桥。

- [日期有界原件观察详情](STONEAGE-INTEGRATION63-BANUM-WATER-VESSEL-SOURCE-GRAPH-20261111.md)
- [完整公开派生索引（没有商业原文/原图）](../../research/recovered/STONEAGE-INTEGRATION63-BANUM-11-VESSEL-STATES-16-SOURCE-EDGES-R1.json)，永久 Git blob `863c76e732e73ce1b9bbdb8aeea97246d3fe93eb`。
- 公共旧QUEST18 `research/recovered/STONEAGE-QUEST18-GIIRU-SINK-SOURCE-R1.json` 原blob `3924e900e265a957429aff2fbc7d51ac3dd5d937`；公共旧ITEM01 shard02 原blob `b91bc8335db508998f4595144ce371979ea8c849`，已跨源核原行/原CREATE。

## 真实原始文件实读结果与独立私人保管

本轮完整重读两私人 ZIP：原NPC 995176B／SHA256 `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`，**2205/2205 成员CRC全部通过**；原ITEM01 5868386B／SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`，**838/838 CRC**。在NPC源中实际扫描17份 `giiru/event/sink/sink*` 原脚本与2501B原CREATE并逐整SHA；11个原CREATE引用脚本与旧QUEST18文件路径、整SHA、楼层/坐标候选一致；其它6份脚本仅为已保存文件，不假定现役部署。私有ITEM两表的11个94字段原行逐CP950重算整SHA同公开shard02。

结果在源中固定**49次完整TYPE:ACCEPT单项DelItem/GetItem命令关系，合并成16个不同有向对**；其中35次来自已有原CREATE文件引用，14次仅来自其它保存脚本。**8**次批量DelItem及GetItem2708、**7**次只有DelItem无本段GetItem，另`sink02`有一条TYPE:MESSAGE中的`2717→19292`，均分别留证而没有误计入16种单项替换。源`sink05a`的EventNo未在物理行首，按严格行首解析未将其内部内容自造为额外事件，不能推断历史无此行为。

11个原水壶道具ID 2708—2718皆关联同一原图别名12924、价格字面500、类型字面16；`2710/2714`均显示4/7、`2711/2715`均显示3/7，逐原字段核各对仅第16列原item ID不同，其余93列完全一致。此处**11道具状态≠11张不同图**。私人实际核早期台湾1.0唯一图像物理RD索引5178、52×68 PNG全字节SHA256 `75bd38c165a57b1aad955c01a36a6fcade56d1223e858e23c4a8079945c01af2`、完整RGBA_SHA与已保存原RD收据一致，原RD新解码0。

新私人可离线查阅包 `StoneAge-INTEGRATION63-Banum-water-vessel-original-source-private.zip` **25951B／SHA256 `b935332ccae71ec59a863ceb0588f597696e764815cd2e6b8a83646e1c8e3a0c`／43个成员**（17原脚本+原CREATE+两表22原物品行+1真实原PNG+现代离线观察页+来源收据）已保存个人 Library `/石器时代/`；通过新Library文件ID在独立路径重新完整取回并核**逐字节一致、全包SHA一致、43/43成员CRC全部通过**。原文及像素仅私人，公开Git只发布派生数字和出处散列。

## 首次失败、修正与所有真实远端 CI 后验

首个候选 `15ee1d1e6d63312430f91fd038a8bd9418d7618e`／tree `e98874a03c32f3d780c1bd998553f3bfd0d0b62b` 在 [Actions run42981804900](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42981804900) / job **130393705650** 专项测试7例中**6通过1错误**，仅因为测试引用`original_rd_sha256`而报告原键实际为`original_RD_sha256`。数据源和真实原RD SHA无矛盾。**不覆盖、抹除首次失败历史**；后续提交仅修复测试字段名大小写，不修改该公开报告和私人原件。

| 验收阶段 | 远端固定事实 |
|---|---|
| 修正后候选分支 | `agent/stoneage-integration63-banum-water-20261111` |
| 候选最终HEAD | **`b6a93257ef65d5c9107b282505cd843e36103c9a`** |
| 最终候选 tree | `81cc9332899087177eb549ff8f4009c55e0e8a4d` |
| 最终候选Actions | **20/20 completed/success**（pull_request 19、push 1，特定HEAD） |
| 专项push | [run42981955920](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42981955920) 成功 |
| 专项PR | [run42981961680](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42981961680) / job **130394199138** 成功，**7项专项测试通过** |
| 合并PR | [#331](https://github.com/chinaneedM/stoneage-rebuild/pull/331)，合并前主线与base SHA一致、PR mergeable=true、5个白名单文件、20/20全部成功，squash |
| 合并后内容 main HEAD | **`7b68bd63db3965c720723da37b5b550375525350`** |
| 合并后内容 tree | **`81cc9332899087177eb549ff8f4009c55e0e8a4d`**（与最终候选树相同） |
| 主线Actions | **27/27 completed/success**；[INTEGRATION63专项 run42982079050](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42982079050) / job **130394581346** 成功，7项测试通过 |
| 完整历史CURRENT | `docs/CURRENT-STATE.md`仍原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` /2709173B，不重新打散或替换 |

注意：首次候选的大批push历史不能作为修正后最新HEAD的通过记录；上表只计**最终HEAD**真实20/20。此验收收据是在上述主线27项真正完成后才写入，其自身新HEAD是否又有Actions需日后另核，不预称成功。CI无法读取私人Library原图，仅验证公开派生数值与旧索引。

## 事实、未知、阶段及最高NEXT

这些数字与脚本`DelItem/GetItem`只是社区后期混合档的原物理命令，不是已经运行的吉鲁原NPC、官方旧版任务流程、原客户端/服务器登录后实际行为或确认成功率；原`NpcWarp`目的地不是已执行地图跳转，`sink05a`严格解析以外部分仍OPEN。台湾1.0零售原RD图与社区NPC/物品同编号只形成**跨来源图像候选**，官方JSS1999/TW1/CN1.82同部署仍OPEN。现阶段**Stage A 7 PARTIAL+2 OPEN**，Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。不开发现代单机游戏引擎，不做联网账号/服务器运营。

**最高NEXT：** 16种水壶有据单项转换和多项命令的源限定关系已闭合。继续查重当前22域，选**不同**且有实际私有源字节可恢复的NPC地图互动、任务道具、宠物或真正原操作关系；如果没有满足来源条件的材料，准确记止点后切换，不围绕已闭合的17份sink脚本继续生产重复索引。
