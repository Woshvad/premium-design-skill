# Typography

`[N]` = independent creators who state the rule (a channel with several videos counts once). `[1★]` = one source, kept because it is canonical (Apple HIG, Butterick, Vercel, Linear, NN/g, Hobday, Kennedy, Anthropic) or fills a gap. `(reported)` = a measured value from one source, a reference and not a default. `(std)` = a widely accepted value that is not in the research. Method and backers: [evidence.md](evidence.md).

**Summary (highest-weight rules)**
- The brand voice is never a default face. Inter, Roboto, Arial, Open Sans, Lato, Times New Roman and the OS font may set body and UI text, but not the headlines on a brand surface [13]. Audition 3 or more brand-specific candidates in the real layout [10]. Native Apple apps are the exception: use SF through text styles [9].
- Track inversely to size: caps labels +0.03 to +0.1em, body 0, headings -0.005em (h6) to -0.02em (h1), never tighter than -0.04em, and never negative at 12px or below [11].
- Set all text from about 9-15 named semantic styles (family, size, weight, line-height and tracking as tokens) [8]. Text steps use a tight ratio (1.125-1.25), and display steps jump to at least 2x, with one display size at 3x or more [7][3].
- Default to one family. Add a second face only if it comes from a different class and has a named job. Use mono only for literal code and data [9][7][6][5].
- Body is 16-17px on the web, 17pt on iOS and 13pt on macOS, at about 1.5 leading and 65-75ch. Headings take 1.1-1.3 and display 1.0-1.1 [7][6][3].

**Decide per brief.** The defaults below must not turn every project into one house style. For each project, choose: the brand face and its class (grotesk, humanist, serif, expressive); its display weight; one family or two; density (marketing scale versus tool scale); 16px or 17px body; whether the hero is product-led or type-led; and light or dark (dark needs weight compensation). Never reuse the previous project's face just because it worked [2].

## 1. Brand voice face vs workhorse face [13]

- [13] Don't let Inter, Roboto, Arial, Open Sans, Lato, Times New Roman or the OS, browser or design-tool default serve as the brand's voice. A neutral workhorse is fine for body and UI text under a display face that has character. One source attributes most of the "looks AI" impression to default type alone.
- [10] Choose a face specific to this brand. Audition at least 3 candidates with the real headline and real body copy, and let the headline type carry the brand. Judge them at display size in the hero, beside a premium player's page: the most crafted face wins over the most on-concept one, and a face drawn for function (cockpit displays, signage, terminals, government forms) reads utilitarian at 70px+, so it takes a narrow job rather than the display voice (synthesis). Never use Impact, Arial Black or the platform sans as the display voice. Load only the weights you use. Specify only a face you can load now (Google Fonts, Fontshare, or font files in the repo); if the right face is commercial, name it in DESIGN.md as the production target and ship a loadable stand-in of the same class that is not on a tell list, then confirm `getComputedStyle(h1).fontFamily` resolves to it rather than a fallback.
- [9] Counterweight: a whole UI in one well-made sans, with hierarchy from size, weight and colour, is the right call for native apps and dense tools (see Context rules 1-2).
- [4] Avoid novelty and trend faces (Comic Sans is the extreme case). Structurally classic families age slowest, for example Akzidenz Grotesk, Avenir, Caslon, Clarendon, DIN, Franklin Gothic, Frutiger, Futura, Garamond, Gill Sans, Helvetica, Sabon, Univers and Bodoni.
- [3] For brand text, prefer a licensed or commissioned face to preinstalled fonts and most free fonts. A custom face is a brand asset, and apple.com's proprietary type is felt even by visitors who can't name it.
- [3] Don't default to an oversized, often italic display serif in the hero. Use a sans display face unless the brand names a serif or the brief is truly editorial or heritage.
- [2] Don't replace one default with the next trending one; vary the face, theme and aesthetic across projects. A subject stereotype (books get a serif, dev tools get mono) never justifies a pick on its own.
- [2] When a UI looks generic, fix type first: set face, sizes and weights per role before touching colour or decoration. [3] Most UIs are text and buttons, so type is the 80/20 lever.

**AI-default font list.** Grep the CSS for these names.

