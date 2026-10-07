# Components and details

Buttons, cards, surfaces, radius, icons, forms, navigation, data views, every state, and the accessibility and performance floor.

Tags: `[N]` = number of independent creators who state the rule. `[1★]` = one canonical source (Apple HIG/WWDC, Vercel, Rauno Freiberg, Emil Kowalski, Hobday, Kennedy, NN/g, Linear) or a single source that fills a real gap. `(std)` = a widely accepted value added here that is not in the research. Sections are ordered by their strongest components/accessibility rule. Rules borrowed from other themes (colour, motion, hierarchy, copy, ai_tells) keep their own tags. Method and backers: [evidence.md](evidence.md).

## Summary

1. Check every foreground/background pair in every state and theme: 4.5:1 for text, 3:1 for large text and for any boundary that identifies a control or its state [8]. Keep interaction conventional and put the distinctiveness in the visual layer [8].
2. Design each component once, as tokens in a coded library, with every state built in: hover, focus, pressed, disabled, loading, empty, error [5][4][3]. Acknowledge every press at once [7].
3. Separate with space first; a container has to earn its place [4][7]. Use one radius scale by role, nested concentrically [5][4]. Show in-flow elevation with tonal surfaces; layered shadows and glass go only on what floats [4][3].
4. Targets: 44x44 on touch and for primary actions; the 24x24 floor applies only to dense pointer UI [4]. Show a visible 2px focus ring [2]. Every animation has a reduced-motion path [4], animates only transform and opacity at 60fps [2], and heavy effects degrade on weak devices [3].

## 1. Contrast and legibility

- [8] Lint or check every fg/bg pair at rest, hover, disabled, in overlays, on images, in light and in dark. Floors: 4.5:1 for body and small text; 3:1 for large text (std: WCAG large = 24px regular or 18.66px bold); 3:1 for icons, control boundaries, focus rings, inactive nav items and badges. Aim for 7:1 for body text on dark surfaces. Never use pale grey for body or dialog text. Never recolour status badges in the brand hue if that drops them below 3:1.
- [3] Put text over a photo only on a calm, even area (crop to create one) or on a subtle gradient or blur scrim. Translucent controls over imagery follow the same rule.
- [2] Colour never carries meaning, state or hierarchy on its own. Pair it with text, an icon, shape, weight, size or position. Motion is never the only signal.
- [2] On glass, put text on the thicker, more opaque material. Keep the faintest label tier (quaternaryLabel) off thin and ultraThin materials. Re-check contrast over varied backgrounds.
- [2] Make contrast a theme parameter so a high-contrast theme comes from the same tokens. Test with Increase Contrast, Reduce Transparency and `prefers-contrast: more`.
- [2] Test legibility at every pixel density the product ships on, including 1x screens and TVs. Fix failures with size, contrast, a backing shape or a more legible face.
- [1★] Text with no surface behind it (over 3D, video or scenery) gets a heavier weight, not a drop shadow (Apple HIG).

## 2. Conventions, semantics, affordance

