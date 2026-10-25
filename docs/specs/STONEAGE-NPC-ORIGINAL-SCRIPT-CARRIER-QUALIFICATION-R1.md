# NPC-10：玄黄事件脚本的既有保存包载体资格补正

2026-10-25（Asia/Shanghai）。结果：**找到既有混合保存包中的精确成员证据；官方同构建归属仍OPEN**。

## 实质新增及前轮补正

本轮目标是确认 `100/sb_kbu.arg` / `100/sb_geno.create` 是否有独立载体、父包摘要和历史地区/build，停止于一组精确载体结果或具体缺源。不再扩现代社区脚本解析器。

NPC-09说未有独立原始载荷及共同原服包SHA，需要限定：**未认证原服包**仍正确，但仓库早已存在独立混合社区保存包的这两个成员及模板摘要。该既有线索不应遗漏。本轮将两份历史清单与父包链实际接通；不称新下载原文件，也不将清单当本轮读过正文。

来源页 https://www.lab.welovesa.com/viewthread.php?extra=&page=1&tid=219 的两卷保存包（服务元数据显示2012-04-07/08，不是游戏发行日期），完整包361255180B、SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。原成员共同位于 `石器2.5客戶端+服務端+登入器/SA2.5服務端/gmsv/data/`；标签2.5及目录名不认证官方地区或build。

| 相对路径 | 原清单字节数 | 两份既有清单一致的SHA256 |
|---|---:|---|
| npc/100/sb_kbu.arg | 258 | 433d17a58869147f91cacc57487795d7686b53415872f0694aba02dbc869502b |
| npc/100/sb_geno.create | 573 | 5aec44349ae3a6071b0882fd40d693f3bf1e7bdaf9ba489ac3ffbc89e26331f1 |
| npc/100/sb_geno.template | 321 | 76a826f1022276dfa9590e5ad51c6a96e9c88146a2fc39790c2cc60cbed60e2d |

完整原路径、父包摘要、清单Git blob与字节摘要固定在 `research/recovered/STONEAGE-NPC-ORIGINAL-SCRIPT-CARRIER-QUALIFICATION-R1.json`。重放分别读取旧static inventory的精确成员尺寸/ALL-FILE SHA与旧gameplay inventory的CANDIDATE行；两份报告属于同一次保存包证据链，**不是两次独立取源**。成员SHA未重算原正文。

## 现代内嵌样本并非同字节

固定现代 `75912001/sa.desktop` 提交 `e9b3f0cfd63b93c11fc77ca5331173dd6c5d2fc8` 的YAML内嵌 `sb_kbu.arg` 亦258B，但SHA为 `961b87cebad2fd7cb7875f9433df0e301f9f64b06c46a558475fc1a0344e9eec`，与保存包成员不同。相同路径/长度不能当无损复制；没有旧正文实读，无法判别编码转换、文本修改、数值差异或逻辑等价。现代2NPC/3warp计数及NPC-09真实失败/订正原样保留。

另检查该固定上游完整Git tree：10532项、truncated=false，未见独立 `sb_kbu.arg` / `sb_geno.create` 路径；这仅限该提交，不推全网没有原件。有限双引擎精确文件名检索出现2011及后续社区目录说明/转抄，未得到有历史官方地区/build的父包；检索结果不是认证服务器原件，未抓原HTML摘要，不报全网灭失。既存JSS2000-04-24洞窟进程修正仍独立，不与混合包合成为原版任务。

## 验收及止点

8项单元含六个逐成员双清单摘要变异、重复候选、父包大小/摘要、同长替换、官方晋级拒绝；语义检查独立于整文件摘要门。全量永久派生报告离线重放，不下361MB包，不存原脚本对白或程序。原服NPC/任务/奖励新增0，DD-028仍ORIGIN_UNRESOLVED，Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，总复原百分比null。

两轮NPC证据均止于归属受限，现回22域原件队列。最高NEXT **WAYI-OFFICIAL-SAEXE-LOGIN-RESOURCE-CONTENT-11**：从既验官方fileid335出链的小型369152B sa.exe样本（SHA `4b5a059b45b589b609ca925d210d76838be1e970b805fab3df863b7d563fbb38`）静态读取PE资源目录、实际菜单/对话框/字符串表的可用标签或精确缺失；先查既有派生是否已完整覆盖，已覆盖则改选有具体新载荷的其他域，不重做511路径字符串/UPX哈希。仅在有新增内容问题时一次取该小样本，不执行原程序、不过度展开调用树。官方列表2005与实际2006捕获分离，不称TW1/JSS初代登录UI或实际运行画面。止于一份实际资源内容规格或缺失结论。原始大包长期保管仍暂停，只有新来源/官方同build凭证或可读旧正文的实质比较依赖才重开NPC；不继续目录转抄/helper链。
