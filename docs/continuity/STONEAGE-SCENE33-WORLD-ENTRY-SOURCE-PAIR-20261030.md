# 2026-10-30 — SCENE33：已有客户端与SAAC/GMSV实物的静态配对资格

承接SCENE32最高NEXT。启动按协议重新读取远端默认分支、分支状态、HEAD/tree、最新提交、Actions、开放PR和七启动文件、路线/22域/R102及最新覆层；main `4657c290f22487268d57f50b405c61816c368915` / tree `c248d962f92c50dbf5159e469c8002cf598e0500`，开放PR为0，最新收据run40974498243实际completed/success。提交前再次读取main未移动。CURRENT2708031B / blob `20050acf279a01555ab06a381dfcdc936bd381a6` 全文保持；README旧121475B作为完整追加前缀。本覆层依协议14追加，不代替CURRENT或重写早期失败记录。

**结果：存在可供下一轮隔离启动试验的修改版服务端候选；静态认证端口/认证值相合，x86直接依赖可具名。尚无任何SAAC/GMSV执行、绑定、握手、客户端配对或世界进入证据。** 同包不等于同次部署，也不等于早期官方2.5。机器状态为 `STATIC_SERVER_CONFIG_AND_X86_DEPENDENCIES_QUALIFIED_RUNTIME_PAIR_OPEN`。

## 真实原件及读取路径

复用已保管mixed25完整RAR361255180B / SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，未重新下载游戏载体。八个目标原件共5240403B全部解出，逐整SHA与旧静态清单相同；两份同字节Cygwin按各自路径保留，不去重。公开报告只含摘要、路径、端口、计数和真假值，不含程序、原配置全文、说明全文或认证值。

| 原件相对路径 | 字节 | SHA256 |
| --- | ---: | --- |
| gmsv/gmsv.exe | 1897867 | d5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00 |
| saac/saac.exe | 178353 | 299910efe3d04ccf83a224a6f670c9fabe379440df36d6e0bf6514d76c834615 |
| gmsv/setup.cf | 9715 | b4936c103efb7b3cad359e5c85c7965187306883a68c0be712ece6c374e3b12d |
| saac/acserv.cf | 807 | 95d3414597dfb2617ea3fc6fd8bcf134652908661d55b03e04c4fe3e76979045 |
| SA2.5服務端/readme.txt | 1345 | c1140aebf9d08a90f1eec62fd27c766b8a4efa4355a6673179b59782ff657b8f |
| stoneage2.5/sa_2903.exe | 561152 | ec678517f76564ebc9ab00cf3f66853ed9975ef6290eb48168b78909a68a5d16 |
| gmsv/cygwin1.dll | 1295582 | c0e27ae6a7b7106da5db889980a17fe55ea515ebfb3d4c03ce1e26d51bf9c73e |
| saac/cygwin1.dll | 1295582 | 与上一行完整SHA相同，独立成员位置 |

系统libarchive能读客户端，却在cygwin1.dll遇到 `Parsing filters is unsupported`；未把失败计作第二次完整解包。系统包下载不可得、更新权限失败后，没有提权，改在临时工作目录编译RARLab官方源 `unrarsrc-7.3.2.tar.gz`（281897B / SHA `f61a1160d6e2ebbda2ad353c8e82f62ab4312f97fde23c6c2c982d25e0014f99`），程序自报UNRAR 7.30 beta 2。只执行新编译的解包器，没有执行历史程序。独立标准库RAR4头解析扫描7952项，核头CRC、八目标成员CRC/解包SHA及原压缩载荷摘要；它不是第二解压实现。初版探针误将Counter(mapping)当键计数，修为Counter(mapping.keys())后从新目录完整重跑，成功报告两次整SHA一致。原件始终未改。

## 候选配对与版本归属

| 路线/组件 | 本轮FACT | 仍为OPEN/限制 |
| --- | --- | --- |
| TW1官方历史路线 | 已有官方原盘/原客户端基准和受限原运行记录 | 缺同版服务器；本社区包不能补成官方服务器 |
| mixed25的SAAC→GMSV | 实际两EXE、两配置、两Cygwin均存在；说明先SAAC后GMSV | 没有运行配对、协议版本或同部署认证 |
| modified sa_2903客户端 | 原字节与既有C / MIXED-MODIFIED评估相同；GUI PE32 | 固定公网端点/社区修改既有，尚未验证本地重定向，不准自动连接 |
| 文档/配置版本 | 说明含2009.01.20日期token；GMSV配置注释含8.0和后期功能 | 日期仅为文档内部字符串，不是官方发布时间；“2.5”包名不认证干净早期版本 |
| R18 full source | 原R18保全2245项gmsv/data文件 | 不含本轮顶层EXE/配置，不能用其标题认证完整可启动服务端 |

五个PE原件均Intel80386 / PE32。两服务器为console subsystem3；客户端GUI subsystem2。标准库读取的**有序DLL导入描述符**与GNU objdump五件全相同：GMSV六项依次Cygwin×3、KERNEL32、Cygwin×2；SAAC为Cygwin、KERNEL32；两Cygwin为ADVAPI32、KERNEL32。客户端九项为KERNEL32、USER32、GDI32、DDRAW、DSOUND、WINMM、DINPUT、WSOCK32、IMM32。重复描述符按原位置保留，不能压成唯一DLL数。直接导入不覆盖动态加载、传递依赖、操作系统行为或所有后端。

