# Layout, spacing and hierarchy

Tags: `[N]` = N independent creators state the rule. `[1★]` = one canonical source, or one source that fills a gap nothing else covers. `(std)` = a widely accepted standard value that is not in the research. `(synthesis)` = an ordering or resolution written for this skill where the data gives none. For method, counts and backers, see [evidence.md](evidence.md).

## Summary

- Use generous whitespace by default [16]. Set every gap by relationship, inner < group < section, with each level at least 2x the one below [14]. Take all values from one 8-based token scale [11].
- Give each view one focal point and at most 2 prominent elements, and keep everything else quiet [8]. Every element must earn its place [8].
- Rank the elements before styling them. Express rank mainly through size [4], and aim space, weight and colour at the same element [4].
- Don't assemble the category's stock section sequence [14]. Give each section one subject and its own format, all on a shared grid and a shared text edge [7].
- Density is decided per surface: generous for marketing, and compact for tools and dashboards using the lower steps of the same scale [3].

## 1. How much whitespace [16]

- [16] On premium, marketing and editorial layouts, use roughly 2-3x the whitespace of a standard interface. Leave empty areas empty. Never enlarge text, add a background layer or add elements to fill a gap. A page whose content ends two-thirds of the way down is finished, not under-filled. Whitespace is space around a group, not a hole inside a row: a column that stops far above its neighbour is a layout fault (§6), not generosity (synthesis).
- [16] Don't shrink vertical space in proportion to width on mobile; the sources add vertical room there.
- Reference values: desktop section padding of 80-160px (`py-20` to `py-40`). Apple's generous whitespace is backed by [4]; its exact measurements come from a single extracted source (a10): 80px section padding, at least 64px above a headline, 48-64px below it, at least 40px around product images, and 24px card padding. Linear and Claude use 96px section padding.
- Padding per side vs the gap between sections (synthesis of [16] and [14]): padding applies to each section, so two 128px-padded sections on one ground leave 256px of empty ground between their content, which reads as dead air, not luxury. Measure the visible gap from one section's last content to the next section's first content: 96-160px on one continuous ground (48-80px padding per side); a band with its own ground carries 80-160px of padding inside it, and the ground change does the separating.
- [5] Apple lets one viewport hold one short headline plus at most a brief paragraph (about 3-6 lines). The product and its imagery carry the rest.
- [3] Give the single most important element the most surrounding space. Isolation is the cheapest emphasis there is.
- [2] Strip each view to the fewest elements and the fewest requested actions, and leave the freed space empty on purpose.
- [3] Guard against trend minimalism. A light-grey canvas with a small headline, tiny grey text, a black pill and no colour is itself a template. Whitespace reads as premium only next to strong hierarchy: confident type size, a real product or image, and full-contrast primary text. Fix a flat result by raising scale and contrast, not by adding elements.
- Decide per brief: the density level (section 8), which element owns the space, and whether the voice is airy and editorial or dense and utilitarian. "Generous" does not mean every section is a single sentence in a full viewport.

## 2. Spacing by relationship [14]

- [14] Never use one uniform gap. Spacing must increase strictly from lines to elements to groups to sections:
  - inside a group: 4-16px, with a label 4-8px from its input
  - between groups: at least 2x the inner gap (24-80px; one source uses 8/16 inside and 64/80 between)
  - between sections: about 32px on mobile app screens and 80-96px or more on desktop marketing pages
  - no element may sit equidistant between two groups
- [5] Bind each heading to its content:
  - title to subtitle is the smallest step
  - heading to body is at most 1-1.25x the heading's own height
  - the space above a heading is 2-3x the space below it
  - subtext to buttons is at least 2x headline to subtext
  - measure and set every one of these instead of accepting tool defaults
