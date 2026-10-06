#!/bin/bash
# 解包产物 UTF-8 关键词扫描 — 对 NPK 提取内容 grep 中文/英文关键词并保存命中与上下文
# 用法: bash npk_content_scan.sh <extract_root> <out_dir>
set -u
EX="$1"; OUT="$2"
mkdir -p "$OUT"
PAT='惊魂夜|逃出惊魂夜|追捕者|逃生者|蒸汽炉|爆米花|莉莉丝|海瑟|梵蒂娅|影爪|失血|痛楚领域|迅影索|念奴娇|歌女|FrightNight|fright_night|Fright_Night'
# 1) 命中文件清单(含次数)
rg -a -c -e "$PAT" "$EX" 2>/dev/null | sort -t: -k2 -rn > "$OUT/file_hits.txt"
# 2) 命中行+上下文(每文件前 40 条, 行截断 400 字节)
rg -a -o -e ".{0,80}($PAT).{0,120}" "$EX" 2>/dev/null \
  | awk '!seen[$1]++ || c[$1]++<40' > "$OUT/hit_contexts_raw.txt" 2>/dev/null || \
  rg -a -o -e ".{0,80}($PAT).{0,120}" "$EX" 2>/dev/null | head -20000 > "$OUT/hit_contexts_raw.txt"
# 3) 仅文本类命中的可读上下文(xml/json/txt/lua)
rg -a -l -e "$PAT" -g '*.bin' "$EX" 2>/dev/null | while read -r f; do
  if head -c 400 "$f" | LC_ALL=C grep -qa '<NeoX>\|{\|<?xml\|\[' ; then
    echo "$f" >> "$OUT/textlike_hits.txt"
  fi
done
wc -l "$OUT"/*.txt
