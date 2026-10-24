# P2B / 台湾1.0至大陆5.0：101条静态图像候选原始双版直接记录联接

2026-10-24。目标是把可验证的NPC图形候选作为**实物资源类别**纳入版本谱系，但不把玩家文章的类别词转成官方NPC身份；所有派生源自原版图像元数据，未执行游戏或复原原服务器NPC。

## 原始来源与实际验收

- 台湾1.0实际零售保存盘衍生：`research/recovered/tw10-resource-metadata/ADRN-R1.tsv.gz` 125,996行/8238749B/SHA-256 `c8669789de1cc6e3575c2412ed86354a49c2b3e90cd2854c1e7b2fc71b0fe9ea`；台湾原盘R99的101个bitmap ID（5846—5946）与物理属性对应 `STONEAGE-TW10-NPC-STATIC-RESOURCE-JOIN-R99.json`，原先NPC类别仅2001玩家版图号判断。
- 大陆5.0真实全CAB新导出：`research/recovered/cn50-resource-metadata/ADRN-R1.tsv.gz` 303,197行/19745873B/SHA-256 `e24afc513d28c7f25bd26bde9c69ddc0de4000147a2b11f50b5176655d8558fd`；来自 `Stoneage-5` 原保留光盘，原CAB 612584670B/全413文件静态解档哈希，含26个LZX目录。该光盘有北京华义MSI内部身份，独立原版压模发行鉴定仍OPEN。
- 上游P2A source run `40091960688` 原字节取得成功，独立报告source custody有ZIP SHA证据；整张CN5资源表实际source run `40093980003` success（初次 `40093556343` failed，修复了SPR物理偏移顺序处理，原失败保留）。
- P2B初步101候选按穷尽相等原件差异投影：Actions `40094709535` success，输出 `STONEAGE-TW10-CN50-STATIC-VISUAL-LINEAGE-P2B-R1.json`。更高等级的**两边完整ADRN原生派生行直接读取对照**：Actions `40095074458` success，输出 `STONEAGE-TW10-CN50-DIRECT-STATIC-VISUAL-P2B-R1.json`。后者每条核对RD block SHA、80B属性摘要SHA、图宽/高、偏移、RD size/flag/尺寸，两个来源表101/101匹配，不依赖仅凭大计数推断。

## 可直接检索的内容

共101物理位图；正确ID范围严格为`5846–5946`（共101条）。5846–5919对应原版`map_number`16000–16073，5920–5946对应16200–16226。`map_number`是原始图形/碰撞资源字段，不是世界地图ID、NPC ID或原场景坐标。每条记录包含原bitmap ID、两版各自真实ADRN物理index、RD块SHA/尺寸/旗标、MAP_ATTR 52B摘要、绘制尺寸/偏移，保留名称、NPC服务器ID、出生位置、NPC脚本及宠物物种ID为null。

举例：bitmap5846，两个版本 AD RN index 均5846，52×72，绘图偏移(-37,-71)，原图形资源`map_number`16000，RD数据2241B/SHA f4880a27d5aa6fb617a308703ea81bd6db3b67fa7a77436183e0b24667ce1911。此号码的具体NPC身份未证。

## 实体层停止条件

- 原始游戏共有多少种NPC、每个NPC的具名形象、任务、宠物成长和生成坐标都不能从本报告推出。2001玩家「NPC号段」是**候选类别**，非官方原画类别鉴定，101不等于101个NPC。无同版角色selector或原服NPC主表，认定具名实体数量仍0。
- 台湾原SPR 242085帧对该号段直接位图引用为0，仅证明该路径未观察到，不排除其他静态图调用。
- 原始图像、版权美术与客户端执行文件没有提交Git；输出仅为来源限定派生索引。
- 日本JSS、台湾1.0、大陆5.0及华义8.5的官方发布归属不互相替代；客户端身份与服务器部署分别认证。

## 后续最有价值工作（不可无限扩helper）

选择一个带同构建原始来源的具体人物/宠物/NPC：优先台湾1.0的sa_3.exe **真实资源选择函数/调用路径**（静态只读，不能猜名字），或者带日期原游戏手册/正式公告的明确图例与资源ID关联，要求一次性把一个明确游戏可见类别或人物对应到原资源ID并有可重放证据。缺原本代码/素材关系则记录阻断，转其他具名版本资料/原版客户端，而不是凭一组大数字编制物种名录。任务仍按DD-028严格分本体、永久版、运营活动和起源不明。Stage A7 PARTIAL+2 OPEN；Stage B/wiki GATED；savedata R79暂缓；全复原进度百分比仍null。