| Tier | Faces / looks | Rule |
|---|---|---|
| A. Universal defaults [13] | Inter, Roboto, Arial, Open Sans, Lato, Times New Roman, `system-ui` as the voice, the design tool's default | Never the brand or headline voice. Acceptable as the body/UI workhorse. |
| B. LLM "distinctive" picks [2-3] | Space Grotesk, Instrument Serif, Instrument Sans, Fraunces, Geist, Syne, Bricolage Grotesque, Sora, Young Serif, Plus Jakarta Sans, DM Sans / DM Serif, Outfit, Playfair Display, Recoleta, Newsreader italic, Cormorant, Lora, Crimson, Space Mono, IBM Plex. Plus the next rotation, the a01/a05 Inter replacements: Satoshi, Clash Display, Clash Grotesk, Cabinet Grotesk, Geist Display | Not as the heading face, and not for more than 25% of page text, unless the brief names it or DESIGN.md gives a written reason. One accent word is tolerated. Geist and Outfit are contested (one source recommends them). |
| C. Spent combinations [4][3] | Instrument Serif italic on warm beige; cream + terracotta + serif display; Inter on slate-900; tiny tracked mono eyebrows | Never a default look. |

The [10] cluster's own examples (Space Grotesk, Playfair, Fraunces, Bricolage, Syne, Sora) overlap tier B. Where they clash, tier B wins: "uncommon" means specific to this brand, not new this season.

**Classes to look in, not picks.** Any named list becomes the next tell once agents reuse it, so select by procedure:
1. Name the classification the reference world points to (grotesk, neo-grotesk, humanist, geometric, condensed, wide, slab, transitional or Didone serif, mono for code), using the industry's own signage, packaging, period lettering or a regional foundry as the source.
2. Exclude tiers A and B above, the face the previous project used, and the faces of this skill's own fixtures (`scripts/fixtures/clean*.html`): they show that a page can be clean, not which face to use, and agents copy them (slop_check `fixture-face`).
3. Shortlist 3 loadable candidates (Google Fonts, Fontshare, repo files). At least one must come from outside every list in this skill, found through the reference world.
4. Set the real headline and body copy in all 3; write in DESIGN.md why the winner beats the other two for this brief.

Examples of where such searches land (illustrations, not defaults): commercial sans display such as ABC Diatype, Söhne Breit, PP Neue Montreal or GT Walsheim; serif display such as PP Editorial New, GT Sectra, Tiempos Headline or Canela when Context rule 3 allows a serif; Didone (Didot or Bodoni style) for fashion and luxury at 32px and up; mono for code and data such as `ui-monospace`, JetBrains Mono or Geist Mono.

## 2. Tracking (letter-spacing) by size [11]

- [11] Spacing that is right at one size looks loose at large sizes and cramped at small ones, so track against size:

| Role | Tracking | Reference values |
|---|---|---|
| Caps labels, tags, 11-13px | +0.03 to +0.1em | 12px caps at +0.06em; 13px eyebrow at +0.4px |
| Body, 14-18px | 0 | apple.com SF body -0.374px at 17px (reported, SF only) |
| h6 / h3 / h1 | -0.005em / -0.015em / -0.02em | |
| Display, 56px and up | down to -0.04em, never tighter | Linear -3px at 80px; Stripe -1.4px at 56px; apple.com -0.28px at 56px (reported) |
| 12px and below | never negative | |

- [11] In native apps that use the system font, never hand-track: the OS applies per-size tracking. Type the SF table in by hand only for static mockups (Figma, Sketch). SF tracking in 1/1000 em: 6pt +41, 10pt +12, 11pt +6, 12pt 0, 13pt -6, 15pt -16, 17pt -26, 20pt -23, 22pt -12, 24pt +3, 28pt +14, 34pt +12, 48pt +8, 60pt +4, 80pt and up 0.
- [2] Capitals are spaced to sit beside lowercase, so all-caps and small caps need extra tracking. Stay within +0.03 to +0.1em. The 0.18-0.22em tracked eyebrow is an AI tell (section 6).
- [2] When Inter substitutes for SF, retune it rather than dropping it in: -0.01em on display sizes, weight 600 for headlines, `ss03` (reported).
- Tailwind (std): `tracking-tight` is -0.025em (fits h1-h2). `tracking-tighter` is -0.05em, which breaks the -0.04em floor, so use `tracking-[-0.03em]`. `tracking-widest` is 0.1em, the ceiling for caps.

## 3. Semantic text styles and the type scale [8]

