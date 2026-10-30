# O11 合并后验与未完成的主线运行记录 — 2026-10-31

## GitHub 真实源与主线状态
- 项目：`chinaneedM/stoneage-rebuild`，PR [#69](https://github.com/chinaneedM/stoneage-rebuild/pull/69)，原候选 HEAD `32134b0e207595a2d878e5474e85dea5e3056835`。
- 候选 **12/12** GitHub check-runs 于此记录检查时 `completed/success`。CI 无私人原件，只重演公开已冻结来源报告及负例。
- 已合并 main 内容 SHA `2fad0a9a1001a2ac6e0244d82417473190c9fe6a`，完整 tree `c468ca4735acec1b9d0f6c687076c1aba7dd2f6a`，父提交 `d87bd74e8e1ac16beef837f0276806433956a688、32134b0e207595a2d878e5474e85dea5e3056835`；Git 完整原 `docs/CURRENT-STATE.md` blob `20050acf279a01555ab06a381dfcdc936bd381a6` 未变。无原版权客户端/RD/PNG/WAV上传公开 Git。
- **主线运行状态未完成**：此条记录建立时已有 11 个主线 workflow runs，分别全部仍为 `queued`，成功数 0，失败数 0。明确不能写“11/11 PASS”。后续必须重新通过 GitHub 远端查实际结论，并新增真正后验收据，不能回写此历史排队记录。

## 原始来源与真正的 O11 增量
- 原台湾1.0 P3H 保存包372626292B/SHA256 `3a4854adaebef056332cdbd7b1dc1c130c571b11704e3f199f53d03aa31cba24`；原SPR帧头组464、动画39065、帧位置242085。
- 保存版三个纯数值组 100250/100251/100252 的24条action0序列与台湾1.0同数值原段按全字节SHA各一致；352原有序帧位置，保留24个数值73、24个数值10000和304个0，原始音效/事件语义都未得到确证。
- 从台湾1.0 ADRN/REAL重新独立解码并按标明的候选调色板，208/208幅画与旧私人保存PNG每一RGBA像素相等。公开原源派生审计文件 `research/recovered/STONEAGE-O11-TW1-208RD-PIXEL-AUDIT-R1.json` 只有索引位置、哈希和数值，不含RD/PNG。
- 原声73的零基候选是表index73 `sam_18.wav`；一基候选是表index72 `sam_17.wav`。这仅是数字索引候选，不能推出帧字段实际表示音效编号。不存在原客户端真实播放/角色技能/物种确认；原游戏世界仍未进入。
- 私人ZIP `StoneAge-O11-private-sprite-frame-sound-candidate-20261031.zip` 216成员，1145869B/SHA256 `a972f91257bef896a07e436727072d8341940c570386b6e9282b4e8d2892f811`；已确实上传私人Library `/石器时代/` 并重新下载全SHA相等。私人原图/音频、现代单页手动试听及真实浏览器画面不会公开。真实 Chromium 内存页面验收通过；`file://` 经 `ERR_BLOCKED_BY_ADMINISTRATOR` 拒绝，不证明用户本机双击已通过。
- 源合同加24项反例本地/PR均通过，真实浏览器没有外部HTTP，不能替换为原运行。
- Stage A 7 PARTIAL+2 OPEN，B/wiki GATED，R79 PAUSED_NON_BLOCKING，整体 `overall_percent=null`。

## 此刻仍在排队的主线工作流
- [41144089539](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089539)：Verify original same-build named-entity source gate R31 — **queued** / no conclusion
- [41144089478](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089478)：Verify original dated map110 three actual cell values R32 — **queued** / no conclusion
- [41144089470](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089470)：Validate Stage A evidence-limited review acceptance — **queued** / no conclusion
- [41144089464](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089464)：Accept primary-source TW1.0 character creation numeric join R16 — **queued** / no conclusion
- [41144089445](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089445)：Accept preserved original TW85 SPR137 full animation material R28 — **queued** / no conclusion
- [41144089439](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089439)：Verify original four village interior materials R34 — **queued** / no conclusion
- [41144089438](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089438)：Verify StoneAge R17 original battle SAB crossversion occurrence conservation — **queued** / no conclusion
- [41144089407](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089407)：Verify preserved mixed25 full server source conservation R18 — **queued** / no conclusion
- [41144089399](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089399)：Verify original local album name material and no master promotion R35 — **queued** / no conclusion
- [41144089392](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089392)：Verify original native album table and saved-name joins R36 — **queued** / no conclusion
- [41144089389](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/41144089389)：Verify StoneAge O11 native source animation and bounded sound-word candidates — **queued** / no conclusion

## 后续最高 O12
返回22域，只取能确证同一版本具体宠物/人物/动作→声音/技能/任务事件发生的原始主表、同版本调用实参或真实游戏内观察；缺原件须记录阻塞并轮换另一实际玩法域，不重复扩大地图和辅助分析。不得凭73/10000猜宠物喊叫或让私人页自动触发。原初代、后代混合保存世界严格分开。
