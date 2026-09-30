<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { http } from '../api.js';

const router = useRouter();
const form = ref({ username: '', password: '' });
const loading = ref(false);

async function submit() {
  if (!form.value.username || !form.value.password) {
    return ElMessage.warning('请输入用户名和密码');
  }
  loading.value = true;
  try {
    const data = await http.post('/auth/login', form.value);
    localStorage.setItem('fne:token', data.token);
    localStorage.setItem('fne:username', data.username);
    ElMessage.success(`欢迎回来,${data.username}`);
    router.push('/');
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center;
    background: radial-gradient(800px 400px at 70% 0%, rgba(124,92,240,.25), transparent), #0d0a1a">
    <div class="page-card" style="width: 380px; padding: 34px">
      <h1 style="font-size: 22px; text-align: center">🌙 逃出惊魂夜 · 管理面板</h1>
      <p style="text-align: center; color: #a89fc7; font-size: 13px; margin: 8px 0 24px">蛋仔派对非对称竞技玩法数据后台</p>
      <el-form :model="form" label-position="top" size="large" @keyup.enter="submit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="admin" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="admin123" />
        </el-form-item>
        <el-button type="primary" size="large" style="width: 100%; margin-top: 6px" :loading="loading" @click="submit">
          登 录
        </el-button>
      </el-form>
      <p style="color: #6b6390; font-size: 12px; margin-top: 16px; text-align: center">默认账号 admin / admin123,登录后请及时修改</p>
    </div>
  </div>
</template>
