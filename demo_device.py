import asyncio
import json
import os
import random

import websockets

BASE = os.getenv('SERVER_WS', 'ws://127.0.0.1/ws/demo-device')

async def main():
    async with websockets.connect(BASE) as ws:
        battery = 78
        while True:
            battery = max(5, battery - random.choice([0, 0, 1]))
            await ws.send(json.dumps({
                'battery': battery,
                'model': 'Demo Android Device',
                'android_version': '15',
                'network': 'Wi-Fi',
                'app_version': '0.1.0'
            }))
            await asyncio.sleep(3)

if __name__ == '__main__':
    asyncio.run(main())
