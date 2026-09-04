from datetime import datetime, timezone
import secrets

DEVICES: dict[str, dict] = {}
TOKENS: dict[str, str] = {}

ALLOWED_TELEMETRY = {'battery', 'model', 'android_version', 'network', 'app_version'}


def create_pairing_token() -> str:
    token = secrets.token_urlsafe(12)
    TOKENS[token] = datetime.now(timezone.utc).isoformat()
    return token


def register_device(device_id: str) -> dict:
    device = DEVICES.setdefault(device_id, {
        'id': device_id,
        'status': 'offline',
        'battery': None,
        'model': None,
        'android_version': None,
        'network': None,
        'app_version': None,
        'last_seen': None,
    })
    device['status'] = 'online'
    device['last_seen'] = datetime.now(timezone.utc).isoformat()
    return device


def update_telemetry(device_id: str, data: dict) -> dict:
    device = register_device(device_id)
    device.update({k: v for k, v in data.items() if k in ALLOWED_TELEMETRY})
    device['last_seen'] = datetime.now(timezone.utc).isoformat()
    return device


def mark_offline(device_id: str) -> None:
    if device_id in DEVICES:
        DEVICES[device_id]['status'] = 'offline'
