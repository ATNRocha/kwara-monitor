#!/usr/bin/env bash
set -euo pipefail

echo "=== services ==="
systemctl is-active kwara-worker.service || true
systemctl is-active kwara-dashboard.service || true

echo
echo "=== dashboard ==="
curl -fsS http://127.0.0.1:8601/health
printf '\n'

echo
echo "=== bind ==="
ss -ltnp | grep ':8601' || true
