import express from 'express';
import cors from 'cors';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { all, get, run } from './db.js';

const app = express();
const PORT = process.env.PORT || 3001;
const JWT_SECRET = process.env.JWT_SECRET || 'fright-night-dev-secret-change-me';

app.use(cors());
app.use(express.json({ limit: '2mb' }));

/* ---------------- 认证中间件 ---------------- */
function auth(req, res, next) {
  const header = req.headers.authorization || '';
  const token = header.startsWith('Bearer ') ? header.slice(7) : '';
  if (!token) return res.status(401).json({ message: '未登录' });
  try {
    req.admin = jwt.verify(token, JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ message: '登录已过期,请重新登录' });
  }
}

/* ---------------- 公开接口:查询 ---------------- */
app.get('/api/chasers', (req, res) => {
  const { q = '', strength = '', sort = 'release_desc' } = req.query;
  let sql = 'SELECT * FROM chasers WHERE 1=1';
  const params = [];
  if (q) { sql += ' AND (name LIKE ? OR title LIKE ?)'; params.push(`%${q}%`, `%${q}%`); }
  if (strength) { sql += ' AND strength = ?'; params.push(strength); }
  const order = {
    release_desc: 'release_date DESC',
    release_asc: 'release_date ASC',
    strength_asc: 'strength ASC',
    difficulty_desc: 'difficulty DESC'
  }[sort] || 'release_date DESC';
  sql += ` ORDER BY ${order}`;
  res.json(all(sql, ...params));
});

app.get('/api/chasers/:id', (req, res) => {
  const row = get('SELECT * FROM chasers WHERE id = ?', req.params.id);
  if (!row) return res.status(404).json({ message: '追捕者不存在' });
  res.json(row);
});

app.get('/api/escapees', (req, res) => {
  const { q = '', role = '' } = req.query;
  let sql = 'SELECT * FROM escapees WHERE 1=1';
  const params = [];
  if (q) { sql += ' AND (name LIKE ? OR title LIKE ?)'; params.push(`%${q}%`, `%${q}%`); }
  if (role) { sql += ' AND role_type = ?'; params.push(role); }
  sql += ' ORDER BY release_date DESC';
  res.json(all(sql, ...params));
});

app.get('/api/escapees/:id', (req, res) => {
  const row = get('SELECT * FROM escapees WHERE id = ?', req.params.id);
  if (!row) return res.status(404).json({ message: '逃生者不存在' });
  res.json(row);
});

app.get('/api/maps', (req, res) => {
  res.json(all('SELECT * FROM maps ORDER BY release_date DESC'));
});

app.get('/api/maps/:id', (req, res) => {
  const map = get('SELECT * FROM maps WHERE id = ?', req.params.id);
  if (!map) return res.status(404).json({ message: '地图不存在' });
  const elements = all('SELECT * FROM map_elements WHERE map_id = ? ORDER BY sort_order, id', map.id);
  res.json({ ...map, elements });
});

/* ---------------- 数据分析统计 ---------------- */
app.get('/api/stats', (_req, res) => {
  const count = (t) => get(`SELECT COUNT(*) AS n FROM ${t}`).n;
  const chasers = count('chasers');
  const escapees = count('escapees');
  const maps = count('maps');
  const elements = count('map_elements');
  const badges = count('badges');
  const patches = count('patches');

  const strengthDist = all('SELECT strength AS name, COUNT(*) AS value FROM chasers GROUP BY strength');
  const roleDist = all("SELECT role_type AS name, COUNT(*) AS value FROM escapees WHERE role_type != '' GROUP BY role_type");
  const timeline = all(`
    SELECT substr(release_date, 1, 7) AS month,
           SUM(kind = '追捕者') AS 追捕者,
           SUM(kind = '逃生者') AS 逃生者
    FROM (
      SELECT release_date, '追捕者' AS kind FROM chasers WHERE release_date != ''
      UNION ALL
      SELECT release_date, '逃生者' AS kind FROM escapees WHERE release_date != ''
    )
    GROUP BY month ORDER BY month`);
  const difficultyDist = all('SELECT difficulty AS name, COUNT(*) AS value FROM chasers GROUP BY difficulty ORDER BY difficulty');
  const elementTypes = all('SELECT type AS name, COUNT(*) AS value FROM map_elements GROUP BY type ORDER BY value DESC');

  res.json({
    overview: { chasers, escapees, maps, elements, badges, patches, ratio: '1 : 4' },
    strengthDist, roleDist, timeline, difficultyDist, elementTypes
  });
});

/* ---------------- 认证 ---------------- */
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body || {};
  const admin = get('SELECT * FROM admins WHERE username = ?', username || '');
  if (!admin || !bcrypt.compareSync(password || '', admin.password_hash)) {
    return res.status(401).json({ message: '用户名或密码错误' });
  }
  const token = jwt.sign({ id: admin.id, username: admin.username }, JWT_SECRET, { expiresIn: '7d' });
  res.json({ token, username: admin.username });
});

app.post('/api/auth/password', auth, (req, res) => {
  const { oldPassword, newPassword } = req.body || {};
  const admin = get('SELECT * FROM admins WHERE id = ?', req.admin.id);
  if (!admin || !bcrypt.compareSync(oldPassword || '', admin.password_hash)) {
    return res.status(400).json({ message: '原密码错误' });
  }
  if (!newPassword || String(newPassword).length < 6) {
    return res.status(400).json({ message: '新密码至少 6 位' });
  }
  run('UPDATE admins SET password_hash = ? WHERE id = ?', bcrypt.hashSync(newPassword, 10), admin.id);
  res.json({ message: '密码修改成功' });
});

