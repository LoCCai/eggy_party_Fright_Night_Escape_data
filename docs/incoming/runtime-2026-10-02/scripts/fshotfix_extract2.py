#!/usr/bin/env python3
"""Extract base64(KLUv)=zstd blobs + string tables from NeoX hotfix marshal blobs."""
import msgpack, sys, re, os, base64
from compression import zstd

path, outdir = sys.argv[1], sys.argv[2]
d = open(path,'rb').read()
obj = msgpack.unpackb(d, raw=True, strict_map_key=False)
scripts = obj[b'scripts']
os.makedirs(outdir, exist_ok=True)
print(f"scripts={len(scripts)} version={obj.get(b'version')!r}")

# map module hash -> real .py name from marshal filename string
def real_names(blob):
    # marshal strings: TYPE_SHORT_ASCII 'z'+len, TYPE_SHORT_ASCII_INTERNED 'z'... find 'N(....t' patterns; simpler: printable runs
    runs = re.findall(rb'[\x20-\x7e]{8,}', blob)
    return [r.decode() for r in runs]

for i, s in enumerate(scripts):
    blob = s[1]
    strings = real_names(blob)
    # real name heuristic: *_py / *_hotfix_*
    pyname = [x for x in strings if x.endswith('_py') or 'hotfix' in x.lower()][:3]
    # base64 zstd
    zn = 0
    for m in re.finditer(rb'[A-Za-z0-9_\-]{64,}', blob):
        seg = m.group()
        if not seg.startswith(b'KLUv'):
            continue
        pad = seg + b'=' * (-len(seg) % 4)
        try:
            raw = base64.b64decode(pad, altchars=b'_-')
            dec = zstd.decompress(raw)
        except Exception as e:
            continue
        zn += 1
        out = f"{outdir}/{i:03d}_{pyname[0] if pyname else 'mod'}.z{zn}.bin"
        open(out,'wb').write(dec)
        print(f"[{i}] {pyname} zstd@{m.start()} -> {len(dec)} bytes -> {out}")
    if not zn and pyname and any('fright' in x.lower() for x in strings):
        print(f"[{i}] FRIGHT module (no zstd): {pyname}")
        # dump strings
        strs = [x for x in strings if len(x) >= 6]
        open(f"{outdir}/{i:03d}_{pyname[0] if pyname else 'mod'}.strings.txt",'w').write('\n'.join(strs))
