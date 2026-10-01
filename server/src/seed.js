/**
 * 种子数据 —— 来源:
 *  1. 百度百科「逃出惊魂夜」词条(baike.baidu.com/item/逃出惊魂夜/65511213,2026-09-28 更新)
 *     33 名角色档案、技能、小传、10 种物品道具、4 张场景地图、34 枚徽章、1v4/2v8 规则
 *  2. 官方公告检索归档(docs/archive/,cutoff 2026-09-29):
 *     29 条版本平衡时间线(补齐角色上线日期)、全部角色定位、码头潜水等地图机制
 *  3. 2026-09-30 调研复核:官方公告直抓(爆破师/画中女郎上线日期、海瑟日期更正、
 *     2026-09-29「一蛋暴富」版本调整)与社区榜单(追捕者强度、逃生者定位补充),
 *     来源明细见 docs/data-sources.md
 *  4. 2026-10-01 复核:官网 09-30 版本公告全文(右系成长分支/右系超级成长全量文本入
 *     characters.json;惊魂寻宝队「苏织的心愿」/苍蓝龙拳/巫山之月补录 patches)与
 *     官方大神 09-28 帖(巅峰2v8新赛季 10-02 预告、「档案解封计划」10-05),
 *     社区抓取存档 docs/incoming/qweb-2026-10-01/,来源明细见 docs/data-sources.md
 * 数据文件位于 src/data/,可通过管理面板继续修订。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import bcrypt from 'bcryptjs';
import db, { run, get } from './db.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA = (p) => JSON.parse(fs.readFileSync(path.resolve(__dirname, 'data', p), 'utf-8'));
const characters = DATA('characters.json');
const patchesSrc = DATA('patches.json');
const badgesSrc = DATA('badges.json');
const archiveRoles = JSON.parse(
  fs.readFileSync(path.resolve(__dirname, '../../docs/archive/01_角色/角色结构化.json'), 'utf-8')
);

/** 角色上线日期:官方公告 + 归档平衡时间线 */
const RELEASE_DATES = {
  // 2024-07-19 玩法随 1v4 模式首发
  '哑女-斯黛拉': '2024-07-19', '疯象-莫比': '2024-07-19',
  '驯兽师-美狄亚': '2024-07-19', '舞女-莉莉丝': '2024-07-19', '士兵-托兰': '2024-07-19',
  '矿工-卢修斯': '2024-07-19', '医生-桑吉斯': '2024-07-19', '魔术师-克莱蕾': '2024-07-19',
  '水鬼-伊文': '2024-07-19',
  // 2024-08-22 2v8 合作模式与新角色
  '贵族-多萝西娅': '2024-08-22', '怨灵小丑-阿巴': '2024-08-22',
  // 官方公告
  '魔警-艾琳': '2024-09-27', '管家-劳埃德': '2024-09-27',
  // 爆破师-苏:官网 2024-11-06 公告「11月8日上线全新逃生者“爆破师”」
  '爆破师-苏': '2024-11-08',
  // 海瑟:原记 2025-04-28 无来源支撑;官方公告(17173 转载 2025-04-25)「4月30日…加入」更正为 04-30
  '丧心护士-海瑟': '2025-04-30', '血衣教师-礼温': '2025-07-18',
  '船长-歌萝佩': '2025-07-18', '影爪-梵蒂娅': '2025-10-31',
  // 归档平衡时间线
  '困兽-雷蒙德': '2024-12-06', '猎人-亨特': '2024-12-20',
  '冥蛇-佩姬': '2025-01-23', '报童-米隆': '2025-01-23',
  '科学家-伊万德': '2025-04-03', '黑拳-瓦格纳': '2025-06-27',
  '灵媒-曦': '2025-09-05', '主教-蓝慈': '2025-12-19',
  '转校生-桃乐丝': '2026-02-13', '学生会长-伊拉拉': '2026-02-13',
  '炼金师-赫拉': '2026-04-10', '行刑官-比努斯': '2026-06-18',
  '歌女-小阿娇': '2026-08-07', '少盟主-沈昭': '2026-08-14',
  // 画中女郎-贝琳达:TapTap 游戏账号「蛋仔」04-20 预告(帖内未显年份,由官方公众号 4-23 文章锁定),2026-04-24 上线(原记 2026-06-03 预告有误)
  '画中女郎-贝琳达': '2026-04-24'
};

