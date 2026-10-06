# 玩法分包(subpackage)映射表 —— 「逃出惊魂夜」定位结论

证据优先级:游戏运行日志(`files/NeoX/log.txt` 2026-10-06 会话、`log_old_0.txt` 2026-09-14 会话)> 包内解出内容实证 > 包头结构。

## 1. 服务器玩法包名 → package_key(日志原文,`log.txt:2011`)

`RecommendGamePlayPackageDownloader _server_pack_name_to_package_key:`

```python
{'gag': 34, 'ib_pet': 19, 'sheji': 48, 'ibbaoweizhan': 33, 'chaoran_moba': 13,
 'jinghunduobaodui': 32, 'pengpengqi': 27, 'farm': 46, 'daodan_trouble_egg': 26,
 'nanguaruqin': 35, 'jinghun_identity_v': 25}
```

## 2. package_key → npk 文件(日志原文,`log.txt:3734-3740` / `log_old_0.txt:3475-3483`)

```
try_init_stop:ext_packer_game_plays_1.npk, package_key:13   → chaoran_moba(超燃竞技场/超燃大乱斗)
try_init_stop:ext_packer_game_plays_4.npk, package_key:26   → daodan_trouble_egg(捣蛋/魔鬼蛋玩法)
try_init_stop:ext_packer_game_plays_7.npk, package_key:32   → jinghunduobaodui(惊魂寻宝队,PvE 合作恐怖寻宝)
try_init_stop:ext_packer_game_plays_9.npk, package_key:34   → gag
try_init_stop:ext_packer_pet_low_1.npk,  package_key:19     → ib_pet
```

## 3. 「逃出惊魂夜」定位结论(与任务假设不同,已用日志证实)

