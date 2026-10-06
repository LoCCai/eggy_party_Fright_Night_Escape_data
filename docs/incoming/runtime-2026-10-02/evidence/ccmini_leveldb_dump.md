# ccmini LevelDB 解析结果(全量)

解析器: scripts/ldbdump.py(自写 SSTable/WAL 读取,snappy 经 ctypes libsnappy;BlockHandle.size 不含 5B trailer)

### ccmini/db/onlineconfig/000019.ldb
- `agc2_adjacent_thresold` = `8`
- `agc2_level_estimator_attack` = `500`
- `agc2_level_estimator_decayr` = `10000`
- `agc2_level_estimator_hardroom` = `35`
- `agc2_level_estimator_threshold` = `-70`
- `agc2_max_gain_db` = `30`
- `agc2_max_processtime_interval` = `60000`
- `agc2_sensitive_factor` = `50`
- `agc2_target_dbfs` = `9`
- `android_device_configs` = `[{"devices":["HUAWEI DCO-AL00","HUAWEI CET-AL00"],"system":"HarmonyOS","min_sys_ver":"3.0.0.187","max_sys_ver":"*","back_sys_ver":"3.0.0","config":{"voip_playback_samplerate":32000}}]`
- `android_ec_mode` = `2`
- `android_enable_agc2` = `true`
- `db_vad_threshold` = `10`
- `dnn_ns_degraded_time` = `2`
- `dnn_ns_factor` = `2`
- `enable_aec3_replace_aec_mode2` = `true`
- `enable_db_vad` = `0`
- `enable_dpcrn_ns_cpu_least` = `4`
- `enable_dpcrn_ns_without_avx2` = `1`
- `enable_msgaudio_send_timestamp_grayscale` = `1`
- `enable_multi_bands_dpcrn_ns` = `1`
- `enable_multi_bands_dpcrn_ns_without_avx2` = `1`
- `fd_count_interval` = `120`
- `jitter_buffer_use_webrtc` = `100`
- `jitter_buffer_webrtc_mode` = `1`
- `kv_query_url` = `http://audioms.cc.163.com/v1/sdkctrl/get_configs`
- `llvm_use_poll_gray` = `100`
- `sdk_config_version` = `1767174518`
- `tmptmp` = `1`
(29 entries)

### ccmini/db/common/000005.ldb
- `kDbExistedKey` = `true`
- `kDeviceUuidStorageKey` = `2zh49akubyi6p20l`
(2 entries)

### ccmini/db/common/000020.ldb
- `kReportURLCacheKey` = `http://audiostatlog.cc.163.com/query`
- `kUserGameAppIDStorageKey` = `10162`
- `kUserUidStorageKey` = `166518579`
(3 entries)

### ccmini/res/res_db/000019.ldb
- `dpcrn_encrypted_performance.model` = `{
	"encryptedName":	"ed65502f06b1c69f05e63229376b24d2.model",
	"md5":	"c39f9aa48b7ef1caa95eb726d16e39a6",
	"compat":	0,
	"modifiedTime":	"1770542439"
}`
- `dpcrn_encrypted_performance_16k.model` = `{
	"encryptedName":	"b42de8e19e2e490fd709fafd2d34d03b.model",
	"md5":	"d07193157a3ed7cf1ef3fb2b5707b1dd",
	"compat":	0,
	"modifiedTime":	"1770542439"
}`
- `dpcrn_encrypted_quality.model` = `{
	"encryptedName":	"d14d170dab11b97737adade23839953b.model",
	"md5":	"fc49a1227fa9dc12dd4893685afc4eb3",
	"compat":	0,
	"modifiedTime":	"1770542438"
}`
- `dpcrn_encrypted_quality_16k.model` = `{
	"encryptedName":	"5432320c9059e53ee24f2dcf5996c46e.model",
	"md5":	"9961e8ee5f11b79483421ee8e9688f74",
	"compat":	0,
	"modifiedTime":	"1770542440"
}`
- `file_list` = `[{
		"compat":	0,
		"size":	920788,
		"updatetime":	"2026-02-08 17:20:00",
		"appids":	[],
		"uids":	[],
		"file_version":	"1713252904",
		"filename":	"dpcrn_encrypted_quality.model",
		"https_download":	"https://cc.fp.ps.netease.com/file/661e2a2835ad5bf918172410Hq5HbOmt05",
		"version":	"2.2.4",
		"max_version":	"",
		"up_compatible":	1,
		"download":	"http://cc.fp.ps.netease.com/file/661e2a2835ad5bf918172410Hq5HbOmt05",
		"os_type":	["all"],
		"uidends":	[],
		"md5":	"fc49a1227fa9dc12dd4893685afc4eb3"
	}, {
		"compat":	0,
		"size":	428704,
		"updatetime":	"2026-02-08 17:20:00",
		"appids":	[],
		"uids":	[],
		"file_version":	"1713252933",
		"filename":	"dpcrn_encrypted_performance.model",
		"https_download":	"https://cc.fp.ps.netease.com/file/661e2a457f7b7a41a44d1dc8xlwZaatC05",
		"version":	"2.2.4",
		"max_version":	"",
		"up_compatible":	1,
		"download":	"http://cc.fp.ps.netease.com/file/661e2a457f7b7a41a44d1dc8xlwZaatC05",
		"os_type":	["all"],
		"uidends":	[],
		"md5":	"c39f9aa48b7ef1caa95eb726d16e39a6"
	}, {
		"compat":	0,
		"size":	458020,
		"updatetime":	"2026-02-08 17:20:00",
		"appids":	[],
		"uids":	[],
		"file_version":	"1740729980",
		"filename":	"dpcrn_encrypted_performance_16k.model",
		"https_download":	"https://cc.fp.ps.netease.com/file/67c16e7c054d77db7b2fe822GFYTt5Uy06",
		"version":	"2.2.4",
		"max_version":	"",
		"up_compatible":	1,
		"download":	"http://cc.fp.ps.netease.com/file/67c16e7c054d77db7b2fe822GFYTt5Uy06",
		"os_type":	["all"],
		"uidends":	[],
		"md5":	"d07193157a3ed7cf1ef3fb2b5707b1dd"
	}, {
		"compat":	0,
		"size":	920788,
		"updatetime":	"2026-02-08 17:20:00",
		"appids":	[],
		"uids":	[],
		"file_version":	"1740730010",
		"filename":	"dpcrn_encrypted_quality_16k.model",
		"https_download":	"https://cc.fp.ps.netease.com/file/67c16e999f531c401a969d64MVHWVtM606",
		"version":	"2.2.4",
		"max_version":	"",
		"up_compatible":	1,
		"download":	"http://cc.fp.ps.netease.com/file/67c16e999f531c401a969d64MVHWVtM606",
		"os_type":	["all"],
`
(5 entries)

## .log(WAL)
- onlineconfig/000046.log、common/000047.log、res_db/000046.log:0 条有效记录(空 WAL)。

## 结论
ccmini 为网易语音/音频 SDK 配置库:onlineconfig=音频引擎开关(agc2/dnn_ns/jitter_buffer/webrtc,配置源 audioms.cc.163.com,sdk_config_version=1767174518);common=设备 UUID(kDeviceUuidStorageKey=2zh49akubyi6p20l)、上报 URL(audiostatlog.cc.163.com)、UserGameAppID=10162、UserUid=166518579;res_db=语音降噪模型索引(dpcrn *.model md5/file_list)。**无玩法开关/功能开关/玩法远程配置,无惊魂夜相关内容。**