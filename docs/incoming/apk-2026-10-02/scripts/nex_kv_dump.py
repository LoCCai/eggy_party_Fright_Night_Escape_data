#!/usr/bin/env python3
"""NeX 二进制资源文件的字符串/数值提取器。

NeX 序列化文件包含: 属性名池(连续 ASCII)、UTF-8 中文文本、float/int 值。
本工具按顺序扫出全部可读串(>=4 字符)与 float 候选,按文件偏移交错输出,
用于人工判读 kv 对应关系。

用法: python3 nex_kv_dump.py <file.bin> [context_hex]
"""
import struct
import sys
import re

PRINTABLE = re.compile(rb'[\x20-\x7e\xe0-\xef][\x20-\x7e\x80-\xbf]{3,}')

def cjk_len(b: bytes) -> int:
    try:
        s = b.decode('utf-8', errors='ignore')
        return len(s)
    except Exception:
        return 0

def main(path, focus=None):
    d = open(path, 'rb').read()
    events = []
    for m in PRINTABLE.finditer(d):
        s = m.group()
        try:
            t = s.decode('utf-8')
        except UnicodeDecodeError:
            try:
                t = s.decode('gbk', errors='ignore')
            except Exception:
                continue
        if len(t) >= 4:
            events.append((m.start(), 'S', t))
    # float 候选: 单精度, 绝对值在 0.001..1e7 之间视为可读数值
    for i in range(0, len(d) - 4):
        (f,) = struct.unpack_from('<f', d, i)
        if f != 0 and 0.001 < abs(f) < 1e7 and abs(f - round(f, 4)) < 1e-9 or (0.001 < abs(f) < 1e7 and (abs(f) < 100 or f == int(f))):
            if abs(f) < 1e7 and (abs(f) >= 0.001):
                # 避免把指针当 float: 只在值"像"数值时记录
                events.append((i, 'F', repr(round(f, 6))))
    events.sort()
    # 合并相邻 float
    out = []
    skip_until = -1
    for off, kind, val in events:
        if off < skip_until:
            continue
        if kind == 'S':
            out.append((off, val))
            skip_until = off + len(val)
        else:
            out.append((off, val))
            skip_until = off + 4
    for off, val in out:
        if focus is not None and focus not in val:
            continue
        print(f"{off:#010x}  {val}")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
