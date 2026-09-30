<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { http } from '../api.js';

const list = ref([]);
const loading = ref(false);
const dialog = ref(false);
const saving = ref(false);
const editingId = ref(null);
const form = ref({});

/** 元素管理抽屉 */
const drawer = ref(false);
const currentMap = ref(null);
const elements = ref([]);
const eleDialog = ref(false);
const eleSaving = ref(false);
const editingEleId = ref(null);
const eleForm = ref({ name: '', type: '机制', icon: '📦', description: '', sort_order: 0 });

const TYPES = ['机制', '地形', '交互', '点位', '道具', '氛围'];

function blank() {
  return { name: '', emoji: '🗺️', theme: '', release_date: '', size: '中型', description: '', status: 'live' };
}

async function load() {
  loading.value = true;
  try { list.value = await http.get('/admin/maps'); } finally { loading.value = false; }
}
onMounted(load);

function openCreate() {
  editingId.value = null;
  form.value = blank();
  dialog.value = true;
}
function openEdit(row) {
  editingId.value = row.id;
  form.value = { ...blank(), ...row };
  dialog.value = true;
}
async function save() {
  if (!form.value.name) return ElMessage.warning('名称不能为空');
  saving.value = true;
  try {
    if (editingId.value) await http.put(`/admin/maps/${editingId.value}`, form.value);
    else await http.post('/admin/maps', form.value);
    ElMessage.success('保存成功');
    dialog.value = false;
    load();
  } finally { saving.value = false; }
}
function remove(row) {
  ElMessageBox.confirm(`确定删除地图「${row.name}」吗?其下所有元素将一并删除!`, '删除确认', { type: 'warning' })
    .then(async () => {
      await http.delete(`/admin/maps/${row.id}`);
      ElMessage.success('已删除');
      load();
    }).catch(() => {});
}

/* ---------- 元素管理 ---------- */
async function openElements(row) {
  currentMap.value = row;
  drawer.value = true;
  await loadElements();
}
async function loadElements() {
  elements.value = await http.get(`/admin/elements/map/${currentMap.value.id}`);
}
function openEleCreate() {
  editingEleId.value = null;
  eleForm.value = { name: '', type: '机制', icon: '📦', description: '', sort_order: elements.value.length };
  eleDialog.value = true;
}
function openEleEdit(row) {
  editingEleId.value = row.id;
  eleForm.value = { ...row };
  eleDialog.value = true;
}
async function saveEle() {
  if (!eleForm.value.name) return ElMessage.warning('元素名称不能为空');
  eleSaving.value = true;
  try {
    if (editingEleId.value) await http.put(`/admin/elements/${editingEleId.value}`, eleForm.value);
    else await http.post(`/admin/elements/map/${currentMap.value.id}`, eleForm.value);
    ElMessage.success('保存成功');
    eleDialog.value = false;
    await loadElements();
    load();
  } finally { eleSaving.value = false; }
}
function removeEle(row) {
  ElMessageBox.confirm(`确定删除元素「${row.name}」吗?`, '删除确认', { type: 'warning' })
    .then(async () => {
      await http.delete(`/admin/elements/${row.id}`);
      ElMessage.success('已删除');
      await loadElements();
      load();
    }).catch(() => {});
}
</script>

<template>
  <div>
    <h2 style="margin-bottom: 16px">地图与元素管理</h2>
    <div class="page-card">
      <div class="toolbar">
        <el-button type="primary" @click="openCreate">+ 新增地图</el-button>
        <span class="spacer"></span>
        <span style="color: #a89fc7; font-size: 13px">共 {{ list.length }} 张</span>
      </div>
      <el-table :data="list" v-loading="loading" style="width: 100%" size="large">
        <el-table-column label="" width="70">
          <template #default="{ row }"><span style="font-size: 24px">{{ row.emoji }}</span></template>
        </el-table-column>
        <el-table-column prop="name" label="地图名" min-width="130" />
        <el-table-column prop="theme" label="主题" min-width="140" />
        <el-table-column prop="size" label="规模" width="90" />
        <el-table-column prop="release_date" label="上线日期" width="120" />
        <el-table-column prop="description" label="简介" min-width="220" show-overflow-tooltip />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="success" plain @click="openElements(row)">元素管理</el-button>
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialog" :title="editingId ? '编辑地图' : '新增地图'" width="620px">
      <el-form :model="form" label-width="90px">
        <el-row :gutter="12">
          <el-col :span="12"><el-form-item label="地图名"><el-input v-model="form.name" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="主题"><el-input v-model="form.theme" placeholder="如:港口·迷雾货仓" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="12">
          <el-col :span="8">
            <el-form-item label="上线日期">
              <el-date-picker v-model="form.release_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="规模">
              <el-select v-model="form.size" style="width: 100%">
                <el-option v-for="s in ['小型', '中型', '大型']" :key="s" :label="s" :value="s" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="状态">
              <el-select v-model="form.status" style="width: 100%">
                <el-option label="已上线" value="live" />
                <el-option label="待上线" value="soon" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="简介"><el-input v-model="form.description" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <el-drawer v-model="drawer" :title="`🧩 ${currentMap?.name} · 元素管理`" size="560px">
      <el-button type="primary" style="margin-bottom: 14px" @click="openEleCreate">+ 新增元素</el-button>
      <div v-for="e in elements" :key="e.id" class="page-card" style="margin-bottom: 10px; position: relative">
        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 6px">
          <span style="font-size: 20px">{{ e.icon }}</span>
          <b>{{ e.name }}</b>
          <el-tag size="small">{{ e.type }}</el-tag>
        </div>
        <p style="color: #a89fc7; font-size: 13px; line-height: 1.7">{{ e.description }}</p>
        <div style="margin-top: 8px">
          <el-button size="small" @click="openEleEdit(e)">编辑</el-button>
          <el-button size="small" type="danger" @click="removeEle(e)">删除</el-button>
        </div>
      </div>

      <el-dialog v-model="eleDialog" :title="editingEleId ? '编辑元素' : '新增元素'" width="480px" append-to-body>
        <el-form :model="eleForm" label-width="80px">
          <el-form-item label="名称"><el-input v-model="eleForm.name" /></el-form-item>
          <el-row :gutter="12">
            <el-col :span="12">
              <el-form-item label="类型">
                <el-select v-model="eleForm.type" style="width: 100%">
                  <el-option v-for="t in TYPES" :key="t" :label="t" :value="t" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12"><el-form-item label="图标"><el-input v-model="eleForm.icon" /></el-form-item></el-col>
          </el-row>
          <el-form-item label="描述"><el-input v-model="eleForm.description" type="textarea" :rows="4" /></el-form-item>
          <el-form-item label="排序"><el-input-number v-model="eleForm.sort_order" :min="0" /></el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="eleDialog = false">取消</el-button>
          <el-button type="primary" :loading="eleSaving" @click="saveEle">保存</el-button>
        </template>
      </el-dialog>
    </el-drawer>
  </div>
</template>
