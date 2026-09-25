---
name: remotion
description: "Vibe Toolkit skill: Remotion - Video bang React + Render Ra MP4 (49.9k stars)"
---

# Remotion — Video Bằng React + Render Ra MP4 (49.9k⭐)

**Repo:** github.com/remotion-dev/remotion | Remotion License*
**Stars:** 49.9k | npm: 900k installs/tháng
**Website:** remotion.dev

*Free cho open-source/personal. Trả phí cho commercial production use.

---

## Cài & Setup

```bash
npx create-video@latest my-video
cd my-video
npm install
npm start  # preview tại localhost:3000
```

**Manual setup (recommended for brand projects):**
```bash
mkdir -p brand/{vertical}/remotion/src public out
```

Create minimal `package.json`:
```json
{
  "dependencies": { "react": "^19.0.0", "react-dom": "^19.0.0", "remotion": "^4.0.0", "@remotion/cli": "^4.0.0" }
}
```

Then `npm install`.

## Component Architecture — Brand Video System

Remotion fits into a 3-component brand architecture for video production:

```
brand.json (colors, durations, style tokens)
     |
     +-- <Intro />    -> 3.5s animated brand reveal
     +-- <Outro />    -> 5s CTA + subscribe
     +-- <Thumbnail /> -> 1920x1080 still image
```

### Entry point — `src/index.tsx`
```tsx
import { registerRoot } from "remotion";
import { Root } from "./Root";
registerRoot(Root);
```

### Composition wiring — `src/Root.tsx`
```tsx
import { Composition } from "remotion";
import { Intro } from "./Intro";
import { brand } from "./brand";

export const Root = () => (
  <>
    <Composition id="Intro" component={Intro}
      durationInFrames={Math.round(3.5 * 30)}  fps={30}
      width={1920} height={1080} />
    <Composition id="Thumbnail" component={Thumbnail}
      durationInFrames={1} fps={30}
      width={1920} height={1080} />
  </>
);
```

### Brand config — `src/brand.ts` (**critical pattern**)
```tsx
// OK: inline TypeScript constants
export const brand = {
  colors: { primary: "#1a6b3c", accent: "#d4a843", bg: "#0d1b11" },
  intro: { duration_seconds: 3.5, fps: 30 },
};

// DO NOT do this: fs/path won't work in browser bundle
// import fs from "fs";
// const brand = JSON.parse(fs.readFileSync("brand.json"));
// -> ReferenceError: fs is not defined
```

**Static assets** (images, fonts) go in `public/` directory, referenced via `staticFile("logo.png")`.

## Animation Patterns

### Intro — Brand Reveal (3.5s ~ 105 frames @ 30fps)

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate, useVideoConfig, Img, staticFile } from "remotion";

export const Intro = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();  // REQUIRED for fps-based timing

  // Logo: scale 0 -> 1 in 1.5s (frames 0-45)
  const logoScale = interpolate(frame, [0, 45], [0, 1], { extrapolateRight: "clamp" });

  // Tagline: fade in after logo starts
  const taglineOpacity = interpolate(frame, [15, 45], [0, 1], { extrapolateRight: "clamp" });

  // Title: slide up 60px + fade (frames 30-70)
  const titleY = interpolate(frame, [30, 70], [60, 0], { extrapolateRight: "clamp" });
  const titleOpacity = interpolate(frame, [30, 70], [0, 1], { extrapolateRight: "clamp" });

  // Background pulse
  const bgPulse = interpolate(frame, [0, fps * 3.5], [1, 1.02], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0d1b11", overflow: "hidden" }}>
      <div style={{
        position: "absolute", inset: 0,
        background: "radial-gradient(ellipse at 50% 40%, #0f4a28 0%, #0d1b11 70%)",
        transform: `scale(${bgPulse})`,
      }} />
      <Img src={staticFile("logo.png")}
        style={{ position: "absolute", top: "50%", left: "50%",
          transform: `translate(-50%, -20%) scale(${logoScale})`, width: 180, height: 180 }} />
      <div style={{ position: "absolute", top: "52%", left: "50%", transform: "translateX(-50%)",
        opacity: taglineOpacity, color: "#d4a843", fontSize: 28, letterSpacing: 6 }}>
        {brand.tagline}
      </div>
      <div style={{ position: "absolute", bottom: "22%", left: "50%",
        transform: `translateX(-50%) translateY(${titleY}px)`, opacity: titleOpacity }}>
        <span style={{ color: "#ffffff", fontSize: 48, fontWeight: 700 }}>Kenh Name</span>
      </div>
    </AbsoluteFill>
  );
};
```

### Outro — CTA (5s ~ 150 frames)

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig, Img, staticFile } from "remotion";

export const Outro = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Logo fade out
  const logoOpacity = interpolate(frame, [0, 30], [1, 0.3], { extrapolateRight: "clamp" });

  // CTA spring bounce (starts at frame 15)
  const ctaSpring = spring({ frame: frame - 15, fps, config: { damping: 12, mass: 0.5, stiffness: 100 } });
  const ctaY = interpolate(ctaSpring, [0, 1], [80, 0]);
  const ctaOpacity = interpolate(frame, [15, 45], [0, 1]);

  // Social handle fade
  const socialOpacity = interpolate(frame, [45, 75], [0, 1]);
  // ...
};
```

### Thumbnail — Still Image (1920x1080)

