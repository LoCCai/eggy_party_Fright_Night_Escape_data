# 外观数据盘点(皮肤/时装/天空盒/语音)—— 可用于数据站扩展

代号一律为包内原始资源名(拼音缩写/官方资源代号),**只对高置信联名标注解读**,其余不臆测。骨架统一为 `danzai01_lod/danzai01_lod_ead7bd`(蛋仔通用骨架),即这些是玩家蛋仔皮肤,不是惊魂夜追捕者/逃生者角色模。

## 0. 计数口径说明与勘误(2026-10-08 独立复核补档)

本文件 §1/§2/§3 的清单为**去重节选**(变体/配色在括号内注记,不逐项展开),标题原标的总数(183/248/122)出自初版未归档的变体归组口径,独立复核用 9 种收割口径均无法复现,**待核验**。现统一改标两层口径:①「清单枚举 N 项」= 该节清单实际列出的条目数(本文可数);②「包内实测」= 可复现脚本 `scripts/count_skin_codes.py` 的三口径数(路径组件级 `<代号>_loading` / gim 实体目录 / gim 基名剥 _lod)。两者不等属预期(清单是节选)。站内建索引**以代号清单本体、bank 数(940/794)、WEM 数(15,354/13,457)与 141 个具名 VO bank 等精确数为准,暂不采信四组旧总数**(ext_packer_8 loading=141、ext_packer_11 loading=90 同批待核验,详见 pack_manifests.md §10)。

## 1. ext_packer_fashion_part_high_2 —— 高模时装部件(清单枚举 176 项;包内 loading 组件级实测 189、其中 t4_* 187;初版记 183 待核验)

- 头部 `t4_head_*`:chqq、hhwntz、hshdj、rdxs、ttwntz、wqpf;整头 t4_hntz。
- 上装 `t4_upper_*` 150+:axyxtz、ayqq、bbbd、bdtq、bkbt、blwq、bsktz、bttz、ccgcy、cgtz、clcgtz、cmtxyz、cpwbtz、crwftz、ddcjltz、dfq、dgsw、djjnyd(01/02)、dsld、dspf(loding 拼写错误原样)、dstz、dysntz、fcztz、fstxjtz、fxqtz、fzzyz、gqdstz、gsdtz、gtys、gwbccmtz、hcttz、hddytz、hdjxs、hhwntz、hjyhtz、hkljtz、hlcbtz、hls、hlwltz、hmqstz、hmsytz、htdjtz、huadantz、hytc、jglb、jhmx、jhxbd_dxh、jjytz、jnhtz、jtxhtz、jwz、jxy、jymytz、kfbg、kfhb、kgsj、kgtz、khzytz、klljy、kly、klyytz、lbyctz、ldrytz、lgxh、lhsntz、lhtz、lingshitz、lkkjtz、lnygtz、lsxztz、lxx、lxxw、lytxj、mdstz、mfstz、mkdytz、mldsy、mlqmtz、mmhtz、mskj、mtsst、mwpstz、mxkrtz、mxyytz、myhd、mysntz、nck、nctzdy、njzrtz、nptz、qlcqtz、qpgtz、qrfstz、qxxq、qyystz、qztz、rlystz、rmwxcbs、scstz、sjyhgy、sldx、slyctz、slztz、smzw、ss、ssaz、ssjstz、sspa、stbltz、sxsztz、tbtj、tchdtz、tchgtz、tflzs、tmzj、tslj、ttsyytz、ttwntz、ttxstz、tyf_ugc、tymtz、wljjdytz、wlsstz、wmnltz、wzxmttz、xbfq、xcjtz、xcyctz、xft、xghb、xhcjtz、xllztz、xltftz、xscz、xssytz、xtxg、xxcstz、xxjtz、xyhttz、xysntz、xytz、ygsztz、yjhw、ykbhtz、ylhgtz、yllxftz、ymqtz、ypgftz、yqsl、ywftz、yxdstz、yxsltz、yyhjnpf、yysr、yyxs、yzwq、zagtz、zcltz、zcnz、zgfltz、zhjtz、ziyutz、zlltz、zs_ugc、zsjstz、zsswtz、zxhd、zymbtz、zyt。
- 下装 `t4_lower_*`:mdstz、mhl;部件 t4_tefg、t4_drqxtz_upper。
- 注:`*_ugc` 两个分件(tyf_ugc/zs_ugc)为 UGC 关联部件。

## 2. ext_packer_low_skin_3 —— 低模皮肤模型(清单枚举 109 项;包内 gim 实体目录实测 120/gim 基名 478;初版记 248 待核验;CDN 当前版 md5 一致)

