<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../api.js';

const router = useRouter();
const list = ref([]);

onMounted(async () => {
  list.value = await api.maps();
});
</script>

<template>
  <div class="container page">
    <h1 class="page-title">🗺️ 地图档案</h1>
    <p class="page-sub">四张惊魂夜战场 —— 每张地图拥有不同的专属元素与撤离机制,点击查看详情</p>
    <div class="map-grid">
      <div v-for="m in list" :key="m.id" class="card map-card" @click="router.push(`/maps/${m.id}`)">
        <div class="banner">{{ m.emoji }}</div>
        <h3 style="font-size: 18px">{{ m.name }}</h3>
        <p style="color: var(--text-dim); font-size: 13px; margin: 6px 0 10px">{{ m.theme }} · {{ m.size }}图</p>
        <div style="display: flex; gap: 8px; flex-wrap: wrap">
          <span class="chip">上线 {{ m.release_date || '待补充' }}</span>
          <span class="chip orange">{{ m.element_count ?? '' }} 种元素</span>
        </div>
      </div>
    </div>
  </div>
</template>
