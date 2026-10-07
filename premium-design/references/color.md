# Colour

`[N]` = number of independent creators who state the rule (a channel with several videos counts once). `[1★]` = one canonical source (Apple HIG, Vercel, Linear, Hobday, Kennedy, NN/g, Anthropic) or a single source that fills a gap. `[1] (aNN)` = one non-canonical source, reported only. `[A N]` = a count from the Apple-only clustering. `(std)` = widely accepted standard value not taken from the research. `(calc)` = contrast ratio computed from the hex values given. Method and backers: [evidence.md](evidence.md). Sections run in evidence order: palette [9], accent [8], contrast [8], then the spent palettes (whose lead tell, purple, is [11]).

**Summary of the highest-weight rules**
- Don't use purple/violet gradients or fills; it is the most-cited AI fingerprint [11]. The cream + terracotta + serif look, near-black + neon and the one-hue-per-card look are also spent [4][2][4].
- Palette = tinted neutrals covering most of the surface + exactly one accent + semantic state colours [9]. The accent goes only on primary CTAs, key controls, selection and focus [8]. Colour comes from the content (photos, product, data), not the chrome [7].
- Body text ≥4.5:1, large text and non-text UI ≥3:1, in every state and both themes [8]. Muted text stays above that floor.
- No pure #000 text on pure #fff; ink is near-black, and text on dark grounds is capped at ~95% lightness [6]. Tint neutrals toward the accent hue [6]. Every colour is a role token, never raw hex [6].
- Defaults are a floor, not a house style. Per brief you still decide: the accent hue, the neutral temperature, light or dark, and the colour strategy: restrained, committed, full palette or drenched (§9, C3, C5).

---

## 1. Palette structure: neutrals + one accent

- **Use neutrals + one accent + semantic states** [9]. Neutrals (white/off-white, greys, near-black) cover most of the surface, unless a committed strategy (§9) gives one brand hue a share. Add exactly one accent, and beyond it only error/warning/success/info. Never add a second accent that competes for the eye. Per brief: which hue, and how warm or cool the neutrals are.
- **Cap the palette at 2-3 colours on top of neutrals** [5]. Only one of them (the accent) is interactive. Start from 2 colours + 2 neutrals and give each colour one named job (accent = action; a second colour = illustration, data or a campaign band). Add a colour only when a real need appears.
- **Take the palette from a concrete source** [4]: the brand guidelines, the product's materials, photography of the real place or product, or the domain's conventions. Name tones after that world (e.g. "limestone", "ink", "olive shadow"). See C6. Naming does not change the values: before locking, measure the OKLab distance (ΔE_ok) from your ground, ink and accent to every hex in the ai-tells.md looks table; if two of the three sit within about 0.04 of one row, it is that look renamed, so move at least two (synthesis threshold; slop_check `cream-terracotta` prints the distances).
- **Check the category's own colour** (synthesis): note the accent hues of the leading competitors. A hue derived from the domain is often the hue every competitor already derived (blue for banking, green for sustainability). If yours is the most common one, take a different element of the same reference world (another material, tool or signal colour from it) or write the differentiation reason into DESIGN.md.
- **Derive supporting hues from colour-wheel harmony** [4] (complementary, split-complementary, analogous, triadic, monochromatic) *from the sourced seed*, never from "a colour I like". OKLCH shortcut: secondary = primary rotated 180° at the same L and C, e.g. `oklch(0.4 0.1 295)` / `oklch(0.4 0.1 115)`. Avoid clashing pairs such as a red logo with a purple accent.
- **Choose the hue for what it means in the domain** [3] (blue for trust in real estate, calm ocean tones for wellness), then echo it faintly in the neutrals (section 5).
- **Use 60-30-10 as a starting check only** [2]: ~60% dominant (usually neutral ground + text), ~30% secondary (cards, alternate bands, visuals), ~10% accent (CTAs). One source flips the 60 and 30; it is a beginner heuristic, not a rule.

## 2. Where the accent goes

