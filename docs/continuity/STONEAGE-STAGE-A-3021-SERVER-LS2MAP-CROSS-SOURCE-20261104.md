# Stage A｜3021 服务端 LS2MAP 双来源字节资格校验（2026-11-04）

**性质：来源隔离负例，不是新地图复原。** 本轮从远端 `main` `c4bbd2a2348803691a4a4431fd46993e859a917b`／tree `6a632d6e0f260b1d9b3af9ec351b30f66a844625` 重新按连续性协议启动；已核 `docs/CURRENT-STATE.md` 原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，不改动其全文。承接 [原RAR有界重读](STONEAGE-STAGE-A-ORIGINAL-RAR-BLOCK-REPLAY-20261104.md)及 [四层DAT缺件审计](STONEAGE-STAGE-A-ORIGINAL-DAT-SOURCE-GAP-20261104.md)，只检验“别处同编号服务端地图能否替换本次解包失败的成员”这一实际资格问题。

## 原RAR服务端候选

从用户私人 Library 实际重新取得 `stoneage-preserved-mixed25-original.rar`，大小 **361255180 B**，本轮完整 SHA-256 再算为 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，同原 MAP01 来源。RAR4 共7952目录成员；与客户端 `stoneage2.5/map/3021.DAT` **不同**，还存在唯一一条服务端成员：

`SA2.5服務端/gmsv/data/map/jyaruga/jaja/3021`（省略RAR根前缀）。

该成员的原 **RAR头**声明未压缩长度 **234476 B**、CRC32 **`5d7be038`**、压缩长度2822 B。再次用本环境 libarchive 读取时仅产生 **196608 B** 后返回 `File CRC error`；不足整长且无匹配CRC，**绝不能当作已经恢复的原LS2MAP**。这是同一 libarchive 实现的又一次有限实际尝试，不是独立RAR3解压器验收。私人原字节与失败输出均未公开。

## 独立公开保存来源：名字和长度相同，校验值却不同