## 配置、资源与具名缺口

两配置CP950逐字节往返成立。受限解析识别GMSV188个有效键出现、11个非键/结构残留行；SAAC18个有效键，原始行号留在报告。此工具不是原程序配置解析器，不据此判断原语法是否可接受。

| 接点或输入 | 实际静态证据 | 启动前仍需判断 |
| --- | --- | --- |
| GMSV认证端 | acserv=localhost / acservport=9200 | localhost实际解析、真实连接与协议握手未测 |
| SAAC监听 | port=9200；两配置认证值逐字节相等，仅公开相等布尔值 | 监听地址、成功绑定和认证接受未测 |
| GMSV玩家端 | port=9065 | 绑定地址与实际玩家协议未测 |
| apport / looptime / enableservice | 三个原值为空，不能静默补默认 | 默认值/必填性/解析行为未知 |
| 地图/NPC路径 | mapdir=data/map、npcdir=data/npc，原归档存在相应树 | 目录/文件存在不证明世界加载、地图正确或NPC可用 |
| 24个限定文件引用 | 除LOCKIP外23项路径各有一个归档项；包含地图索引、战斗索引及若干master | LOCKIP所指lockip.txt未找到，是否必需未知；filesearchnum=8192是数值，不是缺文件 |
| SAAC后端 | 原配置有USEMSSQL=1、AUTOREG=1 | 注释ifdef/配置开关不证明编译实现；无直接SQL命名导入也不证明无需数据库。缺可认证后端种类/版本、schema及初始化输入 |
| 客户端路由 | 原客户端IP:字面marker计数0，既有固定公网端点评估仍在 | 不能沿用TW1的IP:参数。无字面marker也不证明绝无可控入口，需单独有来源核查 |

本轮没有解析全部地图、NPC、数据库或日志语义；log.cf与logdir的组合解析未认证，不能按根目录未见就宣称致命缺件。没有把所有含file字样的键当文件路径，也没有把目录项数当地图/NPC数量。原配置仅作待核材料，绝不是已批准的执行指令。

## 下一最高：SCENE34-ISOLATED-SAAC-GMSV-BOOT

先完成一次有界的**服务端两进程回环启动试验**，此时不启动客户端、不注册或输入真实账号。目标仅回答SAAC能否绑定9200、GMSV能否加载到可观测阶段并向它连接/握手，以及首个确凿缺件是什么；不预报能进入世界。

1. 复用同一已保管父RAR，不重取游戏载体；不可变原树与专用运行副本分开。按实际原引用定界所需data树，验全部运行输入身份；原配置摘要保留，运行副本的每项必要修改单独记录。需要替换认证值时仅用临时合成值，两边一致，值不公开。不要先猜三个空值或凭空补SQL库。
2. 仅一次性隔离Windows x86兼容环境；沿用P3H挂起创建、Job限额、限时终止、清理与出站阻断前后canary的已验思路，但**P3H没有测过回环**，不能直接声称适用。先用自编两进程证明目标环境能回环通信、外部出站被拒、超时和清理有效，再允许原SAAC/GMSV。两服务器分别可归属受控Job；两个进程不能共享原active-process-limit=1。隔离资格失败则不执行原件。
3. 原始网络配置未认证为仅绑定回环，必须在来宾层阻止对外访问/入站暴露并观测实际socket所属PID和本地地址；DNS/外网依赖不可临时开放。原客户端固定端点未解决，所以本包根本不启动它。若无法同时证明回环可用和对外阻断，就具名停止。
4. 顺序SAAC→GMSV，保存有界stdout/stderr、退出码、过程时间、PID/映像/输入摘要、实际监听地址、连接所属和文件访问失败。日志可能含认证值或账号字段，私人保留原件，公开仅脱敏派生。绑定/进程存活不等于成功握手，数据加载提示不等于玩家世界。
5. 若缺SQL后端/schema、lockip或配置语义导致停止，报告首个确切错误与版本范围，不以无限补库、改客户端、驱动/参数树继续。只有完成真实握手与版本限定后，才另包核查客户端路由/协议和游戏进入；此后若确实进入，也只称社区修改版参考世界，不称TW1官方世界。

这是一份最小实验设计，不是已经部署的隔离环境或运行结果。下一轮应先核验现有执行能力及私有源传递/保管路径，再决定能否完成上述资格；缺能力则明确记录并回22域，不继续只造辅助框架。

## 校验与边界

`research/recovered/STONEAGE-SCENE33-SOURCE-PAIR-R1.json` 冻结实际原字节派生事实；`STONEAGE-SCENE33-ACTUAL-PRIVATE-STATIC-AUDIT-R1.json` 固定独立objdump、两CP950、全原件旧清单联接、解包方法与失败。新22项反例后来增加3项audit联接，共25项检查，覆盖官方/运行晋升、错父包/同名换件、丢重复DLL、配对端口/认证值、空配置、缺件/SQL未知及CRC冒领第二解压。公开CI只核派生/合成输入，不取得RAR/原配置、不执行历史程序，source_action_run_id=null。远端Actions待实际后验记录。

本轮新增可运行性知识，不新增官方历史世界内容。Stage A 7 PARTIAL + 2 OPEN、Stage B/wiki GATED、R79暂停、overall_percent=null保持；原世界仍未进入。
