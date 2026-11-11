# INTEGRATION58｜波鲁龙巢三原DAT／龙王事件63／台湾1.0原图32张：来源保管、主线与Actions验收（2026-11-11）

## 最新远端基线与来源分层

从仓库最新main `6e9b490db6022bc98256b8d3714fcea181d1708e`、tree `6814dc032293b038617d1d3af7138acbcff307ae`启动，重新读取远端分支、最近提交、Actions、协议与完整 `docs/CURRENT-STATE.md` 原Git blob、README及设计/历史/来源/路线、按模块优先级与INTEGRATION57正式验收。当前工作的事实来自**本轮GitHub远端现场读取**而非旧聊天SHA。原`CURRENT-STATE.md` 2,709,173B/blob `c89e0e33537990aa2132b47c40fef49a985a935c` 通过Git原blob成功读取；正式main tree又确认文件完全未修改。最新任务离开已经闭合的吉鲁、梦幻洞窟守卫、牧场、矿工、三龙和道场，切换到波鲁龙巢三个原场景有据原图关联。

## 私人原件与可复核的实物结果

- 后期mixed25社区保存的私人 QUEST24 `StoneAge-QUEST24-poru-flag63-four-scenes-private.zip`，23,451,751B，SHA256 `75aad7150fe4ffd4db0da16bc5de92f8ed3c61073beb2fa709a9ad19c8ba83ac`，578/578 ZIP成员CRC成功。实际读取`5509.dat` 21,008B、`5510.dat` 21,608B、`5511.dat` 5,408B完整原字节及SHA，并按三个非交错小端uint16平面在CREATE格(37,35)、(16,50)、(17,12)分别读`407/0/49152`、`4206/0/49152`、`4204/0/49152`。原`poru01.create`#21/#27图100388、`boss.create`#0龙王图100373及对应完整原NPC参数`wpm_5509_35_35`、`wpm_5510_16_50`、`boy04`被重新实读。
- 原`wpm_5509_35_35`有字面`WARP:5510,16,49`、`FREE:ITEM=2414`，龙王原脚本保留`NOWEV=63`、`GetPet:352`、`EndSetFlg:63`；QUEST24旧证已配对社区模板303/图100373。此为静态来源关系而非执行过的传送、宠物领取或原服剧情。
- 另一独立零售台湾1.0 PET07原像素HTML **15,123,277B/SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`**及先前原RD源凭据 **1,617,404B/SHA256 `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`**均整包重读哈希合格。TW1 SPR图号100388组354和100373组339在旧PET07/PET15两份公开源索引严格核同；已存0/2/1动作方向0的52+27共79个原有序帧位置，对应18+14共32张**真正已解码但非本轮新解码的原PNG**。32/32 PNG整SHA与旧RD收据匹配，32张原PNG图像大小全部Pillow实读吻合；本轮`原始RD二进制重新读取=0`、`新原RD解码=0`。
- 本轮新私人证据包`StoneAge-INTEGRATION58-Poru-three-scenes-dragon-original-pixels-private.zip` **8,265,963B/SHA256 `a6262443dabe1181e2ebbbab99fca3e31b98cd316d2d67f17e290a0d2a8892a2`**、47成员CRC全部通过，内含选定3原DAT／7原NPC或模板、3张此前真实源地图画布的现代观察图、32张原TW1图片及完整摘要（私人素材未公开）。已经上传个人Library `/石器时代/`，**独立另路下载并重新验证整ZIP SHA/CRC、46份内部源清单SHA和32 PNG解码/尺寸/SHA成功**。现代私人对照图SHA `5e27154dcdadb30965707b55d3b54a8534dce6841cd68eb8d8a3f51176b14a59`，采用原地图和独立美术左右分列而非贴到地图冒充原生截图。
- Git只有[来源数字、三原DAT格、三个CREATE、旗标63的静态关系与32原PNG来源SHA](../../research/recovered/STONEAGE-INTEGRATION58-PORU-THREE-MAP-DRAGON-FLAG63-TW1-32-PIXELS-R1.json)、专项测试及CI、说明、README五个版权安全文件。没有上传原商业DAT／脚本文本／PNG／HTML；公开CI不从私人Library取原图。

## 逐阶段远端验收（不是预先预计）

| 项目 | 本轮GitHub真实验收结果 |
|---|---|
| 候选分支 | `agent/stoneage-integration58-poru-dragon-20261111` |
| 候选HEAD | `92851bcd6949e740218bbac16fb59bbfdcd273cd` |
| 候选tree | `aa3ab0e1aabe4b2ebbbe48f26217d6cad57ab9a0` |
| PR | [#326](https://github.com/chinaneedM/stoneage-rebuild/pull/326)，mergeable clean且main未移动后，按固定候选HEAD正式squash合并 |
| 候选Actions | **46/46 completed/success**：push 27、pull_request 19；专项push [run 42952135230](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42952135230)、PR [run 42952181012](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42952181012)均成功 |
| 内容main HEAD | **`c5d15d44a034c68ed3c0dd834c0fb485804608ea`** |
| 内容main tree | **`aa3ab0e1aabe4b2ebbbe48f26217d6cad57ab9a0`**；和候选tree一致 |
| 内容main Actions | **27/27 completed/success**，专项 [run 42952257231](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42952257231) 的`python -m unittest discover -s tests -p 'test_stoneage_integration_module_58.py' -v`实际success |
| 历史 CURRENT | Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`／2,709,173B完整保全，无覆盖 |
| 私人原件 | Library存储且独立整包/成员CRC/图像SHA及尺寸回读成功；保管不以临时CI工件代替 |

## FACT / OPEN 严格限界

**FACT：** 原DAT源字节/格、静态配置/参数、独立台湾1.0原图像候选数字与存储图片都真实存在且已从各自原件核验；相同图形编号与先前社区物品模板及任务静态命令可建立可追溯的跨载体候选联接。

**OPEN：** 原历史官方版（含日本JSS1999、TW1.0、国内1.82）是否采用此社区NPC配置、相同客户端/服务端原部署、龙王原生选图/配色/对话/站位、地图碰撞、WARP/ITEM执行、事件63实际得宠及回档。79出现位置不等于79不同图片；32不同位图不是32种宠物；无原商业客户端/服务端原生执行、无Stage B启动。本工作阶段仍为 **Stage A：7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**，总体百分比未知。

**最高NEXT：** 已为龙巢5509/5510/5511/100388/100373建立来源限定静态关系，不重复同一材料或增加观察器。下一轮优先寻找另一类真正有新原件的玩家可见资料，尤其原物品/装备／技能／配方与原地图、NPC或任务之间的具体可证关系；没有新原本体就如实登记缺口并轮换，不做游戏新引擎、账号网络或体验优化。

**此页只在上述内容main 27/27 Actions正式成功之后追加；该验收收据提交自身的HEAD未在此提前宣称又有新的Actions。**
