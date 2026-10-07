# Motion and interaction

Tags: `[N]` = number of independent creators who state the rule. `[1★]` = a single canonical or gap-filling source. `(std)` = a widely used standard value that does not appear in the research. Method, top-60 backers and source index: [evidence.md](evidence.md).

## Summary

- [11] Every animation needs a job you can state in one sentence: feedback, state change, hierarchy, spatial context or story pacing. Everything else stays still. The second most-cited failure is stacking effects to look impressive [7].
- [7] Acknowledge every press instantly with a pressed state, and give visible feedback in under 400ms. Slow work gets an in-place spinner or determinate progress.
- [4] Default motion: an interruptible CSS transition on `transform` and `opacity`, strong ease-out `cubic-bezier(0.16, 1, 0.3, 1)`, 150-300ms. Never linear, never `transition: all`. Springs only for direct manipulation and momentum.
- [4] Animate state changes from their spatial source instead of snapping. A marketing page spends its remaining budget on one signature story motion. Use an Apple-style scroll-scrubbed reveal only when there is a real object to reveal.
- [4] Every motion has a `prefers-reduced-motion` path that removes movement but keeps opacity and state feedback, plus a fallback for low-power devices and slow networks.

## 1. Motion must earn its place [11]

- [11] Before building an animation, write its job in one sentence. If you can't, don't build it. When you have several hero animation ideas, ship one.
- [11] Keep informational sections still. Cut motion added because it looks cool: animating every button, icon and section, confetti, shimmer or wiggle on routine controls, carousels that tell no story, decorative glass transitions.
- [11] Judge motion by how it feels on the 100th use, not the first.
- [7] Don't stack effects (glows, gradients, hover animations, video, floating shapes, WebGL/3D) to show effort. Keep an effect only if it speeds up understanding or expresses the concept. Limit heavy effects to a few sections, such as WebGL in one section only. Cut anything that performs poorly, feels pompous or breaks the page's rhythm. Ask whether it makes the product look smarter or only the designer.
- [3] Keep motion subtle: small offsets and soft opacity or blur fades, never flashy. Users should feel guided without noticing the technique.
- [2] Weigh how often an animation is seen against how novel it is. Anything used many times a day (command palettes, context menus, launchers, routine actions) and anything triggered from the keyboard gets no animation. Remove that motion rather than speeding it up. Reserve animation for rare or novel moments and for direct touch.
- [2] Frequently opened menus appear instantly. If the choice needs confirming, blink the chosen item in the accent colour, then fade the menu out. If a keyboard-switcher shortcut completes quickly, skip its overlay entirely.
- [2] Prefer motion that explains how the product works (a device folding open, a mechanism assembling, steps playing out in order) over motion that only decorates.
- [2] Add motion last, as its own pass, once layout, colour and spacing are clean. Start with simple transitions.
- [2] Never use spectacle (translucency, shimmer, refraction) to cover usability gaps. Judge it on the second and third visit, not the first impression.

## 2. Press feedback and response time [7]

