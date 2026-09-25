# Playwright `page.evaluate` Pitfalls — abtrip.vn Context

## 1. Nested f-string + `\"` Escaping → SyntaxError

### The Bug

```python
# ❌ BROKEN — causes "SyntaxError: Unexpected token '('"
def _try_flight_select(p_page, fn):
    return p_page.evaluate(f"""() => {{
        ...
        if (el.innerText.includes(fn)) {{ ... }}
        ...
    }}(""", fn)
```

When `fn` = `"VN1350"`, the f-string produces:

```javascript
(function() { ... })("VN1350")
```

But the `""` inside the f-string Python conflicting with JS escaping causes:
```
SyntaxError: Unexpected token '('
```

### The Fix

```python
# ✅ WORKS — pass fn as a separate evaluate argument
async def _try_flight_select(p_page, fn):
    js = """
    (fn) => {
        const cards = document.querySelectorAll(...);
        for (const card of cards) {
            if (card.innerText.includes(fn) && card.innerText.includes('Chọn')) {
                ...
            }
        }
        return false;
    }
    """
    return await p_page.evaluate(js, fn)
```

**Rule:** Playwright `page.evaluate(expression, arg)` accepts exactly 1 `arg` parameter. Use a plain JS template with the `(arg_name) => { ... }` pattern and pass dynamic data as the second argument.

Never embed variables via Python f-string `f"...{var}..."` when the JS code contains `{{` / `}}` (curly braces for JS blocks). The result is an unreadable mess that's nearly impossible to debug.

## 2. Multi-value Passing

Playwright `evaluate(expression, arg)` only accepts **one argument**. To pass multiple values:

```python
# ✅ CORRECT — destructure in JS
text = await page.evaluate(
    """(args) => {
        const [el, flight_number] = args;
        return el.textContent;
    }""",
    [element_handle, flight_number]
)
```

```python
# ❌ WRONG — Playwright will error
text = await page.evaluate(
    "(el, fn) => el.textContent",
    element_handle, flight_number  # Only first arg is passed!
)
```

## 3. Return Value Gotchas

- **ElementHandle returns**: `page.evaluate()` does NOT return ElementHandle objects — it returns their serialised properties. Use `page.evaluate_handle()` if you need a handle back.
- **DOM elements in return**: If the JS returns a DOM element, Playwright serialises it as `{}`. Use `element.innerText`, `element.getAttribute(...)`, etc. in the JS side.
- **Promise results**: `page.evaluate()` auto-awaits Promises. If the JS function is `async`, Playwright waits for resolution before returning.

## When This Occurred

This bug was hit in production on `hotline.abtrip.vn` (June 2026) during booking attempts. The `_try_flight_select` function in `abtrip_browser.py` used a triple-quoted f-string with `\"` escape sequences to embed the flight number. The nested escaping became malformed at runtime, causing all booking attempts to fail with:

```json
{"success": false, "error": "Lỗi đặt chỗ Playwright: Page.evaluate: SyntaxError: Unexpected token '('"}
```

Fixed by refactoring to use `page.evaluate(js, fn)` with a plain string and separate argument.
