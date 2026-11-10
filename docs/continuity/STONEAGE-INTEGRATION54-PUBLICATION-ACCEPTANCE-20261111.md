# INTEGRATION54｜吉鲁矿工原DAT／台湾1.0原图观察：正式合并验收（2026-11-11）

## 起点与权限、原历史保全

- 按`docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`从远端 `main` HEAD `9a14e766380e17703eb4556f7c2e28e4934ae908`、tree `9d30d0727a8bf1bafd292f5d5d27083b4e34dea6` 起步，重新读取主分支、HEAD/tree、最新提交、Actions、README、设计、历史、来源、路线及完整旧CURRENT原Git blob。
- 原 `docs/CURRENT-STATE.md` 完整 **2,709,173字节**、Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`。即使普通文件接口对大文件正文返回空串，已改用native Git blob回读并从最终候选/正式合并树核验完全同一原blob；**没有覆盖或编辑旧历史**。
- I53 三龙和I52百人道场已正式验收，本包单独选择真实有源 DAT、NPC 原文件与TW1原像素的吉鲁矿山比赛矿工，不将上一模块数字重算为新增原素材。

## 主线验收后验：各HEAD严格区分

| 阶段 | 实际远端结果 |
| --- | --- |
| 工作分支 | `agent/stoneage-integration54-giiru-miner-20261111` |
| 候选commit/tree | `9e985dc6642c3e258e1a3b49cc4293a2d9fd7e7a` / `9aed9d18efc8735929369efd026ace324c76db2c` |
| PR | [#322](https://github.com/chinaneedM/stoneage-rebuild/pull/322)，squash已合并 |
| 合并main HEAD/tree | `f136b0bd6b13c51c349269a9be1e1ad84ad95acd` / `9aed9d18efc8735929369efd026ace324c76db2c`（tree与候选完全相同） |
| 候选push+PR Actions | **46/46 completed/success**：push27、PR19，0失败 |
| 合并后main Actions | **27/27 completed/success**，0失败 |
| main专项CI | [run #42923919035](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42923919035)／job `130205422745`，`python -m unittest discover -s tests -p 'test_stoneage_integration_module_54.py' -v` completed/success |
| 候选专项CI | push run `42923736365`、PR run `42923770383`均真实completed/success |

PR差异仅有**5处公开权利安全文件**：新派生来源JSON、新专项回归、新工作流、新连续性文档、README加法索引；没有原DAT、NPC全文、商业SPR/RD/PNG、私人ZIP或HTML。CI只对仓库里已发表的源派生数字、原文件SHA和负证执行自动校验，**不会读取私人商业资产，也不是原游戏运行验收**。上述27/27仅属于合并内容HEAD；本收据本身后续单文件提交不能提前据此宣传自己的新HEAD也跑了27项。

## 本轮确实复读的原实物与独立私人保管

- `StoneAge-QUEST12-mining-competition-original-private.zip`：**113,328字节/SHA256 `d93aea416ea40a336e9c05a7cd851dbfc557916322f00152d91224f717c54cd9`**，32个 ZIP 成员CRC全过。实际从ZIP提取`31805.dat`、`31806.dat`各15,008B/50×50，原全SHA与此前QUEST12一致，重新计算原物理三平面**五个原格**。独立回读矿工`300/sb_bac.create`全SHA`3bd43fdb15482cbde4896ded79c5382b777f8e74fe0c0637b97bfa0034613388`、`300/sb_bac.arg`全SHA`93b2893ee9cf5b0229072a9283f8fbb703004cbc2ec3829fb35af71ebdf1bc30`，原`borncenter=26,23,1,1`、`graphicname=100401`，和NPC/矿道许可证静态原字面源参数精确关联。**这不是新发现两份原DAT或原地图已能行走的证明。**
- `StoneAge-PET07-original-sprite-private-catalog.html`：**15,123,277B/SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`**；从独立台湾1.0零售原资源的PET07既存私人PNG字节真正取回编号**82737–82744的8幅**，逐原PNG SHA及RGBA尺寸与PET07真原源RD先前收据一致。只是本轮再次实物观察已解码8张原像素候选，**不是本轮新增8个RD解码**。
- 由两份真读实物组成的私人现代对照研究图（非游戏客户端画面）SHA256 `1516e83cda96ca3a3622fad7f96f89b36f17f30a4d3de50325216459c2973a2a`。私人ZIP `StoneAge-INTEGRATION54-Giiru-miner-map-TW1-sprite-private.zip` **593,529B/SHA256 `3d296aea5359ecfa13f1e17857f42923208272374c070bd475c0c1bca07805fe`**共10成员，已实际上传用户个人Library，随后**重新物化下载**，全包字节/整SHA、10个CRC、研究图SHA与8幅图片逐SHA均通过。保管不代表原图可获开源商业发行许可。

## 关键严格负证和不能晋级的结论

- 台湾1.0零售`graphic 100401`原SPR索引364，原完整段SHA `0284af96efdff07da2b5b73ccc3f8a84a2a4158e9c653e3a4f3977293f3ec2a4`，本轮可观察严格已验动作2/方向0六帧、动作1/方向0两帧。**动作0/方向0的26位置序列**在PET07因bitmap **82729** 源RD严格RLE越界而被正确隔离：`STRICT_RD_RLE_DECODE_OVERRUN_NO_PIXEL_FABRICATION`；PET15后来bounded terminal-zero的104序列可观察资格，不能追认PET07的**严格无损**像素。
- 同保管mixed25社区资料里，图号100401对应原宠物表模板500/544/713/719；模板719的`PETFLG`主表1、另一候选表0，源SHA不同。图号与角色名称、外形相同都不足以证某一唯一宠物、可捕获物种或哪个服务器表实际激活。
- 原`borncenter`不是已运行的唯一出生点，`item=2535`不证原生掉落，原来源`WARP=31806,34,6`与`FREE=ITEM=2527`不证实际传送/扣费；三平面49157不自动解释碰撞。跨载体TW1原图和后期mixed25 NPC、原DAT**未认证官方同构建同服**，1999日本JSS与早期大陆1.82身份均OPEN。
- 原图文件正文、RAR/ZIP、RD、DAT与客户端原生执行没有发布到GitHub。新增原图源组0、本轮从原RD新解码0、原版游戏运行0。本包只达到`ACCEPTED_SOURCE_BOUNDED_PRIVATE_PIXEL_OBSERVATION`。

## 后续优先级

本矿工场景、两DAT、同号100401的8幅严格候选像素关系已形成有保管的档案；没有新的原源字节不再重复此工作。原82729的原RLE严格规则、同部署NPC渲染、任务／敌人执行继续OPEN。

**最高NEXT：** 选择本矿山、三龙、百人道场之外**具有可取得原DAT和NPC/物品/宠物可见源图，但尚未完成实物场景关联的下一独立村庄或剧情区域**，复用已有私人原图观察器/分类层级；若无真实证据则清楚止点并转其他22域模块。始终保留 **Stage A7 PARTIAL + 2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；overall_percent=null**，不启动网络服务器、账号、MMO或未来新单机引擎。
