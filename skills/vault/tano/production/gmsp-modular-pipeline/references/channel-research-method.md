# Channel Research — YouTube Competitive Analysis

## Channels Researched (2026-07-15)

### The Hidden Self (@thehiddenself.pocast)
- **Subs:** 87.9K | **Videos:** 444
- **Bio:** "Nơi sẽ có những sự thật mà xã hội không muốn cho bạn biết"
- **Topic clusters:** Hidden Finance (40%), Dark Psychology (30%), Destiny (15%)
- **Top hook:** Capital Accumulation — The Secret The Elite Doesn't Want You To Know (346K views)
- **Style:** Brutal truth hook, expose hidden system, direct "mày"
- **GMSP fit:** PTBT + Cổ Kim domains
- **Full analysis:** `production/gmsp-modular-pipeline/references/hidden-self-research.md`

### The Hidden Path (@TheHiddenPath)
- **Subs:** 133 | **Topics:** Taoism, Lao Tzu, Stoicism
- **Style:** Question hook → Ancient wisdom → Modern application
- **Sample:** "Transformation Begins With Letting Go" (196 views, 12:52)
- **GMSP fit:** Cổ Kim domain

### Similar Competitors Found
- Clarity & Zen (~55K/video) — Taoist
- Buddhism Flow (~69K/video) — Buddhist
- The Inner Way (~47K/video) — Philosophy
- (Hidden Self English — @The-HiddenSelf, 22.4K, Dark Psychology + Machiavellian)

## Research Method

1. `youtube-research-agent` skill → browser_navigate to channel
2. Click "Popular" tab → snapshot video titles + views
3. web_search for additional video data
4. Cluster topics, analyze hook patterns
5. Map to GMSP framework (Tử Vi + Thuật + Định luật + Tâm lý)
6. Propose 5-7 GMSP topics per channel

## Browser Note

YouTube uses heavy Shadow DOM — standard querySelector does NOT work.
Use accessibility snapshot (browser_snapshot) to read heading texts from the page tree.
Click ref=e41 for "Popular" tab (top videos by views).
