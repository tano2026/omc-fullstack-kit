# Repo Sync — Skills from AI-Vibe-Toolkit

> Absorbed from `repo-sync` (Jul 2026)

## Overview

Syncs skills from the [AI-Vibe-Toolkit](https://github.com/tano2026/AI-Vibe-Toolkit) GitHub repo into the local Hermes skills directory.

## Sync Commands

```bash
# One-time sync
hermes skill sync

# Or manually:
cd ~/.hermes && git clone https://github.com/tano2026/AI-Vibe-Toolkit.git skills-remote
cp -r skills-remote/skills/* skills/
rm -rf skills-remote
```

## What Gets Synced

- New skills from the upstream repo
- Updated skills (overwrites local with remote)
- Category structure (subdirectories)

## What Stays Local

- Agent-created skills (not in upstream repo)
- Pinned skills (protected from overwrite)
- Local modifications to skills that exist in upstream

## Configuration

```yaml
# In config.yaml
skill_sync:
  repo: tano2026/AI-Vibe-Toolkit
  branch: main
  path: skills/
  auto_sync: false  # true = sync every startup
  exclude:
    - "private-*"
```

## Pitfalls

- **Overwrite risk**: Running sync overwrites local skills that match upstream names
- **Conflicts**: If a local skill has same name as a new upstream skill, local is overwritten
- **Network**: Requires GitHub access; fails behind strict proxies
- **Disk space**: Repo ~50MB; clean up old skill directories periodically
- **Dependency**: Sync requires `git` installed and configured
