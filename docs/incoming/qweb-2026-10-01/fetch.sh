#!/usr/bin/env bash
# fetch.sh — 抓取 qweb.icai.top 社区「惊魂夜/逃出惊魂夜」相关帖子(列表翻页 + 详情正文)并存档。
#
# 数据源:
#   ds     — 主源,query=惊魂夜 与 query=逃出惊魂夜 分别翻页,按 id 去重合并
#   taptap — 探测发现可用,同样两个 query 全量抓取
#   4399   — 三个 query(惊魂夜/逃出惊魂夜/蛋仔派对)探测记录命中数(均为 0)
#
# 产物(写入脚本所在目录,可用 QWEB_OUT_DIR 覆盖):
#   posts-ds.json      ds 源帖子数组(列表字段 + 详情 content_blocks/body_text 合并)
#   posts-taptap.json  taptap 源同上
#   posts-4399.json    4399 源(空数组,接口可用但无命中)
#   manifest.json      抓取时间、各源 total/抓取数、去重说明、接口样例
#
# 图片(官方账号「蛋仔派对」发布的更新公告类帖子,不进仓库):
#   /tmp/qweb_images/*.png|jpg|webp   (可用 QWEB_IMG_DIR 覆盖;总量上限 300、单帖上限 12)
#   /tmp/qweb_images/manifest-images.json  每张图所属帖子 id 等记录
#
# 所有 HTTP 请求均由 curl 发起;python3 仅做 JSON 解析/合并/清单组装。
# 用法: bash fetch.sh
set -uo pipefail

BASE="https://qweb.icai.top/qweb/api/v1/public/community"
# 媒体字段(local_url/cover_url)是站点绝对路径 /qweb/api/...,要拼在站点根而非 API 根之后
SITE="${BASE%%/qweb/api*}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="${QWEB_OUT_DIR:-$SCRIPT_DIR}"
IMG_DIR="${QWEB_IMG_DIR:-/tmp/qweb_images}"
MAX_IMAGES="${QWEB_MAX_IMAGES:-300}"
MAX_PER_POST="${QWEB_MAX_PER_POST:-12}"
PAGE_SIZE=50
MAX_PAGES=25          # 单个 (源,query) 翻页上限(50*25=1250,远大于各 query total)
PARALLEL=4            # 详情抓取并发
UA="Mozilla/5.0 (X11; Linux x86_64) qweb-fright-night-archive/1.0 (curl)"
FETCHED_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
WORK="$(mktemp -d /tmp/qweb_fetch.XXXXXX)"
mkdir -p "$OUT" "$IMG_DIR" "$WORK/list" "$WORK/detail" "$WORK/probe"
trap 'rm -rf "$WORK"' EXIT

log() { echo "[fetch.sh $(date -u '+%H:%M:%S')] $*"; }

# curl GET -> 文件,返回 HTTP code;失败(网络错误/非 200)自动重试 3 次
http_get() { # $1=url $2=outfile
  local url="$1" out="$2" code="" attempt
  for attempt in 1 2 3; do
    code="$(curl -sS -m 45 -A "$UA" -o "$out" -w '%{http_code}' "$url" 2>>"$WORK/curl_err.log")" || code="000"
    if [ "$code" = "200" ]; then
      sleep 0.15
      return 0
    fi
    echo "HTTP $code $url (attempt $attempt)" >> "$WORK/http_failures.log"
    sleep "$((attempt * 2))"
  done
  rm -f "$out"
  return 1
}

# ---------- 阶段 0:探测各源可用性(4399 三 query;另记录 taptap query=蛋仔派对 total,不抓取) ----------
log "阶段 0:探测 4399 / taptap 可用性"
probe_source() { # $1=src $2=encoded_query $3=tag
  local f="$WORK/probe/$3.json"
  if http_get "$BASE/$1/posts?page=1&page_size=$PAGE_SIZE&query=$2" "$f"; then
    python3 -c "import json;d=json.load(open('$f'));print(d.get('source','?'),d.get('total','?'))" 2>/dev/null || echo "parse-error"
  else
    echo "unreachable"
  fi
}
probe_source 4399  "%E6%83%8A%E9%AD%82%E5%A4%9C"                  4399-jinghongye > "$WORK/probe/4399.txt"
probe_source 4399  "%E9%80%83%E5%87%BA%E6%83%8A%E9%AD%82%E5%A4%9C" 4399-taochu     > "$WORK/probe/4399_taochu.txt"
probe_source 4399  "%E8%9B%8B%E4%BB%94%E6%B4%BE%E5%AF%B9"         4399-danzai     > "$WORK/probe/4399_danzai.txt"
probe_source taptap "%E8%9B%8B%E4%BB%94%E6%B4%BE%E5%AF%B9"        taptap-danzai   > "$WORK/probe/taptap_danzai.txt"
log "探测: 4399惊魂夜=$(cat "$WORK/probe/4399.txt") 4399逃出惊魂夜=$(cat "$WORK/probe/4399_taochu.txt") 4399蛋仔派对=$(cat "$WORK/probe/4399_danzai.txt") taptap蛋仔派对=$(cat "$WORK/probe/taptap_danzai.txt")"

