# CHARACTER / NPC MODULE 02｜台湾1.0原人物12个候选源全八方向动作2像素（2026-11-03）

## 原件与批量恢复结果

从最新 `main` `2ee8a69ffa2f1be0be6694d36d454c268937b7b5` 与完整未修改 `CURRENT-STATE.md` blob `20050acf279a01555ab06a381dfcdc936bd381a6` 启动，CHAR01主线11项Actions全部实际成功。继续人物/NPC模块，不跨到新游戏设计。沿用来源已经认证的台湾1.0零售样本和SCENE23已固定的同源12个数值；P3H私人原ZIP `372626292B` / SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24` 本轮再次实际取得，实际从其中读取7个原件并逐文件大小与SHA验证，原EXE/SPR/SPRADRN/ADRN/REAL及Palet_0/Palet_1都符合前轮保存的来源固定摘要。

**新增实际源资格**：批量解析原SPR完整12组 `100000,100020,...,100220`，逐整组段SHA与SCENE23的同源派生表全相同；对原数值动作2的八个方向分别保留准确原动画头、duration原整数、帧顺序、偏移、原音效word及位图ID。共 **12个原图形候选组 / 96段实际原动画 / 728个有序原帧位置 / 576个不同原bitmap**；实际从真实REAL每块读取，逐RD完整块SHA与源ADRN物理地址/尺寸核对，576/576个不同RD严格解码成功、0失败。与SCENE23先前12×8＝96个原首帧的原索引像素SHA逐条相同，且补齐各序列原后续帧。

原始动作帧数并不每组相同：例如原100020每方向14帧，100100每方向11帧，100140和100200每方向9帧，其他所选组每方向6帧。**动作码2只是源数字，不能叫行走/死亡/受伤**。这12项来自客户端EXE内部32位数据窗口数值候选及原SPR，不是认证过的官方12个人物名单；数量、名称、性别、发色、选人画面、真实原服创建成功未知。源duration word不当成FPS。调色板以两份原SAP计算仅作为颜色候选，不称真实运行时选择。

## 可直接打开的私人结果

- 完整源限定逐组、逐动画、逐帧及576个原RD收据：`StoneAge-CHAR02-TW1-original-12-actor-action2-public.json`，262602B/SHA256 `8394ece0acdd25126fb1e3755f0c909e515798c7c29ec6b75005e20f810af888`，**此大报告只存在本轮私人工作目录/用户可取的会话附件，不在Git或Library**；远端小收据只存其不可伪造的名字、摘要、大小。
- 原576块真实私有PNG×两SAP候选，全部嵌入 `StoneAge-CHAR02-TW1-12-full-action2-private-observer.html`，6578861B/SHA256 `34c9d0c7489a493a6bd83fea99d44305cd0fb4f828403b7e4359255a29069f55`。本地Chromium实际在安全隔离的`set_content`逐一选完96条方向动画、验证真实图宽高、切100020第14帧及另一候选配色，JS错误0、外部网络请求0。不是原Windows游戏实际启动/原场景原生渲染，`file://`直接导航不称本轮验过。商业原PNG/RD/HTML只私人，不公开Git。
- 项目Git仅提交紧凑的[CHAR02完整12组证据收据](../../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-02-TW1-12-ACTOR-ACTION2-RECEIPT-R1.json)、负例守卫与本文；CI验证派生守恒，不重新拿到原商业源，不宣称CI重新解出576块。私有影像源可信度来自本轮实际原RD复算与本地浏览器，而非Git测试自身。

## 下一优先

**CHARACTER-NPC-MODULE-03**：现有TW1静态NPC-like号段5846–5946计101个原bitmap的物理元数据与可公有索引，缺实际同源批量像素观察，优先复用本次已保管P3H里的完整TW1 ADRN/REAL，按位图原地址原RD严格解码，私人查看其本来图像；但这个号段的NPC归属只见于后期资料玩家分类，不能把101图形称作101官方NPC，更不能把`map_number`冒充世界floor/NPC位置。与后期mixed25原NPC模板/中文名字不做无凭绑定。Stage A7PARTIAL+2OPEN，Stage B/wiki GATED，R79暂停，overall_percent=null。
