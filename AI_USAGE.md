# AI Usage Disclosure

AI assistance was used during the BARQ Academy DevOps assessment.

## Use 1 — Investigation and troubleshooting

- Tool/model: ChatGPT
- Purpose: Assist with understanding the supplied Docker Compose environment, Flask application contract, NGINX configuration, PostgreSQL/Redis configuration, and historical logs.
- Files or decisions affected: `docker-compose.yml`, `Dockerfile`, `nginx/nginx.conf`, application configuration, `docs/log_analysis.md`, and `troubleshooting.md`.
- What you changed or rejected: Configuration changes were reviewed and then applied manually after inspecting the repository and testing the environment. AI suggestions were not treated as evidence by themselves.
- How you independently verified it: Docker Compose commands, container health checks, application endpoints, logs, `docker inspect`, persistence tests, and failure/recovery tests were run locally.
- Related commits: `37168d8`, `0bb3d53`

## Use 2 — Validation and testing

- Tool/model: ChatGPT
- Purpose: Assist with designing and reviewing `validate.py` and `failure_test.py`.
- Files or decisions affected: `validate.py`, `failure_test.py`.
- What you changed or rejected: The validation logic was adapted to the final three-instance deployment and public port `8090`. The failure test was updated to use the final public port.
- How you independently verified it: `python3 validate.py` completed with 22 passed and 0 failed. `python3 failure_test.py` completed with a successful PostgreSQL failure/recovery test.
- Related commit: `2c4edf7`

## Use 3 — Documentation

- Tool/model: ChatGPT
- Purpose: Assist with structuring and reviewing the README and assessment documentation.
- Files or decisions affected: `README.md` and related documentation files.
- What you changed or rejected: Documentation content was reviewed against the actual repository state and observed test results. No fabricated test results, commits, timestamps, or video evidence were intentionally added.
- How you independently verified it: Repository status, Git diffs, Docker Compose status, application endpoint checks, validation output, and failure/recovery output were inspected locally.
- Related commits: Documentation changes are pending final commit.

## Verification principle

AI-generated suggestions were treated as assistance rather than as proof of correctness. Runtime behavior and assessment evidence were verified independently using the repository, Docker Compose, application endpoints, logs, Git history, and local test commands.
