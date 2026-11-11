# INTEGRATION55｜恐龙牧场三条宠物条件与台湾1.0原动画：正式合并、私人实物保管和CI验收（2026-11-11）

## 起点和远端单一事实源

- 重新按 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 自GitHub远端`main` **`ac262f06d8d32ecf75d0bfec773d4f0bc2123f85`**、tree **`954b0a6b8ae44cad8dd0a51fe294800de1dedfb1`**启动；核对远端分支、HEAD/tree、最新提交、Actions，重新读取README、协议、设计/来源/历史/模块路线和**完整** `CURRENT-STATE` 原生Git blob。无开放PR/issue。
- `docs/CURRENT-STATE.md` 经Git blob回读的完整历史原内容**2,709,173字节**、blob **`c89e0e33537990aa2132b47c40fef49a985a935c`**；内容合并后的正式main树仍是完全相同文件。未作删改、重建、截短或假装普通文件API返回空正文意味着真实空文件。
- INTEGRATION54矿山和INTEGRATION53三龙已验收，依照最新NEXT转独立真实**恐龙牧场**三条宠物兑换/凭证任务，形成可见二维原图、源脚本及人物配置相互可查的内容关联，不重复原矿工或百人道场。

## 已完成的提交、正式验收（每一HEAD分别记录）