- [8] Define the text styles once (display, headline, title, body, label, caption; about 9-15 levels in all). Each style fixes family, size, weight, line-height and tracking. Use nothing else: no hand-tuned sizes, no one-off styles. In SwiftUI write `.font(.body)`, not `Font.system(size: 17)`.
- [7] Generate sizes from one ratio rather than by eye. 1.25 from 16px gives 20, 25, 31, 39px. Use 1.125-1.2 for dense dashboards and mobile. Keep 1.618 for a single headline-to-body jump, because over 4 steps it reaches 110px. Snap every size to the scale and delete fractional strays (in one cleanup, 12/14/16/18/20/24/30 replaced 11, 12.5, 13, 13.5 and 28).
- [5] Use units that follow the user's text-size setting: rem on the web, Dynamic Type styles on iOS. Custom fonts on iOS use `Font.custom(name, size:, relativeTo: .body)`. A fixed-size brand font stays put while system text grows, which inverts the hierarchy.
- [3] Make at least one jump dramatic: once per marketing page (usually the hero H1), display text 3x body or more, capped at about 6-8rem. A scale whose steps are all under 1.25x reads flat. [3] Headlines are at least 2x body and heavier than body.
- [2] Counterweight: section titles sit at about 2x body, not 5x. The hero H1 runs 2-3 lines; 4 lines means the size is wrong. Resolution on marketing pages (synthesis of this and the [3] dramatic jump): 2x body sits barely above a 1.2x lead and reads as a label, so section heads run 2.5-3.5x body (about 40-60px at 1440) and at least 1.5x their lead; 5x stays out (render_check `section-scale`). [2] Dense UIs work with about 3 sizes around a 14-16px base, from 12/14/16/18/20/24. Add levels with weight and colour before adding a size.
- Sizing the display token (synthesis of the [3] `clamp(2rem, 7.4vw, 5.5rem)` floor and the [2] `clamp(3rem, 5vw, 5.5rem)` H1 set in a full-width container): the size follows the column the H1 actually sits in and the length of the real headline, not a house number. A split hero's text column holds a smaller display than a full-width one. Check every width from 320 to 1440 (render_check reports H1 lines per size): at most 2 lines at 1440, at most 3 at 320-390. The 3x-body jump is measured at desktop width; phones may sit at 2-2.5x. A 1-3 word name that is the hero (a launch, a house, a venue) is sized as the visual, up to 8-15vw [5] (§10), and the specific sentence moves under it as a lead at 1.25-1.6x body; a sentence H1 capped at 4.5rem beside a product is the timid default that lost blind comparisons to a name set at 200px (synthesis). Break lines on phrase or sentence boundaries (per-breakpoint spans or `text-wrap: balance`); a sentence never ends mid-line with the next one starting beside it.
- [2] Choose the body face first and settle its size, leading and measure; the base of the scale is the size at which it renders crispest. [1★] On brand-led pages the display face can be auditioned first, but body metrics still set the base.

**Token table.** Text steps use 1.25 from 16px; values past 39px are derived from the ratio. Families, the exact ratio and the heading weights are decided per brief: 600 below is one option, not the default (Context rules 6-7).

| Token | Size | Line-height | Weight | Tracking |
|---|---|---|---|---|
| `--text-caption` | 0.75rem (12px) | 1.33 | 400 | 0 (+0.06em if caps) |
| `--text-label` | 0.875rem (14px) | 1.0 single line, 1.43 wrapped | 400-600 | 0 |
| `--text-body` | 1rem (16px) or 1.0625rem (17px) | 1.5 | 400 | 0 |
| `--text-title` | 1.25rem (20px) | 1.3 | 600, or 700 when weight is the only difference | -0.005em |
| `--text-h3` | 1.5625rem (25px) | 1.25 | 600 or 700 | -0.015em |
| `--text-h2` | 1.953rem (31px) in product UI and docs; marketing about clamp(2rem, 1.2rem + 2.2vw, 3.5rem), 2.5-3.5x body | 1.1-1.2 | 600 or 700 (300-400 for a light display face) | -0.015em |
| `--text-h1` | 2.441rem (39px) | 1.1 | per brief: 300-400, 600 or 700-900 | -0.02em |
| `--text-display` | sized to the real H1 in its column at 1440: a sentence up to about 6rem (e.g. clamp(2.25rem, 1rem + 4.5vw, 6rem)) while it fits 2 lines; a 1-3 word name that is the hero up to 8-15vw; floor 2-2.25rem | 1.0-1.1 (1.05+ at 3 lines; 0.9-0.95 for 1-2 line caps or condensed) | per brief: 300-400 light when the size gap is 2x+, 600 for most grotesks, 700-900 for condensed or poster faces | -0.02 to -0.04em |

