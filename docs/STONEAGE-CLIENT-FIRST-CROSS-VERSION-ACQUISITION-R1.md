# 《石器时代》官方客户端实物优先、跨版本去重工程 R1

2026-10-24。工程方法与现有样本审计；本轮未声称已下载全部官方版本。

## 一、已经取得与尚未取得的实物不能混同

| 版本样本 | 本仓库既有证据 | 边界 |
|---|---|---|
| 台湾 Waei/JSS 1.0 Redump 104630 | 已接受早期零售客户端，411 光盘文件/383 核心文件/373,564,663 核心字节，文件哈希完整 | 不是原商业服务器 NPC、宠物和任务全集 |
| 2.5 两分卷保留包 | 已取字节和 SHA-256，混合包内 stoneage2.5 子树 2,302 文件 | 混有服务端及辅助工具，**未被认证为纯净官方 2.5 客户端** |
| 韩国 Inium/Hananet 2000 正式/试玩 | 官方传播路径及正式 sa.exe、试玩 sa_demo.exe、CNET stoneage.zip 文件名/体积已有历史证据 | 具体原始安装包字节仍未找回 |
| 台湾/大陆后期 8.x 等 | 部分历史官方域名链接和社区载体 | 未核对原始安装包字节/文件哈希前只能作为候选 |

旧资源级真实比较：research/recovered/STONEAGE-TW10-VS-25-RESOURCE-DIFF-R1.txt。TW1.0 的 125,996 个 ADRN 记录和 464 个 SPR 组在 2.5 桥接资源的相应结构有精确对应；这不是物种、任务、NPC 或服务端规则相同的证明。

## 二、六层取证与去重顺序

1. **来源身份**：逐发行地区/运营商/版本/构建保存原下载路径、同时代证明、原包体积/哈希、修改风险与版权状况。链接≠下载成功。
2. **原始包**：只读隔离保存；严禁直接删除原始安装包、光盘影像、补丁或分卷；不运行来源不明 EXE。
3. **文件级精确去重**：对提取树逐文件流式 SHA-256，按(size, SHA-256)聚合重复字节，同时保留每版的路径、样本与来源。仅降低重复分析成本，不抹掉历史映射。
4. **资源记录级差异**：再使用既有 ADRN/REAL、SPR、SAB/SAP、地图/音频/协议专用解析器对记录进行精确增量比较。容器变更本身不等于新增宠物或地图。
5. **实体关系**：宠物身份/图像/动作/成长/技能/栖息地，地图/NPC/任务/对白/奖励/存档必须逐版本用同版 ID 与真实原始字段/行为连接，缺失保持 OPEN/null。
6. **任务独立分类**：BASE_GAME_QUEST、PERMANENT_VERSION_QUEST、OPERATOR_EVENT_QUEST、ORIGIN_UNRESOLVED。活动不得混作发行本体。

## 三、本轮实现

新增 tools/stoneage_cross_version_file_inventory.py：离线、只读，接受已解包目录与 ZIP 的真实原始字节；输出 SHA-256 清单、样本摘要、重复文件组和同路径变化。只写元数据，不复制专有内容、运行安装器或自动判真伪。拒绝非法 ZIP 路径、符号链接、大小写路径冲突与不合理超大成员；测试使用合成无版权字节。

输入示例（本机路径是格式示例，不代表当前执行环境已持有这些包）：

```json
{
  "schema": "stoneage.cross_version_input_r1",
  "samples": [
    {"sample_id":"TW10-REDUMP-104630", "local_path":"/archival/tw10/StoneAge", "kind":"directory", "source_class":"ACCEPTED_OFFICIAL_BASELINE", "region":"TW", "claimed_version":"1.0", "evidence_ref":"research/clients/STONEAGE-TW10-FOUNDATION-BASELINE-ACCEPTANCE-R1.md"},
    {"sample_id":"PRESERVED25-CLIENT-SUBTREE", "local_path":"/archival/25/stoneage2.5", "kind":"directory", "source_class":"MIXED_COMMUNITY_BRIDGE", "region":"UNKNOWN", "claimed_version":"2.5", "evidence_ref":"research/clients/STONEAGE-25-PRESERVED-BUNDLE-ASSESSMENT-R1.md"}
  ]
}
```

用法：python tools/stoneage_cross_version_file_inventory.py --input /path/to/specimens.json --output /path/to/report.json

RAR、7z、分卷、ISO 不会被假装当成 ZIP；应先由已有经核验的离线解析器/只读挂载流程取出文件树。脚本不会下载任何候选地址，亦不会自动证明版权授权或版本清洁性。绝对本机原始目录路径只保留在输入，不输出报告。

## 四、下一批优先队列

- P0：接入已经取到的台湾 1.0 与混合 2.5 原始字节，再跑一次真实 SHA-256 文件清单及专用记录级差异，保留与旧报告的差异。
- P1：韩国 2000 Inium/Hananet、JSS1999、日本与台湾早期官方原包。先用来源注册表中已确定的原始下载路径/存档载体，不重复死链盲搜。
- P2：大陆经典 1.82、2.0、2.5、3.0–8.5 以及其它日/韩/台官方分支的全包、补丁、资源增量。资料齐备才计算真实收集覆盖率。
- P3：从各版资源增量进入宠物、任务、NPC、地图、UI、历史世界线可检索实体目录；未获服务端字段继续查早期服务端及同期官方内容，不通过玩家回忆编值。

## 五、准确状态

本轮**建成可运行的文件级比对工具和测试，未新增下载任何官方商业客户端包**。当前执行容器没有已往会话缓存的原包；既有 TW1/2.5 真实差异只能引用仓库有 SHA 的先前报告。全版本收集/全部宠物/任务/原服务器仍未完成，不凭版本号数或测试数报完成百分比。原版权素材和商业程序不进公共 Git。
