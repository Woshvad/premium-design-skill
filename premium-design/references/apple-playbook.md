# Apple playbook: what makes it premium, and what not to copy

`[N]` = independent creators stating the rule, counted in the Apple-only clustering (SKILL.md shows these as `[A N]`; they are not comparable with the main ranking). Apple's HIG, WWDC talks and Newsroom together count as one creator. `[1★]` = a single canonical source (Apple, NN/g, Vercel, Rauno); `[1] (aNN)` = a single non-canonical source, reported only. Methodology, backers and the source index are in [evidence.md](evidence.md).
Value labels: **(a10)** = community-extracted from apple.com CSS (awesome-design-md), not published by Apple. **(obs)** = measured from video keyframes, ±10%. **(reported)** = a claim made in a source, not measured. **(computed)** = arithmetic on research values. **(std)** = a widely accepted standard that is not in the research.

## Summary
- Show the real product large, isolated and centred on a seamless neutral field that matches the section surface. The page stays neutral and the product supplies the colour **[9] [5]**.
- Set all type from a fixed ladder of named text styles in one sans family, and build hierarchy from size and weight **[7] [5]**.
- Use one accent colour, only for interaction. Chrome recedes so content leads **[5] [5]**.
- Subtract until every element earns its place, but never hide essential actions behind overflow or hover. Keep the words per viewport very few **[5] [5] [5]**.
- Copy the discipline, not the costume. SF Pro, Apple blue, black Pro pages, scroll-scrubbed films and witty fragment headlines belong to Apple's brand, licences or budget (section 14).

## 1. Product imagery (top weight [9])
- **[9]** Show the hero product as a large cut-out: isolated, centred, three-quarter or frontal view, on seamless white or `#f5f5f7` (black for Pro). Use only a soft contact shadow, no props and lots of empty space. Make the page background exactly match the render's baked-in background so the product floats with no visible image edge (a40).
- **[4]** Use giant full-bleed photos or video as section building blocks. Overlay one short, centred, white headline and at most one text link, with a scrim or verified contrast (section 8).
- **[4]** Put Pro, flagship and rugged tiers on a pure `#000` canvas with white type and low-key, rim-lit renders. Mainstream products stay on white or light grey.
- **[2]** Always show the real product: photo, render or real UI screenshot. Never use a grey placeholder tile, a logo or an abstract illustration. For software, real UI screenshots are the product photography.
- **[2]** Add in-use shots of real people in real settings next to the cut-outs. Each shot proves one feature or shows scale, for example a hand holding the device edge-on, or a dim room for a night mode.
- **[2]** Show how the product is made, using footage or exploded views of parts that settle into the enclosure, not prose.
- **[6]** (main ranking, imagery_media.0.23/0.25) Keep the image set consistent and grade all images on a page the same way. Apple's design book used one photographer for 450+ photos and re-shot older products to match (a42).
- (obs) Graphic arrangements of colourways: in rows, fans or radial wheels. Devices may bleed off the viewport edge. Macro crops of edges, ports and materials. Device screens show vivid content art against the neutral page.
- Decide per brief: the field (white, `#f5f5f7`, black, or a tint sampled from the product), the lighting tier, and whether you can actually produce imagery at this standard. A stark white page exposes weak photos.

## 2. Typography [7]
- **[7]** Set all text from a fixed set of named semantic styles that lock size, weight and leading. Use about 3 per component: title, then a subheadline in the secondary colour, then body. Never hardcode sizes. SwiftUI: use `.font(.body)`, not `.system(size: 17)`; use `.headline`, not `.body` plus bold.
  iOS ladder (pt, size/leading): Large Title 34/41, Title 1 28/34, Title 2 22/28, Title 3 20/25, Headline 17/22 Semibold, Body 17/22, Callout 16/21, Subhead 15/20, Footnote 13/18, Caption 1 12/16, Caption 2 11/13.
- **[5]** Use one sans family for the whole interface and build hierarchy from size and weight. Don't add a second display face. The only sanctioned companion is the New York serif, and only for long-form reading and quotations, on Apple platforms only (licence (std)) **[2]**.
- **[4]** Body size is the floor for reading text: 17pt on iOS and visionOS, 13pt on macOS (HIG). On the web use 16-17px, chosen by the face's x-height (main ranking [7]). apple.com sets SF Pro Text at 17px/1.47 (a10); that value belongs to SF, not to other faces. Never go below Caption 2: 11pt on iOS, 10pt on macOS.
  apple.com (a10): body is 17px / 400 / 1.47 / -0.374px; hero is 56px / 600 / 1.07 / -0.28px; display line-heights run 1.07-1.19.