- **Accent on action only** [8]: primary CTA, key interactive controls, selected states, focus, and the single item that needs attention right now (e.g. only the imminent time chip turns red). Keep headings, body, icons, input outlines, secondary buttons, cards, chips and card fills neutral. Never use the interactive accent token as a background in product UI, or as a card fill or body-text colour. A committed brand ground (§9, C3) is a separate token, `--brand-ground`, even when it shares the hue. The logo may carry the brand hue [3] (it is the brand asset, not decoration); nothing else non-interactive does.
- **A product with no colour of its own** (black, steel or grey) leaves "let the content supply the colour" [7] with nothing to supply. Take the colour from the reference world (a material, a process, a place) as the accent or one committed band, or from in-use photography; never fall back to grey plus a black pill, which is the trend-minimal tell [3] (synthesis).
- **Keep the chrome neutral and let content carry the colour** [7]. Backgrounds, nav, buttons and icon tiles stay in black/white/grey. Colour comes from photography, product colourways, sparklines, flags and avatars. Luxury sites are black and white once the imagery is gone, and Apple's colour lives in the products on white/grey pages. A black primary button is common here; see C9 for when it becomes a template.
- **One spot colour per view, on the focal object** [5]: the product, the CTA, one data point. Not a headline word; see C8.
- **Apple reference** [A5]: one accent for every link, Buy pill, control, focus and selection; everything else black, grey and white. apple.com links use #0066cc (a10); iOS systemBlue is #007AFF in the HIG light-mode table (std) but shifts with OS release, appearance and Increase Contrast. Use these only as a reference: the hue is decided per brand.
- **Derive states from the same hue** [4]. Build a 9-11 step tint-to-shade ramp or opacity steps: tints for backgrounds, a mid step for the CTA, the darkest for text on tints. Hover = one step lighter; pressed = darker or more saturated; disabled = neutral grey. Never introduce a new hue for a state. Direction when the label is light: C16.
- **The primary action is the highest-contrast clickable thing in its section** [3]: a solid fill, never outline-only or pale grey (a ~#c9c9c9 button reads as disabled).

## 3. Contrast numbers and value hierarchy

- **Contrast floors** [8]: ≥4.5:1 for body and small text; ≥3:1 for large text (≥24px, or ≥18.66px bold (std)); ≥3:1 for non-text UI that identifies a component or state (icons, input/checkbox/toggle edges, outline buttons, focus rings, inactive nav, badges). Target 7:1 for body text on dark surfaces. Check every state: hover, disabled, overlays, text on images, both themes. Never recolour status badges in the brand hue if that drops them below 3:1.
- **Keep strong contrast in both themes** [5]. No light-grey text on grey. Blur alone does not separate icons from imagery. When Linear raised contrast, it darkened text and neutral icons in light mode and lightened them in dark mode.
- **Use 2-3 text tiers** [3]: primary at full contrast; secondary dimmer; tertiary only for disabled/placeholder. Emphasise by dimming what surrounds the key text, not by colouring the key text. Floors: see C7.
  - Reference ramps: `#171717 / #525252 / #A3A3A3` on `#FAFAFA` (the third is ~2.4:1 (calc), so disabled only); `hsl(0 0% 5%)` / `hsl(0 0% 30%)` on light; `95%` / `70%` lightness on dark.
- **Build hierarchy from lightness and saturation, not hue** [3]. Give every palette colour a clearly different lightness. Bright and saturated = important; muted = secondary. Desaturate the screenshot: if hierarchy survives in greyscale, it works in colour.
- **Settle structure in greyscale first** [3]: black, white and their opacities for hierarchy, contrast and elevation. Add hue only once that works. Decide the colour strategy early and apply it late (C12).
- **Text on photos** [3]: place it on a calm, even-toned crop area, or add a subtle gradient scrim or blur behind it. Never on busy imagery.
- **Measure perceptually too** [1★ Vercel]: check with APCA as well as WCAG 2 (see C15). Use colour-blind-safe chart palettes, and make `:hover`, `:active` and `:focus` *higher* contrast than the rest state.

## 4. Don't use the default AI palettes (the spent looks; read after sections 1-3)

- **No purple/violet as the brand colour** [11]. Detector values: hue 250-300°, saturation >0.25, lightness 0.15-0.85, filled at opacity ≥0.5; a single instance counts. That covers purple-to-blue or purple-to-magenta gradients on heroes, headline text, frames and buttons, and indigo fills on CTAs, active pills and badges. Purple is allowed only as an existing brand asset, and even then never as a gradient on white.
- **Glassmorphism is not the main visual** [5]. Frosted cards with thin light borders over gradients are a tell: backdrop-filter blur ≥2px on translucent cards 150-820px wide. Blur goes only on the functional floating layer (sticky nav, toolbars, sheets). See C11.
- **Don't default to the warm-craft trio** [4]: cream ground (#F4F1EA, #f5f1ea, #f7f5f1, #faf7f1), terracotta/oxblood accent (#D97757, #b6553a, #9a2436), warm ink (#1a1714), serif display. Never ship the same warm palette twice in a row. See C6.
- **Don't give every card, stat, icon tile, badge or pill its own hue** [4]. Google-primary icon tiles and four KPI cards in four bright colours are the "fake dashboard" pattern.
- **Don't copy the "Linear look"** wholesale [4] (dark mode + bold sans + complex gradients + glass + monochrome). Squint test: if the palette could be guessed from the category alone, or matches an unrelated product's, rework it.
- **No coloured glows** [3]: no zero-offset or saturated box-shadow halos (detector: blur ≥15px, saturation >0.3, alpha ≥0.1; two per page trigger it). Elevation shadows are neutral, offset and soft.
- **No mesh, aurora, spotlight or radial glow backgrounds** [3], especially the top-centre purple-into-blue/cyan glow behind the H1.
- **No trend minimalism** [3]: light-grey canvas, tiny grey text, black pill CTA, no colour, flat hierarchy. Fix it by committing harder on an existing element (type size, real colour, real image), not by adding ornament.
- **No coloured one-side stripe** [3] on cards, callouts or selected items (a saturated border ≥2px that is >1px wider than the other sides, or a 2-10px `::before` bar covering ≥60% of an edge). Use a fill change or weight instead. Grey/black/white borders are exempt.
- **No flat, reflexive canvas** [3]: not a lone pure white, not a cool grey-white, not a stock dark theme. Choose the ground's temperature deliberately.
- **Near-black + one neon accent** (emerald, acid green, vermilion) on stock components is the generator's dark default [2]. So is a hero background within a few shades of #0A0A0A-#111 picked without a reason [2]. A chosen, tinted value is fine (Linear's #010102 is deliberate).
- **No gradient text** (`background-clip: text`) on headings or metrics [2]. A page with ≥4 elements carrying visible gradients (stop alpha >0.05) reads as generated.

## 5. Neutrals: tint, temperature, pure black and white

- **Tint neutrals toward the brand/accent hue** [6]. Change only the hue and keep the lightness. Default OKLCH chroma ~0.005-0.02 (C4); the research ceiling is ~0.05, or HSB saturation <5%. For dark grounds, use the brand hue at 1-10% HSL lightness instead of #000. The tint should be felt, not noticed. Linear capped how much of its brand hue fed the neutrals and moved to a warmer, less saturated grey [1★ Linear]. When the palette was sampled from the subject [4] and the accent's hue disagrees with the sampled material (a warm accent on a cool material), tint toward the sampled material and keep one temperature (C17). Watch the drift: a red or clay accent pulls tinted neutrals into warm greige, which is the cream-terracotta neighbourhood.
- **No pure #000 ink on pure #fff** [6]. Off-blacks: #1d1d1f (Apple ink), #111111, #121212, #0a0a0a, zinc-950, #1A1C1E, or warm #1E1A14. Off-whites: #F7F5F2, #F4F0E4. Cap headings on dark grounds at ~95% lightness (`hsl(0 0% 95%)` on a 0-10% ground). For where pure values are correct, see C1.
- **Lock one neutral temperature and one accent across the whole product** [5]. All warm or all cool, never mixed: the same role always gets the same colour, through illustrations, inputs, labels, links, CTAs, error states and the favicon. No blue CTA in section 7 of a warm-grey site, and no green email field beside a purple password label. Audit every component before shipping.
- **Build neutrals as a stepped ramp with one role per step** [3]. Steps differ only in lightness (e.g. 90/70/50/30/10%), then take the tint. Never add an ad-hoc grey. Reference only: an After Effects tutorial's palette (5j4HmfgPCDI; its role names) uses the iOS greys #E5E5EA (systemGray5), #8E8E93 (systemGray), #3A3A3C and #1C1C1E (dark-mode systemGray4 and systemGray6) (std names). In native code use `separator`, `secondaryLabel`, `tertiaryLabel` and `secondarySystemBackground`, never these hexes.
- **On coloured grounds, tint shadows, borders and secondary text toward the ground's hue** [3]. On lavender #B4A9EC, use a purple-grey #CFC9DD shadow, not #C7C7C7. Secondary text there is a darker shade of the ground, near-white, or foreground at reduced opacity. Never neutral grey.
- **Surface steps stay small** [1★ Hobday]: the page-to-container brightness difference is within ~12% HSB on dark interfaces and ~7% on light ones.

## 6. Semantic role tokens

- **Every colour is a token named by role** [6] (CSS custom property + matching design-tool variable): canvas, surface, label/secondary label, action/focus, border, success/warning/error/info, data scale. Components reference tokens only. Write each as name + value + role (e.g. "Action Blue #0066cc: links, CTAs, focus").
- **Author in a hue/lightness model** [3] (HSL, HSB or OKLCH), not raw hex, so each variant is a one-number change. Generate ramps in OKLCH [2] so equal L steps look equally light across hues. OKLCH L runs 0-1, and its hue sits ~25-40° above the HSL hue: re-derive values instead of copying numbers. Tailwind v4 already ships OKLCH (`gray-50` = `oklch(0.984 0.003 247.858)`).
- **Re-check after any hue or chroma change** [2]: switch themes and check primary, secondary, hover states and every background the brand will appear on.
- **Generate themes from a few inputs** [1★ Linear]: Linear replaced 98 hand-set variables per theme with 3 inputs (base, accent, contrast) fed through one LCH pipeline that also derives the elevations (background, panel, dialog, modal), for light, dark and custom themes alike.

Template. Every value is a slot to fill from the brief; keep the roles. Values marked "Apple ref" are apple.com measurements (a10), not defaults: a page using 3 or more of them is an Apple clone (slop_check flags it as `apple-tokens`).

```css
:root {
  color-scheme: light dark;
  --canvas:          /* REQUIRED: ground sampled from the reference world */;              /* Apple ref #ffffff */
  --surface-alt:     /* second tier: tinted off-white, brand tint or inverted dark */;     /* Apple ref #f5f5f7 */
  --surface-raised:  /* card on --surface-alt (tonal elevation) */;
  --brand-ground:    /* committed strategy only (§9): the brand hue as a section ground */;
  --label:           /* near-black #111-#1d1d1f range, shifted toward the accent hue at OKLCH chroma 0.005-0.02 */; /* Apple ref #1d1d1f */
  --label-secondary: /* same hue, verified >=4.5:1 on every surface it sits on */;        /* Apple ref #6e6e73 (~5:1 on #fff) */
  --label-disabled:  /* --label at 40% (~2.8:1): disabled only */;
  --separator:       /* decorative; may be <3:1 */;
  --border-control:  /* >=3:1 against its ground (inputs, toggles, outline buttons) */;
  --accent:          /* REQUIRED: brand action hue as a fill (buttons, switches, selection): >=3:1 against its neighbours; never #0066cc/#0071e3/#007AFF unless the brand owns it */;
  --accent-text:     /* the accent as text (links, back labels): >=4.5:1 on --canvas; may be a darker step, or --label (C17) */;
  --link:            var(--accent-text);
  --accent-hover:    /* one ramp step lighter */;
  --accent-pressed:  /* one ramp step darker */;
  --on-accent:       /* text on the accent fill, >=4.5:1 */;
  --focus:           /* from the accent ramp, >=3:1 against its surroundings */;
  --success: ; --warning: ; --danger: ; --info: ;   /* section 11 */
  --data-1: ; --data-2: ; --data-3: ;                 /* chart scale, not accents */
}
@media (prefers-color-scheme: dark) { :root {
  --canvas:          /* tinted off-black: brand hue at 1-10% HSL L */;
  --surface-alt:     /* one step lighter */;
  --surface-raised:  /* lighter again */;                                                 /* Apple ref dark tiles #272729-#2a2a2c */
  --label:           /* ~95% L, tinted */;
  --label-secondary: /* ~65-70% L; verify >=4.5:1 */;
  --link:            /* brighter variant of the accent, dark grounds only */;              /* Apple ref #2997ff */
  --accent:          /* CTA fill: verify --on-accent >=4.5:1 (white on #2997ff is ~3:1 (calc)) */;
}}
@media (prefers-contrast: more) { :root { --label: #000; --canvas: #fff; } }
@media (prefers-contrast: more) and (prefers-color-scheme: dark) { :root { --canvas: #000; --label: #fff; /* (std) */ } }
```

- Tailwind: map the tokens in `@theme` so utilities read `bg-canvas text-label border-control`; no `bg-[#hex]` in components.
- SwiftUI: use `Color(.label)`, `.secondaryLabel`, `.systemBackground` and `.secondarySystemBackground`; set the accent once with `.tint()` at the root; give each custom colour asset Any/Dark/High-Contrast variants (std).
- Apple system colours: systemBlue #007AFF, systemGreen #34C759 and systemRed #FF3B30 are light-mode values from Apple's published tables (std) that shift with OS release, appearance and Increase Contrast; secondaryLabel is #3C3C43 at 60% alpha, rgba(60,60,67,.6) (std), not an opaque grey (opaque, it renders almost as dark as label). Hard-code none of them; they are adaptive roles [1] (a44).

## 7. Section grounds, light vs dark, premium tone

- **Alternate section grounds to break up long pages** [5]: a dark statement or pricing band, one brand-colour or brand-photo band, a distinct ground for a distinct audience. Keep it within the brand's own 2-3 surface tiers. A ground change marks a change of topic or audience, never decoration. [2] Apple pattern (a10): full-bleed bands of white, #f5f5f7 and black butt with 0px gaps and never repeat a surface consecutively. That is one separation method; whitespace alone, a full-bleed image or a hairline are equally valid, so pick one per page.
- **Choose light or dark from the real use scene** [4]. Write one sentence on who uses it, where and under what light. Dark is right for developer tools, night use, media, space or automotive subjects. It is the wrong signal for most consumer and editorial products, and there is no evidence that dark is "better". Consider warm light when every competitor is dark. Default and exceptions: C5.
- **Premium reads darker and more muted** [4]. Keep bright yellow and red out of dominant roles (they signal fast food and discounts); for a warm accent, choose orange over yellow. This means muted colour, not "make it dark" (C5). (Reported, 7ooF1zNWsrQ, about hardware finishes: Apple gives premium products darker, muted colourways and entry products lighter, saturated ones. For UI this only means the product's own finish sets the page mood; it is not a palette rule.)
- **Match the backdrop to the image** [2]: set the section or tile colour to the photo's baked-in background, or to a colour sampled from it. For example `body { background:#000 }` under renders lit on black, or a muted mauve tile behind a magenta cover. Cut-outs should show no edge.

## 8. Saturation

- **Keep UI colour moderate** [4]: OKLCH chroma ≤ ~0.15-0.2 (the scale runs to ~0.4); one source caps the accent at <80% HSB saturation. A grid of maxed-out hues is the second most common colour mistake. Never put saturated colour behind heavy blur or glass.
- **Don't ship an all-grey interface either** [3]. Restrained (tinted neutrals + one accent) is the floor for product UI, not the goal. If the swap test fails because the page reads as a grey template, commit harder on an existing element.

## 9. Committed colour (marketing and brand scale)

- **Choose a colour strategy up front** [4]: Restrained (tinted neutrals + one accent), Committed (one saturated hue owns 30-60% of the surface), Full palette (3-4 named roles) or Drenched (the surface is the colour). Dominant colour with sharp accents beats a timid, evenly spread palette. When to use which: C3.
- **A single hue as the ground** [4]: for a hero, campaign band or poster, flood one saturated hue and set type and UI in white or in lighter/brighter tints of that same hue (orange ground with yellow type, teal with cyan). A different hue per section is allowed only when each section *is* a product colourway.

## 10. Gradients, atmosphere, grain

- **Give grounds atmosphere, from real things** [4, resolved by C2]: photography, lit product renders, material texture, or a flat tinted ground. Don't default to a dead flat colour, and don't fake depth with glows.
- **Grain** [3]: a noise overlay at a few percent opacity (e.g. `opacity: .04` on an SVG `feTurbulence` layer) on photos, flat colour fields or abstract visuals, to stop banding or add material warmth. Leave sections meant to look crisp without it.
- **Gradients in UI elements** [2]: default to a flat fill. If you need a gradient, make it subtle, low-contrast and within one hue (darker to lighter of the same colour). Never two hues (no blue to green). Never on buttons or text.
- **Scale gradient complexity inversely to content density** [1★]: sparse hero, richer gradient; dense content, simple or none. Raycast kept its bold red and dropped the gradient when it simplified.

## 11. Status colours

- **Red and green mean error/danger and success, nothing else** [4]. Map status to real-world conventions and to what the change means: an expense increase is red, a decrease green; "On time" green, "Due in 3 days" amber. Never use them decoratively; a "Log out" in emergency red is wrong. If the brand accent is red or green, see C10.
- **Never signal status by colour alone** [1★ Vercel]: pair it with a text label and/or icon; give icon-only buttons an `aria-label`.
- **Keep alerts uniform and muted** [1★]: same lightness, low chroma, only the hue changes, e.g. danger `oklch(0.5 0.05 30)`, warning `oklch(0.5 0.05 100)`, success `oklch(0.5 0.05 160)`, info `oklch(0.5 0.05 260)`.
- **Chips and badges** [1★]: a pale tint ground with saturated text in the same hue (a "New" chip on ~#CEFECD with green text). On dark, use a dark tint with bright text and a dot. Text inside still ≥4.5:1, the chip edge ≥3:1 only if it is interactive.
- **Charts get their own data-scale tokens** [1★]: distinguishable, colour-blind-safe series. Never paint every chart in the single brand colour, because high and low values then look the same.

## 12. Dark mode construction

- **Every token resolves per appearance** [3]: light, dark, increased contrast (and tinted/clear where the platform offers them), following the OS. CSS reference: default #111 on #f4f4f4; `prefers-contrast: more` gives #000 on #fff; dark gives #ddd on #111/#222; dark + more contrast gives a #000 ground.
- **Keep every ground step in dark** (synthesis). A page whose light theme separates sections by ground (an inverted band, a raised tier) needs the same steps in dark: the inverted band becomes a lighter tier, the brand hue or a band with a rule, never a near-twin of the dark canvas, or the page turns into one slab. render_check runs a dark pass and flags a band that drops under 1.3:1 against the page (`dark-grounds`).
- **Raised surfaces are lighter than the surface beneath** [2 Kennedy, Hobday], in both themes. A darker card on a lighter ground reads wrong. Dark shadows barely show, so carry elevation with tonal steps, plus a 1px lighter top edge on raised elements where needed [1★].
- **Ground**: tinted off-black (section 5), not a reflexive #0a0a0a. Text max ~95% L; secondary ~65-70% L, verified ≥4.5:1; body targets 7:1.
- **Brighter accent variant on dark** (a10): Apple uses #0066cc for links on light, #2997ff on dark tiles and #0071e3 for focus. Derive your own pair from the accent ramp; never use the dark variant on light grounds.
- **Don't drop light-mode colours onto dark unchanged**. Inverting lightness (L → 100-L, keeping hue and saturation) gives a usable first draft [1★]. Then retune every token by eye; one source forbids mechanical inversion outright.
- **Browser chrome** [1★ Vercel]: `color-scheme: dark` on `<html>` for dark themes, `<meta name="theme-color">` equal to the canvas, and explicit `background-color` and `color` on native `<select>` (it fixes Windows dark mode).
- **Materials (Apple platforms)** [1★ HIG]: text and fills on materials use the system vibrant label/fill/separator colours, not fixed custom ones. Choose a material for its semantic role, not its tint. Add a 35% dark dimming layer behind clear Liquid Glass only over bright content.

---

## Context rules (conflict resolutions)

- **C1 Pure #000/#fff.** Treat ink and surface separately. On the web, default ink is near-black (#1d1d1f-#111); on dark, ink is ≤95% L. Native Apple apps keep `Color(.label)` on `Color(.systemBackground)`, which is #000 on #fff in light mode by Apple's own design. Pure #fff *surface* is fine when it is not the only surface: pair it with a second tier (a tinted off-white, a brand band, an inverted section) or put white cards on an off-white page. Match product-photo sweeps exactly to their section. Use pure #000 only for (a) sections whose renders were lit on black, (b) true-black video/media viewers on OLED, (c) `prefers-contrast: more`. Every other dark ground is a brand-tinted off-black (brand hue at 1-10% HSL lightness); a neutral #0a0a0a-#121212 only when chosen for a reason written in DESIGN.md.
- **C2 Gradients and atmosphere.** The avoid side wins by default (~30 creators vs ~11). Use a gradient only when something physical motivates it: light falling across a surface, a vignette seating a product, or a ramp of the existing brand hue. Keep it at hero or section scale and low contrast; never on buttons or text, and never as a top-centre glow. No purple-to-blue/cyan, mesh or aurora.
- **C3 Restrained vs committed.** Restraint wins by default and almost always in product UI. Committed colour applies at section or campaign scale on marketing and brand surfaces when the colour *is* the content: a product colourway, a campaign, a brand whose identity is a colour. Then one hue owns that section (or 30-60% of the surface under a committed strategy) with type in white or its own tints, set as `--brand-ground`. On a committed ground the interactive role switches to a contrast-safe pairing (a white or near-black CTA, or a tint of the same hue); the accent stays the only interactive hue, and chroma stays moderate unless the product itself is that saturated.
- **C4 Tinted vs zero-saturation greys.** Default: barely tinted (OKLCH chroma ~0.005-0.02, hue from the accent, one temperature). Use true neutral or slightly cool greys when content colour must be judged accurately (product colourways, photography, fashion, colour tools, data-viz grounds) or when the brand is deliberately cold and technical.
- **C5 Light vs dark.** Dark is not a shortcut to premium. Default light, which is also Apple's marketing default: white and light grey with near-black ink. Go dark when the use scene argues for it: pro or cinematic renders, photo/video tools, a developer tool's own UI, night use, space or automotive. Docs and dev-tool marketing default to light with an OS-following dark theme. A dark page uses a brand-tinted off-black, accent chroma ≤0.15 (§8) and no neon accent unless it is the brand's. On a light page, the best use of dark is one inverted section for rhythm or a render moment. Product apps support both appearances through tokens and follow the OS. Marketing pages design one deliberate appearance and do not auto-invert art-directed imagery.
- **C6 Replacing purple.** Swapping purple for cream + terracotta + serif fixes nothing; both are AI defaults. Derive the palette from the subject's world (section 1): sample it from photos of the actual subject, never from a list of safe alternatives. Cream is valid only when the subject is made of it (paper, bakery, ceramics, hospitality). Always replace the terracotta/rust accent; default to a sans display. A serif display on cream needs a written reason and must be upright and outside the overused pool. Harmony rules only generate supporting hues from a sourced seed.
- **C7 Muted text vs contrast.** Muting is allowed down to the AA floor, never below it. #6e6e73 on white is ~5:1; black at 60% opacity on white is ~5.7:1; 40% is ~2.8:1 and fails, so keep it for disabled states (WCAG-exempt). Apple's reported secondary #7a7a7a is ~4.3:1 on white (calc), below AA for small text. Low contrast is fine only for decorative lines.
- **C8 Spot colour vs headline accent.** The spot colour goes on the focal object or action, not on a headline word. A coloured, italic or gradient word is now an AI signature. Exception: poster or campaign art where the word is the subject (a product colour name, as in Apple's "orange" in orange). Use it once per site, in a solid palette colour, never as gradient text.
- **C9 CTA colour.** One primary per view, and it is the highest-contrast clickable element. Use the brand accent if the brand has a real one; near-black when imagery or product supplies the colour (fashion, luxury, photo-led). A black pill on an otherwise grey minimal page reads as a template. Never violet. The secondary action is a text link with a chevron, or an outline only when both actions are real and parallel.
- **C10 Brand red/green vs status.** Semantic meaning wins. A red or green brand accent can stay the accent, but status must be distinguishable from it: errors in a different shade or hue plus an icon and text, success in a non-brand green. Don't put the accent on destructive actions unless they really are destructive. For premium work, a red accent stays small (logo, CTA) and never becomes a dominant ground.
- **C11 Glass.** Glass is only for the functional layer floating over content (sticky nav, toolbars, tab bars, sheets), where it replaces a shadow and falls back to solid under reduced transparency or low power. Content (cards, panels, hero) stays solid. Refraction and specular effects are for native Apple components only; don't hand-fake them on the web.
- **C12 Greyscale-first vs exact values first.** Decide the colour strategy early and write the tokens into DESIGN.md; apply colour after the greyscale structure works.
- **C13 Shadows on colour.** Neutral shadows on neutral grounds. On a coloured ground, use a darker, low-chroma shade of that ground. Never a saturated brand-hue glow.
- **C14 Accent on prices** (no dump resolution; resolved from the Apple playbook [5] vs one creator's "junior mistake"). Default: prices neutral and bold. Put the accent on a price or count badge only when it is the one number the user scans for, and no non-interactive element on that screen already carries the accent.
- **C15 WCAG 2 vs APCA** (no dump resolution). WCAG 2 AA ratios are the hard floor (std: the ratios most legal and audit requirements use). APCA is an extra perceptual check, mainly for thin or light text on dark grounds, where WCAG 2 over-reports contrast.
- **C16 Hover direction** ([4] "hover one step lighter" vs [1★ Vercel] "hover raises contrast"; resolved here). Default: one ramp step lighter, which raises contrast for dark text on a tinted chip and for a dark button on a dark ground. On a fill that carries a light label (white on a mid or dark accent), a lighter step lowers the label's contrast, so hover goes one step darker there. Either way the hovered target reads stronger, never weaker [2].
- **C17 Accent as fill vs accent as text, and sampled hues** (synthesis). The accent has two jobs with two floors: as a fill (button, switch, selection, slider thumb) it needs 3:1 against what surrounds it and 4.5:1 for its own label; as text (links, back labels) it needs 4.5:1 against the ground. Give them two tokens. Hues around 60-100° (amber, yellow, ochre) and light cyans cannot reach 4.5:1 as text on a light ground without turning brown or murky: keep the fill bright (with a dark label on it), set links in `--label` with an underline, and check by eye that the fill still reads as the named reference colour. When the accent's hue and the sampled material's hue disagree, the neutrals follow the material and the accent stays the only warm (or cool) note.
- **C18 Emotion vs novelty** (synthesis of [8] emotions, [3] hue for its meaning and [2] vary across projects). The higher count wins: temperature and hue family follow the target emotions and the domain, and cross-project variety moves only the axes they leave open (lightness, chroma, strategy, the specific material). A brief for appetite, hospitality or comfort stays warm: sample one specific warm material (olive oil, saffron, brass, oak, tomato, ochre plaster) and leave the cream-terracotta look through its accent and face. Flipping such a brief to a cool grey-blue or cobalt canvas to differ from the last project reads as a clinic or a booking app.

## Checks an agent can run

1. Grep components for raw colour literals (`#`, `rgb(`, `hsl(`, `oklch(`, Tailwind `-[#`): 0 outside the token file.
2. Count distinct hues with OKLCH chroma > ~0.05 in UI chrome (excluding images, status and data tokens): ≤1 accent (≤3 brand colours only with a named job each).
3. List every element using `--accent`: each is a CTA, link, control, selected state, focus ring or the single attention item.
4. Purple detector: no fill or gradient with hue 250-300°, saturation >0.25, lightness 0.15-0.85, unless purple is a documented brand asset.
5. No `background-clip: text`. No `box-shadow` with blur ≥15px, saturation >0.3 and alpha ≥0.1. No zero-offset coloured shadow. No backdrop-blur on in-flow cards. No coloured one-side border >1px wider than the others.
6. No radial or mesh gradient behind the H1; ≤ hero/section-scale gradients; none on buttons.
7. (web) Text colour is never `#000` on `#fff`. Text on dark grounds is ≤95% L. Pure `#000` grounds appear only in render/video sections or the high-contrast mode. No more than 2 of the apple.com values (#f5f5f7, #1d1d1f, #6e6e73, #0066cc, #0071e3, #2997ff) unless the brief is Apple's.
8. Contrast: body and secondary text ≥4.5:1; large text, control edges, focus rings and badges ≥3:1. Check light, dark, hover, disabled, on tinted surfaces and over images.
9. Desaturate a screenshot: hierarchy still reads, and the primary CTA is the highest-contrast clickable element.
10. All greys share one hue (or chroma 0) and one temperature. Surface steps are within ~7% (light) / ~12% (dark) HSB brightness. In dark mode, raised surfaces are lighter.
11. Dark theme: `color-scheme` set, `meta theme-color` equals the canvas, native `<select>` styled, links use the brighter dark variant, and button text on the accent fill still clears 4.5:1.
12. Every status shows text or an icon besides colour; red and green appear only as status (or as the brand accent, distinguishable per C10).
13. Chart series are distinguishable and colour-blind-safe, not all one brand hue.
14. Every ground change marks a topic or audience change; when full-bleed bands touch, adjacent bands differ. Under a restrained strategy, ≤1 brand-colour or photo statement band; under a committed one, the brand ground covers the share written in DESIGN.md.
15. Swap test: the palette is not one of the spent looks (purple gradient, cream + terracotta + serif, near-black + neon, Linear dark-glass, grey + black pill), and could not be guessed from the category alone.
16. ΔE_ok from ground, ink and accent to the nearest looks-table hex is written in DESIGN.md; no two of the three within about 0.04 of one row (synthesis).
17. The accent hue is not simply the category's most common accent, or DESIGN.md says why it still differs.
18. Hover on a light-labelled fill goes darker (C16); `--accent` (fill) and `--accent-text` (links) each meet their own floor (C17).
