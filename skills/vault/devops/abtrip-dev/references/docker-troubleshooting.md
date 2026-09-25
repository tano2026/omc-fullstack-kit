### Docker Credential Issue on Windows Bash (Hermes Terminal)

**Problem:**
When running `docker` or `docker compose` commands from Hermes's bash terminal on Windows, Docker Desktop might fail with the error:
`error getting credentials - err: exec: "docker-credential-desktop": executable file not found in %PATH%`

This occurs because the bash environment within Hermes does not inherit the correct PATH to `docker-credential-desktop.exe` from Docker Desktop's installation, leading to authentication failures when Docker tries to pull images or interact with the Docker daemon.

**Solution:**
Modify the Docker configuration file `config.json` to disable the `credsStore` helper.

1.  **Locate `config.json`**: This file is typically found at `C:\\Users\\<YourUser>\\.docker\\config.json`.
2.  **Edit `config.json`**: Open the file and change the `credsStore` entry.

    **Before:**
    ```json
    {
        "auths": {},
        "credsStore": "desktop",
        "currentContext": "desktop-linux"
    }
    ```

    **After:**
    ```json
    {
        "auths": {},
        "credsStore": "",
        "currentContext": "desktop-linux"
    }
    ```
    By setting `credsStore` to an empty string, Docker will no longer attempt to use `docker-credential-desktop` for credential management in this context.

### Docker CLI Hangs from Git Bash Even When Desktop Is Running

**Symptoms:**
- `docker ps`, `docker info`, `docker compose` all hang indefinitely (no output, no error)
- `tasklist | grep docker` shows Docker Desktop.exe + com.docker.backend.exe running
- Even using the full path (`C:/Users/.../DockerDesktop/resources/bin/docker.exe`) doesn't help

**Root cause:** Docker Desktop UI started but the Docker Engine (Linux VM) hasn't finished booting. The CLI connects to the daemon via a named pipe — if the daemon isn't accepting connections, the CLI blocks waiting.

**Fix:**
1. Wait for Docker Desktop tray icon to stop animating (whale stops spinning)
2. Run `docker ps` from a Windows-native terminal (cmd.exe / PowerShell) to verify — if it works there but not in Git Bash, the issue is the named pipe path resolution
3. If CLI still hangs after tray icon is stable: restart Docker Desktop (`taskkill /F /IM "Docker Desktop.exe"`, then relaunch)
4. Typical wait: 30-90 seconds after Docker Desktop window appears

**Detection pattern:** Use `tasklist | grep docker` to check if processes exist BEFORE attempting `docker ps`. If backend processes exist but `docker ps` hangs → engine booting, wait and retry.

### Next.js Dev Mode with Docker — volume mount + multi-stage pitfall

**Symptom:** Container exits with `Error: Cannot find module '/app/server.js'` or `sh: next: not found`.

**Root cause:** The multi-stage Dockerfile builds `.next/standalone/server.js`, but at runtime the volume mount `./frontend:/app` replaces the entire `/app` directory with the host's source code, which doesn't contain the built output.

**Anti-pattern: anonymous volume `/app/node_modules`**
Adding `- /app/node_modules` to `docker-compose` volumes creates an empty Docker-managed volume that blocks node_modules from BOTH:
1. The image (bind mount replaced `/app` entirely)
2. The host (anonymous volume takes priority over the bind mount at that path)

Result: `next: not found` even though both image and host have `node_modules/next/`.

**Fix for dev mode:**
1. Dockerfile: single-stage, no build:
   ```dockerfile
   FROM node:20-alpine
   WORKDIR /app
   ENV NODE_ENV=development
   ENV NEXT_TELEMETRY_DISABLED=1
   EXPOSE 3000
   ENV PORT=3000 HOSTNAME=0.0.0.0
   CMD ["npm", "run", "dev"]
   ```
2. docker-compose volumes: just the bind mount, NO anonymous volume:
   ```yaml
   volumes:
     - ./frontend:/app
   ```
3. Host must have `node_modules/` (run `npm install` locally first).

**Verification:** `docker compose logs <service> --tail=20` shows `ready - started server on 0.0.0.0:3000, url: http://localhost:3000`.

### General Docker Troubleshooting Steps (within Hermes)

-   **Check Docker installation/status (outside Hermes)**: If `docker --version` or `docker compose version` fails in Hermes, verify Docker Desktop is installed and running correctly on the host machine (e.g., in PowerShell).
-   **Find absolute path to `docker.exe`**: If Hermes's bash environment doesn't find `docker`, use `where.exe docker` in PowerShell to find its absolute path (e.g., `C:\\Users\\<YourUser>\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe`). Then, use this absolute path in subsequent `terminal` calls.
-   **Debug Docker Compose build errors**:
    1.  **Read Dockerfile**: Inspect `Dockerfile`s for build stages, `COPY` commands, and `RUN` commands.
    2.  **Check missing files/directories**: If `COPY` fails with "not found", check if the source file/directory exists on the host (e.g., using `ls`). Create it if it's missing (e.g., `mkdir`).
    3.  **Check logs of failing containers**: Use `docker compose logs <service_name>` to view detailed error messages for containers that fail to start.
    4.  **Missing dependencies**: For `ModuleNotFoundError` in Python containers, add the missing package to `requirements.txt` and rebuild the image. For Node.js, ensure `npm install` runs correctly.
    5.  **Code-level errors during build**: If TypeScript/JavaScript errors occur during `npm run build`, inspect the code and apply patches (e.g., missing imports, syntax errors).
