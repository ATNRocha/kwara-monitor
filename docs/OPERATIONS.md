# Operations

## Install

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

Edit the private runtime configuration:

```bash
nano /opt/kwara-monitor/config/lots.json
```

Start services:

```bash
sudo systemctl start kwara-worker.service kwara-dashboard.service
```

## Status

```bash
systemctl status kwara-worker.service --no-pager
systemctl status kwara-dashboard.service --no-pager
curl -fsS http://127.0.0.1:8601/health
```

## Logs

```bash
journalctl -u kwara-worker.service -n 100 --no-pager
journalctl -u kwara-dashboard.service -n 100 --no-pager
```

## Boot validation

```bash
systemctl is-enabled kwara-worker.service kwara-dashboard.service
systemctl is-active kwara-worker.service kwara-dashboard.service
```

## Network validation

```bash
ss -ltnp | grep ':8601'
```

Expected bind: `127.0.0.1:8601`.