- **[3]** In native apps, request the system font through the platform text styles, and the OS applies optical size and tracking. When a size outside the text styles is unavoidable (a display numeral), use `.system(size:weight:)` or `UIFont.systemFont(ofSize:)` scaled with `@ScaledMetric` or `UIFontMetrics`. Never embed SF files, and never hand-tune tracking per size in code.
- **[3]** Tracking varies by size. SF table in 1/1000 em: 6pt +41, 11pt +6, 12pt 0, 17pt -26, 20pt -23, 24pt +3, 28pt +14, 48pt +8, 80pt and above 0. apple.com mirrors SF's table: body -0.022em (-0.374px at 17px), the 56px hero only -0.005em (-0.28px), nothing at 12px or below (a10). These values belong to SF; for other faces use the inverse-to-size rule [11] (typography.md).
- **[3]** Map weight to hierarchy: Regular for body, Semibold for a heading at the same size (Headline 17 Semibold over Body 17 Regular). To add a level, switch to another style or use the emphasized variant (Large Title, Title 1 and Title 2 go Bold; Title 3 and smaller go Semibold). Never add a new size.
- **[3]** Emphasise with weight and tone, not colour or size jumps. Put a grey lead-in line above a dark statement, or open a muted sentence with one bold key term. **[2]** Card pattern: a bold dark title, then a smaller, lighter grey description.
- Web weight ladder (a10, [1]): 300/400/600/700, with no 500. Repeated section headlines on apple.com use 600; 300 only for large airy leads (~24px). This is Apple's reference value, not a rule for other brands: a reflexive 700+ on repeated web headlines in a face not drawn for it reads as a marketing template, while a single wordmark-as-graphic (the AirPods Max wordmark is set very heavy (obs, cdzbM0HABqY)) and native emphasized title styles (Bold) are Apple's own. Never use Ultralight, Thin or Light at text sizes **[2]**.
- **[2]** Use faces with optical sizing (a variable opsz axis). SF switches from its Text cut to its Display cut at 20pt.
- **[2]** Use tabular digits for prices, specs, counters, timers and balances: `font-variant-numeric: tabular-nums` (std CSS name), or `.monospacedDigit()` in SwiftUI.
- **[2]** Support Dynamic Type everywhere, including custom fonts: `Font.custom(name, size:, relativeTo: .body)`. iOS Body spans 14pt (xSmall) to 53pt (AX5). At accessibility sizes, reflow the layout (HStack becomes VStack) instead of truncating.
- **[2]** Use SF Pro Rounded only deliberately, for friendly or soft contexts. Use condensed or compressed widths only in tight spaces or for display presence, never for long body text.
- **[2]** Only when recreating apple.com itself (a reference mock, or marketing for an Apple-platform app): `system-ui, -apple-system, BlinkMacSystemFont`, then Inter retuned (600 display, -0.01em display tracking, body line-height 1.44) (a10). For any other brand this is costume and the [13] default-font tell: apply T1 (one licensed family with Text/Display cuts or an opsz axis). If the brief explicitly asks for the native system look, add `slop-check: ignore default-font-only` and write the reason in DESIGN.md.
- **[1★]** HIG: on macOS, Body is 13/16, Large Title 26/32 and Headline 13/16 Bold, with no Dynamic Type. On tvOS, Body is 29/36 Medium and Title 1 is 76/96. Use tight leading only on 1-2 line text in constrained rows, never on 3 or more lines. Text with no backing surface (visionOS) gets bold weight, not drop shadows.
- **[1★]** Never disable zoom (`user-scalable=no`). Set mobile inputs to 16px or more so iOS Safari doesn't auto-zoom (Vercel).
- Decide per brief: the brand typeface on the web is not SF Pro (context rule T1).

## 3. Simplicity, visibility, content first [5]
- **[5]** Keep essential actions and information visible and reachable in one tap, with frequent tasks within about 3 taps (a guideline, not a hard rule). Only nonessential actions go in overflow menus. Nothing essential may appear only on hover. With only 1-2 items, show them inline, not behind a summary card with a "See all" link.
- **[5]** Deference: bars, controls and decoration recede. They never compete with content or block it or its touch targets.
- **[5]** Strip each screen to the fewest elements: remove everything, then add back only what earns its place. Never strip by hiding functions people need. Apple's WWDC26 talk separates simple from minimal.
- **[3]** Build hierarchy from order, spacing, size and whitespace, not colour, borders or effects. Give each screen one visual anchor and check it with a squint test.
- **[3]** Group related bar actions and tabs into one cluster. On custom or web bars, don't scatter controls or float one-off buttons. Native iOS 26+: put search in the system search tab (`Tab(role: .search)`), which the OS renders detached at the trailing end. This is Apple's own pattern (the WWDC25 redesign cuts 5 tabs to 3 plus a detached search; Apple News does the same), even though NN/g criticises it in the App Store (a37).
- **[2]** Map the steps before and after a problem, and remove or combine steps upstream instead of polishing only the problem step.
- **[1★]** Every screen must answer: Where am I? What can I do? Where can I go? (WWDC25) What is interactive, and how? (WWDC26). Turn complex data into a graphic. Add context to a control when it helps people decide, for example replacing a bare play/pause button with a scrubber that shows time remaining (WWDC26).

