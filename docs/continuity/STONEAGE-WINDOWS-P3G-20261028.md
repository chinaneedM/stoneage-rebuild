# 2026-10-28 — P3G：可用Windows的ACP950/8位RGB/输入与有界出站阻断实测

## 从新远端启动及交付范围

本轮从fresh GitHub main `beb4bcb361248afcb8757fd46ffa497f2c4be3d2` / tree `529eb0cb559baba454d50158dea98c1eb972cc5e`启动，重新读取默认分支、HEAD、最新提交、649远端分支、6255项完整tree（无AGENTS）、0开放PR、Actions、协议、README、CURRENT、设计/历史/来源/路线及组合索引和最新R6覆层。前一R6候选/内容主线各11项Actions实际success，最新beb4bcb是文档后记、没有它自身的CI，不冒记父提交运行。

CURRENT完整2680510B、Git blob `031c76a5a8e431f646853909bb2f2e11e6328cd2` / SHA256 `f02f85b837fc09973cb2eca33f7daf4db547a77cb35a81a9576c6308f70142c0` 原样保留。协议14加法覆层继续。最高任务P3G是为后续**原TW1程序**找到可用环境；本轮止于自编程序同时测得的原件启动前提和明确未测范围，不下载或执行原客户端，不以实验窗口充当原世界。

**结果：Windows2025上已测得同一自编x86接收进程的ACP950、8位DirectDraw、真实RGB和鼠标接收；其后另一次运行中，来宾出站阻断生效时这些条件仍成立。Windows2022的失败完整保留。这是有限的合成环境候选，不是原客户端验收。**

## 原P3F清单问题与有限平台对照

