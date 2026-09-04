# Gpt-Android

Android Device Test Harness para testes autorizados e dispositivos emparelhados explicitamente.

## Estrutura

```text
Gpt-Android/
├── starter.py                 # ponto de entrada: python starter.py
├── requirements.txt           # dependências Python
├── app/
│   ├── __init__.py
│   ├── config.py              # configuração e variáveis de ambiente
│   ├── routes.py              # rotas HTTP/WebSocket
│   └── store.py                # estado dos dispositivos e tokens
├── templates/
│   └── index.html             # HTML da interface
└── static/
    ├── style.css              # estilos
    └── app.js                 # lógica do frontend
```

## Arranque

```bash
pip install -r requirements.txt
python starter.py
```

O servidor usa `0.0.0.0:80`. A configuração pode ser alterada por variáveis de ambiente:

- `ADMIN_USER` — utilizador de demonstração (`admin` por defeito)
- `ADMIN_PASSWORD` — password de demonstração (`admin123` por defeito)
- `PUBLIC_URL` — URL pública mostrada no dashboard
- `HOST` — host de escuta (`0.0.0.0` por defeito)
- `PORT` — porta (`80` por defeito)

## Funcionalidades atuais

- Dashboard separado do backend.
- Login de demonstração.
- Geração de tokens de emparelhamento.
- Registo de dispositivos via WebSocket.
- Telemetria autorizada: bateria, modelo, versão Android, rede e versão da app.
- Estado online/offline e última ligação.

O projeto permanece limitado a um harness visível de testes. Não implementa persistência furtiva, interceção de mensagens, recolha de notificações, roubo de credenciais, vigilância oculta, controlo remoto arbitrário ou bloqueio/desbloqueio remoto.
