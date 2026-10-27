# R41 保存包洞窟NPC参数异SHA与三条原始创建配置

2026-10-27（Asia/Shanghai）。本轮解决NPC10明确留下的原正文缺口：实际取得旧三文件，核原SHA/CRC，并比较现代重构文件内嵌的同名参数。证据仅属于社区混合保存包与2026现代项目，不是官方初代/同部署构建或原服任务执行认证。

## 原件取得与来源限定

原source [40451830173](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40451830173) / job122016102981 / HEAD `ea7baa5f58b496611664990854b2e4163f074c65`已实际completed/success。RAR4原目录7954头完整走查、184个严格HTTP206范围共12013836B，未超过16MiB预算、未重取361255180B整包。

原服务器`gmsv/data/npc/100/`三个成员分别为：

| 原文件 | 字节 | 本轮完整原SHA256 |
|---|---:|---|
| sb_kbu.arg | 258 | 433d17a58869147f91cacc57487795d7686b53415872f0694aba02dbc869502b |
| sb_geno.create | 573 | 5aec44349ae3a6071b0882fd40d693f3bf1e7bdaf9ba489ac3ffbc89e26331f1 |
| sb_geno.template | 321 | 76a826f1022276dfa9590e5ad51c6a96e9c88146a2fc39790c2cc60cbed60e2d |

三个完整SHA均与NPC10及旧原件清单吻合；原RAR成员CRC亦逐份验证。NPC10原报告“当轮没有读取正文”保持原样，本轮是新的实物补证，不追改旧结论为当时已读。文件名、2012保存日期及“2.5”标签仍不能认证官方地区/build。

现代对照固定`75912001/sa.desktop@e9b3f0cfd63b93c11fc77ca5331173dd6c5d2fc8`的`map/maps/11208/map.entity.yaml`，原UTF-8文件3328B/Git blob `6e066821bedd0bbef7e59cc3f020cad7783e51c5`重新取得；源端和本地两路全文件身份相同，旧NPC09完整资格门也通过。两现代NPC引用同一份258B参数，SHA `961b87cebad2fd7cb7875f9433df0e301f9f64b06c46a558475fc1a0344e9eec`。

## 参数不同字节的实际原因

两文件都是258B、9个LF、0个CRLF，**有114个字节位置不同**。纯Big5/CP950→GB18030转码无法重现现代字节，原source的`exact_transcode_candidates=[]`原样保留；不能把异SHA仅解释为换编码。

实际CP950和Big5严格解码得到同一份旧Unicode文本。与现代GB18030文本逐字段比较：6个字段完全相同；另3个对白字段`askbattlemsg1`、`startmsg`、`deniedmsg`长度分别仍为19/19/20字符，但共14个字符位置不同。九组实际出现的繁简字符替换（如繼→继、續→续）加上GB18030编码，能够**精确重现全部现代258B与原SHA**。这是本样本的有限字符差异描述，不是通用繁简转换器或服务器实际运行编码证明。

| 原字段 | 两份文件数值 |
|---|---|
| entype | 2 |
| dieact | 0 |
| onebattle | 0 |
| time | 180 |
| enemyno | 1272,1277,1277,1280,1280,1278,1273,1273,1275,1275 |

空`end msg`同样保留，10次enemy编号引用、6个不同编号不合并，也不跨命名空间套成宠物模板/物种。数字相同只说明这两份参数的数值相同；未执行原NPCEnemy、未验证时间单位或整套任务逻辑等价。原对白不公开，保管每个字段的长度、Unicode摘要和有限单字符差异。

## 原创建文件实际有三条配置

原`NPCCREATE`文件有3个创建块；`NPCTEMPLATE`有2个模板块。三条原名称字段都是“風的守護獸”，但不能按名字折成一条：

| 原块序号（0起）/起始行 | floorid原值 | borncenter前两值 | dir原值 | graphicname原值 | 引用模板 / 参数 |
|---|---:|---|---:|---:|---|
| 0 / 3 | 11208 | 26,40 | 0 | 100394 | sb_kbu / 100/sb_kbu.arg |
| 1 / 14 | 11208 | 42,38 | 6 | 100394 | sb_kbu / 100/sb_kbu.arg |
| 2 / 26 | 11214 | 41,36 | 4 | 100343 | sb_kgi / 100/sb_kgi.arg |

每块原`borncenter`四值末两值为1,1，`movecenter`为20,20,100,100，`createnum=1`、`time=60000`，全部保存但不解释单位、活动范围或实际生成数量。两模板均直接写`functionset=NPCEnemy`；各自`type`与所引用创建块的`graphicname`同整数。尚未运行原创建器或原服务器。

已有R40同保存包的完整原SPRADRN索引中，100394对应索引360，100343对应313；仅可补一个**同载体数字候选关联**。R40没有解析这两个组的完整动画，更没有本轮原RD像素/实际NPC画面认证，不能借其存在就声称已看到守护兽。

现代11208单地图中的两NPC位置与原前两创建块、原行3/14准确对应；它的3个warp节点仍是独立类别，本轮原创建文件没有warp配置。第三条属于另一个floorid11214，**不在这份现代11208文件的范围**，未查现代11214，不能说现代删掉了它。现代id4/5仍不是已认证原服NPC ID。

## 保管、独立复核及止点

独立下载artifact12710817519 ZIP18766B，SHA256 `cf0f71c52732f9aebaedd003200484c0753a3f4df0a169cb8190333092038605`与API一致，恰含原样派生JSON和CMS密文。原报告99960B/SHA `b51bbe6ecff9f2763b5f3725ca98d20a0fec2db9cab4085c0dc687fb62ea707d`逐字节归档。私人解密ZIP927B/SHA `462ef782d75e24ba849b00594bbec0f468409754259632fee92b05b857b7eea7`后，三个原文件又独立逐全SHA核验；本地直接比较完整旧/新文本，14位置/9字符对转换后的全部258B精确同一。明文/密文/私钥均不入Git，临时私人副本不宣称已有长期保管。

`SOURCE-R41`保留不可改写原始派生、`LOCAL-COMPARISON-R41`保留独立实际原字节比较、`MATERIAL-R41`保存所有原块/字段位置及限定NPC记录，`CUSTODY-R41`补全run/job/ZIP/raw/Git来源链。离线门拒绝把纯转码失败写成成功、把字符变化掩盖数值变化、丢失第三配置、未知语法被静默跳过、官方/本体任务/执行晋级。旧失败/订正和早期JSS洞窟公告继续分别保留。

最高NEXT `PRESERVED_GENKOU_THIRD_GUARD_ARGUMENT_42`：本轮第三配置实际引用旧`100/sb_kgi.arg`，既有清单281B/SHA `61c2aefca26c9d84db061f34c66c74b980006cac915fe732394f753daddbd586`。仅有界取这份实际文件、核原完整SHA后与已得sb_kbu参数比较，恢复第三模板具体引用/差异；不凭sb_kgi名字猜任务次序或敌人身份，不下载大客户端。取得一份有限实质结果或精确缺口即止，再回22域其它内容，避免扩同一NPC helper树。

本包没有认证任务名、原初版本、奖励、进程条件或实际战斗，DD-028保持`ORIGIN_UNRESOLVED`，新增认证本体任务0。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、P3E阻塞、overall percent=null保持。
