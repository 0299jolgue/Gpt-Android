import secrets
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from .config import ADMIN_PASSWORD, ADMIN_USER, PUBLIC_URL
from .store import create_pairing_token, mark_offline, register_device, update_telemetry

router = APIRouter()

@router.get('/')
async def index():
    return FileResponse('templates/index.html')

@router.get('/static/{path:path}')
async def static_files(path: str):
    return FileResponse(f'static/{path}')

@router.post('/api/login')
async def login(payload: dict):
    ok = secrets.compare_digest(str(payload.get('username', '')), ADMIN_USER) and secrets.compare_digest(str(payload.get('password', '')), ADMIN_PASSWORD)
    return {'ok': True} if ok else {'ok': False}

@router.post('/api/pairing-token')
async def pairing_token():
    return {'token': create_pairing_token()}

@router.get('/api/devices')
async def devices():
    from .store import DEVICES
    return {'devices': list(DEVICES.values()), 'public_url': PUBLIC_URL}

@router.websocket('/ws/{device_id}')
async def websocket(ws: WebSocket, device_id: str):
    await ws.accept()
    register_device(device_id)
    try:
        while True:
            data = await ws.receive_json()
            update_telemetry(device_id, data)
    except WebSocketDisconnect:
        pass
    finally:
        mark_offline(device_id)
