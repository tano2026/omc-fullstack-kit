"""
Reusable Python disk scanner for Windows when du is useless (disk >95% full).

Usage: copy the scan_targets() section below into execute_code,
adjust targets list, and run. Uses os.scandir which is faster than
os.walk on saturated NTFS volumes.
"""
import os, time

def get_size(path):
    """Recursive size via os.scandir — faster than os.walk on Windows."""
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += get_size(entry.path)
                except (PermissionError, OSError):
                    pass
    except (PermissionError, OSError):
        pass
    return total

# ============================================
# SCAN TARGETS — edit this list as needed
# ============================================
user = "Nguyen Ngoc Tan"
targets = [
    # Hermes Agent AppData (can silently grow to 100+ GB)
    rf"C:\Users\{user}\AppData\Local\hermes",

    # Python toolchain caches
    rf"C:\Users\{user}\AppData\Local\uv",
    rf"C:\Users\{user}\AppData\Local\pip",
    rf"C:\Users\{user}\AppData\Local\pip\Cache",

    # Node.js ecosystem
    rf"C:\Users\{user}\AppData\Roaming\npm\node_modules",
    rf"C:\Users\{user}\AppData\Local\npm-cache",
    rf"C:\Users\{user}\AppData\Local\Yarn",
    rf"C:\Users\{user}\AppData\Local\pnpm-cache",

    # Browsers
    rf"C:\Users\{user}\AppData\Local\Google",
    rf"C:\Users\{user}\AppData\Local\CocCoc",

    # Docker
    rf"C:\Users\{user}\AppData\Local\Docker",

    # AI apps
    rf"C:\Users\{user}\AppData\Local\Perplexity",

    # Microsoft
    rf"C:\Users\{user}\AppData\Local\Microsoft",
    rf"C:\Users\{user}\AppData\Local\Temp",

    # Browser automation
    rf"C:\Users\{user}\AppData\Local\ms-playwright",

    # AppData Roaming (VS Code, npm, Zoom, etc)
    rf"C:\Users\{user}\AppData\Roaming\Code",
    rf"C:\Users\{user}\AppData\Roaming\npm",
    rf"C:\Users\{user}\AppData\Roaming\Zoom",
    rf"C:\Users\{user}\AppData\Roaming\ZaloData",

    # User home dot-folders
    rf"C:\Users\{user}\.cache",
    rf"C:\Users\{user}\.docker",
    rf"C:\Users\{user}\.claude",
]

results = []
for t in targets:
    if not os.path.exists(t):
        continue
    start = time.time()
    size = get_size(t)
    elapsed = time.time() - start
    results.append((size, elapsed, t))

results.sort(key=lambda x: -x[0])

print("=== DISK USAGE BY DIRECTORY ===")
total = 0
for size, elapsed, path in results:
    total += size
    marker = " ⚠️ SLOW" if elapsed > 5 else ""
    print(f"  {size/1e9:7.2f} GB  {elapsed:5.1f}s{marker}  {path}")

print(f"\nTotal scanned: {total/1e9:.2f} GB")
