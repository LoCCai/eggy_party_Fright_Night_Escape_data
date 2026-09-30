<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { api } from '../api.js';

const stats = ref(null);
const charts = [];
const els = {};

function render(key, option) {
  const el = els[key];
  if (!el) return;
  const chart = echarts.init(el);
  chart.setOption(option);
  charts.push(chart);
}

const AXIS = { axisLabel: { color: '#a89fc7' }, axisLine: { lineStyle: { color: '#3a3060' } } };

onMounted(async () => {
  stats.value = await api.stats();
  const s = stats.value;

  render('faction', {
    tooltip: { trigger: 'item' },
    legend: { textStyle: { color: '#a89fc7' } },
    series: [{
      type: 'pie', radius: ['42%', '68%'],
      data: [
        { name: '追捕者', value: s.overview.chasers, itemStyle: { color: '#f43f5e' } },
        { name: '逃生者', value: s.overview.escapees, itemStyle: { color: '#a78bfa' } }
      ],
      label: { color: '#e8e4f5' }
    }]
  });

  render('timeline', {
    tooltip: { trigger: 'axis' },
    legend: { textStyle: { color: '#a89fc7' } },
    grid: { left: 40, right: 20, bottom: 30, top: 40 },
    xAxis: { type: 'category', data: s.timeline.map((t) => t.month), ...AXIS },
    yAxis: { type: 'value', minInterval: 1, splitLine: { lineStyle: { color: '#2a2348' } }, ...AXIS },
    series: [
      { name: '追捕者', type: 'bar', stack: 'x', data: s.timeline.map((t) => t['追捕者']), itemStyle: { color: '#f43f5e' } },
      { name: '逃生者', type: 'bar', stack: 'x', data: s.timeline.map((t) => t['逃生者']), itemStyle: { color: '#a78bfa' } }
    ]
  });

  render('roles', {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie', radius: '62%',
      data: s.roleDist.map((r) => ({ name: r.name, value: r.value })),
      label: { color: '#e8e4f5' }
    }]
  });

  render('elements', {
    tooltip: { trigger: 'axis' },
    grid: { left: 60, right: 20, bottom: 30, top: 20 },
    xAxis: { type: 'value', minInterval: 1, splitLine: { lineStyle: { color: '#2a2348' } }, ...AXIS },
    yAxis: { type: 'category', data: s.elementTypes.map((e) => e.name), ...AXIS },
    series: [{ type: 'bar', data: s.elementTypes.map((e) => e.value), itemStyle: { color: '#f97316' }, barWidth: 18 }]
  });

  window.addEventListener('resize', handleResize);
});

function handleResize() { charts.forEach((c) => c.resize()); }
onUnmounted(() => { window.removeEventListener('resize', handleResize); charts.forEach((c) => c.dispose()); });
</script>

<template>
  <div class="container page">
    <h1 class="page-title">📊 数据分析</h1>
    <p class="page-sub">基于本站收录的 {{ stats?.overview?.chasers ?? '?' }} 追捕者 / {{ stats?.overview?.escapees ?? '?' }} 逃生者 / {{ stats?.overview?.maps ?? '?' }} 张地图生成</p>

    <div class="stat-cards" v-if="stats">
      <div class="card stat-card"><div class="num">{{ stats.overview.chasers }}</div><div class="label">追捕者</div></div>
      <div class="card stat-card"><div class="num">{{ stats.overview.escapees }}</div><div class="label">逃生者</div></div>
      <div class="card stat-card"><div class="num">{{ stats.overview.maps }}</div><div class="label">地图</div></div>
      <div class="card stat-card"><div class="num">{{ stats.overview.elements }}</div><div class="label">地图元素</div></div>
      <div class="card stat-card"><div class="num">{{ stats.overview.badges }}</div><div class="label">徽章</div></div>
      <div class="card stat-card"><div class="num">{{ stats.overview.patches }}</div><div class="label">版本公告</div></div>
      <div class="card stat-card"><div class="num">{{ stats.overview.ratio }}</div><div class="label">追捕 : 逃生(1v4)</div></div>
    </div>

    <div class="chart-grid">
      <div class="chart"><h3>阵营构成</h3><div class="chart-body" :ref="(el) => (els.faction = el)"></div></div>
      <div class="chart"><h3>新角色上线时间线</h3><div class="chart-body" :ref="(el) => (els.timeline = el)"></div></div>
      <div class="chart"><h3>逃生者定位分布(有标注者)</h3><div class="chart-body" :ref="(el) => (els.roles = el)"></div></div>
      <div class="chart"><h3>地图元素类型统计</h3><div class="chart-body" :ref="(el) => (els.elements = el)"></div></div>
    </div>
  </div>
</template>
