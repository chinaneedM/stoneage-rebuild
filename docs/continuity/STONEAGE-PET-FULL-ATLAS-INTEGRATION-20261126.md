# PET 全量档案与离线图鉴接续（候选，2026-11-26）

基线 main 27e65d1e80eca9c1e3044c761d7eb852dc37404f / tree 78a4574604ca3b0fd0e80a618dffb01bc7c255bf，历史 CURRENT c89e0e33537990aa2132b47c40fef49a985a935c / 2709173B 原样保留。并发主线已验收[完整恢复门槛](STONEAGE-PET-ACTUAL-RESTORATION-GATE-20261126.md)，保留其协议§29与机器治理不重复修改。用户拒绝将有界查询交付视为整体模块完成，PET继续唯一活动。

本候选仅执行主线新§29的资料整合。复用已有98源统一查询构造主查询全部5924来源位置（预期值，待候选CI实际复验）的离线HTML，支持按来源/名称/编号检索、分页、查看来源字段与关系；明确展示标称7.5条件初值和成长、配置技能及保存取得路径，并读取现有124个早期结构化档案。以PET-000001烏力为可检查模板，原名、图号、56动作序列及原字段未知值逐项展示，绝不填充为后期数值。无需网络或外部依赖，不重新制造索引数据库。命令：

```sh
python tools/stoneage_pet_offline_atlas.py --output pet-source-atlas-r1.html
```

该页只涵盖现有主查询，不含另五个独立查询目录的整合，不含实际原图或原始动画播放，未达到完整图鉴。正式字段不因展示升级；缺原服同部署主档，不能将条件范围认作官服数据。源位置、字面与物种数不等价。历史整体完成UNKNOWN，Stage A 7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停。

NEXT：先验证候选精确CI、实际HTML和浏览器搜索/筛选/分页，再复用既有私人原像素资料，实现按来源位置对照真实头像与动作；整合其他五查询目录并建立逐宠字段专门展示和逐项缺件验收。优先丰富高版本PC资料，再作向下兼容；不切NPC，不进行新游戏设计。不得把本候选的HTML输出计为新增正式宠物或完整模块。

候选 `7cab473f9e543006a536bda2546f99fe242e70dd` 已实证7/7 Actions成功，专项 [run 45850912072](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45850912072) 生成 HTML，artifact15132418569 / ZIP956939B / API digest sha256:adf5d77c861017fcce4127eb93e9b0f23abf2aa5081a8dc56ba236a9f3c8acae（未独立下载）。本修订追加124档原证Git blob校验和实际 file:// Chromium 自动化测试；仍须精确新候选 Actions。私人原图材料仅检索到旧124图概览与重建脚本，未在本轮读取并验证原图资产，不宣称完成。

2026-11-26 后续：候选15b8bc037dfe9ae1f3ec172d1c996122d19b3643 的专项 run45851123719/job140017440469 在档案原证散列断言失败，浏览器步骤未运行。实查候选树与历史PET31索引124项，120完全一致、4项PET-000116至119已由PET32/33合法追加高版本头像候选。逐一读取旧/新8个Git blob做递归字段差异，仅新增appearance.cross_version_original_portrait_rd_candidates及provenance.sources后追加一条来源；其余字段完全不变。保留原PET31不可变，明确四组旧→新散列，严格验证每组两候选及TW1原头像仍缺，其他120项保持严格散列核验。待新候选CI及浏览器实测，不改正式字段。
