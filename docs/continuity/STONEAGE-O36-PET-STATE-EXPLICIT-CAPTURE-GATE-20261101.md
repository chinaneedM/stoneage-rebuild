# O36 — PET-STATE-01：捕获宠物写入玩家拥有列表前必须明确提供六项状态（2026-11-01）

## 现有代码问题与本轮最小修复

依据远端项目 `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md` 第13节和 `research/recovered/STONEAGE-RESTORATION-PORTFOLIO-R1.json` 最高剩余事项 PET-STATE-01：已有后期保存版 `capture` 源模型可以演示战斗回合捕获，把提供的完整 `PetActor` 持久化并重新读取；然而 `resolve_persistent_capture_round` 原先接受缺少 MP、最大MP、经验、升级门槛、改名标识或自由命名的 `PetActor`，这六项不能由现有来源安全填入默认值。如果任由缺字段宠物进入存档，下次成长、使用、显示字段会出现信息损坏/运行时缺失。这不是官方游戏中宠物值已证的意思，而是本项目**当前重构代码的数据完整性**风险。

**只做最小正确变化：**在既有 `tools/stoneage_local_runtime_session_coordinator.py` 的**持久捕获入口**读取任何战斗/建立临时 domain 之前，要求每个被提交为捕获结果的 `PetActor.state` 里显式提供 `mp`、`max_mp`、`exp`、`max_exp`、`rename_flag`、`free_name` 六字段且值不为 `None`；缺失即明确报错，**不会生成 0、满MP、自由名等猜测默认值**。沿用既存捕获、复制、事务与存档逻辑；不新增状态引擎、不引入数据库/服务器、不改变历史战斗规则。为兼容独立低层捕获模型，现有 `SinglePlayerHistoricalRuntime` 仍允许部分状态的实验对象；**只有持久进入玩家拥有列表的 coordinator 边界应用更严格检查**。

## 具体验收

为避免“只是文档”增加两类实测回归至 `tests/test_stoneage_capture_state_lifecycle.py`：六字段分别缺少必须拒绝而且旧角色状态/捕获暂存不被修改，MP明确提供`None`也拒绝；六字段完整时必须完成一次来源输入明确的战斗捕获、结算、磁盘保存、重载，逐字段原值相等。原 `tests/test_stoneage_local_runtime_session_coordinator.py` 的既有成功案例原来只有4/6状态，现补上来自**明示合成测试输入**的MP17/maxMP31/rename0/free_name字符串，禁止将其记录为原版真实数值。所有其他已有测试仍应通过。

**来源局限：**虽然保留了真实原始地图、动画、NPC与游戏背景相关研究，但此变更是现代重构的**事务数据完整性保证**，不是发现台湾1.0真实宠物拥有/命名/MP及EXP数值、原商业客户端运行或原捕捉权限；不提升阶段完成率，不建立新的音效关联。

从本轮已验证合并后的远端主线 `44bf4a7cc85ee4bd5eeb6fa7c305cc3f2c3c250f` / tree `910c8e2ebcc70df417e106821f66b69d67c50fb7` 开始，完整 `docs/CURRENT-STATE.md` 2,708,031B / blob `20050acf279a01555ab06a381dfcdc936bd381a6` 依协议全量读取、保持不变。PR93候选12/12、main10/10已逐项核实。本轮公开 Git 只含源码、测试、派生收据和此说明，没有任何受版权保护的原始游戏素材。Stage A 7 PARTIAL + 2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，overall percent=null。

**NEXT O37：**回到能真正观察的原版内容：优先检查已取证的保存版宠物店地图1003及其 NPC 创建、参数与原像素是否有完整私有原件可交互；缺原MAP/RD载荷或原版传送链就明确止点，不伪造建筑图片、不把现代资料跳转冒充原游戏路线，再轮换到其他有原件的玩法。
