<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { http } from '../api.js';

const route = useRoute();
const faction = computed(() => route.meta.faction);
const isChaser = computed(() => faction.value === 'chasers');

const list = ref([]);
const loading = ref(false);
const dialog = ref(false);
const saving = ref(false);
const form = ref({});
const editingId = ref(null);

const EMOTES = ['🔪', '👻', '🥚', '🦁', '💃', '🪖', '⛏️', '🩺', '🎩', '👒', '🤵', '🏹', '🧨', '📰', '🧪', '🌊', '🥊', '⚓', '🔮', '⛪', '🎀', '⚗️', '🪓', '🎤', '🤫', '🐘', '🤡', '🚨', '🐺', '🐍', '💉', '📚', '🐈‍⬛', '🎒', '🖼️', '⚔️'];

function blank() {
  return {
    name: '', title: '', emoji: isChaser.value ? '🔪' : '🥚', role_type: '', difficulty: 3,
    strength: '', release_date: '', story: '', skills: [], tips: '', status: 'live'
  };
}

async function load() {
  loading.value = true;
  try { list.value = await http.get(`/admin/${faction.value}`); } finally { loading.value = false; }
}
onMounted(load);

function openCreate() {
  editingId.value = null;
  form.value = blank();
  dialog.value = true;
}
function openEdit(row) {
  editingId.value = row.id;
  form.value = { ...blank(), ...row, skills: (row.skills || []).map((s) => ({ ...s })) };
  dialog.value = true;
}

async function save() {
  if (!form.value.name) return ElMessage.warning('名称不能为空');
  saving.value = true;
  try {
    if (editingId.value) await http.put(`/admin/${faction.value}/${editingId.value}`, form.value);
    else await http.post(`/admin/${faction.value}`, form.value);
    ElMessage.success('保存成功');
    dialog.value = false;
    load();
  } finally { saving.value = false; }
}

function remove(row) {
  ElMessageBox.confirm(`确定删除「${row.name}」吗?`, '删除确认', { type: 'warning' }).then(async () => {
    await http.delete(`/admin/${faction.value}/${row.id}`);
    ElMessage.success('已删除');
    load();
  }).catch(() => {});
}

function addSkill() {
  form.value.skills.push({ type: '主动', name: '', desc: '' });
}
</script>

<template>
  <div>
    <h2 style="margin-bottom: 16px">{{ isChaser ? '追捕者管理' : '逃生者管理' }}</h2>
    <div class="page-card">
      <div class="toolbar">
        <el-button type="primary" @click="openCreate">+ 新增{{ isChaser ? '追捕者' : '逃生者' }}</el-button>
        <span class="spacer"></span>
        <span style="color: #a89fc7; font-size: 13px">共 {{ list.length }} 名</span>
      </div>
      <el-table :data="list" v-loading="loading" style="width: 100%" size="large">
        <el-table-column label="头像" width="70">
          <template #default="{ row }"><span style="font-size: 24px">{{ row.emoji }}</span></template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="150" />
        <el-table-column prop="title" label="称号" min-width="130" show-overflow-tooltip />
        <el-table-column v-if="!isChaser" prop="role_type" label="定位" width="120" />
        <el-table-column prop="difficulty" label="难度" width="70" />
        <el-table-column prop="release_date" label="上线日期" width="120" />
        <el-table-column label="技能数" width="80">
          <template #default="{ row }">{{ (row.skills || []).length }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 'live' ? 'success' : 'info'" size="small">
              {{ row.status === 'live' ? '已上线' : '待上线' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialog" :title="editingId ? '编辑角色' : '新增角色'" width="720px" top="4vh">
      <el-form :model="form" label-width="90px">
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="名称"><el-input v-model="form.name" placeholder="如:矿工-卢修斯" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="称号"><el-input v-model="form.title" /></el-form-item></el-col>
          <el-col :span="8">
            <el-form-item label="头像">
              <el-select v-model="form.emoji" filterable allow-create style="width: 100%">
                <el-option v-for="e in EMOTES" :key="e" :label="e" :value="e" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="定位"><el-input v-model="form.role_type" :placeholder="isChaser ? '如:强攻、远程' : '如:修机位'" /></el-form-item></el-col>
          <el-col :span="8">
            <el-form-item label="难度(1-5)">
              <el-input-number v-model="form.difficulty" :min="1" :max="5" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8"><el-form-item label="强度评级"><el-input v-model="form.strength" placeholder="如:T0 / T1(可留空)" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="12">
          <el-col :span="8">
            <el-form-item label="上线日期">
              <el-date-picker v-model="form.release_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="状态">
              <el-select v-model="form.status" style="width: 100%">
                <el-option label="已上线" value="live" />
                <el-option label="待上线/爆料" value="soon" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="角色小传"><el-input v-model="form.story" type="textarea" :rows="4" /></el-form-item>
        <el-form-item label="玩法提示"><el-input v-model="form.tips" type="textarea" :rows="2" /></el-form-item>

        <el-form-item label="技能">
          <div style="width: 100%">
            <div v-for="(s, i) in form.skills" :key="i" style="display: flex; gap: 8px; margin-bottom: 8px">
              <el-select v-model="s.type" style="width: 100px">
                <el-option label="主动" value="主动" />
                <el-option label="被动" value="被动" />
                <el-option label="处决" value="处决" />
              </el-select>
              <el-input v-model="s.name" placeholder="技能名" style="width: 220px" />
              <el-input v-model="s.desc" placeholder="技能描述" />
              <el-button type="danger" plain @click="form.skills.splice(i, 1)">删</el-button>
            </div>
            <el-button size="small" @click="addSkill">+ 添加技能</el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>
