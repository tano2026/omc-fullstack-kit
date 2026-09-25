# ECC Python Testing — Nhúng vào Dev Agent

Skill gốc: `ecc-python-testing` (270 ECC skills)

## Nhúng vào _real_build() — agents/dev/adapters.py

**LLM prompt rules (thêm vào system prompt của _real_build):**
```
RULES:
- TDD: viết test trước code (file test_{tên}.py trước), sau đó code file thật
- File Python phải pass py_compile + có pytest test
- Mock external dependencies (requests, DB, API)
- Test edge cases: empty input, None, boundary
- File path trong D:/MMO Du an/<project>/
- Output JSON phải có "test_results" field
```

**Khi verify build output:**
1. Check file test_*.py tồn tại trước file chính
2. Check có `with pytest.raises()` cho error cases
3. Check có fixture cho database/external API
4. Check có parametrize cho edge cases

**Pitfalls:**
- LLM hay quên viết test trước code → dùng "TDD: viết test trước code sau" ngay đầu prompt
- LLM hay sinh file test thiếu assertion → yêu cầu "assert result == expected" trong mỗi test
