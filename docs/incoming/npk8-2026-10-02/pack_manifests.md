# 每包解包清单 —— npk8-2026-10-02

解包命令(逐包,8 个全部执行):
`python3 runtime-2026-10-02/scripts/npk_zstd_walker.py /home/eggy-test/npk8/src/<包>.npk /home/eggy-test/npk8/<包>/ 惊魂夜,逃出,蒸汽炉,追捕者,逃生者,海瑟,失血,痛楚领域,迅影索,暗影能量,念奴娇,百珍楼,礼温,梵蒂娅`
日志:`/home/eggy-test/npk8/logs/walk_all.log`;逐帧清单:`evidence/<包>.walk.json.gz`(skin_voice 无帧清单,见 §7)。

全部 8 包 `data=COMPLETE table=COMPLETE`(数据区完整到 map_off,文件表完整);文件表加密不可解(沿用 runtime-2026-10-02 结论,本轮对 3 个包抽样确认高熵无明文)。

## 1. zstd 帧链包(6 个)

| 包 | 包头 count | 解出帧数 | 类型分布(帧数) | 落盘文本/配置文件 |
|---|---|---|---|---|
| ext_packer_8 | 3891 | **3890** | ktx 1368 / anim_cfg 1011 / neox_xml 704 / mesh 396 / bin 272 / xml 122 / json 17 | 2,126 |
| ext_packer_11 | 1824 | **1824** | ktx 739 / anim_cfg 451 / neox_xml 256 / mesh 177 / bin 104 / xml 74 / json 23 | 908 |
| ext_packer_fashion_part_high_2 | 2640 | **2640** | anim_cfg 1173 / ktx 694 / mesh 586 / neox_xml 187 | 1,360 |
| ext_packer_low_skin_3 | 3452 | **3452** | anim_cfg 1532 / ktx 737 / mesh 582 / neox_xml 520 / xml 66 / json 13 / bin 2 | 2,133 |
| ext_packer_low_skin_5 | 2582 | **2582** | anim_cfg 1148 / ktx 565 / mesh 460 / neox_xml 407 / bin 1 / xml 1 | 1,557 |
| ext_packer_sky_box_1 | 548 | **548** | anim_cfg 230 / ktx 156 / mesh 115 / bin 47 | 274* |

\* walker 对 ≥8MB 的解出内容不落盘,sky_box_1 有 3 帧因此未落盘(walk.json 有记录)。

帧数 vs 包头 count 的差额(仅 ext_packer_8 差 1)来自数据区末尾/解压失败帧,walk.json 中有逐帧 status;其余包帧数与 count 完全一致。

## 2. ext_packer_8(360,654,424 B,md5 2c2965e70e6b39cda0d93c0a8c89453e)

- 身份:局内热更角色资源增量包(皮肤系列 s11~s22 时代),详见 identity_report.md §2。
- loading 加载页代号(初版记 141 个,系未归档的变体归组口径,2026-10-08 独立复核 9 种收割口径均无法复现,**待核验**;可复现「路径组件级」口径实测 **123** 个,工具与口径定义见 `scripts/count_skin_codes.py`),t0~t3 各档,含:t0_bskq/t0_kqbsyck/t0_lhjjia、t1_bdpj/t1_chn(及其 _cat/_jun 变体)/t1_longnv/t1_ycymn/t1_zgts/t1_xzll、t2_any/t2_argjpf/t2_cmx/t2_ctwwyy/t2_dltz/t2_dsjdl/t2_dylb/t2_gesang/t2_gfxm/t2_gzzt/t2_hlw/t2_hmxb/t2_hsll/t2_jlfs/t2_kbhzdj/t2_kdm/t2_kpbl/t2_lzs/t2_nailong(parts_appear)/t2_psqs/t2_qqy/t2_sdlwjl/t2_sjss/t2_sjzfgbg/t2_syls/t2_tkat/t2_ts/t2_xfb/t2_xhbnn/t2_xylnt/t2_ylmns/t2_ytnr、t3_awnz/t3_bdm/t3_dxhsw/t3_hdlxll/t3_hlwyy/t3_hsxl/t3_lmyb/t3_lpsrzs/t3_mhjs/t3_msxn/t3_qbtt/t3_rshnn/t3_sdxp/t3_slll/t3_stgj/t3_sxg/t3_txbl/t3_txydd/t3_wxr/t3_xbf/t3_xsxz/t3_yds/t3_ydyww/t3_yzgjkk/t3_zhhb/t3_zhxq 等(全表见 walk 产物 strings,此处为去重清单)。
- parts_appear 部件目录:含 motion_t2_niuzaishike(牛仔时刻)/motion_t2_qiangbangbangtang/motion_t3_jingjigongzhu、t2_nailong、t2_gesang、t1_lzjl(含 _yc)、t1_sj_mofang、t1_xzll(cunzhuang/dyxem/mofashu 子部件)等。
- NPC:npc_zombie(含 wwise/chinese/zombie_vo.bnk 出场配音事件)、npc_hxys、npc_luo、npc_dxh。
- 高置信联名:t2_hlw 葫芦娃、t2_nailong 奶龙、t2_ts 汤姆、t1_longnv 龙女、t2_gesang 格桑。

