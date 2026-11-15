# PET21｜日本 Hangame／中国华义历史官方宠物图鉴原图来源受限回读

**阶段：Stage A / 唯一活动内容模块 PET。** 本批不是新游戏设计，也不是复原所有历史物种，不直接发行原商业美术。

## 起点与明确对象

继 PET20 七维验收矩阵、PET16 唯一统一目录，本批仅追踪此前**实际存档的官方网页原图 URL**，不凭临近号码猜出新图或产生页面不存在的链接。

- **JP Hangame**：2003-12-14 的 `chara2.asp` / `chara2-2.asp`，及 2004-02-20 的 `chara2-3.asp`。目录共 **124 个不同网页位置**；原图仅已有 **1 张**来自后来 2006-06-04 的历史单图保存，SHA `593345c3edf78ebcaa2dff0c27a2d10a92b4eefcc4aef4db14aee2efdc5e013f`，只绑定官方网页名称「ウーリ」与所引用的图URL，不能证明 2003-12-14 同时取得这张图片，更非台湾1.0客户端原像素身份。
- **中国华义**：2001-10-23、2001-12-04 官方网页 `new_pet.asp/new_pet1.asp/new_pet2.asp` 的 **104 个网页位置**，其中 **98 个具名、6 个占位尚未读出姓名**；统一目录当前没有独立原图片SHA。网页标注是大陆2.0专区历史资料，不可回填大陆1.82或台湾1.0客户端主表。
- 两来源原 HTML 页面此前已经有逐页 SHA，图片 URL 必须保持其原HTML真实字符串（包括 CN 的编号不按位置自增、大小写混合 `.JPG/.jpg`）。网页序号不是原服务端模板 ID、SPR 号码或完整历史物种种数。

固定来源：PET16 `research/recovered/STONEAGE-PET-MODULE-16-SOURCE-SEPARATED-UNIFIED-CATALOG-R1.json`（Git blob `fdb7d9aade2df62d1a1e06b2d2f9e383693ed980`）；旧日本源 `STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json`（`85e99d6fd6a7ca27eeaa3987510a6bcc1d701708`）；旧中国源 `STONEAGE-WAEI-CN20-NEW-PET-FINITE-CATALOG-R1.json`（`f950aa33af0b3ec8693b2867758faf006aee546b`）。

## 实际网络试验界限

本批新增 `tools/stoneage_pet21_official_web_image_reaccess.py` 使用 PINNED PET16目录，不另复制宠物名字或原图：

- 不扫描未知网址；只对白名单原图目录中的 **23 个已存档位置**进行有界查询：日本 11 个位置、华义 12 个位置，包含全部六份页面存档的代表位、第一条既有原图 SHA 正例和华义未知姓名负例。
- 对每个 URL 先从原网页捕获时间尝试 Internet Archive 的原始字节重放，若失败则查找归档可用性，再对明确的归档捕获尝试读取。每个网络请求 6 秒上限，同时不多于 6 个工人，不超过每图 3 次请求，不猜造新路径。
- 安全约束：远端仅可访问 `web.archive.org` / `archive.org`，原图仅允许上述两家原源 host 和指定路径结构，拒绝其他 URL / 重定向。原始商业图像**只在一次进程内存中**用于计算SHA、图片类型、尺寸；GitHub Actions 不上传、不提交、不生成图片产物。
- **三层结论严格分开**：`ARCHIVED_IMAGE_BYTES_SHA256_OBSERVED` 需要收到历史归档二进制、识别图片 magic、记录图像捕获时间；`NON_IMAGE_RESPONSE` 或 HTTP/超时只是当次查询失败，**不等于图片在全部历史归档均不存在**。即使真读回图片，也不证明它与目录 HTML 同一秒存档，更不证明原服宠物种属、原游戏效果、使用权或可公开引用原商业图。

离线独立测试 `tests/test_stoneage_pet21_official_web_image_reaccess.py` 覆盖：目录 Git blob、23 个已登记的源图 URL、六网页分层、已证单张原 SHA、CN 原图序号/网页序号不相等、未知名字、URL 污染负例、Wayback 非图像/失效档案拒绝、**网络请求失败不冒作缺图**。

### 实际结果

仅当对应PR精确候选提交的 Actions 包含网络回读原日志，才把**真实取得**的图像捕获SHA等写到独立 PET21 收据。代码和 CI 工作流定义本身**不是已经恢复图片**。如网络或 Wayback 无法访问，应写出样本范围、失败 HTTP 状态及可复核日志，不虚报任何像素、图片增量、全部228目录已检验。

## 下一步与不变状态

优先用一次实际 Actions 结果决定该批是否有可追溯原图。如果没有，立即用更适合的合法来源/已有归档，或记录具体不可达止点后在**宠物模块内部**回到 PET20 剩余原RD原像素资格检查；不转 NPC、地图或道具专项、不重复设计玩法。

旧 `docs/CURRENT-STATE.md` 原blob `c89e0e33537990aa2132b47c40fef49a985a935c` 原样保存；Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，总体百分比 **UNKNOWN**。PET当前仍 `SOURCE_BOUNDED_PARTIAL`，没有宠物整体结项、没有版权授权。
