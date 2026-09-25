# Typography

The compiler **pre-bundles a fixed set** of fonts (the table below) — write one of those families in `font-family` and it renders deterministically, offline, with no setup and no warning. A name _outside_ that set is **not silently dropped**: if it's a real Google font the compiler fetches it from Google Fonts at **build time** and embeds it, so it _does_ render — but that implicit path (a) trips a `font_family_without_font_face` lint warning, and (b) is **fail-closed in distributed/cloud renders** — if Google is unreachable the render _errors_ rather than quietly substituting a system font. Beyond that, **local renders auto-capture fonts you actually have**: a family installed on your machine, a local `@font-face` path, or an external CDN stylesheet all get compressed to woff2 and inlined at build time. So a name on **neither** the bundle **nor** Google Fonts only truly falls back to a generic system font when it's _also_ not installed locally and not declared in an `@font-face` — and even that logs a compiler warning. **One caveat**: distributed/cloud (Lambda) renders disable system-font capture, so don't rely on a locally-installed-only font for those. So don't assume an un-bundled display name will Just Work: for anything that must render predictably, pick a bundled family below **or embed your own `@font-face`** (see "Finding Fonts").

## Contents

- Fonts that embed (auto-resolve)
- Banned fonts
- Guardrails
- What you do not do without being told
- Finding fonts
- Selection thinking
- Similar-font pairing
- Dark backgrounds
- OpenType features for data
- Vietnamese font recommendations

## Fonts That Embed (auto-resolve)