t0_zbqs(+_fen/_lan/_low 配色)、t1_bwl(+_2/_3/_low)、t1_bwlbb_ke、t1_snas、t1_tkcz、t1_xy、t2_betxr、t2_bot、t2_bxnsf、t2_cmtz、t2_cnbb、t2_crq、t2_ctjl、t2_cw、t2_djatm、t2_duckoo、t2_gds、t2_gwc、t2_hztt、t2_jljj(+yck)、t2_jttz、t2_kskl、t2_lzlm、t2_mdap、t2_mgqs、t2_mjsnyl、t2_myxxy、t2_sdss、t2_sjl、t2_slatm、t2_smm、t2_smylk、t2_ssdl、t2_tgxy、t2_wxxm、t2_xiaoxiang(+_4)、t2_xrztz、t2_xw、t2_xzy、t2_yc、t2_yn、t2_yysr、t2_zgqthmss、t2_zgqttzxj、t2_ztatm、npc_xy;t3 71 组:bohl、bzdd、cgxb、cmcet、dcr、ddn、dfmj、dme、dxx、dye、dyks、dys、eh、fchmg、fpp、fqlls、fsxg、hdmm、hgtz、hjhk、hjtz、htdd、jg、jsj、lb、mcan、mg、mjgn、myr、nsjj、nxhh、qdd、qlhzs、skbjy、smnn、smzx、st、thdcrn、tsal、tyh、tysy、ufo、wqfj、wwyxs、wx、xcy、xgcc(+lod1)、xgj、xhjyy、xj、xlg、xmtz、xskf、xxsy、yhdgs、yhybb、ylsy、ym、ysdaf、ysdqz、ysdzz、yw、yzss、zzlmma。
高置信联名/彩蛋:t2_duckoo(鸭鸭?)、t2_xiaoxiang(小象? 湘?)——仅列不解读。

## 3. ext_packer_low_skin_5 —— 低模皮肤模型(清单枚举 52 项;包内 gim 实体目录实测 87/gim 基名 237;初版记 122 待核验)

t0_lh(+_2)、t1_lh(+_2)、t1_lhdls(+_2/_3)、t1_lhyc、t1_rygj、t1_syn、t2_aygd、t2_bebe、t2_begz、t2_dfxmm、t2_dsxwz、t2_flwj、t2_fyy、t2_hhh、t2_hjjfbl、t2_htbp、t2_jjsnfx、t2_jkm、t2_jr、t2_lmxgw、t2_loopy、t2_lyjxj、t2_mbgss、t2_mxmmt、t2_myy、t2_tf、t2_tm、t2_xd、t2_xfdty、t2_xhcz、t2_xhh、t2_xlmm、t2_xx、t2_yjsnyr、t2_yswz、t2_zyzc;t3:bol、bosz、dj(+lod1)、mtwm、ss、swk、xy、yrqsjk、zbj、zx。
**渠道服专属 t3(与 low_skin_3 互证该档承载渠道联名)**:t3_233lypf(233 乐园)、t3_hykb(好游快爆)、t3_xhs(小红书)、t3_oppopf(OPPO)、t3_wztqp、t3_jbxst(4399 贝斯特?—— jbxst 仅列不解读)。
高置信联名/文化元素:t3_swk(孙悟空)、t2_loopy(Looky/露比?)、t2_begz(贝果? )——swk 解读为拼音首字母惯例,置信较高;loopy 仅列。

## 4. ext_packer_skin_voice_1 / _3 —— 角色语音 bank(FNV-1 对撞命名,共 141 个)

**skin_voice_1(139 个)**:
airui、aniya、argjte、ays、badi、baobaolong、bgdd、blackjijia、blackxc、bmrr、bs、bsnk、bspzw、bst、bszs、bszssp、buzz、chigui、ctww、cxqsln、dcrab、degula、dexila、duoer、duoji、dyase、dybb、faladi、fmm、fulu、gesang、gzzt、heisen、hhh、hls、hlw、hmxb、hsll、hssn、huanghun、hymm、hznl、hztt、jiaxian、jijia、jirouduoer、jiujietl、jlfsyg、jxg、jyjxj、jymm、kdm、kpbl、ldss、lhww、lion、liubai、ljssbb、lmdl、longnv、lotso、lswket、lwmm、lwp_male、lxjdd、mbg、mdss、meiguiyeqishi、meiledi、mnflt、moumou、muou、mvs、nailong、ncdap、nianbao、pgyym、po、psqske、qingji、qiyaya、qqtbn、qshe、ruyi、rygj、sbhm、sglnfr、shenqian、shifu、sptzflt、ssjlyh、sszssy、sxcz、taikong、taoqimiao、tgx、tiangou、tkcz、tkit、tom、tqqs、tvdl、txdanmei、txdanzong、tzxj、tzxz、woody、wyjl、xc、xcwdd、xemzz、xfb、xhbnn、xhm、xhy、xiaolanmao、xiha、xitong、xllp、xshshs、xst、xsz、xtsyl、xtykk、xyjlhdy、xylnt、xymm、yddlt、ylmns、ynsdl、ytn、yuanzi、yueer、yxlnfr、yysr、zfgbg、zgjl、zombie、zyzc

