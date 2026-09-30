<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../api.js';

const router = useRouter();
const list = ref([]);
const q = ref('');
const role = ref('');

const roles = computed(() => [...new Set(list.value.map((c) => c.role_type).filter(Boolean))]);

const filtered = computed(() => {
  const kw = q.value.trim();
  return list.value.filter(
    (c) => (!kw || (c.name + c.title).includes(kw)) && (!role.value || c.role_type === role.value)
  );
});

onMounted(async () => {
  list.value = await api.escapees();
});
</script>

<template>
  <div class="container page">
    <h1 class="page-title">🥚 逃生者图鉴</h1>
    <p class="page-sub">手办世界的求生者 —— 激活蒸汽炉开启逃生门或地窖,逃离人数达标即获胜</p>

    <div style="display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap">
      <input v-model="q" class="input" placeholder="搜索角色名 / 称号…" />
      <select v-model="role" class="input" style="min-width: 150px">
        <option value="">全部定位</option>
        <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
      </select>
    </div>

    <div v-if="filtered.length" class="char-grid">
      <div
        v-for="c in filtered"
        :key="c.id"
        class="char-card"
        @click="router.push(`/character/escapees/${c.id}`)"
      >
        <span class="corner">{{ c.release_date || '时间待补充' }}</span>
        <div class="avatar">{{ c.emoji }}</div>
        <h3>{{ c.name }}</h3>
        <div class="title">{{ c.title || '—' }}</div>
        <div class="meta">
          <span v-if="c.role_type" class="chip">{{ c.role_type }}</span>
          <span class="chip">难度 {{ c.difficulty }}/5</span>
        </div>
      </div>
    </div>
    <div v-else class="empty">没有找到匹配的逃生者</div>
  </div>
</template>
