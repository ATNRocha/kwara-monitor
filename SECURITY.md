# Security

## Deployment model

The production design keeps the dashboard bound to `127.0.0.1:8601`. Remote access is expected to pass through a reverse tunnel / Zero Trust access layer instead of exposing port 8601 directly to the Internet.

## Never commit

- Cloudflare tunnel tokens or credentials
- SSH private keys
- `.env` files or API secrets
- production SQLite databases
- `config/lots.json` when it contains private bidding ceilings or other strategy data
- infrastructure credentials or private certificates

The repository therefore ignores the runtime database and `config/lots.json` and ships only `config/lots.example.json`.

## Reporting

This is a personal project. Security issues should be reported privately to the repository owner rather than disclosed publicly before a fix is available.
