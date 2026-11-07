# MAP07｜28份原DAT × 234组原RD像素：批量室内场景观察（2026-11-07）

## 启动及证据范围

严格按连续性协议，从 `main=14902e101abdd52e12bc929a14101c129cf59367`、tree `21db4cc07c9c8ac540505407d9d972474d13efca`、完整 `CURRENT-STATE.md` blob `c89e0e33537990aa2132b47c40fef49a985a935c` 和最新MAP06继续。保留2709173B历史CURRENT不覆盖；本文件为加法覆层。唯一目标仍是原版原资料的单机化历史复原，不做新引擎、网服账号或体验优化。

原地图：社区保存混合2.5载体361,255,180B，SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，不冒充初代官方客户同服。原图像：此前已保存台湾1.0零售原RD来源的MAP04资格包（4,166组候选像素），35,673,334B，SHA256 `e9c43222797c7ebcddfcb1ccab6dbeba205b972bbbff4e1f29c14b3ece320d37`。两种来源不能仅凭相同数字认定同一官方部署。

## 原件实际完成

一次来源Actions批量恢复28个互异SHA的原DAT：1002–1004、1101–1105、1201–1205、1301–1305、2001–2005、3001–3005，每个30×30、5,408B，总计151,424B，每一项 SHA、长度与既存MAP04源索引完全一致，源ZIP 28成员CRC通过：

- [源数据成功运行 #42348954323](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42348954323)：整RAR真实SHA校验，28源DAT逐件校验，私密CMS加密传送；公仓库无可读取DAT/私钥。解密ZIP SHA `a132fbc89a981cd72c98ad9b8e1aee882748e8b76995a3b057ee76c435de586b`，本地独立28/28原SHA核对通过。
- [原ADRN偏移成功运行 #42349216764](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42349216764)：从已在Git保存的原TW1 ADRN压缩TSV核原RD索引、宽高与块SHA，派生4166条有源原图偏移，SHA `4ea44469c97d61f108cbc310f4384b4a83083db6d58628082a4c7de330964b24`。

28个原地图格前两平面共得到**4,408次大于99的候选绘图位置、234组完全匹配原TW1 RD的图号**。逐张比对原候选PNG SHA、RGBA SHA、源RD SHA、宽高与原索引；不把MAP04已完成解码算成本轮新解码（本轮新RD解码**0**）。另有前两平面 **21,510次非零1–99数值**原样保留但不认定为可见图块；第三平面完整保留，不猜碰撞、任务或规则。

借历史SCENE21/MAP06现代观察坐标 `(x+y)*32,(y-x)*24` 和原ADRN的 xoff/yoff，28张原地图各生成平面0、平面1、合层，共 **84张候选观察PNG**，每张画布1889×1425。原图不是AI补画；实际观察有岩墙、木墙、室内地面、家具候选。**这些图不等于原客户端截图、原生层序/透明/色盘证据、同服地图、原生碰撞或可玩的世界。**

## 私人交付及独立验收

私用 `StoneAge-MAP07-private-28-original-room-scene-candidates.zip` 最终 **34,044,818B**，SHA256 `2b356fefa1f5c634a2a64837b20904e124ab9839ad6a4e3b9a642e3c05df29a2`，351成员、完整CRC通过；含原28 DAT、234原PNG、84观察图、`MAP07.html`、原位置表、源观察收据和离线 `replay-from-private.py`。28张合层画面使用独立NumPy逐像素覆盖算法与Pillow全画布RGBA相同；离线回放脚本再次从私人包独立读回28原DAT/234原PNG，并核**84张RGBA摘要**全部一致。

公开仅保存 [MAP07来源边界回执](../../research/recovered/STONEAGE-MAP07-28-ORIGINAL-DAT-SOURCE-SCENE-RECEIPT-R1.json)、验证脚本与本篇。公CI只能核原元数据及守恒关系，**不能替代私人商业图像重建验收**。尝试将34MB私人ZIP保存个人Library失败，报 `container_session_unavailable`，故**不主张其已持久化到Library**；私人28场景联系缩略图单独保存成功。正式私人ZIP已生成并可直接交付，用户应保留完整ZIP以供下次复核。

## STATUS / NEXT

MAP07 `SOURCE_BOUNDED_PARTIAL`。原客户端未启动，原地图未原生运行。Stage A **7 PARTIAL + 2 OPEN**、Stage B/wiki `GATED`、R79 `PAUSED_NON_BLOCKING`、overall_percent=`null`，均保持。

**最高 NEXT MAP08：**优先在同一地图模块中继续实际原DAT规模较大的村庄/室内来源场景，或真实取得MAP05尚缺的12原图号；先核真实原字节、来源完整SHA和可观察像素，再扩合图。避免为每张地图重复下载361MB载体；后续优先成批取回并私人保管合格原件，不进入网游重建或Stage B。

## 追加后验：私人Library保管与首次主线验收（2026-11-07）

初次以container_path向Library上传34MB私人ZIP失败的原记录保持不变。随后通过已导出的精确文件快照向个人Library `/石器时代/StoneAge-MAP07-private-28-original-room-scene-candidates.zip` **上传成功**；为避免仅凭API返回推定存档，另从Library重新下载整个文件并在本地核验：**34,044,818B / SHA256 `2b356fefa1f5c634a2a64837b20904e124ab9839ad6a4e3b9a642e3c05df29a2` / 351成员 / 全成员CRC通过**，与原私人交付逐字节全文件SHA一致。此前“Library未确认”描述是早于这次成功操作的阶段记录，不再是最终保管状态；没有私人原地图和原图进入公开Git。

PR [#232](https://github.com/chinaneedM/stoneage-rebuild/pull/232) 已合入主线 `244c8cc5e6258c7ac701bfb0efdd1ce110a126b2`；该**合并SHA**的实际11项 Actions 均为 `completed/success`，包括 MAP07 公开来源验收 [42350176227](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/42350176227)。此后只增补私人持久保管后验与相应公开反例，地图恢复阶段边界和NEXT不变。
