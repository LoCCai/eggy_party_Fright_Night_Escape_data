<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../api.js';

const router = useRouter();
const stats = ref(null);

onMounted(async () => {
  try { stats.value = await api.stats(); } catch { /* ignore */ }
});
</script>

<template>
  <div class="container page">
    <section class="hero">
      <h1>逃出惊魂夜 · 数据站</h1>
      <p class="sub">
        《蛋仔派对》×《第五人格》联动非对称竞技玩法资料库(别称「第五蛋格」)<br />
        收录 {{ stats?.overview?.chasers ?? '?' }} 名追捕者 · {{ stats?.overview?.escapees ?? '?' }} 名逃生者 ·
        {{ stats?.overview?.maps ?? '?' }} 张地图,角色档案 / 技能 / 地图机制一站查询
      </p>
      <div class="cta">
        <button class="btn primary" @click="router.push('/chasers')">🔪 查询追捕者</button>
        <button class="btn primary" @click="router.push('/escapees')">🥚 查询逃生者</button>
        <button class="btn" @click="router.push('/maps')">🗺️ 地图机制</button>
        <button class="btn" @click="router.push('/stats')">📊 数据分析</button>
      </div>
    </section>

    <section class="feature-grid">
      <div class="card feature">
        <div class="icon">🔪</div>
        <h3>追捕者图鉴</h3>
        <p>哑女斯黛拉、疯象莫比、魔警艾琳、血衣教师礼温、影爪梵蒂娅、少盟主沈昭等 12 名追捕者的技能机制与背景小传。</p>
      </div>
      <div class="card feature">
        <div class="icon">🥚</div>
        <h3>逃生者图鉴</h3>
        <p>矿工、医生、魔术师、黑拳、炼金师、行刑官、歌女等 21 名逃生者的主动 / 被动技能与挖煤速度分档。</p>
      </div>
      <div class="card feature">
        <div class="icon">🗺️</div>
        <h3>地图与元素</h3>
        <p>马戏团 / 火车站 / 码头 / 不夜楼四张地图的蒸汽炉、火车、水闸、暗门等专属机制,支持自定义显隐。</p>
      </div>
      <div class="card feature">
        <div class="icon">📊</div>
        <h3>数据分析</h3>
        <p>阵营构成、角色上线时间线、强度与定位分布、地图元素类型统计,图表化呈现玩法生态。</p>
      </div>
    </section>

    <section class="card rules">
      <h3>📖 玩法速览(1v4 / 2v8)</h3>
      <ul>
        <li>对局 15 分钟:1v4 模式 1 名追捕者对抗 4 名逃生者;2024-08-23 起加入 2v8 合作模式。</li>
        <li>逃生者挖煤填充<b>蒸汽炉</b>:1v4 激活 5 座、2v8 激活 7 座即可开启<b>逃生门</b>;1v4 逃离 3 人及以上获胜(2 人平局),2v8 逃离 5 人及以上获胜(4 人平局)。</li>
        <li>追捕者击倒逃生者后将其放入<b>爆米花大炮</b>淘汰;阻止达标人数或耗尽时间即获胜。</li>
        <li>逃生者最多承受 2 次(1v4)/ 3 次(2v8)伤害;可用「走」避免留下脚印,靠近追捕者会触发「啾啾感应」。</li>
        <li>残局可走<b>地窖</b>:最后一名未被淘汰的逃生者可从地窖独自撤离。</li>
      </ul>
    </section>
  </div>
</template>
