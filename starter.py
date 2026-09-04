from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title='Android Device Test Harness')
DEVICES = {}

HTML = '''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gpt-Android</title><style>body{font-family:system-ui;margin:0;background:#101114;color:#eee}main{max-width:1100px;margin:auto;padding:32px}.card{background:#191b20;border:1px solid #30333b;border-radius:14px;padding:20px;margin:12px 0}button{padding:10px 14px;border:0;border-radius:9px;cursor:pointer}input{padding:10px;border-radius:8px;border:1px solid #444;background:#111;color:#fff}</style></head><body><main><h1>Gpt-Android</h1><div class="card"><h2>Login</h2><input id="u" placeholder="Username"><input id="p" type="password" placeholder="Password"><button onclick="login()">Entrar</button><p id="msg"></p></div><div id="panel" hidden><div class="card"><h2>Geral</h2><p id="stats">Dispositivos: 0</p></div><div class="card"><h2>Dispositivos</h2><div id="devices"></div></div></div></main><script>function login(){if(u.value==='admin'&&p.value==='admin123'){document.querySelector('.card').hidden=true;panel.hidden=false;refresh()}else msg.textContent='Credenciais inválidas'}async function refresh(){let r=await fetch('/api/devices');let d=await r.json();stats.textContent='Dispositivos: '+d.length;devices.innerHTML=d.map(x=>'<div class="card"><b>'+x.id+'</b><br>Status: '+x.status+'<br>Bateria: '+(x.battery??'—')+'</div>').join('')||'<p>Nenhum dispositivo ligado.</p>'}setInterval(refresh,3000)</script></body></html>'''

@app.get('/')
async def index():
    return HTMLResponse(HTML)

@app.get('/api/devices')
async def devices():
    return list(DEVICES.values())

@app.websocket('/ws/{device_id}')
async def websocket(ws: WebSocket, device_id: str):
    await ws.accept()
    DEVICES[device_id] = {'id': device_id, 'status': 'online', 'battery': None}
    try:
        while True:
            data = await ws.receive_json()
            DEVICES[device_id].update(data)
            DEVICES[device_id]['status'] = 'online'
    except Exception:
        if device_id in DEVICES:
            DEVICES[device_id]['status'] = 'offline'

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
