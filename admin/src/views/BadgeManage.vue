<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { http } from '../api.js';

const list = ref([]);
const loading = ref(false);
const filterFaction = ref('');
const dialog = ref(false);
const saving = ref(false);
const editingId = ref(null);
const form = ref({});

const CATEGORIES = ['救援', '视野', '加速', '特殊', '追击', '防御', '控场'];

function blank() {
  return { name: '', faction: '逃生者', category: '救援', grade: '稀有', description: '' };
}

async function load() {
  loading.value = true;
  try { list.value = await http.get('/admin/badges'); } finally { loading.value = false; }
}
onMounted(load);

const filtered = () => (filterFaction.value ? list.value.filter((b) => b.faction === filterFaction.value) : list.value);

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
    if (editingId.value) await http.put(`/admin/badges/${editingId.value}`, form.value);
    else await http.post('/admin/badges', form.value);
    ElMessage.success('保存成功');
    dialog.value = false;
    load();
  } finally { saving.value = false; }
}
function remove(row) {
  ElMessageBox.confirm(`确定删除徽章「${row.name}」吗?`, '删除确认', { type: 'warning' }).then(async () => {
    await http.delete(`/admin/badges/${row.id}`);
    ElMessage.success('已删除');
    load();
  }).catch(() => {});
}
</script>

<template>
  <div>
    <h2 style="margin-bottom: 16px">徽章管理</h2>
    <div class="page-card">
      <div class="toolbar">
        <el-button type="primary" @click="openCreate">+ 新增徽章</el-button>
        <el-radio-group v-model="filterFaction" style="margin-left: 10px">
          <el-radio-button value="">全部</el-radio-button>
          <el-radio-button value="逃生者">逃生者</el-radio-button>
          <el-radio-button value="追捕者">追捕者</el-radio-button>
        </el-radio-group>
        <span class="spacer"></span>
        <span style="color: #a89fc7; font-size: 13px">共 {{ filtered().length }} 枚</span>
      </div>
      <el-table :data="filtered()" v-loading="loading" style="width: 100%" size="large">
        <el-table-column prop="name" label="徽章" min-width="130" />
        <el-table-column prop="faction" label="阵营" width="90" />
        <el-table-column prop="category" label="类别" width="90" />
        <el-table-column label="品级" width="90">
          <template #default="{ row }">
            <el-tag :type="row.grade === '典藏' ? 'warning' : 'info'" size="small">{{ row.grade }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="效果" min-width="300" show-overflow-tooltip />
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialog" :title="editingId ? '编辑徽章' : '新增徽章'" width="560px">
      <el-form :model="form" label-width="80px">
        <el-row :gutter="12">
          <el-col :span="10"><el-form-item label="名称"><el-input v-model="form.name" /></el-form-item></el-col>
          <el-col :span="7">
            <el-form-item label="阵营">
              <el-select v-model="form.faction" style="width: 100%">
                <el-option label="逃生者" value="逃生者" />
                <el-option label="追捕者" value="追捕者" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item label="品级">
              <el-select v-model="form.grade" style="width: 100%">
                <el-option label="典藏" value="典藏" />
                <el-option label="稀有" value="稀有" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="类别">
          <el-select v-model="form.category" style="width: 100%">
            <el-option v-for="c in CATEGORIES" :key="c" :label="c" :value="c" />
          </el-select>
        </el-form-item>
        <el-form-item label="效果"><el-input v-model="form.description" type="textarea" :rows="4" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>
