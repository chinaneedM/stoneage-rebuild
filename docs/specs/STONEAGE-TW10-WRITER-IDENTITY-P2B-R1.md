# P2B 限界核查：原版对象图形号写入的来源

新读 main d04e8f55c5bb326b5fc92c9f4522ac9ede679254/tree 188c7f9202d7215b2d8c4fea9db9a926cacfacec，并遵守连续性协议、DD-028及DD-029。上一轮已经核准十个来自台湾1.0原始可执行文件的偏移0x124写入候选，但未建立对象身份。

本包只对已核源的十个RVA进行一次上游局部寄存器定义的限定复查。必须使用真实同一枚原 sa_3.exe（SHA-256 cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a）、原指令逐处SHA、以及上一轮已接受的 source JSON Git blob a9adc6a94e8e062b730e0114df581c7b4ad20d62。报告区别堆栈参数、其它内存、算术组合与局部不能识别，不将反汇编线性相邻伪称控制流可达性。

预设验收止点：原字节取回、十个哈希复核、来源类别有限统计与下一实证缺口；如未发现同构建对象/协议/具名原始主表连结，立即停掉“继续多扫一轮RVA”支线，转换为官方具名原件或原服务器master来源。与R101已验选择器、R99 101个NPC类别候选、P2A完整物理继承严格分层；不恢复虚假的物种数量、任务、成长或真实地图。版权原程序/图片不提交公开仓库。

交付工具 tools/stoneage_tw10_writer_identity_p2b.py、正反测试及独立取源工作流 audit-stoneage-tw10-writer-identity-p2b.yml。此文初始阶段不预支本轮Actions、Artifact及内容发现结果。