**skin_voice_3 在 1 的基础上**:去掉 16 个(aniya、bgdd、buzz、duoer、huanghun、jirouduoer、kdm、lmdl、lotso、lwmm、meiledi、tzxz、woody、xllp、ytn、yueer),新增 2 个:**chnj、pjxj**(共 125 个)。

高置信解读(仅联名/常见词,其余不解读):baobaolong=泡泡龙、hlw=葫芦娃、lotso=草莓熊(熊抱哥)、woody=胡迪、meiledi=美乐蒂、tom=汤姆、nailong=奶龙、longnv=龙女、gesang=格桑、tiangou=天狗、taikong=太空、yueer=月儿、huanghun=黄昏、xiaolanmao=小蓝猫、meiguiyeqishi=玫瑰夜骑士、shenqian=深潜、qiyaya=起亚丫丫?、zombie=僵尸、taoqimiao=淘气喵、dcrab=寄居蟹(crab)。**heisen(海瑟森?黑森?)与 haiser/haise(海瑟拼音)均无证据视为海瑟,如实标注为未解读。**

媒体统计:sv1 = 470 媒体 bank/15,354 WEM/203MB;sv3 = 397/13,457/192MB(Wwise Vorbis 44.1kHz);bank↔WEM 文件名级对应仍需文件表(加密),当前为 bank 级归属。

## 5. ext_packer_sky_box_1 —— 天空盒/环境(CDN 当前版 md5 一致)

赛季天空 skybox_s9~s26(+ yyh2/yyh3 系列通用)、场景级:cwldao_02~05 与 cwldao_city01~03(蛋仔岛城市,含夜景)、jianianhua2(嘉年华)、jingsu_s25_1/s26_1/s31_1(竞速赛季场景)、nchang_haimianbaobao(海绵宝宝)/yaojinselin 昼夜(妖精森林)/xiaoma(小马,+raodong)/xiongmao(熊猫,+02)/xingkong(星空)/gftyuan/xianjing 昼夜、t1_yasha、gongchangyuanjing1(广场远景)、通用 sky_normal/normal2/luolei(落雷)/disturbance/distortion/lerpcolor/change_all。
惊魂夜/百珍楼:0 个场景资源(定向扫描确认)。

## 6. ext_packer_8 / ext_packer_11 中的外观部分

- ext_packer_8:loading 加载页皮肤 t0~t3 档(初版记 141 个,**待核验**;可复现组件级口径 123,见 pack_manifests.md §10)+ parts_appear 登场部件(含 t2_nailong 奶龙、t2_gesang 格桑、motion_t2_niuzaishike 牛仔时刻、motion_t3_jingjigongzhu 竞技公主)+ 特效系列 s11~s22/zy/char_skin + NPC(npc_zombie 僵尸/npc_hxys/npc_luo/npc_dxh)。全表见 pack_manifests.md §2。
- ext_packer_11:loading 皮肤 t0~t3(初版记 90 个,**待核验**;可复现组件级口径 77)+ 特效系列 s30~s33/ip/zy + `char_jhdxlv`/`jhdxh`(疑惊魂主题蛋小绿/蛋小黄,推断未定论)+ t2_daocaorenabu(稻草人阿布)+ npc_gxag。全表见 pack_manifests.md §3。

## 7. 数据站落地建议(依据)

- 可直接建「皮肤代号索引」:以 t*_<代号> 为主键,标注来源包与档位(t0 低模/t4 时装分件/t3 渠道联名档),中文名待官方对照数据。
- 语音可建「VO bank 表」:141 代号 + bank_id + 所在包 + off/size(证据 skin_voice_bank_map.txt),转码播放需 ww2ogg(环境未装,未验证)。
- 天空盒/竞速赛季场景可与站内 4 地图/26 元素页面对照(s25/s26/s31 与版本公告赛季号呼应,但**本会话未做站内比对**,不做断言)。