# ---------- 阶段 1:列表翻页(ds、taptap 各两个 query) ----------
fetch_list() { # $1=源 $2=已编码query $3=标签
  local src="$1" q="$2" tag="$3" page=1 n f
  mkdir -p "$WORK/list/$tag"
  while [ "$page" -le "$MAX_PAGES" ]; do
    f="$WORK/list/$tag/p$page.json"
    if ! http_get "$BASE/$src/posts?page=$page&page_size=$PAGE_SIZE&query=$q" "$f"; then
      log "列表抓取失败:$tag 第 $page 页(已重试 3 次),停止该 query"
      break
    fi
    n="$(python3 -c "import json;print(len(json.load(open('$f')).get('items',[])))" 2>/dev/null || echo 0)"
    [ "$n" = "0" ] && break
    page=$((page + 1))
  done
  echo "$((page - 1))"
}
log "阶段 1:列表翻页"
DS_PAGES_JH="$(fetch_list ds     "%E6%83%8A%E9%AD%82%E5%A4%9C"                  ds-jinghongye)"
DS_PAGES_TC="$(fetch_list ds     "%E9%80%83%E5%87%BA%E6%83%8A%E9%AD%82%E5%A4%9C" ds-taochu)"
TT_PAGES_JH="$(fetch_list taptap "%E6%83%8A%E9%AD%82%E5%A4%9C"                  taptap-jinghongye)"
TT_PAGES_TC="$(fetch_list taptap "%E9%80%83%E5%87%BA%E6%83%8A%E9%AD%82%E5%A4%9C" taptap-taochu)"
log "页数: ds惊魂夜=$DS_PAGES_JH ds逃出惊魂夜=$DS_PAGES_TC taptap惊魂夜=$TT_PAGES_JH taptap逃出惊魂夜=$TT_PAGES_TC"

# ---------- 阶段 2:按源按 id 去重 ----------
python3 - "$WORK" <<'PYEOF'
import json, sys, glob, os
work = sys.argv[1]
stats = {}
for src, tags in (("ds", ["ds-jinghongye", "ds-taochu"]), ("taptap", ["taptap-jinghongye", "taptap-taochu"])):
    per_tag, items_by_id = {}, {}
    for tag in tags:
        files = sorted(glob.glob(f"{work}/list/{tag}/p*.json"),
                       key=lambda p: int(p.rsplit("p", 1)[1].split(".")[0]))
        seen = []
        for fp in files:
            try:
                d = json.load(open(fp))
            except Exception:
                continue
            for it in d.get("items", []):
                pid = str(it.get("id"))
                seen.append(pid)
                if pid in items_by_id:
                    items_by_id[pid]["from_tags"].append(tag)
                else:
                    items_by_id[pid] = {"id": pid, "item": it, "from_tags": [tag]}
        per_tag[tag] = {"pages": len(files), "raw_ids": len(seen), "raw_ids_unique": len(set(seen))}
        if files:  # 记录接口自报的 total(取第一页响应的 total 字段)
            try:
                per_tag[tag]["api_total"] = json.load(open(files[0])).get("total")
            except Exception:
                pass
    os.makedirs(f"{work}/ids", exist_ok=True)
    open(f"{work}/ids/{src}.txt", "w").write("\n".join(items_by_id.keys()))
    json.dump(items_by_id, open(f"{work}/ids/{src}.json", "w"), ensure_ascii=False)
    stats[src] = {"queries": per_tag, "unique": len(items_by_id)}
json.dump(stats, open(f"{work}/dedup_stats.json", "w"), ensure_ascii=False, indent=1)
PYEOF
log "阶段 2 去重:$(python3 -c "import json;d=json.load(open('$WORK/dedup_stats.json'));print({s:v['unique'] for s,v in d.items()})")"

