# 2026-10-28 — P3H：原TW1在Windows实际运行/退出，画面仍黑，完整原件已私人保管

## 启动、交付及止点

本轮从新远端 main `29f9ad13130f311a1080ef537d7638cd5e7a2315` / tree `aeffec524dfcc6c1e7f3f8e24614e6311f9bda6f` 启动。重新核验默认/远端分支、HEAD、完整6268项tree、最新提交、0开放PR、Actions，按协议重新读取README、连续性协议、CURRENT、设计/历史/来源、路线、组合索引及最新P3G覆层。tree没有AGENTS。最新主线自身run40635019986实际success，不借旧聊天的SHA或父提交CI作当前事实。

CURRENT仍完整2680510B，Git blob `031c76a5a8e431f646853909bb2f2e11e6328cd2` / SHA256 `f02f85b837fc09973cb2eca33f7daf4db547a77cb35a81a9576c6308f70142c0`。延续协议14及既有大文件传输限制，用本加法覆层和README指针记录，不替换或缩减完整CURRENT及既有历史文件。

最高任务承接P3G的 `ORIGINAL-TW10-WINDOWS-LOGIN-P3H`：仅恢复认证原TW1未改EXE的真实启动窗口、可观察画面及可退出输入；版本范围为已接受的台湾WAEI/JSS 1.0原盘样本，不用mixed2.5现代观察器充当原程序。本轮止于一组有界Windows原件实验及独立保管/验收，不输入账号密码，不联系原服，不构造世界状态。

**结果PARTIAL：原程序确实运行，三次采样存活并出现所属主窗口；在已知退出坐标点击后，清理前正常退出0。独立目视两张不同原生抓图却只有黑底、右下“半形”和一处光标，不能认证游戏背景、菜单、调色板或繁体UI恢复。世界仍未进入。**

## 未改EXE的外置清单及原件来源

先搜索/列举既有私人保管，没有找到完整TW1运行树或原载体；不把已有mixed2.5载体当TW1。自编x86探针以 `/MANIFEST:NO` 构建，同字节复制为plain和外置manifest两路径；正确asm.v3/2019命名空间、zh-TW、无supportedOS。Windows2025镜像 `win25-vs2026/20261021.278.1` 的实际plain为ACP1252，外置manifest为ACP950，二者256COLOR均8bpp。原PE字节摘要完全相同。相同外置manifest接收器同进程实际GetPixel/Pillow红绿、前台/焦点和down/up/async接收通过；挂起创建、加入一进程Job、读回限制、再恢复执行的自编smoke也正常退出0。

这解决“外置清单能否作用于未改自编PE”的前提，没有直接测原进程GetACP或原GDI文字。随后才取得固定原盘842125501B：MD5 `b37a4a47f4eb608cac67e4ddf7a1621a`、SHA1 `b8cf92720b6ec8b3f46ea2e9bfcda986d21e7ded`，本轮完整SHA256 `55377aa14bfa495b53ad52fa0406c2b7dea224f75a908a238f95aee8dbae36a9`。每段HTTP206/Content-Range和全盘摘要分别核验。

只静态提取STONEAGE.bin，再按固定inventory Git blob `564233902b10c60760d4f93b1ea65d4dd1469206` 验证全部375文件/372529095B；不执行安装器或加载旧驱动。原 `sa_3.exe` 425984B / SHA256 `cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a` 不改。不可变source树与运行副本分开，manifest仅放运行副本旁。三个原样source报告和独立目视后记分别保留，未用后记改写原报告的assistant_viewed=false。

## 同一临时来宾中的阻断、原进程和坐标退出

仅接受github-hosted一次性Windows，拒绝个人/持久/self-hosted主机。预先注册SYSTEM120秒同名规则恢复任务，核三个profile启用，再创建本包唯一全程序/全协议Outbound Block规则；主流程finally和workflow另有同名清理。读回Job flags8200（kill-on-close + active-process-limit）、active1，原件在挂起状态加入Job后才恢复，无breakaway。没有把该机制称为恶意程序安全沙箱。

外部canary为预解析api.github.com的一个IPv4:443 TCP端点；阻断前连接成功，阻断中自编checker实得WSAEACCES10013；同期间再次验证同一自编接收器ACP950/8位RGB/输入，再启动原件。原件观察结束后规则仍Block、canary仍10013。先关闭原Job，再移除规则和任务，remaining0，外部canary重新成功。没有遍测UDP/IPv6、原程序每一次网络尝试或本地回环；策略范围和经验测试范围分开。

原进程PID5960，QueryFullProcessImageName核实际运行副本路径，三次所属窗口采样均为唯一可见主类 `ＳｔｏｎｅＡｇｅ`、640×480客户区、进程存活。采样在阻断开始后约3.812/6.875/9.906秒；脚本另要求总观察不越110秒，不将这些采样时点冒称完整阻断时长。命令使用已有updated/资源路径/windowmode参数，唯一目标为127.0.0.1:9，无服务端应答。