## 3. ext_packer_11(230,694,672 B,md5 7ddd5e305daa58a389a0e14c93ace0c7)

- 身份:局内热更角色资源增量包(皮肤系列 s30~s33 + ip 联名时代),详见 identity_report.md §2。
- loading 代号(初版记 90 个,系未归档归组口径**待核验**;可复现「路径组件级」口径实测 **77** 个,见 `scripts/count_skin_codes.py`):t0_djlw(部件 syd/lang/tgg/texiaolang)/t0_dwlj、t1_bs/t1_bshe/t1_hjnan/t1_qs/t1_qssg/t1_slzs/t1_ssjl(含 _hua/_hudie)/t1_wuwu/t1_apper_znqing、t2_bgdd/t2_ciwei/t2_cxqsln/t2_dcr/t2_hznlbld/t2_jrde/t2_jxg/t2_lwdjb/t2_pgym/t2_qqtbn/t2_sddhlb/t2_sjhshh/t2_sxhshs/t2_tzxjjnk/t2_tzxz/t2_xhm/t2_xllp/t2_ybwwwo/t2_ynsdl/t2_yoyobdzb/t2_yoyocgzz/t2_yoyomfsn、t3_4znqfdg/t3_bmhdp/t3_ccjj/t3_dpr/t3_fh/t3_gxdjf(04)/t3_hhm/t3_hp/t3_hsdz/t3_hzss/t3_ljc/t3_mfs/t3_mxxx/t3_mzdpp/t3_sbw/t3_sdpl/t3_sdz/t3_shms/t3_ssfb/t3_sszjy/t3_tesssh/t3_txzz/t3_xhcy/t3_xtz/t3_xxntt/t3_xzm/t3_ystz/t3_yzfd/t3_zqll。
- 特有:`char/tth/loading/char_jhdxlv_loading`(jhdxlv_d/n/m/bq 四张贴图)+ `jhdxh_loading`(成对,疑为惊魂主题蛋小绿/蛋小黄,jh=惊魂为推断未定论);`moba_dxlv_shouzhang` 引用;`t2_daocaorenabu`(稻草人阿布);npc_gxag 模型(gim 三级 LOD)。

## 4. ext_packer_fashion_part_high_2(243,642,764 B,md5 9a3aba71…)

- 身份:高模时装部件包(t4 档),无整身模型,只有 head/upper/lower 分件。
- loading 单元(初版记 183 个,系未归档归组口径**待核验**;可复现「路径组件级」口径实测 **189** 个、其中 t4_* 前缀 **187** 个,见 `scripts/count_skin_codes.py`):`t4_head_chqq/hhwntz/hshdj/rdxs/ttwntz/wqpf/hntz`、`t4_upper_*` 150+(如 t4_upper_axyxtz/ayqq/bbbd/blwq/ccgcy/djjnyd(01/02)/gqdstz/hhwntz/jhxbd_dxh/lingshitz/rmwxcbs/sjyhgy/tyf_ugc/zs_ugc 等)、`t4_lower_mdstz/mhl`、`t4_tefg`、`t4_drqxtz_upper`。骨架全部引用 `danzai01_lod/danzai01_lod_ead7bd.skeleton`。

