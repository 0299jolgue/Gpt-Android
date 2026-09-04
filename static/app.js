const $ = (id) => document.getElementById(id);

async function login() {
  const response = await fetch('/api/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username: $('u').value, password: $('p').value})
  });
  if (!response.ok) { $('msg').textContent = 'Erro de ligação'; return; }
  const data = await response.json();
  if (data.ok) { $('login').hidden = true; $('app').hidden = false; refresh(); }
  else $('msg').textContent = 'Credenciais inválidas';
}

async function createToken() {
  const response = await fetch('/api/pairing-token', {method: 'POST'});
  const data = await response.json();
  $('tok').textContent = data.token;
}

async function refresh() {
  const response = await fetch('/api/devices');
  const data = await response.json();
  const devices = data.devices || [];
  $('total').textContent = devices.length;
  $('online').textContent = devices.filter(d => d.status === 'online').length;
  $('public').textContent = data.public_url || 'Não configurada';
  $('devices').innerHTML = devices.length ? devices.map(deviceCard).join('') : '<p class="muted">Nenhum dispositivo ligado.</p>';
}

function deviceCard(d) {
  const state = d.status === 'online' ? 'online' : 'offline';
  return `<div class="device"><b>${escapeHtml(d.id)}</b> <span class="pill ${state}">${state}</span><br><span class="muted">${escapeHtml(d.model || 'modelo desconhecido')} · Android ${escapeHtml(d.android_version || '—')} · Bateria ${d.battery ?? '—'}%</span></div>`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

setInterval(() => { if (!$('app').hidden) refresh().catch(() => {}); }, 3000);
