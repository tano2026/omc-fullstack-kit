# Paint Point Engine v2.0 — Architecture Reference

Built: 20/07/2026
File: `D:\MMO Du an\TuVi\engine\paint_point_engine.py`
Lines: ~480 (including STAR_ALIASES, 21 rules, class PaintPointEngine)
Test: `test_engine.py` + `test_chart_data.json` — passed 21/21 matches

## Key Design Decisions

### 1. Class-based, not dict-based
Old v1.0 was a loose dict-of-dicts. v2.0 is a `PaintPointEngine` class with:
- `__init__()` — loads rules + psychology definitions
- `detect(chart_data)` — returns structured results
- `get_urgency_text(hits)` — markdown output for UI
- `get_demo_report(chart_data)` — 7-item demo funnel

### 2. STAR_ALIASES normalization
MCP returns "Thien Co" (no diacritics). Rules use "Thiên Cơ" (with diacritics).
50+ aliases defined. New unmapped names cause 0 matches — catch this immediately in testing.

### 3. Confidence scoring
Each rule has a base (0.70-0.95). Detect() dynamically adjusts:
- Thân cư +0.10
- Hóa (any) +0.05
- Hóa Lộc +0.10
- Tuần/Triệt -0.05
- Floor at 0.30

### 4. Six psychology frameworks
Loss Aversion, Confirmation Bias, Uncertainty Aversion, Social Proof, Sunk Cost, Ego Trap.
Each rule references 1-2 psychology hooks for persuasive output.

## File Locations
- `D:\MMO Du an\TuVi\engine\paint_point_engine.py` — main engine
- `D:\MMO Du an\TuVi\engine\test_engine.py` — test runner using test_chart_data.json
- `D:\MMO Du an\TuVi\engine\test_chart_data.json` — real chart data (Tân, 1/5/1984, 9h sáng, Nam)
