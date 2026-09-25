#!/usr/bin/env python3

import subprocess
import sys
import time
import urllib.request

URL = "http://localhost:8080/ready"
TIMEOUT = 2
RECOVERY_TIMEOUT = 30


def run(cmd):
    return subprocess.run(
        cmd,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def ready_status():
    try:
        with urllib.request.urlopen(URL, timeout=TIMEOUT) as response:
            return response.status
    except Exception as exc:
        if hasattr(exc, "code"):
            return exc.code
        return None


def postgres_healthy():
    result = run([
        "docker", "inspect",
        "--format={{.State.Health.Status}}",
        "postgres",
    ])
    return result.returncode == 0 and result.stdout.strip() == "healthy"


def wait_for_recovery():
    deadline = time.time() + RECOVERY_TIMEOUT

    while time.time() < deadline:
        if postgres_healthy() and ready_status() == 200:
            return True
        time.sleep(2)

    return False


def main():
    print("=== BARQ Failure/Recovery Test ===")

    baseline = ready_status()
    print(f"Baseline /ready status: {baseline}")

    if baseline != 200:
        print("FAIL: baseline is not ready.")
        return 1

    stopped = False

    try:
        print("Stopping PostgreSQL...")
        result = run(["docker", "compose", "stop", "postgres"])

        if result.returncode != 0:
            print(result.stdout)
            print("FAIL: could not stop PostgreSQL.")
            return 1

        stopped = True

        time.sleep(2)

        failed_status = ready_status()
        print(f"During PostgreSQL failure /ready status: {failed_status}")

        if failed_status == 200:
            print("FAIL: /ready remained healthy while PostgreSQL was stopped.")
            return 1

        print("PASS: readiness failure detected.")

        print("Restoring PostgreSQL...")
        result = run(["docker", "compose", "start", "postgres"])

        if result.returncode != 0:
            print(result.stdout)
            print("FAIL: could not start PostgreSQL.")
            return 1

        stopped = False

        print("Waiting for PostgreSQL and application readiness...")

        if not wait_for_recovery():
            print("FAIL: system did not recover within timeout.")
            return 1

        print("PASS: PostgreSQL recovered.")
        print("PASS: /ready returned 200 after recovery.")
        print("=== Failure/Recovery Test: PASS ===")
        return 0

    finally:
        if stopped:
            print("Cleanup: starting PostgreSQL...")
            run(["docker", "compose", "start", "postgres"])


if __name__ == "__main__":
    sys.exit(main())
