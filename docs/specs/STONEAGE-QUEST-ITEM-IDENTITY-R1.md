# QUEST-ITEM-IDENTITY-04：伐木物品的有限后代模板候选

日期：2026-10-17（Asia/Shanghai）。目标是把已有伐木指南的手环、采伐许可、断斧／改造斧／交差新斧名称候选，连接到有固定出处的后代物品表。不是恢复原始商业服任务，不从同名生成TW1.0物品ID。

## 来源和停止条件

既有recovered25保存包取得步骤固定两个分卷与合包SHA256，只在临时目录解压，不执行服务端程序。两个目标表必须分别满足既有尺寸、SHA256、94列、唯一ID与总行数：

| 表 | 字节 | 行数 | 既有setup记录 |
|---|---:|---:|---|
| itemset.txt | 3392473 | 13252 | itemset3/4/5/6file引用 |
| itemset0710.txt | 3668487 | 13910 | 未引用的修订候选 |

新提取仍读取实际setup并记录其字节hash，不能仅凭文件名认定生产服加载。0710不是已认证年代。没有合格取得路径、hash不符或查询无命中时就保留该缺口，不以近似包替换、不反复扫网或复制全部物品内容。

## 候选如何判定

工具 `tools/stoneage_quest_item_identity_probe.py` 只匹配预先列出的杉／衫手环、伐木／采伐许可及哈恩斧头字面词，分别检查UTF-8、GB18030、Big5下可严格解码的name和secretname字段。记录命中的查询词、编码候选、字段、是否整名相等，以及原始名字字节hash；不自动简繁归并，也不认定整个表都属于某一种编码。

命中只是筛选候选，尤其不能把包含查询词的强化品、显示名和隐藏名当同一原版物品。每行记录模板ID、行位置、整行hash、有限数值和生命周期标记；源内名称／描述／函数参数／整行原文不保存。每张表候选上限100，超出就失败并要求重新限定查询。

同一表要求模板ID唯一；跨两表的相同ID另列名字字节是否相等及数值变化，不由ID相同单独推出任务身份相同。断斧、修复斧与交差斧继续分阶段。

## 数值与使用边界

属性保留 `raw_a/raw_b` 两列，不在本包猜成最终装备数值或固定随机结果。`cost`只是源内字段，不直接当塞尚的回购单价；指南14木约5000仍是约数。`level`不直接当任务准入。类型值不绕过既有条件枚举归属；掉地／注销／宠邮／合成标记也只是该后代表的字段，不认证初代实际执行。

手环在后代表里的魅力候选即使与某篇指南数值相近，也不能据此解决早期指南魅+5/-5之争。原始item/NPC/event身份、任务派发和持久化仍未证明；现有普通掉落运行代码不改。

## 验证入口

```bash
python -m unittest tests.test_stoneage_quest_item_identity_probe -v
python tools/stoneage_quest_item_identity_probe.py --data-dir /temporary/gmsv/data --setup /temporary/gmsv/setup.cf --output /tmp/quest-item-derived.json
```

六项合成检查覆盖不同编码与不同字、整名／部分命中、空值／零／负值、行位置、94列／唯一ID／布尔标记及伪表hash拒绝。独立CI只能上传派生JSON；实际取得结果、候选与永久归档验收需以随后记录为准，不能把合成检查通过当实际来源成功。

Stage A仍未终验、九族7 PARTIAL+2 OPEN、Stage B GATED，R79暂停。普通继续不解释为进入新作设计。


## 实际取得的五个候选（两表一致）

[Action38993481443](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/38993481443) / job117280730238成功：旧保存包的分卷与合包hash、两个master表hash、实际setup全部通过。独立环境可取得；之前本地POST405／GET非JSON失败仍保留。setup9715字节/hash `b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d`，四个配置键均引用itemset.txt。

两个表各命中五行，name与secretname在Big5候选下均为预设词的整名匹配；其余编码没有这些命中。下表名称是查询词标签，非导出原始条目全文。