- [3] Set spacing from the outside in, so each nested level is tighter than the one around it. A worked app example: 24px screen wrapper, 32px between sections, 24px from section title to content, 16px card padding, 8px between buttons and tags, and 6px between tightly coupled elements, which is the floor; touching or 1px gaps read as mistakes.
- [2] Specify padding (inside) and gap (outside) as separate tokens, and reuse the same pair on every instance of a component (flex/grid `gap`, Figma auto layout).
- [1★] (Hobday) A container's padding must be greater than or equal to the gap between its children, so the children read as closer to each other than to the edge.
- [1★] (Kennedy) Pad a vertical menu item by about 1x its text height above and below (12px text gets 12px padding). In a top bar, the text is about 20% of the bar height.
- [4] Space optically, not by bounding boxes:
  - Measure from visible edges.
  - Remove the line-box excess from top padding, so a pill or badge looks as far from its top edge as from its left. Use CSS `text-box: trim-both cap alphabetic` where supported (std).
  - Centre icons and odd shapes on their optical centre.
  - Nudge about 1px where perception beats geometry.
  - Build these corrections into components once, never per page.

## 3. Layout variety instead of stock sections [14]

- [14] Don't assemble the category's stock sequence. For SaaS that is: announcement bar, pill badge, gradient hero with a mock, logo cloud, stat strip, 3 identical feature cards, a "3 simple steps" stepper, testimonial cards, 3-tier pricing with the middle tier highlighted, CTA strip, 4-column footer and chat bubble. Derive the sections from this page's content, and give each one its own moment of interest.
- [7] Don't build a feature grid of identical rounded cards (a 3-up, a 3x2 or a 4-6 tile bento), each with an icon on top, a bold title and a one-line promise. Use the content's own shape instead: real product visuals, 2-column alternation, an asymmetric grid, or a pinned scroll section. Put icons beside headings, not in a tile above them.
- [4] Reject template hero skeletons, even in a new visual skin:
  - the centred SaaS hero: pill eyebrow, two-tone headline, subline, pill CTA plus a ghost "Watch demo" button, stat row, icon grid
  - copy left and image right, with a badge row
  - a centred headline over a row of equal cards
  - change the structure, not just the styling
- [3] No big-number hero or banner (3-6 large figures with small labels) unless real data backs the figures. Put a real number inside the section whose claim it supports.
- [2] Apple's layouts are both structured (everything on the grid) and exploratory (each chapter changes format). The feature chapters rotate through formats:
  - a full-bleed video with one centred line
  - a product alone in an empty viewport beside one small paragraph
  - an editorial block: eyebrow, a huge left-aligned headline, body offset into the right half
  - exploded-part callouts on grid columns
  - a staggered two-image grid
  - a bento of real product crops
- [2] Make scattered compositions secretly structured. Snap callouts and objects to grid columns, put large objects low and small ones high, and keep a clear margin around the text.
- [2] Compose the first viewport as a poster: one dominant image and one idea. Borrow a print archetype that fits the business (magazine cover, dossier, newspaper, fashion editorial) instead of assembling components.
- [1★ gap-fill: Taste Skill a05] Variety quotas, advisory only (the binding rule is the [14] "never repeat one section pattern"):
  - use each layout family at most once
  - an 8-section page uses at least 4 families
  - no more than 2 consecutive image/text alternating rows
  - break up a third split with a full-width, stacked or bento section
- [1★] Asymmetric fractional grids give print-like placements, for example `grid-template-columns: 2fr 1fr 1fr 2fr` (Andy Clarke a47, gap-fill). Change proportions between breakpoints by editing only `grid-template-columns`.
- Decide per brief: which sections exist (each must answer a question the visitor actually has), their order, and the one signature format the page is remembered for.

## 4. Spacing scale tokens [11]

- [11] Use one fixed scale stored as tokens. Never eyeball a value and never use a one-off pixel value. The consensus scale is 8-based with 4 as a half-step: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128. Use a 16px root and step in 0.5rem.

