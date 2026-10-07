#!/usr/bin/env python3
r"""
皮肤/时装/加载页「代号」计数器(2026-10-08 研判合并会话补档)。

背景:初版报告(cosmetics_inventory.md / pack_manifests.md)中的四组总数
(fashion t4=183、low_skin_3=248、low_skin_5=122、ext_packer_8 loading=141、
ext_packer_11 loading=90)出自未归档的合并口径(把 _lod/_2/_3/配色等变体人工归组),
独立复核用 9 种收割口径均无法复现(复核实测:目录级/路径边界/清单展开 各不一致)。
本脚本把口径显式化并归档,输出三种可复现原始计数:

  loading_units : 以「路径组件级」口径去重 <代号>_loading——即 token 须位于含
                  / 或 \ 分隔符的路径串中(有父目录);不含分隔符的裸 token
                  (动画状态名,如 stand_loading / t4_head_ablj_loading)不计。
                  不做变体归组(t1_x 与 t1_x_2 记两个;含 char_*_loading 形态),
                  另给出其中 t4_* 前缀数(fashion 分件口径)。
  gim_entities  : 去重 *.gim 模型文件基名,剥离 _lod<数字> 后缀(LOD 变体归并,
                  配色/编号变体不归并)。
  gim_dirs      : *.gim 所属实体目录(路径倒数第二段)去重数。

用法:
  python3 count_skin_codes.py <解包 files 目录> [<解包 files 目录> ...]
扫描对象为目录内全部落盘文件的 ASCII 可打印串(与 npk_wwise_bank_mapper.py
的收割方式一致);ktx/mesh 等未落盘二进制不在统计内(与本报告其余口径相同)。
"""
import os, re, sys, collections

RUN_RE = re.compile(rb'[\w/\\.\-]{4,}')
LOADING_RE = re.compile(r'([A-Za-z][A-Za-z0-9_]{1,40})_loading(\.[A-Za-z0-9]+)?')
GIM_RE = re.compile(r'([A-Za-z][A-Za-z0-9_]{1,60})\.gim(?![A-Za-z0-9_])', re.I)
LOD_SUFFIX = re.compile(r'_lod\d+$', re.I)

def scan(files_dir):
    loading, gims, gim_dirs = set(), set(), set()
    for fn in sorted(os.listdir(files_dir)):
        data = open(os.path.join(files_dir, fn), 'rb').read()
        for m in RUN_RE.finditer(data):
            run = m.group().decode('ascii', 'ignore')
            if not re.search(r'[/\\]', run):
                continue  # 无分隔符的裸 token(动画状态名等)不计——排除 stand_loading 类误计
            parts = re.split(r'[/\\]', run)
            # loading 组件级:段 fullmatch <代号>_loading 且存在父目录
            for seg in parts:
                lm = LOADING_RE.fullmatch(seg)
                if lm:
                    loading.add(lm.group(1))  # 目录形态(无扩展名)与文件形态(带 .gim/.skel 等)均计
            # gim 基名与所属目录
            for i, seg in enumerate(parts):
                gm = GIM_RE.fullmatch(seg)
                if gm:
                    gims.add(LOD_SUFFIX.sub('', gm.group(1)))
                    if i >= 1:
                        gim_dirs.add(parts[i - 1])
    return loading, gims, gim_dirs

if __name__ == '__main__':
    for d in sys.argv[1:]:
        loading, gims, dirs = scan(d)
        t4 = sum(1 for c in loading if c.startswith('t4_'))
        print(f"== {d}")
        print(f"   loading_units={len(loading)} (t4_*={t4}) gim_entities={len(gims)} gim_dirs={len(dirs)}")
