# PET-HIGH-FIRST-44｜四组任务奖励窗口（原件复验完成，候选验收）

恢复远端PET43 main `7486d51627ab97cc8dabf45e7f743f70e26e8fc3` / tree `f033655a501622f09147bf8106b997ea9c345262`，42/42 Actions成功。历史CURRENT仍2,709,173字节/c89e0e33537990aa2132b47c40fef49a985a935c，不覆盖。PET唯一。

## 四原件窗口与奖励槽

|组|脚本|窗口物理行|窗口值字节|宠物槽|独立宠物实例|道具槽|
|---|---|---:|---:|---:|---:|---:|
|JOT A|jaruga/event/oev_ed1|14|135|5|5|10|
|JOT B|jaruga/event/oev_edb|16|135|6|5|10|
|SOT C|sainasu/event/oev_edc|14|119|4|4|10|
|SOT D|sainasu/event/oev_edd|23|120|4|4|10|

四个MESSAGE块全部恰有一个NomalWindowMsg，无NomalMsg、NomalWindowMsg1或其他编号窗口字段；JOT两主窗口值散列相同。19宠物槽（15独立实例，18逐任务不同实例关联）与40道具槽全部按原序保留。JOT B的482两槽，SOT D和JOT B的随机道具68两槽。条件、DelItem、GetPet及GetRandItem与PET42/43一致。没有发布原对话文本。

固定后期PC代码 gavinlinasd/StoneAge @ 1f90cb6cb57c1df70f39cde77a5a8ccd98b66c56，npc_exchangeman.c blob 5d74290ed6f27163e0698b4375d5dc5e187c77c4：367–475 主窗口无后页走直接NPC_AcceptDel，2342–2440另有_NEWEVENT回调条件路径；3210–3217先GetPet，失败则返回；3279–3291后GetRandItem、再GetItem。随机道具返回值未在该调用处检查，不能说二者总是同时成功；列表独立取槽，不证明统计独立。原同载体可执行代码未证，不能推断真实官服概率、发放或首发。四组仅LATER_DIRECT_ACCEPTDEL_CANDIDATE。

## 来源保全

首次45424622075因函数断言截断到3468行失败；修正至3477行，候选2ca4db0fd6d2bf3a43db0165701246006baa37d4。[成功源运行45424732486](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45424732486)，job 138553489933、artifact 14936082779。7954归档头、184段HTTP206、12013836字节，4原成员逐件SHA/CRC与R18/PET43一致。独立下载ZIP 12408B，SHA256 02d177f1153d51e75c30d470de957efbd6640f8e1e83d51b7e3f86ffeafa9df1；JSON 47046B，SHA256 78b37e07efff1ab28ab997b6b28321bd43bb62cf9b3cc622845dbd38980e2dfc，日志重建的数值键按Python原整数顺序排序，Git blob与ZIP原JSON同为bc531842c068154e40b50658092fe553ff6173df。[派生证据](../../research/pets/PET-HIGH-FIRST-44-ORIGINAL-WINDOW-REWARD-R1.json)。

统一查询仅链接已有奖励实例对应档案，TW1图号候选和标称7.5共享模板仍按R42资格标注；不增加物种、正式发行或全字段认证。

**NEXT PET-HIGH-FIRST-45：** 复用既有INTEGRATION05任务图、PET10原服务端派生表、PET41捕捉候选与R32查询，按后期高版本独立模板为主批量核对尚未链接的野生捕捉/任务取得路径；先量化未链接记录、来源覆盖与冲突，再只取缺失原字段。优先保留有明确地图/楼层/实例等级/宠标志的源链，不强求低版同名。不得重做已验PET42–44或跨模块。若有未验收PR先验收。Stage A7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停，整体UNKNOWN。
