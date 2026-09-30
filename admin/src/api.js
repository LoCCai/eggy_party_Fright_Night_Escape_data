import axios from 'axios';
import { ElMessage } from 'element-plus';

export const http = axios.create({ baseURL: '/api', timeout: 15000 });

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('fne:token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

http.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const msg = err.response?.data?.message || err.message || '请求失败';
    ElMessage.error(msg);
    if (err.response?.status === 401 && location.pathname !== '/login') {
      localStorage.removeItem('fne:token');
      location.href = '/login';
    }
    return Promise.reject(err);
  }
);
