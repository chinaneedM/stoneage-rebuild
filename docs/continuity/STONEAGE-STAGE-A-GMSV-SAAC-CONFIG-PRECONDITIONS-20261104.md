# Stage A：原 GMSV/SAAC 账号连接静态先决条件核验（2026-11-04）

**当前事实源**：`main` HEAD `06d0a46547354c5b657ba0d84403074a2a1eb1ac`、tree `c6501c16b219f219805ce2daa7818d61bd50f5ce`。历史 `docs/CURRENT-STATE.md` 原 blob `c89e0e33537990aa2132b47c40fef49a985a935c` 完整保留。严格处于 Stage A 原版复原，不制作新石器、不优化玩法。

## 实际取得的来源和新事实

本轮从用户私人资料库重新取回保存的 **361,255,180 字节**混合 2.5 RAR，实际整文件 SHA-256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，与历史 MAP01 记录相符。使用 `libarchive 3.7.4` 真正解出原 `gmsv/setup.cf`（9715 B）、`gmsv/setup.cf.bak`（9719 B）、`saac/acserv.cf`（807 B），每份输出均按 RAR4 原成员声明长度、CRC32 及新算整件 SHA-256 验收。原文件本身及认证字段未进入公开 Git，见[无原文的完整来源收据](../../research/recovered/STONEAGE-STAGE-A-GMSV-SAAC-ORIGINAL-CONFIG-PRECONDITIONS-R1.json)。

对原文件逐行读取后确认：GMSV 指向本机账号服务（`localhost`）及端口 **9200**，SAAC 也按原配置监听 **9200**；GMSV 的游戏监听端口配置为 **9065**。双方账号认证字段均有原值且彼此逐字节相同；GMSV 备份配置亦匹配。安全边界：**不发布认证字段的实际值或其单独摘要**。GMSV 原创建容量配置数值为 `npctemplatenum=256`、`npccreatenum=8192`，它们是配置参数，不是已成功创建 NPC 的数量。GMSV 当前与备份文件均有525行，仅一行 `PET1` 字段值不同；不从中推断已部署配置的唯一版本。

## 对既有原生启动证据的有限增量

此前同归档 GMSV/SAAC 在隔离、无网卡 QEMU/Wine 来宾中持续运行90秒；15、30、45、60、75、90秒的内核采样均观察到9200与9065两个监听端口。原 GMSV 控制台记录716份地图完成该阶段读取、搜索2203份NPC相关源文件、登记119份正确模板，见[原指令回放与启动收据](../../research/recovered/STONEAGE-STAGE-A-DOJO-ORIGINAL-ROUTE-BOUNDED-REPLAY-R1.json)。本轮验证的是其**原配置的静态先决条件**，不是新的一次来宾进程执行。

**仍未证实**：原 GMSV↔SAAC 实际建立TCP会话或完成认证、NPC真实创建/加载后的场景生成、原客户端登录、道场两条路线在完整游戏中的触发或终点写入。监听 `LISTEN` 不等于 `ESTABLISHED`；认证字段一致不等于已握手。原EXE在本轮所用单个libarchive解码路径有部分输出/CRC失败，不能把这些截断字节当已认证可运行原程序。此前独立7-Zip/UnRAR恢复的原EXE记录仍有效，不能由本轮单解码器失败推翻。

**具体最高 NEXT**：只复用此前合格、同包的原EXE/运行库与隔离来宾，从地图和模板加载完成点继续观察进程间TCP建立与NPC创建阶段。若没有可取的正确原程序或环境，精确保留运行缺件并转下一份实际有原件的可见内容，不扩无关工具、不把静态配置当运行通过。

本公开收据的 CI 只交叉验证元数据和已存原运行报告，**不含版权原配置或密钥、不重新解包私有RAR、不声称CI实际启动原服务端**。原社区混合2.5身份与 JSS1999、台湾1.0、大陆2001版1.82均严格分离。Stage A仍 **7 PARTIAL+2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，总体完成率未知。
