# Hermes Plugin Development

> Absorbed from `hermes-plugin-development` (Jul 2026)

## Plugin Structure

Each plugin is a directory with:

```
my-plugin/
├── plugin.yaml          # Required: metadata + tool definitions
├── tools/               # Tool implementations (Python files)
│   ├── __init__.py
│   ├── my_tool.py
│   └── ...
├── hooks/               # Lifecycle hooks (pre/post processing)
│   ├── before_tool.py
│   └── after_tool.py
└── assets/              # Static assets (optional)
```

## plugin.yaml Format

```yaml
name: my-plugin
version: 1.0.0
description: "Does X for Hermes"

tools:
  - name: my_tool
    description: "Does Y"
    function: tools.my_tool.run
    parameters:
      type: object
      properties:
        input:
          type: string
          description: "Input text"

hooks:
  on_startup:
    - hooks.before_tool.on_startup
  on_shutdown:
    - hooks.after_tool.on_shutdown

dependencies:
  - requests>=2.28
```

## Lifecycle Hooks

| Hook | When | Signature |
|------|------|-----------|
| `on_startup` | Agent starts | `async def on_startup(ctx)` |
| `on_shutdown` | Agent stops | `async def on_shutdown(ctx)` |
| `before_tool_call` | Before each tool | `async def before_tool(ctx, tool_name, args)` |
| `after_tool_call` | After each tool | `async def after_tool(ctx, tool_name, result)` |

## Development Workflow

```bash
# Create new plugin
mkdir -p ~/.hermes/plugins/my-plugin/{tools,hooks,assets}

# Write plugin.yaml
cat > ~/.hermes/plugins/my-plugin/plugin.yaml << 'YAML'
name: my-plugin
version: 1.0.0
tools: []
YAML

# Enable in config
hermes config set plugins.my-plugin.enabled true
```

## Pitfalls

- **Python path**: Plugin tools run in Hermes' Python env; install deps there
- **Async only**: All hooks and tool functions must be async
- **Error handling**: Exceptions in a tool crash the tool, not the agent
- **State**: Plugins are stateless by design; use files/memory for persistence
- **Naming**: Plugin name must be unique; no hyphens in plugin directory names
- **Reload**: Plugins load at Hermes startup; `hermes plugin reload <name>` for hot reload