```css
:root {
  --space-1: 0.25rem;  /* 4  */  --space-2: 0.5rem;  /* 8  */  --space-3: 0.75rem; /* 12 */
  --space-4: 1rem;     /* 16 */  --space-6: 1.5rem;  /* 24 */  --space-8: 2rem;    /* 32 */
  --space-12: 3rem;    /* 48 */  --space-16: 4rem;   /* 64 */  --space-24: 6rem;   /* 96 */
  --space-32: 8rem;    /* 128 */
  /* semantic aliases: tune these per surface (section 8), not the raw scale */
  --gap-inner: var(--space-2);  --gap-group: var(--space-6);  --gap-section: var(--space-24);
}
```

- Tailwind: one spacing unit is 4px (std), so stay on steps 1, 2, 3, 4, 6, 8, 12, 16, 24 and 32 (`gap-4`, `p-6`, `py-24`). No arbitrary values such as `p-[13px]` or `mt-[22px]`.
- [11] Size controls from the same scale: 40px buttons, 32px pills, 16 or 24px icons.
- [11] On widths not divisible by 8 (for example the 375pt iPhone), keep padding on the scale and let one block stretch.
- Off-scale values: if a value is needed once, it is probably wrong; if it is needed twice, add it as a token.
- [2] Alternative: a ratio-based modular scale. Take a base and a ratio (for example 1.618) and derive spacing, type, measure and column widths from it. Small steps are 0.128, 0.272 and 0.618em; large steps are 1, 1.618 and 2.618em. Pick one system per project and never mix it with the 8-scale on the same axis (synthesis).
- Decide per brief: the base unit stays 4/8, but the section-level steps (64/96/128/160) are tuned to the brand's density.

## 5. One focal point per view [8]

- [8] Each screen or composition gets one dominant focal point and at most 2 large elements, with no more than about 3 deliberate stops (for example headline, product, brand). Concentrate boldness in one place.
- [8] Every element must earn its place. Cut decorative wordmarks, sparkle doodles, sticker cards, pill clusters, stat strips, icon rows, boxed promos and mini charts that repeat a motif. Borders, eyebrows, numbering, dividers and pills appear only where they say something about the content.
- [5] Limit the first viewport to the brand, one short headline, one supporting sentence, one CTA group (a primary plus at most one text link) and one dominant image or video. Keep stats, schedules, promos, metadata rows and redundant eyebrows out. The aim is that who you are and what you do land in about 3 seconds. Exception (synthesis): a local venue's first viewport also carries hours, address and the book/order CTA, because what, where and when is what its visitors came for (SKILL.md section 7).
  - Apple's stack: product name, one-line tagline, "From $price", a Buy pill, then a "Learn more >" link.
- [4] Scale the focal subject huge: about half the canvas or more, cropped or bleeding off the edge, set against small type.
- [3] Keep the logo, wordmark and secondary icons small: the logo small at top-left, list and link icons at 16-24px.
- [2] Derive the focal point from the page's one task or message. State it explicitly when prompting, because a model cannot infer what matters.
- One title-level element per view (synthesis of [8]). A large page title and a hero datum (a 64px number) compete; when a datum is the focal point, use an inline or small title, or fold the label into the datum ("12.4 km walked"). A label set above a datum counts toward the eyebrow budget [7]. One object keeps one name on every screen.
- Keep read-only content about one subject contiguous (synthesis of the grouping rules [14][5]). A prompt for input goes before it or after it, never between two halves of it. Solve a fold problem by removing or condensing, not by interleaving.
- [2] On homepages, use one dominant hero and then a short row of smaller entry points (Apple: 1 hero, 2 sub-heroes, about 6 tiles, footer), never competing text blocks with link sidebars.
- [2] Squint before shipping. The first thing the eye lands on must be the most important item, not merely the heaviest or most colourful block.
- Decide per brief: what the star is (the product, a place, a person, the live UI, or the type itself). See context rules 2-3.

## 6. Alignment and grids [7]