# ---------- 阶段 3:抓详情(含完整正文 content_blocks/body_text) ----------
export WORK BASE UA
fetch_detail() { # $1=post_id $2=source
  local id="$1" src="$2"
  local f="$WORK/detail/$src/$id.json"   # 注意:必须单独一行 —— 同一 local 行内后续赋值引用不到前面的赋值
  local code attempt
  mkdir -p "$WORK/detail/$src"
  [ -s "$f" ] && return 0
  for attempt in 1 2 3; do
    code="$(curl -sS -m 45 -A "$UA" -o "$f" -w '%{http_code}' "$BASE/$src/posts/$id?comment_page=1" 2>>"$WORK/curl_err.log")" || code="000"
    if [ "$code" = "200" ]; then sleep 0.12; return 0; fi
    sleep "$attempt"
  done
  echo "$src $id HTTP=$code" >> "$WORK/detail_failures.txt"
  rm -f "$f"
  return 0
}
export -f fetch_detail
log "阶段 3:抓取详情(并发 $PARALLEL)"
for src in ds taptap; do
  [ -s "$WORK/ids/$src.txt" ] || continue
  xargs -P "$PARALLEL" -I{} bash -c 'fetch_detail "$1" "'"$src"'"' _ {} < "$WORK/ids/$src.txt"
done
DETAIL_FAILS=0
[ -f "$WORK/detail_failures.txt" ] && DETAIL_FAILS=$(wc -l < "$WORK/detail_failures.txt")
log "详情抓取完成,失败 $DETAIL_FAILS 条"

# ---------- 阶段 4:合并落盘 posts-{src}.json ----------
python3 - "$WORK" "$OUT" "$FETCHED_AT" <<'PYEOF'
import json, sys, os
work, out, fetched_at = sys.argv[1:4]
merge_stats = {}
for src in ("ds", "taptap", "4399"):
    items_by_id = {}
    if os.path.exists(f"{work}/ids/{src}.json"):
        items_by_id = json.load(open(f"{work}/ids/{src}.json"))
    posts, details_ok, details_missing = [], 0, 0
    for pid, rec in items_by_id.items():
        merged = dict(rec["item"])
        df = f"{work}/detail/{src}/{pid}.json"
        if os.path.exists(df):
            try:
                dp = json.load(open(df)).get("post") or {}
                for k, v in dp.items():          # 详情字段覆盖列表字段(以详情为准)
                    merged[k] = v
                details_ok += 1
            except Exception:
                details_missing += 1
        else:
            details_missing += 1
        merged["_archived_from_queries"] = rec.get("from_tags", [])
        merged["_archived_at"] = fetched_at
        posts.append(merged)
    posts.sort(key=lambda p: str(p.get("published_at") or ""), reverse=True)
    json.dump(posts, open(f"{out}/posts-{src}.json", "w"), ensure_ascii=False, indent=1)
    merge_stats[src] = {"unique": len(posts), "details_merged": details_ok, "details_missing": details_missing}
json.dump(merge_stats, open(f"{work}/merge_stats.json", "w"), ensure_ascii=False, indent=1)
PYEOF
log "阶段 4 合并落盘:$(cat "$WORK/merge_stats.json" | python3 -c "import json,sys;print(json.load(sys.stdin))")"

