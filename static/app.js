const $ = (id) => document.getElementById(id);

async function login() {
    const response = await fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: $('username').value,
            password: $('password').value,
        }),
    });

    const data = await response.json();
    if (data.ok) {
        window.location.href = '/dashboard';
        return;
    }

    $('login-error').hidden = false;
}

async function createToken() {
    const response = await fetch('/api/pairing-token', {method: 'POST'});
    if (!response.ok) return;
    const data = await response.json();
    $('pairing-token').textContent = data.token;
}

async function refreshDashboard() {
    const response = await fetch('/api/devices');
    if (!response.ok) return;

    const data = await response.json();
    const devices = data.devices || [];
    const online = devices.filter((device) => device.status === 'online').length;

    if ($('total')) $('total').textContent = devices.length;
    if ($('online')) $('online').textContent = online;
    if ($('offline')) $('offline').textContent = devices.length - online;
    if ($('public-url')) $('public-url').textContent = `URL pública: ${data.public_url || 'não configurada'}`;

    if (!$('device-list')) return;
    $('device-list').innerHTML = devices.length
        ? devices.map(deviceCard).join('')
        : '<p class="muted">Nenhum dispositivo ligado.</p>';
}

function deviceCard(device) {
    const state = device.status === 'online' ? 'online' : 'offline';
    return `
        <article class="device-card">
            <div class="device-title">
                <strong>${escapeHtml(device.id)}</strong>
                <span class="pill ${state}">${state}</span>
            </div>
            <div class="muted">
                ${escapeHtml(device.model || 'Modelo desconhecido')} ·
                Android ${escapeHtml(device.android_version || '—')} ·
                Bateria ${escapeHtml(device.battery ?? '—')}%
            </div>
            <small class="muted">Último contacto: ${escapeHtml(device.last_seen || '—')}</small>
        </article>`;
}

function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, (character) => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    })[character]);
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = $('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            login().catch(() => {
                $('login-error').hidden = false;
            });
        });
    }

    const tokenButton = $('generate-token');
    if (tokenButton) tokenButton.addEventListener('click', () => createToken().catch(() => {}));

    if ($('device-list')) {
        refreshDashboard().catch(() => {});
        setInterval(() => refreshDashboard().catch(() => {}), 3000);
    }
});