/** 角色头像 emoji */
const EMOJI = {
  '驯兽师-美狄亚': '🦁', '舞女-莉莉丝': '💃', '士兵-托兰': '🪖', '矿工-卢修斯': '⛏️',
  '医生-桑吉斯': '🩺', '魔术师-克莱蕾': '🎩', '贵族-多萝西娅': '👒', '管家-劳埃德': '🤵',
  '猎人-亨特': '🏹', '爆破师-苏': '🧨', '报童-米隆': '📰', '科学家-伊万德': '🧪',
  '水鬼-伊文': '🌊', '黑拳-瓦格纳': '🥊', '船长-歌萝佩': '⚓', '灵媒-曦': '🔮',
  '主教-蓝慈': '⛪', '学生会长-伊拉拉': '🎀', '炼金师-赫拉': '⚗️', '行刑官-比努斯': '🪓',
  '歌女-小阿娇': '🎤',
  '哑女-斯黛拉': '🤫', '疯象-莫比': '🐘', '怨灵小丑-阿巴': '🤡', '魔警-艾琳': '🚨',
  '困兽-雷蒙德': '🐺', '冥蛇-佩姬': '🐍', '丧心护士-海瑟': '💉', '血衣教师-礼温': '📚',
  '影爪-梵蒂娅': '🐈‍⬛', '转校生-桃乐丝': '🎒', '画中女郎-贝琳达': '🖼️', '少盟主-沈昭': '⚔️'
};

/** 挖煤速度档次(官方分档,当前版本),写入逃生者 tips */
const DIG_TIER = {
  1: { rate: '1.15%/秒', members: ['矿工-卢修斯'] },
  2: { rate: '1%/秒', members: ['舞女-莉莉丝', '魔术师-克莱蕾', '贵族-多萝西娅', '科学家-伊万德', '炼金师-赫拉'] },
  3: { rate: '0.8%/秒', members: ['士兵-托兰', '医生-桑吉斯', '猎人-亨特', '爆破师-苏', '报童-米隆', '管家-劳埃德', '水鬼-伊文', '黑拳-瓦格纳', '主教-蓝慈'] },
  4: { rate: '0.5%/秒', members: ['驯兽师-美狄亚', '船长-歌萝佩', '灵媒-曦', '学生会长-伊拉拉', '行刑官-比努斯'] }
};

/** 追捕者强度评级(社区主观评价,非官方;随版本波动):
 *  T0 四人 = 2026-05 攻略榜(游侠 ali213 2026-05-11 与 7724 2026-05-10 两榜一致,ali213 已直抓核验);
 *  T0~T1 = 礼温/阿巴/影爪的社区口碑(2026 年无可回溯的完整榜单,档位存分歧,见 docs/data-sources.md 待核验注);
 *  哑女-斯黛拉原评「下位」因来源不可回溯已回退;哑女/贝琳达/桃乐丝/沈昭/雷蒙德一律留空待核验。 */
const STRENGTH = {
  '疯象-莫比': 'T0(2026-05)', '冥蛇-佩姬': 'T0(2026-05)',
  '丧心护士-海瑟': 'T0(2026-05)', '魔警-艾琳': 'T0(2026-05)',
  '血衣教师-礼温': 'T0~T1(社区口碑)', '怨灵小丑-阿巴': 'T0~T1(社区口碑)',
  '影爪-梵蒂娅': 'T0~T1(社区口碑)'
};

/** 逃生者社区/官方定位补充(2026-09-30 调研,官方或双源以上才收录),与现有定位合并、不覆盖:
 *  矿工「修机之王」(头条 2025-02 直抓)+ 925g「修机快」;
 *  炼金师=挖煤(sohu 2026-04-07 角色文「定位就是挖煤…堪称“挖煤天花板”」,已直抓核验;7724 2026-06 T0 榜列其第1但无「最强挖煤位」表述);
 *  爆破师 925g 排位攻略「修机快+短暂控场」(已直抓核验);
 *  报童 牵制/支援(社区「牵制位多面手」说法,原始引用不可回溯,待核验,见 docs/data-sources.md);
 *  灵媒 TapTap 游戏页技能帖(moment/710646038528004051,帖内含【定位】综合辅助;账号「蛋仔」未见官方标识,内容与百科一致);
 *  主教 TapTap 攻略(moment/770954813469888035「蓝慈定位是高难度辅助」)。 */
