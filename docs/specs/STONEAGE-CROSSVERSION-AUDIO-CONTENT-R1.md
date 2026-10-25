# 跨版本原音频内容15：旧分段继承与sound3实际三重重复

2026-10-25（Asia/Shanghai）。本包交付原音频字节关系，补出一张真实地址表与完整分段元数据。没有运行客户端或播放原声音，没有从文件名推宠物叫声、村落配乐或战斗事件。

## 启动与未重复计数的旧结果

fresh远端main `9854762ef8163dd86f67982379414e9d339f8dcb`，tree `4482253ef2563da0ffdc41c8c9a3ed8469c97aee`；585分支、0开放PR、同HEAD17项Actions实际成功，无运行中。一条10-07旧BecomePig分支历史queued非本包依赖，保留。七启动文件、路线及22域组合索引按远端完整Git字节核验；CURRENT2676050B完整历史保留。本包是末条最高NEXT，不依据旧聊天SHA。

原TW1音频R1已明确114索引分段、116散装SFX、11 BGM、107/1/6同名对比和sak_91/92别名；旧全文件交集也已证明mixed25的sound_1.bin相同。这些不是新音效发现。本轮先将原分段关系实际接入后期载体，再沿已存在的小范围可读载荷补缺，没有重拉大客户端来复算哈希。

## 原sound_1的114分段可以继承，运行编号不能继承

原sound_1.bin长3695418B，SHA256 `c3398c5d9edc116c64eac35794b05274f731f07adf66ba0ef568d877f6bce270`，与mixed25实际文件清单相同。原114分段从0连续覆盖到3695418，无遗漏/重叠；因此其字节位置和分段摘要在mixed25同字节文件中也成立。原table编号/文件名只标作TW1来源，mixed25实际播放编号和文件名保持null，不能因文件一样就认定加载同一张表。

114原出现对应113个不同完整WAV块；109和113是相同字节，但两个原位置都保留。原116散装SFX按所有已知分段匹配，而不是只按同名，得到：

| 与继承分段的关系 | 原散装SFX数 | 含义 |
|---|---:|---|
| 完整WAV字节相同 |109|含sak_91/92分别命中原37/38，不把散装01/02的不同版本替换进去|
| PCM与全部已存格式相同、WAV封装不同 |1|sak_09a.wav对应45，仍是不同完整文件|
| 没有完整WAV或格式一致PCM匹配 |6|只限已知分段集合，不能推在其他载荷绝不存在|

mixed25的2302个实际客户端子树文件中，没有原116散装SFX或11 BGM的完整文件匹配，也没有原soundaddr_1.txt；不能因此称声音被删除，容器内字节和独立路径是不同表面。BGM维持原独立文件空间，没有人工配出sound_1编号。旧容器两样本228次分段引用，逻辑7390836B/不同块3691390B；3699446B是重复分析预算，实际原件删除0B。

## 新取得原件：691B地址表指向898978B，容器却是三份相同段

资料审查发现CN5/TW8.5原清单也有同SHA的soundaddr_3.txt。实际取源只读取既有Stoneage-5光盘载体中的CAB前8MiB逻辑内容；对应原始扇区HTTP206范围为`65856–9699647 / 733057248`，不是整个733MB光盘或612MB CAB。逻辑前缀SHA256 `87973df39afea068021d64a71fc9fb4f290cc0d7447fd3fae6beeea2bdb3c937`，稀疏文件的逻辑长度不能称为已下载字节数；全光盘SHA1没有重新实算。

只解出两个成员：

| 成员 | 实际长度 | SHA256 |
|---|---:|---|
|soundaddr_3.txt|691B|`5afc6a80352d5254c926129e4acdd023cabdc9e67e5f8cf5bf824520ea2be5e7`|
|sound_3.bin|2696934B|`f5c0b5b0bf3dc7e010c3cde867536929b1f51d81a7ace5ff30d143ccff33b148`|

地址表实际27行，文件名saam_01.wav至saam_27.wav，offset/size连续到898978B。原容器依次在0、898978、1797956各有一份完全相同的898978B字节；三份逐字节相等，SHA均为 `32906404a97609aab90f5c22ae57e0619aeac820cac1f965ca2bf1d631c3ec94`，恰与mixed25较小sound_3.bin全文件SHA/长度相同。

因此此前“同名容器898978与2696934B不同”现在可以解释为实际三重重复，而不是擅自推音质升级或81个新增声音。表只直接指向首份；额外两份54个位置不被这张表直接寻址，但没有证明运行时从不读取它们。81个物理WAV位置全部保留，27表项对应26个不同WAV块；表14/15（saam_15/16）同为5362B、同SHA，未因去重删除任一表项。

