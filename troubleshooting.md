# Troubleshooting Journal

This journal records the actual investigation and remediation performed during the BARQ Academy DevOps assessment.

## Entry 1 — Application healthcheck failure

- Symptom: `app-01` and `app-02` were reported as unhealthy.
- Hypothesis: The healthcheck endpoint or application bind address did not match the running Flask server.
- Command or test: Inspected the Docker healthcheck and tested the application `/health` endpoint from inside the container.
- Actual output: The configured healthcheck requested `/healthz`, while the application contract uses `/health`. The application was also initially bound to `127.0.0.1`.
- Failed attempt and what changed your thinking: The initial container state showed an unhealthy application despite the Flask process being present. Checking the actual endpoint and bind configuration identified a configuration mismatch rather than a process startup failure.
- Root cause: Incorrect healthcheck path and application bind address.
- Fix: Changed the healthcheck to `/health` and `APP_HOST` to `0.0.0.0`.
- Retest evidence: Application containers became healthy and `/health` returned HTTP 200.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: None observed in the local validation.

## Entry 2 — NGINX upstream connection failure

- Symptom: NGINX returned upstream connection errors and HTTP 502 responses.
- Hypothesis: NGINX could not reach the Flask backend on the configured upstream address/port.
- Command or test: Reviewed `nginx/nginx.conf`, application port configuration, and NGINX error/access logs.
- Actual output: The upstream configuration referenced `app-01:8081` while the application port was `8080`. Logs also showed connection-refused errors while the application was bound to localhost.
- Failed attempt and what changed your thinking: The first configuration review showed more than one mismatch, so the upstream port and application bind address were tested separately.
- Root cause: Incorrect upstream port combined with the application binding to localhost.
- Fix: Changed the upstream port to `8080` and changed the application bind address to `0.0.0.0`.
- Retest evidence: `nginx -t` passed and requests through NGINX succeeded.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: None observed during local testing.

## Entry 3 — PostgreSQL connectivity mismatch

- Symptom: Application readiness and database operations failed.
- Hypothesis: The application was using a PostgreSQL port or credential different from the database container configuration.
- Command or test: Compared `DATABASE_URL` configuration with the PostgreSQL service configuration and tested the application dependency checks.
- Actual output: PostgreSQL was configured for its container port `5432`, while the application configuration referenced `5433`. A credential mismatch was also identified during dependency testing.
- Failed attempt and what changed your thinking: Correcting only the port did not fully resolve the database dependency, which led to checking the configured credentials.
- Root cause: PostgreSQL port mismatch and credential mismatch.
- Fix: Aligned the application configuration with the PostgreSQL service port and corrected the local runtime credential configuration.
- Retest evidence: PostgreSQL dependency check passed and `/ready` returned HTTP 200.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: The local runtime secret is intentionally not recorded in this journal.

## Entry 4 — Redis connectivity mismatch

- Symptom: Redis-dependent operations were failing and logs contained Redis timeout errors.
- Hypothesis: The application Redis connection settings did not match the Redis service.
- Command or test: Compared the Redis URL configuration with the Redis service port and reviewed application logs.
- Actual output: Redis was configured for container port `6379`, while the application configuration referenced `6380`. Historical application logs also contained Redis timeout errors.
- Failed attempt and what changed your thinking: The application dependency check isolated Redis separately from PostgreSQL, confirming that the Redis connection needed correction.
- Root cause: Redis port mismatch.
- Fix: Changed the application Redis connection to use the container service port `6379`.
- Retest evidence: Redis dependency check passed and `/counter` returned HTTP 200.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: None observed during local validation.

## Entry 5 — PostgreSQL persistence configuration

- Symptom: The original PostgreSQL storage configuration did not use `/var/lib/postgresql/data` as the persistent database data location.
- Hypothesis: Container recreation could lose database state.
- Command or test: Inspected the PostgreSQL volume and tmpfs configuration, created a database backup, corrected the volume mount, restored the data, and recreated the PostgreSQL container without deleting the named volume.
- Actual output: The original configuration used a backup-path mount and tmpfs for the PostgreSQL data directory.
- Failed attempt and what changed your thinking: The initial persistence configuration was insufficient for the required data directory, so the database storage mapping was corrected before performing the persistence test.
- Root cause: Incorrect PostgreSQL data volume configuration.
- Fix: Changed the persistent mount to the named volume `postgres-data:/var/lib/postgresql/data` and removed the tmpfs data mount.
- Retest evidence: Three records remained available after PostgreSQL container recreation.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: This is local Docker-volume persistence, not an off-host disaster-recovery mechanism.

