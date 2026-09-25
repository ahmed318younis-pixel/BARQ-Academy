# Security Review

## Scope

This review covers the Docker Compose environment, container image, networking,
secrets handling, persistence, and runtime configuration.

## Findings

### 1. Plain-text PostgreSQL credential in Compose

**Risk:** The PostgreSQL password is defined directly in `docker-compose.yml`.

**Impact:** Anyone with access to the repository or Compose configuration may
obtain the database credential.

**Current mitigation:** The application secret file is no longer copied into
the Docker image and `config/app.env` is removed from Git tracking.

**Recommendation:** Use Docker secrets or an external secret-management
mechanism for production deployments.

---

### 2. Application environment file contains secrets

**Risk:** `config/app.env` contains application credentials.

**Impact:** Accidental commit or sharing of the file could expose credentials.

**Current mitigation:** `config/app.env` is listed in `.gitignore` and removed
from Git tracking.

**Recommendation:** Provide a sanitized `.env.example` containing only
placeholders.

---

### 3. Database and Redis are isolated from NGINX

**Risk:** Backend services should not be directly reachable from the reverse
proxy.

**Current mitigation:** NGINX is connected only to the `frontend` network,
while PostgreSQL and Redis are connected only to `backend`.

**Validation:** NGINX could no longer resolve the PostgreSQL and Redis service
names after the network isolation change.

---

### 4. Backend network is marked internal

**Risk:** Backend services should not require direct external network access.

**Current mitigation:** The Docker `backend` network is configured with
`internal: true`.

**Recommendation:** Keep database and cache services on the internal backend
network.

---

### 5. Backend services do not publish host ports

**Risk:** Publishing PostgreSQL or Redis ports unnecessarily increases the
attack surface.

**Current mitigation:** PostgreSQL, Redis, and both application containers
have no host port bindings.

**Validation:** Container inspection confirmed no host port bindings for these
services.

---

### 6. Application containers initially ran as root

**Risk:** A compromised application process running as root has greater
container privileges.

**Current mitigation:** The Dockerfile creates a dedicated `app` user with
UID/GID 10001 and runs the application as that user.

**Validation:** `docker exec app-01 id` reported UID 10001.

---

### 7. Application image previously contained the environment file

**Risk:** Copying a secret-containing environment file into an image can
persist credentials in image layers.

**Current mitigation:** The Dockerfile no longer copies `config/app.env`.

**Validation:** `/srv/app.env` was absent from the rebuilt application
container while the application continued to receive configuration through
Compose.

---

### 8. Unbounded application resources

**Risk:** A runaway application process could consume excessive CPU or memory.

**Current mitigation:** Application containers have a limit of 0.50 CPU and
128 MiB memory.

**Note:** These values are engineering limits selected for this assessment and
are not stated as BARQ Systems production requirements.

---

### 9. Container startup dependency ordering

**Risk:** Applications may start before PostgreSQL or Redis are ready.

**Current mitigation:** Application services depend on healthy PostgreSQL and
Redis services. NGINX depends on healthy application instances.

**Validation:** `docker compose config` showed `service_healthy` dependency
conditions.

---

### 10. Host exposure is limited to the reverse proxy

**Risk:** Exposing multiple application/service ports increases attack
surface.

**Current mitigation:** Only NGINX publishes the host port, bound to
`127.0.0.1:${PUBLIC_PORT:-8080}`.

**Recommendation:** For a remotely accessible deployment, expose the reverse
proxy through the intended firewall/load-balancer boundary rather than
publishing backend services.
