# Log Analysis

## Scope

The supplied logs were analyzed without modifying the original files.

Files analyzed:

- `logs/access.log` — 726 lines
- `logs/application.log` — 730 lines
- `logs/error.log` — 68 lines

## Access Log Summary

The access log contains JSON Lines records.

HTTP status distribution:

| Status | Count |
|---|---:|
| 200 | 620 |
| 404 | 10 |
| 502 | 40 |
| 503 | 47 |
| 504 | 8 |

There was 1 malformed/truncated JSON line in `access.log`, at line 311.

Valid JSON records: 725
Invalid records: 1

Total 5xx responses: 95.

All observed 5xx responses occurred during the 11:00 hour in the supplied dataset.

## Timeline and Correlation

### 11:05–11:09 — NGINX upstream connection failures

NGINX reported repeated:

`connect() failed (111: Connection refused) while connecting to upstream`

The affected upstream was `172.23.0.12:8080`.

Requests included `/health`, `/ready`, `/records`, `/counter`, `/instance`, and `/`.

This indicates that NGINX could resolve/reach the upstream address but the upstream application was not accepting connections at that time.

### 11:12–11:15 — Redis dependency timeouts

The application logs show repeated Redis `TimeoutError` events affecting both `app-01` and `app-02`.

This affected dependency operations across both application instances.

### 11:20–11:21 — PostgreSQL authentication failures

The application logs show repeated PostgreSQL `InvalidPassword` errors affecting both `app-01` and `app-02`.

This indicates an application/database credential mismatch during the incident.

## Root Cause / Findings

The investigation identified configuration and environment issues affecting application startup, upstream connectivity, dependency connectivity, and persistence.

The main corrected issues included:

- Application binding to the container network interface instead of loopback.
- Incorrect NGINX upstream port.
- Incorrect PostgreSQL and Redis ports.
- PostgreSQL credential mismatch.
- Incorrect PostgreSQL persistence configuration.
- Redis persistence disabled.
- Incorrect NGINX network access.
- Missing dependency health ordering.
- Incorrect application healthcheck endpoint.
- Duplicate application instance identity.
- Missing application resource limits.
- Application container initially running as root.
- Application environment file copied into the image.

## Retest

After the configuration fixes:

- All required containers were running.
- `app-01`, `app-02`, PostgreSQL and Redis were healthy.
- During the initial investigation state, NGINX published host port `8080`; the final challenge state changed the public port to `8090`.
- Application endpoints `/`, `/health`, `/ready`, `/instance`, `/records`, and `/counter` returned HTTP 200.
- PostgreSQL and Redis were reachable through the application.
- PostgreSQL data survived container recreation.
- Redis state survived container recreation.
- NGINX could no longer resolve PostgreSQL or Redis after network isolation.

## Limitations

The access log contains one malformed/truncated record. Therefore status counts are based on the 725 valid JSON records.

The available logs establish temporal correlation between HTTP failures and dependency/upstream errors. They do not by themselves prove a one-to-one causal mapping between every individual 5xx response and a specific dependency error.
