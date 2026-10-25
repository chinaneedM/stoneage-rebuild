# 2026-10-25｜CHARACTER-CREATION-16原始数值材料续接

这是对约2.68MB的 `docs/CURRENT-STATE.md` **追加式日期补记**，不替换原本体或旧失败/验收记录。每轮仍以新读取远端main/完整CURRENT/RESTORATION-ROADMAP最高NEXT为准；若后续MAIN超越本补记，后者不具有优先级。

本轮启动远端main HEAD `fa97b026893e8285f619ee907af60c55aaaff85a` / tree `eb3170e2481533e9c525c8ff46c1e7069ff5a26d` / commit `docs: preserve actual source and main acceptance for audio content integration`（2026-10-25T11:35:05Z）；主线此HEAD多项Actions实际success。检查原Git树5749条（不截断）；CURRENT blob `031c76a5a8e431f646853909bb2f2e11e6328cd2`、2680510B；普通读接口空正文，改原生 `fetch_blob` 阅读完整约230万字符与尾部真实 NEXT16，**没有任何缩减/覆盖旧历史**。Protocol、README、设计决定、历史年表、来源登记、Roadmap `c11eff237a8aaa1cc34488a6c3c7fcdd596f9ce2`、NPC09 overlay 均已重读；最新路线末条与CURRENT NEXT一致。

最高原任务 `ORIGINAL-CHARACTER-CREATION-CONTENT-16` 已完成一项带原客户端物理字节的同版本SPR材料关联，详见 `docs/specs/STONEAGE-TW10-CHARACTER-CREATION-BODY-SOURCE-R16.md`。真实源run40195712866/job121175972333 success，原始衍生ZIP1670B/SHA256 368a7b3ed200f5164835e1ac68ca50c3e67eb32ac712fa0438c4f4faadfa5e6c；唯一原派生JSON12876B/SHA256 03be7a2c14f71c96c8114156c7189d836d99b805895510edf453ae9f706d7a59，永久存档Git blob4e0d8bddf6ee9e9de372b0b484d3489796007726，实际archive run40196456122 success/commit5ee3a6d213ce8ca47237bc4160f80b92782c7719。原 `sa_3.exe` SHA256 cdab9ea049a98bbc96ce93eeaa8b63c688f0c0f0ad8b3183e79d75e47621441a 未进Git。

原客户端 `RVA 71013` indexed DWORD基值 `0x458e28`，32项固定窗口的前12项是 `100000+20*i`（i=0..11，即100000至100220），全部在同版原SPR464组内；位置12原值198非该序列。原128B字节窗口SHA256 0e9687f40dae13f8b700426b44b8fcd1b5b462396541b0123464034fbb755d65，重编码与原见证一致。与此前CreateNewChar原编译体字段第3位及静态写入、R101原动画组索引作独立联接。**实际表长、角色总数、动作组与名字、图像渲染/服务端成功均不能声称已证。** 没有从2001玩家12外观反推初代人数。无地图/NPC/任务同版master新增；没有私人大包全部收齐，也未删除任何原资源。

Actions：原源40195712866、独立旧源交叉40196161564、永久归档40196456122、全源反例候选40196651280均已实际success，不能以此称历史游戏可运行。最新候选/main后续门槛以实际验收事实补充，不预支。本轮采用安全追加文档，旧CURRENT blob保留原样不动；旧导航/图片/源失败均保留。

本包止于十二个**候选数值**的原始字节/SPR联接。按协议13返回22域全局材料轮换，下一最高优先级 `OFFICIAL-NAMED-CONTENT-MATERIAL-ROTATION-17`：官方早期具名NPC/本体任务或宠物实际同版数据载体，先检查已有下载和同版原主表，再做一项有效实物审查或精确缺口，不重复大包抓取或通过网络图片臆造任务。活动运营任务/本体任务等依DD-028四档分离。Stage A7 PARTIAL+2 OPEN，Stage B/wiki GATED、R79暂停、大包私人持久保存暂停、总体百分比null不变。

### R16文档断言订正（2026-10-25）

首次含注册/文档门槛的候选Actions `40197075154`，20项中19项通过、1项失败：文档守卫要求在连续性覆层出现字面最高组号`100220`，覆层原写了等价公式`100000+20*i（i=0..11）`，未显写末项；实际原源 JSON、128B SHA、12组关联及其它校验均不变。本补正保留失败历史、显示最高号并重新跑CI，不把原先失败改写为成功。

## CHARACTER16 真实主线发布后验（2026-10-25）

- 候选初次全档文档Actions `40197075154/job121180125331` 为 **completed/failure**：20项中19项通过，仅因连续性覆层仅用 `100000+20*i` 未显写末项 `100220`；此失败事实完整保留。修订后同source元数据/原SHA的候选 `40197164435/job121180390998` 为 **completed/success**；原始源Actions `40195712866`、静态关联 `40196161564`、永久归档 `40196456122`、早期候选主验 `40196651280` 均真实success。
- 候选经过非强制快进已推至主线内容 HEAD `e1525884fb22967930143273da1cf39e4b8c8b1f`、tree `4c57a727c68bf78d877edc55d29711704f85b175`。正式 **同HEAD主线** 人物16来源/20项门槛 `40197210813/job121180530245` `completed/success`；相邻Stage A接受门槛 `40197210836/job121180530495` `completed/success`，不能将CI合格解释为原游戏屏幕或原商业服人物实际创建成功。
- 主线原生Git全部5761树项 `truncated=false`；旧 `docs/CURRENT-STATE.md` 仍blob `031c76a5a8e431f646853909bb2f2e11e6328cd2` / 2680510B；原 `RESTORATION-ROADMAP-R2.md` blob `c11eff237a8aaa1cc34488a6c3c7fcdd596f9ce2`、主 `SOURCE-REGISTRY.md` blob `ee3b2d70dabedfe02e3761b3fdb25476a79e147c`、协议blob `a064174339b7a4656efe00b4446a066fd7abf304` 均原样。原派生永久blob `4e0d8bddf6ee9e9de372b0b484d3489796007726`、12876B。所有原版权源/索引/完整档案无删除，旧R15与NPC09覆盖层未改写。
- 发布后验收据：`research/recovered/STONEAGE-TW10-CREATION-BODY-R16-PUBLICATION.json`，只记真实已完成的前一内容主线；本条后验提交本身的Actions必须以后续实际状态判断，不在此预写success。最高NEXT17与四类本体/活动任务隔离、Stage A7 PARTIAL/2 OPEN、B/wiki GATED、R79暂停、复原率未知全部保持。
