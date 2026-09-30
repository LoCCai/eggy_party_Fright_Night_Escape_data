<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../api.js';

const router = useRouter();
const list = ref([]);
const q = ref('');
const sort = ref('release_desc');

const filtered = computed(() => {
  const kw = q.value.trim();
  if (!kw) return list.value;
  return list.value.filter((c) => (c.name + c.title).includes(kw));
});

onMounted(async () => {
  list.value = await api.chasers();
});
</script>

<template>
  <div class="container page">
    <h1 class="page-title">🔪 追捕者图鉴</h1>
    <p class="page-sub">绝命镇的复仇者们 —— 击倒逃生者并将其投入爆米花大炮,阻止逃生人数达标即获胜</p>

    <div style="display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap">
      <input v-model="q" class="input" placeholder="搜索角色名 / 称号…" />
      <select v-model="sort" class="input" style="min-width: 150px">
        <option value="release_desc">按上线时间(新→旧)</option>
        <option value="release_asc">按上线时间(旧→新)</option>
        <option value="difficulty_desc">按上手难度</option>
      </select>
    </div>

    <div v-if="filtered.length" class="char-grid">
      <div
        v-for="c in filtered"
        :key="c.id"
        class="char-card chaser"
        @click="router.push(`/character/chasers/${c.id}`)"
      >
        <span class="corner">{{ c.release_date || '时间待补充' }}</span>
        <div class="avatar">{{ c.emoji }}</div>
        <h3>{{ c.name }}</h3>
        <div class="title">{{ c.title || '—' }}</div>
        <div class="meta">
          <span class="chip" style="background: rgba(244,63,94,.12); color: #fb7185; border-color: rgba(244,63,94,.4)">
            {{ (c.skills || []).length }} 个技能
          </span>
          <span v-if="c.strength" class="chip orange">强度 {{ c.strength }}</span>
          <span class="chip">难度 {{ c.difficulty }}/5</span>
        </div>
      </div>
    </div>
    <div v-else class="empty">没有找到匹配的追捕者</div>
  </div>
</template>
