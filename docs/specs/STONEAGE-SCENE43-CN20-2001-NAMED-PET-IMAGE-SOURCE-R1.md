# SCENE43：华义2.0原版运营站宠物两格照片原字节取证

2026-10-30。用户要求继续历史复原，按GitHub远端完整连续性协议和现存 `SCENE43-OFFICIAL-PET-NAMED-IMAGE-SOURCE-REVIEW` 的高优先级行动。起点main `46c3421e21764c83c4a9eaa1e2c703b7fbac0d51`、tree `fc4c32675358289602152917b901e862c00e1cea`。CURRENT大文件原Git blob `20050acf279a01555ab06a381dfcdc936bd381a6` 实读完整，不覆盖。

## 一页既有官方文献，两项新增的真实图像字节

复用旧大陆2.0运营站2001-10-23 18:16:29 UTC存档 [华义新增宠物第81—104格](https://web.archive.org/web/20011023181629id_/http://www.waei.com.cn/ZHUANQU/stoneage2/pet/new_pet2.asp)。原HTML实际重新核验 **64,382B**、SHA256 `2c7aea8d0319c2070d5c7590a95bfc892c2463deb76c5b95fca8c281549c76f0`，GB18030严格可解，与旧R104同一原字节；**网页本身旧已登记，不计新来源网站**。

实际原HTML中格位/名称/图片引用须**同一个表格单元**取得：第85格（1行5列）“瑞德宝”指向 `img/newpet/84.JPG`，第86格（2行1列）“瑞里西尔”指向 `img/newpet/85.JPG`，页位置、文件编号不能混为一谈。旧R104第84/88/89格三图片完整已取得，这次均不重计。

| 网页格号／原名 | 原图引用 | Wayback图片本身捕获 UTC | 图片字节/完整SHA256 | 实际解码 |
| --- | --- | --- | --- | --- |
| 085 瑞德宝 | `img/newpet/84.JPG` | 2001-10-26 01:34:55 | **3753B** / `ba7b663a9445a0e32117eb768db33e991c566ddfac8ad1ae5d93bb7cf6372e31` | JPEG RGB 83×90 单帧 |
| 086 瑞里西尔 | `img/newpet/85.JPG` | 2001-10-26 01:30:52 | **4494B** / `9951490cc47de15342fd88e671a8e54d1c6c33c7786655af4ffe4b93300f16b2` | JPEG RGB 83×90 单帧 |

原来源回放已在 GitHub PR #57 source run `41053616995` 取回整页及上述两幅JPEG字节，来源解码工具对JPEG 83×90 RGB实际完整解码并计算RGBA全部像素SHA，图片本身、HTML均未提交或交付公共Git。归档每条原图实际捕获时间、引用路径、文件与RGBA摘要、无视觉目视声明、归属版本及限制。

注意2001-10-23 HTML引用的图片实际取自2001-10-26**后3天不同档案时点**，不能声称10-23页面原屏显示的那两份JPEG字节就与10-26完全相同。2001标签证实运营站网页关联与两份历史档案图像，并**没有**认证最初JSS1999、TW1的原客户端物种ID、同build的资源图号/SPR，亦没有恢复宠物技能、属性、生态、捕捉、骑乘动作、真实服务器选择逻辑或小游戏操作画面。**未亲眼目视新图**，因此不描述颜色和外形。

当前大陆2.0原104个**网页引用位置**合计旧已取7张＋此次2张＝9张独立参考，95项暂未取，这只是图片引用覆盖，不是已恢复宠物种数／复原百分比。另日本Hangame已实取23图属于另地区，不合计成同版物种。

## 来源链、证据门和下一项

本次单次源任务仅请求一个已证的华义原网页和2条已证 src 的Wayback目标，核对全部原字节、同表格位置、原URL路径、14位捕获时间及JPEG解码。页/图原字节**均不入仓库**，只归档`research/recovered/STONEAGE-SCENE43-CN20-TWO-NAMED-PET-WEB-IMAGES-R1.json`与2个七字段规范研究记录。8个首轮负例涵盖变字节、错格号/路径、archive宿主/时间以及HTML假JPEG/错误尺寸；冻结报告补强后重复回放，以主线CI实测结论为准。

原文页面发表日、图片捕获时间、客户端build三者是不同维度，保留所有源差异。下一`SCENE44-CROSS-DOMAIN-MATERIAL-ROTATION`停止无限续抓图片，优先关注进入真实游戏世界的上游输入通道和一条可视/可操作内容；Stage A7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79 PAUSED_NON_BLOCKING、整体percent=null与原boot BLOCKED_PRIVATE_INPUT_CHANNEL均不变。
