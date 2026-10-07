# NPK 包身份判定报告 —— 8 个游戏运行时热更包(2026-10-07 会话)

来源:用户补发 8 个 NXPK v3 包(魔数 NXPK 已验),暂存 `/home/eggy-test/npk8/src/`(原文件位于 prompt-attachments 各子目录,前缀 01-)。
工具:上轮 `runtime-2026-10-02/scripts/npk_zstd_walker.py`(先读用法后使用)+ 本会话新增脚本(见 `scripts/`)。

## 0. 判定方法(全部为本次实测)

1. **解包**:npk_zstd_walker.py 按 zstd 帧链提取(帧头 28B52FFD 自带 Frame_Content_Size),统计每包帧数/类型;日志 `walk_all.log`。
2. **CDN 官方对照**(身份金标准):拉取 `https://u5.update.netease.com/pl/npk_version_android.txt`(2026-10-07 实测,原件存 `evidence/cdn_npk_version_android_20261007.txt`),`npkext` 分节按 size+md5 与本地包逐个对照;`update_in_game_npkext_list` 分节判定包系列性质。
3. **内容鉴定**:对解出文件全量 strings/正则收割资源路径与实体代号(`char/loading/t*/*_loading`、`char/parts_appear/*`、`effect/char/<系列>/*`、`wwise/*.bnk` 引用)。
4. **设备侧佐证**:上轮备份 `/home/eggy-test/extracted/files/NeoX/log.txt`(2026-10-06 会话)中 8 个包名全部以 FileLoader 挂载于 `…/Documents/subpackage/<包名>`(log.txt 18:44:07 段)。

## 1. CDN 对照结果(命令:`python3` 对照 npkext 分节,2026-10-07 实测)

| 包 | 本地 size / md5 | CDN 当前 size / md5 | 判定 |
|---|---|---|---|
| ext_packer_low_skin_3 | 88,620,928 / 17ad8d59… | 88,620,928 / 17ad8d59… | **与 CDN 当前版全 md5 一致** |
| ext_packer_sky_box_1 | 130,499,024 / 39a31114… | 130,499,024 / 39a31114… | **与 CDN 当前版全 md5 一致** |
| ext_packer_8 | 360,654,424 / 2c2965e7… | 360,523,236 / d856f60c… | 同名官方包,本地为旧版(CDN 已更新) |
| ext_packer_11 | 230,694,672 / 7ddd5e30… | 285,155,356 / c033116c… | 同上,旧版 |
| ext_packer_fashion_part_high_2 | 243,642,764 / 9a3aba71… | 309,128,368 / 7de1f6e9… | 同上,旧版 |
| ext_packer_low_skin_5 | 84,533,328 / 1c1f98ab… | 83,762,736 / 4a42c2b3… | 同上,旧版 |
| ext_packer_skin_voice_1 | 206,597,180 / 03ef5774… | 211,254,056 / 5c54fd9f… | 同上,旧版 |
| ext_packer_skin_voice_3 | 195,473,136 / e0fc5b9d… | 199,627,920 / 74a1e37c… | 同上,旧版 |

CDN `npkext` 分节共 217 条,系列统计:ext_packer(基础编号)30 条、game_plays 45、low_skin 33、story_book 30、skin_voice 9、fashion_part_high/low 各 6、sky_box 6、sound 6、ui_img 9、accessory 6、editor_props 6、emoji 3、face_high 3、official_city 3、pet_high/low 各 3、shader_cache 6。→ **`ext_packer_8.npk`、`ext_packer_11.npk` 就是官方名称**(基础编号系列第 8/11 号),非用户杜撰名。

CDN `update_in_game_npkext_list` 原文(节选):`["ext_packer_1","ext_packer_10","ext_packer_11","ext_packer_2","ext_packer_3","ext_packer_4","ext_packer_5","ext_packer_6","ext_packer_8","ext_packer_9","ext_packer_fashion_part_high_1","ext_packer_fashion_part_high_2","ext_packer_pet_high_1","ext_packer_skin_voice_1","ext_packer_skin_voice_2","ext_packer_skin_voice_3","ext_packer_sound_1"]`
→ 基础编号系列、fashion_part_high、skin_voice 均属**局内热更(in-game update)资源包**;low_skin/sky_box 不在该表(常规下载分包)。

## 2. ext_packer_8 与 ext_packer_11 是什么(编号包身份)

**结论:两者都是「局内热更」的角色/皮肤资源增量包(基础编号系列 ext_packer_N 的第 8、11 号),不是惊魂夜玩法包,也不是地图包。**

