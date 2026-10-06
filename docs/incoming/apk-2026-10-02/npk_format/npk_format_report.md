# 蛋仔派对 APK NPK 格式分析报告

- 样本:蛋仔派对官方安卓 APK `release-v1.16.1.4`(2026-09-10 构建,2,129,719,032 字节)
- 分析日期:2026-10-06;分析环境:Linux x64,Python 3.14.4(zstd stdlib),zstd CLI v1.5.7,Info-ZIP unzip 6.00
- 所有脚本见本目录 `scripts/`,原始解包位于 `/tmp/eggyapk/`(临时,不入仓库)

## 1. APK 层

- `unzip` 全量解包得 **5,377 个文件 / 2,414,256,313 字节**,与情报的 5,377 条目一致。
- 类型盘点:见 `inventory/inventory.json`(44 种扩展名;res/ 资源 3,715 XML + 1,277 PNG;assets/ 内 11 个 .npk 共 1.89 GB;12 个 dex;137 个 .so)。
- assets/ 下数字命名 JSON(3262241293.json 等 12 个)经查为桌面小组件/SDK 配置,与游戏玩法数据无关;明文层 15 个关键词全部零命中(见 `plaintext_scan/hits_summary.txt`)。

## 2. NXPK 容器结构(逆向确认)

11 个 .npk 全部为网易 NeoX 引擎 NPK v3 格式:

```
偏移   字段                 样本值(script.npk / wwise.npk)
0x00   magic 'NXPK'        4E 58 50 4B
0x04   条目数 u32           41903 / 126
0x08   保留 u32             0
0x0C   版本 u32             3(全部为 3)
0x10   保留 u32             0
0x14   文件表偏移 u32        0xB76DE08 / 0x2AC3484(=文件大小−表长)
0x18   数据区开始(条目数据)
表偏移  文件表(条目数×28 字节,直至文件尾)
```

文件表 28 字节/条目(与 ZhangFengze/NeoXResearch 公布的 NeoX NPK 表结构一致):
`[0:4] 文件名哈希 ID, [4:8] 数据偏移, [8:12] 压缩大小, [12:16] 解压大小, [16:24] 未知(hash/时间戳), [24:26] 压缩方式, [26:27] 加密方式, [27] 填充0`。

### 关键结论:数据块 = 明文 zstd 帧序列

- 资源类 NPK(wwise/res/char/scene/props/gui2/props_*/char_loading)的数据区是一串连续 zstd 帧,每条目一个帧。
- 帧头直接从 0x18 开始:`28 B5 2F FD` + FHD(实测见 0x20/0x60/0xA0 三种)+ FCS(按 RFC 8878 规则 0/1/2/4/8 字节)。
- 验证:wwise.npk 帧@0x4D0B0 块链 = RAW 131072 + RAW 131072 + RAW 109324,内容即明文 `RIFF....WAVEfmt`(RIFF 尺寸字段 0x05AB04+8 与帧 FCS=0x05AB0C 精确吻合)。
- 帧尾常见 0~3 字节 0x00 填充(解压时需剥离,见 `npk_extract.py` 的 walk_frame/pad 逻辑)。
- Python `compression.zstd` 单帧解压报 "Unknown frame descriptor" 的原因不是帧头非法,而是尾部填充被当作下一帧前缀(`prefix_unknown`)。

### 关键结论:文件表全部加密

- script.npk 表 = 包尾 1,173,264 字节,与 assets/full_indices_script(PZ$C 魔数 + zstd 流,解压后 1,173,284 = 41903×28)一致;解压后熵 **8.000**,28 字节条目各字段零占比均 ~0.4%,重复密钥 XOR 检测(keylen 1..64)全部阴性(`npk_table_attack.py` 输出)。
- wwise.npk 表(尾部 3,528 字节)同样高熵。即:**v3 格式蛋仔 NPK 的文件表在包内一律加密**,且由引擎内嵌逻辑解密(libclient.so 含 'PZ$' 字符串引用,位于 0x72B9368)。
- `assets/res/npk_file_full_info_bin`(PZ$E 魔数,2,914,974 B)与 `assets/full_indices_script_patch`(PZ$C)同理:PZ$C=明文 zstd 容器装加密载荷,PZ$E 载荷熵 8.0(zlib/lz4/单字节 XOR/4 字节 XOR 假设均排除)。

### 各包加密状态汇总

