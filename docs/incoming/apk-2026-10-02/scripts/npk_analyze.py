#!/usr/bin/env python3
"""NXPK 格式分析器 — 分析网易 NeX 引擎 .npk 文件结构。

用法: python3 npk_analyze.py <file.npk> [max_frames]
输出: 头部字段、zstd 帧序列位置、每帧解压后首部内容预览。
"""
import struct
import sys
import os

ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"

def try_decompress_first(data: bytes, offset: int, out_len=128):
    """尝试在 offset 处解压一个 zstd 帧,返回 (成功?, 解压字节, 消耗的压缩字节)"""
    try:
        import compression.zstd as zstd
    except ImportError:
        return False, b"", 0
    # 用流式解压器逐块喂入,直到一帧结束
    try:
        dctx = zstd.ZstdDecompressor()
        chunk = 1 << 16
        out = b""
        pos = offset
        consumed = 0
        max_in = min(len(data) - offset, 32 << 20)
        # 流式读取: python 的 compression.zstd 提供 zstd stream reader
        # 简化方案: 截断式 —— 用 skippable 处理。这里用块喂法:
        # python 3.14 compression.zstd 没有逐步 feed API? 用 decompressobj
        obj = zstd.ZstdDecompressor().decompressobj()
        while pos < offset + max_in:
            piece = data[pos:pos + chunk]
            try:
                out += obj.decompress(piece)
            except Exception as e:
                # 一帧结束时可能抛 EOFError 或返回 eof 标志
                consumed = pos - offset
                return True, out[:out_len], consumed
            pos += chunk
            if obj.eof:
                consumed = pos - offset - chunk + 0
                return True, out[:out_len], consumed
        return True, out[:out_len], pos - offset
    except Exception as e:
        return False, str(e).encode(), 0

def analyze(path: str, max_frames: int = 12):
    with open(path, "rb") as f:
        head = f.read(0x40)
    size = os.path.getsize(path)
    print(f"=== {os.path.basename(path)} (size={size}) ===")
    magic = head[0:4]
    print(f"magic: {magic!r}")
    if magic != b"NXPK":
        print("不是 NXPK 格式, 跳过")
        return
    u32 = lambda o: struct.unpack_from("<I", head, o)[0]
    print(f"field@0x04 = {u32(4)}")
    print(f"field@0x08 = {u32(8)}")
    print(f"field@0x0C = {u32(0x0C)} (version?)")
    print(f"field@0x10 = {u32(0x10)}")
    print(f"field@0x14 = {u32(0x14)} (0x{u32(0x14):x})")
    print(f"field@0x18 = {u32(0x18)} (0x{u32(0x18):x})")
    print(f"field@0x1C = {u32(0x1C)} (0x{u32(0x1C):x})")

    with open(path, "rb") as f:
        data = f.read(min(size, 64 << 20))  # 最多读 64MB 用于帧扫描

    # 扫描前 N 个 zstd 帧魔数位置
    positions = []
    start = 0
    while len(positions) < max_frames:
        i = data.find(ZSTD_MAGIC, start)
        if i < 0:
            break
        positions.append(i)
        start = i + 1
    print(f"前 {len(positions)} 个 zstd 帧魔数偏移: {positions}")
    for n, p in enumerate(positions[:6]):
        ok, out, consumed = try_decompress_first(data, p)
        if ok:
            prev = out[:64]
            printable = all(32 <= b < 127 or b in (9, 10, 13) for b in prev[:32]) if prev else False
            print(f"  frame#{n} @{p:#x} consumed={consumed} out_len>= {len(out)} preview={prev[:48]!r} ascii={printable}")
        else:
            print(f"  frame#{n} @{p:#x} 解压失败: {out[:80]!r}")
    print()

if __name__ == "__main__":
    for p in sys.argv[1:]:
        analyze(p)
