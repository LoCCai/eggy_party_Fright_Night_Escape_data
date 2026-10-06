#!/usr/bin/env python3
"""流式字节级扫描 NPK:逐帧解压,按 utf-8/utf-16-le 字节模式搜关键词,保存命中上下文。
用法: python3 scan_bytes.py <in.npk> <out.txt> <kwfile>"""
import sys, struct
import compression.zstd as z

ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"

def walk_frame(data, start, limit):
    off = start + 4
    if off >= limit: return None, "truncated"
    fhd = data[off]; fcs_flag = fhd >> 6; single = (fhd >> 5) & 1; off += 1
    if not single: off += 1
    fcs_size = {0: (1 if single else 0), 1: 2, 2: 4, 3: 8}[fcs_flag]
    off += fcs_size
    while off + 3 <= limit:
        v = int.from_bytes(data[off:off+3], "little")
        last = v & 1; btype = (v >> 1) & 3; bsize = v >> 3
        if btype == 3: return None, "reserved"
        off += 3 + (0 if btype == 1 else bsize)
        if off > limit: return None, "overflow"
        if last: break
    else:
        return None, "nolast"
    frame = data[start:off]
    try:
        return off, z.decompress(frame)
    except Exception:
        for pad in (1,2,3,4):
            try: return off-pad, z.decompress(data[start:off-pad])
            except Exception: continue
        return None, "decode"

def main(npk, out, kwfile):
    kws = [l.strip() for l in open(kwfile, encoding='utf-8').read().splitlines() if l.strip()]
    pats = [(kw, kw.encode('utf-8'), kw.encode('utf-16-le')) for kw in kws]
    data = open(npk,'rb').read()
    table_off = struct.unpack_from('<I', data, 0x14)[0]
    pos = []; i = 0
    while True:
        j = data.find(ZSTD_MAGIC, i, table_off or len(data))
        if j < 0: break
        pos.append(j); i = j + 1
    print(f"{npk}: {len(pos)} frames", flush=True)
    nhit = 0
    fo = open(out, 'w', encoding='utf-8')
    for n, p in enumerate(pos):
        end, out_b = walk_frame(data, p, table_off or len(data))
        if end is None: continue
        for kw, u8, u16 in pats:
            for enc, needle in (('u8', u8), ('u16', u16)):
                start = 0
                while True:
                    k = out_b.find(needle, start)
                    if k < 0: break
                    s = max(0, k-160); e = min(len(out_b), k+len(needle)+320)
                    ctx = out_b[s:e].decode('utf-8', errors='replace').replace('\x00','').replace('\n','\\n')
                    fo.write(f"frame{n:06d}@{p:#x} {enc} [{kw}] ...{ctx}...\n")
                    nhit += 1
                    start = k + 1
                    if nhit > 200000: break
    fo.close()
    print(f"hits={nhit}", flush=True)

main(sys.argv[1], sys.argv[2], sys.argv[3])
