# WORLD34-R2｜混合2.5服务端RAR解档尾部失败与完整PE装载段证据（2026-11-06）

**来源与启动。** 新核 GitHub main `d5d0603e73849eb2b456b90e822164188b8ee4d7`，tree `fd7c1e7d6d1ec0a9388daca2a3b798e27a211866`，此前 WORLD34 研究/回归及 main Actions 成功。完整历史 `docs/CURRENT-STATE.md` 原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` **保持不改**。本工作严格 Stage A 原版恢复；公开只提交派生哈希、坐标和检查器。

## 本次实际重新检查的原字节

用户私人Library保存的社区混合2.5 RAR `361255180B`，整包 SHA-256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5` 再核相同；配置中实际使用的 `itemset.txt`、`setup.cf`、`stoneage2.5/sa_2903.exe` 与此前完整 SHA / RAR CRC 一致。三条物品 `1232/12530/12555` 的94列原行（含CRLF的物理行SHA）、参数「體600／體320／氣20體185」、场景1/0/2与目标2/1/1全部逐原字节再次校验，使用字段与来源行不可互换。

`gmsv/gmsv.exe` **整文件仍然不通过CRC**：普通libarchive输出 `1,835,008B` 后 `File CRC error`；block模式虽输出 `1,897,867B`，但 SHA256 `e61c417b18f939a22d25b800240f1d2d0f889a78024a8657e06502ff0ccdff0f` 与既有原完整 SHA `d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00` 不同。本次没有替换原件、发布二进制、运行原服务、宣称整 EXE 完整恢复。

关键新定位：实际PE包含四个有原始文件字节的装载段 `.text/.data/.rdata/.idata`，它们的文件偏移末端分别为 **1,419,776 / 1,633,280 / 1,739,264 / 1,742,336**，均严格小于普通libarchive已输出的1,835,008B。COFF符号表从1,742,336起有5,210×18字节记录，其记录末端为1,836,116；读取中断点1,835,008**位于COFF符号记录内部**。这使原执行代码与数据装载段位于当前可读区之内，但**不等于整个原 EXE 或全部装载段的历史原SHA已独立证明**。

本轮用Python独立从当前真实前缀PE头解析各装载段，重算四个整段SHA，并对旧 WORLD31 服务端6窗口、WORLD33服务端12窗口及客户端5窗口逐一重算SHA——**23/23精确匹配**。另追踪14个物品使用关键静态调用/跳转：`lssproto_ID_recv 0x41324c→CHAR_ItemUse 0x4746e0`、`0x4748a8`以整数键19取回调函数地址、`0x474a00`间接调用，以及`ITEM_useRecovery 0x500590`按工作键0选择战斗（0x50060f）/场外（0x500629→0x4fe4d0）分支。场外函数内部存在原 `CHAR_setInt` 属性写入调用和两个 `CHAR_DelItem` 调用点。它们属于**可到达的代码结构**，不是任何指定物品已真正写入状态或已删道具的动态结论。

[本次静态来源派生收据](../../research/recovered/STONEAGE-STAGE-A-WORLD34-R2-MAPPED-PE-SOURCE-R1.json) 保留全部装载段SHA/COFF边界、14个源指令SHA/相对跳转目标、先前源资格及明确未证的结果。新[私人可运行核验器](../../tools/stoneage_world34_mapped_pe_source.py)从调用者提供的本地已解档前缀、客户端和itemset重新做整段及上述历史窗SHA和原94列逐行比对，不会启动原二进制。公共CI只跑不含原商业字节的结构/反例测试：

```sh
python -m tools.stoneage_world34_mapped_pe_source /private/gmsv-prefix.exe /private/sa_2903.exe /private/itemset.txt
python -m unittest -v tests.test_stoneage_stage_a_world34_r2_mapped_pe_source
```

**NEXT WORLD34-R3（仍OPEN）**：取得完整 SHA/CRC 有效的同一 `gmsv.exe`（先评估可用的另一Rar算法），或在每条实际执行窗均单独证明源资格后采用有界隔离原指令观察。实测场外入口→回复回调**返回**，三物品scene1/0/2、角色/宠物/队伍目标、数值写入及背包删除/拒绝。没有动态原程序返回结果，不将“静态有分支”扩大成“场景1可使用”或原官服漏洞；混合保存版不等同台湾1.0/JSS1999/大陆1.82。Stage A仍 7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null。
