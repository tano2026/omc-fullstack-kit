# Windows + Docker + MSYS Pitfalls

## MSYS_NO_PATHCONV=1 is MANDATORY

On Windows with Git Bash (MSYS), any path containing a `/` gets mangled into a Windows-style path.
This breaks `docker cp` and `docker exec` commands because Docker sees the mangled path.

### The Problem

```bash
# WRONG — MSYS converts /app/test.py → C:/Program Files/Git/app/test.py
docker exec abtrip-abtrip-backend-1 python /app/test.py
# → python: can't open file '/app/C:/Program Files/Git/app/test.py': [Errno 2] No such file or directory
```

### The Fix

Always prefix Docker commands with `MSYS_NO_PATHCONV=1`:

```bash
# CORRECT
MSYS_NO_PATHCONV=1 docker cp test.py abtrip-abtrip-backend-1:/app/test.py
MSYS_NO_PATHCONV=1 docker exec abtrip-abtrip-backend-1 python /app/test.py
```

### Canonical Docker dev-test pattern

```bash
cd "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/backend" && \
  MSYS_NO_PATHCONV=1 docker cp test_e2e.py abtrip-abtrip-backend-1:/app/test_e2e.py && \
  MSYS_NO_PATHCONV=1 docker exec abtrip-abtrip-backend-1 python /app/test_e2e.py
```

## Rebuild & restart

```bash
cd "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip" && \
  docker compose -f docker-compose.local.yml up -d --build --force-recreate --no-deps abtrip-backend
```

Always `sleep 5` after rebuild before running tests — container needs time to start.
