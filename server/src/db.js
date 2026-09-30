import { DatabaseSync } from 'node:sqlite';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dataDir = path.join(__dirname, '..', 'data');
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

const db = new DatabaseSync(path.join(dataDir, 'fright-night.db'));
db.exec('PRAGMA foreign_keys = ON');

db.exec(`
CREATE TABLE IF NOT EXISTS admins (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS chasers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  title TEXT DEFAULT '',
  emoji TEXT DEFAULT '👻',
  role_type TEXT DEFAULT '',
  difficulty INTEGER DEFAULT 3,
  strength TEXT DEFAULT 'T2',
  release_date TEXT DEFAULT '',
  story TEXT DEFAULT '',
  skills TEXT DEFAULT '[]',
  tips TEXT DEFAULT '',
  status TEXT DEFAULT 'live',
  created_at TEXT DEFAULT (datetime('now', 'localtime')),
  updated_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS escapees (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  title TEXT DEFAULT '',
  emoji TEXT DEFAULT '🥚',
  role_type TEXT DEFAULT '',
  difficulty INTEGER DEFAULT 3,
  release_date TEXT DEFAULT '',
  story TEXT DEFAULT '',
  skills TEXT DEFAULT '[]',
  tips TEXT DEFAULT '',
  status TEXT DEFAULT 'live',
  created_at TEXT DEFAULT (datetime('now', 'localtime')),
  updated_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS maps (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  emoji TEXT DEFAULT '🗺️',
  theme TEXT DEFAULT '',
  release_date TEXT DEFAULT '',
  size TEXT DEFAULT '',
  description TEXT DEFAULT '',
  status TEXT DEFAULT 'live',
  created_at TEXT DEFAULT (datetime('now', 'localtime')),
  updated_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS map_elements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  map_id INTEGER NOT NULL REFERENCES maps(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  type TEXT DEFAULT '机制',
  icon TEXT DEFAULT '📦',
  description TEXT DEFAULT '',
  sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS patches (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT DEFAULT '',
  title TEXT DEFAULT '',
  summary TEXT DEFAULT '[]',
  created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS badges (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  faction TEXT DEFAULT '逃生者',
  category TEXT DEFAULT '',
  grade TEXT DEFAULT '稀有',
  description TEXT DEFAULT '',
  created_at TEXT DEFAULT (datetime('now', 'localtime'))
);
`);

/** 把数据库行里的 JSON 字段解析成对象 */
function parseRow(row) {
  if (!row) return row;
  const out = { ...row };
  for (const col of ['skills', 'summary']) {
    if (typeof out[col] === 'string') {
      try { out[col] = JSON.parse(out[col]); } catch { out[col] = []; }
    }
  }
  return out;
}

export function all(sql, ...params) {
  return db.prepare(sql).all(...params).map(parseRow);
}
export function get(sql, ...params) {
  return parseRow(db.prepare(sql).get(...params));
}
export function run(sql, ...params) {
  return db.prepare(sql).run(...params);
}

export default db;
