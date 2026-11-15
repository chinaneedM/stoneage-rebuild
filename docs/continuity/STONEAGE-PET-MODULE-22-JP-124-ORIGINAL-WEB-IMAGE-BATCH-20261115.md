# PET22｜日本 Hangame 原官方宠物网页124处图片批量来源回读

**模块锁：PET唯一 ACTIVE，仍 SOURCE_BOUNDED_PARTIAL。** 本批延续 PET21 真实 23 网址网络试验（日本 9 张真实已读GIF/8个新增SHA），不修改旧图片字节/源文本、也不把某个网页序号当做原服宠物ID。

## 复用真实原网页与确切图片URL

输入仍为 GitHub 已固定的 PET16 来源分离目录 blob `fdb7d9aade2df62d1a1e06b2d2f9e383693ed980`。其中日本 Hangame 官方旧网页三份不同存档：

| 早期运营网页位置 | 原页面已存档日期 | PET22 只读原页面真实图片URL |
| --- | --- | --- |
| `chara2.asp` | 2003-12-14 | `petpicgroup1-1.gif` 至 `petpicgroup1-45.gif`，**45项** |
| `chara2-2.asp` | 2003-12-14 | `petpicgroup2-1.gif` 至 `petpicgroup2-45.gif`，**45项** |
| `chara2-3.asp` | 2004-02-20 | `petpicgroup3-1.gif` 至 `petpicgroup3-34.gif`，**34项** |

这三批共124条历史网页位置，不是“124种经认证的初代游戏宠物”。上述文件名序列只是作为**原来源完整性自测**的观察，不当作猜图URL生成器；真正每次HTTP请求的URL必须由已固定PET16原字段提供，若原网址不匹配则拒绝。

PET21较早取得的9个日本GIF与SHA仍保留其**原归档图片捕获时间**：可能早于也可能晚于本网页HTML快照。新一轮同位置图片SHA若不同，不自动覆盖旧事实，而是保留为另一版图片／待考异文；仅同SHA两次独立验证才可称重复回读。

## 实际网络验证方式

`tools/stoneage_pet22_jp_official_124_archive_batch.py` 通过 PET21 已经测试的 allowlist 和档案回放工具，切三组使用 GitHub Actions 的独立原Runner，最多三个组并行、每组不超过三个同时请求，每个请求的限时6秒、最大读取256KB。原商业 GIF **只在原Python进程内存中**用于 SHA256、图片格式与尺寸鉴别；绝不上传Actions图片Artifact、复制原图像正文或以源码方法嵌入Git。当前公共仓库只保留版权安全的URL/时间/字节数/哈希和判定状态。

实际完成的判断只认**精确候选提交**的真正Actions日志。若某组因原Internet Archive访问受限、限流、归档不完整而失败，保留URL及失败状态，不能宣称原图永远不存在。若真实取得原图压缩字节，同样不代表取得同版游戏客户端图号／种属身份、不代表原客户端渲染效果、不代表拥有公开攻略站或新游戏使用原画许可。

已有来源文件：
- PET21（初始真实SHA收据）：`research/recovered/STONEAGE-PET-MODULE-21-OFFICIAL-WEB-ARCHIVED-IMAGE-REACCESS-R1.json`
- PET20七维验收矩阵：`research/recovered/STONEAGE-PET-MODULE-20-FIELD-COVERAGE-AND-SOURCE-STOP-MATRIX-R1.json`
- 旧日本官网原网页来源：`research/recovered/STONEAGE-JP-OFFICIAL-PET-CATALOG-R1.json`

## 当前验收和后续

本文件在启动时不提前宣称124个URL均可取得图像，不填写无原字节的新SHA。正式批量检索证据将在Actions三组原日志完成后**前向追加**到 `research/recovered/STONEAGE-PET-MODULE-22-JP-124-ARCHIVED-IMAGE-RECOVERY-R1.json`。动态网络结果不能用命令行源代码或单元测试预期值取代。

实际成果若已具备明确历史归档原图片URL/SHA，但**尚未持久保存在私人资源库**，仍严格标记“字节即时已读、私存未核”。下一步骤仅允许PET继续检索其它已登记原图并设计安全私人校SHA保管；相关台版/大陆初版官方服身份、原技能效果、原版2D动画时序、商业原画未来许可等依PET20仍OPEN。

历史 `docs/CURRENT-STATE.md` 原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c` 不改；Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、总体百分比 UNKNOWN。宠物模块未结项，不解锁NPC或其他模块。
