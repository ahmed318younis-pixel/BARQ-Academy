# BARQ Academy DevOps Internship — Final Submission

## Overview

This repository contains the repaired and validated BARQ Academy DevOps assessment environment.

Final runtime:

- NGINX reverse proxy
- Three Flask application instances: `app-01`, `app-02`, `app-03`
- PostgreSQL
- Redis
- Docker Compose
- Frontend and internal backend networks
- Persistent PostgreSQL and Redis volumes

Final public endpoint:

`http://127.0.0.1:8090`

## Prerequisites

- Linux or WSL2
- Python 3.12+
- Git
- Docker
- Docker Compose

This is a disposable local lab. Do not expose it publicly and do not use real credentials or production data.

## Configuration

Create the local environment file:

`cp .env.example .env`

Set a local PostgreSQL password in `.env`.

The real `config/app.env` is local-only and must not be committed.

Validate the Compose configuration:

`docker compose config`

## Build and Start

`docker compose up --build -d`

Check the services:

`docker compose ps`

Expected services:

- `app-01`
- `app-02`
- `app-03`
- `nginx`
- `postgres`
- `redis`

Only NGINX publishes a host port:

`127.0.0.1:8090 -> nginx:80`

The application, PostgreSQL and Redis containers do not publish host ports.

## Application Tests

Run:

`curl http://127.0.0.1:8090/`

`curl http://127.0.0.1:8090/health`

`curl http://127.0.0.1:8090/ready`

`curl -i http://127.0.0.1:8090/instance`

`curl http://127.0.0.1:8090/records`

`curl http://127.0.0.1:8090/counter`

Complete environment validation:

`python3 validate.py`

The final validation checks the three application instances, service health, NGINX port 8090, prohibited host-port bindings and required endpoints.

## Failure and Recovery Test

Run:

`python3 failure_test.py`

The test verifies that PostgreSQL failure causes readiness to fail and that readiness returns successfully after PostgreSQL recovery.

Do not use `docker compose down` during the recorded runtime challenge.

## Backup and Restore

Create a PostgreSQL backup:

`./backup.sh`

Restore a backup:

`./restore.sh backups/<backup-file>.sql`

Backups are disposable lab artifacts and must not be committed.

## Persistence

PostgreSQL uses the named volume `postgres-data`.

Redis uses the named volume `redis-data`.

To recreate PostgreSQL without deleting its named volume:

`docker compose rm -sf postgres`

`docker compose up -d postgres`

Then verify:

`curl http://127.0.0.1:8090/records`

Do not use `docker compose down -v` during persistence testing because `-v` removes named volumes.

## Logs and Troubleshooting

Check services:

`docker compose ps`

View logs:

`docker compose logs --no-color`

Historical log analysis is documented in `docs/log_analysis.md`.

Troubleshooting is documented in `troubleshooting.md`.

## Automated Tests

Create the virtual environment:

`python3 -m venv .venv`

Activate it:

`source .venv/bin/activate`

Install dependencies:

`python -m pip install -r requirements.txt`

Run application tests:

`python -m unittest discover -s tests -v`

Run environment validation:

`python3 validate.py`

Run failure/recovery validation:

`python3 failure_test.py`

## Recorded Challenge

The supplied challenge script is:

`./video_challenge.sh`

The assessment challenge requires runtime fault diagnosis and recovery, the live public-port change from 8080 to 8090, addition of the third application instance and final validation.

Keep the challenge receipt under `.assessment/challenge.json` when available.

Do not delete or modify challenge state to retry the one-run challenge.

## Final Architecture

Client -> NGINX :8090 -> app-01/app-02/app-03 :8080

The application instances communicate with PostgreSQL :5432 and Redis :6379 through the internal backend network.

NGINX uses the frontend network and is not directly connected to the backend network.

See `docs/ARCHITECTURE.md` and `architecture.png`.

## Documentation

- `docs/log_analysis.md` — historical log investigation
- `troubleshooting.md` — troubleshooting record
- `decisions.md` — engineering decisions and trade-offs
- `docs/security_review.md` — security review
- `docs/ARCHITECTURE.md` — architecture documentation
- `docs/EVIDENCE_INDEX.md` — submission evidence mapping
- `AI_USAGE.md` — AI usage disclosure
- `assessment/TASK.md` — assessment requirements
- `assessment/APPLICATION.md` — application contract

## Stop and Cleanup

Stop the lab:

`docker compose down`

To intentionally remove persistent volumes:

`docker compose down -v`

Use `-v` only when deletion of PostgreSQL and Redis data is intentional.

Avoid global Docker cleanup commands such as `docker system prune`.

## Git Safety

Before committing:

`git status`

`git diff`

Never commit:

- `.env`
- `config/app.env`
- PostgreSQL backups
- dumps
- virtual environments
- credentials or tokens

## Evidence Screenshots

Selected screenshots are stored under `Photos/evidence/`. Sensitive screenshots
containing visible credentials were intentionally excluded.

### NGINX and Runtime Investigation

![NGINX upstream investigation](Photos/evidence/Screenshot%202026-09-25%20180752.png)

![NGINX upstream port investigation](Photos/evidence/Screenshot%202026-09-25%20181021.png)

### Application Validation

![Application records validation](Photos/evidence/Screenshot%202026-09-25%20195335.png)

![Redis counter validation](Photos/evidence/Screenshot%202026-09-25%20200130.png)

### Network and Persistence

![Network isolation validation](Photos/evidence/Screenshot%202026-09-25%20201423.png)

![PostgreSQL persistence validation](Photos/evidence/Screenshot%202026-09-25%20215059.png)

### Security Hardening

![Non-root application validation](Photos/evidence/Screenshot%202026-09-25%20233030.png)
