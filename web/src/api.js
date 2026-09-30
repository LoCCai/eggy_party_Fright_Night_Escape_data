async function request(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) {
    let msg = `请求失败 (${res.status})`;
    try { msg = (await res.json()).message || msg; } catch { /* ignore */ }
    throw new Error(msg);
  }
  return res.json();
}

export const api = {
  chasers: (params = '') => request(`/api/chasers${params}`),
  chaser: (id) => request(`/api/chasers/${id}`),
  escapees: (params = '') => request(`/api/escapees${params}`),
  escapee: (id) => request(`/api/escapees/${id}`),
  maps: () => request('/api/maps'),
  map: (id) => request(`/api/maps/${id}`),
  patches: () => request('/api/patches'),
  badges: (params = '') => request(`/api/badges${params}`),
  stats: () => request('/api/stats')
};

/** 地图元素显隐偏好(localStorage 持久化) */
const HIDDEN_KEY = 'fne:visibility';
function readStore() {
  try { return JSON.parse(localStorage.getItem(HIDDEN_KEY)) || {}; } catch { return {}; }
}
export const visibility = {
  getHidden(mapId) {
    return new Set(readStore()[mapId] || []);
  },
  toggle(mapId, elementId) {
    const store = readStore();
    const set = new Set(store[mapId] || []);
    set.has(elementId) ? set.delete(elementId) : set.add(elementId);
    store[mapId] = [...set];
    localStorage.setItem(HIDDEN_KEY, JSON.stringify(store));
    return set;
  },
  setHidden(mapId, ids) {
    const store = readStore();
    store[mapId] = ids;
    localStorage.setItem(HIDDEN_KEY, JSON.stringify(store));
  },
  reset(mapId) {
    this.setHidden(mapId, []);
  }
};
