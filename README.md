# Gpt-Android

Visible Android Device Test Harness for authorized testing.

## Run

```bash
pip install -r requirements.txt
python starter.py
```

The server listens on port 80. The demo login is `admin` / `admin123`; change these before production use.

## Scope

This project is intentionally designed as a visible test harness. Devices pair explicitly and publish non-sensitive telemetry such as model, Android version and battery state.

It does not implement hidden persistence, message interception, notification scraping, credential theft, covert surveillance, arbitrary remote control, or lock/unlock control.

Set `PUBLIC_URL` in the hosting environment to display the externally reachable URL in the dashboard.