| NPK | 条目数 | 数据区 | 表 | 提取结果 |
|---|---|---|---|---|
| script.npk 193MB | 41903 | **整体加密**(全文件 0 个 zstd 魔数,熵 7.999) | 加密 | 不可提取 |
| script_patch.npk 404KB | 109 | **整体加密**(0 魔数,熵 7.999) | 加密 | 不可提取 |
| res.npk 513MB | 99658 | zstd 明文 | 加密 | 106851 帧,OK 105991 / 失败 860(块载荷加密) |
| char.npk 259MB | 27740 | zstd 明文 | 加密 | 27739/27739 全成功 |
| scene.npk 242MB | 9587 | zstd 明文 | 加密 | 9583/9587 |
| props.npk 362MB | 57528 | zstd 明文 | 加密 | 57528/57528 全成功 |
| gui2.npk 235MB | 31396 | zstd 明文 | 加密 | 31393/31393 |
| wwise.npk 44MB | 126 | zstd 明文(31 帧,大 WAVE 多条目共帧/未压缩存储) | 加密 | 31/31 |
| props_zhucheng.npk 2.7MB | 272 | zstd 明文 | 加密 | 272/272 全成功 |
| props_ui_model.npk 1.8MB | 306 | zstd 明文 | 加密 | 306/306 全成功 |
| char_loading.npk 36MB | 739 | zstd 明文 | 加密 | 739/739 全成功 |

注:res 的 860 个失败条目呈「帧骨架明文、块载荷加密」;script/script_patch 连帧骨架都加密,层级不同。加密算法未定:so 内未找到 AES S-box/MD5/SHA256 常量,RC4 候选密钥(script/NeX/NXPK/eggy 及其 md5/sha1/sha256 派生)以「条目[27]=0」预言机检验全部阴性(≤3/100,基线 0.4)。密钥应在混淆的 libclient.so(145MB,含内嵌 CPython)内,本次未能在会话约束内完成静态逆向。

## 3. 社区工具核验(任务 3a)

- [YJBeetle/unnpk](https://github.com/YJBeetle/unnpk)(v2023,面向阴阳师等旧版 zlib NPK):编译成功(gcc,需 libmagic-dev),对 props_zhucheng.npk 实测输出 `W: Uncompress failed! Z_DATA_ERROR: Data is not zlib`——**不兼容蛋仔 v3(zstd+加密表)格式**。
- [ZhangFengze/NeoXResearch](https://github.com/ZhangFengze/NeoXResearch):提供 28 字节表结构与压缩/加密标志定义,本报告据此对照验证。
- 看雪 thread-255512 有人机验证无法抓取;CSDN 教程均为 unnpk 用法复述,无蛋仔 v3 专属解法。
- 结论:本目录 `npk_extract.py`(无需文件表、按 zstd 帧扫描)对蛋仔资源包的提取率优于社区现成工具。

## 4. 已解内容的数据形态

- 贴图:KTX1.1(`AB KTX 11 BB`)、DDS;音频:WAVE PCM;模型/场景:NeX 私有二进制(串池+记录区,可读属性名/中文文案/lua lambda)。
- NeX 二进制结构(以 res/092570 为例,`nex_kv_dump.py`/`scan/092570_strings.json`):
  `[u32 串数=420][u32 0][u32 偏移表×420][UTF-8 串池 0x698~0x286A][类型标签+池索引的记录区 9651B]`
  串池内含属性名(cd_time_fml、blood_cd、tick_delta_blood、tick_interval、passive_blood_radius 等)、资源路径、中文技能/角色/buff 名,以及**自含数值的 lua 表达式** `lambda unit: fixmath.round(Fix32(30))` 等 29 处。
  记录区的字段→值精确配对需进一步格式逆向(未完成,如实记录)。

## 5. 局限与未竟事项(如实声明)

1. script.npk / script_patch.npk 整体加密未能解开,Lua 脚本与模式配置表(惊魂夜玩法权威数值最可能所在)未能获取。
2. res.npk 860 个加密条目(0.8%)未解,其中可能含部分配置。
3. NeX 记录区的属性名→数值精确配对未完成;当前证据为「属性名池 + lambda 数值 + 上下文共现」,可人工判读但非结构化表。
4. 文件表加密 ⇒ 提取文件无原始文件名,以「序号_包内偏移」命名。

## 6. 原始 NPK 字节级 UTF-8 扫描(2026-10-06 补测)

对 11 个 .npk 原始字节直接 grep(rg -a):惊魂夜/追捕者/海瑟/失血/痛楚领域/迅影索/念奴娇 **全部 0 命中**——符合预期:资源包内容是 zstd 压缩流、脚本包整体加密,UTF-8 关键词只有在**解包后**的 NeX 串池中才可见(见 scan/keyword_freq.txt:解包后惊魂夜 606、追捕 138、海瑟 8、失血 8、痛楚 1 等)。这也再次证明:对蛋仔 v3 NPK,「先解帧、再扫内容」是唯一有效路径。
