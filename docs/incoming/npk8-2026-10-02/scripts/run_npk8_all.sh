#!/bin/bash
KW='惊魂夜,逃出,蒸汽炉,追捕者,逃生者,海瑟,失血,痛楚领域,迅影索,暗影能量,念奴娇,百珍楼,礼温,梵蒂娅'
W=/home/ccai/eggy_party_Fright_Night_Escape_data/docs/incoming/runtime-2026-10-02/scripts/npk_zstd_walker.py
for p in ext_packer_8 ext_packer_11 ext_packer_fashion_part_high_2 ext_packer_low_skin_3 ext_packer_low_skin_5 ext_packer_skin_voice_1 ext_packer_skin_voice_3 ext_packer_sky_box_1; do
  echo "===== $p start $(date +%T) ====="
  python3 "$W" "/home/eggy-test/npk8/src/$p.npk" "/home/eggy-test/npk8/$p" "$KW"
  echo "===== $p done $(date +%T) rc=$? ====="
done
echo ALL_DONE
