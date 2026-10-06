# NeoX NPK 格式分析报告(蛋仔派对运行时,2026-10 备份)

分析对象:`files/NeoX/Documents/script.npk`(76.9 MiB)、`script_patch.npk`(416 KiB)、`subpackage/ext_packer_*.npk`、`subpackage/subpacktemp/*.orbit.tmp`。
分析方法:魔数/结构实证 + 社区工具对照(unnpk、zhouhang95/neox_tools、ExMC-Github/New-EggyPartyNeoXResearch)+ 自写解析器(见 `scripts/npk_zstd_walker.py`)。所有结论均在本次会话实测验证。

## 1. 文件头(实测)

```
偏移  长度  含义                          script.npk 实测值
0x00  4    魔数 "NXPK"                   4E 58 50 4B
0x04  4    文件数 count                  6632 (0x19E8)
0x08  4    0                             0
0x0C  4    版本 = 3                      3
0x10  4    0                             0
0x14  4    文件表(map)偏移 map_off     0x04CAF308 (script.npk) / 0x000674C0 (script_patch.npk)
```

- 资源包 `assets.ppk`/`*.ppkn` 魔数 `NXPP`,`.ppk.info` 魔数 `PKIN`,`.ppk.map` 与 `res/npk_file_full_info_bin` 魔数 `PZ$E`(加密 pbin,见 §5)。
- 头之后到 `map_off` 为**数据区**,`map_off` 到文件尾为**文件表**。

## 2. 文件表结构(布局确认,内容加密)

- 表区大小 = `count × 28` 字节,**两包均精确整除**(script_patch:3332/119=28.00;script.npk:185696/6632=28.00),与 unnpk/neox_tools 的 7×u32 条目一致:
  `sign, data_offset, stored_size, original_size, zcrc, crc, flag`。
- 但**表内容被加密**(随机分布;阴阳师老格式为明文,unnpk 可直读)。实测:
  - 用 neox_tools 的 EXPK `moba_xor_key` RC4 变体密钥流直接异或 → 0 个可信条目(offset/size 均越界);
  - 对该密钥流做 0..1,000,000 起始偏移扫描(script_patch 表前 56 字节,判据 `24<=off && off+ln<=size`)→ 0 候选。
- 结论:蛋仔派对(2026 包版本)的 NXPK 文件表使用**独立密钥/算法**。社区资料(New-EggyPartyNeoXResearch README)指明解密入口为游戏内 `package.pkg_decrypt(3, data, 'ppk')`(官方混淆模块,需运行游戏或逆向 libneox so 才能取得算法/密钥)。本备份不含 APK/so,**无法解密文件表**——如实记录,不猜测密钥。

## 3. 数据区(已破解:连续 zstd 帧)★本次核心成果

- `script.npk`/`script_patch.npk` 数据区:zlib 扫描(0x78 0x01/0x9C/0xDA 起始 + 试解压)0 成功,zstd 魔数 0 → **脚本数据整体加密**。
- `subpackage/ext_packer_*.npk` 数据区:zstd 魔数(`28 B5 2F FD`)高密度出现(6MB 样本 107~148 个),且全部 **4 字节对齐**;逐帧解析 `Frame_Header_Descriptor` 取 `Frame_Content_Size`,用 `zstd.get_frame_size()` 定界后 `zstd.decompress()` **全部成功**。
- 即:**玩法/资源包内每个文件独立 zstd 压缩、首尾相接、未加密**,可直接按帧链解出全部内容,完全绕过加密文件表。
- 实测帧数 vs 表 count(高度吻合,差额为少量非 zstd 存储的文件):

