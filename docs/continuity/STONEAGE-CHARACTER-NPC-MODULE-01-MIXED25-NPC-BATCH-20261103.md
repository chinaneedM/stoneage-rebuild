# CHARACTER / NPC MODULE 01｜混合2.5原RAR完整NPC子树实物批量复原（2026-11-03）

## 原始材料和实物验收

本轮依协议重新读取 GitHub 远端 `main` `4fd244f32fc6b6b8ef1fa96cbc359be766d160e3`/tree `487616c96b7a748bc6807ae269410df4498bc07d`、完整 `CURRENT-STATE.md`原blob `20050acf279a01555ab06a381dfcdc936bd381a6`、最新提交、Actions及模块路线。最新PET10主线原11项Actions均success，下一模块为人物/NPC。原历史CURRENT和此前NPC研究不修改。

用户私人Library原载体 `stoneage-preserved-mixed25-original.rar`（361255180B / SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`）已在本工作环境重新实际逐全包SHA核对。Python `rarfile`原RAR目录7952项、系统libarchive通过ctypes逐源解出完整 `gmsv/data/npc/` 子树2205个原成员、合计1930332B；每个原件的实际解压大小/全SHA256/源RAR CRC32三重校验通过，原源失败0。原文件仅私有保存，不放到Public仓库。共包含189个`.create`、46个`.template`、309个`.arg`、1585个无扩展名文件（大量原对白/参数），另包括31个`.conf`及其它原成员，完整类别见[公开有界收据](../../research/recovered/STONEAGE-CHARACTER-NPC-MODULE-01-MIXED25-SOURCE-RECEIPT-R1.json)。

## 完整文件批处理实得

- 189份原 `NPCCREATE` 文件的真实源分块 **4985条**；其中有2451条非空名称字段、2482条数值 `graphicname` 出现，共254个不同数值图号和633种数值 `floorid`。它们包含原 `npcgen_warp` 2904条及真正人物候选、商店、任务、竞技、事件、宠物摆设等，**4985不是原NPC人数，254不是人物模型数，633不是地图数**。
- 46个原模板源文件含119条 `NPCTEMPLATE` 区块；使用配置里的 `enemy=` 精确源代码token寻找同包定义，4131条同目录唯一、853条同RAR其他目录唯一、1条跨目录歧义。同文件/同包找到定义只表示静态位置，不保证实际载入执行。唯一歧义为 `giiru/event/sikkoku/sikkoku.create` 第5块的 `npc_transmigration`，命中 `777.old/allnpc.template` 与 `777/allnpc.template`，不臆断哪个运行。
- 4985配置中出现1803次 `file:` 精确路径引用：1788在同一原NPC子树有完全同名目标文件并校验原文件SHA，另15缺同路径目标（均为 `genout/msg_...`，详情收据逐条列明）。缺当前RAR目标不等于原发布缺功能，可能有其它载体/运行时生成文件。
- 所有源配置的物理原块位置、原块SHA、源图号、楼层、坐标、模板命中候选及原 `file:` 目标资格都已入本轮完整**1798170B**派生行级索引，SHA256 `f6beb17b76b23211d36113bcf462c16ac38435233b3891bb21765179b84e4566`。由于本轮文件上传容器会话接口报告expired，**这份大行级索引仅作为本轮会话可下载完整产物，不冒称已写入远端Git或持久Library**；远端公开收据完整固定源SHA/数量/缺口。原2205私有源ZIP已确认成功入Library。
- 原文本编码以CP950为主要候选，但部分原文件对CP950严格解码失败；私人ZIP保留无损原字节，UI在此少数条目使用有标注的替换候选，不能当作已权威校订。完整原对白未公开。

**私人实际可阅交付：** `StoneAge-CHAR01-original-mixed25-npc-catalog-private.html` 1357638B / SHA256 `3daaf6e18eb65d7781ea859861889d363ffba0a2fd5ba640803c56ade9626217`；支持简体中文界面按原文件名/原NPC名称/楼层/图号/功能token筛选、源SHA和原创建字段详情。Chromium本地实际 `set_content` 检查初始4985行、分页80行、原文件筛选25行、图号16017筛选45行、无图号2503行、详情字段、0 JS错误/0请求。打开HTML不是原游戏NPC交谈或运行。

### 与早期台湾1.0材料严格独立

先前已证台湾1.0原EXE建角数值窗口含12组 `100000..100220` 候选，与原SPR同构建来源相接；R99另存原TW1静态NPC-like位图区间 `5846..5946` 共101原位图资源。这两类**不与混合2.5服务器原NPC姓名/职责自动绑定**。此次没有重新解码早期角色动画原RD、没有认证原官方NPC物种、同服菜单或实际世界运行。

Stage A7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING，总完成率UNKNOWN；仍为历史复原，不进行现代体验/引擎/任务优化。

**NEXT：CHARACTER-NPC-MODULE-02**。集中复用已保存TW1完整原P3H及SCENE23/31的人物真实原SPR/RD和R99静态资源，优先批量恢复12个早期原人物图形候选的实际可视原帧/动作，再向NPC的101原静态图像补原像素；若同源像素短缺则定量注明，不把所有`.create`当人物，也不混合早期官方身份和后期社区服原名。