- 逃出惊魂夜的官方内部标识 = **`jinghun_identity_v`,package_key = 25**(`jinghun_identity_v` 即「惊魂·第五人格式非对称对抗」;游戏内 OGC 模块 `ogc2_identity_v`、热更模块 `624044_idv_skilldetail_mode_diff`(1v4/2v8 数值切换)、`623573_idv_boiler_tab_remove`(蒸汽炉页签)与公告中 1v4/2v8 数值切换功能互相印证)。
- **本设备未下载该包**:两次会话日志均显示 `_try_start_download_recommend_packs, ['chaoran_moba', 'farm', 'jinghun_identity_v']` 后下载被暂停(`pause download`),subpackage/ 与 subpacktemp/ 中均无对应 npk。**因此备份中没有逃出惊魂夜的玩法包**,457MB 的 `game_plays_7.npk` 实为「惊魂寻宝队」(另一玩法,见 §4),不应混淆。
- 完整 npk 文件名(推测为 `ext_packer_game_plays_25.npk`,因 npk 序号≠package_key,已验证的 4 组映射 1↔13、4↔26、7↔32、9↔34 均无线性关系,**该推测仅为惯例推断,未经证实**——npk 实际序号需 `npk_file_full_info_bin`(PZ$E 加密)解密后确认。

## 4. 备份内全部玩法/资源包清单(subpack_ver 实测 size/md5/pack_ver + 包头)

| npk | size(字节) | pack_ver | md5 | 玩法/用途(证据) |
|---|---|---|---|---|
| ext_packer_game_plays_1 | 219,738,680 | 276 | ca2c986d… | 超燃(chaoran_moba,key13;日志绑定)※备份未含,仅 subpack_ver+日志 |
| ext_packer_game_plays_3 | 359,258,668(目标) | 299 | b2a1e216… | 未定名(force_update 在更新;日志加载 354,239,504 旧版) |
| ext_packer_game_plays_4 | 71,890,772 | 278 | dc41f179… | 捣蛋 daodan_trouble_egg(key26;日志绑定) |
| **ext_packer_game_plays_7** | **479,776,776** | 281 | 9c66ee9c… | **惊魂寻宝队 jinghunduobaodui(key32;日志绑定)** |
| ext_packer_game_plays_8 | 39,643,712 | 256 | 170a0153… | 未定名(纯美术资源) |
| ext_packer_game_plays_9 | 58,785,444 | 276 | 6b51ced2… | gag(key34;日志绑定) |
| ext_packer_game_plays_10 | 15,108,112 | 256 | 96d29b8a… | 未定名 |
| ext_packer_game_plays_11 | 11,904,668 | 256 | 2cc79625… | 未定名 |
| ext_packer_game_plays_12 | 51,864,156 | 256 | 629d3086… | 未定名 |
| ext_packer_game_plays_13 | 25,181,568 | 278 | d5a03dc3… | 未定名(解出 234 文件,纯动画/贴图) |
| ext_packer_game_plays_14 | 88,007,964 | 281 | 5bdc9a9e… | 未定名(纯美术) |
| ext_packer_game_plays_15 | — | — | — | force_update 在列;备份未含 |
| **ext_packer_game_plays_17** | **252,061,080(完整)** | — | — | **蛋仔城(解出 `data.city_npc_data`/`data.city_npc_appearance_data`,NPC 名:治安官/茶饮师/探险家/画家/奶茶店长…)** |
| ext_packer_accessory_1/2 | 172,699,924 / 281,890,128 | 234/99999 | … | 饰品 |
| ext_packer_emoji_1 | 133,055,188 | 263 | … | 表情 |
| ext_packer_face_high_1 | 21,396,140 | 99999 | … | 高模脸 |
| ext_packer_fashion_part_low_1/2 | 70,263,784 / 80,722,176 | 99999 | … | 低模时装 |
| ext_packer_low_skin_7 | 44,922,080 | 234 | … | 低模皮肤 |
| ext_packer_official_city_1 | 39,212,256 | 256 | … | 官方城市资源(蛋仔城美术;count=1289 与断点包 -2032157815 完全一致) |
| ext_packer_pet_high_1 | 32,324,552 | 256 | … | 高模宠物 |
| ext_packer_pet_low_1 | 591,963,360 | 99999 | … | 低模宠物(force_update 在列;备份未含) |
| ext_packer_sky_box_2 | 13,023,540 | 295 | … | 天空盒 |

## 5. 玩法名对照表(服务器 pack name ↔ 中文,由 9/29 公告与玩法体系交叉确认)

| pack name | 中文玩法 | package_key | 备份内 npk |
|---|---|---|---|
| **jinghun_identity_v** | **逃出惊魂夜(1v4/2v8 非对称追逃)** | **25** | **无(未下载)** |
| jinghunduobaodui | 惊魂寻宝队(PvE 合作:怪蛋疯人院/收藏室/宝物图鉴) | 32 | game_plays_7.npk |
| chaoran_moba | 超燃竞技场/超燃大乱斗 | 13 | (game_plays_1.npk,未含) |
| sheji | 激战先锋(枪战) | 48 | 未含 |
| farm | 疯狂农场 | 46 | 未含 |
| ibbaoweizhan | 岛保卫战 | 33 | 未含 |
| pengpengqi | 碰碰棋 | 27 | 未含 |
| nanguaruqin | 南瓜如琴 | 35 | 未含 |
| daodan_trouble_egg | 捣蛋/魔鬼蛋 | 26 | (game_plays_4.npk,未含) |
| gag | (代号,未定名) | 34 | (game_plays_9.npk,未含) |
| ib_pet | 蛋仔岛宠物 | 19 | (pet_low_1.npk,未含) |

## 6. 与「惊魂夜」相关的其他运行时数据(备份内确实存在的)

- OGC 热更模块 `fright_night_common`(fshotfix_v3 内,已解出附属数据,见 evidence/fright_night_common_ogc_hotfix_data.bin;含 editor_ability/character/group/modifier/trigger/unit 7 类编辑器 prefab 索引与 4 组 trigger 数据)。
- 热更模块 `624044_hotfix_idv_skilldetail_mode_diff_py`(常量 `IDV_GAME_TYPE_2V8`、`IDV_MODE_DIFF_TID_SUFFIX`、`ogc2_fix_skill_detail_message`)、`623573_hotfix_idv_boiler_tab_remove_py`、`624044_hotfix_idv_qte_decode_rate_order`。
- OGC 加载记录:`Loaded OGC module custom.pub.ogc.fright_night_promotion_2026`、`ogc2_identity_v_island`(log_old_0.txt:4040 等)。
- 用户聊天缓存:「每天没事干了,打一下惊魂夜。」(chat_last_private_msg.json)。
- UGC 地图池含玩家自制惊魂夜主题图:「惊魂夜抽卡模拟器」「惊魂泳池派对」「惊魂档案:桃乐丝」「挖穿疯人院」(map_pool_cache/166518579/map_pool_info.conf)。
