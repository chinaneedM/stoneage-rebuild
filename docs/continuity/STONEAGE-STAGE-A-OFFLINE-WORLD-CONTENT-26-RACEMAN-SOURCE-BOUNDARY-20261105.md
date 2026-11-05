# Stage A｜WORLD26 猎宠活动Raceman的精确缺源止点（2026-11-05）

从fresh远端main `09276c368c0b3d096eaa9f88c4d9a713bd2620c6` / tree `223da0a7c30c6650174e29d0dc9679a4a4cd376b`启动，0开放PR、853远端分支、7,186树文件；最新内容主线WORLD25的11项Actions实际success，最新收据提交没有新内容工作流。重新核启动文档及完整CURRENT的2,709,173原字节与该远端Git blob一致；原blob `c89e0e33537990aa2132b47c40fef49a985a935c`不改。

本项只解决WORLD23剩余唯一Raceman参数的GetItem能否在**已取得的同保存包编译样本**中获得语义。取得有据用途或精确缺源即止，不继续竞速、家族活动、物品解析器或服务器运行链。

## 实际核验与结论

完整重读GMSV 1,897,867 B / SHA256 `d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00`；完整核私人NPC ZIP `c35ed12638f5ff1eb7e076d8989010b083fe529db5543d50bfc52a179f3eab2f`的2,205成员逐长度/SHA/CRC。父RAR没有重新读取，不启动原程序，不解包或发布原程序/对白。

`race2/second.create`经`npc_raceman`→`race2/second.template`的`functionset=Raceman`→`race2/second.arg`，原地图3206、坐标(15,19)、图号16171和三文件SHA均与O88旧记录一致。原第20/21行分别是`CheckItem:20760`和`GetItem:20760`，GetItem行SHA与WORLD23完全相同。这一活动及其日期、名称和静态文字**早已由O88/QUEST04记录**，本轮新增发现活动数为0，不重复宣称发现。

原`NPC_searchFunctionSet` VA `0x48aa20`：从表`0x579a40`读取名称指针，记录步长68，索引0至59（含）共60项，调用`strcasecmp`作名称比较，未命中返回-1。核对完整60条记录/名称与SHA，**没有任何大小写形式的Raceman匹配项**；完整原EXE也没有该ASCII子串。`NPC_copyFunctionSetToChar`的同索引边界亦核对。表中索引56/57确有`PetRaceMaster`/`PetRacePet`，它们是不同名称，不能替代Raceman来证明这份猎宠参数的字段用途。

因此结论严格为：**当前这份编译样本的该名称查找域不含Raceman；匹配处理器缺源，GetItem发放/消耗用途保持OPEN。** 不是已经观察NPC加载失败、活动无法参与、所有版本均缺该实现，更不认证台湾1.0/JSS1999/大陆1.82官方部署。即使同父保存包，也不能推定全部参数与EXE属于相同可运行配置。

## 两候选物品表与旧证据保留

ITEM01的20760索引在表A原行SHA为null、表B有原行SHA。O88原A表缺项结论仍正确，QUEST04已记录B表存在；不把旧缺项扩大为所有版本缺猎宠证，也不把B表存在当作同服发放成功。本轮复核已发布的逐ID元数据，不冒称重读整份B表。旧WORLD23原始数字目录、O88、QUEST04全部原样保留，无需复制已有私人原文字包或再造观察器。

[公开受限报告](../../research/recovered/STONEAGE-STAGE-A-OFFLINE-WORLD-CONTENT-26-RACEMAN-SOURCE-BOUNDARY-R1.json)18,061 B / SHA256 `85cf12f931872e040620f8cc92dfb495ab8dd3f926775fb4615c900235a6bc3f`，只存源元数据、60个功能标识/表记录哈希、编译查找窗口SHA与物品索引。独立不导入项目PE工具的节映射读取器逐一核同60条记录/名称/哈希；nm独立核三个选定COFF符号与strcasecmp，objdump独立核查找步长/边界/失败返回。本地56/56相关测试通过，无skip；公开CI只重放派生数据，不读私人EXE/NPC。实际远端结果在成功后追加。

## 回模块内容队列

重开条件仅为有来源的匹配Raceman处理器/构建或对这些确切参数的原生踪迹。现在离开编译物品字段辅助链，保留OPEN，不扩邻近PetRace实现。

**最高NEXT WORLD27：任务模块原交宠分支整批来源联接。** 对现有完整NPC子树初筛，17份原脚本有97条`DelPet`物理字段。下轮以完整原条件块/创建引用、相关原奖励和物品/宠物来源整理这一批交宠任务资料，复用WORLD21/22的读取与私人原文观察能力；先查重已有QUEST/O系列成果，不把97字段叫97任务，不猜`PET>`等语法、物种命名空间或实际删除行为。常驻本体/运营活动/起源未明分开，有原件才联接，缺件精确记录。交付应是可连续查阅的有源任务内容，不能变成又一条无限处理器辅助链。

Stage A **7 PARTIAL + 2 OPEN**，Stage B/wiki **GATED**，R79 **PAUSED_NON_BLOCKING**，整体完成率未知。当前仍为忠实历史复原；不做网游基础设施、新引擎或体验优化。