| 核验阶段 | 真实结果 |
| --- | --- |
| 开发分支 | `agent/stoneage-integration55-ranch-three-pets-20261111` |
| 候选HEAD | `aeb378a0f3a5212879aab118f2df8e7ae49ccb4b` |
| 候选tree | `9bacb66e10cdaa4e3ab6947875436fb557c08210` |
| PR | [#323](https://github.com/chinaneedM/stoneage-rebuild/pull/323)，已真实squash合并 |
| 正式内容main HEAD | **`76b74cf2934b5fd03d4008db9efbe160b418d763`** |
| 合并后main tree | **`9bacb66e10cdaa4e3ab6947875436fb557c08210`**，与候选tree一致 |
| 候选push+PR CI | **46/46 completed/success**（push27、PR19），0失败 |
| 合并后main CI | **27/27 completed/success**，0失败 |
| 主线专项核验 | [run #42929098675](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42929098675)，job `130223016541`；步骤`python -m unittest discover -s tests -p 'test_stoneage_integration_module_55.py' -v` completed/success |
| 候选专项CI | push run`42928914621`、PR run`42928961512`均completed/success |

PR准确只有**五个公开权利安全文件**：新增来源关系派生JSON、11个专项合同测试、新小型Actions工作流、连续性报告和README追加。**无原商业动画、DAT、RD、PNG、NPC全文、私有HTML/ZIP入公开Git。** CI只能验证**已经公开的衍生哈希及数字**，没有访问、下载或运行个人Library的商业原资源；主线CI成功不等于原游戏真实宠物交换或跨版本官方同服得到证明。

## 本轮真正私人原来源复读结果及永久保管

1. 原后期mixed25社区任务包`StoneAge-QUEST17-dino-ranch-original-private.zip`：**29,802字节／SHA256 `07fac6014b9eeef0a352d8c7b74f2fb1ac47cd97347ed796d16a0c7a52243081`／32成员CRC全过**；内部公开源索引原Git blob准确为`20bae57956e9b3a25df94a71f47fff0641b81b4d`，同仓库QUEST17，直接重读原`bait_03a2/b2/c2`，分别见到`DelPet:PET>0-560/559/558*4/3/2/1`四套字面、两处`DelPet:EVDEL`等；原CREATE的牧场楼层201上三名配置依次为(19,13)/(19,14)/(19,15)，另三名NPC和20901楼层原配置亦保留。
2. 台湾1.0零售以前真实从源RD解出的PET07完整保存HTML`StoneAge-PET07-original-sprite-private-catalog.html`：**15,123,277字节／SHA256 `58e8ee4ff5165ed2f61663d67ae1cd0a8183622fa3375c480232784bfce9dc76`**。同时复读前次独立原RD源凭据JSON**1,617,404字节／SHA256 `b5ad2e58930afbe90604a1d72e3c17ab0adea446e7c118be775e3973315e6cb4`**。从原HTML真实提取三组图号100271、100335、100368各**16张不同原PNG**（48张），逐SHA、尺寸与真实原RD来源凭据一致；选中源动作0/2/1方向0的原序列共16/17/54个**位置**，最后一组有重复位置，不能当54张不同原图。本次不是新的商业RD解码：原RD新解码数**0**。
3. 社区两份原宠物模板表将原条件数值`560/559/558`映射到图号`100271/100335/100368`，两表各自原行SHA相同、PETFLG字面1；但这三图号各还有其他不同模板，共用画面并不证明唯一原物种或玩家真实拥有某宠物。台湾1.0独立源SPR原段索引分别**261/305/334**，各56个原SPR序列有已核原哈希。三个晚期原凭证ID分别2594/2595/2596；原社区物品表指向候选图号22120/22114/22118，四幅已真读台湾1.0物品原RD图候选（含另一个多物品复用图号24222）的SHA从QUEST17私包核同。跨载体为**有资格候选的数值联接**，从未认证同一官方运行部署。
4. 以上48幅原动画PNG、4幅原物品PNG、1690×1260私人研究图和逐字节源保管收据构成**54成员**私包`StoneAge-INTEGRATION55-ranch-three-pet-original-pixels-private.zip`，**582,786字节／SHA256 `970326a4169e5ffb6a9a70b8219162e6d59c319f1f151afb048781ebde9b23e8`**。私人研究图源SHA256 `a7c3799d4b883422a26eabe98d01c1f02541ed428451cdc654a784f3faa7cdcf`，不是原生游戏截图。实际上传个人Library`/石器时代/`，再**独立重新下载并逐整包字节比较，54个CRC、48个宠物PNG逐个SHA一致**。商业原画仅私人保管。

## 必须保持OPEN的内容边界

- 本轮没有实际重读原MAP09地图**201**与**20901**的DAT二进制；这两张楼层的以往原DAT SHA和70×70等原尺寸**只是旧公开索引来源限定**，不能称本轮新解出两张地图的格、拼出原牧场原生画面或测得NPC原点位站立/碰撞。
- `DelPet:PET>0-560/559/558`、`GetItem`、`NotDel`和`EVDEL`是未经原服务器运行证实的字面条件/调用，真实分支优先级、宠物移除、背包变化、领手环或任务完成都未证。后备`bait_03a/b/c`存在，但未证哪一服务器载入；没有声称三组图就是原官方三种独立宠物或哪只可以捕捉。
- 台湾1.0原美术与晚期社区保存NPC/宠物表**不是已认证的同构建同部署**；日本JSS1999起源、早期大陆1.82同剧情同图的身份仍OPEN。原官方动画帧率、真实调色板、原客户端真实画面/角色行为及新单机引擎均未运行／未开发。新原商业图字节0、新原RD实物解码0、新宠物官方物种身份0。
- 本组交付仅 `ACCEPTED_SOURCE_BOUNDED_PRIVATE_PNG_OBSERVATION_AND_TRIPLE_QUEST_PET_BRIDGE`，整库Stage A仍7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。

## 交接

**下一最高优先级：** 离开已完成的恐龙牧场图号、吉鲁矿工、三龙和百人道场，寻找**新的有资格原地图场景/原NPC/宠物/物品可见内容**，实际源文件可重读时优先完整源DATA+图片复原；若该楼层原DAT实物不在当前保管库，明确缺口，转其他来源充足的世界模块，不以假原格/引擎或账号服填空。

本收据是**正式内容CI成功后新增的单独提交**。在未观察新HEAD Actions前，绝不能把合并内容HEAD`76b74cf2934b5fd03d4008db9efbe160b418d763`的27/27称为**本收据提交自身**已经通过27项。