| 查询角色／标签 | 后代模板ID | 部分原始数值／标记 | 不能推出的结论 |
|---|---:|---|---|
| 交差斧「哈恩的斧頭」 | 2465 | 攻35/35，防-15/-15，敏-15/-15；level25 | 不等于改造斧，不把level25当任务准入 |
| 「採伐許可證」 | 2478 | cost10，图像24222，vanishatdrop1，dropatlogout0，canpetmail0 | 未取得NPC配置证明它就是该流程实际交回的许可 |
| 手环「杉的手環」 | 2481 | 攻8/8，防5/5，敏-5/-5，魅-5/-5；level30 | 与2003指南数字相近，仍不能认证早期魅力-5或消除+5差异 |
| 「折斷的斧頭」 | 2484 | vanishatdrop1，dropatlogout0，canmergefrom1 | 字段不等于实际合成／修理事务已运行 |
| 「伐木許可證」 | 20197 | cost0，图像24222，vanishatdrop1，dropatlogout0，canpetmail0 | 与2478同图、同销毁字段仍是不同模板与名字字节，不能合并 |

这五个ID在两表中均有相同名字／隐藏名字字节、相同完整行hash和所选数值；物理行位置不同。两份修订表不是两个独立历史规则作者。固定查询中的改造斧未命中，只说明本次词表未找到它，不能说游戏没有改造斧。

原始派生JSON为16378字节，SHA256 `9ee594a8f9871a675c320f30c3ea727bd6eb92e5fa34584a0078bc0d42480618`，永久Git blob `d0ac9e5f5d26db5afcee07119295fd05803011b9`。下载artifact12085893496 ZIP2092字节、SHA256 `bb5a6cbedae5f06e2f12c2a51c8a2b259e6899d6757b4f79f517fa7cf258b8e8` 与API一致。详见[永久报告](../../research/recovered/STONEAGE-QUEST-ITEM-CI-DERIVED-R1.json)及[验收链](../../research/recovered/STONEAGE-QUEST-ITEM-ACCEPTANCE-R1.json)。

归档后增加raw JSON大小/hash/Git blob、元数据一致性、来源晋级/重复ID/伪编码/比较篡改反例，共9项本地检查。后续归档CI重放永久元数据和这些检查，不反复下载整个原始保存包；只有首次缺归档或显式workflow_dispatch才执行原始资料取得。未把归档重放称作一次新来源获取。

**Highest NEXT QUEST-NPC-ITEM-BINDING-05**：在同一已认证保存包内，仅追踪这五个ID在现有NPC配置／参数语法中的来源角色，区别两种许可、交差斧、断斧和手环的发放／收回关系；利用现有NPC参数解析，不用普通数字grep冒充绑定。不穷举全世界/NPC，不因本次未命中而扩大改造斧搜索；无明确参数或脚本时保留UNKNOWN。后代绑定仍不倒填台湾1.0，Stage B保持GATED。


## 归档后验收与后续绑定约束

归档Action38993879936/job117281964762已通过9项检查及永久元数据重放，原始包取得步骤明确跳过；main非强制整合至c4a36fc4a755bfa673bf5306a4362e51ba173438。新增提取AST合同和schema-helper指纹核对后本地共11项；它们固定第一次真实源实验所用的提取函数／查询／常量，提取逻辑改动不能只靠旧派生数据蒙混通过，须重新来源验收。

[下一项绑定预检](../../research/recovered/STONEAGE-QUEST-ITEM-NEXT-BINDING-INTAKE-R1.json)只固定已有解析工具和五个目标ID，尚无NPC配置抽取结果。GetItem／DelItem方向必须按实际FunctionSet解释；FREE条件、普通ItemShop商品与ExChangeMan发奖不混为一谈。模板歧义和缺参数文件仍算缺口，数字命中不直接算任务绑定。
