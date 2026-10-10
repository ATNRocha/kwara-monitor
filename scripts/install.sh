#!/usr/bin/env bash
set -euo pipefail

APP="${APP:-/opt/kwara-monitor}"
SRC="$(cd "$(dirname "$0")/.." && pwd)"

sudo mkdir -p "$APP"
sudo chown -R "${USER}:${USER}" "$APP"

# Preserve runtime data and the private lot configuration.
rsync -a --delete \
  --exclude '.git' \
  --exclude '.venv' \
  --exclude 'data/kwara.db*' \
  --exclude 'config/lots.json' \
  "$SRC/" "$APP/"

cd "$APP"
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip rsync curl ca-certificates sqlite3

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip wheel
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
sudo .venv/bin/python -m playwright install-deps chromium || true

if [[ ! -f config/lots.json ]]; then
  cp config/lots.example.json config/lots.json
  echo "Created $APP/config/lots.json from the example. Edit it before starting the worker."
fi

.venv/bin/python -c "from app.db import init_db; init_db(); print('DB OK')"

sudo cp systemd/kwara-worker.service /etc/systemd/system/
sudo cp systemd/kwara-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kwara-worker.service kwara-dashboard.service

echo "Installed in $APP"
echo "Next: edit config/lots.json, then start the services."