/* ---------------- 公开接口:版本公告 / 徽章 ---------------- */
app.get('/api/patches', (_req, res) => {
  res.json(all('SELECT * FROM patches ORDER BY date DESC, id DESC'));
});

app.get('/api/badges', (req, res) => {
  const { faction = '', category = '' } = req.query;
  let sql = 'SELECT * FROM badges WHERE 1=1';
  const params = [];
  if (faction) { sql += ' AND faction = ?'; params.push(faction); }
  if (category) { sql += ' AND category = ?'; params.push(category); }
  sql += " ORDER BY CASE grade WHEN '典藏' THEN 0 ELSE 1 END, faction DESC, id";
  res.json(all(sql, ...params));
});

/* ---------------- 管理接口:通用 CRUD 工厂 ---------------- */
const JSON_COLS = new Set(['skills', 'summary']);
const TABLES = {
  chasers: ['name', 'title', 'emoji', 'difficulty', 'strength', 'release_date', 'story', 'skills', 'tips', 'status'],
  escapees: ['name', 'title', 'emoji', 'role_type', 'difficulty', 'release_date', 'story', 'skills', 'tips', 'status'],
  maps: ['name', 'emoji', 'theme', 'release_date', 'size', 'description', 'status'],
  patches: ['date', 'title', 'summary'],
  badges: ['name', 'faction', 'category', 'grade', 'description']
};

function listAll(table) {
  const order = { patches: 'date DESC, id DESC', badges: "CASE grade WHEN '典藏' THEN 0 ELSE 1 END, faction DESC, id" }[table] || 'id';
  return (_req, res) => res.json(all(`SELECT * FROM ${table} ORDER BY ${order}`));
}

function createOne(table) {
  const cols = TABLES[table];
  return (req, res) => {
    const body = req.body || {};
    if (!body.name && !body.title) return res.status(400).json({ message: '名称不能为空' });
    const values = cols.map((c) => {
      const v = body[c];
      if (JSON_COLS.has(c)) return JSON.stringify(Array.isArray(v) ? v : []);
      return v ?? '';
    });
    const placeholders = cols.map(() => '?').join(',');
    const result = run(`INSERT INTO ${table} (${cols.join(',')}) VALUES (${placeholders})`, ...values);
    res.json(get(`SELECT * FROM ${table} WHERE id = ?`, result.lastInsertRowid));
  };
}

function updateOne(table) {
  const cols = TABLES[table];
  return (req, res) => {
    const existing = get(`SELECT * FROM ${table} WHERE id = ?`, req.params.id);
    if (!existing) return res.status(404).json({ message: '记录不存在' });
    const body = req.body || {};
    const colsInBody = cols.filter((c) => c in body);
    if (!colsInBody.length) return res.json(existing);
    const sets = colsInBody.map((c) => `${c} = ?`);
    const values = colsInBody.map((c) => {
      const v = body[c];
      return JSON_COLS.has(c) ? JSON.stringify(Array.isArray(v) ? v : []) : (v ?? '');
    });
    if (table !== 'patches' && table !== 'badges') sets.push("updated_at = datetime('now', 'localtime')");
    run(`UPDATE ${table} SET ${sets.join(', ')} WHERE id = ?`, ...values, req.params.id);
    res.json(get(`SELECT * FROM ${table} WHERE id = ?`, req.params.id));
  };
}

function deleteOne(table) {
  return (req, res) => {
    run(`DELETE FROM ${table} WHERE id = ?`, req.params.id);
    res.json({ message: '删除成功' });
  };
}

for (const table of Object.keys(TABLES)) {
  const r = express.Router();
  r.get('/', auth, listAll(table));
  r.post('/', auth, createOne(table));
  r.put('/:id', auth, updateOne(table));
  r.delete('/:id', auth, deleteOne(table));
  app.use(`/api/admin/${table}`, r);
}

/* ---------------- 地图元素管理 ---------------- */
const elements = express.Router();

elements.get('/map/:mapId', auth, (req, res) => {
  res.json(all('SELECT * FROM map_elements WHERE map_id = ? ORDER BY sort_order, id', req.params.mapId));
});

elements.post('/map/:mapId', auth, (req, res) => {
  const { name, type = '机制', icon = '📦', description = '', sort_order = 0 } = req.body || {};
  if (!name) return res.status(400).json({ message: '元素名称不能为空' });
  const map = get('SELECT id FROM maps WHERE id = ?', req.params.mapId);
  if (!map) return res.status(404).json({ message: '地图不存在' });
  const result = run(
    'INSERT INTO map_elements (map_id, name, type, icon, description, sort_order) VALUES (?,?,?,?,?,?)',
    map.id, name, type, icon, description, sort_order
  );
  res.json(get('SELECT * FROM map_elements WHERE id = ?', result.lastInsertRowid));
});

elements.put('/:id', auth, (req, res) => {
  const body = req.body || {};
  const sets = [];
  const values = [];
  for (const col of ['name', 'type', 'icon', 'description', 'sort_order']) {
    if (col in body) { sets.push(`${col} = ?`); values.push(body[col]); }
  }
  if (sets.length) run(`UPDATE map_elements SET ${sets.join(', ')} WHERE id = ?`, ...values, req.params.id);
  res.json(get('SELECT * FROM map_elements WHERE id = ?', req.params.id));
});

elements.delete('/:id', auth, (req, res) => {
  run('DELETE FROM map_elements WHERE id = ?', req.params.id);
  res.json({ message: '删除成功' });
});

app.use('/api/admin/elements', elements);

app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({ message: '服务器内部错误' });
});

app.listen(PORT, () => {
  console.log(`🌙 逃出惊魂夜数据站后端已启动: http://localhost:${PORT}`);
});
