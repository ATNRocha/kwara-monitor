# Changelog

## v0.4.3 — Smooth Live Update

- Replaced full-page/iframe-style refresh behavior with a lightweight Python `ThreadingHTTPServer`.
- Added `/api/state` JSON endpoint for background UI updates.
- Added `/health` endpoint.
- Kept countdown updates at 1 second and state refreshes at 5 seconds without recreating the page.
- Dashboard bound to `127.0.0.1:8601`.
- Added official ATN IT header identity.
- Production services validated after a controlled VM reboot.

## v0.4.2 — Final Polish

- Final visual refinement of the Digital/Cyber dashboard.
- Improved cards, priority display, table, lot detail and history presentation.

## v0.4.1 — Digital/Cyber UI Match

- UI alignment with the approved visual reference.

## v0.4 — Digital/Cyber Upgrade

- Major redesign of the monitoring interface.

## v0.3 — Upgrade

- Intermediate dashboard evolution and operational improvements.

## v0.2 — OCI ARM64

- Linux/ARM64 deployment baseline.
- Persistent Chromium worker.
- SQLite snapshots and worker status.
- systemd services and resource limits.
- Adaptive polling based on time to auction close.

## v0.1 — Local prototype

- Initial local monitor prototype.