旧P3F实际XML把 `windowsSettings` 放入2019/WindowsSettings命名空间。Microsoft [应用清单](https://learn.microsoft.com/en-us/windows/win32/sbscs/application-manifests#activecodepage) 的示例则将application和windowsSettings放入asm.v3，只有activeCodePage属于2019命名空间。新包保留旧文件不改，独立建立错误命名空间zh-TW、正确zh-TW、正确UTF-8三个清单；三者均无supportedOS，避免把清单OS声明对8位兼容路径的影响混入对照。四程序由同一自编PE复制后嵌清单，使用mt.exe从每个实际PE读回清单，再解析命名空间/页值及记录原摘要。

官方文档可作实验依据，不能覆盖实测。两个可用镜像使用同一C/Python来源、默认和256COLOR两个设置，未继续WINXP/Wine/驱动参数树：

| 来宾/条件 | plain ACP/bpp | 错命名空间zh-TW | 正确zh-TW | 正确UTF-8 |
| --- | --- | --- | --- | --- |
| Windows2022 默认 | 1252/32 | 1252/32 | 1252/32 | 65001/32 |
| Windows2022 256COLOR | 1252/8 | 1252/8 | 1252/8 | 65001/8 |
| Windows2025 默认 | 1252/32 | 1252/32 | 950/32 | 65001/32 |
| Windows2025 256COLOR | 1252/8 | 1252/8 | 950/8 | 65001/8 |

2022镜像win22/20261022.344.1；2025实际镜像win25-vs2026/20261021.278.1。2022的UTF-8正对照说明正确清单确实可生效，但该镜像下zh-TW仍1252，不能说“只修命名空间就解决2022”。2025的同平台三清单对照支持命名空间对zh-TW结果的实质影响；跨镜像结果只归属这两个实际平台，不宣称所有Server2022都不支持某功能或仅凭OS名作因果结论。console950没有取代GetACP；八条测量中GetACP前后相同。

## 同一原生接收进程的真实颜色和输入

仅2025正确zh-TW/256COLOR探针通过后，才启动同清单自编GDI和DDraw接收器。两例都报告ACP950/8bpp，GetPixel实得红[222,0,0]、绿[0,200,80]，独立Pillow屏幕抓取分别计19300红及19300绿像素。DDraw创建、offscreen8位、调色板附着、primary附着及Blt均成功。前台/激活/焦点三门槛通过；两接收器均实收down+1/up+1/async轮询+8，结束前正常退出0。不是只看SendInput返回值，也没有从不同进程拼接ACP/图色/输入能力。

这里没有测原程序的ANSI GDI文字。Microsoft [UTF-8/进程页说明](https://learn.microsoft.com/en-us/windows/apps/design/globalizing/use-utf8-code-page) 明确区分GDI与进程activeCodePage；ACP950和红绿块通过不能推出原繁体文字、字体、原Palette或QUIT通过。也未改新游戏的Unicode/UTF-8选择。

## 一次性来宾出站阻断与同期间接收验证

第三个独立Windows2025 source作业只运行自编程序。脚本强制要求GITHUB_ACTIONS和github-hosted，拒绝个人/持久/self-hosted主机。在创建临时阻断前，先注册SYSTEM任务：120秒后删除本包唯一名称的规则；主流程另有finally清理，workflow也有最后同名清理。未更改默认策略或其他规则，不把此机制称为恶意程序安全沙箱。

实际读回规则为Outbound/Block/EnabledTrue、ProfileAny、ProtocolAny、ProgramAny、local/remote address均Any；三个Domain/Private/Public profile实际启用。政策定义覆盖来宾全部程序/协议，**经验测试只覆盖两个同字节自编程序路径向同一已预解析api.github.com IPv4:443的TCP连接**：阻断前两路径连接成功；阻断中两路径均失败、WSAEACCES10013；同期间运行正确zh-TW/256COLOR探针和DDraw颜色/输入接收器；随后再读规则并再次实得10013，排除提前恢复后才测颜色的情况。最后删除后remaining0，原路径连接重新成功。

实际测量阻断窗口约5.282秒，小于120秒watchdog；watchdog在正常清理后注销。同期间自编接收器仍ACP950/8bpp，颜色/接收/焦点均通过。规则全程序覆盖与具体canary证据分开陈述；没有假称已遍测UDP、IPv6、原程序、全部外部目标或本地服务器回环。原程序尚未置入此环境；原进程隔离资格字段仍false。

## 原样来源、永久保管和验收边界

三次源作业均实际completed/success；前两次不同平台结果和第三次临时阻断分别保管：

| source run / job | source HEAD | artifact / ZIP SHA256 |
| --- | --- | --- |
| 40633664224 / 122635585777 | 75a9541f46e58c886042a05260e8608ce0773060 | 12792787192 / 62ddb594074a38be33a706355449a2581270bc63ff0a1c190b1213c2c259c52d |
| 40633836213 / 122636128243 | 93e3ec784a12e8bac6d3dca74e32744bfec30cc2 | 12792249088 / a2df3444169ffc9818b6a3c1d44ff53d7fce581a1baf4e69eda476d4ae01f468 |
| 40634200624 / 122637279605 | 3e99f965941f4a4c2981cb8ecca661419be6f639 | 12792254654 / 40c4b13b09f107a784ba2004fad12052555620ef6272be77fc066598fb142b6e |

三个完整ZIP均真正独立下载、逐SHA与API digest相同，恰一个派生JSON，分别64571B、86930B、19435B。原样raw SHA/Git blob、source HEAD/tree、run/job/artifact/ZIP全部写入 `research/recovered/STONEAGE-P3G-CUSTODY-R1.json`。派生JSON全文永久入Git；没有原商业程序/资源/原图/音频、编译exe/obj或截图进入Git/工件。平台报告四源码指纹逐一匹配Git LF精确转为Windows CRLF，不把行尾差异当版本变化。

最终离线条件增加“恰三profile全部启用”守卫，实际source报告本来就满足；保留source旧指纹和新收紧说明，不重新跑断网实验只为重算摘要。独立离线重放不调用新平台判定函数，重算原报告的清单、GetACP、颜色/输入、版本区别及网络边界；39项本地P3G/P3F/P3E检查通过。候选与主线CI仅离线验收，待真实运行后补记；源作业绿色不等于原世界完成。

## 下一最高：ORIGINAL-TW10-WINDOWS-LOGIN-P3H

本包环境前提取得实质结果后止点。下一包只做**原TW1真实登录屏幕与可退出输入**的有限Windows观察：先核原程序/最低运行文件全SHA及既有私人保管；验证外置正确清单能作用于未修改的程序，不能把本包自编嵌清单结果直接迁移。仅在临时来宾隔离与回读门槛实际就绪时启动认证原件，原EXE字节不改；私有画面须有完整来源/加密保管。原文字、颜色、菜单/QUIT分别观察，任何条件失败即留下精确止点，不再展开参数树。若缺实际原件保管，不为摘要重复下整盘。

该登录验收不等于世界进入；真正选角/行走/战斗还需要单独的loopback通路与来源限定服务器消息，不能用现代观察器、伪人物或编造的官方状态替代。Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79暂停、整体完成率null，DD-028/030及全部历史失败不变。

## 内容候选及主线的真实后验验收

归档候选 `20862d8d9a16730cab51ed4734b13f3470335948` / tree `daaa29e402a92bee7993bb4af8c1958de2ed8741` 的11项Actions全部实际completed/success；专用run40634805494/job122639193496通过39项测试和完整离线源重放。重新核对main与PR clean/mergeable及精确HEAD后，经PR#20非强制merge进入 `5e05ab7ab3b451fe1346e94d1123e26a6e5d1e8f`，合入tree与本地已验全树相同。

内容主线的11项Actions也全部实际completed/success；专用run40634887467的真实日志再次确认39测试与P3G_ACTUAL_SOURCE_OFFLINE_ACCEPTANCE。全部候选/主线run、job、13路径Git blob及历史前缀资格永久固定于 `research/recovered/STONEAGE-P3G-PUBLICATION-R1.json`。这22项是离线验收，不冒称重新执行原程序或重复断网；三个真正Windows源作业另有完整保管链。

三个原样报告的CRLF完整保留；diff whitespace按cr-at-eol核验，不为消除行尾提示改写源证据。六份启动/历史文件全文原样，README原93817B完整前缀保留。该后验收据自身的后续CI不预支成功。P3H与原客户端/文字/回环/世界边界不变。