- [7] Show a pressed state the moment a control is touched: `transform: scale(0.95)` on `:active` (reported for Apple's buttons) or a darker or grey fill. In Tailwind: `active:scale-95 transition-transform duration-100`. Every input gets visible feedback within 400ms (the Doherty threshold).
- [2] A long action puts the button itself into a loading state: a spinner plus the original label. Wait 150-300ms before showing the spinner or skeleton, then keep it visible for at least 300-500ms, so fast responses don't flicker.
- [2] For multi-second waits, show determinate progress that names the real step ("Verifying with your bank", "214 of 340") instead of a generic spinner.
- [2] Budget: POST, PATCH and DELETE complete in under 500ms. Profile with CPU and network throttling and in iOS Low Power Mode.
- [1★ Vercel] Use optimistic UI when success is likely: update immediately, reconcile with the server, and roll back or offer Undo if it fails.
- [1★ Emil Kowalski] Keep loaders snappy. With the same wait, a slow, labouring spinner makes it feel longer.
- [1★ Laws of UX] A short deliberate delay may come before the result of a task that looks hard but finishes instantly. Never delay the acknowledgement of the input itself.
- [1★ Laws of UX] Don't trigger several significant changes at once, because people miss simultaneous changes. Stage them and give each one a clear cue.
- [1★ Vercel] In a group of tooltips, delay the first one, then show its neighbours instantly.

## 3. Build: CSS-first, compositor-only, interruptible [4]

- [4] Choose tools in this order: CSS transitions and keyframes, then the Web Animations API, then a JS library (Motion/Framer Motion in React) only for what CSS can't do, such as shared-element layout or gesture springs.
- [4] Animate only `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`, `margin` or `padding`. For size changes, use FLIP or animate `grid-template-rows` from `0fr` to `1fr`. Colour, background, border and shadow transitions of 200ms or less for hover, press and state feedback are fine: they repaint without layout, and the reduced-motion rule (section 6) keeps them (synthesis).
- [1★ Vercel] Never write `transition: all` or `transition-all`. Name the properties: `transition-property: opacity, transform` (Tailwind `transition-[opacity,transform]` or `transition-transform`).
- [4] Make every animation interruptible: input must be able to reverse or retarget it mid-flight. Use CSS transitions (they retarget from the current value) or springs for interactive state. Keep keyframes for one-shot sequences. Never ignore input until playback ends; a pushed screen that can't be swiped back while it slides in is the cited anti-pattern.
- [1★ Vercel] Set `transform-origin` where the motion physically starts: a dropdown scales from its trigger, a popover from its anchor. For SVG, transform a `<g>` with `transform-box: fill-box`.
- [2] Hold 60fps (16ms frames) before doing any other polish. Dropped frames undo everything else.
- [1★ Emil Kowalski] Motion that runs while the main thread is busy (route changes, page loads, an active-tab indicator during navigation) must use CSS or WAAPI, not requestAnimationFrame-driven JS layout animation.
- [1★ Vercel] Scale a wrapper rather than the text node, to avoid anti-aliasing shimmer. Apply `will-change: transform` only for the duration of a known animation.
- [1★] Never drive animation from `scroll` listeners or per-pixel React state. Use `IntersectionObserver`, CSS `animation-timeline: view()` or `scroll()`, and throttle any canvas draw with `requestAnimationFrame`. Don't stack several animation libraries on one page.
- [1★ Vercel] Touch: set `touch-action: manipulation` on controls, set `-webkit-tap-highlight-color` deliberately, use `overscroll-behavior: contain` on modals and drawers, and turn off text selection and apply `inert` while dragging.
- [2] Back works as undo: sync UI state (tabs, filters, expanded panels) to the URL and restore scroll position on Back and Forward.

## 4. Timing: easing, duration, springs [4]

Starting tokens. Every value is from the research; the per-brief choices are listed at the end of this section.

```css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1); /* expo-out: default for UI and entrances */
  --dur-press: 100ms;  /* press, hover, toggle: 100-150ms */
  --dur-state: 200ms;  /* dropdown, tab indicator, badge, accordion: 150-300ms */
  --dur-panel: 250ms;  /* modal, sheet, panel, page: 250-300ms */
  --dur-view: 400ms;   /* large layout or view move across the screen: up to 500ms */
  --dur-hero: 600ms;   /* the single authored entrance: 600ms max */
}
```

- [4] Never use linear timing for UI movement; it reads as cheap. Default to a strong ease-out that starts fast and settles long: `cubic-bezier(0.16, 1, 0.3, 1)`. Other curves in the data: `cubic-bezier(0.2, 0, 0, 1)` as one mechanical curve for the whole system (Google Labs DESIGN.md), and an "Apple-style" After Effects preset `(0, 0.88, 0.04, 1)`, which comes from a tutorial and was not measured on apple.com. Linear is right only where position is the input (scroll-scrubbed progress) and for constant loops such as an `offset-path` orbit.
- [3] Size the duration to the distance and the consequence. Routine UI is capped at 300ms ("if it takes longer, cut it").

| Change | Duration |
|---|---|
| Press, hover, toggle | 100-150ms (one spec: 120ms) |
| State change: dropdown, tab glide, badge, accordion | 150-300ms; 150-250ms for most product UI |
| Modal, sheet, panel, page | 250-300ms |
| Large layout or view move across the screen | up to 500ms |
| The one authored focal entrance on a page | 600ms max; never delays content or LCP |

- [1★ Impeccable] Exits are faster than entrances: put the exit at the low end of its band, e.g. a modal opens in 250ms and closes in 150ms.
- [1★ Impeccable] Restrained motion travels 10-20px, not 40px. Reveal offsets in the data range from 12px (minimal) to 24px.
- [4] Use springs where the hand drives the motion or it carries momentum: drag, swipe, sheet or drawer release, toggle, reorder, pinch. Ranges: stiffness 1-1000, damping 1-100, mass 1-100. A cited starting point is stiffness 100, damping 20. Scale the bounce to the object's conceptual weight: a swiped card barely bounces, while an object morphing magnetically into a target may bounce more. Productivity UI is critically damped, with bounce of about 0-0.15. In CSS, approximate a spring with `linear()` easing before adding a library. In SwiftUI, springs are the default: `.smooth` has no bounce and `.snappy` a small bounce (std).
- [2] Use one easing token and one duration scale across the product, not per-component curves.
- [1★ Emil Kowalski] The character of the easing is a brand decision. A toast library deliberately runs slightly slower with plain `ease` to feel elegant. **Decide per brief:** crisp and mechanical (tools, dense data) or soft and unhurried (luxury, editorial), and how much bounce, if any, the brand allows. The tokens above are a floor, not a house style.
- [1★ Emil Kowalski, Rauno] Tune timing by trial. Record the interaction, step through it in slow motion, and review it again the next day.

## 5. Animate state changes from their spatial source [4]

- [4] Don't let state changes snap. Animate badges and changing numbers, card resizes, panels, modals, dropdowns, text swaps, and a tab indicator that glides to the new tab. Keyboard-first tools are the exception, because the frequency rule in section 1 wins there.
- [3] Morph one continuous element between states (icon to widget, compact control to expanded options, card to detail view) instead of cutting between two separate elements. Implement with Motion `layoutId`, SwiftUI `matchedGeometryEffect` or the View Transitions API (std). Morph only in response to a user action.
- [2] A view enters from its source and leaves back toward it: a dropdown from its trigger, a detail view from the tapped card, a pushed screen from the right edge, which implies a swipe right dismisses it. Don't hard-cut between screens in an app.
- [1★ Emil Kowalski] When content inside a resizing container changes, crossfade its opacity together with the height animation so items don't pop.
- [2] Animate counters with tabular figures (`font-variant-numeric: tabular-nums`) so the digits don't jitter.
- [1★ Apple HIG] Native only: content-layer sliders and toggles take on Liquid Glass only while being manipulated, and the scroll edge effect blurs and fades content as it passes under the bars.

## 6. Reduced motion, low power, accessibility [4]

- [4] Give every animation a deliberate reduced-motion path. Replace spatial movement (translate, scale-in, parallax, infinite loops, scroll-jacking, scrubbed sequences) with a short opacity fade or a static state. Keep state and interaction feedback such as pressed states, colour changes and focus. Pause decorative loops with `animation-play-state: paused` rather than `animation: none`, and keep paused elements visible.

```css
@media (prefers-reduced-motion: reduce) {
  .reveal { transform: none; transition: opacity 200ms var(--ease-out); }
  .loop   { animation-play-state: paused; }
}
```

  Tailwind uses `motion-safe:` and `motion-reduce:` (std). Framer Motion: `useReducedMotion()`, then zero the x/y offsets and keep the opacity. SwiftUI: read `accessibilityReduceMotion` (std).
- [3] Detect low-power hardware, battery saver and slow connections, and serve a lighter page: solid surfaces instead of blur, no WebGL shader, one still image instead of a frame sequence. Load heavy effects asynchronously and code-split, fade them in after load, and make the core visual work without them. On slow 3G, Apple's AirPods Pro page loaded 8 of 111 requests (347KB of 2.6MB) by falling back to one image.
- [2] Motion must add no input latency and no page weight. Keep INP under 200ms, LCP under 2.5s and CLS under 0.1. Test on a mid-tier Android phone or an iPad, not a fast laptop.
- [1★ Vercel] Autoplay only muted, non-essential loops. Anything that moves for longer than 5s needs a pause, stop or hide control. Replace GIFs with `<video autoplay muted loop playsinline>` and gate it behind the reduced-motion query.
- [2] A heavy scroll sequence can be opt-in, behind a visible start/stop control.
- [2] Never let motion be the only signal of a difference. Pair it with text, an icon or a change of shape.
- (std) Nothing flashes more than 3 times per second (WCAG 2.3.1).

## 7. Scroll-driven storytelling, the Apple way [4]

What apple.com does (see the anatomy in the research): the visitor controls the pace. The product rotates, assembles or splits apart to reveal one attribute; the iMac, for example, turns to show its 11.5mm profile. One centred line fades in and out over black or over a pinned texture video. Motion sections alternate with still ones, and a video beat comes right after a text-heavy stretch.

- [4] Scrub a pre-rendered sequence of a real product with the scroll position, and fade one short line of copy in and out alongside it, one attribute per beat. Scroll replaces autoplay. Use it only when there is a physical product or object to reveal and this is the page's one chosen big idea, at most once per page. Copy the pacing and the one-idea-per-viewport structure, not the asset pipeline.
- [2] Pace the page: alternate motion with stillness, never place two high-novelty sections back to back, leave whitespace between them, and add a short motion beat after a stretch of reading.
- [2] Hand attention to the next focal element with motion, e.g. the hero recedes and blurs as the next section slides over it, instead of an abrupt cut.
- [2] For a linear process, highlight one step at a time as the user scrolls: an underline that fills, or an arc that rotates each step into focus.
- [1★] Give every scroll beat the same viewport distance. Never tie timing to the height of the container being animated; sections of 800-2400px made one crawl and the next fly past.
- Density of a pinned sequence (synthesis): about 0.6 viewport of scroll per step, and the pinned visual fills at least half the viewport height on desktop and a third on phones. A small sticky figure with long empty stretches between short paragraphs reads as an empty dark band; un-pin it and show the stages as a row instead. Keep the pinned figure beside the line being read.
- [1★] Keep light content motion (CSS text fades, slide-ins, sticky pins) separate from heavy graphical motion (frame sequences, 3D, video), and use the heavy kind only where it carries the story.
- [1] (a40, CSS-Tricks recreation; Apple's own code is not documented) Build: a fixed or sticky centred `<canvas>` inside a tall section, driven by native scroll. `p = scrollTop / (scrollHeight - innerHeight)`, `i = Math.min(n - 1, Math.floor(p * n))`, then `drawImage` inside `requestAnimationFrame`. Don't swap `<img src>` on each tick (it flashes). Apple's AirPods Pro hero used 148 JPG frames. Render your own frames; never hotlink or download apple.com sequence assets.
- [2] Avoid sequences of hundreds of stills unless per-frame control is truly needed. Never put several on one page, and never serve full resolution to every device: a naive multi-sequence page cost 1,609 requests, 55.8MB and a 30s load. Serve device-sized frame sets.
- [2] Never hijack scrolling: don't intercept the wheel, and don't pin the viewport to play a build-up the reader has to wait through. Content arrives finished as it enters the viewport.

## 8. Motion budget per surface [4]

- [4] Don't ship a fully static page. Scale motion to the context. Visually led and marketing pages get 2-3 intentional motions, e.g. a hero entrance, one scroll-linked, sticky or depth effect, and considered hover and press states. Before building, write an interaction thesis of 2-3 motion ideas.
- [2] Spend motion the user didn't trigger on one orchestrated moment: one page-load sequence or one reveal, staggered with `animation-delay`. Never repeat the same entrance on every section. Product UI gets no load choreography, and content is visible by default.
- [2] Set a motion-intensity dial from 1 to 10 for the surface. Preset examples: SaaS landing 6, agency 8, editorial 4, public sector 2, Linear-style minimal 3-4. Above 4, the page needs a hero entrance, reveals on key sections and physical hover on CTAs. If you can't ship working motion at that level, drop to about 3 and ship a clean static page. The dial is advisory [2]: context rule 1 [11] governs, and one signature motion the visitor triggers (with a visible invitation) meets "not static" without a load entrance.
- **Decide per brief:** the surface type (persuade, operate, read, experience), the dial setting, and which single moment carries the motion. The section 1 restraint rules still apply at every dial setting.

## 9. Physical response, gestures, haptics, sound [4]

- [4] Physical materials (controls that bend toward the touch point, refraction, specular highlights that follow device tilt) are for native Apple platforms only, through system components. Don't hand-fake them on the web (see context rule 3).
- [3] Behave like objects: momentum on flicks, friction on drags, rubber-band resistance at scroll ends.
- [1★ Rauno] Track a gesture 1:1 from the first pixel, then hand off to an animation once a threshold is passed. Never leave a dead zone followed by a canned 0-to-1 animation.
- [1★ Rauno] On release, carry the gesture's velocity and angle into the follow-through by seeding the spring with the release velocity. Don't play a fixed, centred animation of constant length.
- [1★ Rauno] Commit destructive or navigational outcomes only on release. Let users peek, and cancel if they reverse the drag. Light, reversible actions (revealing a search field or an overlay) may fire mid-gesture once a distance threshold is crossed.
- [1★ Rauno] Keep a drag alive when the finger slides off a small control such as a slider or seek bar. Anchor pinch-zoom between the fingers. Don't let a scroll in progress be captured by a nested scroller the pointer passes over.
- [2] Map gestures to hand actions: drag is grab, move and release; a horizontal swipe turns a page; a pinch zooms precisely. [1★ Rauno] Reuse a small gesture vocabulary so that learning one gesture teaches the rest.
- [2] Haptics are crisp, short and calibrated, like a click, never a buzz. Use the platform's system feedback APIs, e.g. SwiftUI `.sensoryFeedback` (std).
- [2] Sound is optional. Where the platform expects it (shutter, passcode tap) or in motion pieces, cues are soft and match the smoothness of the motion.

## 10. Hover and focus [2]

- [2] Hover and focus make the target stronger: one shade lighter or darker, a small glow, a switch to the brand colour, or an arrow that nudges forward. Never fade, dim, hide or vertically shift the hovered target, and leave no gap between a trigger and its dropdown that closes the menu.
- [8] Focus rings reach at least 3:1 contrast against what surrounds them. Use `:focus-visible`.
- [2] Never put essential information or actions behind hover; touch screens have none. If it matters, show it.
- [2] Don't put a hover animation on every card. [3] Zooming or rotating images on hover is a tell.
- [1★ design-md corpus] Treat pressed as the universal state and hover as an enhancement. Gate hover CSS with `@media (hover: hover)` (std).

## 11. Staggers and entrances [2]

- [2] Stagger real lists, and the words of a headline, so they arrive in reading order: 60-80ms per item, with a capped total delay. Stagger only lists that are genuinely lists.
- [1★ Taste Skill] Reveal values from one source: opacity 0 to 1, translateY 24px to 0 (12px for a minimal look), 600ms, expo-out, triggered once when 30% of the element is visible.
- [2] Masked headline reveal: text rises from behind an invisible edge (an `overflow: hidden` wrapper or `clip-path`), short and strongly eased. Reserve it for the one authored moment, not every heading.
- [2] Don't fade or slide up every section, and never trigger reveals on timers, because readers scroll past before they fire. Content is visible by default and the entrance only enhances it; if the script or observer fails, nothing stays blank.

## 12. Signature motion and brand [2]

- [2] Define one or two signature motions, such as how sections hand over or how panels open, and repeat them site-wide with one easing token and one duration scale. Consistent motion becomes part of the identity.
- [2] Make motion specific to the product: a feature card whose hover depicts that feature, or the product's own data list drifting slowly while items light up about every 5s. This is allowed only when the motion shows the product's real data or mechanism; generic tickers are cut (section 13).
- A signature motion that needs a visitor action (dragging a value, completing a sample task) is invisible unless invited: put a short caption in the first viewport ("Drag the handle to compare"), and let every state reserve its space so nothing shifts (synthesis).
- [2] Plan one or two moments of delight at the emotional peak or at the end of a flow (a confirmation, a completion). Build them into the design; never bolt on confetti at the end.
- **Decide per brief:** the signature move, the easing character and the bounce allowance. Two brands following this file should not move identically.

## 13. What reads as AI-generated or cheap [3]

- [3] Decorative ambient motion that cost nothing to generate: glows that follow the cursor, buttons that chase it, meteors, lines or SVG paths that follow the scroll, pulsing status dots not tied to live data, fake blinking cursors, marquee or ticker bars, images that zoom or rotate on hover.
- [7] Stacked effects: gradient, glow, 3D and video all on one card or section.
- [4] Linear timing. [1★ Impeccable] Bounce or elastic easing on UI.
- [2] Fade-and-slide-up on every section, timer-driven reveals, a hover transition on every card.
- [2] The LLM default extremes: infinite micro-animations everywhere, or the minimal-animation default where nothing is designed.
- [2] Typing animations that type out a fake prompt and answer, and animated placeholder product demos. Show the real product (a faithful render of its real output counts).
- [1★ NN/g] UI that moves by itself: labels that scroll like tickers, controls that morph after a timeout, tab buttons that shimmer or pulse.
- [11] Carousels with no narrative purpose. [1★] Auto-advancing carousels, buttons that morph between shapes, and a sticky header that shows two menus at once mid-transition.
- [1★ Emil Kowalski] Slow, labouring spinners. [2] Scroll hijacking or smooth-scroll overrides that make scrolling feel heavy.

## Context rules (conflicts resolved)

1. **Restraint [11] vs "never ship a static page" [4].** The one-sentence job test governs. Product UI animates state changes at 150-300ms and has no load choreography. A marketing page gets ONE signature story motion (a scroll-scrubbed reveal or a sticky depth section), and only when there is a real product or object to show and that motion is the page's chosen main idea. Add a short entrance of 600ms or less that never delays content or LCP, plus real hover and press states. That is the non-static minimum. A looping hero video is allowed only when the footage IS the content (the place, the product in use): muted, with a poster frame and a pause control, never generic b-roll. Cut all decorative ambient motion: marquees, cursor followers, meteors, parallax on every section, image hover zoom.
2. **Springs [4] vs strong ease-out [4].** Default to interruptible CSS transitions with `cubic-bezier(0.16,1,0.3,1)`, 150-300ms, exits faster than entrances, no overshoot. Use springs for direct manipulation and momentum (drag, swipe, sheet release, toggle, reorder, pinch); they are also SwiftUI's native default. Keep bounce at about 0-0.15, critically damped in productivity UI. Go higher only for light, playful objects in consumer or brand moments. An HTML mock of a native app cannot run system springs: approximate them with CSS `linear()` (std) or use the expo-out token, and say so; "never hand-write a cubic-bezier to imitate Apple" applies to SwiftUI code.
3. **Lively physical materials [4] vs glassmorphism as an AI tell [5].** Glass belongs only on the functional layer that floats over content (nav, toolbars, tab bars, sheets), with a solid fallback for reduced transparency and low power. Refraction, specular highlights and bend appear only on native Apple platforms through system components; on the web they read as imitation and cost performance.
4. **Reduced motion: fade [4] vs collapse every duration to 0ms [1].** Use the fade-or-static replacement and keep feedback. A global `0.01ms` kill switch removes feedback and is flagged as a mistake.
5. **Native scroll [2] vs smooth-scroll libraries and scrubbed sequences [4]** (this file's resolution; the research records none). Default to native scrolling with no wheel interception. A scrubbed sequence only reads the native scroll position, so the user scrolls normally and can scroll past it. Use Lenis-style smoothing only when the brief is an immersive luxury or experience piece, and disable it under reduced motion.
6. **Frame sequence vs scrubbed video** (this file's resolution). Apple reportedly moved to scrubbing one compressed video, with assets up to 80% smaller. MP4 scrubbing lags unless every frame is a keyframe; a keyframe interval of 1 was much smoother than 20. Use video when you can encode it that way, and canvas frames when you need per-frame precision. Either way, serve device-sized assets with a still fallback. Lazy-load the sequence as its section approaches, then preload all its frames before enabling scrubbing, showing the poster in the meantime.
7. **Design hover [2] vs never document hover [1].** Design hover for pointer devices behind `(hover: hover)`, and let nothing essential depend on it. Pressed and focus states are mandatory everywhere.
8. **Tab bar that shrinks on scroll (Apple Newsroom) vs stable navigation (NN/g)** (resolved by the "decide by layer" rule). On iOS, use the system tab bar and its behaviour. On the web, keep nav positions and items stable. A sticky nav may compact smoothly from its detached to its fixed state, but it never shows two navs at once and never hides key destinations.
9. **Morphing controls [3] vs stable affordances [1].** Morph only in response to a user action, on one element, keeping its identity. Never morph on a timer, and never change a button's shape between visits.
10. **Animate every state change [4] vs frequency [2].** In keyboard-first and high-frequency tools, remove indicator glides and list add/remove motion. Keep state-change motion for pointer and touch moments that happen rarely.
11. **Deliberate delay [1] vs instant feedback [7].** Acknowledge input instantly, always. A delay may only come before a result is revealed.

## Checks

Code:
- [ ] `grep -E "transition:\s*all|transition-all"` returns 0 hits.
- [ ] No transition or keyframe animates `width`, `height`, `top`, `left`, `right`, `bottom`, `margin` or `padding` (the `grid-template-rows: 0fr to 1fr` technique is allowed).
- [ ] Routine UI durations are 300ms or less; large layout or view moves up to 500ms; only the single authored entrance (600ms max, never delaying LCP) and scroll-linked progress go longer. Each exit is shorter than its entrance.
- [ ] No `linear` or `ease-linear` on UI transitions. In product UI, no `cubic-bezier` y-value falls outside 0-1 (no overshoot) unless it is a spring on direct manipulation.
- [ ] All easings and durations reference one token set (`--ease-*`, `--dur-*`). No per-component magic curves.
- [ ] A `prefers-reduced-motion` path (`@media`, `motion-reduce:` or `useReducedMotion`) covers every translate, scale, parallax, loop and scroll sequence, and keeps opacity and state feedback. There is no global `0.01ms` override.
- [ ] Every button and link has an `:active` pressed style and a `:focus-visible` ring at 3:1 or better. Hover rules sit inside `@media (hover: hover)` and never lower the target's opacity.
- [ ] No `addEventListener('scroll'` or `onScroll` state drives an animation. No `preventDefault` on `wheel` or `touchmove`.
- [ ] Command palettes, context menus and keyboard-triggered UI have no entrance animation.
- [ ] Every `infinite` animation is a loading indicator or reflects live data. Any motion lasting more than 5s has a pause control.
- [ ] Loading buttons keep their label. Spinners wait 150-300ms before appearing and stay up at least 300-500ms. Animated numbers use `tabular-nums`.

Screenshot and runtime:
- [ ] A full-page screenshot taken without scrolling shows every section's content, with nothing stuck at opacity 0.
- [ ] A motion inventory (element / trigger / one-sentence job / duration / easing) exists, and rows without a job are deleted. Marketing pages: 2-3 motions, at most 1 signature story motion. Product UI: state-change motion only.
- [ ] Under slow 3G and 4x CPU throttling the page is usable, heavy sequences fall back to a still, and INP < 200ms, LCP < 2.5s, CLS < 0.1.
- [ ] A performance trace recorded during each animation shows no frames over 16ms.
- [ ] Interrupt test: double-click a toggle or accordion and press Esc mid-open. The animation reverses from where it is, with no jump.
- [ ] With the OS reduced-motion setting on: no translation, parallax or autoplaying loop, and press and focus feedback still show.
