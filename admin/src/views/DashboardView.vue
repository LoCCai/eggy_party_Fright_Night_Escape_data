<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { http } from '../api.js';

const stats = ref(null);
const charts = [];
const els = {};

onMounted(async () => {
  stats.value = await http.get('/stats');
  await nextTick();
  const s = stats.value;
  const axis = { axisLabel: { color: '#a89fc7' }, axisLine: { lineStyle: { color: '#3a3060' } } };

  const make = (key, option) => {
    const chart = echarts.init(els[key]);
    chart.setOption(option);
    charts.push(chart);
  };

  make('faction', {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie', radius: ['40%', '68%'],
      data: [
        { name: '追捕者', value: s.overview.chasers, itemStyle: { color: '#f43f5e' } },
        { name: '逃生者', value: s.overview.escapees, itemStyle: { color: '#a78bfa' } }
      ],
      label: { color: '#e8e4f5' }
    }]
  });

  make('timeline', {
    tooltip: { trigger: 'axis' },
    grid: { left: 40, right: 20, bottom: 30, top: 30 },
    xAxis: { type: 'category', data: s.timeline.map((t) => t.month), ...axis },
    yAxis: { type: 'value', minInterval: 1, splitLine: { lineStyle: { color: '#2a2348' } }, ...axis },
    series: [
      { name: '追捕者', type: 'bar', stack: 'x', data: s.timeline.map((t) => t['追捕者']), itemStyle: { color: '#f43f5e' } },
      { name: '逃生者', type: 'bar', stack: 'x', data: s.timeline.map((t) => t['逃生者']), itemStyle: { color: '#a78bfa' } }
    ]
  });

  make('elements', {
    tooltip: { trigger: 'axis' },
    grid: { left: 60, right: 20, bottom: 30, top: 20 },
    xAxis: { type: 'value', minInterval: 1, splitLine: { lineStyle: { color: '#2a2348' } }, ...axis },
    yAxis: { type: 'category', data: s.elementTypes.map((e) => e.name), ...axis },
    series: [{ type: 'bar', data: s.elementTypes.map((e) => e.value), itemStyle: { color: '#f97316' }, barWidth: 16 }]
  });

  window.addEventListener('resize', resize);
});

function resize() { charts.forEach((c) => c.resize()); }
onUnmounted(() => { window.removeEventListener('resize', resize); charts.forEach((c) => c.dispose()); });
</script>

<template>
  <div v-if="stats">
    <h2 style="margin-bottom: 16px">仪表盘</h2>
    <el-row :gutter="14" style="margin-bottom: 16px">
      <el-col v-for="item in [
        { label: '追捕者', value: stats.overview.chasers, color: '#f43f5e' },
        { label: '逃生者', value: stats.overview.escapees, color: '#a78bfa' },
        { label: '地图', value: stats.overview.maps, color: '#f97316' },
        { label: '地图元素', value: stats.overview.elements, color: '#34d399' }
      ]" :key="item.label" :span="6">
        <div class="page-card" style="text-align: center">
          <div style="font-size: 30px; font-weight: 800" :style="{ color: item.color }">{{ item.value }}</div>
          <div style="color: #a89fc7; font-size: 13px; margin-top: 4px">{{ item.label }}</div>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="14">
      <el-col :span="8"><div class="page-card" :ref="(el) => (els.faction = el)" style="height: 300px" /></el-col>
      <el-col :span="8"><div class="page-card" :ref="(el) => (els.timeline = el)" style="height: 300px" /></el-col>
      <el-col :span="8"><div class="page-card" :ref="(el) => (els.elements = el)" style="height: 300px" /></el-col>
    </el-row>
  </div>
</template>
