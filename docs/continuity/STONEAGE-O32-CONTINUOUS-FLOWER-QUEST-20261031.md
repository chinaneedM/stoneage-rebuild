# O32 — 连续原图世界内复用原始送花/贝壳静态任务（2026-10-31）

## 本轮真实增量

**没有重新制作一套任务引擎。** 在 O31 具备原保存版 DAT 地图1000→武器店1001、五条实际 `warp_y.create` 源 Warp 创建记录的**同一私人离线可行走场景**内，直接复用 [O24 两 NPC 原创建/任务脚本证据](STONEAGE-O24-TWO-TOWN-ORIGINAL-EVENT-SOURCE-20261031.md)与 [O26 双村落原图/原对话/浏览器实验](STONEAGE-O26-TWO-TOWN-OFFLINE-OBSERVER-20261031.md)，把此前 O31 日美子的静态“仅交谈”推进到一轮完整可见的来源条件**现代模拟**。在萨姆吉尔1000(57,124)日美子交谈并确认 REQUEST，模拟领取 ID2415 `仙尼亞的花`；使用单独标明“资料切换，非原传送”的按钮进入真实保存版地图2000(55,92)彌生近旁，确认 ACCEPT 模拟 DelItem2415/GetItem2414 `不可思議的貝殼`；返回之前1000原坐标，日美子 ACCEPT 模拟 DelItem2414/GetItem2415，**本观察止于一次三步**，不声称原版可刷取无限奖励或符合原版任务达成条件。所有源文字仅私存，公开写必要名称、数字、来源 SHA。

**源资格：** 1000.DAT SHA `94b19cb5…`，2000.DAT SHA `d7523143…`，日美子/彌生原事件文件分别 `eb3f9a9c…`/`6f4d04e6…`，均来自已验 O24/O26 的后期 preserved mixed25；原图借助台湾1.0 TW1 真实 RD，不同部署未做历史同版合并。O31 257 原图 alias、1000/1001 现成 DAT 窗口、五 Warp 源格、商店 ID0 来源资料经私有源码完整对象相等校验**原样保留**；玛丽娜丝独立视窗使用 O26 真实原图像素、原 NPC 图像与原对话对象整值相等。没有新原创图、原服务端引擎或臆造 1000→2000 的传送路径。

**事实与现代模拟分离：** O24 源脚本两名 NPC 各有 CLEAN/ACCEPT/REQUEST 及 EventNo2 静态分支，原 SP、LV、NOWEV、ENDEV、ITEM 条件与服务器背包事务**没有运行**。本轮实现的是便于观察的保守**单轮示范状态**，不是历史真实任务判定。日美子/彌生在原保存版地图坐标有创建记录；台湾1.0/JSS1999同一部署、原 NPC 渲染 selector、原碰撞/原路线仍为 OPEN。任务不擅自归为节日活动。

## 独立验收和版权

本轮私有 HTML 2732647B / SHA256 `b0b19c2fd76adb4d1613e16f2495836e7f81636c04bf9df271883f33fc16f86b`，保留原图与原对话。实际 Chromium 通过 Playwright `page.set_content` 执行 **33/33**：请求/交换/回赠、错误任务阶段不越权、模拟背包 ID、资料切换坐标回返、玛丽娜丝原合成 PNG 真实加载、原1000自动门口行走到1001、商店真实 ID0 行仍可读、复位、无 JS 错误、无外部 HTTP。两张实际浏览器截图私人保存；不声称 `file://` 双击成功（O32 未测试），不声称原 `sa.exe` 或原商业服启动。

私人 6 成员 ZIP `/石器时代/StoneAge-O32-private-continuous-flower-quest.zip` 2919651B / SHA256 `03c7e4f5a091efe3ffe84e77e47b0af1f763223b1fc0562256a3926a587de3ce` 已上传个人 Library，再下载全量逐字节、SHA、ZIP CRC 一致。公开 Git 仅保存[派生来源/验收收据](../../research/recovered/STONEAGE-O32-CONTINUOUS-FLOWER-QUEST-R1.json)、本增量记录、README 指针；**不得公开原图、完整原对话、完整私有 HTML、原地图载荷**。

## 连续性与 NEXT

本轮起点 main `01af2f6f9c394532b1fb5be82697f1c779326792` / tree `e7e7460f16c56718b40919a1854c8afb0e4e618b`；完整历史 `docs/CURRENT-STATE.md` 2708031B / blob `20050acf279a01555ab06a381dfcdc936bd381a6` 已原生全量读取，保持原样，不做“只写尾部”操作。O31 的事件值49155专属性 OPEN、原碰撞止点均不改变。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总完成度 null。

**下一优先 O33：** 根据22域优先级，换到尚未由 O27/O28 覆盖的**一个**真正有原载荷的新游戏交互内容（优先现存宠物关联玩法材料）；缺原件就记录具体止点并轮换。禁止再为 O32 扩任务框架、复制两个观察器或补造原旅行/战斗规则。
