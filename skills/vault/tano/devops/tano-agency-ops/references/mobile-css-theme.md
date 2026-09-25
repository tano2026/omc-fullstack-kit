# Mobile CSS Theme — GMSP Brand

## Complete CSS for dark dashboard

```css
:root {
    --bg: #0D0D12;
    --bg2: #16161E;
    --bg3: #1E1E2A;
    --gold: #FFD700;
    --red: #8B0000;
    --text: #E8E6E3;
    --text2: #9C9A9B;
    --border: #2A2A3A;
    --success: #22C55E;
    --warning: #F59E0B;
    --danger: #EF4444;
    --radius: 12px;
}
```

## To customize for other brands
Replace `--gold` (primary accent) and `--red` (secondary accent). Keep bg/bg2/bg3/text/text2/border for dark theme consistency.

## Mobile patterns to always include
1. `padding-bottom: max(6px, env(safe-area-inset-bottom))` on bottom nav
2. Skeleton loading with shimmer animation
3. Toast notification (fixed bottom-center, auto-dismiss)
4. Bottom nav with 4 tabs + active state
5. Sticky header with backdrop-filter blur
6. Card-based layout (no horizontal scrolling)
7. Step pipeline as vertical list (not table)
8. Progress bar with gradient fill
9. `font-size: 15px` body text (readable on mobile)
10. All buttons have `:active { transform: scale(0.97) }` for tap feedback
