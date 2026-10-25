# NPC-QUEST-SAME-BUILD-PRIMARY-EVENT-09 — 玄黄NPC事件配置的原字节边界

2026-10-25。状态：CANDIDATE_DERIVED_BYTES_NO_ORIGINAL_BUILD；不是原JSS1999/台湾1.0任务复原完成。

## 新实证：现代派生文件中存在可核的NPC配置字节

现代社区项目 https://github.com/75912001/sa.desktop 在提交 e9b3f0cfd63b93c11fc77ca5331173dd6c5d2fc8 的 map/maps/11208/map.entity.yaml（Git blob 6e066821bedd0bbef7e59cc3f020cad7783e51c5）内标示 map_id 11208、五条现代NPC记录。两条名「风的守护兽」，当代配置对象 id=4，坐标(26,40)及id=5，坐标(42,38)，均使用NPCEnemy模板 sb_kbu，引用现代文件注记100/sb_geno.create块0/1、行3/14。两处均内嵌同一份文件内容100/sb_kbu.arg；经过独立Base64解码、GB18030严格解码与本地SHA256计算，真实内嵌载荷258B、SHA256 961b87cebad2fd7cb7875f9433df0e301f9f64b06c46a558475fc1a0344e9eec，与两条注记完全相同。

该内容有 entype、askbattlemsg1、startmsg、dieact、end msg、enemyno、deniedmsg、onebattle、time 九字段。十次敌号出现为1272/1277/1277/1280/1280/1278/1273/1273/1275/1275，只有六种不同整数。time=180、entype=2是静态参数，不是原版运行时秒数或十个已恢复敌人。

现代项目 README 明确是Godot 4.6时代的重构工作。来源中的「原版」及旧路径名只是它自己的注记；至今没有100/sb_kbu.arg和100/sb_geno.create原始独立载荷、它们共同的原服包SHA、历史build和发行权限链。另有晚近社区网页https://www.shiqisifu.cc/Article/5/News_207.html列出这些路径及「玄黄」标注，但几个网站转抄同一份树表，不能算多份独立原始文件。

## 一手官方记录必须隔离

仓库既存JSS第一方 verup.html 的2001年档案记录运营方自述在2000-04-24修正「玄黄の洞窟」进程，源见 docs/specs/STONEAGE-JSS-EARLY-QUEST-ORIGINS-R116.md。它是另一个有界的官方历史声明，不能和上述2026现代导出合并为同构建原服脚本。不能从日文「イベント」或现代目录用词直接判断有限运营活动、1999首发本体或后续永久任务。

DD-028四档继续判 ORIGIN_UNRESOLVED。新认证JSS/TW1.0 NPC=0，原服任务ID=0，奖品ID=0，原服务器实际执行=未证；现代2个对象不能计2个原服实体。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总恢复百分比null，私人原客户端永久保管仍受外部存储条件阻塞。

## 接续

本次已将**实际解码字节摘要与记录位置**保存成派生JSON，不入库有版权疑义的原对白、原游戏文件或图像。下一最高任务 NPC-QUEST-ORIGINAL-SCRIPT-CARRIER-QUALIFICATION-10：只尝试有来源链的原始100/sb_kbu.arg/100/sb_geno.create或同地区同构建一手NPC事件记录；若一个有界取源单元仍没有独立原字节，转其它22域可得原始实物内容，拒绝继续重复现代目录或无源helper。
