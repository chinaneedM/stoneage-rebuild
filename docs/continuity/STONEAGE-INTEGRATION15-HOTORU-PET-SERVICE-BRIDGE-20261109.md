# INTEGRATION15-R1｜霍特爾寵物店 1303 兩項服務與原參數的現場關聯

2026-11-09 從主線 `9ca6cf09962538f115d05cb0389e0ecd468e2a40`、tree `53ad7612ec5e5b3c40c9df8e28d52261abacd6b9` 起步。依連續性協議讀過最新原證登記、11 條配置的 INTEGRATION13、21 家技能商店 GAMEPLAY03 和 16 家寄放服務 GAMEPLAY05。三份上游公開 JSON 均保留原區分；本輪只把**同一份保存 RAR** 的原 CREATE 配置與已驗原參數建立同場地可查關係，不假稱再次取回原 RAR 或重新解碼圖像。

## 一、同一個 1303 房間中的兩條原服務配置

- **收寵／寄放來源配置**（PetShop）：原 `genout/shop_m.create#53`、座標 **(16,13)**、數字圖號 **16048**，原塊 SHA `478b8668a020ba8b0a76e50e4893b6e33d5e6712a0f6bf4658e02a9929498d57` 精確對上 GAMEPLAY05；源參數 `genout/ps_1303_16_13` SHA `8beaa8a89b834d90be34e9213abf40d5bdb9ff832a6b6c5bb674db738577f022`。源 `nomal_rate=1.0`（原拼寫保留），`special_rate=1.5`，`pool_flg` 和 `pool_cost` 字段缺失，`special_pet` 字段存在但原值為空。缺字段不是数值零。
- **宠物技能课程来源配置**（PetSkillShop）：原 `genout/shop_m.create#54`、座標 **(13,13)**、图号 **16049**，创建块 SHA `f799a403d749cae89ad3e3a5a1983818d764e2ff48517acff62fe737440ab1ca` 精确对上 GAMEPLAY03。外参 `genout/psks_1303_13_13` SHA `310106449c8b0ee0e4e5f0a474dfcf47f126d413d57a047207bfe80a8d14f3db`，`skill_rate` 字面 **1.1**，课程数字按原顺序 **0、1、2、3、50、61、130**。这七个编号在两份*候选*技能表均有独立原行；既未选定实服有效表，也未证明实际收费、学会技能。

两条服务在 INTEGRATION13 同一张已验 30×30 原 DAT（SHA `d6f85cccec0eec22eaccfbef84eafcfaecea97995bbb6af3062ab84625221ec4`）和 LS2MAP 下，有同源 CREATE 记录和独立源参数；私有 MAP07 1303 候选底图 PNG SHA `f69fffd8171a729e10d7a2f7ad1414e993d74f82d414f502506d4de313d1c209`。这是**新增跨模块现场索引**，不是新增原地图绘制。

## 二、同图号不合并为同一角色

同室 `shop_m.create#61` 的 TownPeople 位于 **(11,6)**，使用数字图号 **16049**，与技能导师共用图号，但原创建块、参数路径和座标不同。按原配置应保留两条实体；一个图号不能证明同一 NPC、同一句对白或同一交互。另有 **六条 npcgen_mugon 配置**及 **两条到 1300 的 Warp 原配置**；本轮不替六条配置猜测人物身份或语义。

## 三、验收范围与后续止点

[派生可查索引](../../research/recovered/STONEAGE-INTEGRATION15-HOTORU-PET-SERVICE-BRIDGE-R1.json)仅引用三份既有上游报告的原块 SHA、原参数 SHA、位置和源字面，`tests/test_stoneage_integration_module_15.py` 独立重算全部重要 join 和负边界。公开测试不加载私人原商业字节。

本轮**原件重新读取 0、新原 RD 解码 0、私人 HTML 修改 0、原图浏览器验收 0**。尚未从已有私人 INTEGRATION13 观察包中重新取得并验明 16048/16049 图像的来源像素，不得写成新图已展示。日本1999／台湾1.0官方同服、混合2.5原生载入、技能学习、寄存交易与客户端 UI 全部未证。本记录为 **INTEGRATION15-R1 的 SOURCE JOIN PARTIAL**，不表示整个 INTEGRATION15 已闭合。

**NEXT INTEGRATION15-R2**：只在取得来源合格的私人 INTEGRATION13 观察包及图像候选实物后，将这两条原参数接到 1303 实际可查离线观察页并做独立浏览器/像素核验；不能取得则止于现有可审计关系，转向已有原材料的其它内容。Stage A 仍 7 PARTIAL + 2 OPEN，Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING，整体完成百分比未知。旧 `docs/CURRENT-STATE.md` 2709173 字节的完整历史保留原 blob `c89e0e33537990aa2132b47c40fef49a985a935c`。
