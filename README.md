# 🌙 蛋仔派对 · 逃出惊魂夜 数据查询站

一个供玩家查询《蛋仔派对》「逃出惊魂夜」玩法(别称 **第五蛋格**,与《第五人格》联动的非对称竞技模式)数据的站点,前后端分离架构,内置管理面板与数据分析。

## 项目结构

```
eggy_party_Fright_Night_Escape_data/
├── server/     # 后端服务:Express + SQLite(Node 内置 node:sqlite,零编译依赖)
│   ├── src/index.js       # REST API(公开查询 + JWT 管理接口 + 统计)
│   ├── src/db.js          # 数据库建表(角色/地图/元素/公告/徽章/管理员)
│   ├── src/seed.js        # 种子数据写入
│   └── src/data/          # 角色结构化数据、版本公告、徽章(JSON)
├── web/        # 玩家端展示站:Vue 3 + Vite + ECharts(深色惊魂夜主题)
├── admin/      # 管理面板:Vue 3 + Element Plus(登录 / 角色·地图·公告·徽章 CRUD / 仪表盘)
└── docs/       # 数据来源说明与官方公告检索归档(docs/archive/)
```

## 快速启动

```bash
# 1. 安装依赖
npm run setup          # 或分别进入 server / web / admin 执行 npm install

# 2. 写入种子数据(首次启动前)
npm run seed           # 默认管理员 admin / admin123

# 3. 分别启动三个服务(三个终端)
npm run server         # 后端 API  → http://localhost:3001
npm run web            # 玩家端    → http://localhost:5173
npm run admin          # 管理面板  → http://localhost:5174
```

开发模式下 web / admin 均已配置代理,`/api` 请求自动转发到 3001 端口。

## 功能一览

### 玩家端(web)
- **首页**:玩法速览(1v4 / 2v8 获胜条件、蒸汽炉、爆米花大炮、地窖规则)+ 数据概览
- **追捕者图鉴**(12 名):哑女-斯黛拉、疯象-莫比、怨灵小丑-阿巴、魔警-艾琳、困兽-雷蒙德、冥蛇-佩姬、丧心护士-海瑟、血衣教师-礼温、影爪-梵蒂娅、转校生-桃乐丝、画中女郎-贝琳达、少盟主-沈昭;支持搜索与排序
- **逃生者图鉴**(21 名):驯兽师-美狄亚、舞女-莉莉丝、矿工-卢修斯、医生-桑吉斯、炼金师-赫拉、行刑官-比努斯、歌女-小阿娇等;支持按定位筛选
- **角色详情**:主动 / 被动 / 处决技能、官方定位、上线日期、角色小传
- **地图档案**(4 张):惊魂马戏团(2024-07-19)、惊魂火车站(2025-01-24)、惊魂码头(2025-07-18)、惊魂不夜楼(2026-08-14),含码头潜水、火车站双撤离等专属机制
- **地图元素自定义显隐**:每张地图的蒸汽炉 / 火车 / 水闸 / 暗门等元素,可点击 👁 单独隐藏或恢复,支持按类型筛选,偏好保存在浏览器 localStorage(按地图独立)
- **徽章图鉴**(34 枚):逃生者(救援/视野/加速/特殊)与追捕者(追击/防御/控场/视野)阵营徽章,典藏/稀有筛选
- **版本动态**(29 条):2024-08 ~ 2026-09 的新角色 / 新地图 / 平衡调整时间线
- **数据分析**:阵营构成、新角色上线时间线、逃生者定位分布、地图元素类型统计(ECharts)

### 管理面板(admin,http://localhost:5174)
- JWT 登录(默认 `admin / admin123`,可修改密码)
- 追捕者 / 逃生者管理:新增、编辑(含技能条目动态编辑)、删除
- 地图管理:地图 CRUD + **元素管理抽屉**(每张地图可维护任意数量的专属元素)
- 版本公告管理:日期 + 标题 + 逐条摘要
- 徽章管理:阵营 / 类别 / 品级 / 效果
- 仪表盘:数据统计与图表

## API 摘要

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /api/chasers / /api/escapees | 角色列表(支持 `q` 搜索、`sort` 排序、`role` 定位筛选) |
| GET | /api/chasers/:id / /api/escapees/:id | 角色详情 |
| GET | /api/maps, /api/maps/:id | 地图列表 / 详情(详情含元素) |
| GET | /api/patches | 版本公告时间线(按日期倒序) |
| GET | /api/badges | 徽章列表(支持 `faction` / `category` 筛选) |
| GET | /api/stats | 数据分析统计 |
| POST | /api/auth/login | 管理员登录 |
| POST | /api/auth/password | 修改密码(需 Token) |
| CRUD | /api/admin/{chasers\|escapees\|maps\|patches\|badges} | 管理接口(需 Token) |
| CRUD | /api/admin/elements/map/:mapId, /api/admin/elements/:id | 地图元素管理(需 Token) |

## 数据库

SQLite 单文件(`server/data/fright-night.db`),表:`admins` / `chasers` / `escapees` / `maps` / `map_elements` / `patches` / `badges`。
角色 `skills`、公告 `summary` 字段以 JSON 数组存储,例如技能:`[{ "type": "主动|被动|处决", "name": "...", "desc": "..." }]`。

## 数据来源与免责

角色档案、技能、地图机制整理自 [百度百科「逃出惊魂夜」词条](https://baike.baidu.com/item/%E9%80%83%E5%87%BA%E6%83%8A%E9%AD%82%E5%A4%9C/65511213)、官方公告检索归档(`docs/archive/`)与网易官方公告(详见 `docs/data-sources.md`),仅供玩家查询参考,属于非官方粉丝项目;部分未核实字段(如爆破师-苏与画中女郎-贝琳达的上线日期)留空待管理面板补充。本站与网易《蛋仔派对》官方无关联。
