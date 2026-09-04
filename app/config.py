import os

ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
PUBLIC_URL = os.getenv('PUBLIC_URL', '')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '80'))