## 5. ext_packer_low_skin_3(88,620,928 B,md5 17ad8d59…,**CDN 当前版全 md5 一致**)

- 身份:低模皮肤模型包(t0~t3),模型代号(初版记 248 个,系未归档归组口径**待核验**;可复现口径 gim 实体目录 **120**、gim 基名(剥 _lod 后缀)**478**,见 `scripts/count_skin_codes.py`;含 _fen/_lan/_low/_2/_3/_4 配色与 LOD 变体)。
- 代表:t0_zbqs(多配色)、t1_bwl/t1_tkcz/t1_xy/t1_snas、t2_betxr/t2_bot/t2_bxnsf/t2_cnbb/t2_ctjl/t2_cw/t2_djatm/t2_duckoo/t2_gwc/t2_hztt/t2_jljj/t2_kskl/t2_lzlm/t2_mdap/t2_mgqs/t2_mjsnyl/t2_myxxy/t2_sjl/t2_smm/t2_smylk/t2_ssdl/t2_tgxy/t2_wxxm/t2_xiaoxiang/t2_xrztz/t2_yysr/t2_zgqthmss、npc_xy、t3_* 70+(t3_bohl/bzdd/cgxb/cmcet/dcr/ddn/dfmj/dxx/dyks/fchmg/fqlls/fsxg/hdmm/hgtz/hjhk/hjtz/htdd/jsj/mcan/mjgn/nsjj/nxhh/qdd/qlhzs/skbjy/smnn/smzx/st/thdcrn/tsal/tysy/ufo/wqfj/wwyxs/xgcc/xhjyy/xlg/xmtz/xskf/xxsy/yhdgs/yhybb/ylsy/ysdaf/ysdqz/ysdzz/yw/yzss/zzlmma 等)。

## 6. ext_packer_low_skin_5(84,533,328 B,md5 1c1f98ab…)

- 身份:低模皮肤模型包(t0~t3),模型代号(初版记 122 个,系未归档归组口径**待核验**;可复现口径 gim 实体目录 **87**、gim 基名(剥 _lod 后缀)**237**,见 `scripts/count_skin_codes.py`)。
- 代表:t0_lh、t1_rygj/t1_syn/t1_lhdls/t1_lhyc、t2_aygd/t2_bebe/t2_begz/t2_dfxmm/t2_dsxwz/t2_flwj/t2_hhh/t2_hjjfbl/t2_htbp/t2_jjsnfx/t2_jkm/t2_lmxgw/t2_loopy/t2_lyjxj/t2_mbgss/t2_mxmmt/t2_xfdty/t2_xhcz/t2_xlmm/t2_xx/t2_yjsnyr/t2_yswz/t2_zyzc、t3_sdbl/t3_dl/t3_jjls/t3_wyqdp/t3_cqdhzb/t3_yrqsjk/t3_cjgjkk/t3_mfl/t3_mtwm/t3_swk(孙悟空?)/t3_xy/t3_zbj/t3_zx、**渠道服联名 t3_233lypf(233 乐园)/t3_hykb(好游快爆)/t3_xhs(小红书)/t3_oppopf(OPPO)/t3_wztqp/t3_jbxst**。

## 7. ext_packer_skin_voice_1 / _3(语音包,非 zstd 帧链)

| 包 | bank 数 | 媒体 bank | 事件 bank | WEM 总数 | 音频字节 | 命名 VO bank |
|---|---|---|---|---|---|---|
| skin_voice_1 | 940 | 470 | 470 | 15,354 | 203,156,524 | **139** |
| skin_voice_3 | 794 | 397 | 397 | 13,457 | 192,480,528 | **125** |

