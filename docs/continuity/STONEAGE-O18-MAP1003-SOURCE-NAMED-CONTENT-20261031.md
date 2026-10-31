# O18：同保存版1003服务端原地名、客户端图层和三处NPC原资料（2026-10-31）

## 可核准的同一载体字节
承接已合并 O17 main `1192fbbc5e4c766f6af206cff773da45d1901387` / tree `703bd8847358101ead11770b29c9539aeda0ad6a`。完整私存 `stoneage-preserved-mixed25-original.rar` 361255180B/SHA256 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5` 本轮重新整包哈希。另从此同一个 RAR **实际读取**四项新增原成员（而非网页/同图号猜测）：

- `stoneage2.5/map/1003.MAP`，1808B，SHA256 `f9597ba0cfdf9d77176e0fab6058de99b9b07932c18fa2058a477e344c9fcec0`。它的二进制数值未证语义，不擅称原碰撞或地形第三平面。
- `gmsv/data/map/sainasu/samugiru/1003`，3644B，SHA256 `d297801034864d09f52e76d20b7c71137b9330f28ef7be90b931705f94d60567`。LS2MAP 原头44B，big-endian 1003、30×30，CP950 原名 **「薩姆吉爾的寵物店|0」**，严格往返相同。内含两片各900个 big-endian u16：与同RAR/O17已读客户端 `1003.DAT` 两可见小端平面 **900/900 + 900/900 完全相同**；证明这个**保存混合版载体内部**真实地图/名称/图形值对应，不证明2003官方部署/TW1初代。
- `gmsv/data/npc/genout/msg_1003_16_13`，220B/SHA256 `a96b0aa7dc09abde9ab2ff872f5fdc38255ef6e78ec2054ae95fa0244b9170a5`，原 CP950 确认，为宠物属性、教养等原静态讲解候选，源文件名中的16,13不是已认证可互动NPC实例。
- `gmsv/data/npc/genout/ps_1003_12_13`，397B/SHA256 `f4759c08d7391033b8fcee4d2580832c77e8210d637009b608be460b51285cbe`，原文本13字段包括 `nomal_rate`（保留原拼写）、`pool_cost`、`pool_flg` 和买卖/寄放提示；仅静态数据，不证明真实交易、价格公式或执行。
- `gmsv/data/npc/genout/psks_1003_18_13`，105B/SHA256 `c4063d4fe350ff3b1ed4638e72f62f919b229e042112c0f6e7aec7af24e41558`，原字段 `skill_rate`、`main_msg`、`pet_skill`；不能宣称原技能教学已可执行。

三段原文件经 CP950 解码/原字节往返同一；没有取得运行时原 create 指针/已触发的 NPC、对话或交易事件。同一 mixed25 保存档拥有客户端与服务端内容，不等于已经证实这些文件来自一个被运营商实际上线的同构建，也不能把后代「宠物店」或本服文本倒写到2003玩家稿、台湾1.0/JSS1999官方版本。

## 原资料保管和独立性
私人 ZIP `StoneAge-O18-private-map1003-server-name-and-NPC-source.zip` 3724B/SHA256 `892bf7f282e38978abfa9c5f976e715bed78a3b009d24f461b7de6a0b47c1578`，7个内部成员（含已保存原DAT、原服务器地图、原MAP、三段原文和生成时元数据）；7成员ZIP CRC 和原地图/三段原文回读一致。原 CP950 全文/服务器地图字节不入公开 Git；仅上载数值源合同及hash、负例和文档。CI 只能验公开派生事实；原始字节是私人工作区中实际抽取/复验，不冒充原生游戏播放。

## 有界下一步
**NEXT O19-1003-ONE-NPC-CREATE-POINTER**：只追 `ps_1003_12_13` 这一个有同版文件名坐标和原参数的创建引用，查已保存的原 NPC 创建配置、起始行为或明确缺源；若源创建未发现则止点回22域，不无限扩NPC/交易/helper。原原版世界仍未真正进入；Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79暂停，overall_percent=null，版权边界不变。O17 的全图/图号证据和既往 CURRENT 完整保留。
