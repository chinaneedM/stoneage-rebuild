# JP2005 宠物图鉴登记文献规格 R87


## R87 — 2026-10-23 JP2005 宠物图鉴的画面登记与两阶段更新

FACT：按新读远端main `cf52a0a35ea7d4f13e24b1ff17abfefd4ebb16a0`／tree `2dd6065ef8fa7c3d44f6540a385893bd3e84c54c` 启动，497分支、0开放PR／运行中Actions，上一轮最终候选10/main11实际全部成功；旧queued37642417333单列不动。八启动文件严格UTF8完整读取并比对fresh checkout原生Git；CURRENT旧全文2441519 bytes／SHA256 `27cc3dadfee0ef9794f3170f0b8645b4cede828dae8ac00d7472e6530240cc18`，无AGENTS，22域索引全文核读。按最高OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-87转具体图鉴交互文献，查JP2004展示宠物和CN2003操作已有规格，不重复计新结果。

交付 `STONEAGE-JP2005-PET-ENCYCLOPEDIA-SOURCE-CONTRACT-R1`、SOURCE JSON、专用工具／测试／工作流 `stoneage_jp2005_pet_encyclopedia_source`。只选2005日本GaiaX运营时期报道，不认证1999／TW1／CN1.82同build，也不把新作StoneAge2的Pal图鉴规则挪入。没有同版audio实参，不重开音效helper或savedataR79。

来源 https://www.4gamer.net/news/history/2005.07/20050705162235detail.html ，标题ガイアックス，「ストーンエイジ」で新ペット恐竜を実装，显示2005/07/05 16:22，署名TET。当前200无跳转17834 bytes／SHA256 `983b11f84dd9c492c4b868bc96921fecbbb582e87a6243c322c9f8ad684f06b9`，SHIFT_JIS严格解码零替换。为同期记者报道，非原样运营公告；当前字节不认证2005原字节，原更新页／脚本／精确客户端未取得。

实质规格：7月5日定期维护后补新宠及同种野外怪物图形、扩充宠物图鉴；7月12日维护后补此前未出现的Lv.1野外恐龙并改部分配置，明确新恐龙实际登场在第二次补丁后。图形存在不等于已在世界启用，不把“此前未出Lv1”扩大成全游戏首次有Lv1，也不补物种数／具体地点／刷新率。两阶段部署与事件仅为所报／所计划，不是实服执行验证。

图鉴正文明确：新宠显示在画面上→该新宠的名字登记于ペット図鑑。此句不以捕获／拥有为触发，不把名字登记当得到宠物或全属性／技能已登记；其它必要条件、全部旧宠适用、精确按钮与版面、持久化、重复处理与存储仍OPEN。7月12日22时前后GM展示为计划与约时，无精确分秒／时区；寻找GM是指南建议，不当只有GM展示才能登记。与CN2.0“曾拥有宠可拍照”的相簿描述、JP官方网页宠物目录分别存，不互补规则／不当同一UI。

实际配图只有正文链接 `/news/image/2005.07/20050705162235_0.jpg`，3371 bytes／SHA256 `81a547ca33684426e6c9b42fcace9850e543955b379d49487d2da6d276383394`，200无跳转，JPEG RGB96×104单帧完整解码／目视：浅蓝甲壳蟹形小插图、黑底，无物种名／图鉴UI；不猜_big图，不认作原SPR／动画／某具名物种，不因一图宣称只新增一宠，不认证历史像素。原HTML/JPEG仅临时保存，Git为派生研究元数据。

5条目录记录：两阶段教程＋登记规则教程＋计划GM展示教程＋未具名插图，7必填／19合法集合、game_ids空／非发行授权。三父报告及共享解析器固定原bytes／SHA256／Git blob。独立regex/entity正文逐字一致，19项真实HTML语义改写排除全部指纹门、2项隐藏／正文外反例及外围script正例通过；初始本包7tests及关联回归、源回放通过。止点一报道一实际小图，重开需原操作视频／同build脚本或具名图像／数值绑定，不靠更多匿名宣传图扩张。

NEXT：候选10/main11实际成功后永久保存双端原样派生JSON与准确run/job/artifact/ZIP/raw/blob收据，强制保管链校验并再验收。最高后续 OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-88 优先早期具名人物/NPC对话或具名宠物属性的原始证据，不连扩匿名插图或奖励宣传。阶段A仍7PARTIAL＋2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING；无整体完成百分比。


### R87 内容双端实际验收与永久派生保管 — 2026-10-23

内容提交 `7c734e08fc53540045063816409484c8133732df`／tree `8cc44097da5c022ef12e488ec72156411b1b7e7f`，候选10/main11共21个实际Actions全部completed/success，专用日志初始各7tests成功。

candidate: run39935988520／job120355531891／artifact12494111171，ZIP2720 bytes `sha256:0179f8b274a1003612b70f36cab4355ecd3fb257c7d731fcdf8642c8ed8169a4`；原样JSON10170 bytes SHA256 `c1f6ba1456c16a9cd5479deb43456d00e14f03e10c2f352eb13451ea32fdaaa5`，Git blob `b0142336c98750fc831b753179c7a23e5e3d56e1`。

main: run39936177726／job120356148265／artifact12493847454，ZIP2720 bytes `sha256:d65293c7d90e418f886c28c56698424e73bbc5d4d89c3c1fb8ec65f8f5c3815d`；原样JSON10170 bytes SHA256 `c1f6ba1456c16a9cd5479deb43456d00e14f03e10c2f352eb13451ea32fdaaa5`，Git blob `b0142336c98750fc831b753179c7a23e5e3d56e1`。

双ZIP已实际下载核GitHub长度与digest，唯一成员replay.json；候选/main/初始local的原样JSON与两个实际输入bytes/SHA256一致。双原CI派生JSON及CUSTODY永久入Git，原HTML/JPEG不入Git；7份证据pin固定SOURCE、三父、解析器和双原报告bytes/SHA256/Git blob。收据与代码常量锁定完整七pin清单摘要，反例同时改证据与重算receipt pin仍拒绝；收据锁定21真实run清单摘要、准确双run/job/artifact及ZIP摘要；CLI强制保管，拒绝缺失/等长篡改、run/job/artifact替换、遗漏/重复/复用工件、虚报原输入相等及历史/本服权威抬高。第8项专测还拒绝插图指认物种、图鉴实际交互已测、名字登记等于获得宠物。保管候选及main自身仍须实际后验；原内容CI7tests历史不改称8tests。

交付为文献中的画面显示→名字登记与两次更新范围；没有运行原服/完整图鉴数据/宠物原属性或UI画面。最高NEXT OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-88优先早期具名人物/NPC对话或具名宠物属性，避免连续匿名插图/奖励宣传。Stage A7PARTIAL+2OPEN，B/wiki GATED，savedataR79 PAUSED_NON_BLOCKING。

R87保管门本包8项／关联24项本地测试成功；CLI原输入回放与初始输出逐字节不变。完整七pin身份摘要另固定在代码常量中，连同篡改证据后重算收据pin的反例一起通过。
