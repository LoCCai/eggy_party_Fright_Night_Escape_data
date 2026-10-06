#!/usr/bin/env python3
"""NeX NPK 提取器(无需文件表)。

原理(2026-10 对蛋仔派对 release-v1.16.1.4 逆向得出):
- 头 20 字节: 'NXPK' + 条目数(u32) + 0(u32) + 版本3(u32) + 文件表偏移(u32)
- 数据区 = 一串 zstd 帧;每帧 = [28b52ffd][FHD][FCS][块链][可选 0~3 字节填充]
- 文件表在包尾,蛋仔的表已整体加密(熵 8.0),故按帧扫描提取内容,文件名丢失。

用法: python3 npk_extract.py <in.npk> <out_dir> [--limit N]
"""
import os
import struct
import sys

ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"


def walk_frame(data: bytes, start: int, limit: int):
    """从 start(魔数处)走块链,返回 (帧结束偏移, 解压输出 bytes) 或 (None, 错误信息)"""
    import compression.zstd as z
    off = start + 4
    if off >= limit:
        return None, "truncated header"
    fhd = data[off]
    fcs_flag = fhd >> 6
    single = (fhd >> 5) & 1
    off += 1
    if not single:
        off += 1  # window descriptor
    # FCS 字段尺寸: flag0→0(无 single)/1(有 single), flag1→2, flag2→4, flag3→8
    fcs_size = {0: (1 if single else 0), 1: 2, 2: 4, 3: 8}[fcs_flag]
    off += fcs_size
    # 走块链
    while off + 3 <= limit:
        v = int.from_bytes(data[off:off + 3], "little")
        last = v & 1
        btype = (v >> 1) & 3
        bsize = v >> 3
        if btype == 3:
            return None, "reserved block type"
        off += 3 + (0 if btype == 1 else bsize)
        if off > limit:
            return None, "block overflow"
        if last:
            break
    else:
        return None, "no last block"
    frame = data[start:off]
    try:
        out = z.decompress(frame)
    except Exception as e:
        # 尝试去掉尾部填充(0~3 字节)
        for pad in (1, 2, 3, 4):
            try:
                out = z.decompress(data[start:off - pad])
                return off - pad, out
            except Exception:
                continue
        return None, f"decode fail: {e}"
    return off, out


def main(npk: str, outdir: str, limit_n: int = 0):
    os.makedirs(outdir, exist_ok=True)
    with open(npk, "rb") as f:
        data = f.read()
    count = struct.unpack_from("<I", data, 4)[0]
    table_off = struct.unpack_from("<I", data, 0x14)[0]
    print(f"{os.path.basename(npk)}: entries={count} table@{table_off:#x} size={len(data)}")
    # 扫魔数
    positions = []
    i = 0
    while True:
        j = data.find(ZSTD_MAGIC, i, table_off if table_off else len(data))
        if j < 0:
            break
        positions.append(j)
        i = j + 1
    print(f"found {len(positions)} zstd frames")
    if limit_n:
        positions = positions[:limit_n]
    ok = fail = 0
    manifest = []
    for n, p in enumerate(positions):
        end, out = walk_frame(data, p, table_off or len(data))
        if end is None:
            fail += 1
            manifest.append({"index": n, "offset": p, "error": out})
            continue
        ok += 1
        fn = os.path.join(outdir, f"{n:06d}_{p:08x}.bin")
        with open(fn, "wb") as f:
            f.write(out)
        manifest.append({"index": n, "offset": p, "frame_end": end,
                         "size": len(out), "file": os.path.basename(fn),
                         "head_hex": out[:16].hex()})
        if n < 5 or n % 100 == 0:
            print(f"  [{n}] @{p:#x} -> {len(out)} bytes head={out[:12]!r}")
    print(f"OK={ok} FAIL={fail}")
    import json
    with open(os.path.join(outdir, "_extract_manifest.json"), "w") as f:
        json.dump({"npk": npk, "entries_declared": count, "frames": len(positions),
                   "ok": ok, "fail": fail, "items": manifest}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    lim = 0
    args = [a for a in sys.argv[1:]]
    if "--limit" in args:
        i = args.index("--limit")
        lim = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    main(args[0], args[1], lim)
