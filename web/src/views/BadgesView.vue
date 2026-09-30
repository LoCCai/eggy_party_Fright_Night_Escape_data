<script setup>
import { ref, computed, onMounted } from 'vue';
import { api } from '../api.js';

const list = ref([]);
const faction = ref('');
const grade = ref('');

const categories = computed(() => {
  const pool = list.value.filter((b) => !faction.value || b.faction === faction.value);
  return [...new Set(pool.map((b) => b.category).filter(Boolean))];
});
const filtered = computed(() =>
  list.value.filter(
    (b) =>
      (!faction.value || b.faction === faction.value) &&
      (!grade.value || b.grade === grade.value) &&
      (!cat.value || b.category === cat.value)
  )
);
const cat = ref('');

onMounted(async () => {
  list.value = await api.badges();
  document.title = '徽章图鉴 · 逃出惊魂夜数据站';
});
</script>

<template>
  <div class="container page">
    <h1 class="page-title">🎖️ 徽章图鉴</h1>
    <p class="page-sub">
      2025-04-03 上线的阵营通用被动系统:局内可佩戴 1 枚典藏 + 3 枚稀有徽章,同等级×3 可合成升级(共 3 级)
    </p>

    <div style="display: flex; gap: 10px; margin-bottom: 18px; flex-wrap: wrap">
      <button
        v-for="f in ['', '逃生者', '追捕者']"
        :key="f || 'all'"
        class="btn"
        :class="{ primary: faction === f }"
        style="padding: 6px 16px; font-size: 13px"
        @click="faction = f; cat = ''"
      >
        {{ f || '全部阵营' }}
      </button>
      <span style="width: 14px"></span>
      <button
        v-for="g in ['', '典藏', '稀有']"
        :key="g || 'allg'"
        class="btn"
        :class="{ primary: grade === g }"
        style="padding: 6px 16px; font-size: 13px"
        @click="grade = g"
      >
        {{ g || '全部品级' }}
      </button>
    </div>
    <div style="display: flex; gap: 8px; margin-bottom: 18px; flex-wrap: wrap">
      <button
        v-for="c in categories"
        :key="c"
        class="btn"
        :class="{ primary: cat === c }"
        style="padding: 4px 14px; font-size: 12.5px"
        @click="cat = cat === c ? '' : c"
      >
        {{ c }}
      </button>
    </div>

    <div class="badge-grid">
      <div v-for="b in filtered" :key="b.id" class="card badge-card" :class="{ legendary: b.grade === '典藏' }">
        <div class="badge-head">
          <h3>{{ b.name }}</h3>
          <span class="chip" :class="b.grade === '典藏' ? 'orange' : ''">{{ b.grade }}</span>
        </div>
        <div style="margin: 8px 0 10px; display: flex; gap: 6px; flex-wrap: wrap">
          <span class="chip" :style="b.faction === '追捕者' ? 'background:rgba(244,63,94,.12);color:#fb7185;border-color:rgba(244,63,94,.4)' : ''">
            {{ b.faction }}
          </span>
          <span v-if="b.category" class="chip">{{ b.category }}</span>
        </div>
        <p class="badge-desc">{{ b.description }}</p>
      </div>
    </div>
    <div v-if="!filtered.length" class="empty">没有匹配的徽章</div>
  </div>
</template>