- 两包 VO 名单重叠 123;仅 1 号有:aniya/bgdd/buzz/duoer/huanghun/jirouduoer/kdm/lmdl/lotso/lwmm/meiledi/tzxz/woody/xllp/ytn/yueer;仅 3 号有:chnj/pjxj。
- 全部 141 个具名 VO 见 `cosmetics_inventory.md` §4;bank 级 off/size 见 `evidence/skin_voice_bank_map.txt`。
- WEM = Wwise Vorbis(`RIFF/WAVE` + `fmt ` tag 0xFFFF、单声道 44100Hz 实测样本),未做转码(如需试听需 ww2ogg+codebooks,未安装,如实记录)。

## 8. ext_packer_sky_box_1(130,499,024 B,md5 39a31114…,**CDN 当前版全 md5 一致**)

- 身份:天空盒/场景环境包。内容(scene_w 下 cube .dds + 配套 tga):
  - 蛋仔岛/城市:cwldao_02~05、cwldao_city01~03(含 _n 夜景)
  - 嘉年华:jianianhua2
  - 竞速赛季场景:jingsu_s25_1、jingsu_s26_1、jingsu_s31_1(skybox_s9~s26_cube 系列全覆盖)
  - 农场/内场 nchang_*:haimianbaobao(海绵宝宝)、yaojingsenlin(妖精森林,昼/夜)、xiaoma(小马,含 raodong 绕动变体)、xiongmao(熊猫,02)、xingkong(星空)、gftyuan、xianjing_d/_n
  - 其他:t1_yasha、gongchangyuanjing1(广场远景)、sky_normal/sky_normal2、sky_luolei(落雷)、sky_disturbance/distortion/lerpcolor/change_all、yyh2/yyh3 系列
- **无「百珍楼/bzl/baizhen」任何资源**(定向扫描 0 命中)。

## 9. 产物位置

- 工作区(不入库):`/home/eggy-test/npk8/<包>/files/*.bin`、`<包>/<包>.walk.json`、`src/`(8 包原档)、`logs/`。
- 入库(本目录):identity_report.md、pack_manifests.md(本文)、keyword_hits.md、cosmetics_inventory.md、manifest.json、evidence/(walk 清单 gz、skin_voice_bank_map.txt、CDN 原件)、scripts/(walker 沿用上轮,新增 mapper/多编码扫描/驱动脚本)。

## 10. 计数口径勘误(2026-10-08 独立复核补档)

初版四组总数(ext_packer_8 loading=141、ext_packer_11 loading=90、fashion t4=183、low_skin_3=248、low_skin_5=122)出自**未归档**的变体归组口径(把 _lod/_2/_3/配色等变体人工归组),独立复核以目录级/路径边界/strings 模拟/清单展开等 9 种收割口径均无法复现(各组得一区间而非单值)。已在各节就地标注「初版记 X,**待核验**」,并补档可复现口径脚本 `scripts/count_skin_codes.py`(2026-10-08 实测,三口径):

| 包 | 初版总数(待核验) | 组件级 loading_units | gim 实体目录 | gim 基名(剥 _lod) |
|---|---|---|---|---|
| ext_packer_8 | 141 | **123** | 60 | 91 |
| ext_packer_11 | 90 | **77** | 14 | 25 |
| ext_packer_fashion_part_high_2 | 183 | **189**(t4_* 187) | — | — |
| ext_packer_low_skin_3 | 248 | 0(无组件级 loading token) | **120** | 478 |
| ext_packer_low_skin_5 | 122 | 0(无组件级 loading token) | **87** | 237 |

站内建索引时**以已验证的代号清单/bank(940/794)/WEM(15,354/13,457)与 141 个具名 VO bank 精确数为准,暂不采信四组旧总数**;清单本身的枚举数(标题已统一)与包内可复现口径数可能不等(清单为去重节选,如 low_skin 系列清单仅列代表代号)。
