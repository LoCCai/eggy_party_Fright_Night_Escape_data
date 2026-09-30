<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { http } from '../api.js';

const router = useRouter();
const route = useRoute();
const username = localStorage.getItem('fne:username') || 'admin';
const pwdVisible = ref(false);
const pwd = ref({ oldPassword: '', newPassword: '' });

const menus = [
  { path: '/', label: '仪表盘', icon: 'Odometer' },
  { path: '/chasers', label: '追捕者管理', icon: 'Knife' },
  { path: '/escapees', label: '逃生者管理', icon: 'Chicken' },
  { path: '/maps', label: '地图与元素', icon: 'MapLocation' },
  { path: '/patches', label: '版本公告', icon: 'Bell' },
  { path: '/badges', label: '徽章管理', icon: 'Trophy' }
];

async function changePwd() {
  if (!pwd.value.oldPassword || pwd.value.newPassword.length < 6) {
    return ElMessage.warning('新密码至少 6 位');
  }
  await http.post('/auth/password', pwd.value);
  ElMessage.success('密码修改成功');
  pwdVisible.value = false;
  pwd.value = { oldPassword: '', newPassword: '' };
}

function logout() {
  ElMessageBox.confirm('确定退出登录吗?', '提示', { type: 'warning' }).then(() => {
    localStorage.removeItem('fne:token');
    router.push('/login');
  }).catch(() => {});
}
</script>

<template>
  <el-container style="min-height: 100vh">
    <el-aside width="220px" style="background: #171230; border-right: 1px solid #3a3060">
      <div style="padding: 20px 18px; font-weight: 800; font-size: 16px">🌙 惊魂夜 · 后台</div>
      <el-menu :default-active="route.path" router style="border: none; background: transparent" text-color="#a89fc7" active-text-color="#a78bfa">
        <el-menu-item v-for="m in menus" :key="m.path" :index="m.path">
          <el-icon><component :is="m.icon" /></el-icon>
          <span>{{ m.label }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header style="display: flex; align-items: center; justify-content: flex-end; gap: 14px; background: #1e1839; border-bottom: 1px solid #3a3060">
        <el-button text @click="pwdVisible = true">修改密码</el-button>
        <el-tag type="primary">{{ username }}</el-tag>
        <el-button text type="danger" @click="logout">退出</el-button>
      </el-header>
      <el-main style="background: #0d0a1a">
        <router-view />
      </el-main>
    </el-container>
  </el-container>

  <el-dialog v-model="pwdVisible" title="修改密码" width="420px">
    <el-form label-position="top">
      <el-form-item label="原密码"><el-input v-model="pwd.oldPassword" type="password" show-password /></el-form-item>
      <el-form-item label="新密码(至少 6 位)"><el-input v-model="pwd.newPassword" type="password" show-password /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="pwdVisible = false">取消</el-button>
      <el-button type="primary" @click="changePwd">保存</el-button>
    </template>
  </el-dialog>
</template>
