# Progressive Playwright DOM Debugging

Khi `book_flight` thất bại, cách debug nhanh nhất là viết các script độc lập tăng dần độ phức tạp.

## Pattern: 5 script progression

### 1. `debug_book.py` — Load page, dump ALL DOM info
```python
# Navigate → wait for render → dump what's visible
# Answer: does the page render? Is the element there at all?
from playwright.async_api import async_playwright...

body = await page.inner_text("body")
# Check: VN1829 in body? Chọn in body?
# Then dump element matches via evaluate()
```

### 2. `debug_click.py` — Find the exact DOM hierarchy
```python
# querySelectorAll + evaluate to find WHERE the target is
# TreeWalker to navigate elements
# Answer: what's the exact tag/class/parent chain?
hierarchy = await page.evaluate("""() => {
    const walker = document.createTreeWalker(document.body, 4);
    let node;
    while (node = walker.nextNode()) {
        if (node.textContent.trim() === 'VN1829') {
            // walk up 12 levels of parentElement
        }
    }
}""")
```

### 3. `debug_click2.py` — Find ALL interactive elements
```python
# Find every element that says "Chọn"
# Check: button? div? span? a?
all_els = document.querySelectorAll('*');
for (const el of all_els) {
    if (el.innerText.includes('Chọn') && el.children.length === 0) {
        // dump tag, class, parent class, position
    }
}
```

### 4. `debug_click3.py` — Try the click + check what happens
```python
# Now we know the structure: div.air-item > span "Chọn"
# Attempt click, then dump page state after click
clicked = await page.evaluate("""
    const items = document.querySelectorAll('div.air-item');
    for (const item of items) {
        if (item.innerText.includes('VN1829')) {
            const spans = item.querySelectorAll('span');
            for (const s of spans) {
                if (s.innerText.trim() === 'Chọn') { s.click(); return true; }
            }
        }
    }
""")
# After click: what inputs appear?
form = await page.evaluate("""() => {
    return document.querySelectorAll('input').map(i => ({
        name: i.name, placeholder: i.placeholder, type: i.type
    }));
}""")
```

### 5. `debug_click4.py` — Full fill + submit
```python
# Fill all fields, then find submit button
# Answer: what's the form field names? Where's the submit button?
```

## Key Lessons from abtrip.vn debugging

1. **querySelectorAll('button') returns 0** — abtrip.vn uses `<SPAN>` inside `<DIV.action-button>`, not real `<button>` elements
2. **Ant Design forms use `input[name]`** — field names like `passengers.adults.0.firstName`
3. **Gender radio must click `<label>`, not `<input>`** — `label:has(input[name="...gender"])`
4. **Always dump ALL inputs** — don't assume field names from memory
5. **Next.js SSR needs 6-9 seconds** — retry loop with `wait_for_timeout(3000)`
6. **`page.evaluate(js, arg)` only accepts 1 arg** — destructure via `(args) => { const [a, b] = args; }`
7. **Always dump ALL buttons vs querySelectorAll('button')** — compare count: some pages have 0 real `<button>` elements but many clickable `<span>`/`<div>` with listeners
8. **Debug in 5-script progression:** 1) render check → 2) DOM hierarchy → 3) find interactive elements → 4) click + form → 5) full fill + submit. Never skip to step 5.
