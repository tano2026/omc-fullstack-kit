# Dashboard Deploy Pitfall — `__pycache__` Stale Code

## The Bug

Sau khi sửa `dashboard/app.py` hoặc `dashboard/__init__.py`, kill process cũ và chạy lại:

```bash
taskkill /F /PID <old_pid>
cd "D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core" && python dashboard/app.py
```

API trả về **data cũ** (VD: `/api/projects` trả 4 projects dù code có 5).

## Root cause

Python cache `.pyc` files trong `__pycache__/`. Khi chạy `python dashboard/app.py`, Python import `dashboard.app` từ `.pyc` cũ — không đọc file `.py` đã sửa.

Đặc biệt nghiêm trọng trên Windows vì:
- File timestamp ko đáng tin (Windows FAT vs NTFS)
- `importlib.invalidate_caches()` không luôn clear `.pyc` cache

## Fix

Xoá toàn bộ `__pycache__` trong agent-core tree TRƯỚC khi restart:

```python
import shutil, os

root = "D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core"
for dirpath, dirnames, _ in os.walk(root):
    if '__pycache__' in dirnames:
        cache = os.path.join(dirpath, '__pycache__')
        shutil.rmtree(cache)
        print(f"Removed: {cache}")
```

Sau đó kill process cũ + start mới:

```python
import subprocess, time
subprocess.run(r'taskkill /F /PID <old_pid> 2>nul', shell=True)
time.sleep(1)
p = subprocess.Popen(['python', 'dashboard/app.py'], cwd=root, ...)
time.sleep(3)  # wait for startup
```

## Prevention

Trong `app.py`, thêm cache invalidation ở đầu file:

```python
import sys
# Force reimport on every startup
for mod in list(sys.modules.keys()):
    if 'dashboard' in mod:
        del sys.modules[mod]
```

(Nhưng cách này ko đủ — vẫn cần xoá `__pycache__`.)
