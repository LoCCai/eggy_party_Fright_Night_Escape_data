#!/usr/bin/env python3
"""NeX 记录区(field→type schema 对 + 数值成分)探针 —— 2026-10-06 研判合并员追加。

在 npk_extract.py 提取产物上运行,用于复核 data-sources.md「APK 复核」节的以下结论:

1. NeX 二进制 = [u32 串数][u32×(串数+1) 偏移表][UTF-8 串池][记录区]
   (偏移表为 N+1 项,末项=串池总长;修正了 nex_kv_dump.py 把偏移表字节误读成 float 的问题)
2. 记录区成分(LEB128 varint 在 res/092383 验证:95 a0 80 80 04 = 1073745941,
   即该文件串池 '1073745941_uid' 的数字;其余在 res/092392 哑女钩爪配置上验证):
   - f32(前导 0x12)/f64(前导 0x22)与 typed array `27 <元素类型> <个数>`(27 12 03 = 3×f32)
   - 对象标记 `86 <varint>`;字母序 (field_idx, type_idx) schema 对
     (type: 0x12=f32 0x22=f64 0x05=字符串 0x0b/0x11=引用,已用 bite_stun_duration→f32、
      cd_time→f32、cast_sfx→字符串 语义校验通过)
3. 未解决:字段↔数值的端到端配对(数值区对象头/类映射未定)。
   已用已知答案否证两种朴素假设:
   - Fix32(16.16) 整数 varint(如 12.0=0xC0000 → 80 80 30)在 092392 记录区 0 命中;
   - wiki 数值 f32(冷却 12.0/眩晕 2.0)在记录区同样 0 命中 → 数值经公式/引用字段存储,
     不能用朴素共现或暴力扫描配对。拒绝把 ogc2_tick_delta_blood 等字段与 lambda 数值
     (Fix32(0.1) 等)直接配对入库。

用法:
  python3 nex_pair_probe.py <extract>/res/092392_*.bin   # 打印 schema 对 + Fix32/已知值探针
  python3 nex_pair_probe.py <extract>/res/092570_*.bin   # 海瑟 ogc2_* 同样探针(结论同上)
"""
import struct
import sys
import re


def load_pool(path):
    d = open(path, 'rb').read()
    n = struct.unpack_from('<I', d, 0)[0]
    offs = struct.unpack_from('<%dI' % (n + 1), d, 4)
    ps = 4 + (n + 1) * 4
    strings = [d[ps + offs[i]:ps + offs[i + 1]] for i in range(n)]
    rec_start = ps + offs[n]
    return d, strings, rec_start


def varint_len(b, p):
    n = 0
    while b[p + n] & 0x80:
        n += 1
    return n + 1


TYPE_NAMES = {0x01: 'bool/int8?', 0x03: 'list?', 0x05: 'str-ref', 0x0b: 'ref/varint?',
              0x11: 'id-ref', 0x12: 'f32', 0x22: 'f64'}


def probe(path):
    d, strings, rs = load_pool(path)
    reg = d[rs:]
    print(f"{path}: 串数={len(strings)} 记录区={len(reg)}B @0x{rs:x}")

    # 1) 已知值 varint/f32 探针(哑女钩爪 wiki 数值:冷却12s/眩晕2s/强化3s/3爪)
    for label, val in [('Fix32(12.0)=0xC0000', 12 * 65536), ('Fix32(2.0)', 2 * 65536),
                       ('Fix32(3.0)', 3 * 65536), ('Fix32(1.5)', 0x18000)]:
        v = val
        out = b''
        while True:
            x = v & 0x7f
            v >>= 7
            out += bytes([x | 0x80]) if v else bytes([x])
            if not v:
                break
        hits = [hex(m.start()) for m in re.finditer(re.escape(out), reg)]
        print(f"  {label:22s} varint {out.hex(' '):12s} → {len(hits)} 命中")
    for f in (12.0, 2.0, 3.0, 100.0):
        needle = struct.pack('<f', f)
        hits = [hex(m.start()) for m in re.finditer(re.escape(needle), reg)]
        print(f"  f32 {f:<6}                {needle.hex(' '):12s} → {len(hits)} 命中")

    # 2) uid varint 对照组(应命中,证明 varint 编码本身存在)
    uid = bytes([0x95, 0xA0, 0x80, 0x80, 0x04])  # 1073745941
    print(f"  uid 1073745941 varint     {uid.hex(' ')} → "
          f"{len(re.findall(re.escape(uid), reg))} 命中(对照组)")

    # 3) schema (field,type) 对游程探测:连续 ≥30 对 (idx<0x60, type∈已知类型)
    TYPES = {0x01, 0x03, 0x05, 0x0b, 0x11, 0x12, 0x22}
    for start in range(0x40, 0x400):
        p = start
        pairs = []
        for _ in range(30):
            if p + 1 >= len(reg) or reg[p] > 0x60 or reg[p + 1] not in TYPES:
                break
            pairs.append((reg[p], reg[p + 1]))
            p += 2
        if len(pairs) == 30:
            print(f"  schema 对游程 @记录区+0x{start:x}(示例,前 14 对):")
            for f, t in pairs[:14]:
                name = strings[f].decode('utf-8', 'replace') if f < len(strings) else f'?{f}'
                print(f"    {f:#04x} {name[:36]:38s} {t:#04x} {TYPE_NAMES.get(t, '?')}")
            break
    else:
        print("  未找到 schema 对游程(该文件可能无字母序 schema 段)")


if __name__ == '__main__':
    for p in sys.argv[1:]:
        probe(p)