依据(解出内容实测):
- 内容构成一致:`char/loading/t0~t3/<代号>_loading`(皮肤加载页模型)、`char/parts_appear/*`(登场动画部件)、`char/parts/(back|waist)_parts/*`(背饰/腰饰)、`effect/char/<皮肤系列>/t*`(皮肤特效)、`shader/`、贴图与网格。
- ext_packer_8 覆盖皮肤特效系列 **s11/s13/s14/s15/s18/s19/s20/s21/s22 + zy + char_skin**;ext_packer_11 覆盖 **s30/s31/s32/s33 + ip(联名)+ zy**。s 系列即皮肤批次号(与包内 wwise 引用 `skin_appear_action_s21_2`、`skin_appear_action_s31` 互证)→ 8 号是较早批次的增量包,11 号是较新批次。两者时间跨度不同、内容无重叠,属同一滚动增量机制的先后两块。
- **ext_packer_8 特有**:NPC 模型与音效引用 `char\npc\npc_zombie`(僵尸)、`npc_hxys`、`npc_luo`、`npc_dxh`;wwise 事件 `Play_npc_zombie_eat / _foot_first / _foot_second / _run_vo / Play_vo_chuchang_zombie_1`(带中文配音引用 `wwise/chinese/zombie_vo.bnk`)——僵尸 NPC 有出场配音。`zombie_vo` bank 已在 skin_voice_1/3 中按 FNV-1 对撞确认存在(闭环,见 §4)。
- **ext_packer_11 特有**:`char/tth/loading/char_jhdxlv_loading` 与 `jhdxh_loading` 成对(jhdxlv/jhdxh;包内另有 `moba_dxlv_shouzhang` 引用佐证 dxlv 为"蛋小绿"类代号,jh=惊魂为推断,**未定论,如实记录**);`t0_djlw`(部件 syd/lang/tgg/texiaolang);`t2_daocaorenabu`(稻草人阿布)、`t2_yoyobdzb/yoyocgzz/yoyomfsn`、`npc_gxag`;t3 档加载页(t3_4znqfdg/gxdjf/sdz/ssfb/xhcy/zqll/mfs/hzss/shms/sdpl)。
- 两包的 json 帧均为贴图压缩参数(`{"extra_param":"-nordo","astc_rate":"4x4"}`,17/23 个),无业务文案。
- 反向排除:两包与 8 包全体对 `jinghun/idv/fright/boiler` 等token扫描仅命中 base64/浮点随机碰撞(上轮已核验过同类),**无惊魂夜玩法数据**。package_key 25(jinghun_identity_v)对应的玩法 npk 仍不在手。

## 3. 皮肤/语音代号↔中文名的边界声明

包内只有拼音缩写代号,官方中文名对照表在服务器/加密 script.npk 侧,本会话**只对高置信度联名给出解读**(nailong=奶龙、hlw=葫芦娃、tom=汤姆、lotso=草莓熊、woody=胡迪、meiledi=美乐蒂、longnv=龙女、gesang=格桑、daocaorenabu=稻草人阿布、zombie=僵尸等),其余代号原样列出,**不做臆测**。数据站扩展时可直接用代号作键。

## 4. 皮肤语音包(skin_voice_1/3)的格式突破

- 数据区**不是 zstd 帧链**:0x18 起为裸 Wwise SoundBank 顺序拼接(walker 因此报 "no zstd frames")。这是 NXPK 数据区第三种形态(前两种:zstd 帧链 / PZ$E 加密)。
- 结构:940(sv1)/794(sv3)个 bank,每包恰为「纯事件 bank(HIRC)」+「媒体 bank(DIDX+DATA)」对半(470+470 / 397+397);无 STID 字符串块,bank 名只有 32 位数字 ID。
- **ID→名字用 FNV-1(lower 32)对撞破解**:从 6 个解包包收割 175 个 `wwise/*.bnk` 引用名,命中 120;再以全部实体代号 + `_vo` 变体扩表,sv1 命名 139/940、sv3 125/794,共 **141 个 `<角色代号>_vo` 语音 bank**。Wwise bank ID 散列为 FNV-1、输入小写,已固化在 `scripts/npk_wwise_bank_mapper.py`(selftest 复核 2026-10-08:以 ext_packer_8+ext_packer_11 两个解包目录收割,sv1 named=**119**、sv3 named=**106**;初版注记「106 named/2 目录」实为 sv3 之值,对 sv1 不符,已订正;最终 139/125 采用 6 个解包目录全量收割)。
- 媒体为 Wwise Vorbis WEM(`RIFF/WAVE`,`fmt ` tag 0xFFFF,44100Hz):sv1 共 15,354 个 WEM/203,156,524 B 音频;sv3 共 13,457 个/192,480,528 B。
- 语音清单见 `cosmetics_inventory.md` §4;bank 全表见 `evidence/skin_voice_bank_map.txt`。
- 包内文件表仍为加密(map_off 头部高熵,与上轮 PZ$E 结论一致),故 WEM 与 bank 的文件名级对应仍不可得;能定的是 bank 级角色归属。