## 4. Colour [5]
- **[5]** Use exactly one accent colour for every interactive element: links, Buy pills, controls, focus and selection. Everything else is black, grey or white. Prices stay neutral (apple.com hero: a small grey "From $"); put the accent on a price or count badge only under color.md C14. Never use the accent decoratively, and never add a second accent.
  apple.com (a10): `#0066cc` on light surfaces (5.6:1 on white, computed); `#2997ff` for links on dark (7.0:1 on `#000`, computed); `#0071e3` focus ring. iOS systemBlue: the HIG has published RGB (0,122,255) = `#007AFF` for light mode, but values change between OS releases, appearances and Increase Contrast (std). Never hard-code it; use `Color.accentColor`, `.tint()` or `UIColor.systemBlue`.
- **[5]** Keep the page and base palette neutral (white, `#f5f5f7`, black) and let products, materials and screen art bring all the colour. Colour at most one headline word in the product's colour, and only when that colour is the subject.
- **[4]** Make every colour a semantic role token (label, secondaryLabel, systemBackground, accent, divider, disabled) with light, dark, increased-contrast and vibrancy variants. Components reference token names, never raw hex. Reference values: apple.com Ink `#1d1d1f`, Parchment `#f5f5f7`, Hairline `#e0e0e0`, Action Blue `#0066cc` (a10). iOS system greys as used in an After Effects tutorial's palette (5j4HmfgPCDI; the role names are the tutorial's): `#E5E5EA` (systemGray5), `#8E8E93` (systemGray), `#3A3A3C` and `#1C1C1E` (dark-mode systemGray4/systemGray6) (std names). In native code use `separator`, `secondaryLabel`, `tertiaryLabel` and `secondarySystemBackground`, never these hexes.
- (a10) Text ink is `#1d1d1f`, not `#000`. Pure black is kept for the global nav, video backgrounds and photo overlays. Secondary text is listed as `#333` / `#7a7a7a`, but `#7a7a7a` measures 4.3:1 on white and 3.9:1 on `#f5f5f7` (computed), which fails AA for body text. Use `#6e6e73` instead: 5.1:1 on white, 4.7:1 on `#f5f5f7`.
- (a10) The system has zero gradient tokens; atmosphere comes from photography. There is one shadow, `rgba(0,0,0,0.22) 3px 5px 30px`, used only on product renders. Cards get a 1px `rgba(0,0,0,0.08)` hairline instead. Adjacent dark tiles step through `#272729`, `#2a2a2c` and `#252527`.
- (reported, 7ooF1zNWsrQ; hardware finishes) Apple gives premium products darker, muted colourways and entry products lighter, saturated ones. For UI this only means: let the product's own finish set the page mood; it is not a palette rule.
- Decide per brief: the accent hue. Apple blue is Apple's action colour, so take yours from the brand. Whether the CTA uses the accent or near-black is covered in T6.

