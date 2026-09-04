import secrets
from pathlib import Path

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from .config import ADMIN_PASSWORD, ADMIN_USER, PUBLIC_URL
from .store import create_pairing_token, mark_offline, register_device, update_telemetry

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

@router.get('/')
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get('/dashboard')
async def dashboard_page(request: Request):
    return templates.TemplateResponse('dashboard.html', {'request': request})

@router.post('/api/login')
async def login(payload: dict):
    ok = (
        secrets.compare_digest(str(payload.get('username', '')), ADMIN_USER)
        and secrets.compare_digest(str(payload.get('password', '')), ADMIN_PASSWORD)
    )
    return {'ok': ok}

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

@router.get('/static/{path:path}')
async def static_files(path: str):
    return FileResponse(BASE_DIR / 'static' / path)
