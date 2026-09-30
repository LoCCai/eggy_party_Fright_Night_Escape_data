<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { http } from '../api.js';

const list = ref([]);
const loading = ref(false);
const dialog = ref(false);
const saving = ref(false);
const editingId = ref(null);
const form = ref({ date: '', title: '', summaryText: '' });

async function load() {
  loading.value = true;
  try { list.value = await http.get('/admin/patches'); } finally { loading.value = false; }
}
onMounted(load);

function openCreate() {
  editingId.value = null;
  form.value = { date: '', title: '', summaryText: '' };
  dialog.value = true;
}
function openEdit(row) {
  editingId.value = row.id;
  form.value = { date: row.date, title: row.title, summaryText: (row.summary || []).join('\n') };
  dialog.value = true;
}
async function save() {
  if (!form.value.title) return ElMessage.warning('标题不能为空');
  saving.value = true;
  try {
    const payload = {
      date: form.value.date || '',
      title: form.value.title,
      summary: form.value.summaryText.split('\n').map((s) => s.trim()).filter(Boolean)
    };
    if (editingId.value) await http.put(`/admin/patches/${editingId.value}`, payload);
    else await http.post('/admin/patches', payload);
    ElMessage.success('保存成功');
    dialog.value = false;
    load();
  } finally { saving.value = false; }
}
function remove(row) {
  ElMessageBox.confirm(`确定删除公告「${row.title}」吗?`, '删除确认', { type: 'warning' }).then(async () => {
    await http.delete(`/admin/patches/${row.id}`);
    ElMessage.success('已删除');
    load();
  }).catch(() => {});
}
</script>

<template>
  <div>
    <h2 style="margin-bottom: 16px">版本公告管理</h2>
    <div class="page-card">
      <div class="toolbar">
        <el-button type="primary" @click="openCreate">+ 新增公告</el-button>
        <span class="spacer"></span>
        <span style="color: #a89fc7; font-size: 13px">共 {{ list.length }} 条</span>
      </div>
      <el-table :data="list" v-loading="loading" style="width: 100%" size="large">
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="title" label="标题" min-width="220" />
        <el-table-column label="摘要条数" width="100">
          <template #default="{ row }">{{ (row.summary || []).length }}</template>
        </el-table-column>
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialog" :title="editingId ? '编辑公告' : '新增公告'" width="620px">
      <el-form label-width="80px">
        <el-row :gutter="12">
          <el-col :span="10">
            <el-form-item label="日期">
              <el-date-picker v-model="form.date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="14"><el-form-item label="标题"><el-input v-model="form.title" placeholder="如:血衣教师 + 船长 + 码头" /></el-form-item></el-col>
        </el-row>
        <el-form-item label="摘要">
          <el-input
            v-model="form.summaryText" type="textarea" :rows="8"
            placeholder="每行一条摘要,例如:&#10;新追捕者 血衣教师-礼温&#10;新地图 惊魂码头"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>
