#!/usr/bin/env python3
"""Minimal LevelDB SSTable reader using ctypes libsnappy."""
import struct, os, sys, ctypes, ctypes.util

_snappy = ctypes.CDLL("libsnappy.so.1")
_snappy.snappy_uncompressed_length.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
_snappy.snappy_uncompress.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)]

def snappy_decompress(data):
    n = ctypes.c_size_t()
    _snappy.snappy_uncompressed_length(data, len(data), ctypes.byref(n))
    buf = ctypes.create_string_buffer(n.value)
    outlen = ctypes.c_size_t(n.value)
    rc = _snappy.snappy_uncompress(data, len(data), buf, ctypes.byref(outlen))
    if rc != 0: raise ValueError(f"snappy rc={rc}")
    return buf.raw[:outlen.value]

def get_varint(buf, pos):
    r = 0; s = 0
    while True:
        b = buf[pos]; pos += 1
        r |= (b & 0x7f) << s
        if not b & 0x80: break
        s += 7
    return r, pos

def read_block(d, off, size):
    raw = d[off:off+size]
    btype = raw[-5]
    data = raw[:-5]
    if btype == 1:
        data = snappy_decompress(data)
    elif btype != 0:
        raise ValueError(f"block type {btype}")
    return data

def entries_in_block(data):
    pos = 0; last_key = b''
    out = []
    n_restarts, = struct.unpack('<I', data[-4:])
    end = len(data) - 4 - n_restarts*4
    while pos < end:
        shared, pos = get_varint(data, pos)
        non_shared, pos = get_varint(data, pos)
        vlen, pos = get_varint(data, pos)
        key = last_key[:shared] + data[pos:pos+non_shared]; pos += non_shared
        val = data[pos:pos+vlen]; pos += vlen
        out.append((key, val))
        last_key = key
    return out

def parse_ldb(path):
    d = open(path,'rb').read()
    if len(d) < 48: return []
    magic, = struct.unpack('<Q', d[-48+40:])
    if magic != 0xdb4775248b80fb57: return None
    foot = d[-48:]
    _, p = get_varint(foot, 0)
    ioff, p = get_varint(foot, p); isize, p = get_varint(foot, p)
    idx = read_block(d, ioff, isize)
    results = []
    for key, val in entries_in_block(idx):
        off, p2 = get_varint(val, 0)
        size, _ = get_varint(val, p2)
        for k2, v2 in entries_in_block(read_block(d, off, size)):
            results.append((k2, v2))
    return results

def parse_log(path):
    """leveldb WAL .log: 32KB blocks, record header 4B crc + 2B len + 1B type"""
    d = open(path,'rb').read()
    out = []
    pos = 0
    full = b''
    while pos + 7 <= len(d):
        crc, ln, typ = struct.unpack('<IHB', d[pos:pos+7])
        if typ == 0 and ln == 0: break
        payload = d[pos+7:pos+7+ln]
        if typ == 1: full = payload
        elif typ == 2: full += payload  # first
        elif typ == 3: full += payload  # middle
        elif typ == 4:
            full += payload
            out.append(full); full = b''
        elif typ == 0: pass
        pos += 7 + ln
    if full: out.append(full)
    return out  # list of write batches (raw)

def decode_batch(b):
    # WriteBatch: 8B seq + 4B count, then records: 1B type, varint keylen, key, varint vallen, val
    if len(b) < 12: return []
    seq, = struct.unpack('<Q', b[:8]); cnt, = struct.unpack('<I', b[8:12])
    pos = 12; out = []
    for _ in range(cnt):
        try:
            typ = b[pos]; pos += 1
            klen, pos = get_varint(b, pos)
            key = b[pos:pos+klen]; pos += klen
            if typ == 1:
                out.append((key, None)); continue
            vlen, pos = get_varint(b, pos)
            val = b[pos:pos+vlen]; pos += vlen
            out.append((key, val))
        except Exception:
            break
    return out

if __name__ == '__main__':
    path = sys.argv[1]
    if path.endswith('.ldb'):
        r = parse_ldb(path)
        if r is None: print("not ldb"); sys.exit()
        print(f"{len(r)} entries")
        for k, v in r:
            print(repr(k)[:100], "=>", repr(v)[:200])
    elif path.endswith('.log'):
        for batch in parse_log(path):
            for k, v in decode_batch(batch):
                print(repr(k)[:100], "=>", repr(v)[:200])
