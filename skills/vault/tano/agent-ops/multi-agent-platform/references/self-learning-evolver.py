# Self-Learning Engine: core/evolver.py
# Live at: D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core/core/evolver.py
# Created: 2026-07-18

## Evolver.run(agent, min_confidence=0.7) -> int (new skills created)
- Calls ready_to_evolve() from InstinctManager
- For each instinct: compose skill .md file into skills/auto/<slug>.md
- Format includes: title, pattern_type, agent, confidence, trigger, action, description, source observations
- Mark instinct as evolved

## run_evolve(agent="ceo", min_confidence=0.7) -> int
Entry point for cron/auto-learn.py:
  1. PatternDetector.scan(agent, since_hours=48)
  2. InstinctManager.batch_upsert(agent, patterns)
  3. Evolver.run(agent, min_confidence)

## Evolver.report(agent) -> str
User-readable report: instinct count, confidence bars, hit counts, evolved flags

## auto-learn.py
Standalone script:
  from core.evolver import run_evolve
  print(run_evolve(sys.argv[1] if len>1 else "ceo"))

Evolved skills go to: agent-core/skills/auto/<name>.md
