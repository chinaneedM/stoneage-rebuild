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


## 2026-11-15 三组真实 Actions 完成记录与永久 SHA 收据（前向追加）

已真正执行 [GitHub Actions run 43694793122](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/43694793122) 的3个完整工作Job，全部 `completed/success`；其初始精确代码候选提交 `cd6c6034c43ee52026ae79ccf24fd2ab8d92886f`。注意这是**网络来源回读作业通过**而非124张全部成功下载，亦不是客户端运行。

| 原官网来源组 | 原网页位置 | 本次确有原归档 GIF 字节 | 本次网络未取得图片字节 |
| --- | ---: | ---: | ---: |
| 第1页，Job `132752851878` | 45 | 10 | 35 |
| 第2页，Job `132752852047` | 45 | 5 | 40 |
| 第3页，Job `132752851995` | 34 | 9 | 25 |
| **合计** | **124** | **24** | **100** |

100次未取得图像中，92次是Wayback返回可用候选但**原字节重放仍不可读取**，8次当次无法取得可读取档案或网络接口受阻。失败可能受限流、归档实际缺失或中间网络条件影响，本批**没有证明具体失败的唯一原因**，不能把这些图号标成不存在。

**必须去重的两批历史事实：** PET21已经实际有9个日本官网位置的归档GIF哈希（含PET16早先已核的第1张）。PET22当次24个成功回读，其中 **5 个同位置旧SHA再次完全一致**，另 **4 个PET21已成功但本次读图失败，仍要保留旧SHA**；因此PET22相对PET21新确认 **19 个不同位置**，两批合并共 **28 个不同官网位置具有真实已取原GIF字节的SHA证据**。其余 **96 个位置尚无可验证原图片字节**。这是官网网页位置的哈希覆盖，不是28种已确认原游戏宠物。

上述全部124处官网原序号、确切原HTML网页与图片URL、原页面SHA及捕获时间、当次网络结果、真实图像SHA/大小/60×65 GIF、独立重复与历史失败保留在：
[PET22 124个位置完整机器来源账](../../research/recovered/STONEAGE-PET-MODULE-22-JP-124-ARCHIVED-IMAGE-RECOVERY-R1.json)。

**原始图片归档时间不得与网页同年混淆。** 本次多处同样有2008年的GIF捕获时间，而原HTML网页是2003/2004。独立同SHA可证明两次观测到相同文件哈希，仍不证明2003原页面同时使用该后续捕获、初代宠物图号或历史同部署。原图在Runner内存暂存后丢弃，**本批新增私人源GIF永久保存数量0、公开Git发布GIF数量0**；如以后要供个人离线图鉴查看，必须在外部合法私有路径使用收据内真实Archive URL再次下载并核SHA，不得发布商美术或声称已具授权。

现通过同一宠物统一查询入口：
```bash
python tools/stoneage_pet16_lookup.py --operator-web jp --web-ordinal 4
python tools/stoneage_pet16_lookup.py --operator-web jp --web-ordinal 44
python tools/stoneage_pet16_lookup.py --operator-web jp --web-ordinal 100
python tools/stoneage_pet16_lookup.py --operator-web cn --web-ordinal 1
```

- 第4位置由PET22首次取得图像SHA；
- 第44位置PET21已有图像SHA，本次网络失败但**不丢旧证**；
- 第100位置尚无新旧真实图像SHA；
- 华义第1位置仍只有2001原网页图片引用和未识别原名，不会被日本来源代替。

**不变状态**：PET `SOURCE_BOUNDED_PARTIAL`；原官方完整物种主档、晚期与台湾1.0同服身份、技能/成长真实效果、完整TW85像素和私人商业图片版权仍OPEN；Stage A 7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall_percent=null。最高PET23：先审查网络失败是否存在可复用的有界、低频、合法二次读取资格，再落实已认证来源SHA图片的**私有保管与再次核验**；不应直接将100项网络失败解释为长期历史材料不存在，更不转到NPC模块。