- [7] Align every element to at least one other along a shared axis: a grid line, an edge, a baseline or an optical centre. That includes chrome such as sidebar labels, icons and tab rows. Verify by drawing guide lines along the edges.
- [5] Design and verify every breakpoint: phone, tablet, laptop, ultra-wide (simulate at 50% browser zoom) and resized windows.
  - Recompose for each one (stack columns, collapse the nav, reorient strips) while keeping one visual system.
  - Respect `env(safe-area-inset-*)` and avoid stray scrollbars.
  - [2] Work mobile-first: the base is a single column in normal flow, with grids added at about 30em, 48em and 64em.
- [4] Keep the frame, the grid, the primary actions and the key controls in the same position on every screen and step (for example Back/Next at bottom-right on every step).
- [4] Use one shared text edge, normally the left, for the heading, header controls and content, and keep it from section to section. Centre only short display text. Never centre body copy, and never centre a title over left-aligned content.
- [3] Use a column grid: 12 columns on desktop, 8 on tablet, 4 on mobile. 12 divides into 1, 2, 3, 4 and 6.
- [3] Keep body text at 45-90 characters per line, targeting about 65 (`max-width: 65ch`). Put the page in a max-width container of about 1080-1440px that turns extra width into margin. Rauno uses 1080px as 3 x 360px columns; Apple measures about 980px for text and about 1440px for grids.
- A lone reading column on a wide desktop (synthesis): either it shares its row with something that earns the other columns (the drawing of the step, the tool, the product), or it sits deliberately on the grid (for example columns 4-9 of 12) with its text still left-aligned. A 65ch column against the left edge with half the viewport empty beside it reads as a blog post dropped into the page.
- A split hero's two columns end within about a quarter of each other's height, or the taller one (usually the UI) crops at the fold (synthesis); a short text column beside a tall panel leaves a dead corner. The same holds for every two-column section: balance the columns, centre the short one on the tall one, move the heading above the row as a full-width head, or stack. A sticky short column only hides the hole while its content fills most of the view. render_check `dead-column` flags a top-aligned column that ends 160px+ (and a quarter of the row) early (synthesis threshold).
- [3] Viewport side padding is at least 16px (24-32px ideal). Padding inside bordered or filled containers is at least 8px (12-16px ideal). Keep elements out of corners unless they deliberately bleed.
- [3] Pin secondary metadata (price, time, location) to a right-aligned column opposite the title, and fade overflowing text out before that column.
- [2] Align peripheral elements (logo, nav, side labels, social icons) to one inset frame. Align horizontal runs on the strongest line, either the baseline or the cap height.
- [2] Give repeated items identical dimensions, a common edge and equal gaps along one axis.
- [1★] (Rauno) Components respond to their container, not the viewport: `container-type: inline-size;` with `@container (max-width: 560px)`.
- [2] At accessibility text sizes, switch horizontal rows to vertical stacks (SwiftUI: `if dynamicTypeSize.isAccessibilitySize { VStack } else { HStack }`) and use fewer text columns. [1★] (HIG) Never truncate at large sizes, and keep the relative hierarchy intact when text scales.

## 7. Section rhythm and length [5]

- [5] Break dense content into self-contained, well-spaced modules of about 5-9 items, so people can scan and jump between them instead of reading top to bottom.
- [3] Give each section one subject: a short headline and a small text block paired with one image or video, repeated down the page as chapters. Each section has one job: explain, prove, deepen or convert.
- [3] Stack a section as a large heading, then a short muted paragraph (65ch or less), then a single CTA, so it reads before the imagery. Split the headline left with an explainer right only when the right column holds a visual or an interactive element; heading-left/paragraphs-right in every section is one repeated pattern that leaves a void under each short heading.
- [3] The hero fills the first viewport:
  - `min-height: 100dvh`, or `calc(100svh - <header height>)` under a sticky header
  - never Tailwind `h-screen`
  - top padding no more than `pt-24`
  - a headline of 2 lines or fewer, subtext of 20 words or fewer, and 1-2 CTAs, all visible without scrolling
