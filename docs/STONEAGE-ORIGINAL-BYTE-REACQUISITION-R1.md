# 官方客户端原始字节重新取得：R1 有界验收

日期：2026-10-24。当前优先级 `CLIENT-ARTIFACT-ACQUISITION-AND-CROSS-VERSION-DEDUP-01`。本文件及新工作流是对旧两个*已存在的来源*进行真实字节再次取得和逐项校验，而不是声称另行获得新官方版本。 **新工作流通过前，结果为 PENDING，不能把历史哈希连接视为本轮重新取得成功。**

## 两个实物与等级

- 台湾 Waei/JSS 1.0：既验 Redump 104630，Internet Archive `stoneage_tw_2000_win/CD_DIC.rar`，842125501 B，MD5 `b37a4a47f4eb608cac67e4ddf7a1621a`，SHA1 `b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded`，其中 `STONEAGE.bin` 523449360 B。发行光盘内容是来源已认证的早期客户端，不是完整商业服务器。
- 保存的 2.5 桥接包：MediaFire 双分卷源 `ev7l29fw77891go` / `ytaa168o5jih0lx`，完整合并包 SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`。社区打包中带服务端、辅助脚本及改动的运行文件，客户端子树只能记为 `MIXED_COMMUNITY_BRIDGE`，**不是干净官方 2.5 发行版**。

## 审核过程

新工作流 `.github/workflows/reacquire-stoneage-cross-version-original-bytes.yml` 用现成、受历史鉴定的两个下载流程取回临时源包，校验原压缩包摘要和分卷摘要，隔离解档而不执行 EXE，再由现有 `stoneage_tw10_client_inventory` 对光盘读取 ISO 文件 extent，逐文件重算 SHA256；对 2.5 客户端子树 2302 个文件逐一独立重哈希，与两个不可变原清单 Git blobs 校对。任何丢失、新增、内容漂移、重名冲突、软链接或总量不符应失败。

期望交集：台湾核心383，桥接子树2302，台湾核心文件完全相同235、未匹配148、桥接路径命中237、完全相同 TW 文件累计3882018字节。严格不从文件同哈希推导物种、宠物成长、地图 NPC 或运营服务器任务 ID，也不把不同的 REAL/ADRN/SPR 容器误报成内部绝无共享素材。

本流程从不把原图、客户端、商业代码或游戏素材写入 Git；Actions 工件只上传派生 JSON，30日有效。**永久发布取证收据**必须另外核验实际 run/job、原包摘要、源文件个数、派生 ZIP/raw SHA、真实日志和入库 Git blob，然后保留历史完整状态前缀，按远端 lease 非强制快进回 main。若下载 404/500/超时，只登记一次新的传输失败及重开条件，不冒充原包取得。

下一批有效实物来源仍优先 JSS1999/韩2000、台湾/大陆早期正式客户端和地图/更新补丁；精确下载路径与作者/版权/修改风险独立列明。运营活动任务继续与本体及正式版本永久新增任务分档。