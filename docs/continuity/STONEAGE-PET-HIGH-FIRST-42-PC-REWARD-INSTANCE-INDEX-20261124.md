# PET-HIGH-FIRST-42｜奖励编号的同载体实例解析（原件复验完成，候选验收）

主线 `a320a197da3a7813d26925dd4e3228cadb9156eb` / tree `b9131178503d1f864d629a4b582c44eb6887b18b`，42/42 Actions 成功，无未合并PR。历史CURRENT仍2,709,173字节、blob c89e0e33537990aa2132b47c40fef49a985a935c。仅PET。

[36个实例的派生索引](../../research/pets/PET-HIGH-FIRST-42-REWARD-INSTANCE-INDEX-R1.json) 从已验INTEGRATION05、PET10、QUEST01原派生记录逐行重接。同源RAR SHA256 d71e2e6766e8eac9f3fd1a8d3ab910b4b903daaf5f26f4077f07660d0102faa5，23个脚本SHA逐份与QUEST01匹配，两个主表SHA与PET41实读成员匹配。24个CREATE引用／23脚本／25 GetPet指令行／40数字出现（按不同脚本去重，保留同列表重复）。36不同实例全部唯一连接36模板及36图号，全部模板PETFLG=1；33图号对应既有TW1客户端名候选，3图号没有TW1候选，独立保留，32条与旧指南确切模板+图号相合。实例标记、等级、同版实际发奖在本派生索引中不补猜。

|取得线索|原奖励实例号→模板号|原脚本与楼层|
|---|---|---|
|卡坦鱼／鸟|93→171 修寶；341→274 朵拉比斯|seimu/event/event02_1，100，两ACCEPT块|
|SOT C|48→73 多薩金格，94→172 卡搭寶斯，350→301 奧卡洛斯，482→175 布魯寶|sainasu/event/oev_edc，1000|
|SOT D|76→142 奇拉頓，309→193 格魯西斯，361→324 達伊諾洛斯，96→174 多洛加|sainasu/event/oev_edd，2000|
|JOT A|358→321 史多拉奇頓，96→174 多洛加，328→243 海主人，309→193 格魯西斯，365→333 可利多洛斯|jaruga/event/oev_ed1，4000|
|JOT B|338→271 帖拉格恩，360→323 阿利給洛斯，366→334 諾斯多洛斯，482→175 布魯寶（出现两次），78→144 格爾格|jaruga/event/oev_edb，3000|

SOT/JOT四脚本的多值GetPet均处于MESSAGE块；不能从配置推定实际发奖或随机概率。其他21个GetPet块为ACCEPT，也不证明执行。2001指南SOT D南岛标签和2003北岛说法不强行统一。初始索引本身未读新原件，现已另行完成原件复验，见下。后期源码用于语义参考，原部署资格仍OPEN。

## 实读补证与独立保全

首次源运行 [45419117341](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45419117341) 因setup路径前缀断言过窄而失败，保留日志，无派生物。修正为与PET41一致的文件后缀检查（提交5584efae27ccd4b9da64fedf4e8934ae7b084d22）。[成功源运行45419861471](https://github.com/chinaneedM/stoneage-rebuild/actions/runs/45419861471)，job 138536105158，artifact 14931969878。184个HTTP206区间、12,013,836字节，7954归档头；26份原成员按R18原SHA256/CRC复验，未重取整包。独立下载ZIP 16905字节，SHA256 f886b0b1fcad267bac5b338dbb8e3b848bc0b9cdd64e10c9d9ea37170ca998cf，与API相符；原JSON 82025字节，SHA256 d0139127c20357f051ceb45390bb2185d5d8ea9972677ac864337cdfde1ab4a0，独立日志重建与下载原JSON Git blob 同为779077c98b745f6045733d4ba1410768e989f73e。[原件派生](../../research/pets/PET-HIGH-FIRST-42-ORIGINAL-MEMBER-REPLAY-R1.json)。

36实例等级区间均[1,1]，实例及模板宠物标记均1；23份脚本25个原GetPet行和40个数字原序一致。四处实例别名与模板名不同，保留两列。卡坦鱼鸟原配置：修寶93要求LV>0、25-221*1及25-222*1、ITEM2607、NOWEV35，删除所列宠物与道具；朵拉比斯341要求LV>0、两种PET组合（25-558*1及25-293*1，或25-292*1及25-293*1）、ITEM2607、ENDEV35，DelPet:EVDEL。旧玩家记载的四只鱼／鸟与此保存配置不一致，保留两个来源，不强行补齐。条件编号的具体宠种、实际消耗语义、原首发及官服运行尚未证。四组SOT/JOT MESSAGE分别以2564/2587道具和部分ENDEV门控；后期固定C源码NPC_TypeCheck的MESSAGE+NomalMsg分支可调用NPC_AcceptDel，其GetPet处理进入NPC_EventAddPet。不能因为MESSAGE就判定仅显示；本轮未确认每个脚本NomalMsg内容及同一部署执行、随机权重，重复482仍保留。

## 高版本候选的独立归档

[模板指纹交叉表](../../research/pets/PET-HIGH-FIRST-42-EXACT-TEMPLATE-CROSSWALK-R1.json) 36/36与标称7.5版2012公开保存表中的模板ID、图号、行字段SHA256相同，原名一致；这是共享行证据，不是独立官服双证。33个TW1图号候选中31个模板名相同，两例异名（卡拉寶斯/卡搭寶斯、愛麗兒隊的加美/加美）保留。3个不在TW1图号档内的后期候选：瑪蕾菲雅718/100451、迪歐719/100401、魯烏720/100432。均接入现有标称7.5查询行，不新增查询位置、不计新物种。TW1仅来源链接。无需回低版强找身份；未证图鉴像素和实际发行。

**NEXT PET-HIGH-FIRST-43：** 从已证卡坦交换条件的PET编号语义、221/222/558/292/293配置来源与道具2607入手（先复用已存原表和指令代码），确认交换宠种及等级与消耗边界；再用已有任务奖励脚本索引继续SOT/JOT MESSAGE实际触发和随机选择语义，不能把保存版反投历史官服。只有缺字段才实读原件。若存在未验收PR先验收。PET唯一，Stage A7 PARTIAL+2 OPEN，Stage B/wiki GATED，R79暂停，整体未知。
