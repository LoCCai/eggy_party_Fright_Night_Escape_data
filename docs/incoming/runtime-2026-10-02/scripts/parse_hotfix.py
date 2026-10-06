#!/usr/bin/env python3
"""Parse NeoX mcache hotfix files (msgpack of precompiled marshal modules)."""
import msgpack, sys, re, os

def walk(o, path="", out=None):
    if out is None: out = []
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, f"{path}/{k}", out)
    elif isinstance(o, (list, tuple)):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]", out)
    elif isinstance(o, bytes):
        out.append((path, o))
    elif isinstance(o, str):
        out.append((path, o.encode()))
    return out

def main(path):
    d = open(path,'rb').read()
    obj = msgpack.unpackb(d, raw=False, strict_map_key=False)
    entries = walk(obj)
    print(f"{os.path.basename(path)}: {len(entries)} leaf entries")
    for p, b in entries:
        name = p.split('/')[-1]
        if isinstance(b, bytes) and len(b) > 4:
            print(f"  {p}  bytes={len(b)} head={b[:24]!r}")
    return obj

if __name__ == '__main__':
    main(sys.argv[1])