另一公共研究源 `chenmingbiao/stone-age` 的 `gmsv/data/map/jyaruga/jaja/3021` 当前 `master` 对应 Git blob **`e34245c7ed4346f863e1b3ed17a8beb464b673f6`**，固定来源为 [Git blob API](https://api.github.com/repos/chenmingbiao/stone-age/git/blobs/e34245c7ed4346f863e1b3ed17a8beb464b673f6)；该对象以内容寻址，不依赖日后 `master` 指针。

本轮通过 GitHub 连通接口读取该 blob 的**完整 base64 字节**，实际解码 **234476 B**，起始 ASCII **`LS2MAP`**，按全部字节重新计算 **CRC32 `8f4aaf0e`**。其来源属于第三方历史后代资料，未认证为当年同版同部署正式服务器。

| 校验字段 | 私人混合2.5 RAR原成员头 | 公开后代源完整Git blob |
|---|---|---|
| 相对路径 | `gmsv/data/map/jyaruga/jaja/3021` | 同名 |
| 预期/实得文件长度 | 234476 B（仅RAR声明） | 234476 B（**完整实读**） |
| CRC32 | `5d7be038`（**RAR原头声明**） | `8f4aaf0e`（本轮实算） |
| 该来源完整字节可验 | **否** | **是，仅对应公开blob自身** |
| 能否用来替换私人RAR成员 | 否 | **否，CRC不匹配** |

**结论：同名、同长度、相同LS2MAP家族不等于同一地图原字节。** 公开后代文件最多在其自身已固定来源下单独研究，不能冒充与私人RAR逐字节相同，不能代替原RAR服务端成员，更无法补齐另一路 **客户端 `3021.DAT` 351656 B / RAR预期CRC `c0d8a645`**。未把文件大小相同当作任何地图像素、碰撞、进出点或正式部署一致的证明。

原 `3021.MAP` 两份此前已完整认证相同 SHA，不会由这份服务端候选改变。既有 `recovered25` 服务端地图覆盖属于其独立后代版本来源，也不构成本包RAR完整解压成功。

## 止点与后续

本次**新确认了第二来源的真实字节CRC冲突及同包服务端3021成员的具体失败资格**；恢复原客户端DAT **0份**、原服同部署资格 **0项**、原游戏原生运行 **0次**。不制作伪地图、不跨源合并实体。只有取得通过原RAR头**全长度+CRC**的独立RAR3兼容解包结果，或具有完整来源身份并确实可比对的另一原成员，才重新打开；先处理3021，再对100/3000/200作同样实物资格检验，不沿重复解压器helper无限扩张。

Stage A仍为 **7 PARTIAL + 2 OPEN**、Stage B/Wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、整体百分比 **UNKNOWN**。


## 同日续办｜两份私人原 MAP 完整复读与公开 LS2MAP 原名、双层数据（追加，不改前述结论）

基准已按远端 `main` `ffd93298eec4156926013a950d380834e9bdb56a` 启动；`CURRENT-STATE.md` 的历史完整 blob `c89e0e33537990aa2132b47c40fef49a985a935c` 继续保持原样。本补充不是完成 `3021.DAT` 解压的公告。

1. **同一私人混合2.5 RAR中的两个独立客户端/附带工具路径 `3021.MAP`**（`stoneage2.5/map/3021.MAP` 与 `SACH-MX0.30/MAP/3021.MAP`）本轮再次经 libarchive 完整实读；各为117224字节、`CRC32=5ca00592`、`SHA256=57a230c56ab77c418101e296480f7a04ce653e0aaf0512e15050e22b335ab789`，前8字节解释为小端407×144，余下117216字节；该负载的整 `SHA256=f061a3e24c310dbffa6649e21faa2d2c8bb5950ff0d2be4cbacad1ea6362cbab`。两个原件确实相同，仍不能推出它们与缺失的三平面 `3021.DAT` 同字节，亦不能推成两份认证官方发行版。

2. **公开后代源 `chenmingbiao/stone-age`（master commit `0c58fb6683a49a178a8ad845a8c296c2cb83bd81`；blob `e34245c7ed4346f863e1b3ed17a8beb464b673f6`）完整重新读取原234476字节**，`SHA256=82e2d34062aad62673cad62c3b8d4aef7f1ffe167b83ef2d70839e5829a0dbc5`、`CRC32=8f4aaf0e`，确认 `LS2MAP` 大端楼层ID **3021**、宽407、高144、44字节头、后接各117216字节的 tile 和 object 两平面。解析方法直接参照仓库已存在的 `tools/stoneage_server_static_map.py::parse_ls2map`，未发明新格式。两平面 `SHA256` 分别为 `5e21a0e6c4f7dc7c859ac03e4db0e9c62a097d26f67e8275739bf6cd39101a7d` / `91da587f4c11db9ad8634f5c8ec28f7968dd921c74accdf477e3454dd987837b`；tile有108种数字值、15576个非零格，object有11种数字值、45981个非零格。**非零不等于不可通行、可见物体或游戏实绘**；仍须同源mapset、碰撞规则及运行验证。

3. **新可识别原文**：该公开LS2MAP的32字节内置名称字段（位置8..39）经GBK可往返解为字面 `百人联手道场|0`。将 `|0` 原样保留，不擅自解释为客户端显示名或0费用。与后期玩家资料的“百人联手道场”文本近似，仅支持此**后代资料中的来源限定名称候选**；不证明1999 JSS、台湾1.0、2001大陆1.82曾以此名称或地图配置运营，更不能证明私人RAR服务器同版。

4. **双来源不互换的直接内容边界**：私人 `3021.MAP` 的117216字节负载是小端单平面，其原顺序 CRC32 `4d5ca38f`；将每个16位数换成大端后 SHA256 `7eca9a9dcc0eebb29ac764ae23f6f7d126abdc910cbca29cd72a58fd149533a0`，**既不等于**公开LS2MAP的tile SHA也不等于object SHA。二者各自源有效，不同格式与不匹配哈希阻止静默合并；不尝试填造第三事件层或把单平面当做缺损三平面 DAT。此前公共源LS2MAP CRC与私人RAR服务端成员RAR头CRC的冲突仍成立，未取得可替换原字节。

**交付与止点**：此追加提供一份有原字节摘要、原名、图号覆盖以及跨档来源边界的紧凑证据记录；新认证私人客户端DAT数 **0**、可证明同版运营服务端数 **0**、原游戏运行次数 **0**。后续首要仍是独立RAR3兼容解压器完整提取、与原成员长度/CRC比对，或取得经来源证明的独立同源 `3021.DAT`；缺件时保持OPEN，不继续重复libarchive或扩展帮助脚本。Stage A 7 PARTIAL + 2 OPEN、Stage B/Wiki GATED、R79 PAUSED_NON_BLOCKING、overall_percent未知不变。