全部实际分段均为有界RIFF/WAVE PCM，单声道8bit。采样率原值为11025×1、22000×13、22050×9、22255×2、5564×2，未修正成惯常采样率。27行与TW1的114索引、116散装SFX和11 BGM都无完整WAV或格式一致PCM匹配；这是固定原样本的字节/格式差异，不是27种新宠物、27个游戏事件或官方首发归属证明。

同SHA表和完整容器的旧实取文件摘要，将新27行关系有据转接到CN5、TW8.5保存样本；mixed25按单段完整文件SHA转接。这三样本分别有27、81、81个物理位置，但均只有27个表项。来源仍为保存载体，各自没有被认证为纯净官方压盘或同一已部署build。后两份容器字节的重复原因、实际可选声音号、调用事件和配乐场景保持OPEN。

## 独立验证与永久保管

本地通过libarchive3.7.2静态解CAB，另以标准库wave逐一读取81个物理位置的帧格式/PCM摘要；没有播放。独立源Action **40188767159/job121155060294**，HEAD `ef49fef9540b8a332df55be94bbabd69065bc168`，使用cabextract重新有界取源/解压，实际completed/success，两个成员和完整派生JSON逐字节cmp相同。原取源、格式审查和清理步骤均实际通过。

永久原派生报告`STONEAGE-SOUND3-ORIGINAL-CONTENT-R1.json` 21230B，SHA256 `ed5d9387a6f8e70da5ad269fc9fa46f8ad5d0b6e0aaf25e3b6d969fe2e1934d0`，Git blob `4339a0229176c88628a17af64da816c927cc1ce0`。保管链见`STONEAGE-SOUND3-ORIGINAL-CONTENT-CUSTODY-R1.json`；没有临时ZIP工件，不伪造ZIP摘要。只提交数值地址/文件名/格式/哈希和参考关系，原表正文、原WAV/容器与程序均未入Git。

综合报告`STONEAGE-CROSSVERSION-AUDIO-CONTENT-R1.json`固定7份派生输入，覆盖114旧分段、116散装、11 BGM、新sound3原表及三载体绑定。内容候选/main仅离线重放；源工作流限制在专用source分支，避免主线反复取原件。22项集成测试、6项新原件结构负例、既有6项音频/清单测试和30项Stage A边界检查合计64项通过。本包后验CI另据实际，不预支成功。

```sh
python -m tools.stoneage_crossversion_audio_content --verify
python -m unittest tests.test_stoneage_crossversion_audio_content tests.test_stoneage_sound3_original_content tests.test_stoneage_tw10_audio_metadata tests.test_stoneage_tw10_preserved25_file_intersection -v
```

## 止点与下一项

音频本包已有实际原内容与跨版集成，止于此；不扩WinMM/驱动或一般播放器helper。只有同版原执行体明确的声音表选择和具名事件依赖才重开运行时链。私人大包保管仍暂停；本轮有界前缀为补原表/内容，未拿它冒充全包长存。

最高NEXT **ORIGINAL-CHARACTER-CREATION-CONTENT-16**：优先原TW1人物创建body选择基表与已存CreateNewChar输入/464组SPR的同版关联。先排除旧登录/选角及R101动画规格已覆盖项；只取必要原exe字节（可用有界读则不下整盘），最多交付一个有真实表界限/值的外观键联接，或精确缺源即止。JSS2001的12类48外观不直接回填TW1角色数，不扩所有写入者/通用helper树，不造名字或宣称实际画面运行。

DD-028四任务档、Stage A7 PARTIAL+2 OPEN、Stage B/wiki GATED、R79 PAUSED_NON_BLOCKING、总体percent=null保留。


## 音频15实际内容主线终验

内容main3049018051f858e7bc218d9ccde71882ba3ee7c4/tree70a30042e3e65463e203b755e583852506226db1，候选11项、主线12项Actions实际全部completed/success。原件源40188767159/job121155060294独立有界复取/cabextract与本地libarchive结果同字节；内容候选离线40189279082/job121156600160及主线40189337392均通过22项集成测试、7源全表精确重放。主线未重取原载荷。本地64相关检查、标准库wave81物理位置、独立SQL417跨样本引用/139不同块全部成立；13683682B逻辑引用/4585006B不同块只是无损分析预算，原件删除0B。15上传路径逐blob、远端tree、报告/源收据全文回读同本地，五份历史完整前缀保留。源/主线实际作业和所有派生SHA/blob见STONEAGE-CROSSVERSION-AUDIO-CONTENT-PUBLICATION-R1.json，无原声音或ZIP工件。该后验提交自身Actions另据实际观察；最高NEXT人物创建同版body表/SPR关联16和全部边界不变。
