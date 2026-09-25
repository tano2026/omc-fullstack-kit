# Self-Learning Engine: core/instinct.py
# Live at: D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core/core/instinct.py
# Created: 2026-07-18
# 3 classes: ObservationHook, PatternDetector, InstinctManager
# SQLite-backed, zero-dep (stdlib)

## ObservationHook
- record(agent, ttype, prompt, response, outcome, user_feedback, duration_ms, error_msg) -> obs_id
- mark_correction(obs_id, user_feedback)
- recent(agent, limit=50) -> list[dict]

## PatternDetector.scan(agent, since_hours=24) -> list[(pattern_type, title, desc, trigger, action, confidence)]
4 patterns:
  - correction (keyword heuristic: không/đừng/sai/thay vì/nên/hãy)
  - error (group by error_msg prefix, min 2 occurrences)
  - repetition (same ttype 3+ times in window)
  - workflow (multi-step success within 30min windows)

## InstinctManager
- upsert(agent, pattern_type, title, desc, trigger, action, confidence, source_ids)
- batch_upsert(agent, list_of_patterns) — preferred for cron
- ready_to_evolve(agent, min_confidence=0.7) -> list[dict]
- mark_evolved(instinct_id, skill_name)
- all(agent, min_confidence) -> list[dict]

## Tables
observations(id, agent, ttype, prompt, response, outcome, user_feedback, duration_ms, error_msg, created_at)
instincts(id, agent, pattern_type, title, description, trigger_hint, action_hint, confidence, hit_count, last_matched, evolved_into_skill, source_observation_ids, created_at)