- [8] Keep interaction conventional (Jakob's law): logo top-left; nav at the top or side; search and account/cart top-right; a drawer on mobile web; standard submenus, filters, modals, cart and checkout. Label anything non-standard. Decide per brief: the visual voice (type, colour, imagery, composition). That is where the distinctiveness goes.
- [4] An element's look predicts its behaviour. Anything clickable looks pressable: a fill or 1px border, ~0.5rem radius, a hover change and a pointer cursor. Nothing that isn't clickable is styled as a button. Controls that look alike behave alike. Avoid lines and unlabelled icons that might or might not be interactive.
- [3] Underline inline links, and use underline for nothing else. Use one link style across the site, clearly different from body text.
- [3] Let structure explain itself through built-in signifiers instead of tutorials or instructional copy.
- [2] Use `<a>`/`<Link>` for navigation and `<button>` for actions. No click handlers on div or span. Never disguise a submit as a link or as text. Real anchors keep Cmd/Ctrl-click, middle-click and the context menu working.
- [2] Recurring actions (share, copy link, primary toolbar actions) stay in the same place on every view. Never reorder menus by recency or usage.
- [2] Destructive or high-stakes actions need a confirmation or an Undo window. Routine actions get neither.
- [1★] On Apple platforms, use system materials and standard controls through SwiftUI/UIKit/AppKit rather than hand-built copies. Never strip default material backgrounds (Apple HIG).
- [1★] Ask for permissions and personal data in context, when the feature needs them, and say what they are for. Never ask at launch (Apple WWDC).

## 3. States and feedback

- [8] The accent colour marks only the primary action, key controls, the selected state and the one item that needs attention. Everything else stays neutral (colour rule). Decide per brief: the accent hue.
- [7] Acknowledge every press immediately. Show the pressed state on pointer-down (`transform: scale(0.95)` (a10), a subtler `scale(0.97)`-`scale(0.98)` (std), or a darker fill) and give visible feedback within 400ms. If the result takes longer, switch to a loading state so a slow response never reads as a missed click.
- [4] Build hover, pressed and disabled from the component's own hue ramp, not new hues: hover one step lighter, pressed darker or more saturated, disabled neutral grey.
- [4] Animate state changes instead of snapping: badges, counts, panels and modals opening, dropdowns, an active-tab indicator that glides. Use 100-150ms for feedback and 150-300ms for state changes, with exits faster than entrances [3].
- [3] Design every state of every interactive component: default, hover, focus, pressed, disabled, loading, error, success, empty. Buttons: pressed is slightly smaller; disabled is grey with a faded label; loading swaps the icon for a spinner and keeps the label. Overlays escape `overflow` via `<dialog>`, the popover API or a portal.
- [3] Use skeletons shaped like the final layout, never a spinner in the middle of content.
- [3] Error messages say exactly what failed and how to fix it, in a positive tone without apology. Put them inline below the field. Toasts are only for transient confirmations.
- [2] A loading button keeps its label. Show the spinner after a 150-300ms delay and keep it up for at least 300-500ms so it doesn't flicker. The same timing applies to skeletons.
- [2] Hover and focus make the target stand out: one shade lighter, or a switch to the action colour. A hovered target never fades, dims or recedes.
- [2] Frequently opened menus, command palettes and switchers get no entrance animation. At most, blink the chosen item in the accent colour and fade the menu quickly on close.
- [1★] Never disable submit in advance. Keep it enabled until the request starts, then show the spinner and send an idempotency key (Vercel).
- [1★] Use optimistic UI when success is likely: update at once, reconcile with the server, and roll back or offer Undo on failure (Vercel).
- [1★] Design the empty, sparse, dense and error version of every screen, and give each one a next step (Vercel). Empty state: an icon, a specific headline ("No invoices yet"), one sentence on what will appear, and a primary plus a secondary action. Never a bare "No data". Every string on an empty screen (title, date, header) must be true when there is no data, its CTA is the one action that produces the first data, and a removal pass never deletes its only explanation (synthesis).
- A signature interaction the visitor must trigger (drag a value, complete a sample task) gets a short visible invitation in the first viewport, not only an `aria-label`, and every state of the component reserves its final size so the change shifts no layout (synthesis; CLS under 0.1 (std)).
- [1★] Show a selected tab or chip with a filled container in a contrasting shade, not just a change in text weight or colour. Never use a coloured stripe on one side that is more than 1px wider than the other sides [3].
- [1★] For long background jobs, show live per-item status, a time estimate up front and a "we'll notify you" way out, not a blocking spinner.
- [1★] Delay the first tooltip in a group, then show its neighbours instantly (Vercel). Prefer visible inline help to tooltips [2].

## 4. Cards, containers, separation

- [7] Never lay features out as a grid of rounded cards, each with an icon on top, a bold title and a one-line promise (3-up, 3x2, or a 4-6 tile bento). Build the section from the real content: product visuals, a zig-zag, an asymmetric layout.
- [4] Separate groups with space first. Add a border, divider or container background only when space and headings can't do the job. Test: strip the border, shadow, fill and radius; if the content still reads, it is not a card. No cards in the hero and no dashboard card mosaics.
- [4] Never wrap every block in its own rounded, shadowed card. Never nest cards or stack outlines.
- [3] No full-contrast borders on cards and chips: remove the stroke or drop it to low opacity. Keep a `--border-card` token, equal to the card fill in light mode, separate from the functional `--border`.
- [2] A functional border (input, or a panel whose edge carries meaning) must read against both surfaces: darker than both in light UI, lighter than both in dark UI (e.g. `hsl(0 0% 30%)` on 0-10% surfaces). Never a value between the two.
- [2] Card internals come from the spacing scale: ~16px padding in cards and rows. The gap between rows inside a card is never larger than the gap between cards (cards 8px apart means rows 6-8px apart).
- [2] Listing cards stay lean: one large image, the name in bold, the variant muted, the rating, the price in bold. No stacks of badges, multicolour tag pills, strikethroughs or promo strips.
- [2] Bento grids have exactly as many cells as items (3 = 1+2; 5 = 2+3 or a hero + 4). Vary sizes by importance, give at least 2-3 cells real visuals, and leave no empty trailing tile. 3-5 tiles beat 8.
- [2] Options people choose between (tiers, models) sit in side-by-side columns with aligned spec rows. Pricing: at most ~4 tiers in price order, each with one name, one price and one action.
- Decide per brief: whether the content is made of objects (products, files, plans, messages) that justify cards at all, and which card variant to use (tonal, outlined or elevated). Choose once and reuse it.

## 5. Icons

- [6] No emoji or Unicode glyphs as icons in nav, sidebars, buttons, filter pills or headings. A detector flags it when 40% or more of sidebar links carry emoji. Exception: user-chosen content icons, such as Notion page emoji.
- [3] Take icons from one library with one global stroke width (1.5 or 2.0), matched to the type in fill, weight and corner style. Use SF Symbols on Apple platforms. Never mix ad-hoc one-off SVG paths into the set. Avoid cliché metaphors (rocket, shield). When no library can load (a single self-contained file), draw the set to one spec; a set that copies Lucide or Feather metaphors and geometry stroke for stroke still reads as that library, so give it one owned trait from the signature (stroke weight, terminals, a corner), or in a native mock say that SF Symbols are the production target. Device chrome glyphs (signal, battery) are not part of the icon set (synthesis).
- A domain symbol keeps one meaning across the page (synthesis). A tick that means "verified" is not also a bullet, a generic success mark and a pricing checkmark, and a legend's keys mean the same thing wherever the same letters appear.
- [3] Use fewer, smaller icons. Keep them where they replace or clarify a word in repeated, scannable data: metadata rows, object types, status, tab labels. Never use them as decoration on headings, feature tiles or marketing bullets.
- [3] Size icons at 16-20px inline with text and 16-24px in lists and links. Keep the logo small, top-left.
- [1★] Next to text, lower the icon's contrast (opacity or a lighter tone) so it doesn't outweigh the label (Hobday). Tune the icon's stroke, size or gap to the adjacent text (Vercel).
- [1★] No coloured background tiles behind small entity or team icons (Linear).
- [1★] Universally known icons (home, bookmark, user) can go unlabelled; ambiguous ones get a label. Icon-only buttons get `aria-label`; decorative icons get `aria-hidden="true"` (Vercel).
- [1★] In a list item, align the icon with the first line (the title), not the centre of the title-plus-description block.
- Decide per brief: which library. Restyle it rather than shipping the stock default; unmodified Lucide in shadcn reads as the AI default. A commissioned set drawn to one spec is the flagship option.

## 6. Component system and tokens

- [6] Define colours as role-named tokens (canvas, surface, label, secondaryLabel, action, focus, border, success/warning/error) and reference them in components, never raw hex.
- [5] Build from a coded, composable component library (e.g. React + Tailwind + shadcn/ui) with states and motion built in. Design in the library code, not in static mockups.
- [4] Restyle every library default (tokens, font, icons, radius, effects) before it ships as the identity.
- [4] Design each repeated component once. Copies differ only in content, never in size, radius, image position or type style. The button set reads as one family.
- [2] Each component is a token group that references base tokens, with each state stored as its own named variant. Reference (Apple): `button-primary` uses bg `#0066cc`, 17px/400, radius 9999px, padding 11px 22px; `-active` is scale(0.95); `-focus` is 2px solid `#0071e3` (a10 extraction; live apple.com CSS appears to use #0071e3 for filled pills and #0066cc for links; verify before quoting, and never ship either as your accent).
- [1★] Pick one depth technique (soft shadows, hard shadows, or flat) and use it on every surface (Hobday).
- [1★] Theme the browser surfaces you didn't draw: `::selection`, `caret-color`, scrollbars, the focus ring, `text-underline-offset`. Set `<meta name="theme-color">` to the page background and `color-scheme: dark` on `<html>` in dark themes, and give native `<select>` explicit colours (Vercel).
- [1★] Never write `transition: all`. List the exact properties, usually `opacity, transform` (Vercel).

## 7. Text size, zoom, responsiveness

- [5] Never hard-code font sizes. Use named text-style tokens (title, headline, body, caption) in units that follow the user's setting. Web: rem on a 16px base (24px = 1.5rem, 14px = .875rem, 12px = .75rem). iOS: Dynamic Type styles, with custom fonts set via `.custom("Brand", size: 16, relativeTo: .body)`.
- [2] Stress-test at the largest accessibility sizes (iOS Body runs from 14pt at xSmall through the 17pt default to 53pt at AX5), with long strings and other languages. Adapt the layout; clamp with `.dynamicTypeSize(...)` only when it truly can't fit.
- [2] Make every layout responsive, check it at each breakpoint in device emulation, then check it on a real phone.
- [1★] Never disable zoom (`user-scalable=no`, `maximum-scale=1`). Set mobile input font-size to at least 16px so iOS Safari doesn't zoom on focus (Vercel).

## 8. Corner radius

- [5] Use one small radius scale on every component and section. Either all sharp (0-4px), all soft (12-16px), or a documented mix by role (e.g. pill buttons, 16px cards, 8px inputs; Apple uses 8px utility buttons, 18px cards and 9999px pills). Never mix sharp and round in one view, and never improvise in-between values. Reserve full pills for actions: CTAs, chips, search.
- [4] Nest corners concentrically: inner radius = outer radius - padding. The inner radius never exceeds the parent's; if the result is 0 or less, square the inner corner. An outer 30px with a 20px inset gives an inner 10px. CSS: `border-radius: max(0px, calc(var(--r-outer) - var(--inset)))`. The rule binds an inner element that hugs the parent's corner (an image or panel inset by the padding); a button or input that sits away from the corner keeps its own role radius (synthesis).
- [3] Prefer continuous-curvature corners (squircle, G2) where the platform supports them: SwiftUI `RoundedRectangle(cornerRadius: 16, style: .continuous)`, Figma corner smoothing. On the web, use `corner-shape: squircle` inside `@supports` (std) or fall back to a plain radius.
- Starting scale (from the conflict resolution): inputs 8px, cards 12-16px, large containers 20-28px, pills 9999px. Tailwind equivalents (std): `rounded-lg` 8px, `rounded-2xl` 16px, `rounded-3xl` 24px, `rounded-full`.
- Decide per brief, from the reference world (the product's hardware, packaging, signage, the brand mark), not from the category label: sharp (0-4px, tends to read luxury or editorial) or soft (reads friendly). Don't default to soft. Button shape is its own decision: pill, radius-matched rectangle or sharp; pill is one option, not the default.

## 9. Tables, dashboards, lists, charts

- [5] Keep chrome subordinate to the workspace. Dim the sidebar a few notches and shrink headers, greetings and page titles so the data is the focal point.
- [3] Density is a decision. Dashboards, tables, directories, settings and checkout use the lower steps of the same spacing scale (4/8/12/16) and a tighter 1.125-1.2 type scale; data text can go to 13-15px, but the primary datum stays at 15px or above. Get there by shrinking, never by deleting relationship gaps or hiding functions.
- [3] In each row, card or stat tile, the one datum users came for (price, amount, metric, title) is the largest and boldest. Labels and metadata are small muted captions. No uniform "Label: value" rows.
- [3] Use tabular figures for numbers that are compared or that change (prices, stats, counters, timers, table columns): `font-variant-numeric: tabular-nums`, Tailwind `tabular-nums`, SwiftUI `.monospacedDigit()`. Keep proportional figures in running text.
- [2] Product UI default: a calm surface hierarchy, few colours, dense but readable, minimal chrome and one accent for action or state. Structure: workspace, navigation and an optional inspector panel.
- [2] Collapse per-row button clusters into one trailing overflow (kebab) menu, reduce text chips to icons and right-align the key metric. See the context rules for which action stays visible.
- [2] Give product pages plain operational headings ("Invoices"), with no tagline or hero.
- [2] Virtualize lists longer than 50 items (`content-visibility: auto` or a virtualizer). Sync filters, tabs, pagination and expanded panels to the URL, and restore scroll position on Back/Forward.
- [1★] Keep management tables to 3-4 essential columns and move secondary metrics to their own tab. One interaction per column header: sort or drag, not both.
- [1★] Size and test dynamic values at their longest realistic length ($1,633,782.48, not $3,782.48). Truncate with `min-width: 0` plus ellipsis or line-clamp (Vercel).
- [1★] Metric rows: right-align the value, followed by a smaller muted "vs previous" value and a tinted percent-change badge. When comparing periods, draw the previous period as a paler tint of the same hue.
- [1★] Show numeric series as charts with labelled axes and hover tooltips rather than raw number tables.
- Chart craft (synthesis; load the `dataviz` skill when it is available, for marks, axes and data colours): place axis labels at their data values and centre each on its tick (end labels may clamp inward), never spread them with `justify-content: space-between`; inspect every chart at 2x zoom; a segment narrower than about 2x the stroke width becomes a hairline tick or merges with its neighbour, so the least important event never becomes the heaviest mark; a monochrome chart that encodes category by position (lanes) is fine and needs no hue per series; every encoding in a mini-chart is labelled in the same view; a non-interactive graphic never looks like a control (slider, progress bar, switch).
- Code-drawn technical diagrams follow one drafting convention (synthesis): every dimension has extension lines and matching terminators, a callout leader touches the feature it names, and no label floats without an extent. Labels render at 12px or more at every width (HTML over the SVG, or a label set per breakpoint).

## 10. Elevation, shadows, glass, borders

- [4] Use frosted glass (`backdrop-filter`) only on the functional layer that floats over content: sticky nav and sub-nav, toolbars, tab bars, sheets, overlays. There it replaces the shadow. Never use it on content (cards, panels, the hero, the app background). Apple sub-nav: 52px tall, `rgba(245,245,247,.8)` with `-webkit-backdrop-filter: saturate(180%) blur(20px); backdrop-filter: saturate(180%) blur(20px)` (Safari before 18 needs the prefix (std)). Provide a solid fallback under `@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px)))`, `prefers-reduced-transparency` (which Safari ignores (std)) and `prefers-contrast: more`, and for low-power devices. Never put saturated colour behind heavy blur.
- [3] Show in-flow elevation tonally: white cards on an off-white page in light UI, and each raised layer one step lighter in dark UI. Page/card/raised: about 0/5/10% lightness in dark mode, 90/95/100% in light mode [2].
- [3] Elements that float (menus, popovers, dialogs, sticky bars, dragged items) get shadows of at least two layers (ambient plus direct), at three levels:
  - `sm` (compact cards, controls, pills): `0 2px 3px -1px rgba(0,0,0,.1), 0 1px 0 rgba(25,28,33,.02), 0 0 0 1px rgba(25,28,33,.08)`
  - `md` (panels, popovers): `0 0 0 1px rgba(0,0,0,.06), 0 1px 1px -.5px, 0 3px 3px -1.5px, 0 6px 6px -3px, 0 12px 12px -6px, 0 24px 24px -12px`, each step `rgba(0,0,0,.06)`
  - `lg` (modals, hero media): `0 2.8px 2.2px rgba(0,0,0,.034), 0 6.7px 5.3px rgba(0,0,0,.048), 0 12.5px 10px rgba(0,0,0,.06), 0 22.3px 17.9px rgba(0,0,0,.072), 0 41.8px 33.4px rgba(0,0,0,.086), 0 100px 80px rgba(0,0,0,.12)`
- [3] Keep shadows soft and diffuse with a downward offset, e.g. `0 12px 48px #e9e9e9` on `#f5f5f5`. Never a zero-offset mid-grey halo such as `0 0 48px #9f9f9f`.
- [3] No coloured glows, neon halos or zero-offset coloured shadows on cards, buttons or text. A detector flags blur of 15px or more, saturation above 0.3 and alpha of 0.1 or more.
- [2] Light everything from one source above: tops lighter, bottoms darker, shadows falling downward. Optionally add a 1px lighter top edge (`--highlight`: `#fff` in light mode, `hsl(0 0% 60%)` in dark). Never light from below.
- [2] Default to subtle depth ("flatty"): small shadows and brightness shifts that mark what can be pressed, between flat and skeuomorphic.
- [1★] For hand-built shadows, set blur to twice the Y offset (4px offset, 8px blur), and lower the opacity as the element rises (Hobday). Pair a shadow with a 1px semi-transparent border for a crisp edge on any background (Vercel).
- [1★] Inset (recessed) is for things you put something into: text fields, slider tracks, unchecked boxes, pressed buttons. Outset (raised) is for things you push or that float: buttons, slider thumbs, dropdowns, popups (Kennedy).
- Decide per brief: the depth technique (soft, hard/offset or flat) and whether glass appears at all.

## 11. Buttons and calls to action

- [4] One primary action per view (the same action repeated in the sticky nav counts once). It is filled and is the highest-contrast clickable element. Secondary actions are visibly weaker (an outline, a light-grey fill or a text link), never an equal-weight twin. Cut competing buttons.
- [4] Label each button with the specific action, in active voice ("Save changes", "Create invoice"). Never "Submit", "Continue" or "OK".
- [3] The primary fill is solid and stands out sharply from its surroundings. Never outline-only, pale grey (`#c9c9c9` reads as disabled) or low-contrast.
- [3] A secondary placed beside the primary has the same shape, in outline or a light fill.
- [2] Each CTA intent has one label of 1-3 words that never wraps, worded the same in the nav, hero and footer. Don't cap a CTA's max-width so tightly that the label wraps. A compact nav link that scrolls to the buy section ("Buy") is navigation, not a second wording of the button that changes state ("Add to basket"); one outcome never gets two verbs (synthesis).
- [2] Put CTAs directly under the copy they act on, as one group, with clear space around them. On landing pages, put the primary CTA in the hero and in the sticky nav, and repeat it about every 2-3 screens.
- Sizing: height comes from content, not a fixed value: text size plus padding in 8pt multiples [1★]. Horizontal padding is about twice the vertical [1★ Hobday] (Apple: 11px/22px at 17px text). Linear's CTAs are at least 40px tall; every touch CTA is at least 44px [4]. Sibling buttons and chips sit exactly 8px apart [1★]. Press state: section 3 [7].
- Decide per brief: the primary colour and the button shape (pill, radius-matched rectangle or sharp). Use the brand accent if the brand has a real one, and near-black when the imagery or product supplies the colour; on a committed brand ground, a white or near-black fill or a tint of the ground's hue. A black pill on a grey page is the trend template, not a default. Never violet.

## 12. Touch and hit targets

- [4] Minimum size: 44x44 (pt on iOS, CSS px on the web) for any coarse pointer and for every primary action. 24x24 is allowed only in dense fine-pointer UI such as toolbars and table row actions. Grow desktop-sized controls under `@media (pointer: coarse)` (Linear: tab pills go from 36px to 44px on touch; inputs are at least 44px).
- [4] The hit area is at least as large as the visual. Pad small icons or extend them with a pseudo-element, leave no dead zones, and give a checkbox or radio one shared target with its label. NN/g physical guideline: a 1cm x 1cm target with 0.4cm between targets. 44px does not equal 1cm.
- [3] Make frequent targets large and place them near the thumb, the pointer or a screen edge. Never compress toolbars or tab bars until controls crowd.
- [1★] Space adjacent tappable buttons 12-48px apart, more for larger buttons.
- [1★] Set `touch-action: manipulation` on controls, choose `-webkit-tap-highlight-color` deliberately, and use `overscroll-behavior: contain` in modals and drawers (Vercel).
- [1★] Keep a drag alive when the finger slides off a small control (slider, scrubber), and keep tracking while it stays pressed (Rauno).

## 13. Navigation

- [4] Catalogue sites: one persistent, flat top nav with the logo, about 7 text categories and up to 3 icons (search, bag). Every key destination is a visible link, reachable in about two clicks. No "Home" dropdown hiding Contact or About.
- [4] Group related tabs and controls in one shared container (a pill track or toolbar group) and set unrelated ones apart. On custom and web bars, don't split search into a separate floating button. Native iOS 26+: put search in the system search tab (`Tab(role: .search)`), which the OS renders detached at the trailing end; that is Apple's own pattern (apple-playbook.md §3).
- [2] Never hide essential actions behind hover or an overflow menu; only nonessential ones go in "...". Hover doesn't exist on touch.
- [2] Single-purpose landing pages: the logo, 3-4 links and one CTA button. Product pages: a slim sticky local nav with the product name on the left and 2-3 section links plus one compact "Buy" pill on the right, translucent light on light pages and dark on dark.
- [2] Large catalogues: a strip of small product icon tiles with tiny labels under the nav, then a few large banners. Search and big sets get filter and sort controls.
- [1★] Native apps (Apple WWDC): the tab bar holds 3-5 essential top-level sections; merge any tab that is only a sub-view. Actions, even "+", never go in the tab bar; they go in the screen's toolbar. Every screen has a toolbar with a plain title, and a back button on drill-downs.
- [1★ gap-fill: tom is loading] Use segmented or inset tabs only to switch between 2-3 views of the same thing. Page-level routing uses a sidebar, a side nav or underline tabs.
- [1★] Size tab bars to their content, not full width, with smaller icons and text (Linear).
- [1★] A transparent nav over video or changing imagery needs a scrim or solid fallback. A sticky header animates from detached to fixed and never renders both menus at once. Never truncate key context (URL, site identity) between toolbar icons (NN/g).

## 14. Reduced motion and performance budgets

- [4] Give every animation a `prefers-reduced-motion: reduce` path. Replace translate, parallax, infinite loops and scroll-jacking with a short opacity fade (e.g. 0.2s) or a static state. Pause decorative loops with `animation-play-state: paused` and keep paused elements visible. Keep state feedback. Framer Motion: `useReducedMotion()` sets translate to 0 and keeps opacity. Tailwind: `motion-reduce:` (std).
- [3] Detect low-power hardware, battery saver and slow networks, and serve a lighter page: solid surfaces instead of blur, no WebGL, one static image instead of a frame sequence, smaller assets. Load heavy effects async and code-split, fade them in after load, and make sure the core visual works without them. Apple's AirPods Pro page on slow 3G loads 8 of 111 requests, 347KB of 2.6MB.
- [2] Hold 60fps (16ms frames) before any visual polish.
- [2] Animate only `transform` and `opacity`. Resize via FLIP or `grid-template-rows`. Use `will-change` only during a known animation. The rule targets movement and layout; a short colour, background or shadow transition on hover and state changes repaints without reflow and is fine (synthesis with the [4] reduced-motion rule, which keeps colour changes).
- [2] Respond to input within 400ms and complete POST/PATCH/DELETE in under 500ms. Profile with CPU and network throttling and in iOS Low Power Mode.
- [2] Never trade the basics (speed, legible type, layout stability, focus states) for a premium animated look. Motion adds no input latency. Targets: INP under 200ms, LCP under 2.5s, CLS under 0.1.
- [2] Load in priority order. Give images explicit `width` and `height`. Use `fetchpriority="high"` only above the fold and `loading="lazy"` below it. Preload and subset critical fonts with `font-display: swap`. `preconnect` to CDNs. Compress video hard.
- [2] Avoid scroll-scrubbed sequences of hundreds of stills; one page with several measured 1,609 requests, 55.8MB and a 30s load. Never serve full-resolution frames to every device.
- [2] Build hero effects from stacked DOM, SVG and CSS layers rather than canvas or bitmaps. A shader is only an optional top layer.
- [1★] Motion that runs while the main thread is busy (route changes, page load) uses CSS or the Web Animations API, not rAF-driven JS (Emil Kowalski).
- [1★] Drive scroll effects with IntersectionObserver or `animation-timeline: view()`, never with per-scroll-event handlers or scroll position in React state.
- [1★] Autoplay only muted, non-essential loops, and give any motion longer than 5s a pause control (Vercel).
- [1★] Keep a content page's weight on the order of a plain-text novel (~700KB). Compress every image. Test on a mid-tier Android phone or iPad, not only a fast laptop.

## 15. Forms and input

- [3] Accept messy input and normalise it yourself (Postel's law). Tolerate typos and varied formats, and suggest corrections instead of a dead-end "0 results".
- [3] Pre-fill what you already know (earlier answers, location, saved details) and ask users to confirm rather than type.
- [2] Fields behave like native ones. Each has a visible, clickable label above it, 4-8px away (spacing rule [14]); an example placeholder ("e.g. pat@example.com"); the correct `type` and `inputmode`; `autocomplete` with a meaningful `name`; and `spellcheck="false"` on email, code and username fields. Enter submits a single-input form; Cmd/Ctrl+Enter submits a textarea. Warn before leaving with unsaved changes. On submit, move focus to the first error.
- [2] Inputs stand out from the background (e.g. a light-grey fill on a white card). Placeholder, filled and focus states look clearly different; focus shows an accent border plus a soft outer ring.
- [2] Multi-step or unfinished tasks show a progress bar or checklist.
- [1★] Never block paste (Vercel).
- Restyle native controls to the system's tokens [5] (nothing left at its default): a range input needs `appearance: none` plus `::-webkit-slider-thumb`, `::-webkit-slider-runnable-track`, `::-moz-range-thumb` and `::-moz-range-track` rules, because `accent-color` alone ships the browser's pill track and round thumb into a sharp system. Checkboxes and radios may keep their native form with `accent-color`, sized for touch. slop_check flags unstyled range inputs (`native-control-default`).
- [1★] Short creation forms go in a compact modal with two columns and advanced options collapsed. Preset-choice screens add a search field and a "Skip" for users none of the presets fit.

## 16. Focus, keyboard, screen readers

- [2] Every flow works from the keyboard. Every focusable control shows a visible 2px focus ring in a dedicated focus colour via `:focus-visible` (and `:focus-within` for grouped controls). Never ship `outline: none` without a replacement. The ring meets 3:1 [8]. References: Apple `outline: 2px solid #0071e3`; Linear 2px `#5e69d1` at 50%. Add `outline-offset: 2px` (std) so the ring clears the fill.
- [2] Keep decoration out of the accessibility tree: `alt=""` plus `aria-hidden="true"` on presentational images. Collapse an illustration into one `role="img"` with a short `aria-label`. Announce events such as "Copied" through a polite live region.
- [2] Give accessibility its own section in the design spec, and ship the floor without being asked: responsive down to mobile, visible focus, reduced motion, AA contrast.
- [1★] Trap focus inside overlays, move it in on open and restore it on close. Sticky headers and overlays never cover the focused element (Vercel, WAI-ARIA patterns).
- [1★] Hide screen-reader-only text with a visually-hidden utility (Tailwind `sr-only`, std), never with `display: none` or `visibility: hidden` (Rauno).

## Context rules (where sources disagree)

- **Borders vs 3:1.** WCAG 1.4.11 requires 3:1 only where a boundary identifies a control or its state. Default: decorative separators and card edges are faint or absent. Use 3:1 for inputs, checkboxes, toggles, outline buttons, focus rings, selected states, and any card whose outline is the only sign it is interactive. A quiet input gets a tonal fill with a 3:1 edge or focus state, not a faint hairline.
- **Muted text.** Default: mute down to 4.5:1 and no further (#6e6e73 on white is about 5:1; black at 60% is about 5.7:1; black at 40% is about 2.8:1 and fails). Go below that only for disabled states and decorative lines.
- **Cards.** Default: space and type do the separating. Use a container only when the content is an object (product, file, plan, message), is interactive, or holds real media. A bento grid is fine only when every tile holds a distinct real visual or measured fact and tile sizes vary.
- **Primary colour and the secondary.** Default: the brand accent. Use near-black when imagery or product supplies the colour. The secondary defaults to a text link with a chevron. Use a filled-plus-outline pair only for two real, parallel actions (like Apple's "Learn more" and "Buy"), never a vague "Watch demo".
- **Radius.** Default: one scale with steps by role, nested concentrically. That satisfies both "never mix radii" and "vary by hierarchy". Sharp versus soft is a brand decision; never both in one view.
- **Shadows.** Default: tonal surfaces in flow, layered shadows only on floating elements, and a contact shadow only under product cut-outs. Neutral shadows on neutral grounds; on a coloured ground, a darker low-chroma shade of that ground. Never brand-hue glows.
- **Glass.** Glass goes only on the floating functional layer, where it replaces a shadow. Refraction, specular highlights and bend belong to native Apple platforms via system components; don't fake them by hand on the web.
- **Icons.** Use icons in repeated, scannable data at 16-20px, not as decoration. Source: an established library, restyled, or a commissioned set. "Never hand-drawn" means no ad-hoc paths mixed into a set.
- **Visibility and nav count.** Decide by frequency and importance: frequent actions and destinations stay visible; rare and advanced ones go behind disclosure. The "4 options or fewer" rule applies to a single decision point, not the whole nav. Single product or service site: 5 nav items or fewer. Multi-category catalogue: about 7-9 flat links. Mobile web: a drawer is fine. Native apps: a 3-5 item tab bar, never a hamburger. Table rows: the most-used action stays visible, the rest go in a kebab, and nothing is hover-only.
- **Targets.** 44x44 on coarse pointers and for every primary action. 24x24 only in dense fine-pointer UI, with padded hit areas and enough spacing that targets don't overlap.
- **Density.** Generous whitespace for marketing, editorial and product-story pages. Compact for dashboards, tables, settings and checkout: scale steps 4/8/12/16, data text 13-15px, primary datum at 15px or more, nothing below ~12px on the web or 11pt on iOS. Reading text stays at 16-17px.
- **Conventions vs distinctiveness.** Interaction, information architecture and controls stay conventional; type, colour, imagery, composition and copy carry the identity. Break an interaction convention only when the new interaction is the product's core value, then label it and test it with users.
- **Brand vs platform.** Identity (palette, type voice, imagery, tone, motion character) is identical everywhere. Components, navigation and gestures stay native to each platform.
- **Reduced motion: fade or 0ms** (resolved here by weight). Three of four sources keep a short opacity fade and all state feedback, and they flag a global `0.01ms` kill switch as a mistake; one sets every duration to 0ms. Default: a fade of 200ms or less and no spatial motion. Use 0ms only for decorative motion that gives no feedback.
- **Frame preloading** (resolved here by weight). One source preloads every frame of a scroll sequence; two say to preload only essentials. Default: preload only above-the-fold essentials. If a sequence is the page's one signature motion, preload that sequence alone, with frame sets sized per device and a static-image fallback on slow connections [3].
- **Flat vs tactile chrome** (resolved here by weight). Default: subtle depth [2]. Pure flat chrome [1] loses affordance. Gel or skeuomorphic controls [2] only as a deliberate brand direction, such as playful products or new, intimidating technology.
- **Stable vs adaptive chrome.** Default: stable positions [2]. Adaptive tab bars only where the platform provides them through system components (iOS 26) [1]; never hand-roll menus that move.
- **Filters on premium listings.** A small curated collection gets no filter bar, or a minimal visual one [1]. A large catalogue gets search, filters and sort [2].

## Checks

In code:
- [ ] Every text token pair meets 4.5:1 (large text 3:1), including muted tiers. Control boundaries, focus rings and icons meet 3:1. Checked in light, dark and hover.
- [ ] No `outline: none` or `outline-none` without a `:focus-visible` replacement. The ring is 2px.
- [ ] No `onClick` on div or span. Navigation uses `<a>`, actions use `<button>`.
- [ ] No `user-scalable=no` or `maximum-scale=1`. Mobile input font-size is at least 16px.
- [ ] Every interactive component defines hover, focus-visible, active, disabled and loading styles.
- [ ] Interactive elements are at least 44px under `(pointer: coarse)` and never under 24px.
- [ ] Every animation has a reduced-motion path. No `transition: all`. Movement and size change only through `transform` and `opacity`; colour, background and shadow transitions of 200ms or less for hover and state are fine.
- [ ] Radii come from a handful of tokens. Every nested radius equals the outer radius minus padding, floored at 0.
- [ ] In-flow cards have no shadow, or a tonal surface only. Floating layers use shadows of 2+ layers. No zero-offset coloured shadow.
- [ ] `backdrop-filter` appears only on nav, toolbars and overlays, with a solid fallback.
- [ ] No emoji in nav, buttons or headings. Icons come from one import source with one stroke width.
- [ ] Images have `width`/`height`. `fetchpriority="high"` is on the LCP asset only; everything below the fold has `loading="lazy"`. Critical fonts are preloaded with `font-display: swap`.
- [ ] Numeric columns and counters use `tabular-nums`.
- [ ] Inputs have a label, `type`, `autocomplete` and `name`. No `onPaste` preventDefault. Submit is not disabled before the request.
- [ ] Decorative images and icons have `alt=""` and `aria-hidden`. Icon-only buttons have an `aria-label`.
- [ ] Range, select and other native controls are restyled to the radius and colour tokens.
- [ ] Charts: axis labels positioned by value and centred on ticks; at 2x zoom no tiny segment renders as a blob.
- [ ] Two values in one row sit in two fixed tracks; one unit and duration format throughout.

In a screenshot (1440px and 390px):
- [ ] One filled primary action per view, and it is the highest-contrast clickable thing. Labels are 1-3 words and none wrap.
- [ ] Strip a card's border, shadow and fill in your head: if nothing breaks, remove the card. No 3-up icon-title-promise grid, no nested cards.
- [ ] No one-sided coloured stripes, glows or full-contrast card borders.
- [ ] The empty, loading (skeleton), error and longest-value versions of each screen exist and hold their layout.
- [ ] No horizontal overflow and no crowded tab bar on mobile; essential nav and actions are visible without hover.
- [ ] Text over images sits on a calm area or a scrim.
