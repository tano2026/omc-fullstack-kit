# Python Package Naming — Hyphen vs Underscore

## The Rule

**Python cannot import packages with hyphens in the directory name.**

```python
# ❌ SAI — thư mục named "watcher-api"
import watcher-api          # SyntaxError
from watcher-api import x   # SyntaxError

# ✅ ĐÚNG — rename thành "watcher_api"
from watcher_api import x
```

## Why

The `-` (hyphen/minus) is not a valid identifier character in Python. When the interpreter sees `import watcher-api`, it parses it as `import watcher - api` which is a subtraction expression, not an import statement.

## Fix

```bash
mv watcher-api watcher_api
mv watcher-scraper watcher_scraper
```

Then create `__init__.py` in the renamed directory:

```python
"""watcher_api package — description."""
```

## Also affects

- Import statements in all submodules (must use underscores)
- Any `sys.path.insert(0, ...)` + import pattern
- pyproject.toml `packages` directive (if using setuptools)
- MCP server references in configuration files (use path, not import)
