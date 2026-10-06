#!/bin/bash
# 明文层关键词扫描 — 对 APK 解包后的文本类文件 grep 游戏关键词
# 用法: bash plaintext_scan.sh <apk_extract_dir> <out_dir>
set -u
APK="$1"; OUT="$2"
mkdir -p "$OUT"
# 关键词表(模式名|正则)
KEYWORDS=(
  "惊魂夜|惊魂夜"
  "逃出惊魂夜|逃出惊魂夜"
  "追捕者|追捕者"
  "逃生者|逃生者"
  "蒸汽炉|蒸汽炉"
  "爆米花|爆米花"
  "莉莉丝|莉莉丝"
  "海瑟|海瑟"
  "梵蒂娅|梵蒂娅"
  "影爪|影爪"
  "失血|失血"
  "痛楚领域|痛楚领域"
  "迅影索|迅影索"
  "念奴娇|念奴娇"
  "歌女|歌女"
  "FrightNight|FrightNight"
  "fright_night|fright_night"
  "hunter_battle|hunter_battle"
)
# 只扫文本类
FILES=$(find "$APK" -type f \( -name '*.json' -o -name '*.xml' -o -name '*.txt' -o -name '*.dat' -o -name '*.html' -o -name '*.js' -o -name '*.ini' -o -name '*.properties' -o -name '*.lst' -o -name '*.md' -o -name '*.rule' \) 2>/dev/null)
echo "scanning $(echo "$FILES" | wc -l) text files" > "$OUT/hits_summary.txt"
for kw in "${KEYWORDS[@]}"; do
  name="${kw%%|*}"; pat="${kw#*|}"
  hits=$(grep -F -c "$pat" $FILES 2>/dev/null | grep -v ':0$' || true)
  {
    echo "=== $name ==="
    if [ -n "$hits" ]; then
      echo "$hits"
    else
      echo "(no hits)"
    fi
  } >> "$OUT/hits_summary.txt"
done
# 上下文提取: 对命中的文件保存行级上下文
grep -F -o -h -E "(惊魂夜|追捕者|逃生者|蒸汽炉|爆米花|莉莉丝|海瑟|梵蒂娅|影爪|失血|痛楚领域|迅影索|念奴娇|歌女).{0,60}" $FILES 2>/dev/null | head -300 > "$OUT/context_samples.txt" || true
echo "done" >> "$OUT/hits_summary.txt"