## 5. One language, native conventions, stable controls [5]
- **[5]** Use one design language (materials, patterns, controls, visual style) across every product, platform and page, from the smallest switch to full screens. Each platform keeps its own qualities. Don't reinvent the look every year.
- **[4]** Default to native components and conventions: HIG, system frameworks, standard window chrome and navigation, standard placements. Add personality only in chosen places, and never borrow another platform's style. Before hand-building glass, use the system APIs. Liquid Glass (functional layer): SwiftUI `.glassEffect()`, UIKit `UIVisualEffectView(effect: UIGlassEffect())`, AppKit `NSGlassEffectView` (std, verify in the SDK). Standard materials (content layer): SwiftUI `Material`, `UIBlurEffect`, `NSVisualEffectView`.
- **[3]** Keep key actions and navigation in the same place and state on every screen and device, and make controls that look alike behave alike. Keep learned gestures through redesigns; the Mac close button is always top-left.
- **[3]** Make touch targets at least 44x44pt/px, with about 0.4cm between adjacent targets. apple.com icon buttons are exactly 44x44.
- **[3]** Use continuous-curvature (G2) corners: `.continuous` in SwiftUI, corner smoothing in Figma. **[2]** Base surfaces on the rounded rectangle. Make radii concentric: inner radius = outer radius minus the inset. Web radius grammar (a10): 0 for full-bleed tiles, 8px for compact buttons, 11px (role not given in a10; don't copy), 18px for utility cards, 9999px for pills, which are reserved for actions.
- **[2]** Treat icons as part of type: match icon stroke weight to the adjacent text weight, scale icons with text size, and colour them from text tokens. **[1★]** On Apple platforms, use SF Symbols for common actions and never repurpose a standard glyph: the trash can always means delete. On the web and other platforms, SF Symbols are not licensed (std); use one open-licence library (Phosphor, Lucide, Tabler or Radix) at one stroke weight matched to the type.
- **[2]** Primary controls look touchable. Hover states affirm (one shade lighter, or a switch to the brand colour) and never recede.
- **[2]** Derive web chrome from the product's current material language. apple.com followed Platinum, Aqua, aluminium, glass, then flat (2014) (7PeSluyP8FE). The OS moved to Liquid Glass in 2025 (a35); no source in the research shows apple.com adopting it.
- **[1★]** Native details (Rauno): put high-frequency commands at corners and edges (Fitts's law); blur sensitive content in the app-switcher snapshot; keep icon art inside the safe zone so system morphs don't stretch it.

## 6. Copy [5]
- **[5]** Use very few words: a wordmark, or one short headline plus at most a ~3-6 line paragraph per viewport. Imagery carries the message.
- **[4]** Write headlines as the product name plus a short declarative fragment or two-beat line about one benefit. Use sentence case, end even fragments with a full stop, and stack 1-3 words per line when stacking. Patterns: fragment benefit ("Symphonic boom."), setup then payoff ("Looks tough. Because it is."), category reframe, narrative arrival.
- (anatomy) Feature callouts open with the bolded part name, then one plain sentence. Prices are exact and include monthly terms ("From $X or $Y/mo. for 12 mo."). CTAs are a blue "Buy" pill plus a text link ending in ">".
- Decide per brief: this cadence depends on brand familiarity. For an unknown product, specificity wins (T8).

## 7. Motion and feedback [4]
- **[4]** Animate state and view changes instead of hard cuts. Morph one shape into the next (icon to widget, app to icon), expand cards into detail views, and enter from and return to the spatial source (the tapped icon, or the right edge for a pushed screen).
- **[4]** Tie product-story sequences to scroll position so the visitor sets the pace: hardware reveal, then software, then use in context. Short ambient clips and a highlights carousel may autoplay muted (apple.com does both), with a visible pause control for anything that moves longer than 5s (WCAG 2.2.2, std), and stop under `prefers-reduced-motion`. Rotate or assemble the product to reveal one attribute (the iMac turning to its 11.5 mm profile) while headlines fade in and out. Alternate motion with static sections; every moving element needs a job.
- **[3]** Make interaction physical: momentum on flicks, friction on drags, rubber-band bounce at scroll ends. On release, carry the gesture's velocity and angle into the follow-through.
- **[2]** Use springs tuned by stiffness, damping and mass, and scale bounce to the object's conceptual weight: a swiped card bounces less than an app morphing into the Island. **[2]** Keep motion subtle, smooth and quick, with immediate feedback; never flashy.
- **[2]** Never add motion for its own sake. Routine controls get no shimmer, wiggle, pulse or timer-driven morphing (NN/g on iOS 26). Check that it still feels right on the 10th and 100th use.
- **[2]** Confirm routine actions with tiny feedback: a haptic tick, an elastic bounce, an opacity-plus-blur fade, a number count-up. Buttons scale to 0.95 on press (a10); 7 creators back instant pressed feedback within 400ms. **[2]** Use crisp, short haptics and soft sound cues that are as smooth as the motion.
- **[1★]** Rauno: make every animation interruptible, commit navigation and destructive gestures only when the finger lifts, and don't animate high-frequency UI (context menus, Cmd-Tab).
- Timing (T5), split by platform. Web UI: `cubic-bezier(0.16,1,0.3,1)` at 150-300ms, exits faster than entrances, entrances 600ms or less (a web ease-out from a05 and Kowalski, not an Apple measurement). Native Apple: system springs for all transitions; never hand-write a cubic-bezier to imitate Apple. The often-quoted "Apple" curve `0.00, 0.88, 0.04, 1.00` comes from an After Effects tutorial and was not measured on apple.com.

## 8. Depth, materials, Liquid Glass [4]
- **[4]** Show hierarchy through depth: translucent, blurred planes over content, plus parallax and motion. Icons and buttons inside each layer stay flat. Pick one depth mechanism and use it consistently.
- **[3]** Guarantee legibility over glass and photos. Put a gradient or a ~35% dark dimming layer behind text and controls over bright or busy content, because blur alone is not enough. Verify contrast against varied backgrounds.
- **[3]** Put controls and navigation on a distinct translucent layer that floats above content, with content scrolling underneath and showing through. Don't separate a bar from content with a shadow. apple.com sticky sub-nav (a10): 52px tall, `background: rgba(245,245,247,.8); -webkit-backdrop-filter: saturate(180%) blur(20px); backdrop-filter: saturate(180%) blur(20px)`, no shadow (Safari before 18 needs the prefix (std)).
- **[3]** AVOID glass, translucency or transitions as decoration, or as a skin over an unchanged interaction model. Limit them to the few most important functional elements.
- **[3]** AVOID shipping a redesign that is merely different, or spectacle (refraction, shimmer) put ahead of usability. Judge it after weeks of real use.
- **[2]** Take faux textures (leather, wood), gloss and heavy shadows out of chrome. Simulate light, layering and depth of field instead.
- **[2]** Web approximation of glass, for detached floating panels only (popovers, sheets): `-webkit-backdrop-filter` and `backdrop-filter: blur(24px) saturate(180%)`, a 1px `rgba(255,255,255,.32)` border and an inset top highlight. Add the `0 18px 60px rgba(0,0,0,.18)` shadow only to detached panels, never to bars (see above). Fall back to a solid surface under `@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px)))`, `@media (prefers-reduced-transparency: reduce)` and `@media (prefers-contrast: more)` (std; Safari ignores prefers-reduced-transparency). Use it only over colourful or detailed content; over a flat colour it just looks transparent.
- **[1★]** HIG Materials (2025):
  - Liquid Glass belongs only to the functional layer, never to content (backgrounds, cards). Content-layer sliders and toggles take glass only while being manipulated.
  - Use the regular variant for text-heavy components (alerts, sidebars, popovers). Use clear only over photos or video, with a 35% dimming layer when the content is bright.
  - Apply the scroll edge effect: blur and fade content where it passes under bars.
  - Liquid Glass has only the regular and clear variants (a34). Standard materials (content layer) are a separate system with thicknesses ultraThin, thin, regular and thick: thick behind text, thin where the background should stay visible, regular by default.
  - Step text hierarchy through vibrancy: label, secondaryLabel, tertiaryLabel, quaternaryLabel. Never put quaternaryLabel on thin or ultraThin. Choose a material by meaning, never for its tint.
  - Test with Reduce Transparency, Increase Contrast and each Liquid Glass look.
- **[1★]** Newsroom 2025: glass takes its tint from the content beneath, and its radii are concentric with the hardware. Tab bars shrink on scroll down and expand on scroll up (but see T16).

## 9. Spacing [4]
- **[4]** Use drastic whitespace; a whole viewport may hold one short line or one product shot. Take all spacing from tokens. apple.com (a10):
  - Section padding 80px; at least 64px above headlines and 48-64px below; at least 40px around product images; 24px card padding.
  - Space tokens 4/8/12/17/24/32/48/80 (17 matches SF's body size, not the 4/8 grid; don't copy it).
  - Max width about 980px for text and about 1440px for grids. Global nav 44px.
- **[3]** Use an 8pt grid with 4pt half-steps. On widths not divisible by 8 (the 375pt iPhone), keep spacing on the grid and let one block stretch. This is a reverse-engineered convention, not an Apple mandate.
- (a10) Section rhythm: full-bleed bands alternate between light, dark and parchment with 0px gaps, so the surface change divides sections. The same surface never appears twice in a row. This is Apple's separation method, one of several (whitespace, a full-bleed image, a hairline); copy it only if the brief chooses banding.
- Decide per brief: density (T4). Tools, dashboards and checkout use the lower steps of the scale.

## 10. Craft and process [4]
- **[4]** Write the system down as a spec (HIG or DESIGN.md) in this order: philosophy, colour roles, typography, components, spacing and layout (targets, materials), accessibility, then explicit Do's and Don'ts naming the anti-patterns.
- **[4]** Finish unseen details (hidden states, alignment, interiors) to the hero's standard, and apply the same craft to sound, haptics and packaging.
- **[3]** Work in a fixed order: structure, then details, then finishes, then motion. Check the whole after each layer. For an app redesign: Structure, Navigation, Content, then Visual design.
- **[2]** Treat design as never finished: iterate after launch, and go back to the drawing board when real use shows a detail is wrong.
- **[1★]** Jobs's "staying beginners" (via Fadell, 9uOMectkCCs): review the product every day as a brand-new customer would, and hunt for the annoyances everyone has grown numb to.

## 11. apple.com page anatomy, top to bottom [3]
Evidence spans about 2014-2024 (KZ-eAiBW6gA ~2020, 7PeSluyP8FE to 2019, cdzbM0HABqY ~2024); verify against the live site before citing anything as current.
1. **Global nav [2]** (as captured c.2019-2020): a slim full-width bar, 44px (a10). Logo first, 7-9 plain-text categories evenly spaced, search and bag icons at the right, no dropdowns. Rule: flat text links sized to the real catalogue; add flyouts only when categories have many children (conflict resolution). The live apple.com now uses more categories with hover flyouts (std, verify).
2. **Category sub-nav [2]** (category pages only): one row of small line-icon product tiles with tiny labels (models, Compare, accessories, OS) and small "New" tags, then a few large banners instead of a full price list.
3. **Sticky local nav [2]** (product pages): product name at left; 2-3 small links (Overview, Tech Specs); a compact blue Buy pill at right. Translucent light on light pages, dark on black pages, 52px tall.
4. **Hero [3]:** a centred stack: optional small "New" eyebrow, product name, one-line tagline, small grey "From $" price, then at most two small blue CTAs (a filled pill plus a "Learn more >" link or an outlined pill). Flagship variant: a short cinematic set piece before content or price, with a near-viewport-wide wordmark and the product in front of it **[2]**.
5. **"Get the highlights" carousel:** wide rounded cards with short copy, a play/pause control and dots.
6. **Feature chapters [2]:** a long scroll in which each chapter covers one feature with one short headline, moving from benefits to technical detail. The format changes every chapter:
   - a full-bleed greyscale macro video under a centred headline that swaps as you scroll;
   - a scroll-driven product rotation in an empty white viewport;
   - a stacked headline alone on white;
   - an editorial block: eyebrow, huge left-aligned 3-line headline, body offset into the right half;
   - a build story with bold-keyword callouts on the grid;
   - a staggered two-image grid;
   - a bento of rounded tiles, each holding a real visual;
   - a spec chapter.
7. **Colours and finishes:** swatch dots beside a coloured product profile.
8. **Compare:** 3 columns of image, swatches, name, "From $", Buy pill and Learn more, then aligned spec rows.
9. **Footer:** `#f5f5f7`; link stacks at line-height 2.41 (a10).
- **Homepage [2]:** one dominant product hero, about 2 flagship sub-heroes, about 6 smaller tiles, then the footer. Never link sidebars or news columns.
- **[2]** Every layout is structured (on the grid) and exploratory (each section has its own moment). Never repeat one section pattern down the page, and never assemble stock template sections.

## 12. Building scroll stories on the web [2]
- **[1]** (a41) Keep content motion (text fades, pins and slides with CSS `transform`/`opacity`, `animation-timeline: view()` or IntersectionObserver) separate from graphical motion (image sequences, 3D, video). Use graphical motion only where it carries the narrative. Map each animation to a fixed viewport range, never to the container's height.
- (a40, a CSS-Tricks recreation of the AirPods Pro hero; Apple's own code is not documented) Apple used 148 JPG frames. The tutorial:
  - draws zero-padded frames to a canvas: `position: fixed; left: 50%; top: 50%; transform: translate(-50%,-50%); max-width: 100vw; max-height: 100vh`;
  - uses about a 5x scroll runway (`body` 500vh).
  - Render your own frames; never hotlink or download apple.com sequence assets.
  - `frameIndex = min(frameCount-1, floor(scrollFraction*frameCount))`, drawn inside `requestAnimationFrame`.
- **[2]** Budget:
  - Put at most one sequence on a page, and serve device-sized frame sets. Several sequences on one page cost 1,609 requests, 55.8MB and a 30s load.
  - On a slow connection, serve a single static image. Apple's page on slow 3G loaded 8 of 111 requests, 347KB of 2.6MB.
  - Video scrubbing makes assets up to 80% smaller (a41). MP4 scrubbing can lag; a keyframe interval of 1 was much smoother than 20 (a40).
- **[2]** Under `prefers-reduced-motion`, swap to a fade or a static frame. Make heavy sequences opt-in with a visible start/stop control. **[1★]** (Vercel) Profile on iOS Low Power Mode and throttled Safari.

## 13. Apple's design principles, 2025-26 (Apple = one creator; [1★] unless tagged)
- **Classic trio:** Clarity **[2]** (legible, precise, plainly shows what it does), Deference **[5]**, Depth **[4]**.
- **2025 Liquid Glass trio:**
  - Hierarchy **[3]**: controls sit above content; hierarchy comes from spacing, size and component behaviour, not just colour or effects.
  - Harmony **[2]**: shapes are concentric with the hardware.
  - Consistency: platform conventions, adapted to each window size; design systems, not screens.
- **WWDC25 Design foundations:**
  - Do an information-architecture pass first: list everything, imagine the contexts of use, then remove, rename and group. Use progressive disclosure.
  - Ask the three orientation questions. Squint-test for one anchor.
  - Use system text styles and semantic colours, and the accent sparingly.
  - Decide where to lean on the system and where to add personality.
- **WWDC26 Principles of great design**: eight principles that trade off against each other, with no formula:
  - *Purpose:* make every feature intentional, because each one costs time, attention and trust.
  - *Agency:* let people go straight in and explore, with no forced linear onboarding. Make sends, edits and deletes undoable **[2]**.
  - *Responsibility:* act in people's interest. Ask for permissions and data in context, ask only for what's needed, and say why. Assume AI features will sometimes be wrong: add previews and confirmations, and cut the feature if the risk outweighs its value.
  - *Familiarity:* use metaphors that are neither too literal nor too abstract, keep placements stable **[3]**, and use standard glyphs.
  - *Flexibility:* design for each device and context (touch on phone, pointer on desktop, hands-free in the car) and support Dynamic Type.
  - *Simplicity:* every element earns its place, with fewer steps. It is not the same as minimalism.
  - *Craft:* fonts and colours that adapt, clear icons, responsive animation. Failures to avoid: laggy taps, jittery scroll, misaligned icons, layouts that break on rotation.
  - *Delight:* the sum of the other seven, not confetti added at the end.

## 14. Apply the principles, not the costume
Copy these: subtraction, one idea per viewport, real product imagery, a single action colour, named type styles, neutral fields, a written spec, and restrained motion.
Do not copy these:
- **SF Pro, New York and SF Symbols outside Apple-platform apps.** SF Pro may not be self-hosted or embedded on the web. A `system-ui` stack renders SF only on Apple devices (Segoe UI or Roboto elsewhere), so the brand voice changes with the OS. A web brand needs its own licensed face (T1). SF Symbols and New York carry the same Apple-platform-only licence (std); `ui-serif` renders New York only in Safari on Apple devices. In native Apple apps, SF through text styles and SF Symbols are correct.
- **Apple's own assets.** Taglines, product photos, renders, frame sequences, the Apple logo and SF Symbols are copyrighted or trademarked. Use them as pattern references only, never in a build or mock-up for another brand (std). Write your own lines in the pattern, or none (T8).
- **Apple blue as your accent.** It is Apple's action colour. Derive yours from the brand.
- **Scroll-scrubbed films and 3D build sequences.** They need CGI of a physical product plus engineering budget, and a naive copy weighed 55.8MB. Most imitations copy the look and miss the pacing logic; copy the pacing instead.
- **Stark white pages without Apple-grade photography.** White exposes weak images. Never fill the gap with stock photos, or with generated images that depict the actual product.
- **The "slow down" intro before price.** It works because visitors already want the product (the analyst's inference). An unknown brand loses visitors who came for facts.
- **Witty fragment headlines and pure-black Pro pages.** They lean on brand familiarity and on colourways that do the colour work. The short fragment cadence now reads as AI copy (T8).
- **Liquid Glass or glassmorphism as decoration**, or hand-faked refraction on the web (T7).
- **Hex snapshots of system or apple.com colours** (`#007AFF`, `#0071e3`) hard-coded as if they were stable tokens.
- **Template tells mistaken for Apple:** a reflexive 700+ weight on repeated web headlines in a face not drawn for it, mesh or aurora gradients, shadows on cards or buttons, bento grids with empty cells or icon tiles.
- **Apple's own misses:**
  - iOS 26 critiques (NN/g a37; contested, not consensus): search moved to the bottom, Android-style left-aligned titles, the tab count hidden in an ellipsis menu, shimmering tab bars, cramped Photos controls, contrast problems in the beta. Native apps still adopt system behaviour; apply the critique only to custom and web chrome.
  - The Saved products page: an orphaned Edit link, and one item behind a summary card.
- **Native mocks: system behaviour, not Apple's own apps** (synthesis). Copy what the platform gives every app (navigation, back, inset lists, switches, text styles, tab bars). Do not copy the screen layouts of Apple's first-party apps: if a screen maps 1:1 onto Health, Clock, Fitness or Weather (the same hero number, the same chart order, the same list), change at least two of hero composition, chart encoding and list structure. The signature move must not be the category's standard chart either. Hand-drawn status-bar glyphs, a floating glass tab bar and a home indicator are device chrome, not brand. An HTML mock renders the same on every OS only if its titles use a loaded face (SKILL.md section 7, web mock).
- **Decide per brief, never inherit from Apple:** accent hue, light or dark canvas, brand typeface and display weight, corner softness (from the reference world, not the category label), density, headline voice, the one signature motion, and the photography you can actually produce.

## 15. Context rules (from audited conflicts)
- **T1 Typeface.**
  - Native Apple apps: SF through system text styles wins outright.
  - Web and marketing: headings use a licensed face with character from a serious foundry. Body uses that family's Text cut or a neutral workhorse. Not Inter, Geist, DM Sans, Plus Jakarta or Space Grotesk as display.
  - Dense data tools: one neutral sans with tabular figures.
  - Add a second face only with a named job (an editorial serif, mono for code). Ceiling: two voices plus mono.
- **T2 Black and white.** Web and marketing: ink is never `#000` on `#fff`; use about `#1d1d1f` to `#111`. A pure `#fff` surface is fine when paired with a second tier (an off-white such as `#f5f5f7`, a brand band, an inverted section). Use pure `#000` only for renders lit on black, OLED media viewers and `prefers-contrast: more`. Other dark grounds are brand-tinted off-black (brand hue at 1-10% HSL lightness); a neutral `#0a0a0a`-`#121212` only when chosen for a reason written in DESIGN.md. Native Apple apps: use `Color(.label)` on `Color(.systemBackground)`; pure black on white in light mode is Apple's own system value, so never override it with hex.
- **T3 Light or dark.** Default to light; Apple's marketing is mostly light. Go dark only when the use scene argues for it: pro or cinematic renders, media tools, developer tools, night use. One inverted section per page is for rhythm. Apps support both appearances through tokens and follow the OS.
- **T4 Whitespace or density.** Use generous whitespace (about 80-160px desktop section padding) on marketing, editorial and hero layouts, and only with strong hierarchy. If small grey type floats in emptiness, raise the scale and contrast. Tools, tables, settings and checkout use the 4/8/12/16 steps. Gaps follow relationships in both modes.
- **T5 Motion.**
  - Web UI: ease-out `cubic-bezier(0.16,1,0.3,1)` at 150-300ms, exits faster than entrances, no overshoot; springs only for drag, swipe, sheet release and toggles (bounce 0-0.15).
  - Native Apple: system springs for all transitions (`withAnimation` default, `.smooth`, `.snappy`), bounce 0 for state changes and up to about 0.15 for gesture release; never hand-write a cubic-bezier to imitate Apple.
  - Marketing pages get ONE signature story motion, and only when there is a real object to reveal. Entrances never delay LCP. Always provide a reduced-motion path.
- **T6 CTA.** One primary per view: the highest-contrast clickable element.
  - Colour: the brand accent if the brand has a real one; near-black when imagery or product supplies the colour. A black pill on a grey minimal page reads as a template.
  - Secondary: a chevron text link. Use a filled-plus-outline pair only for two real parallel actions (Buy and Learn more).
- **T7 Glass.** Use it only on the floating functional layer, where it replaces a shadow, with a solid fallback for reduced transparency and low-power devices. Refraction and specular light only through native Apple components. Never put saturated colour behind heavy blur.
- **T8 Headlines.** For an unknown brand, say what the product is and what it achieves, in 2 lines or fewer on desktop. Use an evocative tagline only when visitors already know the category, and pair it with a plain descriptive subline. No "Not X. Just Y." and no formula triads.
- **T9 Hero structure.**
  - Physical product with strong imagery: a centred, product-led hero, or a full-bleed image with text on a calm area behind a scrim or with verified contrast.
  - Software or services: a left-aligned text stack with a real UI visual.
  - Type crossing behind the product: once per site.
- **T10 Nav count.** Catalogue sites: about 7-9 flat links (apple.com as captured c.2019-2020), with flyouts only when categories have many children. Single-product or service sites: 5 or fewer. Native apps: a tab bar with 3-5 destinations, never a hamburger.
- **T11 Images by role.** Product, catalogue and detail views: cut-outs on a sweep matched to the section surface. Hero and campaign: one art-directed scene per section. One grade per page.
- **T12 Colour commitment.** Restraint is the default. Flood a section in one hue only when that colour is the content (a product colourway, as Apple does). The accent stays the only interactive colour.
- **T13 Neutrals.** Default to a barely tinted ramp (OKLCH chroma 0.005-0.02). Use Apple-like true or cool greys when product colour must be judged accurately. Either way, keep one temperature throughout.
- **T14 Radius.** Use one scale by role: 8px for inputs, 12-16px for cards, 20-28px for large containers, pills only for actions. Nest radii concentrically. Use squircles natively and where CSS `corner-shape` is supported; otherwise a plain radius is fine.
- **T15 Muted text.** Mute only down to 4.5:1. Black at 60% opacity is about 5.7:1 on white; at 40% it is about 2.8:1, which fails, so reserve 40% for disabled states only.
- **T16 Adaptive chrome or stable controls** (resolved here; no audited entry). Apple shrinks tab bars on scroll **[2]**, while stable placement has **[3]**. Shrink chrome in place and restore it on scroll-up. Never relocate or reorder controls, move them into overflow, or change the control set by context.
- **T17 Sequence pipeline** (resolved here; a40 and a41 disagree). Default to no sequence. If you need one: one per page, lazy-loaded near the viewport, with a static fallback. Prefer an all-keyframe compressed video for long sequences.

## 16. Checks (code or screenshot)
- [ ] (web) No `#000` text on `#fff`; body ink is near-black. Native: semantic label colours, no hex. Secondary text measures 4.5:1 or better on every surface it sits on (`#7a7a7a` fails).
- [ ] Exactly one saturated interactive hue outside semantic states, and it never appears on non-interactive decoration.
- [ ] Components contain no literal `font-size` values; all come from named style tokens. SwiftUI has no `.system(size:)`, and reading text is 16-17px or more on the web.
- [ ] No `@font-face` for SF Pro or New York, no SF files and no SF Symbols in the web build. Display weight is a documented per-brief choice (repeated web headlines at 600 or below in the Apple reference; a single wordmark-as-graphic and native emphasized title styles are exempt), and no weight of 300 or lighter is used under 24px.
- [ ] Every margin, padding and gap is on the 4/8 token scale. Desktop marketing sections have 80px or more of vertical padding.
- [ ] Touch targets are 44x44 or larger under `(pointer: coarse)`. The viewport meta doesn't disable zoom, and mobile inputs are 16px or larger.
- [ ] `backdrop-filter` appears only on the nav, toolbars, sheets and popovers, never on cards or the hero, and each use has a solid fallback.
- [ ] Shadows appear only on floating elements and product renders; cards use a hairline or a tonal surface. No decorative section gradients (scrims behind text are fine).
- [ ] Screenshot, physical-product pages: the product is the largest element in the hero and no image edge shows against the section surface. Software and services: a real UI visual is in the first viewport (T9).
- [ ] Each marketing viewport has 1 headline and about 6 or fewer lines of body text. The hero has 2 or fewer CTAs, with exactly one filled.
- [ ] Adjacent sections never repeat a layout pattern [14]. Every ground change marks a topic or audience change; if the brief uses surface banding, bands that touch never share a surface (apple.com, a10); otherwise sections may share a surface and separate by spacing.
- [ ] Animations use only `transform`/`opacity`, there is a `prefers-reduced-motion` branch, and no control loops or shimmers.
- [ ] Nested rounded elements satisfy inner radius = outer radius minus padding. Prices and specs use tabular figures.
- [ ] Text over images has a scrim or measured contrast of 4.5:1 (3:1 for large text).
- [ ] Squint test: one anchor per screen, and each screen answers where am I, what can I do, and where can I go.
- [ ] (native mock) No screen maps 1:1 onto an Apple first-party app; titles render in a loaded face on non-Apple machines; grouped backgrounds use platform values unless a reason is written.
