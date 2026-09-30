<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { api, visibility } from '../api.js';

const route = useRoute();
const map = ref(null);
const typeFilter = ref('');
const showHidden = ref(false);
const hiddenSet = ref(new Set());

const types = computed(() => [...new Set((map.value?.elements || []).map((e) => e.type))]);

const visibleElements = computed(() =>
  (map.value?.elements || []).filter((e) => {
    if (typeFilter.value && e.type !== typeFilter.value) return false;
    if (showHidden.value) return true;
    return !hiddenSet.value.has(e.id);
  })
);

const hiddenCount = computed(() => (map.value?.elements || []).filter((e) => hiddenSet.value.has(e.id)).length);

function toggleElement(id) {
  hiddenSet.value = visibility.toggle(route.params.id, id);
}
function showAll() {
  visibility.reset(route.params.id);
  hiddenSet.value = new Set();
}

onMounted(async () => {
  map.value = await api.map(route.params.id);
  hiddenSet.value = visibility.getHidden(route.params.id);
  document.title = `${map.value.name} · 逃出惊魂夜数据站`;
});
</script>

<template>
  <div class="container page" v-if="map">
    <p style="margin-bottom: 18px">
      <router-link to="/maps" style="color: var(--accent); font-size: 13px">← 返回地图列表</router-link>
    </p>

    <div class="card" style="display: flex; gap: 22px; align-items: center">
      <div style="font-size: 64px">{{ map.emoji }}</div>
      <div style="flex: 1">
        <h1 style="font-size: 28px; font-weight: 800">{{ map.name }}</h1>
        <p style="color: var(--text-dim); font-size: 14px; margin: 8px 0 10px">{{ map.description }}</p>
        <div style="display: flex; gap: 8px; flex-wrap: wrap">
          <span class="chip">{{ map.theme }}</span>
          <span class="chip">{{ map.size }}图</span>
          <span class="chip orange">上线 {{ map.release_date || '待补充' }}</span>
          <span class="chip">{{ map.elements.length }} 种元素</span>
        </div>
      </div>
    </div>

    <div style="display: flex; align-items: center; gap: 10px; margin: 24px 0 14px; flex-wrap: wrap">
      <h2 style="font-size: 19px; margin-right: 6px">🧩 地图元素</h2>
      <button
        v-for="t in types"
        :key="t"
        class="btn"
        :class="{ primary: typeFilter === t }"
        style="padding: 5px 14px; font-size: 12.5px"
        @click="typeFilter = typeFilter === t ? '' : t"
      >
        {{ t }}
      </button>
      <span style="flex: 1"></span>
      <label style="display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--text-dim); cursor: pointer">
        <input type="checkbox" v-model="showHidden" />
        显示已隐藏({{ hiddenCount }})
      </label>
      <button class="btn ghost" style="padding: 5px 14px; font-size: 12.5px" @click="showAll">全部恢复显示</button>
    </div>
    <p style="color: var(--text-dim); font-size: 12.5px; margin-bottom: 14px">
      💡 每张地图的元素信息都可以点击右上角 👁 自定义展示或隐藏,偏好会保存在本地浏览器中。
    </p>

    <div class="elem-grid">
      <div
        v-for="e in visibleElements"
        :key="e.id"
        class="card elem-card"
        :class="{ 'hidden-card': hiddenSet.has(e.id) }"
      >
        <button class="eye" :title="hiddenSet.has(e.id) ? '恢复显示' : '隐藏该元素'" @click="toggleElement(e.id)">
          {{ hiddenSet.has(e.id) ? '🙈' : '👁️' }}
        </button>
        <div class="elem-head">
          <div class="elem-icon">{{ e.icon }}</div>
          <div>
            <div class="elem-name">{{ e.name }}</div>
            <span class="chip" style="margin-top: 2px">{{ e.type }}</span>
          </div>
        </div>
        <p class="elem-desc">{{ e.description }}</p>
      </div>
    </div>
    <div v-if="!visibleElements.length" class="empty">
      {{ hiddenCount ? '当前元素均已隐藏 —— 勾选「显示已隐藏」可查看' : '暂无该类型元素' }}
    </div>
  </div>
  <div v-else class="empty container page">加载中…</div>
</template>
