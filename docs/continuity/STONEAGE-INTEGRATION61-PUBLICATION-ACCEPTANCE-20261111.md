# INTEGRATION61｜两地主厨原菜单—三物品—台湾1.0原RD：正式发布与实物保管验收（2026-11-11）

## 远端事实源与内容验收

本单元按`docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`从真实GitHub主线 `4090ac47f4ce807d0ab0ed3740a3859f204bb585` / tree `ba07222d9cfe5c8ec10c1b2913dde62a40e8df11` 启动，重新读取分支/HEAD/tree/最新提交/Actions、协议、原始`docs/CURRENT-STATE.md` Git blob、README/路线/设计/来源/历史与INTEGRATION60验收。根据INTEGRATION60 NEXT查重原物品、宠物技能、料理/任务，选用之前O75已有同名来源但尚未固定三幅台湾1.0实际保存原RD图像关联的料理内容；**三物品同名此前已记录，并非本批新发现**。

- [源限定日期说明](STONEAGE-INTEGRATION61-CHEF-DISH-PIXEL-SOURCE-20261111.md)与[纯数字/散列可复核索引](../../research/recovered/STONEAGE-INTEGRATION61-TWO-CHEFS-THREE-DISHES-TW1-PIXEL-SOURCE-R1.json)保留双主厨原CREATE位置和原菜单两份来源的准确身份。
- 楼层2009主厨(25,41)的三条菜单原名与原物品表**不完全同名**，继续ID未知；不伪造同名、同作品或实际菜单成功调用。
- 楼层3009主厨(25,43)原菜单已有三个严格同名物品ID **12607、12780、12754**；原itemset双表对应三行整SHA相同、类型/回调和素材原值不变；实际台湾1.0原图别名 **24484/24443/24531** 与原ADRN物理位图序号 **6651/6610/6698** 明确区分。三图分别28×42、44×35、32×34，实际已保存原PNG SHA、RGBA SHA均重读一致。

## 原始私人素材真实资格及耐久保管

从已保存原来源分析资料`StoneAge-ITEM01-private-two-itemsets-832-original-RD-icon-observer.zip`重新取回 **5,868,386B / SHA256 `cb88d0a837686edae507910bdc11fcf6abb35df9aa43819fd80c741c51b755aa`**；实际**838/838 ZIP成员CRC**通过，三条物品原两表94栏记录和三张原台湾1.0来源PNG逐SHA/尺寸/RGBA核对全同。实际新增原RD二进制解码0、原社区361MB RAR本批没有重新打开、原主厨菜单原文文件没有重新提取，全部边界明列在报告。

本批另外制作仅含三个保留原PNG、简易离线私人观察页及私人来源收据的`StoneAge-INTEGRATION61-original-three-chef-dishes-private.zip`：**13,335B / SHA256 `52454d22d8dc681bbce8f40873228b397b1764328c285826473480bcdb41a0fd` / 5成员CRC全部通过**。已上传个人Library `/石器时代/`，再从独立新副本实际下载，**整包字节逐字节相同、完整SHA与全部成员CRC再核通过**。本包和原文字/商业PNG不进入Git；公开CI只使用不含版权原图/原对白的派生索引。

## Pull Request／Actions的实际结果

| 阶段 | 真实后验 |
|---|---|
| 候选分支 | `agent/stoneage-integration61-chef-dish-pixels-20261111` |
| 候选 HEAD | `2d8826c3adf62e091e441ea2a6df300292d05fb8` |
| 候选 tree | `89d5f08c4c9610539bd46f5b03f0470558fef056` |
| PR | [#329](https://github.com/chinaneedM/stoneage-rebuild/pull/329) 在固定候选HEAD、主线基准、mergeable=true、Actions全成功后squash合并 |
| 候选 Actions | **46/46 completed/success**，其中push27+PR19；[专项push run42962948820](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42962948820) 与 [专项PR run42962996978](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42962996978)真实success |
| 内容主线 HEAD | **`e9beadbc922c67b3a137812a9dbbbdd89192080e`** |
| 内容主线 tree | **`89d5f08c4c9610539bd46f5b03f0470558fef056`**（与候选tree完全同一） |
| 内容main Actions | **27/27 completed/success**；[INTEGRATION61专项 run42963118752](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42963118752)成功，5项专项测试通过 |
| 历史CURRENT保管 | 原Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，2,709,173B，原样保留未修改 |

本页仅在内容main的27项实际验收后发布，**验收收据自身最新HEAD是否新增Actions必须另核，不在此预称成功**。CI并不包含版权原图片，不能代替私人来源实物读取。

## FACT / OPEN / 本批最高NEXT

原晚期社区mixed25保存的NPC/菜谱/原物品，和台湾1.0零售原图的同数字跨版本联系，只能证明候选来源链，**不是**官方JSS1999/TW1/CN1.82同一部署、早期主厨真实出场、宠物料理成功率、菜单交易、原客户端运行、原生选图与配色，也没有真正恢复可操作原游戏世界；三条不完全同名菜谱仍UNKNOWN。

Stage A **7 PARTIAL+2 OPEN**、Stage B/wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、overall_percent=null均不变；不进入账号/网络/服务端运营或未来新引擎。

**最高NEXT：** 三道已知同名料理的原物品图像源桥已有限闭合。下一步优先检查**其它**具有实物、尚未加入来源链的宠物技能、任务道具、宠物服务或不同原场景互动；先查重、限定一个有实源的内容增量，缺件则精准标OPEN并轮换，不重复餐饮配方模拟，也不重复当前三图。
