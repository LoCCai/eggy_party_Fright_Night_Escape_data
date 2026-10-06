#!/usr/bin/env python3
"""关键词全盘扫描(UTF-8/GBK/UTF-16LE),用于复现 keyword_hits.md 第 1-3 节。
用法: python3 keyword_scan.py <解压根目录> <npk解包输出目录>"""
import os, sys, json
KWS = ["惊魂夜","逃出","追捕者","逃生者","蒸汽炉","爆米花","莉莉丝","海瑟","礼温","梵蒂娅",
       "失血","痛楚领域","迅影索","影爪","歌女","念奴娇","暗影能量","斯黛拉","小阿娇","蓝慈",
       "赫拉","艾琳","雷蒙德","美狄亚","托兰","卢修斯","桑吉斯","克莱蕾","莫比","阿巴",
       "血月潮引","猩红日蚀","幽冥之爪","江南旧忆","游园惊梦","fright_night","idv"]
SKIP_EXT = ('.npk','.ppk','.ppkn')  # 包文件由 npk_zstd_walker.py 单独处理

def scan_plain(root):
    res = {}
    for r, _, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(r, fn)
            if fn.endswith(SKIP_EXT) or '.orbit.tmp' in fn: continue
            try:
                if os.path.getsize(p) > 60_000_000: continue
                d = open(p,'rb').read()
            except Exception: continue
            hits = {}
            for kw in KWS:
                kb = kw.encode('utf-8')
                if kw.isascii():
                    c = d.count(kb)
                else:
                    c = d.count(kb) + d.count(kw.encode('utf-16-le')) + d.count(kw.encode('gbk'))
                if c: hits[kw] = c
            if hits: res[os.path.relpath(p, root)] = hits
    return res

if __name__ == '__main__':
    root = sys.argv[1]
    res = scan_plain(root)
    json.dump(res, open(sys.argv[2],'w'), ensure_ascii=False, indent=1)
    print(f"{len(res)} files with hits -> {sys.argv[2]}")