# ---------- 阶段 5:图片 —— 官方账号「蛋仔派对」发布的更新公告类帖子 ----------
# 选帖规则:author.nickname=="蛋仔派对"(或 identity 含「官方」),且 title/summary/body_text
# 命中公告类关键词(更新/维护/公告/版本/平衡/赛季/上线/修复/新增/调整/优化/前瞻/爆料/预告/解封/活动/福利/礼包/返场/周年/礼包码)。
# 按 published_at 倒序取帖,单帖最多 12 张,全局上限 300 张;逐图记录所属帖子 id。
log "阶段 5:筛选官方公告帖并生成图片下载计划"
python3 - "$OUT" "$IMG_DIR" "$MAX_IMAGES" "$MAX_PER_POST" > "$WORK/img_plan.tsv" <<'PYEOF'
import json, sys, re, os
out, img_dir, max_total, max_per_post = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
KW = re.compile(r"更新|维护|公告|版本|平衡|赛季|上线|修复|新增|调整|优化|前瞻|爆料|预告|解封|活动|福利|礼包|返场|周年")
EXT_OK = {"png", "jpg", "jpeg", "webp", "gif"}
total = 0
for src in ("ds", "taptap"):
    posts = json.load(open(f"{out}/posts-{src}.json"))
    for p in posts:
        a = p.get("author") or {}
        official = (a.get("nickname") == "蛋仔派对") or ("官方" in (a.get("identity") or ""))
        text = " ".join(str(p.get(k) or "") for k in ("title", "summary", "body_text"))
        if not (official and KW.search(text)):
            continue
        urls = [b.get("local_url") for b in (p.get("content_blocks") or [])
                if isinstance(b, dict) and b.get("type") == "image" and b.get("local_url")]
        if not urls:
            continue
        for i, u in enumerate(urls[:max_per_post], 1):
            if total >= max_total:
                break
            ext = os.path.splitext(u)[1].lstrip(".").lower()
            ext = ext if ext in EXT_OK else "bin"
            print(f"{src}\t{p['id']}\t{i}\t{u}\t{img_dir}/{p['id']}_{i:02d}.{ext}")
            total += 1
        if total >= max_total:
            break
    if total >= max_total:
        break
