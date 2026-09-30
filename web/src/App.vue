<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();
</script>

<template>
  <div>
    <nav class="nav">
      <div class="nav-inner">
        <a class="logo" href="/" @click.prevent="router.push('/')">
          <span class="moon">🌙</span> 逃出惊魂夜 · 数据站
        </a>
        <a class="link" href="/chasers" @click.prevent="router.push('/chasers')">追捕者</a>
        <a class="link" href="/escapees" @click.prevent="router.push('/escapees')">逃生者</a>
        <a class="link" href="/maps" @click.prevent="router.push('/maps')">地图</a>
        <a class="link" href="/badges" @click.prevent="router.push('/badges')">徽章</a>
        <a class="link" href="/versions" @click.prevent="router.push('/versions')">版本动态</a>
        <a class="link" href="/stats" @click.prevent="router.push('/stats')">数据分析</a>
        <span class="spacer"></span>
        <span class="tag">第五蛋格</span>
      </div>
    </nav>
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <footer class="footer">
      <div class="container">
        蛋仔派对「逃出惊魂夜」非官方玩家数据站 · 数据整理自百度百科词条与网易官方公告,仅供查询参考<br />
        资料来源:<a href="https://baike.baidu.com/item/%E9%80%83%E5%87%BA%E6%83%8A%E9%AD%82%E5%A4%9C/65511213" target="_blank">百度百科-逃出惊魂夜</a> ·
        <a href="https://party.163.com" target="_blank">蛋仔派对官网</a>
      </div>
    </footer>
  </div>
</template>