const ROLE_EXTRA = {
  '矿工-卢修斯': '修机位',
  '炼金师-赫拉': '修机位',
  '爆破师-苏': '修机位',
  '报童-米隆': '牵制/支援',
  '灵媒-曦': '综合辅助',
  '主教-蓝慈': '高难度辅助'
};

/** 角色定位:归档《角色结构化.json》提供全量定位;百科【定位】优先(官方角色档案) */
function buildRoleMap() {
  const roles = {};
  for (const group of ['survivors', 'pursuers']) {
    for (const c of archiveRoles[group]) {
      const key = c.code ? `${c.name}-${c.code}` : c.name;
      roles[key] = c.role || '';
    }
  }
  // 归档中这两名追捕者未记录正式名(code 为 null),按已知正式名补映射
  roles['影爪-梵蒂娅'] = roles['影爪-梵蒂娅'] || roles['影爪'] || '';
  roles['丧心护士-海瑟'] = roles['丧心护士-海瑟'] || roles['丧心护士'] || '';
  return roles;
}

const maps = [
  {
    name: '惊魂马戏团', emoji: '🎪', theme: '马戏·迷雾剧场', release_date: '2024-07-19', size: '中型',
    description: '「逃出惊魂夜」随 1v4 模式同日上线的首张地图。以手办世界「绝命镇」的马戏团为舞台,庭院、旋转木马、瞭望高点与地下室构成第一座审判场。',
    elements: [
      { name: '蒸汽炉', type: '机制', icon: '🔥', description: '复古机器分散在各处,逃生者挖煤填充燃料,1v4 模式激活 5 座开启逃生门。填充时会出现校准气压,踩点成功触发「普通/完美的一铲」;多人填充有速度加成。' },
      { name: '爆米花大炮', type: '机制', icon: '💣', description: '逃生者被放入后有 60 秒挣扎时间,分两阶段:第一阶段被救下后下次从第二阶段开始,第二阶段被救下则下次直接淘汰。淘汰过人的大炮无法再使用。' },
      { name: '柜子', type: '交互', icon: '🚪', description: '散落在地图中,逃生者可躲入;被追捕者发现可直接被扛起送去大炮。躲太久追捕者会收到提示。' },
      { name: '墙体及拉板', type: '地形', icon: '🧱', description: '墙体双方都可翻越,拉板仅逃生者可翻越,追捕者需破板;追捕者处于拉板范围内时拉板可将其短暂眩晕。' },
      { name: '逃生门', type: '点位', icon: '🚪', description: '蒸汽炉达标后开启,跟随地图图标前往即可逃出生天。' },
      { name: '地窖', type: '点位', icon: '🕳️', description: '当 3 座蒸汽炉未激活时随机刷新点位;全场仅剩最后一人时无论炉况都会开启。' },
      { name: '地下室', type: '点位', icon: '🏚️', description: '马戏团地下区域,残局阶段的重要逃生通道,通常在特定蒸汽炉进度后开放。' },
      { name: '庭院与旋转木马', type: '地形', icon: '🎠', description: '核心区域外的开阔绕行空间,瞭望高点提供视野博弈位。' }
    ]
  },
  {
    name: '惊魂火车站', emoji: '🚂', theme: '车站·铁轨突围', release_date: '2025-01-24', size: '大型',
    description: '2025 年 1 月与冥蛇-佩姬、报童-米隆同期上线。多区域车站与车厢建筑,适合高机动与视野博弈,是唯一拥有双撤离方式的地图。',
    elements: [
      { name: '蒸汽炉', type: '机制', icon: '🔥', description: '包含场地中央信号房旁的黄色蒸汽炉——它是发动火车的关键条件之一。' },
      { name: '火车', type: '机制', icon: '🚂', description: '本图专属撤离方式:①激活黄色蒸汽炉;②信号房拉杆切到向上(蓝灯变黄);③全部蒸汽炉激活。由一名逃生者向火车头填充燃料后火车开动撞墙,开启隐藏出口。拉杆方向错误火车会撞山逼停。拉杆双方均可切换!' },
      { name: '广告牌', type: '地形', icon: '🪧', description: '本图专属。立起的广告牌可折断,落点随折断者位置变化;落在低矮障碍上时逃生者可「滑铲」穿过,落成斜面时双方可通行且无法击碎;已落下的广告牌追捕者可普攻击碎。' },
      { name: '车厢与站台', type: '地形', icon: '🚉', description: '多区域结构,车厢内空间修正与技能碰撞经过多轮版本修复,适合绕后拉扯。' },
      { name: '爆米花大炮', type: '机制', icon: '💣', description: '淘汰逃生者的处刑装置,两阶段挣扎与救援规则同基础机制。' },
      { name: '逃生门 / 地窖', type: '点位', icon: '🚪', description: '常规撤离点:炉门达标开门,残局走地窖。' }
    ]
  },
  {
    name: '惊魂码头', emoji: '🚢', theme: '港口·迷雾货仓', release_date: '2025-07-18', size: '大型',
    description: '随「血衣教师-礼温」与逃生者「船长-歌萝佩」同期上线的地图。水域玩法突出:逃生者可潜水躲藏,但水中移动速度明显受限;水鬼、船长等角色在此如鱼得水。',
    elements: [
      { name: '蒸汽炉', type: '机制', icon: '🔥', description: '散布于码头与货仓,激活 5 座(1v4)开启逃生门。' },
      { name: '水下区域', type: '机制', icon: '🤿', description: '本图特色。逃生者可进入水下隐藏行踪,水中移动速度受到明显限制;是船长与水鬼等角色的特色博弈区域。' },
      { name: '水闸', type: '机制', icon: '🌊', description: '本图专属机关。激活水闸旁的蒸汽炉即可开启水闸,放出数个木箱——红色的为炸药箱,追捕者命中炸药箱会被爆炸眩晕一段时间。' },
      { name: '爆米花大炮', type: '机制', icon: '💣', description: '淘汰逃生者的处刑装置。' },
      { name: '柜子 / 墙体及拉板', type: '地形', icon: '🧱', description: '躲藏与翻越博弈的基础交互。' },
      { name: '逃生门 / 地窖', type: '点位', icon: '🚪', description: '常规撤离点:炉门达标开门,残局走地窖。' }
    ]
  },
  {
    name: '惊魂不夜楼', emoji: '🌃', theme: '江南·夜色楼阁', release_date: '2026-08-14', size: '大型',
    description: '随「少盟主-沈昭」同期上线的最新地图,官方描述为江南夜色楼阁主题:多层空间、舞台帘幕、水域与大量柜子,独有的暗门传送打通内外。',
    elements: [
      { name: '蒸汽炉', type: '机制', icon: '🔥', description: '分布于一楼与主街等地,激活 5 座(1v4)开启逃生门。' },
      { name: '暗门', type: '机制', icon: '🌫️', description: '本图专属。激活不夜楼一楼的蒸汽炉即可激活暗门,靠近点击图标,稍候即可从不夜楼内部传送到主街。' },
      { name: '舞台与帘幕', type: '地形', icon: '🎭', description: '一、二层多层结构与舞台幕布交互,经过多轮碰撞与灯光修复,绕后路线极多。' },
      { name: '水域', type: '地形', icon: '💧', description: '楼内含水鬼通道与水域,与暗门位置联动,注意靠近暗门处的水鬼通道异常曾在版本中修复。' },
      { name: '爆米花大炮', type: '机制', icon: '💣', description: '淘汰逃生者的处刑装置。' },
      { name: '逃生门 / 地窖', type: '点位', icon: '🚪', description: '常规撤离点:炉门达标开门,残局走地窖。' }
    ]
  }
];