PYEOF
IMG_TOTAL=$(wc -l < "$WORK/img_plan.tsv" | tr -d ' ')
log "图片计划 $IMG_TOTAL 张,开始下载到 $IMG_DIR"
: > "$WORK/img_results.tsv"
download_images() {
  local src pid idx url dest code magic real_ext want dl_url
  while IFS=$'\t' read -r src pid idx url dest; do
    case "$url" in
      http*)   dl_url="$url" ;;
      /qweb/*) dl_url="${SITE}${url}" ;;   # 站点绝对路径(媒体字段均为此形态)
      *)       dl_url="${BASE}/${url#/}" ;;
    esac
    code="$(curl -sS -m 45 -A "$UA" -o "$dest" -w '%{http_code}' "$dl_url" 2>>"$WORK/curl_err.log")" || code="000"
    magic="$(head -c 4 "$dest" 2>/dev/null | od -An -tx1 | tr -d ' \n')"
    case "$magic" in
      89504e47) real_ext="png" ;; 47494638) real_ext="gif" ;;
      ffd8ff*)  real_ext="jpg" ;;
      52494646) real_ext="webp" ;; # RIFF(WebP 头含 RIFF)
      *)
        echo -e "$src\t$pid\t$idx\t$dl_url\tFAIL\t$code\tbad_magic:$magic" >> "$WORK/img_results.tsv"
        rm -f "$dest"; continue ;;
    esac
    # 按真实格式改名
    want="${dest%.*}.$real_ext"
    [ "$want" != "$dest" ] && mv -f "$dest" "$want" && dest="$want"
    echo -e "$src\t$pid\t$idx\t$dl_url\tOK\t$code\t$dest" >> "$WORK/img_results.tsv"
    sleep 0.1
  done < "$WORK/img_plan.tsv"
}
download_images
IMG_OK=$(grep -c $'\tOK\t' "$WORK/img_results.tsv" || true)
IMG_FAIL=$(grep -c $'\tFAIL\t' "$WORK/img_results.tsv" || true)
log "图片下载完成:成功 $IMG_OK,失败 $IMG_FAIL"

# ---------- 阶段 6:manifest.json 与 manifest-images.json ----------
python3 - "$WORK" "$OUT" "$IMG_DIR" "$FETCHED_AT" "$BASE" "$DS_PAGES_JH" "$DS_PAGES_TC" "$TT_PAGES_JH" "$TT_PAGES_TC" "$DETAIL_FAILS" "$IMG_OK" "$IMG_FAIL" "$MAX_IMAGES" "$MAX_PER_POST" <<'PYEOF'
import json, sys, os, glob
(work, out, img_dir, fetched_at, base, ds_pj, ds_pt, tt_pj, tt_pt,
 detail_fails, img_ok, img_fail, max_total, max_per) = sys.argv[1:15]

dedup = json.load(open(f"{work}/dedup_stats.json"))
merge = json.load(open(f"{work}/merge_stats.json"))
ds_posts = json.load(open(f"{out}/posts-ds.json"))
tt_posts = json.load(open(f"{out}/posts-taptap.json"))
probes = {t: open(f"{work}/probe/{t}.txt").read().strip()
          for t in ("4399", "4399_taochu", "4399_danzai", "taptap_danzai")}

def probe_total(v):
    try:
        parts = v.split()
        return int(parts[-1]) if parts[-1].isdigit() else None
    except Exception:
        return None

# 官方公告帖统计
KW = None  # 与阶段 5 一致,仅做统计
import re
KW = re.compile(r"更新|维护|公告|版本|平衡|赛季|上线|修复|新增|调整|优化|前瞻|爆料|预告|解封|活动|福利|礼包|返场|周年")
official_announce = {}
for src, posts in (("ds", ds_posts), ("taptap", tt_posts)):
    n_off = n_off_ann = 0
    for p in posts:
        a = p.get("author") or {}
        if (a.get("nickname") == "蛋仔派对") or ("官方" in (a.get("identity") or "")):
            n_off += 1
            text = " ".join(str(p.get(k) or "") for k in ("title", "summary", "body_text"))
            if KW.search(text):
                n_off_ann += 1
    official_announce[src] = {"official_posts": n_off, "official_announcement_posts": n_off_ann}

# 接口样例(截断)
def sample_item(src, tag):
    files = sorted(glob.glob(f"{work}/list/{tag}/p1.json"))
    if not files:
        return None
    try:
        items = json.load(open(files[0])).get("items", [])
        return items[0] if items else None
    except Exception:
        return None

def sample_detail(src):
    pid = ds_posts[0]["id"] if src == "ds" and ds_posts else (tt_posts[0]["id"] if tt_posts else None)
    if not pid:
        return None
    fp = f"{work}/detail/{src}/{pid}.json"
    if not os.path.exists(fp):
        return None
    try:
        d = json.load(open(fp))
        p = d.get("post") or {}
        blocks = p.get("content_blocks") or []
        return {
            "endpoint": f"{base}/{src}/posts/{pid}?comment_page=1",
            "top_keys": sorted(d.keys()),
            "post_keys": sorted(p.keys()),
            "content_block_types": [b.get("type") for b in blocks][:20],
            "body_text_first_200": (p.get("body_text") or "")[:200],
            "comment_total": d.get("comment_total"),
        }
    except Exception:
        return None

manifest = {
    "task": "抓取 qweb.icai.top 社区「惊魂夜/逃出惊魂夜」相关帖子并存档",
    "fetched_at_utc": fetched_at,
    "base_url": base,
    "endpoints": {
        "list":   f"{base}/{{source}}/posts?page=N&page_size=50&query=<关键词>",
        "detail": f"{base}/{{source}}/posts/{{id}}?comment_page=1",
        "media":  f"{base}/media-assets/<asset_id> 或 {base}/media/...",
    },
    "queries_used": {"惊魂夜": "%E6%83%8A%E9%AD%82%E5%A4%9C", "逃出惊魂夜": "%E9%80%83%E5%87%BA%E6%83%8A%E9%AD%82%E5%A4%9C"},
    "sources": {
        "ds": {
            "available": True,
            "queries": {
                "惊魂夜":   {"total": dedup["ds"]["queries"]["ds-jinghongye"].get("api_total"),
                              "pages": int(ds_pj), "raw_ids_unique": dedup["ds"]["queries"]["ds-jinghongye"]["raw_ids_unique"]},
                "逃出惊魂夜": {"total": dedup["ds"]["queries"]["ds-taochu"].get("api_total"),
                                "pages": int(ds_pt), "raw_ids_unique": dedup["ds"]["queries"]["ds-taochu"]["raw_ids_unique"]},
            },
            "unique_posts": merge["ds"]["unique"],
            "details_merged": merge["ds"]["details_merged"],
            "details_missing": merge["ds"]["details_missing"],
            "output": "posts-ds.json",
            **official_announce["ds"],
        },
        "taptap": {
            "available": True,
            "queries": {
                "惊魂夜":   {"total": dedup["taptap"]["queries"]["taptap-jinghongye"].get("api_total"),
                              "pages": int(tt_pj), "raw_ids_unique": dedup["taptap"]["queries"]["taptap-jinghongye"]["raw_ids_unique"]},
                "逃出惊魂夜": {"total": dedup["taptap"]["queries"]["taptap-taochu"].get("api_total"),
                                "pages": int(tt_pt), "raw_ids_unique": dedup["taptap"]["queries"]["taptap-taochu"]["raw_ids_unique"]},
                "蛋仔派对": {"total": probe_total(probes["taptap_danzai"]), "scraped": False,
                              "note": "仅探测记录 total,超出「惊魂夜/逃出惊魂夜」任务范围,未抓取"},
            },
            "unique_posts": merge["taptap"]["unique"],
            "details_merged": merge["taptap"]["details_merged"],
            "details_missing": merge["taptap"]["details_missing"],
            "output": "posts-taptap.json",
            **official_announce["taptap"],
        },
        "4399": {
            "available": True,
            "queries": {
                "惊魂夜":   {"total": probe_total(probes["4399"])},
                "逃出惊魂夜": {"total": probe_total(probes["4399_taochu"])},
                "蛋仔派对": {"total": probe_total(probes["4399_danzai"])},
            },
            "unique_posts": 0,
            "output": "posts-4399.json",
            "note": "接口正常返回(total=0),但三个 query 均无命中,无可抓取内容",
        },
    },
    "dedup": {
        "strategy": "按源内帖子 id 去重(两个 query 的并集);ds 与 taptap 的 id 空间独立,未跨源合并",
        "ds": dedup["ds"],
        "taptap": dedup["taptap"],
    },
    "comments": "详情接口附带评论第一页(comment_page=1),已随详情一并并入 posts-*.json;未翻页抓全部评论",
    "images": {
        "dir": img_dir,
        "manifest": f"{img_dir}/manifest-images.json",
        "in_repo": False,
        "selection_rule": "author.nickname=='蛋仔派对'(或 identity 含「官方」)且 title/summary/body_text 命中公告类关键词(更新/维护/公告/版本/平衡/赛季/上线/修复/新增/调整/优化/前瞻/爆料/预告/解封/活动/福利/礼包/返场/周年)",
        "limits": {"total": int(max_total), "per_post": int(max_per)},
        "downloaded": int(img_ok),
        "failed": int(img_fail),
        "official_announcement_posts": official_announce,
    },
    "detail_failures": int(detail_fails),
    "samples": {
        "list_item_ds": sample_item("ds", "ds-jinghongye"),
        "list_item_taptap": sample_item("taptap", "taptap-jinghongye"),
        "detail_ds": sample_detail("ds"),
    },
    "reproduce": "bash fetch.sh(同目录;可用 QWEB_OUT_DIR / QWEB_IMG_DIR / QWEB_MAX_IMAGES / QWEB_MAX_PER_POST 覆盖)",
}
json.dump(manifest, open(f"{out}/manifest.json", "w"), ensure_ascii=False, indent=1)

# 图片清单
img_rows = []
fails = []
if os.path.exists(f"{work}/img_results.tsv"):
    for line in open(f"{work}/img_results.tsv"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 7:
            continue
        src, pid, idx, url, status, code, payload = parts[:7]
        if status == "OK":
            img_rows.append({
                "post_id": pid, "source": src, "index_in_post": int(idx),
                "file": os.path.basename(payload),
                "bytes": os.path.getsize(payload) if os.path.exists(payload) else 0,
                "image_url": url,  # TSV 中已存解析后的完整 URL
                "source_url": next((p.get("source_url") for p in (ds_posts + tt_posts) if p.get("id") == pid), None),
                "published_at": next((p.get("published_at") for p in (ds_posts + tt_posts) if p.get("id") == pid), None),
            })
        else:
            fails.append({"post_id": pid, "source": src, "index_in_post": int(idx),
                          "image_url": url, "http_code": code, "reason": payload})
sel_ids = sorted({r["post_id"] for r in img_rows})
img_manifest = {
    "fetched_at_utc": fetched_at,
    "base_url": base,
    "selection_rule": "官方账号「蛋仔派对」发布的更新公告类帖子(title/summary/body_text 命中公告关键词)",
    "limits": {"total": int(max_total), "per_post": int(max_per)},
    "images_downloaded": len(img_rows),
    "images_failed": len(fails),
    "posts_covered": len(sel_ids),
    "post_ids": sel_ids,
    "images": img_rows,
    "failures": fails,
}
json.dump(img_manifest, open(f"{img_dir}/manifest-images.json", "w"), ensure_ascii=False, indent=1)
print(f"manifest written; images={len(img_rows)} failed={len(fails)} posts={len(sel_ids)}")
PYEOF
log "阶段 6 完成:manifest.json 与 manifest-images.json 已写入"
log "全部完成。产物目录:$OUT(图片在 $IMG_DIR)"
