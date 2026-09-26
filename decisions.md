# Technical Decisions

This document records the main technical decisions made during the BARQ Academy DevOps assessment.

## Decision 1 — Pinned container images

- Choice: Use the supplied image versions with immutable SHA256 digests.
- Why: Makes the assessment environment reproducible and avoids unexpected image changes.
- Alternative: Use mutable version tags such as `postgres:16-alpine`.
- Trade-off: Digest-pinned images require an explicit update when a newer image digest is desired.
- Evidence / commit: Pinned image digests in `docker-compose.yml`; commit `37168d8`.
- Production improvement: Establish an image update process with vulnerability scanning and controlled digest updates.

## Decision 2 — Separate liveness and readiness checks

- Choice: `/health` is used for application liveness, while `/ready` verifies PostgreSQL and Redis dependencies.
- Why: A running Flask process is not necessarily ready to serve dependency-dependent requests.
- Alternative: Use a single health endpoint for both purposes.
- Trade-off: Separate checks are clearer but require clients and orchestration to understand the distinction.
- Evidence / commit: `validate.py` and `failure_test.py`; final validation alignment commit `2c4edf7`.
- Production improvement: Add dependency-specific metrics and alerting around readiness failures.

## Decision 3 — Frontend/backend network separation

- Choice: NGINX is attached only to the frontend network; Flask instances are attached to frontend and backend; PostgreSQL and Redis are backend-only.
- Why: Prevents the reverse proxy from directly reaching database and cache services.
- Alternative: Put every service on one shared Docker network.
- Trade-off: Network isolation adds configuration complexity but reduces unnecessary connectivity.
- Evidence / commit: Docker Compose network configuration and manual negative connectivity test; implementation commit `37168d8`.
- Production improvement: Apply equivalent segmentation and least-privilege network policies in the target orchestration platform.

## Decision 4 — Named persistent storage

- Choice: PostgreSQL uses a named Docker volume for `/var/lib/postgresql/data`, and Redis uses a named volume with AOF enabled.
- Why: Container recreation should not remove application state.
- Alternative: Store database state in the container filesystem or use temporary storage.
- Trade-off: Named volumes preserve state locally but are not a complete production backup/DR solution.
- Evidence / commit: Backup/restore scripts and persistence testing; implementation commit `37168d8`.
- Production improvement: Use managed database/cache services or durable storage with tested off-host backups.

## Decision 5 — Dependency-aware startup ordering

- Choice: Flask services depend on healthy PostgreSQL and Redis; NGINX depends on healthy Flask instances.
- Why: Reduces startup races and prevents NGINX from starting against unavailable application backends.
- Alternative: Start all services simultaneously and rely only on application retries.
- Trade-off: Startup can take longer while dependencies become healthy.
- Evidence / commit: `docker-compose.yml` health-based `depends_on`; implementation commit `37168d8`.
- Production improvement: Combine orchestration readiness probes with application-level retry/backoff behavior.

## Decision 6 — Restart policy and resource limits

- Choice: Application services use `unless-stopped`; each Flask instance has a 0.50 CPU and 128 MB memory limit.
- Why: Restart policy improves recovery from process/container failure, while resource limits provide bounded lab resource consumption.
- Alternative: Disable automatic restart and leave resources unlimited.
- Trade-off: Automatic restarts can hide recurring failures if monitoring is absent, and the selected limits are assessment/lab values rather than production sizing.
- Evidence / commit: Docker Compose restart/resource configuration and container inspection; implementation commit `37168d8`.
- Production improvement: Size limits from observed workload data and add monitoring/alerting for OOM and restart loops.

## Decision 7 — Run the Flask application as a non-root user

- Choice: Create an unprivileged `app` user and run the application with that user.
- Why: Reduces the privileges available to the application process if compromised.
- Alternative: Run the container as root.
- Trade-off: File ownership and permissions must be handled correctly.
- Evidence / commit: Dockerfile and `docker exec app-01 id`; implementation commit `37168d8`.
- Production improvement: Add filesystem read-only controls and further container hardening where compatible with the application.

## Decision 8 — Keep runtime secrets out of the image

- Choice: Remove `config/app.env` from the Docker image and require the PostgreSQL password through environment substitution.
- Why: Secrets should not be baked into an image layer or committed to source control.
- Alternative: Copy the runtime environment file into the image.
- Trade-off: The runtime environment must provide the required secret before Compose starts.
- Evidence / commit: Dockerfile, `.gitignore`, `.env.example`, and Compose configuration; implementation commit `37168d8`.
- Production improvement: Use a dedicated secret manager or Docker/Orchestrator secrets mechanism rather than local `.env` files.
