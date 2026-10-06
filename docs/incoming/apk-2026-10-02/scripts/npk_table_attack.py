#!/usr/bin/env python3
"""对 NXPK 加密文件表做统计分析,判断加密类型并尝试恢复明文结构。

思路:
1. 高熵判定(卡方/字节分布)。
2. 重复密钥 XOR 检测: 按 mod keylen 分桶找最常见字节(利用表中大量 0x00)。
3. 若非 XOR,输出证据(熵、重复模式缺失)供报告使用。
"""
import struct
import sys
from collections import Counter

def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    c = Counter(data)
    n = len(data)
    import math
    return -sum((v / n) * math.log2(v / n) for v in c.values())

def xor_key_detect(data: bytes, max_keylen=64):
    """对每个候选 keylen,统计各桶最常见字节;若占比显著(>40%)则可疑。"""
    results = []
    for kl in range(1, max_keylen + 1):
        if len(data) < kl * 8:
            continue
        scores = []
        for pos in range(kl):
            col = data[pos::kl]
            top = Counter(col).most_common(1)[0]
            scores.append((top[1] / len(col), top[0]))
        avg = sum(s for s, _ in scores) / kl
        results.append((avg, kl, scores))
    results.sort(key=lambda x: -x[0])
    return results

def main(path: str):
    with open(path, "rb") as f:
        data = f.read()
    n = len(data)
    print(f"=== {path} (len={n}, = {n // 28} entries x 28 + {n % 28} remainder)")
    print(f"entropy = {entropy(data):.3f} bits/byte (8.0 = 随机)")
    # 28 字节对齐下各字段位置的字节分布
    for field, (off, ln) in {
        "id[0:4]": (0, 4), "offset[4:8]": (4, 4), "size[8:12]": (8, 4),
        "usize[12:16]": (12, 4), "u16[16:18]": (16, 2), "u32[20:24]": (20, 4),
        "comp[24:26]": (24, 2), "enc[26:27]": (26, 1), "pad[27:28]": (27, 1),
    }.items():
        col = b"".join(data[i + off:i + off + ln] for i in range(0, n - 27, 28))
        c = Counter(col).most_common(3)
        zeros = col.count(0) / len(col) if col else 0
        print(f"  {field:<14} zero%={zeros:.2%} top3={[hex(b) for b, _ in c]}")
    # XOR 重复密钥检测
    print("XOR keylen 检测 (avg top-freq / 1.0):")
    top5 = xor_key_detect(data[: 1 << 20])
    for avg, kl, scores in top5[:5]:
        print(f"  keylen={kl:<3} avg_top_freq={avg:.3f}")
        if avg > 0.35:
            key = bytes(b for _, b in scores)
            print(f"    -> 候选密钥(hex): {key.hex()}")
    # 尝试所有字节单字节 XOR 看是否出现 NXPK/路径类明文
    print("单字节 XOR 全表扫描 28 字节对齐结构假设: 无操作")

if __name__ == "__main__":
    main(sys.argv[1])
