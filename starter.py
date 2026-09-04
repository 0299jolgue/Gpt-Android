import os
import secrets
from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

APP_USER = os.getenv('ADMIN_USER', 'admin')
APP_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
PUBLIC_URL = os.getenv('PUBLIC_URL', '')

app = FastAPI(title='Gpt-Android Test Harness')
DEVICES = {}
TOKENS = {}

HTML = r'''<!doctype html><html lang="pt"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gpt-Android</title><style>
*{box-sizing:border-box}body{margin:0;background:#0b0d11;color:#eef1f6;font-family:Inter,system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:28px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#151821;border:1px solid #282d38;border-radius:16px;padding:20px;margin:12px 0;box-shadow:0 10px 30px #0003}h1{margin:0 0 5px}h2{margin-top:0}.muted{color:#9299a8}.stat{font-size:30px;font-weight:800}input,button{font:inherit;border-radius:10px;padding:11px 13px;border:1px solid #343a46}input{background:#0f1218;color:white;margin-right:8px}button{background:#e9edf5;color:#101217;cursor:pointer}.danger{background:#52222a;color:#fff}.device{padding:14px;border:1px solid #2c313d;border-radius:12px;margin-top:10px}.online{color:#68e28c}.offline{color:#ff8c93}.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.pill{display:inline-block;padding:4px 8px;border-radius:999px;background:#222834;font-size:12px}.notice{padding:11px;border-left:3px solid #8794ff;background:#131720;border-radius:8px}
@media(max-width:800px){.grid{grid-template-columns:1fr}}
</style></head><body><main>
<div class="card"><h1>Gpt-Android</h1><div class="muted">Android Device Test Harness · controlo exclusivamente por dispositivos emparelhados</div></div>
<div id="login" class="card"><h2>Entrar</h2><input id="u" placeholder="Utilizador" autocomplete="username"><input id="p" type="password" placeholder="Password" autocomplete="current-password"><button onclick="login()">Entrar</button><span id="msg" class="muted"></span></div>
<div id="app" hidden><div class="grid"><div class="card"><div class="muted">Total</div><div id="total" class="stat">0</div></div><div class="card"><div class="muted">Online</div><div id="online" class="stat">0</div></div><div class="card"><div class="muted">URL pública</div><div id="public" class="pill">Não configurada</div></div></div>
<div class="card"><h2>Emparelhamento</h2><div class="row"><button onclick="token()">Gerar token</button><code id="tok" class="pill">—</code></div><p class="muted">O cliente Android deve apresentar o estado de emparelhamento ao utilizador e enviar apenas telemetria autorizada.</p></div>
<div class="card"><h2>Dispositivos</h2><div id="devices"><p class="muted">Nenhum dispositivo ligado.</p></div></div>
<div class="card"><h2>Testes</h2><div class="notice">Ações invasivas como espionagem de mensagens/notificações, bloqueio remoto, controlo oculto ou extração de dados não fazem parte deste harness.</div></div></div>
<script>
const $=id=>document.getElementById(id);
async function login(){let r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:$('u').value,password:$('p').value})});if(r.ok){$('login').hidden=true;$('app').hidden=false;refresh();}else $('msg').textContent='Credenciais inválidas';}
async function token(){let r=await fetch('/api/pairing-token',{method:'POST'});let d=await r.json();$('tok').textContent=d.token;}
async function refresh(){let r=await fetch('/api/devices');let d=await r.json();$('total').textContent=d.length;$('online').textContent=d.filter(x=>x.status==='online').length;$('public').textContent=d.public_url||'Não configurada';let items=d.devices||[];$('devices').innerHTML=items.length?items.map(x=>`<div class="device"><b>${x.id}</b> <span class="pill ${x.status==='online'?'online':'offline'}">${x.status}</span><br><span class="muted">${x.model||'modelo desconhecido'} · Android ${x.android_version||'—'} · Bateria ${x.battery??'—'}%</span></div>`).join(''):'<p class="muted">Nenhum dispositivo ligado.</p>';}
setInterval(()=>{if(!$('app').hidden)refresh()},3000);
</script></main></body></html>'''

@app.get('/')
async def index():
    return HTMLResponse(HTML)

@app.post('/api/login')
async def login(payload: dict):
    ok = secrets.compare_digest(str(payload.get('username','')), APP_USER) and secrets.compare_digest(str(payload.get('password','')), APP_PASSWORD)
    return {'ok': ok} if ok else HTMLResponse('Unauthorized', status_code=401)

@app.post('/api/pairing-token')
async def pairing_token():
    token = secrets.token_urlsafe(12)
    TOKENS[token] = datetime.now(timezone.utc).isoformat()
    return {'token': token}

@app.get('/api/devices')
async def devices():
    items = list(DEVICES.values())
    return {'devices': items, 'public_url': PUBLIC_URL}

@app.websocket('/ws/{device_id}')
async def websocket(ws: WebSocket, device_id: str):
    await ws.accept()
    DEVICES[device_id] = {'id': device_id, 'status': 'online', 'battery': None, 'model': None, 'android_version': None, 'last_seen': datetime.now(timezone.utc).isoformat()}
    try:
        while True:
            data = await ws.receive_json()
            allowed = {'battery','model','android_version','network','app_version'}
            DEVICES[device_id].update({k:v for k,v in data.items() if k in allowed})
            DEVICES[device_id]['status'] = 'online'
            DEVICES[device_id]['last_seen'] = datetime.now(timezone.utc).isoformat()
    except WebSocketDisconnect:
        pass
    finally:
        if device_id in DEVICES:
            DEVICES[device_id]['status'] = 'offline'

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
