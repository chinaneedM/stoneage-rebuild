# 台湾1.0物品静态图候选与原始消息 graphic_id 字段核查

2026-10-18。有限工作包 `TW10-ITEM-STATIC-BITMAP-SOURCE-SELECTOR-01`。起始远端main `c8a9cb702e7aae3bd8e756008d4f88d31deed7c1`，tree `24331cdb040740856a3db7f2c5ba09c2b87cc816`，同HEAD已有9项主线Actions SUCCESS。此前已证台湾1.0原SPR动画引用玩家所谓“物品图像”5973—7003号段**0帧**，不能因此说原游戏不会显示物品图。

## 可认证的真正原版来源

`STONEAGE-TW10-GAMEPLAY-SCHEMA-R1.json`、原版回调源码派生指纹`STONEAGE-TW10-GAMEPLAY-CALLBACKS-R1.txt`及原台湾1.0原光盘ADRN数据不是后代游戏建模。原回调定位：

- 完整背包：`S:I` 20个槽，每槽9字段，第5字段是按早期谱系命名的 `graphic_id`，原编译客户端分派RVA `0x30922`；该位置直接观察，名称语义是早期谱系。
- 增量背包：`I`消息10字段，第6字段 `graphic_id`，回调RVA `0x325f0`。
- 地面物品：`C`记录6字段，第4字段 `graphic_id`，回调RVA `0x31260`。

这三处仅证实接收消息*相应整数位置*及已有的谱系解释，**没有取得真实原服务器下发的graphic_id值、此值是否直接等于ADRN bitmapno、客户端转写/缓存/绘制使用函数或实际屏幕**。

## 本包新增原盘静态元数据交叉检验

`tools/stoneage_tw10_item_static_bitmap_source.py`逐一读取原台湾1.0已封存ADRN-R1压缩索引，并交叉玩家2001年`stonepic`静态图片候选区间：NPC、物品、魔法、宠物相片、UI。对于各区间，独立计算位图ID存在性、宽高、偏移、RD标识、原派生图块SHA256唯一性及前五份指纹。作为**源元数据**保留，不写入原像素、原服务端数据库或重新拼图片。

`stonepic`的原页面由现存迁移页提供；它对各范围的“NPC/物品/魔法”用途解释仅为历史玩家标签，不因ADRN数值一致而升格原版客户端实际用途。即使有1031个不同位图号，也不能推得台湾1.0存在1031种不同物品。若某个bitmap没有被SPR帧引用，只能得出“在这一帧表无记录”，不能排除静态绘图途径。

**本包停止条件**：物理ADRN静态段完整元数据可验收、原三消息字段位置可验收、无可信绘制selector运行实参时，标记 `BOUNDED_ORIGINAL_RESOURCE_METADATA_AND_PROTOCOL_FIELD_JOIN_OPEN_DRAW_SELECTOR`，不反编译出一个猜测值、更不照搬后代服务器物品ID。只有可归属的同版原始客户端调用链、原服务端确切graphic_id实例或同步可验证的物品画面能重开“物品实体→图号”真正映射。

**下一项**：`TW10-MAP-CONTENT-ORIGINAL-RESOURCE-BOUNDARY-01`，转原台湾1.0原盘地图块/地图读取结构的具名内容边界，优先实际同版可恢复内容。不设计新引擎/新作或网站，不推进R79，保留22域、九系统7 PARTIAL+2 OPEN、Stage B GATED。测试和来源报告在独立Actions验收后另记结果，不能预先称成功。
