# INTEGRATION15-R2｜霍特爾宠物店 1303 原造型与已验服务源配置可查观察

**2026-11-09**。从最新主线 `b5079bff54fcaf90b77a3210d3e2793317008685` / Git tree `bf49ad1c0c74923b97792bc8daaf85c9d93a2f19`、11/11 主线 Actions completed/success 重新启动。按连续性协议取回旧 `docs/CURRENT-STATE.md` 的原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，完整历史 2,709,173 B 不改。本轮承接 R1 已核的两条服务 CREATE/参数和 WORLD11 原静态资源，不重复恢复已解码的同一原 RD。

## 真实取回与来源界限

- 私人 INTEGRATION13 五房间包 **2,867,302 B / SHA256 `c4cb208810a8ae0ad1ad76f59f3569f2f19b8bfd0389fe71aa6d3ffa91ff44eb`** 实际取回，34 条 ZIP CRC 全过；1303 原 DAT `d6f85cccec0eec22eaccfbef84eafcfaecea97995bbb6af3062ab84625221ec4`、原参数成员和旧完整基底场景 PNG `f69fffd8171a729e10d7a2f7ad1414e993d74f82d414f502506d4de313d1c209` 按先前 SHA 逐个重验。
- 私人 WORLD11 观察包 **10,711,617 B / SHA256 `ef7f658864bcfbbbf7948c110a0a040a075e8127d78a1fba8ecc2a6079619e00`** 实际取回，34 条 ZIP CRC 全过。混合2.5社区保存 RAR 的图号 16048 / 16049 在 WORLD11 已验完整 ADRN、RD 记录、两实现解码与 PNG。本轮真正取出两张私有 PNG，逐个验证 PNG SHA、尺寸、RGBA SHA 与公开 WORLD11；新增**原始 RD 重新解码为 0**。这是同保存载体资源编号/源图的限定证据，不认证早期官方运营部署。
- **16048**（36×79，原 ADRN 位移 -18,-70）对应 1303 (16,13) 的 PetShop；**16049**（32×79，位移 -15,-70）对应 (13,13) 的 PetSkillShop，并在独立 (11,6) TownPeople CREATE 再次引用。共两份原静态 PNG、三个现代叠图实例。图像坐标为现代观察器原点投影 + 原 ADRN 记录位移，非原生客户端层次/位置验收。

## 直接可用的私人离线交付

沿用 INTEGRATION13 的五房间静态页面和五张 PNG，**只改 1303 的候选叠图与来源详情**，保留其它 34 项中 33 项全字节。加一个默认关闭的来源叠图开关、图号 16048/16049 两源文件、三个互不合并的原配置可点标记、原 CP950 参数可展开的资料卡。原 `nomal_rate`、`skill_rate` 与技能数值来自原私人脚本，正文只在私人 ZIP，不发布到公开 Git。村民 (11,6) 的标记在现代候选底图主体外，原坐标保留且不擅改成室内站位。

私人包 `StoneAge-INTEGRATION15-R2-hotoru-pet-services-private.zip` **2,878,571 B / SHA256 `5e7e127f87e41c58f3ef193ecf0286899dce74112b00b3f164fd3e2280bdb36a`**，37 个成员、全部 CRC 通过；已存至个人 Library `/石器时代/`，**实际二次取回**并核同整 ZIP SHA、37 成员 CRC。原商业源/PNG、原 CP950 参数及页面只存私人库，Git 只收本案的数值/指纹和验证程序。

## 浏览器事实与运行未证边界

Chromium **144.0.7559.96** 的 Playwright 实际加载带原封不动图像字节的测试页面：浏览器每张源图 natural size 与公开 WORLD11 相符；三个标记锚点、三个资料卡、技能原参数展开、开关显隐通过；叠图关掉后完整场景截图回到基线；0 JS 错误、0 对外 HTTP 请求。测试环境对 **file:// 以及 127.0.0.1 页面导航均报 `ERR_BLOCKED_BY_ADMINISTRATOR`**；因此仅对**临时内存测试副本**以相同原 PNG 字节替换为 data URI 并将 CSP 的图像来源改为 data 执行。不能宣称原 ZIP 的 `index.html` 在本环境成功直接打开，更不能称原生商业客户端已执行。

原图候选的光照/配色、精灵层级、存宠费率计算、技能价格和学习、对话触发、官方同服及实际客户端地图行为均未得到原生证实。现代叠图为研究工具，**不是原版游戏截屏**。

## 验收与下一步

[公开派生收据](../../research/recovered/STONEAGE-INTEGRATION15-R2-HOTORU-PET-VISUAL-RECEIPT-R1.json) 与 `tests/test_stoneage_integration_module_15_r2.py` 对照 INTEGRATION13、R1、WORLD11 三套已发表源 SHA/数量、角色/图号/参数路径和所有运行负证。CI 只验证公开的可追溯关系，不访问私人原图与 CP950 脚本。Stage A 仍 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 暂停，总体完成率未知。

**NEXT INTEGRATION16**：按模块队列优先寻找尚未联接的真实宠物／室内关系，要求源证及新的可查图像/机制关联；不重复 16048/16049、目录 helper、游戏账号或服务器建设，缺材料则精确止点并轮换下一实际内容。