```css
:root {
  --font-display: "Brand Display", ui-sans-serif, system-ui, sans-serif;  /* fallback of the same class */
  --font-text: "Brand Text", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; /* tail (std) */
  --font-mono: ui-monospace, "SF Mono", "JetBrains Mono", monospace;
  --text-body: 1rem; --leading-body: 1.5;
  --text-h1: 2.441rem; --leading-h1: 1.1; --tracking-h1: -0.02em;
  --weight-regular: 400; --weight-strong: 600;
}
h1 { font: var(--weight-strong) var(--text-h1)/var(--leading-h1) var(--font-display); letter-spacing: var(--tracking-h1); }
```
Tailwind's default steps (12/14/16/18/20/24/30/36/48px (std)) are not a ratio scale. Either redefine `theme.fontSize` from the tokens or restrict the project to a documented subset.

## 4. Families, pairing and face count [9]

- [9] Default: one clean, highly readable sans family across the whole interface, with hierarchy from size, weight and colour alone. Add a mono or serif companion only for code or long-form reading.
- [7] When there are two faces, take them from different classifications that share a mood: a display or serif heading over a sans body, a sans heading over a serif body, condensed with wide, or display with mono. Never two faces of one class or near-twins (Georgia + Times New Roman). Give each face a fallback from its own class.
- [6] One face is enough and two is the normal maximum. A third is the ceiling and gets one narrow job. Never use four. (Apple runs SF plus New York.)
- [5] Mono gets one narrow job: code, terminal output, IDs and hashes, timestamps, tabular data, and anything that must line up in character cells. Never paragraphs or marketing copy, and never eyebrows (Context rule 4). SwiftUI: `.font(.system(.body, design: .monospaced))`.
- [4] A display serif can set headlines, or only the emotional beats (welcome, success screens) while the functional UI stays sans. A high-contrast Didone reads as luxury. Context rule 3 bounds both.
- [3] Use a rounded variant (SF Pro Rounded, `design: .rounded`) only for a deliberately friendly tone or to match soft UI, never as the default. Sharp, square forms read as luxury and professional.
- [2] For a second style, use a superfamily or companion cut: Source Sans / Serif / Code, SF + New York (Apple platforms only), or Inter Display + Inter (Linear).
- [2] Never set paragraphs or small text in display, script or handwritten faces.
- [2] Use condensed or compressed widths only in tight spaces (watch faces, crowded nav bars) or to give display headlines presence. Never use them for body text on phone-sized screens and up. SwiftUI: `.fontWidth(.compressed)` on bold titles.
- [1★] Use New York (`design: .serif`) for long-form editorial reading and quotations, not as the general UI font.

## 5. Body size and platform floors [7]

- [7] Web body is 16-17px; reading text never goes below 15-16px. apple.com body is 17px/400/1.47 (reported). In apps, use the platform default: 17pt on iOS and visionOS, 13pt on macOS, 16pt on watchOS, 29pt on tvOS.
- [7] Absolute minimums: 11pt on iOS (Caption 2), 10pt on macOS, 23pt on tvOS, 12pt on visionOS and watchOS. Detail text that is too small or faint to read gets enlarged or deleted.
- [7] iOS Safari zooms into focused inputs below 16px, so set mobile inputs to 16px or more. Never disable zoom (`user-scalable=no`, `maximum-scale=1`).
- [2] Size text only as large as its job needs at the real output size. Keep scannable lists and directories compact rather than inflating them.

## 6. Case and eyebrows [7]

- [7] Default: no eyebrow label or pill badge above headings or the H1; put its words into the heading. The tell is `text-[11px] uppercase tracking-[0.18em]`, or mono at 10.5px with 0.22em, or a thin-bordered pill ("Introducing X"). Keep an eyebrow only when it carries information the headline doesn't (a product name above a tagline, an article category, a date), and use at most one per three sections.
- [4] Use all-caps only for short labels that fit on one line. Headlines, links, list items and alerts use sentence case. Show urgency with a coloured status pill, not "DUE IN 3 DAYS!!". Vercel uses sentence-case headlines ending in a full stop, with caps only in mono labels.
- [4] Don't use uppercase tracked text by default. One detector flags any uppercase run with letter-spacing of 0.5px or more.
- [1★] Never fake small caps. Without true small-cap glyphs in the font, don't use `font-variant: small-caps`.

## 7. Line-height [6]