```tsx
import { AbsoluteFill, Img, staticFile } from "remotion";

export const Thumbnail = ({ title = "Episode", imagePath = staticFile("bg.jpg") }) => (
  <AbsoluteFill style={{ width: 1920, height: 1080, overflow: "hidden" }}>
    <Img src={imagePath} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
    <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: "40%",
      background: "linear-gradient(transparent, #0d1b11)", opacity: 0.75 }} />
    <div style={{ position: "absolute", top: 24, right: 24, background: "#1a6b3c", padding: "10px 20px", borderRadius: 6 }}>
      <span style={{ color: "white", fontSize: 24, fontWeight: 700 }}>Kenh Name</span>
    </div>
    <div style={{ position: "absolute", bottom: 60, left: 40, right: 40 }}>
      <div style={{ color: "white", fontSize: 72, fontWeight: 900, textShadow: "2px 2px 8px rgba(0,0,0,0.8)" }}>
        {title}
      </div>
      <div style={{ marginTop: 16, width: 80, height: 4, background: "#d4a843", borderRadius: 2 }} />
    </div>
  </AbsoluteFill>
);
```

## Audio Component Pattern

Use Remotion's `<Audio>` component for voiceover/BGM — it's frame-precise synced natively:

```tsx
import {AbsoluteFill, Audio, staticFile, Sequence, useCurrentFrame, Img} from 'remotion';

export const AudioDemo = () => {
  const fps = 30;
  const audioDuration = 24.5; // seconds
  const totalFrames = Math.round(audioDuration * fps);

  return (
    <AbsoluteFill style={{backgroundColor: '#0d0d0d'}}>
      {/* Audio track — file must be in public/ */}
      <Audio src={staticFile("voiceover.mp3")} />

      {/* Visual — show an image throughout */}
      <Img src={staticFile("frame-001.png")}
        style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </AbsoluteFill>
  );
};
```

Register the composition in Root.tsx:
```tsx
<Composition
  id="audio-demo"
  component={AudioDemo}
  durationInFrames={Math.round(24.5 * 30)} // 24.5s @ 30fps
  fps={30}
  width={1920}
  height={1080}
/>
```

Copy audio to public/ before render:
```bash
cp /path/to/voiceover.mp3 public/
```

## Render Commands

```bash
# Video
npx remotion render src/index.tsx Intro out/intro.mp4
npx remotion render src/index.tsx Outro out/outro.mp4

# Still image
npx remotion still src/index.tsx Thumbnail out/thumbnail.png

# Audio demo
npx remotion render audio-demo out/audio_demo.mp4

# Custom
npx remotion render MyVideo out/video.mp4 --fps=60 --width=1920 --height=1080
```

## Pitfalls

### Windows: npx remotion fails — space in username path
On Windows, `npx remotion render` can fail with cryptic errors if the username contains spaces (e.g. `C:\Users\Nguyen Ngoc Tan\`). Workaround:

1. Install `@remotion/cli` as a dev dependency:
```bash
npm install --save-dev @remotion/cli
```

2. Run via the local binary instead of npx:
```bash
node_modules/.bin/remotion.cmd render src/index.tsx MyVideo out/video.mp4
# OR via npm script:
npx --no-install remotion render src/index.tsx MyVideo out/video.mp4
```

Add to `package.json`:
```json
"scripts": {
  "render": "node_modules/.bin/remotion.cmd render src/index.tsx"
}
```
Then `npm run render MyVideo out/video.mp4`.

### render-demo.js (Node API) needs absolute paths
When using the Node.js API (`@remotion/renderer`), all paths must be absolute — `path.resolve()` your `serveUrl` and `outputLocation`.

### NO Node.js built-ins in components
Remotion bundles your code for Chrome headless (browser runtime). `fs`, `path`, `os` do NOT exist there. Always use:
- **Brand config:** inline TypeScript constants, NOT `JSON.parse(fs.readFileSync(...))`
- **Assets:** `staticFile("filename.png")` -- files must be in `public/`
- **Dynamic data:** composition `defaultProps` or input props

### useVideoConfig for fps
If your animation uses `fps`, always call:
```tsx
const { fps } = useVideoConfig();
```
Without it `fps` is undefined -> render crash on frame 2.

### create-video on existing directory fails
`npx create-video@latest --template blank .` fails with "Something already exists" on existing dirs. Use a fresh empty directory.

### Render time estimates
- Intro (3.5s, 105 frames): ~30s bundle + ~15s render = ~45s
- Outro (5s, 150 frames): ~30-45s
- Thumbnail (still): ~30s
First run downloads Chrome Headless Shell (~113 MB).

## When to Use Remotion vs Alternatives

| Situation | Use This |
|-----------|----------|
| Know React | Remotion |
| Brand intro/outro animation | **Remotion** |
| Complex text animations | Remotion |
| Quick simple video | html-video |
| No coding | HyperFrames |
| Data-driven video | Remotion |
| Long-form body (20 min image-based) | **FFmpeg** (faster for bulk) |
| Audio sync (voiceover demo/prototype) | HyperFrames + FFmpeg mux — render video (5-10s) + mux audio (2s) = faster iteration |
| Audio sync (production, frame-precise) | **Remotion** — `<Audio>` component, native sync, but dev loop ~3m/25s clip |
| Dev iteration speed | Remotion: bundle+render slow (~3m per short clip) | HyperFrames: 5-10s render + instant mux | FFmpeg: fastest for pure image+audio |

*Note: avoid magenta/bright pink in any brand visual outputs — user strongly dislikes it.*

---

## Related Skills & References

- `references/pipeline-integration.md` — How Remotion brand assets (intro/outro/thumbnail) integrate with FFmpeg-based video pipeline (ASS subtitles, brand.json, intro/outro concat)
- `hyperframes` — HTML-based alternative for slide-based video (no React needed)
- `video-production-pipeline` — Full production workflow from topic to publish

---

*skills/remotion-skill.md | AI Vibe Toolkit | thang 7/2026*
