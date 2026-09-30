<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { api } from '../api.js';

const route = useRoute();
const faction = computed(() => route.params.faction);
const char = ref(null);

const TYPE_COLOR = { 主动: '#a78bfa', 被动: '#34d399', 处决: '#f43f5e' };

onMounted(async () => {
  char.value =
    faction.value === 'chasers' ? await api.chaser(route.params.id) : await api.escapee(route.params.id);
  document.title = `${char.value.name} · 逃出惊魂夜数据站`;
});
</script>

<template>
  <div class="container page" v-if="char">
    <p style="margin-bottom: 18px">
      <router-link :to="faction === 'chasers' ? '/chasers' : '/escapees'" style="color: var(--accent); font-size: 13px">
        ← 返回{{ faction === 'chasers' ? '追捕者' : '逃生者' }}列表
      </router-link>
    </p>

    <div class="card detail-hero" :class="{ 'chaser-hero': faction === 'chasers' }">
      <div class="avatar">{{ char.emoji }}</div>
      <div style="flex: 1">
        <h1 style="font-size: 30px; font-weight: 800">{{ char.name }}</h1>
        <p style="color: var(--text-dim); margin: 6px 0 14px">{{ char.title || '—' }}</p>
        <div style="display: flex; gap: 8px; flex-wrap: wrap">
          <span class="chip" :class="{ orange: faction === 'chasers' }">
            {{ faction === 'chasers' ? '追捕者阵营' : '逃生者阵营' }}
          </span>
          <span v-if="char.role_type" class="chip">定位:{{ char.role_type }}</span>
          <span v-if="char.strength" class="chip orange">强度 {{ char.strength }}</span>
          <span class="chip">难度 {{ char.difficulty }}/5</span>
          <span class="chip">{{ char.release_date ? `上线 ${char.release_date}` : '上线时间待补充' }}</span>
        </div>
      </div>
    </div>

    <h2 style="margin: 28px 0 4px; font-size: 19px">⚡ 技能</h2>
    <div v-for="(s, i) in char.skills || []" :key="i" class="skill">
      <div class="skill-head">
        <span class="chip" :style="`background:${TYPE_COLOR[s.type]}22;color:${TYPE_COLOR[s.type] || '#a78bfa'};border-color:${TYPE_COLOR[s.type]}55`">
          {{ s.type || '技能' }}
        </span>
        <span class="skill-name">{{ s.name }}</span>
      </div>
      <p class="skill-desc">{{ s.desc || '描述待补充' }}</p>
    </div>
    <div v-if="!(char.skills || []).length" class="empty">技能资料待补充</div>

    <h2 style="margin: 28px 0 10px; font-size: 19px">📜 角色小传</h2>
    <div class="card" style="color: var(--text-dim); font-size: 14px; line-height: 2; white-space: pre-wrap">
      {{ char.story || '暂无小传资料。' }}
    </div>

    <template v-if="char.tips">
      <h2 style="margin: 28px 0 10px; font-size: 19px">💡 玩法提示</h2>
      <div class="card" style="color: var(--text-dim); font-size: 13.5px; line-height: 1.9">{{ char.tips }}</div>
    </template>
  </div>
  <div v-else class="empty container page">加载中…</div>
</template>
