#!/usr/bin/env python3
"""
NPK 内嵌 Wwise bank 身份映射器(本会话新增)。

背景:ext_packer_skin_voice_1/3 的 NXPK 数据区不是 zstd 帧链,而是 940/794 个
裸 Wwise SoundBank 顺序拼接(BKHD+HIRC/DIDX/DATA)。bank 名在包内不存在(无 STID
块),只有 32 位数字 bank_id;但 Wwise 用 FNV-1(lower 32)对 bank 名小写做散列,
因此可以用「从其他解包包里收割的资源名(wwise/*.bnk 引用、实体代号)」生成候选名,
对撞出 bank 名。本次实测 175 个收割引用名命中 120 个,voice bank 命名规律
`<角色代号>_vo` 据此批量还原(共 141 个)。

用法:
  python3 npk_wwise_bank_mapper.py <npk 文件或任意含 BKHD 的文件> \
      [--harvest-dir 解包文件目录 ...] [--out 输出.txt]
"""
import struct, re, os, sys, collections

FNV_OFFSET = 0x811c9dc5
FNV_PRIME = 0x01000193

def fnv1_lower(s: str) -> int:
    """Wwise bank/event ID:FNV-1,输入先转小写,取 lower 32 位。"""
    h = FNV_OFFSET
    for b in s.encode().lower():
        h = (h * FNV_PRIME) & 0xFFFFFFFF
        h ^= b
    return h

def find_banks(data: bytes):
    """返回 [(offset, size, bank_id)];按 BKHD 边界切分。"""
    offs, i = [], 0
    while True:
        j = data.find(b'BKHD', i)
        if j < 0: break
        offs.append(j); i = j + 4
    out = []
    for n, o in enumerate(offs):
        end = offs[n + 1] if n + 1 < len(offs) else len(data)
        bid, = struct.unpack_from('<I', data, o + 12)  # BKHD: ver u32 @+8, id u32 @+12
        out.append((o, end - o, bid))
    return out

def harvest_candidates(dirs):
    """从解包文件目录收割候选名并生成变体(_vo/.bnk/wwise 前缀)。"""
    toks = set()
    tokpat = re.compile(r'[A-Za-z][A-Za-z0-9_]{2,30}')
    for d in dirs:
        for fn in os.listdir(d):
            data = open(os.path.join(d, fn), 'rb').read()
            for m in re.finditer(rb'[\w/\\.\-]{4,}', data):
                toks.update(tokpat.findall(m.group().decode('ascii', 'ignore')))
    variants = set()
    for t in toks:
        tl = t.lower()
        variants |= {tl, tl + '_vo', tl + '.bnk',
                     'wwise/' + tl + '.bnk', 'wwise/chinese/' + tl + '.bnk',
                     'wwise/chinese/' + tl + '_vo.bnk'}
    return variants

def main():
    path = sys.argv[1]
    data = open(path, 'rb').read()
    harvest = [a for a in sys.argv[2:] if a != '--out']
    out = None
    if '--out' in sys.argv:
        out = sys.argv[sys.argv.index('--out') + 1]
        harvest.remove(out)
    banks = find_banks(data)
    hm = collections.defaultdict(list)
    for v in harvest_candidates(harvest):
        hm[fnv1_lower(v)].append(v)
    named = unknown = 0
    lines = [f"== {os.path.basename(path)}: {len(banks)} banks"]
    for off, sz, bid in banks:
        cands = hm.get(bid)
        if cands:
            named += 1
            lines.append(f"  {cands[0]:44s} bank_id={bid:#010x} off={off:#010x} size={sz:>9d}")
        else:
            unknown += 1
            lines.append(f"  {'<unknown>':44s} bank_id={bid:#010x} off={off:#010x} size={sz:>9d}")
    lines.append(f"named={named} unknown={unknown}")
    text = '\n'.join(lines)
    print(f"named={named} unknown={unknown}")
    if out:
        open(out, 'w').write(text)

if __name__ == '__main__':
    main()
