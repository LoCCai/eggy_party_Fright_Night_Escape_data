#!/usr/bin/env python3
"""
NPK 解包产物多编码关键词扫描器(本会话新增)。

对解出的帧文件目录与原始 npk 字节流,用 UTF-8 / UTF-16LE / UTF-16BE / GBK
四种编码扫描关键词(NXPK 数据区里可能有任意编码文本;仅 UTF-8 会漏 UTF-16)。
输出命中文件与编码;对 2~4 字节的短模式命中务必人工核验上下文——
压缩/二进制数据中存在随机碰撞(上轮 runtime-2026-10-02 与本轮均验证过)。

用法:
  python3 npk_multiscan_keywords.py <关键词逗号分隔> <目录或.npk文件> ...
"""
import os, sys

ENCODE = {
    'utf8': lambda s: s.encode('utf-8'),
    'utf16le': lambda s: s.encode('utf-16-le'),
    'utf16be': lambda s: s.encode('utf-16-be'),
    'gbk': lambda s: s.encode('gbk'),
}

def scan(kws, targets):
    pats = {kw: {e: fn(kw) for e, fn in ENCODE.items()} for kw in kws}
    hits = {kw: [] for kw in kws}
    for t in targets:
        paths = []
        if os.path.isdir(t):
            paths = [os.path.join(t, f) for f in os.listdir(t)]
        else:
            paths = [t]
        for p in paths:
            data = open(p, 'rb').read()
            for kw in kws:
                for e, pat in pats[kw].items():
                    if pat in data:
                        hits[kw].append((p, e))
    return hits

if __name__ == '__main__':
    kws = sys.argv[1].split(',')
    hits = scan(kws, sys.argv[2:])
    for kw in kws:
        h = hits[kw]
        tag = f"HIT  {kw}: {len(h)}" if h else f"ZERO {kw}"
        print(tag)
        for p, e in h[:12]:
            print(f"      {p} [{e}]")
    if not any(hits.values()):
        print("(all zero —— 与 runtime-2026-10-02 结论一致:文本表不在资源包,在加密 script.npk 与服务器侧)")
