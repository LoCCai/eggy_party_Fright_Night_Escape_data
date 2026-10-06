#!/usr/bin/env python3
"""Brute-force keystream start offset: decrypt NPK table with EXPK moba keystream
starting at index k; check structural plausibility of entries."""
import struct, sys
sys.path.insert(0, '/home/eggy-test/work')
from npktry import gen_keys

KS = gen_keys(2_000_000)

def plausible(e, fsize):
    sign, off, ln, oln, zcrc, crc, flag = e
    return (24 <= off < fsize and 0 < ln <= fsize and off + ln <= fsize
            and 0 <= oln < 64_000_000 and (flag & 0xffff) in (0,1,2,3) and (flag >> 16) in (0,1,2,3))

def scan(path):
    d = open(path,'rb').read()
    count, = struct.unpack_from('<I', d, 4)
    map_off, = struct.unpack_from('<I', d, 0x14)
    fsize = len(d)
    tbl = d[map_off:map_off+28*4]
    hits = []
    for k in range(0, 1_000_000):
        e = struct.unpack('<7I', bytes(a^b for a,b in zip(tbl[:28], KS[k:k+28])))
        if plausible(e, fsize):
            # verify second entry too
            e2 = struct.unpack('<7I', bytes(a^b for a,b in zip(tbl[28:56], KS[k+28:k+56])))
            if plausible(e2, fsize):
                hits.append((k, e, e2))
                if len(hits) <= 5:
                    print(f"  candidate k={k}: e0={[hex(x) for x in e]}")
    print(f"{path.split('/')[-1]}: candidates={len(hits)}")
    return hits

for p in sys.argv[1:]:
    scan(p)