只对精确PID/映像/主类/客户区通过且前台激活的原窗口输入。坐标(350,380)来自此前P3C已目视的客户区退出位置，不沿用Wine root坐标(350,410)。本轮SendInput down/up各返回1，随后进程退出0、所属窗口为空，finally清理前poll仍0。**这是已知坐标输入后退出的实际行为；没有在本轮图上辨认出QUIT标签，也没有测到原程序内部down/up计数。** 因此不能把自编接收器计数移植为原handler实测。

## 黑屏原图的独立核对：非均匀不等于游戏画面

完整工件独立下载并匹配GitHub API digest后，本地解密、逐375成员重哈希，再逐三帧重算PNG/RGB摘要与源报告一致。真正打开了第0、1两张不同图片；第2张与第0张PNG/RGB全字节同一。画面均为黑底，仅见“半形”和偶发光标，没有可辨认的游戏插画、标题或START/QUIT文字。

| 帧 | 黑像素 / 307200 | 非黑像素 | 不同RGB数 |
| --- | --- | --- | --- |
| 0 | 307103 | 97 | 2 |
| 1 | 307096 | 104 | 2 |
| 2 | 307103 | 97 | 2 |

源脚本的nonuniform_pixels=true只说明IME/光标使图非均匀；原图没有自编红绿块。独立后记明确visible_game_picture_verified、原Palette、原ANSI GDI文字、原GetACP直接测量、认证登录及世界进入全部false。黑屏也不能证明原DirectDraw surface绝对没画过：本轮只有Pillow/GDI屏幕路径，没有原surface只读回读。这一原因保持OPEN，不猜“资源损坏/代码页已好/截图API漏图”中的任何一个为FACT。

## 三次失败及修正来源保持可见

| run / job | HEAD | 实际结果 |
| --- | --- | --- |
| 40636052597 / 122643158994 | 906804c4df70537d71f9b7130219b54abe643262 | PEM换行使证书pin拒绝；无原件下载/执行，无report工件 |
| 40636474207 / 122644488781 | 5683d2d8b018ce72ef0c3380a21e561d289c0521 | 外置清单与Job通过、原盘摘要匹配；inventory换行导致提取前拒绝，无原程序执行 |
| 40636750207 / 122645368520 | e6f226bcd5a3e5fdc63e0ebf1719e939debfae79 | checkout-index恢复未取得精确inventory字节；前移门槛在下载前拒绝，无原程序执行 |
| 40636932361 / 122645935038 | d3f426505909ce47d07a21e86083dd73d7cd8bce | 精确Git stdout恢复210632B inventory并核原blob；实际运行/坐标退出、封装保管成功，原画面仍OPEN |

证书只对CRLF→LF规范化后核同一完整PEM摘要，内容变更仍拒绝；inventory则直接以byte-returning `git show HEAD:path` 取得并核Git blob，再写回相同原字节。未改变375成员或原EXE摘要门槛。第二次失败曾取得完整载体但没有形成可复用运行包，随后清理；明确记录这次浪费，不把它写成已保存。第三次已在下载前停止。只为取得实际原运行结果的最终原件实验完成后，不再重拉全盘复算摘要。

第二、三失败的原样JSON分别25907B/423B，均独立下载完整ZIP、匹配API digest后永久保存。首轮只有真实失败日志，没有虚构raw报告或artifact。四组HEAD/tree/run/job/artifact/ZIP/raw SHA/Git blob和错误边界详见 `research/recovered/STONEAGE-P3H-CUSTODY-R1.json`。

## 保管、离线验收及下一最高项

成功源artifact12793698659，完整ZIP372671446B / SHA256 `2d71b0a5f99f8e4171ce0b84920860fcaa7366864020d32f116272d1bd296eba`，恰有派生source-report.json及CMS AES256密文。明文原件、三帧及私有源报告封装ZIP372626292B / SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`，完整375原文件逐SHA再次验证。完整运行包 `StoneAge-TW1-original-runtime-and-native-observation-P3H.zip` 和准确命名的黑屏观察PNG均已私人持久保存，另从持久副本完整回读匹配摘要。未来先检索/复用此包，不能为摘要再下载原盘。私钥、明文原件、原图和CMS密文均未写入公开Git；只提交派生元数据、工具、测试及公开接收证书。

新增离线检查独立复算原报告的原件/探针区别、所属窗口、Job/出站拒绝前后、自然退出资格及三帧目视边界；反例覆盖强杀冒领退出、SendInput冒领接收、IME非均匀冒领游戏画面、原GetACP/世界升级和身份/工件漂移。本地相关52项测试通过，候选/主线CI需后验另记，不预支绿色。

最高NEXT为 **ORIGINAL-TW10-NATIVE-FRAMEBUFFER-P3I**：只判别原surface/调色板未出图与既有屏幕抓取路径漏图这一具体缺口。先复用已保管375文件及P3C/P3H图证核对原生绘图路径，只有能改变这个结论的一项只读原生观测才继续；不扩WINXP/Wine/驱动/参数树，不把外置清单或合成红绿资格当原GetACP/原Palette实测。若无法取得不同于现有Pillow路径的有效读出，就保留精确阻塞并回组合域队列，不耗尽helper。账号面板、loopback登录及原世界移动/战斗仍独立待资格，不造官方服务器状态。

Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、DD-028/030和总体完成率null均保留。
