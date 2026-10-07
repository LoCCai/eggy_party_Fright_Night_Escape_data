# 关键词命中报告 —— 8 个热更 NPK(2026-10-07 会话)

## 1. 扫描范围与方法

- **解出内容**:6 个 zstd 帧链包共 8,358 个落盘文件(neox_xml/json/xml/anim_cfg/anim_param/bin;walker 已按内容魔数分类落盘,ktx/mesh 等纯二进制未落盘)。
- **原始字节**:8 个 npk 全文件字节流(含 skin_voice_1/3 的 Wwise bank 区)。
- **编码**:UTF-8 / UTF-16LE / UTF-16BE / GBK 四种(仅扫 UTF-8 会漏 UTF-16 文本,故四路全扫)。工具:`scripts/npk_multiscan_keywords.py`(本会话新增,可复现)。
- **关键词**(任务单 14 词 + 缺口拼音/英文推测):惊魂夜 逃出 蒸汽炉 追捕者 逃生者 海瑟 失血 痛楚领域 迅影索 暗影能量 念奴娇 百珍楼 礼温 梵蒂娅 / jinghun identity_v fright boiler yingzhua xunying niannujiao fandiya liwen haiser haise xiaoejiao baizhenlou zhengqilu。

## 2. 结果:全部命中均为随机碰撞,零真实文本

| 关键词 | 解出文件命中 | 原始 npk 命中 | 人工核验 |
|---|---|---|---|
| 礼温 | **1**(ext_packer_8 `0003561_bin…bin` @0x32dfcf,UTF-16LE) | 4(ext8 gbk / ext11 utf16le / fashion gbk / sv1 gbk RAW) | 解出命中处上下文为 `3c 79 29 6e 28 2c 00…` 的定长浮点/顶点记录表(DDS 纹理文件,4,194,416 B,魔数 `DDS `、dwSize=0x7C),UTF-16「礼温」= `3c 79 29 6e` 恰与浮点字节重合 → **碰撞** |
| 逃出 | 0 | 1(ext8 RAW @0xdcfda72) | 高熵压缩流 → 碰撞 |
| 失血 | 0 | 1(ext8 RAW @0x3e58273) | 同上 → 碰撞 |
| 海瑟 | 0 | 2(fashion RAW) | 同上 → 碰撞 |
| 惊魂夜/蒸汽炉/追捕者/逃生者/痛楚领域/迅影索/暗影能量/念奴娇/百珍楼/梵蒂娅 | 0 | 0 | 零命中 |
| jinghun/idv/fright/boiler/yingzhua/xunying/niannujiao/fandiya/liwen/haiser/haise/xiaoejiao/baizhenlou/zhengqilu(ASCII) | 0(idv 仅 base64/浮点随机串,与上轮 game_plays_7 同类,已核验) | — | 零真实命中 |

碰撞判定方法:2~4 字节模式在数百 MB 压缩/二进制数据中随机出现属预期(上轮 runtime-2026-10-02 §4 已确立同一结论并验证过同类命中);本轮对每个命中打印 ±16~32 字节上下文人工确认。

> **勘误(2026-10-08 独立复核订正)**:① 礼温原始流命中为 **4** 处(ext8 gbk / ext11 utf16le / fashion gbk / sv1 gbk),初版记 3 漏计 sv1;② 全量命中合计 **9**(解出 1 + 原始流 8:礼温 5、海瑟 2、逃出 1、失血 1),初版表内合计 8、manifest.json collisions_verified=7 均有漏计,已同步订正;③ 命中文件 0003561 魔数实测为 **DDS 纹理**(`DDS ` + dwSize=0x7C),初版「DDRS 二进制格式」系笔误;碰撞判定本身成立(命中 @0x32dfcf 与初版一致,邻域高熵无文本结构,复核实测 4KB 邻域香农熵 7.95 bits/byte)。

## 3. 结构性发现(非文本但与惊魂夜字形相关)

- ext_packer_11 存在 `char/tth/loading/char_jhdxlv_loading` 与 `jhdxh_loading` 成对资源(jhdxlv_d/n/m/bq 贴图),另有 `moba_dxlv_shouzhang` 引用佐证 dxlv 代号;jh=惊魂属推断,**无文案可证实,未定论**。
- ext_packer_8 有 `eff_jh_v01`/`eff_expression_jh_v01`(effect/char 表情贴图),jh 前缀语义同样无法证实。
- skin_voice_1/3 含 **zombie_vo** 配音 bank(与 ext_packer_8 的 npc_zombie/僵尸 NPC 引用闭环)——是 Halloween 风格 NPC,与惊魂夜玩法无文本层关联。

## 4. 与上轮结论的衔接(去重声明)

上轮(runtime-2026-10-02)已确认:迅影索/念奴娇/暗影能量/爆米花在运行时备份全域 0 命中;海瑟文本命中均属超燃系或蛋仔城 NPC。本轮 8 个新包扫描后,这三个词**依旧 0 命中**,不新增证据;本报告不重复上轮已入库的公告/词库内容(见 runtime-2026-10-02/keyword_hits.md)。

## 5. 复现命令

```bash
python3 scripts/npk_multiscan_keywords.py \
  "惊魂夜,逃出,蒸汽炉,追捕者,逃生者,海瑟,失血,痛楚领域,迅影索,暗影能量,念奴娇,百珍楼,礼温,梵蒂娅" \
  /home/eggy-test/npk8/ext_packer_8/files /home/eggy-test/npk8/ext_packer_11/files \
  /home/eggy-test/npk8/ext_packer_fashion_part_high_2/files /home/eggy-test/npk8/ext_packer_low_skin_3/files \
  /home/eggy-test/npk8/ext_packer_low_skin_5/files /home/eggy-test/npk8/ext_packer_sky_box_1/files \
  /home/eggy-test/npk8/src/ext_packer_8.npk /home/eggy-test/npk8/src/ext_packer_11.npk \
  /home/eggy-test/npk8/src/ext_packer_fashion_part_high_2.npk /home/eggy-test/npk8/src/ext_packer_low_skin_3.npk \
  /home/eggy-test/npk8/src/ext_packer_low_skin_5.npk /home/eggy-test/npk8/src/ext_packer_skin_voice_1.npk \
  /home/eggy-test/npk8/src/ext_packer_skin_voice_3.npk /home/eggy-test/npk8/src/ext_packer_sky_box_1.npk
```
