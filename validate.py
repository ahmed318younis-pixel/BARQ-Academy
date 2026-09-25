#!/usr/bin/env python3
"""Bounded environment validation for the BARQ Academy assessment."""

import json
import subprocess
import sys
import urllib.error
import urllib.request

EXPECTED_CONTAINERS = ["app-01", "app-02", "nginx", "postgres", "redis"]
ENDPOINTS = ["/", "/health", "/ready", "/instance", "/records", "/counter"]


def run(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check(name, condition, detail=""):
    if condition:
        print(f"PASS: {name}")
        return True

    message = f"FAIL: {name}"
    if detail:
        message += f" — {detail}"
    print(message)
    return False


def main():
    passed = 0
    failed = 0

    def record(name, condition, detail=""):
        nonlocal passed, failed
        if check(name, condition, detail):
            passed += 1
        else:
            failed += 1

    # 1. Required containers exist and are running.
    for container in EXPECTED_CONTAINERS:
        rc, stdout, stderr = run(
            ["docker", "inspect", "--format", "{{.State.Status}}", container]
        )
        record(
            f"container {container} is running",
            rc == 0 and stdout == "running",
            stderr or stdout,
        )

    # 2. Health status for services that provide healthchecks.
    for container in ["app-01", "app-02", "postgres", "redis"]:
        rc, stdout, stderr = run(
            ["docker", "inspect", "--format", "{{.State.Health.Status}}", container]
        )
        record(
            f"{container} is healthy",
            rc == 0 and stdout == "healthy",
            stderr or stdout,
        )

    # 3. Only NGINX should publish a host port.
    rc, stdout, stderr = run(
        ["docker", "inspect", "--format", "{{json .HostConfig.PortBindings}}", "nginx"]
    )
    nginx_ports = stdout if rc == 0 else ""
    record(
        "nginx publishes host port 8080",
        rc == 0 and '"80/tcp"' in nginx_ports and '"8080"' in nginx_ports,
        stderr or nginx_ports,
    )

    for container in ["postgres", "redis", "app-01", "app-02"]:
        rc, stdout, stderr = run(
            ["docker", "inspect", "--format", "{{json .HostConfig.PortBindings}}", container]
        )
        record(
            f"{container} has no host port bindings",
            rc == 0 and stdout == "{}",
            stderr or stdout,
        )

    # 4. Required application endpoints return HTTP 200.
    for endpoint in ENDPOINTS:
        url = f"http://127.0.0.1:8080{endpoint}"
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                status = response.status
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            status = None
            error = str(exc)
        else:
            error = ""

        record(
            f"GET {endpoint} returns 200",
            status == 200,
            error or f"HTTP {status}",
        )

    print()
    print(f"Validation summary: {passed} passed, {failed} failed")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())