function seed() {
  run('DELETE FROM map_elements');
  run('DELETE FROM maps');
  run('DELETE FROM chasers');
  run('DELETE FROM escapees');
  run('DELETE FROM patches');
  run('DELETE FROM badges');
  run('DELETE FROM admins');
  run('INSERT INTO admins (username, password_hash) VALUES (?, ?)', 'admin', bcrypt.hashSync('admin123', 10));

  const roleMap = buildRoleMap();
  const tierOf = (name) => Object.entries(DIG_TIER).find(([, t]) => t.members.includes(name));

  const insChaser = 'INSERT INTO chasers (name,title,emoji,difficulty,strength,release_date,story,skills,tips,role_type,status) VALUES (?,?,?,?,?,?,?,?,?,?,?)';
  for (const c of characters.chasers) {
    const [prof] = c.name.split('-');
    // 贝琳达:归档标注 announcement_only,以百科角色档案为准保留技能,定位用百科值
    const role = c.role || roleMap[c.name] || '';
    run(insChaser, c.name, prof, EMOJI[c.name] || '👻', 3, STRENGTH[c.name] || '', RELEASE_DATES[c.name] || '',
      c.story, JSON.stringify(c.skills), '', role, c.name === '画中女郎-贝琳达' ? 'live' : 'live');
  }

  const insEscapee = 'INSERT INTO escapees (name,title,emoji,role_type,difficulty,release_date,story,skills,tips,status) VALUES (?,?,?,?,?,?,?,?,?,?)';
  for (const c of characters.escapees) {
    const [prof] = c.name.split('-');
    const tier = tierOf(c.name);
    const tips = tier ? `挖煤速度档次${tier[0]}(${tier[1].rate});2025-11 全局挖煤重构分档` : '';
    // 定位合并:百科/归档定位在前,社区补充(ROLE_EXTRA)在后;新标签若为旧标签的
    // 更完整表述则替换(如 灵媒「辅助」→「综合辅助」),不清空已有定位
    const parts = (c.role || roleMap[c.name] || '').split('/').map((s) => s.trim()).filter(Boolean);
    for (const p of (ROLE_EXTRA[c.name] || '').split('/')) {
      if (!p) continue;
      const i = parts.findIndex((e) => e !== p && p.includes(e));
      if (i >= 0) parts[i] = p;
      else if (!parts.includes(p)) parts.push(p);
    }
    run(insEscapee, c.name, prof, EMOJI[c.name] || '🥚', parts.join('/'), 3, RELEASE_DATES[c.name] || '',
      c.story, JSON.stringify(c.skills), tips, 'live');
  }

  const insMap = 'INSERT INTO maps (name,emoji,theme,release_date,size,description,status) VALUES (?,?,?,?,?,?,?)';
  const insEle = 'INSERT INTO map_elements (map_id,name,type,icon,description,sort_order) VALUES (?,?,?,?,?,?)';
  for (const m of maps) {
    const res = run(insMap, m.name, m.emoji, m.theme, m.release_date, m.size, m.description, 'live');
    m.elements.forEach((el, i) => run(insEle, Number(res.lastInsertRowid), el.name, el.type, el.icon, el.description, i));
  }

  const insPatch = 'INSERT INTO patches (date,title,summary) VALUES (?,?,?)';
  for (const p of patchesSrc) {
    run(insPatch, p.date || '2025-02-01', p.title, JSON.stringify(p.summary || []));
  }

  const insBadge = 'INSERT INTO badges (name,faction,category,grade,description) VALUES (?,?,?,?,?)';
  for (const b of badgesSrc) {
    run(insBadge, b.name, b.faction, b.category, b.grade, b.description);
  }

  const counts = {
    chasers: get('SELECT COUNT(*) AS n FROM chasers').n,
    escapees: get('SELECT COUNT(*) AS n FROM escapees').n,
    maps: get('SELECT COUNT(*) AS n FROM maps').n,
    elements: get('SELECT COUNT(*) AS n FROM map_elements').n,
    patches: get('SELECT COUNT(*) AS n FROM patches').n,
    badges: get('SELECT COUNT(*) AS n FROM badges').n,
    dated_chars: get("SELECT COUNT(*) AS n FROM (SELECT 1 FROM chasers WHERE release_date != '' UNION ALL SELECT 1 FROM escapees WHERE release_date != '')").n
  };
  console.log('✅ 种子数据写入完成:', counts);
  console.log('👤 默认管理员: admin / admin123');
}

seed();
