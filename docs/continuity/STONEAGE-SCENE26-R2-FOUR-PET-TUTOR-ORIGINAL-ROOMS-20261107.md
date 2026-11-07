# SCENE26-R2｜补齐原“宠物常识解说员”第四间真正DAT房间（2026-11-07）

## 本轮实质新交付
以 GitHub 远端 `main=38f489e57d4e460803f5d9e4d03f9001e4d4eea9` / tree `629807d2f64ef240fc6e6e8e72125c1d2b27b2ed`、最新11/11主线Actions及完整连续性协议/原 `CURRENT` blob为基线，按SCENE26受限止点专门查找原4003房间，**没有重复早已完成的1003/2003/3003三间源画面**。私人Library确实已存更广的 `StoneAge-MAP09-691-source-ready-map-catalog-private.zip`（46,844,444B，SHA256 `d84d0800dd600798769dfb7251a1d7816588ac061ccc27812ac64a37922d4a8a`），里面嵌有955件原DAT包（1,988,312B，SHA256 `c079a1c25bfa11902b69c1f2839058d4fb20f025ef15c93f649f636c7e5f833a`）；原大包4,195个成员CRC合格，内层955件原DAT成员CRC也合格。之前SCENE26只接入更小MAP07包，所以其4003缺件是**私人子包缺件而非游戏缺地图**。

本轮真正重新读取 `4003.dat` 完整5,408字节/SHA256 `0a9fa2a089b6936e86eea458bca464038b8d5cb7fee057b9d2b393ffc6c6d6d4`，与公开MAP09、QUEST05和SCENE26先前有界原索引的三处独立记录均同号同整SHA。原 `sa60/newbie/newbie.create` 第7号CREATE依然同 `petmaster`，源楼层 **4003**、`borncenter=(14,17)`、`graphicname=16122`、原方向4。**重新读取DAT对应三张900格u16平面在原坐标的真实值为 `[5002,12802,49152]`**，不是空、猜定或拿其它房间补。这个格的第二平面非零；目前不解释该值为NPC、阻挡、触发或地形性质。

## 原二维像素与现代观察交付
复用MAP09此前已核源的45幅台湾1.0原RD候选别名，不重新挖造图：第0/1候选平面总143个源>99绘图位置，画布1889×1425，参考原点(16,712)。重放4003的plane0、plane1、combined三种完整RG​BA候选画面；**NumPy按透明值拼接与独立Pillow paste逐像素相同**，且三画布完整RGBA SHA256均与已存MAP09来源收据一致，合层为 `4512cdc85c6973d775efcd1d53ada6732bf023ef559f1baa6182a7b146d3722e`。现代黄色圆点仅用投影 `(16+(14+17)*32,712+(17-14)*24)=(1008,784)` 标注原CREATE站位，**没有凭空绘制 NPC 精灵**。旧三间原DAT整SHA重新验同，旧三张有标记原图复用未重算发明。

将1003、2003、3003、4003四个源限定房间、四间对照图、原4003 DAT、两原导师配置/脚本和源指纹私有保存为 `/石器时代/StoneAge-SCENE26-R2-four-original-pet-tutor-rooms-private.zip`（2,532,646B，SHA256 `cf7d0d6dbb34fc77e64740f2d4990a0012a15a347bfb683e3cd1dc97eb02ca4c`，11成员CRC通过）。独立的四间预览图 `/石器时代/StoneAge-SCENE26-R2-four-original-pet-tutor-rooms-contact.jpg`（222,802B，SHA256 `c149529a610e08fb044b648926fd7a3076cb9c5202196d4ca051b2b3366013ad`）。两件都已上传私人Library，并再次从库独立取回对比原本完整字节/整SHA一致。

## 来源界限、验收和下一项
公开Git只保存[来源限定四房间数值图](../../research/recovered/STONEAGE-SCENE26-R2-FOUR-ORIGINAL-PET-TUTOR-ROOMS-SOURCE-R1.json)、[确定性正负例](../../tests/test_stoneage_scene26_r2_four_original_pet_tutor_rooms.py)及本说明；商业原DAT、原美术PNG和原CP950脚本不公开。公开CI通过已验三源JSON验证4003原DAT的整SHA、原CREATE创建位、45候选别名、143绘制位置、三种完整像素SHA及源分隔。**CI不拥有原DAT/RD，不独立执行3图的源字节重绘；真正独立原字节和像素核验仅是本轮私人回放和保存收据**。旧 SCENE26 基线记录中“4003没有私有MAP07图片”的历史叙述维持不变，这是一条有来源的后续补齐，不覆写旧证据。

本轮**新增真正重新实读原DAT一份、之前未连至导师的完整候选地图画面一间**。来源是后期社区混合2.5保存的DAT/CREATE与早期台湾1.0原RD候选，**没有证明它们来自同一正式游戏部署**，没有找到16122或16127同源真实精灵，不曾在原客户端/原服实际运行导师对话、碰撞或绘制。新增下载的历史新DAT=0，新增原RD解码=0，Stage A仍7 PARTIAL+2 OPEN、B/wiki GATED、R79 PAUSED_NON_BLOCKING、总体percent=null。保留完整旧 `docs/CURRENT-STATE.md` Git blob `c89e0e33537990aa2132b47c40fef49a985a935c`，不修改历史大文件。

**NEXT：** 这四间导师源房间已完成私人可视止点。只有取得原16122/16127同部署SPR/RD或准确原程序绘制/交互源，才推进真NPC画面/运行；其余没有新原件时不再扩模板/联表，转有实际未恢复原图或机制的其他高价值模块，仍为单机离线历史复原。
