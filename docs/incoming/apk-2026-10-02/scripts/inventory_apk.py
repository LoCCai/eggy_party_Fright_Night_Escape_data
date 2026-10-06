#!/usr/bin/env python3
"""蛋仔派对 APK 解包盘点脚本 — 统计 5377 个条目按扩展名/目录分类。

用法: python3 inventory_apk.py <extracted_apk_dir> <out_dir>
输出: <out_dir>/inventory.json / inventory_by_ext.txt / inventory_tree.txt
"""
import json
import os
import sys
from collections import Counter

def main(root: str, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    files = []
    total_bytes = 0
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            try:
                sz = os.path.getsize(p)
            except OSError:
                sz = -1
            files.append((rel, sz))
            total_bytes += max(sz, 0)

    by_ext = Counter()
    by_ext_bytes = Counter()
    by_top = Counter()
    by_top_bytes = Counter()
    for rel, sz in files:
        ext = os.path.splitext(rel)[1].lower() or "(noext)"
        top = rel.split(os.sep)[0]
        by_ext[ext] += 1
        by_ext_bytes[ext] += max(sz, 0)
        by_top[top] += 1
        by_top_bytes[top] += max(sz, 0)

    inv = {
        "apk_root": root,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "by_extension": {
            e: {"count": by_ext[e], "bytes": by_ext_bytes[e]}
            for e in sorted(by_ext, key=lambda x: -by_ext_bytes[x])
        },
        "by_top_dir": {
            t: {"count": by_top[t], "bytes": by_top_bytes[t]}
            for t in sorted(by_top, key=lambda x: -by_top_bytes[x])
        },
    }
    with open(os.path.join(out_dir, "inventory.json"), "w", encoding="utf-8") as f:
        json.dump(inv, f, ensure_ascii=False, indent=2)

    with open(os.path.join(out_dir, "inventory_by_ext.txt"), "w", encoding="utf-8") as f:
        f.write(f"{'ext':<12}{'count':>8}{'bytes':>16}\n")
        for e, c in by_ext.most_common():
            f.write(f"{e:<12}{c:>8}{by_ext_bytes[e]:>16}\n")
        f.write(f"{'TOTAL':<12}{len(files):>8}{total_bytes:>16}\n")

    # 二级目录树(assets 重点展开)
    lvl2 = Counter()
    for rel, sz in files:
        parts = rel.split(os.sep)
        key = "/".join(parts[:2]) if len(parts) > 2 else parts[0]
        lvl2[key] += 1
    with open(os.path.join(out_dir, "inventory_tree.txt"), "w", encoding="utf-8") as f:
        for k, c in sorted(lvl2.items(), key=lambda x: -x[1]):
            f.write(f"{c:>8}  {k}\n")

    # 大文件 top100
    with open(os.path.join(out_dir, "inventory_top100.txt"), "w", encoding="utf-8") as f:
        for rel, sz in sorted(files, key=lambda x: -x[1])[:100]:
            f.write(f"{sz:>16}  {rel}\n")

    print(f"files={len(files)} bytes={total_bytes} extensions={len(by_ext)}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
