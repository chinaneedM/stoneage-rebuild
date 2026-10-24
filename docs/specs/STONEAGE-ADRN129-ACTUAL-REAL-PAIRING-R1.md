# 官方 ADRN129 修复索引与实际 TW8.5 REAL 配对 R1

日期：2026-10-25。任务：TW-WAYI-ADRN129-REAL-COMPANION-QUALIFICATION-06。

本包恢复的是官方修复索引在一个**实际已取得的像素容器**中的地址、长度、RD 头与块哈希对应关系。不是按 `129` / `158` 文件名猜版本。官方列表 2005-05-18 的 7.5 黑屏修复说明、2006-09-11 实取补丁，以及后存 TW8.5 客户端载体仍分别标注；不能据此认证 2005 同 build 或纯净官方 TW8.5 压盘。

## 实物与来源

沿既有六卷载体原 SHA 规则，source run [40140366886](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/40140366886) / job121010641458 一次实取 1,145,465,184B 包，静态 MSI 解包，逐 SHA 验证两原件与旧 557 文件清单一致。未执行原程序。官方补丁使用上一包已全记录重放通过的 metadata，不重复下载 RAR。

| 实际容器 | 字节数 | SHA256 |
|---|---:|---|
| adrn_158.bin | 33,297,600 | `16ba4fa3825b2c4b6645bab8b4fe3152a262a4789c8bb89e3043a7d3f0d53681` |
| real_158.bin | 1,607,321,502 | `e0f9c0d20fd3d9daae0701d8a872c9842e27d3da1be4d449d558c9c76d1c5f5b` |

完整 source 元数据保存在 `research/recovered/adrn129-tw85-real-pair/`，三个原始派生成员永久保留；原安装器、容器和像素不入公开 Git 或 Actions 工件。原字节没有因此获得私人长存，后续不能冒称完整客户合集已保存。

## 逐出现配对结果（FACT）

| 范围 | 物理记录 | 不同 bitmap 号 | 重号后续出现 |
|---|---:|---:|---:|
| 原 TW8.5 索引 | 416,220 | 416,192 | 28 |
| 官方补丁索引 | 389,698 | 389,670 | 28 |

全部 389,698 条补丁的 `(bitmapno, 原80B记录SHA)` 在原 TW8.5 索引中恰好各有一个精确匹配。七个头字段与属性 SHA 也逐项相同；每条原 offset/size 的实际 REAL 读区间、RD magic、头尺寸及全块 SHA 均已导出。原 TW8.5 还有 26,522 条物理记录不在补丁中。保留全部位置和候选，不套 last-wins，不按重复号去掉不同记录。

与 CN5 原派生 RD 块哈希比较：303,020 次物理出现块字节相同、177 次块字节不同、113,023 次编号在该基线未见。这不是宠物/NPC/地图个数，也不是新增内容或恢复百分比。CN5 基线按号查询不替代本包按完整记录键保留重复出现。

## 首版长度判定的有日期修正

首版 source 将 RD 头 offset12 的长度字段必须等于 ADRN size 纳入严格 `HEADER_MATCH`。结果为 native416189匹配/31不匹配、patch389671匹配/27不匹配；这些原始表、report 和严格计数**均保持原样**。

复核31条全部是 flag0，RD/ADRN 宽高相同，实际 ADRN size 恰好为 `16+width*height`；冗余 RD 长度字段都多 8,621,844。这是观察到的共同差，不对其历史成因编造解释。仓库既有 `tools/stoneage_rd_codec.py::decode_rd_block` 使用 ADRN authoritative block size 切 payload，flag0 按宽高取原始像素，并不以头部冗余长度决定区间。因此首版谓词不足以把这些记录认作损坏或不可配对。

新增独立、有日期的 `STONEAGE-ADRN129-REAL-ACCEPTANCE-R1.json`：保留全部31条 native及27条 patch位置、头字段和全块哈希；对已经 source 证实 magic/有界读/块哈希、宽高匹配、flag0且精确原始 payload 大小的记录增加 `RAW_FLAG0_ADRN_SIZE_AUTHORITATIVE` 资格。其余 HEADER_MATCH 仍只称头结构匹配。最终结构资格 native416220、patch389698。不修改头、不重新下载大包。

这不是所有压缩块已逐像素解码或画面运行验证；少数特殊尺寸也原样保留，不凭结构资格宣称可显示。具名物种/NPC/任务、像素语义、同2005构建、官方完整合集与原服主表仍 OPEN。

## 可重放验收及保管

source HEAD92a739bfc12e1d19f0513e3c1fe138111d774f0d 成功后，bot派生提交d82113d7a9dcd53d43f2f4c3d9113d542c746f44 / tree37246c14dd35dddc69c6487e19641758d727c893。artifact12578736519 ZIP76,621,759B，完整独立下载重哈希 `8839d4bd38e5af92e46d732924fecaa8403272b5be51c23290ee6956764ddf14` 与 API digest 同一，恰三个成员逐字节等于 Git。派生 gz 共77,368,422B（native43,825,625 + pairs33,542,797），不包含原像素。

`tools/stoneage_adrn129_real_archive.py` 独立遍历全部 native 与 patch行，重算所有 source汇总、候选列表、物理顺序、重复号守恒、原头/属性对应、CN5哈希关系及修正资格，与保存overlay完全一致。原REAL实际块哈希来自source作业，本地离线重放不冒称第二次独立读取原REAL。12项相邻单元通过，包括13类合同变异与6种错误原始块例；重复号合成例保持所有匹配候选。归档及main只运行离线验收。

完整 pins、8个fresh启动文件、4历史文件原前缀、source/job/ZIP/hash保管链在 `STONEAGE-ADRN129-REAL-CUSTODY-R1.json`。候选/main自身Actions在发布后实际后验记录，不预支成功。

## 有限下一包

这两包已完成修复索引实物及实际REAL配对，不继续扩展头字段 helper。下一任务 **CLIENT-ORIGINAL-ARTIFACT-PRIVATE-CUSTODY-07**：先查可用的私人持久存储能力、单件/总容量和回读校验路径，将原客户实际包/分卷按原SHA及位置无损保存的可行性变成可验证结果。只在容量及回读链成立、确有原件保管交付时再实取一次必要载体；已验元数据优先复用，不能为复算哈希反复下大包。若能力不足，有限登记精确限制并回22域具名资源/客户端原件队列；不公开商用资产、不宣称持久保管已完成。Stage A7 PARTIAL+2 OPEN、B/wiki GATED、R79暂停、任务四档及总percent=null均不变。
