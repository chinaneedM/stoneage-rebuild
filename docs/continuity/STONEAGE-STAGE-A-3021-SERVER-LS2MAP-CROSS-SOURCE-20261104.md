# Stage A｜3021 服务端 LS2MAP 双来源字节资格校验（2026-11-04）

**性质：来源隔离负例，不是新地图复原。** 本轮从远端 `main` `c4bbd2a2348803691a4a4431fd46993e859a917b`／tree `6a632d6e0f260b1d9b3af9ec351b30f66a844625` 重新按连续性协议启动；已核 `docs/CURRENT-STATE.md` 原 Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，不改动其全文。承接 [原RAR有界重读](STONEAGE-STAGE-A-ORIGINAL-RAR-BLOCK-REPLAY-20261104.md)及 [四层DAT缺件审计](STONEAGE-STAGE-A-ORIGINAL-DAT-SOURCE-GAP-20261104.md)，只检验“别处同编号服务端地图能否替换本次解包失败的成员”这一实际资格问题。

## 原RAR服务端候选

从用户私人 Library 实际重新取得 `stoneage-preserved-mixed25-original.rar`，大小 **361255180 B**，本轮完整 SHA-256 再算为 `d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5`，同原 MAP01 来源。RAR4 共7952目录成员；与客户端 `stoneage2.5/map/3021.DAT` **不同**，还存在唯一一条服务端成员：

`SA2.5服務端/gmsv/data/map/jyaruga/jaja/3021`（省略RAR根前缀）。

该成员的原 **RAR头**声明未压缩长度 **234476 B**、CRC32 **`5d7be038`**、压缩长度2822 B。再次用本环境 libarchive 读取时仅产生 **196608 B** 后返回 `File CRC error`；不足整长且无匹配CRC，**绝不能当作已经恢复的原LS2MAP**。这是同一 libarchive 实现的又一次有限实际尝试，不是独立RAR3解压器验收。私人原字节与失败输出均未公开。

## 独立公开保存来源：名字和长度相同，校验值却不同

另一公共研究源 `chenmingbiao/stone-age` 的 `gmsv/data/map/jyaruga/jaja/3021` 当前 `master` 对应 Git blob **`e34245c7ed4346f863e1b3ed17a8beb464b673f6`**，可固定访问 [GitHub blob](https://github.com/chenmingbiao/stone-age/blob/e34245c7ed4346f863e1b3ed17a8beb464b673f6/gmsv/data/map/jyaruga/jaja/3021)（**此链接使用对象 SHA 而非提交 SHA 时不可用；可使用下列 API 内容寻址链接**：[Git blob API](https://api.github.com/repos/chenmingbiao/stone-age/git/blobs/e34245c7ed4346f863e1b3ed17a8beb464b673f6)）。

本轮通过 GitHub 连通接口读取该 blob 的**完整 base64 字节**，实际解码 **234476 B**，起始 ASCII **`LS2MAP`**，按全部字节重新计算 **CRC32 `8f4aaf0e`**。其来源属于第三方历史后代资料，未认证为当年同版同部署正式服务器。

| 校验字段 | 私人混合2.5 RAR原成员头 | 公开后代源完整Git blob |
|---|---|---|
| 相对路径 | `gmsv/data/map/jyaruga/jaja/3021` | 同名 |
| 预期/实得文件长度 | 234476 B（仅RAR声明） | 234476 B（**完整实读**） |
| CRC32 | `5d7be038`（**RAR原头声明**） | `8f4aaf0e`（本轮实算） |
| 该来源完整字节可验 | **否** | **是，仅对应公开blob自身** |
| 能否用来替换私人RAR成员 | 否 | **否，CRC不匹配** |

**结论：同名、同长度、相同LS2MAP家族不等于同一地图原字节。** 公开后代文件最多在其自身已固定来源下单独研究，不能冒充与私人RAR逐字节相同，不能代替原RAS服务器成员，更无法补齐另一路 **客户端 `3021.DAT` 351656 B / RAR预期CRC `c0d8a645`**。未把文件大小相同当作任何地图像素、碰撞、进出点或正式部署一致的证明。

原 `3021.MAP` 两份此前已完整认证相同 SHA，不会由这份服务端候选改变。既有 `recovered25` 服务端地图覆盖属于其独立后代版本来源，也不构成本包RAR完整解压成功。

## 止点与后续

本次**新确认了第二来源的真实字节CRC冲突及同包服务端3021成员的具体失败资格**；恢复原客户端DAT **0份**、原服同部署资格 **0项**、原游戏原生运行 **0次**。不制作伪地图、不跨源合并实体。只有取得通过原RAR头**全长度+CRC**的独立RAR3兼容解包结果，或具有完整来源身份并确实可比对的另一原成员，才重新打开；先处理3021，再对100/3000/200作同样实物资格检验，不沿重复解压器helper无限扩张。

Stage A仍为 **7 PARTIAL + 2 OPEN**、Stage B/Wiki **GATED**、R79 **PAUSED_NON_BLOCKING**、整体百分比 **UNKNOWN**。