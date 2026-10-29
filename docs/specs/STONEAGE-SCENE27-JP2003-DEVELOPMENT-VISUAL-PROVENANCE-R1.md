# SCENE27 — 日本2003开发中图集位置02/03原JPEG来源合同

2026-10-29；源类别：**2003同期出版方标记开发中画面**。这是2003日服出版图集的实物截图身份恢复，不是原客户端执行、不是真实战斗流程取证，也不能推1999 JSS、台湾1.0或大陆1.82同构建。

## 原件链和新增事实

历史来源索引为4Gamer刊于2003-12-12 20:20的《ストーンエイジのScreenshots集をUp》，指向 https://www.4gamer.net/store/shots/stoneage/index.html 。原图集第一页面标`12th Dec. 2003`、`画面は開発中のものです`；该页15个具体位置，先前R63只真正取得第0/1位置原JPEG。源根证据原报告 `research/recovered/STONEAGE-JP2003-BATTLE-FIELD-VISUAL-SOURCE-R1.json` / Git blob `e84da9c7db1b8792a643d18b191761efa0d73e88`。

本包仅沿该图集的既有 `pages/image0002.html` 与 `pages/image0003.html` 取独立HTML和各自实际内链`../images/image0002.jpg`、`../images/image0003.jpg`。真实GitHub Action `40884309567` 首次取得，`40884459116` 再次完整取回同字节；不是单靠目录名猜文件，也没有扩抓图集剩余位置。

|位置|原JPEG字节|SHA-256|原JPEG完整解码|对应HTML SHA-256|
|---|---:|---|---|---|
|image0002|185950|`8f5c642bcdfffb75fd2f1bb4851db09be2016a97a2acb339cf6a4c2fd773d10a`|JPEG 640×480 RGB，单帧|`eb81231f5aa623dc17be46bc4915d92439bc542ab86275cb439589c17b5a33da`|
|image0003|185778|`2e681e3a93a763f6b78ef4325d9b5f939438c5c57fbc93684df5a960f36a6384`|JPEG 640×480 RGB，单帧|`5ece5743d1573ea331fd4007f0b170d16d9d16c81a3cc373e25efc3c9a2c3ab2`|

原JPEG总计371728字节，新增两个有身份的原图位置，第一图集15位置已有4个精确JPEG身份（R63 0/1，SCENE27 2/3），不称40个全取得。**图像具体内容仍未实际逐像素目视并由人记录**，不凭文件号标注场景、角色或物种。文件640×480是当前下载JPEG尺寸，不认证游戏原生分辨率、拍摄日期、商业部署build或操作/声音。当前URL与2003发表页面的同一历史字节关系未由2003时点文件SHA独立证明。

## 保护、程序、验收

永久数字来源合同：`research/recovered/STONEAGE-JP2003-GALLERY-SLOTS-02-03-SOURCE-R1.json`，保留每个引用、真实HTTP URL、页面/JPEG字节数、SHA-256、图像格式和未证字段；`tools/stoneage_jp2003_screenshot_slots_2_3.py`支援重复真实取源/本地合成测试，`--check-published`校核源报告原SHA与无证边界。专用CI既有8项模拟测试，另4项报告变异拒绝；有真实HTTP原件时还严格要求实际响应URL及完整解码。**公开 Git 仅保留代码、派生JSON及文档；不保存原HTML/JPEG/像素或版权图**。GitHub Actions的临时工件只保留派生 JSON。

首轮 `40883950720` 因Pillow JPEG无`n_frames`属性，8测试4错误、外部取源未执行；现改为`getattr(...,1)`并如实保存失败。随后 `40884309567`、`40884459116`均实际取源成功，旧失败不改为success。候选PR与主线CI/正式合并须依据最终实际后验，不能由本文预支。

## 游戏行为缺口和止点

本包确实增加两张开发图集原文件的可核来源，但**没有**提供新的TW1服务端脚本、原宠物主表、原商店交易、原客户端启动、原声事件联动或可行走世界。原版可操作世界仍未进入，Stage A7PARTIAL+2OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent=null。

**下一门槛**：在能直接访问原JPEG时用版本标签和文件SHA进行有限目视，最多描述具体看见的界面；没有合法原件/目视通道时，停止在这两个位置，不续扫15/约40图，返回22域的原本体地图/战斗/宠物实物内容。最终现代新游戏仍默认简体中文；日服图中文字不覆盖中文原文及来源版次。
