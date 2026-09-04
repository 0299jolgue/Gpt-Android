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

@app.get('/')
async def index():
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        return HTMLResponse(f.read())

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
    return {'devices': list(DEVICES.values()), 'public_url': PUBLIC_URL}

@app.websocket('/ws/{device_id}')
async def websocket(ws: WebSocket, device_id: str):
    await ws.accept()
    DEVICES[device_id] = {
        'id': device_id,
        'status': 'online',
        'battery': None,
        'model': None,
        'android_version': None,
        'last_seen': datetime.now(timezone.utc).isoformat(),
    }
    try:
        while True:
            data = await ws.receive_json()
            allowed = {'battery', 'model', 'android_version', 'network', 'app_version'}
            DEVICES[device_id].update({k: v for k, v in data.items() if k in allowed})
            DEVICES[device_id]['status'] = 'online'
            DEVICES[device_id]['last_seen'] = datetime.now(timezone.utc).isoformat()
    except WebSocketDisconnect:
        pass
    finally:
        if device_id in DEVICES:
            DEVICES[device_id]['status'] = 'offline'

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