| 包 | count(表) | 实解帧数 | 类型分布 |
|---|---|---|---|
| game_plays_7(479.8MB) | 18468 | 18391 | ktx 6840, anim_cfg 4654, mesh 2035, neox_xml 1932, json 1275, bin 1337, xml 314, riff 4 |
| game_plays_8(39.6MB) | 332 | 306 | ktx 217, anim_cfg 23, mesh 11, bin 47 … |
| game_plays_13(25.2MB) | 234 | 234(全) | anim_cfg 111, ktx 56, mesh 35, xml 11, neox_xml 10, bin 11 |
| game_plays_14(88.0MB) | 2525 | 2517 | ktx 1663, neox_xml 333, anim_cfg 187, mesh 77 … |
| subpacktemp/game_plays_17(252.1MB) | 24876 | 24863 | anim_cfg 10197, ktx 5346, mesh 4529, bin 2781, neox_xml 1275, json 377 … |
| official_city_1 / low_skin_7 / pet_high_1 / emoji_1 / sky_box_2 / face_high_1 | — | 与 count 相等 | 纯美术资源 |

- 帧内容识别到的类型:`KTX 11` 纹理、`\xc1YA\r` AnimationConfigFile、`AnimParam`、`34 80 C8 BB` mesh、`<NeoX …>` 特效/动画 XML、JSON、RIFF(WAV)。
- 文件名不可得(在加密表中),以帧序号+类型命名保存(如 `0000583_neox_xml_...bin`)。

## 4. orbit.tmp 断点包(详见 orbit_tmp_analysis.md)

`subpacktemp/*.orbit.tmp` 为 Orbit 下载器断点文件,内容即目标 NPK 的**原始前缀**(同样 NXPK 头),按头部 count/map_off 可精确判定数据区/文件表完整度。12 个断点包数据区均截断(9.4%~83.7%),仅 `ext_packer_game_plays_17.npk` 下载完整(尺寸与 map_off+count×28 精确相等)。

## 5. 周边 pbin 容器(PZ$C / PZ$E / G$MZ)

- `PZ$C` + zstd:明文 pbin(实测 CDN `full_indices_script`、本地 `npk_update/full_indices_*`);但**解压后内容仍为密文**(NPK 索引本体再加密一层)。
- `PZ$E` + zstd:pkg_decrypt(3,…,'ppk') 后 zstd——`res/npk_file_full_info_bin`(2.9MB)、`*.ppk.map` 均属此类,无密钥不可解。
- `G$MZ` + zstd:设置类容器,可直接解(实测 `etc/game_setting_file_new.db` → msgpack 游戏设置;`etc/game_data.bin` → 单字节)。
- `PKIN`(.ppk.info,如 `assets.ppk.info` 10MB):`PKIN`+count(0x07FECD≈52 万)+版本 0x0303,内容加密。

## 6. 密钥/解密的可达边界(如实声明)

| 目标 | 状态 |
|---|---|
| NXPK 文件表(文件名/offset) | ❌ 不可解,密钥在 libneox 原生库/官方 package 模块 |
| script.npk / script_patch.npk 数据(Python 脚本) | ❌ 加密,无有效 zlib/zstd 流 |
| game_plays/资源包数据(美术/动画/XML/JSON) | ✅ 已全量解出(zstd 帧链) |
| PZ$E pbin(npk_file_full_info_bin、ppk.map) | ❌ 需 pkg_decrypt |
| mcache 热更(client_hotfix_v1 / fshotfix_v3) | ✅ msgpack+marshal 可解析,含明文文本与 zstd 附属数据 |

若后续拿到 APK 的 `libneox*.so` 或可运行客户端,按 New-EggyPartyNeoXResearch 的注入/导出路线获取 `pkg_decrypt` 即可补齐文件表与 script.npk;本报告不虚构密钥。

## 7. 复现脚本

- `scripts/npk_zstd_walker.py` — NXPK zstd 帧遍历器(类型分类、关键词扫描、截断标注、清单 JSON)
- `scripts/fshotfix_extract2.py` — mcache 热更 msgpack/marshal 解析 + base64(zstd) 附属数据解压
- `scripts/ldbdump.py` — 无依赖 LevelDB SSTable/WAL 读取器(ctypes libsnappy)
