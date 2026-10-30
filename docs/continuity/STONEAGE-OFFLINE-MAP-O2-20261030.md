# 《石器时代》O2 原图地图离线观察（2026-10-30）

## 启动与优先级
本轮按协议核实远端 main HEAD 0a715fedb94223d2e223ba5cdf16fec744678718、tree ae1dd87bf525c0e70e072098d2c874ba6856e5b9；CURRENT-STATE完整blob 20050acf279a01555ab06a381dfcdc936bd381a6、2708031B；旧文件仍保留，接口返回空字符串不表示文件为空。最新Actions 41057028958 为 completed/success。本文件为增量续接，不覆盖大CURRENT。
最新用户优先级以单机原客户端素材观察优先，已取代旧SCENE44网站搜图；当前任务 OFFLINE-CLIENT-SAME-SOURCE-MAP-SCENE-O2。原版客户端联网、旧私服和Windows驱动并非前置条件。

## 证据与版本隔离
- 台湾TW1原零售文件中还未找到可认证的同版1000.DAT世界地图：SCENE30审阅旧文件库存不等于找到原地图，原生TW1地图身份仍OPEN。
- 现有SCENE21的1000.DAT来自后期保存mixed25文件，而不是认证的官方台湾1.0部署。现有独立源报告证实160×160地图中的有限77格、85次图像布置、55种地图原图号和一个NPC候选；图形资源属于TW1与mixed25已证明的相同文件前缀，不等于同版地图或原世界。
- SCENE21私有输出内有DAT、调色板、56原RD、八PNG与原图观察HTML；旧工作曾实际读原图并校验，本轮环境没有该完整私人包，不声称新执行原画、真正进入原版世界或者已认证原先调色板/碰撞/图层。原始资源仍不得上传公开仓库。

## 本轮变更
1. 新增 tools/stoneage_offline_original_map_o2.py，只读取已保存的私人SCENE21输出，用冻结公开源合同认证：报告、私有ZIP精确58条、原DAT/SAP和56个RD完整摘要、77原格与85布置、双RD解码、完整原像素索引、候选RGBA、八张完整拼合原图的PNG和像素SHA，并验证私人HTML证据及仓库模板。伪造/缺失/混版即失败，不下载、不运行旧EXE、不连接服务器。
2. 通过才在仓库外空私人目录输出原图观察入口、八PNG和来源收据。明确标记后期mixed25地图及TW1字节前缀关系，严禁声称TW1官方原世界已认证。拒绝覆盖、符号链接和仓库内原版权资源。
3. 扩展 tools/stoneage_singleplayer_observation_kit.py：增加可选 --scene21-private-dir，已有TW1原动画一键观察不变；有合格私有地图时同一入口同时查看分版标注的离线原图场景。失败回滚。
4. 新增测试 tests/test_stoneage_offline_original_map_o2.py，并扩展既存单机观察包测试与专用GitHub Actions。远端CI/合并必须以实际结果为准，不预先报成功。

## 私人运行（目录仅为示例，不代表本轮已具备材料）
先建立仓库外空目录 /private/stoneage-observation/map-only；运行：
    python3 -m tools.stoneage_offline_original_map_o2 --scene21-private-dir /private/scene21-verified-export --private-output-dir /private/stoneage-observation/map-only
或者在已认证TW1 data目录和SCENE21材料同时在场时，先创建空的/private/stoneage-observation/combined，再运行：
    python3 -m tools.stoneage_singleplayer_observation_kit --original-dir /private/TW1/StoneAge/data --scene21-private-dir /private/scene21-verified-export --output-dir /private/stoneage-observation/combined --spr-no 100000 --direction 0 --action 6
打开私人index.html即可查阅。所有原图/声音保持私人输出；没有原件时运行必须拒绝，公开CI只验源合同与合成否证测试。

## 验收边界和最高下一项
- **CODE**：源码层面新增O2有界地图桥与版本负例；实际私人O2包未在本轮环境执行，因此还不能把功能等同于新实图验收。
- **FACT**：SCENE21既有mixed25地图及原TW1图形字节前缀报告可复用，不重复搜同一来源；有限内容数不扩大。
- **OPEN**：原始TW1同版map→tile→pixel身份缺件，O2严格同源验收仍未完成；真正原客户端可操作世界、原生图层、碰撞/任务/战斗/互动均未认证。
- **NEXT**：真实拿到既存SCENE21私有包后运行并回读O2，验证实际原图八状态；如仍缺该包，优先取得精确同版TW1原地图材料并定义有界验证，不能靠截图推断或复活私服/驱动无限支线。
Stage A仍是7 PARTIAL + 2 OPEN；Stage B/wiki GATED；R79 PAUSED_NON_BLOCKING；overall_percent=null。版权、版本和旧失败证据保持。
