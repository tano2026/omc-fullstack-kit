# Playwright DOM Debug Methodology for abtrip.vn (Next.js + Ant Design)

## The Core Problem

abtrip.vn uses Next.js (React Server Components) + Ant Design (React UI library). This means:
- DOM structure is **not static HTML** — it changes between builds
- React synthetic events mean `element.click()` in JS may NOT propagate to React state
- Form inputs have Ant Design wrapper layers, not standard `<form>` structures
- Buttons may not be `<button>` tags — they can be `<span>`, `<div>`, `<a>` with styled "button" appearance

## The Debug Flow That Works

### Phase 1: Check What EXISTS

Never assume DOM structure. Verify first:

```python
# Check if "Chọn" buttons exist and what tags they use
all_selectors = await page.evaluate("""() => {
    const results = [];
    const all = document.querySelectorAll('*');
    for (const el of all) {
        const t = (el.innerText || '').trim();
        if (t.startsWith('Chọn') || t === 'Chọn') {
            results.push({
                tag: el.tagName,
                has_children: el.children.length,
                class: (el.className || '').slice(0, 150),
                id: el.id || '',
                onclick: el.getAttribute('onclick') || '',
                role: el.getAttribute('role') || '',
                cursor: window.getComputedStyle(el).cursor,
                rect_visible: el.getBoundingClientRect().width > 0,
                parent_text: ((el.parentElement?.innerText) || '').slice(0, 150)
            });
            if (results.length >= 3) break;
        }
    }
    return results;
}""")
```

Key insight: `querySelectorAll('button')` returning 0 means buttons are NOT `<button>` tags.

### Phase 2: Trace the DOM Hierarchy from a Known Text Node

Once you find a flight number like `VN1829` as a text node, walk UP the hierarchy:

```python
hierarchy = await page.evaluate("""() => {
    const walker = document.createTreeWalker(document.body, 4);
    let node;
    while (node = walker.nextNode()) {
        if (node.textContent.trim() === 'VN1829') {
            let p = node.parentElement;
            const chain = [];
            for (let d = 0; d < 12 && p; d++) {
                chain.push({
                    tag: p.tagName,
                    class: (p.className || '').slice(0, 200),
                    children_count: p.children.length,
                    child_0_tag: p.children[0]?.tagName || '',
                    child_1_tag: p.children[1]?.tagName || ''
                });
                p = p.parentElement;
            }
            return chain;
        }
    }
    return null;
}""")
```

This reveals the full ancestor chain:
```
SPAN.flight-num → DIV.airline-logo → DIV.flight-sum → ... → DIV.air-item → DIV.air-options
```

### Phase 3: Find the Action Target

Once you know the hierarchy, find the actionable element relative to the flight number:

```python
# Method: find SPAN with "Chọn" text inside the same air-item that contains the flight number
click_js = """
(fn) => {
    const items = document.querySelectorAll('div.air-item');
    for (const item of items) {
        if (item.innerText.includes(fn)) {
            const spans = item.querySelectorAll('span');
            for (const s of spans) {
                if (s.innerText.trim() === 'Chọn') {
                    s.click();
                    return true;
                }
            }
        }
    }
    return false;
}
"""
clicked = await page.evaluate(click_js, flight_number)
```

### Phase 4: Verify After Click

After clicking, wait and check what appeared:

```python
await page.wait_for_timeout(5000)

# Check form fields
form = await page.evaluate("""() => {
    const inputs = document.querySelectorAll('input');
    return Array.from(inputs).map(i => ({
        name: i.name || '',
        placeholder: i.placeholder || '',
        type: i.type || ''
    }));
}""")
print(json.dumps(form, ensure_ascii=False, indent=2))
```

### Phase 5: Test Form Fill Independently

Before integrating into the book flow, test fill + submit separately:

```python
# Fill each field
el = await page.query_selector('input[name="passengers.adults.0.firstName"]')
if el: await el.fill("NGUYEN")

# Gender — click LABEL, NOT the radio input directly
glabels = await page.query_selector_all('label:has(input[name="passengers.adults.0.gender"])')
for gl in glabels:
    text = (await gl.inner_text()).strip().lower()
    if text == "nam":
        await gl.click()
        break

# Submit
submit = await page.query_selector('button:has(span:text("Đặt vé"))')
if submit:
    await submit.scroll_into_view_if_needed()
    await submit.click()
```

## Key Pitfalls Discovered

1. **`querySelectorAll('button')` trả về 0** — abtrip.vn uses `<SPAN>` inside `<DIV.action-button>` for "Chọn", not `<button>`. The actual submit button IS a `<button>` though.

2. **`page.evaluate()` only accepts 1 arg** — To pass multiple values, use destructuring: `(args) => { const [el, fn] = args; }` with `[element, string]`

3. **Gender via radio inputs** — Click the `<label>` wrapping the radio, not the `<input type="radio">` directly. Labels are visible and clickable.

4. **DOB format** — abtrip.vn expects `dd/mm/yyyy`, not `yyyy-mm-dd` or ISO format.

5. **Flight value pipe-separated** — The tool returns `VN1833|SGN|PQC|...|1728000`, need `.split("|")[0]`

6. **Never trust page load after 3s** — abtrip.vn Next.js SSR can take 6-9s for route with many flights. Use a loop polling `body.innerText` for "Có " and " chuyến bay" as ready indicator.

## When To Use This Methodology

- Any time `book_flight()` returns "Không tìm thấy chuyến bay" despite the flight existing on the page
- After abtrip.vn deploys a new version (DOM structure changes)
- When debugging new route types that might use different layouts (UIH→SGN uses older layout, HAN→DAD uses newer)
- When form fields change names (Ant Design version upgrades)