- [2] One separation method: full-bleed bands of surface colour instead of divider lines. Bands touch with 0 gap, and the same surface never appears twice in a row (Apple: light, dark #272729, light, then #f5f5f7). Whitespace alone, a full-bleed image or a hairline are equally valid methods; choose one per page and record it in DESIGN.md. Banding across the brand's 2-3 tiers (one inverted band plus one raised band) is still one method; mixing it with hairlines at the same transitions is two. In apps, give the sidebar, the content and any map clearly different tones.
- Inverted and pinned sections (synthesis): an inverted (dark on light) band is a rhythm accent, so keep it near a quarter of the page height or less (render_check reports the share); past that, the page has become a dark page and must be justified as one (color.md C5). A scroll-pinned sequence spends about 0.6 viewport of scroll per step, and its pinned visual fills at least half the viewport height on desktop and a third on phones; otherwise un-pin it and show the stages as a row. Give every beat the same scroll distance [1★] (motion.md §7).
- Section heads vary too (synthesis): no more than 2 consecutive sections share one head layout (2-line H2 plus a muted paragraph, top-left). Alternatives: the head beside the module, the head inside it, a plain label, or no head when the module explains itself.
- [2] Plan the sequence as a narrative before building. The minimal default is hero, support, detail, final CTA. Add proof, pricing or FAQ only when visitors need them (context rule 12).
- [1★] (Hobday) Never stack two hard divides, such as a rule at a background change or a container edge. Remove one.
- [1★] (Butterick) Mark paragraphs with either a first-line indent (1-4x the point size) or 4-10pt of space between them, never both.
- Decide per brief: page length (short is fine), the surface sequence, and which section, if any, flips to dark or brand colour.

## 8. Density by surface [5]

- [5] Keep navigation and chrome subordinate to the work. Dim the sidebar a few notches while keeping it legible, shrink headers, greetings and page titles, and make the content the focal point. [1★] (Linear) The sidebar plus top bar forms an inverted L that users touch on every screen, so refine it first.
- [4] Judge simplicity by ease of use, not by element count. Reduce noise (icons, separators, contrast) while keeping information density, and don't hide functions in overflow just to look minimal.
- [4] A single decision point shows at most 4 visible options: one dominant action, 1-2 secondary ones, and the rest in a menu.
- [3] Choose density deliberately for the audience and the task. Build compact layouts from the smaller steps of the same scale, never by deleting the relationship ladder.
- [3] Make frequent targets large and place them near the user's focus or at screen edges. Never compress toolbars or tab bars.
- [2] The top bar is one line, 64-72px tall (80px at most). Reported Apple values: 44px global nav and a 52px sticky local nav.

| Surface | Section gap | Group gap | Inner gap | Text | Note |
|---|---|---|---|---|---|
| Marketing, product story, editorial | 80-160px desktop | 24-80px | 8-24px | body 16-17px | one idea per viewport for known brands; unknown brands keep specs, pricing and limits in 5-9 item modules |
| Mobile app screen | 32px | 24px (title to content) | 8px; 16px card padding | platform styles | 24px wrapper, 16px minimum |
| Dashboard, data tool, settings | next steps up, about 24-32px (synthesis) | 12-16px | 4-8px | data and secondary text 13-15px; primary value 15px or more | chrome dimmed; no 3x display jump |
| Catalogue, directory | as marketing | as dashboard | 8px masonry gap | condensed but legible | see the products-per-row rule below |

- [1★] (gap-fill, a30) Products per row:
  - 4 for large catalogues, with de-emphasised names
  - 3 or fewer for small and mid-size ranges, with large images
  - 1 per row, editorial style, for single products or very high-value items
- Text floor everywhere: 12px on the web and 11pt on iOS. Running text stays at 15px or more.

## 9. Hierarchy levers, in the order to reach for them [4]

The order used here: size, then space, then position, then weight, then colour, then effects. Size is the lever the sources call strongest and fastest [4]. Apple builds hierarchy from order, spacing, size and whitespace before colour, borders or effects [3]. Colour is potent, so spend it on one thing [3]. Never rely on colour or effects alone [4].

1. **Size** [4]
   - Rank the elements, make #1 the largest (and usually the boldest), and step each lower level down in size, weight and contrast. The order of sizes becomes the reading order.
   - [3] In cards, rows and stat tiles, the one datum users came for (price, amount, metric, title) is the largest and boldest text. Labels become small muted captions. In each block, one thing is bold and large, one thing is coloured, and the rest is muted.
   - [1] Exception: the largest element can be a visual hook such as an image, with the facts set smaller.
   - For the size of the jumps, see context rule 5.
2. **Space and isolation** [3]
   - Extra space around an element promotes it, and proximity groups elements [14].
3. **Position and order**
   - [2] Put the recommended option first and set it apart.
   - [1★] (Laws of UX) First and last positions in lists and nav are remembered best, so put key items at the ends.
   - In left-to-right text-led layouts, the entry point is top-left.
4. **Weight** [3]
   - When weight marks a change of level, make the step visible (context rule 6).
   - [3] Add a level through a semantic bold variant (SwiftUI `.headline` over `.body`, both 17pt), never ad-hoc bold.
   - [2] Use bold sparingly. [1★] (Butterick) Never combine bold and italic.
5. **Colour and contrast** [3]
   - One or two saturated colours lead and the rest stays neutral.
   - [4] Exactly one filled, high-contrast primary action per screen that has a primary action; a settings or detail screen with none adds none. Secondary actions are an outline, a light-grey fill or a text link, never an equal twin.
   - [3] Make the key item differ on one strong dimension (Von Restorff), and only where everything around it is consistent; too many distinct items compete.
   - [2] Opacity tiers: primary text at full strength, secondary at about 60-70%, disabled at 38%, subject to the 4.5:1 floor in context rule 7.
6. **Depth and effects** [2]
   - Overlays and control layers sit on translucent planes above the content (context rule 19).

Method and structure:

- [3] Before styling, list the elements in rank order and decide where the eye enters, where it goes second and where it finishes. When restructuring, first flatten everything to one muted style, then promote only what the user needs first.
- [4] Aim several levers at the focal point at once (size + weight + colour, or size + space), so hierarchy survives greyscale and colour blindness.
- [2] Per view, use at most 3 contrast levels (header, subheader, body). The style system is one family at 3-4 sizes and 2-3 weights, plus 1-2 colours and neutrals (context rule 17).
- [3] Elements that share a function share a treatment; different roles get visibly different treatments (labels, placeholders, entered text and links all differ). When proximity alone leaves grouping ambiguous, add a second cue such as colour or a common region [2].
- [3] Break flat lists into labelled groups ("Tomorrow", "Next week"), and turn key nouns into typed inline elements: links, avatars, tags and time chips.
- [3] Show position in a sequence. Use a persistent segmented progress bar for multi-step flows (about 7 steps at most), with the current step at full contrast and the others dimmed.

## Context rules (resolved conflicts)

1. **Whitespace or density.** Default to generous space (section 1) for marketing, editorial, product-story and hero layouts. Use compact density for tools, dashboards, tables, directories, settings and checkout: the lower steps 4/8/12/16, with the relationship ladder kept and no functions hidden.
2. **Hero structure: let the star decide.**
   - A physical product or place with strong imagery gets a centred, product-led hero: the product large on the vertical axis, a headline of 2 lines or fewer, one primary CTA plus a text link.
   - The alternative is a full-bleed image with overlaid text, but only on a calm area with verified contrast or a subtle scrim.
   - Software and services get a left-aligned text stack on the page's shared edge, next to real product UI.
   - A split layout is fine once the template parts are gone (badge row, stat row, ghost "Watch demo"). Paragraphs are never centred.
3. **Product or type as the star.** By default the product or subject is the largest element and type supports it. Type becomes the star only when there is no strong visual (services, abstract software, a name reveal), and it is huge because it is the subject, never to fill space. Rotated type belongs only in campaign or poster contexts. The nav logo stays small.
4. **Hero height.** By default, fill the first viewport [3]. When the hero is an edge-to-edge image with no visible end, let a sliver of the next section (10px or more) show instead of adding a "scroll down" cue [1]. Scroll cues are on the delete list [5].
5. **Size jumps.**
   - Text and UI steps stay at 1.125-1.2, or use the platform ladder.
   - Headlines are at least 2x body. Each marketing page gets one display size at least 3x body, usually the hero H1 or the name. Marketing section headings run 2.5-3.5x body and at least 1.5x their lead; never 5x [2] (synthesis: at 2x a section head reads as a label beside a 1.2x lead).
   - Display sizes are `clamp()` tokens capped at about 6-8rem, sized to the column the H1 sits in: `clamp(3rem, 5vw, 5.5rem)` holds 2-3 lines in a full-width container [2]; a split column or a phone needs a floor near 2-2.25rem [3] (typography.md §3).
   - A hero headline that wraps to 4 lines at any width from 320px up is a size error. The 3x-body jump is measured at desktop width.
   - Dashboards skip the 3x jump and use weight and colour instead.
6. **Weight steps.** Default to 400/600 when size or colour also changes. Use 400/700 when weight is the only difference at the same size. Extreme pairs (100-200 against 800-900) only for display text above about 32px.
7. **Muted text.** Tiers are allowed down to the AA floor and no further. Secondary text keeps at least 4.5:1: #6e6e73 on white is about 5:1, and black at 60% on white is about 5.7:1. 40% opacity (about 2.8:1) is for disabled states only. Check every tier in both themes and on tinted surfaces.
8. **Borders.** By default, spacing and surface tone separate content, and decorative separators are faint or absent. Any boundary that identifies a control or its state must meet 3:1 (WCAG 1.4.11): inputs, checkboxes, toggles, outline buttons, focus rings, selected states, and any card whose outline is the only sign it can be clicked.
9. **Cards and bento.** By default there is no container. Add one only for an object (product, file, plan, message), an interactive module, or a module that holds real media. A bento is allowed only when every tile holds a distinct real visual or a measured fact and tile sizes vary by importance. Where cards are justified, use tonal elevation (white on off-white), one card component and no nesting.
10. **Tokens, optics and grid breaks.** Tokens and the grid win by default. Build optical corrections into components. Allow one deliberate grid break per view, used to isolate the key element.
11. **Section backgrounds.** Alternate between the brand's own 2-3 surface tiers (e.g. a tinted ground, a raised tier, one inverted or brand ground). Under a restrained colour strategy, add the brand colour or a full-bleed photo for at most one statement section; a committed strategy may give the brand hue 30-60% (color.md C3). A background change marks a change of topic or audience, never decoration.
12. **Planned sequence or stock sequence.** No section exists just because the category usually has one. Proof must be real and sits next to the claim it supports. Logo walls suit B2B, founder and team proof suits services, and product facts suit product pages.
13. **Equal grid or masonry (synthesis).** Default to equal-size items for equivalent things [2]. Use masonry with a constant gap (for example 8px) only for items whose heights are inherently uneven, such as mixed-aspect photos or posts [2].
14. **Alternating rows (synthesis).** Feature storytelling allows no more than 2 consecutive alternating rows [1★ gap-fill: Taste Skill]. A lineup of parallel models may run one full-width alternating row per model and end in a compare block (Apple category pages) [1].
15. **Option and nav counts.** The 4-option limit applies to a single decision point, not to the nav. A single-product or service site has 5 or fewer nav items. A multi-category catalogue has about 7-9 flat links. Native apps use a tab bar of 3-5 destinations, never a hamburger. On the mobile web, a drawer is fine.
16. **Target size.** 44x44 for any coarse pointer (`@media (pointer: coarse)`) and for every primary action. 24x24 only in dense fine-pointer UI (toolbars, table row actions), with the hit area padded beyond the icon.
17. **Style count.** A marketing view uses at most 3 contrast levels and 3-4 sizes [2]. Native apps use the platform's full named text-style ladder [2] (synthesis).
18. **Scan patterns.** The F- and Z-pattern advice comes from single, conflicting sources. Use hierarchy to direct the eye and don't force a pattern [1].
19. **Depth.** Glass belongs only on the functional layer that floats over content (sticky nav, toolbars, tab bars, sheets), with a solid fallback. Content surfaces stay solid. Use one depth mechanism throughout.

## Checks

In code or computed styles:

- [ ] Every margin, padding and gap is on the token scale. A Tailwind search for arbitrary spacing (`-\[\d+(px|rem)\]`) returns 0 untokenised hits.
- [ ] For every heading, the space above is at least 2x the space below. Heading to body is at most 1.25x the heading's height.
- [ ] The group gap is at least 2x the inner gap, and the section gap is larger than the group gap. Container padding is at least the gap between its children.
- [ ] Desktop marketing section padding is 80px or more. Mobile app sections are about 32px apart.
- [ ] Body text lines are no longer than 90 characters, ideally about 65ch. The page container is 1080-1440px. Side padding is at least 16px at 375px width.
- [ ] There is no horizontal scroll at 320, 375, 768, 1024 or 1440px, or at 50% zoom. Safe-area insets are applied.
- [ ] The hero uses `min-height` with dvh or svh, not `h-screen`. The H1 is 2 lines or fewer on desktop and 3 or fewer at 320-390px, subtext is 20 words or fewer, and there are at most 2 CTAs. There is no stat strip, logo wall or pill eyebrow in the first viewport (docs pages have no hero; venues add hours and address). At 320x640 and 375x667 the product or UI is visible in the first viewport (synthesis).
- [ ] Each view has at most one filled primary button (the same action repeated in the sticky nav counts once); settings and detail screens may have none.
- [ ] The visible gap between consecutive sections on one ground is 96-160px on desktop, not two full paddings stacked.
- [ ] Each view has one title-level element; data about one subject is not split by an input prompt.
- [ ] On a marketing page, the largest display size is at least 3x body (usually the hero H1 or the name), section headings 2.5-3.5x body (render_check `section-scale`), and no top-aligned column ends far above its neighbour (`dead-column`).
- [ ] Secondary text is at least 4.5:1 in both themes. Control boundaries and focus rings are at least 3:1.
- [ ] Every ground change marks a topic or audience change. If sections are separated by background change, adjacent bands never share a surface and there is no divider at the change. Separation by whitespace alone, a full-bleed image or a hairline is equally valid; one method per page, recorded in DESIGN.md.
- [ ] No section pattern repeats down the page [14] and there is no uniform grid of icon cards. Advisory [1★ gap-fill]: no layout family repeated, no more than 2 consecutive alternating rows.
- [ ] Touch targets are at least 44x44 under `pointer: coarse`.

On a screenshot:

- [ ] Squint or blur test: the first fixation is the intended focal point. There are at most 2 prominent elements per viewport.
- [ ] With guide lines drawn, every edge lands on a column line or on another element's edge, and the text in a section shares one left edge (render_check `text-edges` measures it at 1440).
- [ ] An inverted band takes about a quarter of the page height or less; a pinned sequence's visual fills at least half the viewport (a third on phones).
- [ ] Converted to greyscale, the hierarchy still reads.
- [ ] In every data card, the key value is the largest text.
- [ ] The chrome (sidebar, header) is visibly quieter than the content.