These **18 families** are the ones the renderer **pre-bundles** — embedded as local data URIs with no network fetch, so they render offline and deterministically with zero setup, no lint warning, and no fail-closed fetch risk. Write any of them as a `font-family` and it renders; **only the listed weights exist** (asking for a weight a family doesn't ship gives a synthetic/fallback weight, not a real cut). (Any _other_ real Google font still works via the implicit build-time fetch described in the intro — but only these render with none of those caveats.)

| Family            | Weights         | Role              |
| ----------------- | --------------- | ----------------- |
| Inter             | 400 · 700 · 900 | sans (body/UI)    |
| Roboto            | 400 · 700 · 900 | sans              |
| Open Sans         | 400 · 700       | sans              |
| Lato              | 400 · 700 · 900 | sans              |
| Nunito            | 400 · 700 · 900 | sans (rounded)    |
| Montserrat        | 400 · 700 · 900 | geometric sans    |
| Poppins           | 400 · 700 · 900 | geometric sans    |
| Outfit            | 400 · 700 · 900 | geometric sans    |
| Oswald            | 400 · 700       | condensed sans    |
| **League Gothic** | **400 only**    | condensed display |
| **Archivo Black** | **400 only**    | heavy display     |
| Playfair Display  | 400 · 700 · 900 | serif (display)   |
| EB Garamond       | 400 · 700       | serif (text)      |
| Space Mono        | 400 · 700       | mono              |
| IBM Plex Mono     | 400 · 700       | mono              |
| JetBrains Mono    | 400 · 700       | mono              |
| Source Code Pro   | 400 · 700       | mono              |
| Noto Sans JP      | 400 · 700       | CJK (Japanese)    |

> ⚠ **League Gothic and Archivo Black ship weight 400 ONLY** — they are already heavy/condensed display faces. Do not request `font-weight: 700/900` on them.

**Aliases** — these common names resolve to an embedded family, so you may safely write them: `Helvetica Neue` / `Helvetica` / `Arial` → Inter · `Futura` / `DIN Alternate` / `Arial Black` → Montserrat · `Bebas Neue` → League Gothic · `Segoe UI` → Roboto · `Courier New` / `Courier` → JetBrains Mono · `Garamond` → EB Garamond. (This is why a "safe" `Helvetica Neue` stack always renders — it maps to embedded Inter.)

**Reconciling with the Banned list below:** several embedded families (Inter, Roboto, Open Sans, Lato, Nunito, Poppins, Outfit, Playfair Display, EB Garamond) are _also_ on the Banned monoculture list — they render fine but read as generic. The families that are **embedded AND not banned** — your safe-and-distinctive picks — are: **Montserrat, Oswald, League Gothic, Archivo Black, Space Mono, IBM Plex Mono, JetBrains Mono, Source Code Pro, Noto Sans JP**. Reach for these (or a non-bundled font you've confirmed via the Finding-Fonts step). A non-bundled name isn't guaranteed-broken — a real Google font is auto-fetched and embedded — but it carries a lint warning and a fail-closed fetch in cloud renders, so for anything that must render predictably, **embed it yourself via `@font-face`** (see "Finding Fonts") rather than relying on the implicit fetch.

## Banned

Training-data defaults that every LLM reaches for. These produce monoculture across compositions.

Inter, Roboto, Open Sans, Noto Sans, Arimo, Lato, Source Sans, PT Sans, Nunito, Poppins, Outfit, Sora, Playfair Display, Cormorant Garamond, Bodoni Moda, EB Garamond, Cinzel, Prata, Syne

**Syne in particular** is the most overused "distinctive" display font. It is an instant AI design tell.

## Guardrails

You know these rules but you violate them. Stop.

- **Don't pair two sans-serifs.** You do this constantly — one for headlines, one for body. Cross the boundary: serif + sans, or sans + mono.
- **One expressive font per scene.** You pick two interesting fonts trying to make it "better." One performs, one recedes.
- **Weight contrast must be extreme.** You default to 400 vs 700. Video needs 300 vs 900. The difference must be visible in motion at a glance.
- **Video sizes, not web sizes.** Full-screen viewing (YouTube / website embed): body 20px minimum, headlines 60px+, data labels 16px. **In-feed viewing** (destination = X / LinkedIn / Instagram feed — the video plays small inside a scrolling feed, so scale up — body ≥32px, headlines ≥90px, data labels ≥24px (first-pass values; calibrate against real renders)). You will try to use 14px. Don't.

## What You Don't Do Without Being Told

- **Tension should mean something.** Don't pattern-match pairings. Ask WHY these two fonts disagree. The pairing should embody the content's contradiction — mechanical vs human, public vs private, institutional vs personal. If you can't articulate the tension, it's arbitrary.
- **Register switching.** Assign different fonts to different communicative modes — one voice for statements, another for data, another for attribution. Not hierarchy on a page. Voices in a conversation.
- **Tension can live inside a single font.** A font that looks familiar but is secretly strange creates tension with the viewer's expectations, not with another font.
- **One variable changed = dramatic contrast.** Same letterforms, monospaced vs proportional. Same family at different optical sizes. Changing only rhythm while everything else stays constant.
- **Double personality works.** Two expressive fonts can coexist if they share an attitude (both irreverent, both precise) even when their forms are completely different.
- **Time is hierarchy.** The first element to appear is the most important. In video, sequence replaces position.
- **Motion is typography.** How a word enters carries as much meaning as the font. A 0.1s slam vs a 2s fade — same font, completely different message.
- **Fixed reading time.** 3 seconds on screen = must be readable in 2. Fewer words, larger type.
- **Tracking tighter than web.** -0.03em to -0.05em on display sizes. Video encoding compresses letter detail.

## Finding Fonts

Don't default to what you know. If the content is luxury, a grotesque sans might create more tension than the expected Didone serif. Decide the register first, then search.

Run with `curl -s 'https://fonts.google.com/metadata/fonts' > /tmp/gfonts.json && python3 /tmp/fontquery.py /tmp/gfonts.json`.

The fontquery.py script (reference original for exact script) accepts a Google Fonts metadata JSON, filters out banned/prefixed families, and prints randomized top picks per category: Trending Sans, Trending Serif, Monospace, Impact & Condensed, Script & Handwriting.

Five categories: trending sans, trending serif, monospace, impact/condensed, script/handwriting. All dynamically filtered from Google Fonts metadata — no hardcoded font names. Cross classification boundaries when pairing.

## Selection Thinking

Don't pick fonts by category reflex (editorial → serif, tech → mono, modern → geometric sans). That's pattern matching, not design.

1. **Name the register.** What voice is the content speaking in? Institutional authority? Personal confession? Technical precision? Casual irreverence? The register narrows the field more than the category.
2. **Think physically.** Imagine the font as a physical object the brand could ship — a museum exhibit caption, a hand-painted shop sign, a 1970s mainframe terminal manual, a fabric label inside a coat, a children's book printed on cheap newsprint, a tax form. Whichever physical object fits the register is pointing at the right _kind_ of typeface.
3. **Reject your first instinct.** The first font that feels right is usually your training-data default for that register. If you picked it last time too, find something else.
4. **Cross-check the assumption.** An editorial brief does NOT need a serif. A technical brief does NOT need a sans. A children's product does NOT need a rounded display font. The most distinctive choice often contradicts the category expectation.

## Similar-Font Pairing

Never pair two fonts that are similar but not identical — two geometric sans-serifs, two transitional serifs, two humanist sans. They create visual friction without clear hierarchy. The viewer senses something is "off" but can't articulate it. Either use one font at two weights, or pair fonts that contrast on multiple axes: serif + sans, condensed + wide, geometric + humanist.

## Dark Backgrounds

Light text on dark backgrounds creates two optical illusions you need to compensate for:

- **Increased apparent weight.** Light-on-dark reads heavier than dark-on-light at the same `font-weight`. Use 350 instead of 400 for body text. Headlines are less affected because size compensates.
- **Tighter apparent spacing.** Light halos around letterforms reduce perceived gaps. Increase `line-height` by 0.05-0.1 beyond your light-background value. For display sizes, add 0.01em `letter-spacing` to counteract.

## OpenType Features for Data

Most fonts ship with OpenType features that are off by default. Turn them on for data compositions:

```css
/* Tabular numbers — digits align vertically in columns */
.stat-value,
.timer,
.data-column {
  font-variant-numeric: tabular-nums;
}

/* Diagonal fractions — renders 1/2 as ½ */
.recipe-amount,
.ratio {
  font-variant-numeric: diagonal-fractions;
}

/* Small caps for abbreviations — less visual shouting */
.abbreviation,
.unit {
  font-variant-caps: all-small-caps;
}

/* Disable ligatures in code — fi, fl, ffi should stay separate */
code,
.code {
  font-variant-ligatures: none;
}
```

`tabular-nums` is essential any time numbers are stacked vertically — stat callouts, timers, scoreboards, data tables. Without it, digits have proportional widths and columns don't align.

## Vietnamese Font Recommendations

For Vietnamese-language videos (using đ, ă, â, ê, ô, ơ, ư and tone marks), not all bundled fonts handle the diacritics well.

### Recommended Pairing for Podcast / Narrated Videos

| Role                | Font               | Why                          |
| ------------------- | ------------------ | ---------------------------- |
| Headline / Quote    | Playfair Display   | Serif handles diacritics well; Dark Academia aesthetic; bundled in HyperFrames |
| Body / Scene tags   | Inter              | Clean sans, readable at small sizes, good Vietnamese support; bundled |
| CTA / Brand text    | Inter              | Caps text looks clean; UPPERCASE works well |

This pairing uses a "banned" display font (Playfair Display) with a generic body font (Inter) intentionally — the serif+sans contrast satisfies the guardrails, and for Vietnamese, predictable readability and proper diacritic rendering take priority over font uniqueness.

### Fonts to Avoid for Vietnamese

- **Condensed fonts** (League Gothic, Oswald): diacritics get clipped at small sizes
- **Fonts with very tight ascenders/descenders**: tone marks (á, ạ, ả, ã) collide with line above
- **All-caps display fonts**: Vietnamese tone marks on uppercase vowels look cramped

### Check: Does a Font Support Vietnamese?

If choosing a non-bundled font, verify Vietnamese subset support:

```bash
curl -s 'https://fonts.google.com/metadata/fonts' | python3 -c "
import json,sys
f = json.load(sys.stdin)['familyMetadataList']
query = ' | '.join(sys.argv[1:]) if sys.argv[1:] else 'Your Font Name'
for ff in f:
    if query.lower() in ff['family'].lower():
        has_vn = 'vietnamese' in (ff.get('subsets') or [])
        print(f\"{ff['family']}: Vietnamese={'YES' if has_vn else 'NO'} ({ff.get('subsets',[])})\")
"
```