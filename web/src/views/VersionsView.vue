<script setup>
import { ref, onMounted } from 'vue';
import { api } from '../api.js';

const patches = ref([]);

onMounted(async () => {
  patches.value = await api.patches();
  document.title = '版本动态 · 逃出惊魂夜数据站';
});
</script>

<template>
  <div class="container page">
    <h1 class="page-title">📌 版本动态</h1>
    <p class="page-sub">
      新角色 / 新地图 / 平衡调整时间线,共 {{ patches.length }} 条 —— 整理自官方公告检索归档(截止 2026-09-29)
    </p>

    <div class="timeline">
      <div v-for="p in patches" :key="p.id" class="tl-item">
        <div class="tl-dot"></div>
        <div class="card tl-card">
          <div class="tl-head">
            <span class="chip orange">{{ p.date }}</span>
            <h3>{{ p.title }}</h3>
          </div>
          <ul class="tl-list">
            <li v-for="(s, i) in p.summary" :key="i">{{ s }}</li>
          </ul>
        </div>
      </div>
    </div>
    <div v-if="!patches.length" class="empty">暂无版本数据</div>
  </div>
</template>