## Entry 6 — Redis persistence

- Symptom: The original Redis configuration disabled persistence.
- Hypothesis: Redis counter state would not survive container recreation.
- Command or test: Inspected Redis command arguments and persistence configuration, then enabled AOF and added a named volume.
- Actual output: The original configuration used `--save "" --appendonly no`.
- Failed attempt and what changed your thinking: The original configuration explicitly disabled both snapshot and AOF persistence, so a persistent volume alone would not preserve Redis state.
- Root cause: Redis persistence was disabled.
- Fix: Enabled `--appendonly yes` and mounted the named `redis-data` volume at `/data`.
- Retest evidence: Redis persistence was verified across container recreation and the counter state was retained.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: Redis persistence here is intended for the assessment environment and is not a substitute for a production Redis durability/HA design.

## Entry 7 — Network isolation

- Symptom: NGINX initially had connectivity to the backend network.
- Hypothesis: NGINX could potentially reach PostgreSQL or Redis directly.
- Command or test: Inspected NGINX network attachments and attempted connectivity from the NGINX container to PostgreSQL.
- Actual output: NGINX was initially attached to the backend network.
- Failed attempt and what changed your thinking: The negative connectivity test demonstrated why network membership needed to be restricted.
- Root cause: NGINX had unnecessary backend network membership.
- Fix: Removed the backend network from NGINX; PostgreSQL and Redis remain backend-only.
- Retest evidence: NGINX could no longer resolve/reach the PostgreSQL service by its backend service name.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: Docker network isolation is specific to this Compose environment.

## Entry 8 — Duplicate application identity

- Symptom: Both application instances were configured with the same `INSTANCE_ID`.
- Hypothesis: Requests could not reliably identify which Flask instance handled them.
- Command or test: Compared the two service environment configurations and tested `/instance`.
- Actual output: `app-02` initially used `INSTANCE_ID: app-01`.
- Failed attempt and what changed your thinking: Reviewing the service definitions showed the duplicate identity directly.
- Root cause: Incorrect environment value for `app-02`.
- Fix: Changed `app-02` to `INSTANCE_ID: app-02`.
- Retest evidence: Both instances expose distinct identity values through `/instance` and `X-Instance-ID`.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: The final three-instance configuration is part of the later challenge phase.

## Entry 9 — Runtime secret in image

- Symptom: The Dockerfile copied `config/app.env` into the application image.
- Hypothesis: Runtime credentials could become part of the image filesystem/layers.
- Command or test: Inspected the Dockerfile and rebuilt the image after removing the copy instruction.
- Actual output: The original Dockerfile contained a copy of `config/app.env`.
- Failed attempt and what changed your thinking: The configuration was identified as a security issue during the container hardening review.
- Root cause: Runtime secret configuration was included in the image build context.
- Fix: Removed the `COPY config/app.env` instruction and kept the runtime configuration outside the image.
- Retest evidence: `/srv/app.env` was absent from the rebuilt container and the application remained functional.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: Production should use a dedicated secret-management mechanism rather than local environment files.

## Entry 10 — Failure and recovery validation

- Symptom: A deliberate backend failure was required to prove readiness behavior and recovery.
- Hypothesis: Stopping PostgreSQL should cause `/ready` to fail and restoring PostgreSQL should return the application to ready state.
- Command or test: Executed `./failure_test.py`.
- Actual output: Baseline `/ready` returned 200; PostgreSQL was stopped; `/ready` returned 503; PostgreSQL was restored; `/ready` returned 200 after recovery.
- Failed attempt and what changed your thinking: No failed test attempt was recorded; the manual failure/recovery test was performed first to establish the expected behavior.
- Root cause: Not an incident; this was a deliberate failure-injection test.
- Fix: No application fix was required. PostgreSQL was restored after the test.
- Retest evidence: `=== Failure/Recovery Test: PASS ===`.
- Related commit: To be linked after implementation commit.
- Remaining uncertainty: The test covers PostgreSQL dependency failure; it does not represent every possible infrastructure failure mode.
