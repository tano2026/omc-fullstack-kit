# Multi-Skill Upgrade Pattern

## Khi nào dùng
Khi cần nâng cấp 1 production module (analytics, bot, pipeline) bằng cách tận dụng các class-level skills có sẵn trong skill library, thay vì code từ đầu hoặc chỉ patch lẻ tẻ.

## Giá trị
- Mỗi class-level skill chứa 1 design pattern đã được verification
- Phối hợp 3-5 skills → module production-ready với chống ảo giác built-in
- Verification loop tự động catch lỗi structure trước khi chạy thật

## Workflow (5 bước)

### Bước 1: Load skill library
```python
# Load tất cả skills liên quan đến class của module
skill_view('ecc-market-research')      # output format template
skill_view('fact-checker')             # rating system chống ảo giác
skill_view('ecc-deep-research')        # sub-question workflow
skill_view('harness-engineering')      # verification loop + progress tracker
skill_view('superpowers')              # incremental build pattern
```

### Bước 2: Map skill → class
Module cần nâng cấp thường có N classes. Với mỗi class:

| Skill Pattern | Áp dụng cho class | Tác dụng |
|--------------|-------------------|----------|
| Output format (ecc-market-research) | MarketAnalyzer, KPIDashboard | Exec summary → Findings → Implications → Risks → Rec → Sources |
| Fact-checker rating (fact-checker) | SentimentMiner, MarketAnalyzer | ✅/🟡/🔄/🟠/❌/❓ cho từng claim |
| Sub-question workflow (ecc-deep-research) | TrendForecaster, MarketAnalyzer | Break topic → 3-5 queries → multi-source → synthesize |
| Verification loop (harness-engineering) | ALL classes | Auto-check output structure trước khi deliver |
| Progress tracker (harness-engineering) | Pipeline wrapper | Checkpoint persistence for resume |
| /plan → /build → /verify (superpowers) | Implementation sequence | Incremental, each class verified before next |

### Bước 3: Patch incremental — 1 class at a time
```python
todo = [
    {"id": "1", "content": "Patch ClassA — output format + fact/inference/rec", "status": "in_progress"},
    {"id": "2", "content": "Patch ClassB — fact-checker rating system", "status": "pending"},
    {"id": "3", "content": "Add VerificationLoop + ProgressTracker", "status": "pending"},
]
```

### Bước 4: Verify after each patch
```python
python -c "import module; test_methods(); print('✅ OK')"
```
Patches produce lint output automatically — check for errors.

### Bước 5: Tổng hợp test
```python
# Test all classes instantiate, all methods dispatch, edge cases
an = module.Analytics()
assert an.run('market', 'test', industry='tech')
assert an.run('unknown', 'test').startswith('❌')
```

## Nguyên tắc chống ảo giác (bắt buộc cho mọi class)
1. Mọi số liệu đều có **rating** (✅ verified / 🟡 partial / 🔄 unverified / ❓ unknown)
2. Phân biệt **fact** vs **inference** vs **recommendation** rõ ràng
3. Không tự sinh nội dung generic khi thiếu data — nói thẳng "không đủ dữ liệu"
4. Methodology section trong mỗi report — ghi rõ đã search gì, bao nhiêu nguồn
5. Verification loop check structural integrity trước khi deliver

## Ví dụ thực tế
Session Jul 2026: analytics.py v1 → v2.0 (750 → 1395 dòng)
- 5 classes được patch: MarketAnalyzer, SentimentMiner, TrendForecaster, KPIDashboard, VerificationLoop, ProgressTracker
- 5 skills được phối hợp: ecc-market-research, fact-checker, ecc-deep-research, harness-engineering, superpowers
- Toàn bộ chạy incremental: 1 class → verify → next class → verify → total verify
- Kết quả: mọi claim có rating, mọi số có nguồn, có verification loop built-in
