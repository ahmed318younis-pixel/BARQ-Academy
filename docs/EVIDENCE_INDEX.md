# Evidence and Submission Index

## Submission metadata

- Repository URL: https://github.com/ahmed318younis-pixel/BARQ-Academy
- Final commit: Pending final documentation commit and push.
- Matching CI run: Pending CI run for the final commit.
- Continuous 12-18 minute video URL: Not recorded in this repository.
- Challenge receipt ID: Not verified in this repository.
- Starting video commit: Not verified.
- Later documentation-only commits, if any: Pending final commit.

## Known implementation commits

- `37168d8` — main technical implementation and security/runtime fixes.
- `0bb3d53` — final demo changes: third application instance, public port 8090,
  NGINX healthcheck, and app-03 upstream.
- `2c4edf7` — validation and failure-recovery scripts aligned with the final
  three-instance / port-8090 state.

## Requirement evidence

| Requirement | Evidence | Commit / state | Video timestamp |
|---|---|---|---|
| Log analysis | `docs/log_analysis.md`, `logs/` | `37168d8` | Not recorded |
| Troubleshooting journal | `troubleshooting.md` | `37168d8` | Not recorded |
| Docker/Compose runtime | `docker-compose.yml`, `Dockerfile` | `37168d8` | Not recorded |
| Three Flask instances | `docker-compose.yml`, `nginx/nginx.conf` | `0bb3d53` | Not recorded |
| Public port 8090 | `docker-compose.yml`, `validate.py` | `0bb3d53`, `2c4edf7` | Not recorded |
| Health/readiness | `validate.py`, application endpoints | `2c4edf7` | Not recorded |
| PostgreSQL persistence | `docker-compose.yml`, `backup.sh`, `restore.sh` | `37168d8` | Not recorded |
| Redis persistence | `docker-compose.yml` | `37168d8` | Not recorded |
| Failure/recovery test | `failure_test.py` | `2c4edf7` | Not recorded |
| Security review | `docs/security_review.md` | Final documentation state | Not recorded |
| Architecture diagram | `architecture.png` | Final documentation state | Not recorded |
| Decisions | `decisions.md` | `37168d8` | Not recorded |
| AI usage disclosure | `AI_USAGE.md` | Final documentation state | Not recorded |
| README / setup and validation | `README.md` | Final documentation state | Not recorded |
| CI | `.github/workflows/ci.yml` | Final CI run pending | Not recorded |

## Final-state validation

The final local validation state was verified with:

- `python3 validate.py` → 22 passed, 0 failed.
- `./failure_test.py` → failure detected during PostgreSQL outage and
  readiness recovered successfully.
- Final runtime: `app-01`, `app-02`, `app-03`, `nginx`, `postgres`, and `redis`.
- Final public endpoint: `127.0.0.1:8090`.

Video timestamps and challenge receipt information are intentionally marked
as unavailable until the actual evidence is available. No video or receipt
evidence is fabricated.

## Screenshot evidence

The repository includes a selected subset of screenshots under
`Photos/evidence/`. Sensitive screenshots containing visible credentials were
intentionally excluded from the repository.

| Screenshot | Evidence area |
|---|---|
| `Photos/evidence/Screenshot 2026-09-25 180752.png` | NGINX / application configuration investigation |
| `Photos/evidence/Screenshot 2026-09-25 181021.png` | Initial NGINX upstream configuration issue |
| `Photos/evidence/Screenshot 2026-09-25 181622.png` | Initial NGINX port configuration |
| `Photos/evidence/Screenshot 2026-09-25 181900.png` | NGINX/application runtime investigation |
| `Photos/evidence/Screenshot 2026-09-25 185812.png` | Dependency/readiness validation |
| `Photos/evidence/Screenshot 2026-09-25 195335.png` | Application records validation |
| `Photos/evidence/Screenshot 2026-09-25 200130.png` | Redis counter validation |
| `Photos/evidence/Screenshot 2026-09-25 200141.png` | PostgreSQL record creation validation |
| `Photos/evidence/Screenshot 2026-09-25 201423.png` | Network isolation validation |
| `Photos/evidence/Screenshot 2026-09-25 215059.png` | PostgreSQL persistence validation |
| `Photos/evidence/Screenshot 2026-09-25 215158.png` | PostgreSQL recreation/restore validation |
| `Photos/evidence/Screenshot 2026-09-25 232221.png` | Application resource limits |
| `Photos/evidence/Screenshot 2026-09-25 233030.png` | Non-root application container validation |

These screenshots supplement the repository files and command outputs; they
are not used as a substitute for reproducible validation commands.