- [6] Body about 1.5 (range 1.45-1.6). Headings 1.1-1.3. The largest display lines about 1.0. Pair tight, heavy headings with relaxed body copy. (Butterick's body range is lower: 1.2-1.45.)
- [3] Leading goes up as size goes down or lines get longer, and down as type gets bigger. Never use tight leading on 3 or more lines; keep it for 1-2 line rows. A serif body gets slightly more leading and measure than a sans.
- [2] Write line-height unitless (`1.5`, not `24px`): body 1.5-1.6, h1 about 1.1, single-line labels 1.0.
- [2] When substituting a face, retune leading for its x-height. Inter's taller x-height takes body 1.44 where SF uses 1.47 (reported).
- [1★] Set explicit leading on every style; the design tool's "Auto" is tuned for body and runs too loose at display sizes. Italic display words with descenders need at least 1.1 plus a small bottom reserve, because `leading-none` clips y, g, j, p and q.
- Reference: iOS size/leading in pt: Large Title 34/41, Title 1 28/34, Title 2 22/28, Title 3 20/25, Headline 17/22, Body 17/22, Callout 16/21, Subhead 15/20, Footnote 13/18, Caption 1 12/16, Caption 2 11/13. apple.com: display 1.07-1.19, body 1.47, footer link stacks 2.41 (reported).

## 8. Weight, colour tiers and emphasis [5]

- [5] Titles and key values are bold and at full contrast. Supporting text is smaller, Regular and muted (about 65-70% of text contrast). Supporting text never outweighs its title, and every repeated pair uses the same treatment. Example tokens: light mode text hsl(0 0% 5%) with muted hsl(0 0% 30%); dark mode 95% with muted 70%. "Supporting" means metadata, captions, labels and a one-line description under a list title. Leads, story paragraphs, instructions and anything read for meaning stay at full ink; if most running text is muted, the page drifts into grey trend-minimalism [3] (synthesis; render_check reports the muted share and flags it above half).
- [4] Regular 400 sets body and nearly everything else; SemiBold 600 (or Bold) sets headlines and emphasis. Use 2-4 weights per product and at most 2 per screen. apple.com uses 300/400/600/700 with no 500, and 300 only for large, airy leads of about 24px (reported).
- [3] Use 2-3 text tiers. Emphasise key text by dimming what surrounds it, not by restyling the key text. Muted tiers still pass 4.5:1: #6e6e73 on white is about 5:1, black at 60% about 5.7:1, and black at 40% about 2.8:1, which fails.
- [3] For a level at the same size, use the emphasised variant through its token (iOS Headline 17pt Semibold over Body 17pt Regular), so write `.font(.headline)`, not `.body` plus `.bold()`. Emphasised Large Title, Title 1 and Title 2 go Bold; Title 3 and smaller go Semibold.
- [3] No Ultralight, Thin, Light or Black below about 20pt. Keep extreme weights for display sizes, and set any thin weight larger than default. (iOS 7's light Helvetica Neue is the cautionary case.)
- [2] On dark, translucent or busy backgrounds, go up one weight tier (Regular to Medium) and add a little leading and tracking. Small labels on glass may take at most a `0 2px 4px rgba(0,0,0,0.15)` shadow.
- [2] Use bold and italic sparingly; don't bold every heading. [1★] Never underline for emphasis, because underline means link.
- [2] When a headline or key figure is already much larger than its surroundings, its weight can drop (Bold to Regular or Light); see Context rule 7.
- [1★] Never let a translucent bar or overlay sit over body text so that text stacks on text (NN/g on the iOS 26 Mail search bar).

## 9. Optical sizing [5]

- [5] Match the cut to the size: the Text cut below 20pt and the Display cut at 20pt and above (40pt on a 1x/72dpi canvas), or let a variable font's `opsz` axis handle it. On the web, keep `font-optical-sizing: auto` (std, the CSS default). In UIs that span many sizes, prefer faces with optical sizes, since a face without them looks right at one size only.
- [1★] For small screen text, choose faces with open apertures on a and e, long descenders, wide f and t crossbars, and i-dots clear of the stem. Test at 1x and on TVs as well as Retina screens.

## 10. Display type and headlines [5]

- [5] Display type can be the main visual of a hero: a headline or wordmark at nearly the full viewport width, crossing or sitting behind the product, cropped at the edges. Push the scale past "correct" before refining. Context rule 8 sets when type is the star.
- [3] Each page gets exactly one H1, the largest and boldest text, stating what the page is about. A clearly smaller secondary line and the CTA sit below it, and H2s divide the rest.
- [3] Set big hero headlines in a condensed or normal-width heavy face, not an ultra-wide extended one (an extended face clipped a word at mobile width). Size them with `clamp(2rem, 7.4vw, 5.5rem)` so no word overflows at 390px.
- [3] To split a headline, use a muted lead-in line that names the feature over a bright statement line, or light against bold weights of the same face.
- [3] Don't accent one word of a headline with serif italic, a second colour, gradient text, a highlighter background or an underline. Get emphasis from size or weight (Context rule 10).
- [2] Write headlines as short statements of 2-6 words ending in a full stop, stacked over 2 or more short lines (Apple's pattern).
- [1★] Balance multi-line headings with `text-wrap: balance` (Tailwind `text-balance`), and use `text-wrap: pretty` on paragraphs to avoid one-word last lines (Vercel). render_check `orphans` lists headings and leads that still end on one word.

## 11. Measure and alignment [3]

- [3] Cap body text at 65-75 characters per line (`max-width: 70ch`) and never exceed 80. Butterick's range is 45-90 including spaces. Data tables may run to 120ch or more. Longer lines need more leading. Tailwind `max-w-prose` is 65ch (std).
- [2] Set running text flush left, ragged right; never force-justify body copy. Stacked text blocks share one left edge.

## 12. Numerals [3]

- [3] Use tabular figures for numbers that are compared or that change: prices, stats, counts, timers, animating values and table columns. CSS `font-variant-numeric: tabular-nums` (Tailwind `tabular-nums`), OpenType `tnum`, SwiftUI `.monospacedDigit()`. Numbers inside running text keep the default proportional figures. Stripe pairs `tnum` with slight negative tracking on numeric captions (reported).
- Where a face's tabular cut widens punctuation ("2 . 6 kg"), keep `tnum` where digits align in columns or update in place, and let a lone figure (one hero price) use proportional lining figures, `font-variant-numeric: lining-nums` (std). Values in a row sit in fixed grid tracks, never spaced with non-breaking spaces; one unit and duration format runs through the product ("2 h 30 min" everywhere, never "2h 30m" beside "45 min"), written into DESIGN.md (synthesis).
- If the only need is aligned digits, use tabular figures in the main face, not a mono face.
- [1★] Size number containers for the longest realistic value, not the sample ($3,782.48 became $1,633,782.48).
- [1★] Set fractions as real fraction glyphs (½, or `font-variant-numeric: diagonal-fractions` (std)), not as full-size digits with a slash.

## 13. Micro-typography [2]

- [2] Use real characters: curly quotes “ ” ‘ ’, downward apostrophes (’90s), primes only for feet and inches (6′ 2″), the … glyph (also in "Saving…" and in menu items that open further input, "Rename…"), and correct hyphens, en dashes and em dashes, never `--`. Write ™ ® © instead of (TM), (R), (c). Put non-breaking spaces in "10 MB" and "⌘ K". Resolution with the em-dash tell [3]: this rule is about not faking glyphs; UI and marketing copy still carry no em dashes, and ranges take an en dash or a hyphen, one choice per product (synthesis).
- SVG text is set in drawing units: its rendered size is font-size x (rendered width / viewBox width), so an 11-unit label in an 890-wide drawing shown 690px wide is 8.5px. Every label must render at 12px or more at every width (render_check measures it); use HTML labels positioned over the drawing, or a separate label set per breakpoint (synthesis).
- [2] Keep kerning on: `font-kerning: normal`, or `text-rendering: optimizeLegibility`.
- [2] Give links a style distinct from body text. Kinds can be told apart by underline style, for example solid for objects and dotted for people or defined terms.
- [1★] To scale or animate text, animate a wrapper element rather than the text node, adding `translateZ(0)` or `will-change: transform` if rendering blurs (Vercel).
- [1★] Use one space between sentences (Butterick).

## 14. Platform defaults, loading and licensing

- **Web:** body 16-17px in rem. To render the platform system face (native-feeling tools only, never as a brand voice), use `system-ui, -apple-system, BlinkMacSystemFont`, which renders SF only on Apple devices; Windows gets Segoe UI and Android gets Roboto. A brand that needs one voice everywhere needs its own licensed web font.
- **iOS / iPadOS:** SF Pro through the text styles in section 7. Dynamic Type runs Body from 14pt (xSmall) to 53pt (AX5); test the largest accessibility sizes, long strings and other languages. Use SF Compact on watchOS (system-chosen), New York via `design: .serif`, and SF Mono via `design: .monospaced`. Use the full style vocabulary, not one or two styles.
- **macOS:** Body 13/16, Headline 13/16 Bold, Title 1 22/26, Large Title 26/32, Caption 10/13 (pt). There is no Dynamic Type. Use the dynamic system font variants (e.g. `controlContentFont`) for text that sits next to standard controls.
- **tvOS / visionOS:** tvOS body is 29/36 with Medium as the base weight, and Title 1 is 76/96. visionOS uses bolder body and title styles, with Extra Large Title 1 and 2 for editorial layouts. Keep readable text flat (2D).
- **Loading [2] (Vercel):** preload the critical font (`<link rel="preload" as="font" crossorigin>`, crossorigin (std)), subset it with `unicode-range`, use `font-display: swap`, keep variable axes to those used, and preconnect to font CDNs. Load only the weights you use [10], and give each face a metric-compatible fallback (`size-adjust` / `ascent-override` (std)).
- **Licensing:** never embed or ship the system fonts in an app; reference them through the system font APIs [1★ HIG]. SF Pro may not be self-hosted as a web font on a non-Apple website (conflict log). Apple's SF, New York and SF Symbols licences cover UI and mockups for Apple platforms only (std); `ui-serif` renders New York only in Safari on Apple devices. Google Fonts faces are mostly SIL OFL, so self-hosting is allowed (std). Commercial foundry web licences are usually separate from desktop licences and priced by traffic, so confirm before shipping (std).

## Context rules (from the conflict log)

1. **Brand face vs one system sans.** Decide by layer and surface. On marketing sites, brand surfaces and web products, headings take a well-made face with character (a licensed foundry face, or a loadable stand-in of the same class until it is licensed; section 1): unusual in its category, classic in structure, ideally with optical sizes. Body and UI use the same family's Text cut (Apple's method) or a neutral workhorse. In native iOS and macOS apps, SF through system text styles wins outright, with the brand face limited to a few display moments (onboarding, large titles, empty states); that face differs from SF in class or construction (serif, condensed, rounded, a strongly stylised cut), because a second grotesk beside SF is a near-twin [7]. An HTML mock of a native app is viewed on every OS: a bare `-apple-system` stack shows Inter or Segoe UI off Apple devices, so set its titles in a loaded face or document the stand-in. One neutral sans with tabular figures also wins in dense data tools.
2. **Face count.** Default to one family with optical sizes and 2-3 weights. Add a second face only for (a) an editorial, literary, luxury or heritage voice that is a serif display, or (b) mono for code and data, which doesn't count as a brand voice. The ceiling is two voices plus mono. Cut any face that is there only to look "designed".
3. **Serif display.** Sans display is the default for tech and product work. A serif fits only a genuinely editorial, literary, hospitality, fashion/luxury or heritage brief. Even then it is upright, not italic; not from the overused pool (Fraunces, Instrument Serif, Playfair, Recoleta, Newsreader italic); on a cream ground only with a written reason (cream is valid only when the subject is made of it) and never with a terracotta accent; and used throughout, not as an accent word. A Didone only at about 32px and up, where its hairlines survive. Inside product UI, a serif may own a few emotional beats.
4. **Mono.** Use it only for content that is literally code-like or must align in character cells. Never for eyebrows, section labels or marketing captions, even on developer products. For aligned numbers, use tabular figures in the main face.
5. **Scale ratio vs dramatic jumps.** Use one named ladder, which need not be geometric. Text and UI steps stay tight: 1.125-1.2, or the platform ladder exactly. Display steps jump: headline at least 2x body, and one display size at least 3x body per marketing page at desktop width (usually the hero H1 or the name; marketing section headings 2.5-3.5x body, never 5x [2], section 3), as fluid `clamp()` tokens sized to the real column (section 3) and capped at about 6-8rem. Go near viewport width only for a single wordmark or name moment. Product UI keeps a fixed rem scale with no fluid headings, and dense dashboards skip the 3x jump. Every size, display included, is a token; in a native app or its mock, the platform ladder overrides the web leading and weights-per-screen rules.
6. **Weight steps.** Default to 400/600, which in practice comes with a size or colour difference as well. When weight is the only difference at the same size and the semibold is subtle, use 400/700. Extreme pairs (thin against black, 100-200 against 800-900) only above about 32px. Use 2 weights per screen and 2-4 per product. Display weight is a per-brief choice written into DESIGN.md: 300-400 when the size gap is 2x or more [2], 600 for most grotesks (apple.com's repeated headlines use 600, a10 [1]), 700-900 for condensed or normal-width poster heroes [3]. The tell is a reflexive 700+ on a wide face not drawn for it.
7. **Heavier or lighter when large** (not in the conflict log; resolved here). The headline is heavier than the body by default [3]. A light weight at large size [2] is allowed only when the size gap is already 2x or more and the text is one intro title or one key figure.
8. **Type vs product as the hero.** One star per view. A visually strong product is the largest element, and the type supports it. Type is the star when there is no strong visual (services, abstract software, a name reveal), or it joins the product as one focal unit: the wordmark behind it, or a name at display scale beside a full-height product panel (a launch, a house, a venue). Make type huge because it is the subject, never to fill space. Rotated type belongs only in campaign or poster work. The nav logo stays small.
9. **Body size vs density.** Reading text stays at 16-17px on the web (13pt on native macOS). Dense UIs may drop secondary and data text to 13-15px with a 1.125-1.2 scale. The primary data point and any running text stay at 15px or above, and nothing goes below the platform minimum (11pt iOS, about 12px web).
10. **Headline emphasis.** Spot colour goes on the focal object or action, not on a headline word. A coloured, italic-serif or gradient word is a strong AI signature. The exception is campaign or poster art where the word is the subject (a product name, a colourway): once per site, in a solid palette colour, never gradient. Apple's two-tone device works because the muted lead-in is its own line in the same face.
11. **Display leading.** Default to 1.0-1.1. Go to 0.9-0.95 only for 1-2 line headlines in all-caps or a condensed face, where ascenders and descenders can't collide. Anything that wraps to 3 or more lines gets 1.05 or more. Body stays at about 1.5.
12. **Eyebrows and caps tracking.** No eyebrow by default (section 6). Short caps tags take a modest +0.03 to +0.1em; 0.18-0.22em is the tell. Heading and body tracking rules are unaffected.
13. **Muted text.** Muting may go down to the AA floor (4.5:1 for body, 3:1 for large text) and never below. 40% opacity is only for states WCAG exempts, such as disabled. Check muted tiers in both themes and on tinted surfaces.
14. **Trend vs timeless.** "Uncommon" means specific to this brand's world, not new this season. Choose a structurally classic, well-made face and use it in an unexpected context. Test it: would it still look deliberate in 5 years, and would you choose it if no competitor were using it?

## Checks (verifiable in code or a screenshot)

- [ ] `font-family` on h1/h2/display is not a tier A face, and not a tier B face unless the brief names it or DESIGN.md gives a reason. No tier C combination is present. The computed face is the loaded one, not a fallback.
- [ ] Face count: at most 2 families plus mono. Mono appears only in `code`, `pre`, `kbd`, IDs, timestamps and data cells, never in eyebrows or headings.
- [ ] Every `font-size` resolves to a token or text style. No px or pt literals in components. No fractional or off-scale sizes. SwiftUI has no `Font.system(size:)` for text that has a semantic style.
- [ ] Body text is 16px or more on the web (17pt iOS, 13pt macOS). Nothing is under 12px on the web or 11pt on iOS. Mobile inputs are 16px or more. Zoom is not disabled.
- [ ] `letter-spacing`: negative values only at about 20px and above, none at 12px or below, none tighter than -0.04em. Uppercase runs sit between +0.03 and +0.1em, with no 0.18em-plus eyebrows.
- [ ] `line-height` is unitless. Body is 1.45-1.6. Display is 1.0-1.1, and headings that wrap to 3 or more lines are at 1.05 or above. No `leading-none` on italic display words with descenders.
- [ ] Paragraph containers have `max-width` of 75ch or less (never more than 80ch). No `text-align: justify` on body copy.
- [ ] Each screen uses at most 2 weights. No weight of 300 or less below 20px. Supporting text never outweighs its title.
- [ ] Muted text tiers measure 4.5:1 or better in light and dark themes and on tinted surfaces.
- [ ] Prices, tables, counters and timers have `tabular-nums` (or `.monospacedDigit()`).
- [ ] One H1 per page. The hero H1 wraps to 2 lines or fewer at 1440px and 3 or fewer at 320-390px, breaks on phrase boundaries, with no overflow. Headline is at least 2x body. A marketing page has one display size at least 3x body at desktop width (usually the hero H1 or the name), and section headings run 2.5-3.5x body and 1.5x+ their lead; dense tools and docs are exempt. Headings carry `text-wrap: balance`, leads `pretty`.
- [ ] Rendered SVG labels are 12px or more at every width; muted text holds metadata and captions, not the running copy.
- [ ] The display face is not a fixture face of this skill and not the previous project's face.
- [ ] Display weight matches the per-brief choice in DESIGN.md.
- [ ] No headline has 2 or more styled runs (italic-serif word, gradient text, second colour) outside the one-per-site campaign exception. No all-caps run is longer than one line. Headlines are in sentence case.
- [ ] Copy uses curly quotes, … and real dashes. No straight `'` or `"` in prose, no `...`, no `--`.
- [ ] Only the weights in use are loaded. `font-display: swap` is set, critical fonts are preloaded, and SF is not self-hosted on a non-Apple site.
- [ ] Squint test on a screenshot: the headline face reads as specific to this brand and cannot be guessed from the product category alone.
