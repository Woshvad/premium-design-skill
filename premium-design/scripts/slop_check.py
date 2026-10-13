#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
slop_check.py - flag AI-design tells in HTML / CSS / JS / JSX / TSX / Vue / Svelte / Astro.

Part of the premium-design skill. Every rule maps to a ranked decision cluster from the
research (see ../references/evidence.md). [N] = number of INDEPENDENT creators who state
the decision (a channel with four videos counts once). Severity is derived from N only:
    high = 7+ creators     med = 4-6 creators     low = 1-3 creators
Exit status: 1 if any high finding, 0 otherwise, 2 on usage error.

Usage
    python3 slop_check.py PATH [PATH ...] [--surface marketing|product|dashboard|native]
                          [--json] [--min-severity low|med|high] [--max N] [--all]
                          [--ignore rule-a,rule-b] [--brief FILE] [--list-rules] [--explain RULE]
    (use "python" on Windows.) PATH is a file or a directory. node_modules, dist, build,
    out, vendor, hidden folders (.next, .git ...) and *.min.* files are skipped. Exit 2
    when a file has an unsupported type (e.g. .swift) or no supported file is found, so an
    empty scan never reads as a pass. The summary line prints first (and again after the
    findings, so it is visible at the end of long output); the default text
    output groups findings by rule with up to 3 example locations each and --max N
    example locations in total (default 40); --all lists every finding. On a large
    directory start with --min-severity med. --surface matches the surface pinned in the
    brief: product, dashboard and native allow one neutral sans, 13-15px secondary/data
    text and short status badges ("Beta") above page titles. A deliberate, documented
    exception is silenced with --ignore; inside one element (and its children) with the
    attribute data-slop-ignore="rule-a rule-b"; or for one file with a comment containing
    "slop-check: ignore rule-a, rule-b" (unknown ids in a directive are reported on
    stderr). Prefer the element attribute: a file-wide directive also hides the next real
    instance. A pooled finding is silenced by a directive in any file it was derived from.
    --brief FILE (the brief as text) turns on brief-echo. A clean scan is the floor, not
    evidence of quality: run render_check.py on the rendered page as well.
    Python 3.8+, standard library only; files are read as UTF-8 with errors='replace';
    output is UTF-8 when piped; long Windows paths are supported.

Scope and limits
    * Web code only: HTML, CSS/SCSS/Sass/Less, JS/TS/JSX/TSX, Vue, Svelte, Astro. SwiftUI
      and other native code are not scanned (use apple-playbook.md section 16).
    * Every full HTML document (has <html>, <head> or <body>) is checked as one page,
      together with the local stylesheets it links. All other files under one PATH
      (components, CSS, Tailwind config) are pooled as one app, so a font chosen in
      layout.tsx counts for every component. Fonts loaded by a document's <link> also
      count for the app pooled from the same PATH. The stock-section check pools per
      route instead (see stock-section-sequence).
    * CSS matching is approximate: only the last compound selector (tag, classes, id) is
      compared with an element, the cascade and specificity are ignored, and var() is
      resolved from the first :root/html/@theme definition.
    * Markup parsing is a tolerant tag scanner, not a browser. JSX is parsed only where
      a tag follows ( = : ? , [ { } > && || or "return".
    * A finding is a place to look, not a verdict. Every heuristic below errs toward
      silence; the false positives listed are the ones that remain.
    * Detection cutoffs (e.g. "5+ animations", "24+ words", "70% of radii") are checker
      calibration chosen to stay quiet on restrained pages, not design targets. Design
      values quoted in messages and fixes come from the research clusters named.
    * A rule's default is not a house style: e.g. pure-black-white accepts any tinted
      ground, accent-hue-count accepts any one accent hue, default-font-only accepts any
      chosen face. The checker only flags the reflexive default, never prescribes the look.

Rules, heuristics and known false positives
-------------------------------------------
stock-section-sequence [14] ai_tells.0.41  (high)
    5+ stock SaaS blocks on one page: announcement bar, pill badge over a heading,
    gradient hero, logo cloud ("Trusted by ... teams"), stat strip, icon-card grid,
    "How it works" / numbered steps, testimonials, "Most popular" pricing, FAQ,
    "Ready to ...?" CTA strip, 4-column footer, floating chat button. When no single
    file reaches 5, each route entry (app/**/page.*, pages/**, src/routes/**,
    +page.svelte) is pooled with the shared layouts and the components it imports
    (relative, @/, ~/ and $lib/ imports, 4 levels), never with other routes. With no
    route entry in the scan, all files are pooled and reported at med severity as a
    "possible" sequence.
    FP: a page whose content really needs most of these blocks.
default-font-only [13] ai_tells.0.2  (high)
    Every chosen non-mono family is Inter/Roboto/Arial/Open Sans/Lato/Times/system-ui
    (incl. -apple-system, Segoe UI, sans-serif); or the unit owns the page root
    (html/body/:root) and sets no family at all (browser default, or Tailwind's default
    font-sans = ui-sans-serif, system-ui). Families come from font-family/font
    declarations, --font-* tokens, @font-face, Google/Bunny/Fontshare links, next/font and
    @fontsource imports, Tailwind fontFamily config. Unresolvable var() fonts silence it;
    icon fonts (Font Awesome, Material Symbols ...) and monospace faces are not counted.
    Helvetica / Helvetica Neue are not defaults (the [13] cluster does not list them;
    typography.0.7 [4] recommends Helvetica). This all-default test is skipped with --surface
    native, and with --surface product|dashboard when at most one named neutral sans is in use.
    Headline voice (marketing): also flagged when a brand face is loaded but the first <h1>
    still resolves to a default face through its own rules or its ancestors'. Web mock of a
    native app (--surface native on .html): flagged when the first h1, h2 or h3 starts with
    a system-stack name (-apple-system, system-ui), because off Apple devices it renders in
    whatever the stack falls back to. Tailwind font-* family classes silence both.
    FP: fonts injected at runtime; a mock that documents Inter as a deliberate stand-in.
purple-ai-colour [11] ai_tells.0.0  (high)
    Hue 250-300 deg (HSL), saturation > 0.25, lightness 0.15-0.85 (plus vivid indigo
    238-250 deg, saturation >= 0.6) in: any gradient stop; a solid fill (alpha >= 0.5)
    on a button/CTA/pill/badge/active state; a --primary/--accent/--brand token;
    Tailwind from-/via-/to- violet|purple|indigo|fuchsia-300+ or bg-*-400+ on
    buttons/badges. Colours parsed from hex, rgb(), hsl(), oklch(), names, var().
    FP: brands whose existing identity really is purple (then still no gradient on white).
neg-tracking-small [11] typography.0.51  (high)
    letter-spacing below 0 at <= 12px (same CSS rule, inline style, or Tailwind
    tracking-* with text-xs on the same element). 13-15px is not flagged: slight
    negative tracking there is within the research (SF's own table runs -0.006 to
    -0.026em at 13-17pt).
    FP: a size set elsewhere than the rule or element that holds the letter-spacing.
tracking-too-tight [11] typography.0.51  (high)
    letter-spacing at or below -0.045em at any size (the research floor is -0.04em;
    Tailwind tracking-tighter, -0.05em, is flagged).
    FP: a display face drawn loose that needs extra tightening; logotype lockups.
animation-overload [11] motion_interaction.0.0  (high)
    5+ distinct animation names, or 12+ animated elements/rules (CSS animation,
    Tailwind animate-*, Framer Motion motion.* props, GSAP tweens, AOS). Spinners,
    loaders and skeletons are excluded: names or classes matching spin/loader/loading/
    skeleton/progress, anything within 4 ancestors of aria-busy="true", role=status|
    progressbar or a skeleton/loading/placeholder class or component, and empty neutral
    (bg-gray/zinc/muted...) animate-pulse blocks.
    FP: an animation-led brand or game page; generated CSS frameworks bundled into the scan.
body-text-small [7] typography.0.42  (high)
    body/html/p/article/main/.lead/.prose rules with font-size < 15px; <p> elements
    with 24+ words set in text-xs/text-sm (or a matched CSS size < 15px) and no larger
    responsive size. Footers, captions, legal, labels, tables, nav, buttons are ignored.
    With --surface product|dashboard|native the floor is 13px, except paragraphs of 60+
    words, which keep 15px.
    FP: product UI scanned without --surface.
eyebrow-pill [7] ai_tells.0.10  (high)
    The element right before an h1/h2 is short (<= 60 chars, <= 9 words) and is either
    (a) a pill: class pill|badge|chip|lozenge|announcement, a Badge/Pill/Chip component,
    Tailwind rounded-full + border/bg + small text, CSS 999px radius + border/background;
    (b) a launch label: text starting New / Now / Introducing / Announcing / Meet /
    Powered by / Just launched / Beta / vX / an emoji; or (c) a plain eyebrow: class
    eyebrow|kicker|overline|tag|label|tagline, uppercase + tracking, tiny mono text.
    (a), (b) and anything above the h1 always count, except a plain label (c) above the h1 that names the
    product (shares a word with the <title> or the logo/wordmark) or carries a date: the rule's own
    exception. (c) above h2s is tolerated up to one per three h1/h2 sections (the research's ceiling) and
    flagged beyond that.
    With --surface product|dashboard|native, a pill or launch label of 1-2 words
    ("Beta", "New") beside a page title is allowed.
    FP: a news category over an article title; a product name the <title> does not contain.
icon-card-grid [7] ai_tells.0.14  (high)
    A parent with 3+ same-tag children, >= 75% of them shaped icon -> title -> text
    (icon = svg, <i>, icon class, *Icon component, emoji-only element); or a JS array
    with 3+ objects that all have icon + title + description keys, reported only when
    the same file renders a multi-column grid (grid-cols-2..6, grid-template-columns,
    flex-wrap) and its .map() template stacks the item's icon above its title. Objects
    with href/url/path/to/route/onClick/action/shortcut keys (nav menus, settings
    indexes, command palettes) are skipped. An icon that sits beside its heading in a
    flex row (the recommended alternative) is not counted.
    FP: real docs/category indexes where an icon identifies each object type.
too-many-typefaces [6] typography.0.8  (med)
    4+ distinct non-generic families declared or loaded.
    FP: font specimens, multi-brand pages, unused loaded fonts.
emoji-icon [6] ai_tells.0.18  (med)
    Emoji / pictographic glyphs (U+1F300-1FAFF, U+2600-27BF except stars) inside
    headings, buttons, links, nav, labels, summary, li inside nav/aside, icon/badge/
    tab/feature classes, emoji-only elements, or JS data fields icon/emoji/symbol.
    Flags (U+1F1E6-1F1FF) are not checked.
    FP: products where emoji are user content or a deliberate brand device (Notion pages).
pure-black-white [6] color.0.28  (med)
    html/body/:root/#root/#__next/main (or Tailwind min-h-screen wrappers) with
    background exactly #000; ink exactly #000; or background exactly #fff when the unit
    has no second surface tier. Any declared non-white section or surface ground counts
    as one: an off-white (lightness 0.90-0.985), a brand-colour band or an inverted dark
    section (section/band/hero/footer/panel/card... selectors or elements, --surface-*/
    --card/--muted tokens, Tailwind bg-* on section-like elements). Also --background/
    --foreground tokens. Ignored inside @media (prefers-contrast).
    FP: true-black media viewers and product-render sections lit on black.
glassmorphism [5] ai_tells.0.25  (med)
    backdrop-filter blur / Tailwind backdrop-blur on content (not nav, header, toolbar,
    sticky/fixed bars, menus, dialogs, overlays): flagged when 2+ such surfaces exist,
    or 1 on a card/panel/tile/glass/feature/pricing element.
    FP: floating media controls over video; native-like sheets not named as such.
mono-display [5] typography.0.20  (med)
    Monospace family (or Tailwind font-mono) on body/html, h1-h4, p, blockquote, hero/
    title/headline/lead/tagline/subtitle classes, or any element with 8+ words.
    Short mono labels, code, pre, kbd, terminals and data cells are not flagged.
    FP: developer tools whose product IS a terminal; specimen pages.
numbered-sections [4] ai_tells.0.12  (med)
    A run of zero-padded 01 -> 02 -> 03 (optionally "Step/Phase/Section 01", "01 /", "01.")
    or "Step 1 -> Step 2 -> Step 3" as short standalone text, or "01".."03" string values
    under step/number/index/label keys in JS data. Times like 01:30 and numbers inside
    tables, <time>, <select> are ignored.
    FP: genuine ordered procedures (install guides) and real image pagination.
uniform-radius [4] ai_tells.0.15  (med)
    6+ radius values (CSS border-radius, Tailwind rounded-*) where one value >= 12px
    covers >= 70% of non-pill uses (pills 999px/50%/rounded-full excluded).
    FP: soft-brand systems that documented one radius on purpose (still nest concentrically).
accent-hue-count [4] ai_tells.0.29  (med)
    Saturated colours (chroma >= 0.2) grouped into hue families: 3+ non-semantic
    families (orange, cyan/teal, blue, violet, pink) or 6+ families in total
    (red/green/amber count as semantic). Gradient stops, inline <svg>, chart/syntax
    tokens and Tailwind shades below 400 are excluded.
    FP: data-viz palettes not named chart/data/series; multi-product colourway pages.
tracked-caps-labels [4] ai_tells.0.11  (med)
    4+ uppercase elements/rules tracked wider than +0.1em (outside the research band of
    +0.03..+0.1em), or any one at >= 0.15em (the 0.18-0.22em AI eyebrow). Table headers
    (th, thead) are exempt; caps inside the band are never counted.
    FP: editorial systems that set wide caps tags deliberately.
template-copy [4] ai_tells.0.34  (med)
    Visible text and prose strings with: streamline, empower, supercharge, world-class,
    next-gen, elevate, seamless, unleash, revolutionize, game-changer, delve, tapestry,
    unlock, cutting-edge, state-of-the-art, lightning/blazing-fast, user-friendly,
    effortless, skyrocket, to the next level, all-in-one, reimagined, powered by AI,
    Introducing, "Welcome to our website" (buzzwords are reported only when a file has
    2+ of them or one sits in a heading/button/<title>, so a lone "streamlined" in long
    prose passes); always reported: "Not X. Just Y.", "No X. No Y.", "No X, just Y.",
    "Ready to transform/get started ...".
    FP: legitimate literal uses ("unlock the door", "elevate the bed head").
placeholder-content [4] copy_content.0.15  (med)
    lorem ipsum, John/Jane Doe/Smith, Acme, "Your Company"/"Company Name", placeholder
    image hosts (placehold.co, via.placeholder, picsum, pravatar, randomuser, ui-avatars).
    FP: a brand actually named Acme; test fixtures inside the scanned folder.
generic-cta-label [4] copy_content.0.21  (med)
    <button>, input[type=submit], role=button or .btn/.cta link whose whole label is
    Submit, Continue, OK, Okay, Yes, No or Click here ("Click here" is (std) usability
    practice, not from the research). Options in a set are not calls to action and are
    skipped: role radio/option/tab/switch/checkbox, aria-pressed/-checked/-selected, or a
    parent within 3 levels with role radiogroup/listbox/tablist/group/toolbar or <fieldset>.
    FP: genuine yes/no confirmation pairs in system dialogs.
hero-centered-two-tone [4] ai_tells.0.36  (med)
    The first h1 of a file is centred (text-center / text-align:center on it or an
    ancestor within 4 levels, with no sm/md/lg:text-left) AND contains an accent run
    (see headline-accent-word).
    FP: a poster-like campaign hero where the accented word is the product itself.
reduced-motion-missing [4] accessibility_performance.0.33  (med)
    Animations, Framer Motion or transform transitions exist but nothing in the unit
    mentions prefers-reduced-motion, motion-reduce:/motion-safe:, useReducedMotion or
    reducedMotion.
    FP: reduced-motion handled in a file outside the scan.
linear-easing [4] motion_interaction.0.5  (med)
    transition / *-timing-function / non-infinite animation using linear; Tailwind
    ease-linear. linear() spring curves, spinners, marquees and progress are ignored.
    FP: scroll-scrubbed sequences where linear mapping to scroll is intended.
layout-prop-animation [4] motion_interaction.0.34  (med)
    transition(-property) or @keyframes animating width/height/max-height/top/left/
    right/bottom/margin/padding/inset; Tailwind transition-[width|height|...].
    FP: accordions on content too small to matter.
cream-terracotta [4] ai_tells.0.6  (med)
    The look's neighbourhood, not only its exact hexes: a warm light ground (a background
    or --bg/--canvas/--surface/--paper token at OKLCH L >= 0.88, chroma 0.004-0.06, hue
    30-100: cream, ivory, greige) together with a clay accent anywhere outside semantic
    error/warning tokens (OKLCH L 0.35-0.72, chroma >= 0.08, hue 10-52: terracotta, rust,
    brick) or oxblood. The message gives the OKLab distance (dE_ok) to the nearest spent
    hex in the ai-tells looks table; renaming the tones after the reference world does not
    move them. Red-brand pages whose neutrals are tinted toward the red land here too: that
    is the point (tinting toward a clay accent recreates the look).
    FP: subjects really made of these materials (ceramics, bakery, paper goods).
headline-accent-word [3] ai_tells.0.9  (low)
    An h1/h2 (<= 140 chars) containing an inline <em>/<i>/<mark>/<u> or a span styled
    by a gradient/accent/highlight/italic/serif class, a saturated text colour (class,
    inline or CSS), gradient clip or a different font-family. Muted grey spans and runs
    without letters (version numbers, counts) are ignored.
    FP: titles that italicise a work title or a foreign word.
side-stripe-border [3] ai_tells.0.17  (low)
    border-left/right/top/inline-start >= 2px in a saturated colour on a card/callout
    (shorthand or longhands; Tailwind border-l-4 + chromatic border colour), unless the
    other sides share the same width. blockquote and border-bottom tab underlines exempt.
    FP: chart legends and diff views where the stripe encodes data.
colored-glow [3] ai_tells.0.24  (low)
    box-shadow / text-shadow / drop-shadow with blur >= 15px, saturated colour
    (saturation > 0.3) at alpha >= 0.1; Tailwind shadow-<hue>-<shade> and arbitrary
    shadow-[...] glows.
    FP: focus rings drawn as blurred shadows (use outline instead anyway).
ambient-glow-bg [3] ai_tells.0.23  (low)
    radial/conic gradients with a saturated stop (alpha >= 0.08), CSS blobs (filter blur
    >= 40px + saturated background), Tailwind absolute rounded-full blur-2xl/3xl blobs.
    FP: a real light-falloff vignette behind a product render.
ambient-animation [3] ai_tells.0.27  (low)
    Every infinite animation (CSS infinite, Tailwind animate-pulse/ping/bounce, Framer
    repeat: Infinity, GSAP repeat:-1), marquee/ticker. Spinners, loaders and skeletons
    are exempt (same test as animation-overload).
    FP: a pulse on a real live-data indicator.
em-dash [3] ai_tells.0.33  (low)
    3+ em-dashes in visible copy of one file.
    FP: long-form editorial content where the house style uses em-dashes.
vanity-metrics [3] ai_tells.0.13  (low)
    3+ sibling elements each led by a bare metric (10K+, 99.9%, 4.9/5, 3x, 24/7, 12ms),
    or 3+ such value: strings in JS data. Price rows and anything inside a <table>
    (account codes, years, IDs) are ignored.
    FP: a real KPI dashboard with real data.
stock-photo [3] ai_tells.0.19  (low)
    URLs on images.unsplash.com, source.unsplash.com, pexels, istock, shutterstock,
    getty, freepik.
    FP: commissioned work hosted on those services.
ai-favourite-font [2] ai_tells.0.3  (low)
    Space Grotesk, Instrument Serif/Sans, Fraunces, Geist, Syne, Bricolage Grotesque,
    Sora, Young Serif, Plus Jakarta Sans, DM Sans/Serif, Outfit, Playfair, Cormorant,
    Lora, Crimson, Newsreader, Recoleta, IBM Plex Sans/Serif (mono cuts ignored); plus
    the next rotation that a01/a05 recommend as Inter replacements: Satoshi, Clash
    Display, Clash Grotesk, Cabinet Grotesk, Geist Display.
    Tension: one source recommends Geist/Outfit as Inter replacements; low severity.
scroll-reveal-everything [2] ai_tells.0.28  (low)
    3+ scroll-reveal elements (data-aos, whileInView, reveal/fade-up/slide-up classes).
    FP: none common; one reveal per page is fine.
gradient-text [2] ai_tells.0.22  (low)
    background-clip:text / -webkit-background-clip:text / Tailwind bg-clip-text.
    A purple gradient additionally triggers purple-ai-colour [11].
grey-minimal-pill [3] ai_tells.0.43  (low)
    A declared light neutral page ground (lightness >= 0.9, chroma <= 0.03), no
    saturated colour outside red/amber/green status anywhere, fewer than 2 photos, and a
    rounded-full (or 100px+ radius) near-black button or link.
    FP: a monochrome brand whose photography carries the colour but is loaded at runtime.
near-black-neon [2] ai_tells.0.8  (low)
    A neutral near-black page ground (lightness <= 0.09, chroma <= 0.03: #000-#171717)
    plus a neon accent (HSL saturation > 0.6, hue 75-165 or 5-20; Tailwind emerald/
    green/lime 400+) on an --accent/--primary/--brand token, a CTA or a badge/pill/step.
    Status selectors (error, success ...) and dark-theme blocks are ignored.
    FP: a brand whose documented colour really is that green.
outline-removed [2] accessibility_performance.0.24  (low)
    outline: none|0 or Tailwind outline-none/outline-0 when the unit has no
    :focus-visible rule, no focus-visible: variant and no focus:ring|shadow|border.
    FP: focus styles defined in a stylesheet outside the scan.
broadsheet [1★ Anthropic] ai_tells.0.68  (low)
    Zero radius (no radius at all, or >= 90% of radius uses at 0), 6+ hairline rules
    (1px border-top/bottom, border-t/border-b/divide-y, <hr>) and 2+ uppercase mono labels.
    FP: a real newspaper or archive whose brand is that look.
transition-all [1★ Vercel] motion_interaction.0.35  (low)
    transition: all ..., transition-property: all, Tailwind transition-all.
zoom-disabled [1★ Vercel] accessibility_performance.0.26  (low)
    viewport meta with user-scalable=no|0 or maximum-scale=1; Next.js viewport config
    userScalable: false / maximumScale: 1.
hero-h-screen [3] spacing_layout.0.22  (low)
    Tailwind h-screen on a section/header or hero element; height: 100vh in a hero rule.
    min-h-screen is not flagged.
apple-font-on-web [A3] apple.1.29  (low)
    An @font-face whose family or src names SF Pro, SF Compact, SF Mono, New York, SF
    Symbols or San Francisco (Apple-platform licence only (std)).
apple-tokens [syn] synthesis  (low)
    3+ of the apple.com values #f5f5f7, #1d1d1f, #6e6e73, #0066cc, #0071e3, #2997ff
    anywhere in the unit: the Apple costume rather than the brand's own palette.
    FP: an Apple reference mock or an Apple-platform app's marketing page.
uniform-item-grid [7] ai_tells.0.14  (med: reported below the rule's weight because it extends the
    icon-on-top rule to its icon-less variant)
    A grid parent (CSS display:grid with 2+ column tracks, or Tailwind grid-cols-2..6) whose 4+ children are
    all title + blurb items: a short title (h3-h6, dt, strong or b, 8 words or fewer) followed by 6-60 words of
    text, wherever an icon sits. Footer, nav, tables, forms and figures (depicted product UI) are
    skipped; marketing surface only.
    FP: a real index of equal objects (a docs category page); a glossary set as a grid.
repeated-item-pattern [14] ai_tells.0.41  (med: a heuristic for "never repeat one section pattern")
    3+ sections (section/article elements, or h2-headed blocks) each built around a list of 3+ title + blurb
    items (same item test as uniform-item-grid; dl/dt+dd pairs, li with strong + text, div with h3 + p).
    Marketing surface only (settings and inspector rows repeat this shape by design).
    FP: a long docs or FAQ page whose content really is a series of definition lists.
native-control-default [5] process_mindset.0.34  (med)
    An <input type="range"> while no stylesheet in the unit styles a slider thumb or track
    (::-webkit-slider-thumb, ::-moz-range-thumb, ::-webkit-slider-runnable-track, ::-moz-range-track).
    accent-color alone counts as default. Checkboxes and radios are not checked (accent-color is a
    reasonable native treatment there).
    FP: a product UI that deliberately keeps platform-native controls (then document it in DESIGN.md).
design-commentary [3] copy_content.0.19  (low)
    An HTML or block comment in a page that reads like a design spec: 3+ of "thesis", "reference world",
    "signature move", "direction card(s)", "values to confirm", "rejected", "overrides:", "don't:".
    FP: a template or fixture whose comment documents itself for developers (move it to a README).
brief-echo [3] copy_content.0.19  (low)  only with --brief FILE
    A run of 5+ consecutive words (at least 2 of them not stop words) shared by the brief file and the
    visible copy, ignoring words that appear in the <title> or a heading of the brief's product name.
    FP: product names, legal names and quoted specs the brief supplies verbatim.
fixture-face [syn] synthesis  (low)
    A family loaded or declared by the page that one of this skill's clean fixtures uses
    (scripts/fixtures/clean*.html, read at run time). Files inside the fixtures folder are exempt.
    FP: a brief that pins that face.
heading-cadence [syn] synthesis  (low)
    5+ h1/h2 headings on a page and at least 80% of them are sentences ending in a full stop.
    FP: an established brand whose house voice is the short declarative (then keep it to known categories).
"""

from __future__ import print_function

import argparse
import bisect
import colorsys
import html as htmllib
import json
import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict

# --------------------------------------------------------------------------------------
# Rule table
# --------------------------------------------------------------------------------------

RULES = OrderedDict()


def _rule(rid, key, weight, title, fix, label=None, sev=None):
    """label overrides the printed evidence tag: '1★ Vercel' for one canonical source, 'syn' for a synthesis.
    sev caps the severity of a heuristic that only approximates its research rule (documented per rule)."""
    RULES[rid] = {'id': rid, 'key': key, 'weight': weight, 'title': title, 'fix': fix,
                  'label': label or str(weight), 'sev': sev}


_rule('stock-section-sequence', 'ai_tells.0.41', 14,
      'Page assembled from the stock SaaS section sequence',
      'Derive sections from this page\'s content; cut stock blocks (logo cloud, stat strip, 3 cards, steps, '
      'testimonials, highlighted-middle pricing, CTA strip) that carry no real information, and give the '
      'remaining sections their own structure.')
_rule('default-font-only', 'ai_tells.0.2', 13,
      'Default font is the only voice',
      'Set headings in a licensed face with character chosen for this brand (audition 3 in the real layout); '
      'keep Inter/system-ui only as the body/UI workhorse. Native apps and dense data tools may use SF/system-ui '
      'deliberately.')
_rule('purple-ai-colour', 'ai_tells.0.0', 11,
      'Purple/violet gradient, CTA fill or brand token',
      'Take the accent from the brand\'s own world (materials, photography, domain); use a neutral active state '
      '(a fill step in the neutral ramp). Purple only if it is an existing brand asset, and never as a gradient '
      'on white.')
_rule('neg-tracking-small', 'typography.0.51', 11,
      'Negative letter-spacing at 12px or below',
      'Track inversely to size: body text at or near 0, small labels and captions +0.03 to +0.1em; never '
      'negative at 12px or smaller.')
_rule('tracking-too-tight', 'typography.0.51', 11,
      'Tracking tighter than -0.04em',
      'Tighten headings gradually (about -0.02em at h1) and go no tighter than -0.04em on the largest type '
      '(Tailwind tracking-tighter is -0.05em; use tracking-[-0.03em]).')
_rule('animation-overload', 'motion_interaction.0.0', 11,
      'Too many animations',
      'Keep only motion whose job fits in one sentence (feedback, state change, one signature story motion); '
      'delete the rest.')
_rule('body-text-small', 'typography.0.42', 7,
      'Body copy below 15px',
      'Set body copy at 16-17px (1rem-1.0625rem) with line-height about 1.5; enlarge or delete detail text '
      'that is too small to read.')
_rule('eyebrow-pill', 'ai_tells.0.10', 7,
      'Eyebrow label / pill badge above a heading',
      'Delete it and work its words into the heading or body. Keep one only if it carries information the '
      'heading lacks (product name, date, category), in sentence case, at most once per three sections.')
_rule('icon-card-grid', 'ai_tells.0.14', 7,
      'Grid of icon + title + text feature cards',
      'Build the section from the content: 2-column zig-zag, asymmetric grid, real product graphics or a list; '
      'put icons beside headings, not in tiles above them.')
_rule('too-many-typefaces', 'typography.0.8', 6,
      'Four or more typefaces',
      'One family is enough, two at most (heading + body); a third only for code or data.')
_rule('emoji-icon', 'ai_tells.0.18', 6,
      'Emoji used as an icon',
      'Replace with one drawn icon family (authored SVG or one library at one stroke width) or remove the icon.')
_rule('pure-black-white', 'color.0.28', 6,
      'Pure #000 / #fff page ground or ink',
      'Ink near-black (#111-#1d1d1f); dark grounds brand-tinted off-black (brand hue at 1-10% HSL lightness); a '
      'neutral #0a0a0a-#121212 only when chosen for a reason written in DESIGN.md; pure #fff only alongside a '
      'second surface tier (a tinted off-white, a brand band or an inverted section).')
_rule('glassmorphism', 'ai_tells.0.25', 5,
      'Frosted-glass content surfaces',
      'Keep backdrop blur on the floating functional layer only (sticky nav, toolbar, sheet, overlay); make '
      'content cards solid.')
_rule('mono-display', 'typography.0.20', 5,
      'Monospace used for display or body text',
      'Reserve monospace for code, IDs, timestamps and data; set headings and copy in the display/text face.')
_rule('numbered-sections', 'ai_tells.0.12', 4,
      '01 / 02 / 03 numbering',
      'Name the topic in plain words; for a real procedure use verb-noun steps (Install, Configure, Ship) in '
      'an <ol>.')
_rule('uniform-radius', 'ai_tells.0.15', 4,
      'One large radius on everything',
      'Use a radius scale by role (e.g. 8px inputs, 12-16px cards, 20-28px large containers, pills only for '
      'actions) and nest concentrically (inner = outer - padding).')
_rule('accent-hue-count', 'ai_tells.0.29', 4,
      'Too many accent hues',
      'One accent for action, selection and focus plus semantic red/amber/green; set stat cards, icon chips '
      'and badges neutral (supports color.0.0 [9]: neutrals + exactly one accent).')
_rule('tracked-caps-labels', 'ai_tells.0.11', 4,
      'All-caps labels tracked past +0.1em',
      'Sentence or title case with normal tracking; if caps stay on a short tag, +0.03 to +0.1em, never '
      '0.18-0.22em.')
_rule('template-copy', 'ai_tells.0.34', 4,
      'Template / buzzword copy',
      'Name what the product literally does with real nouns and numbers; cut buzzwords and "Not X. Just Y." '
      'cadences.')
_rule('placeholder-content', 'copy_content.0.15', 4,
      'Placeholder content',
      'Replace lorem ipsum, placeholder names/brands and placeholder images with real, brief-specific content.')
_rule('generic-cta-label', 'copy_content.0.21', 4,
      'Generic button label',
      'Label the button with the action it performs ("Save changes", "Send invoice").')
_rule('hero-centered-two-tone', 'ai_tells.0.36', 4,
      'Centred template hero with a two-tone headline',
      'Change the hero\'s structure, not its skin: one-face, one-colour headline with emphasis from size or '
      'weight, in a content-led (often left-aligned or asymmetric) composition.')
_rule('reduced-motion-missing', 'accessibility_performance.0.33', 4,
      'No prefers-reduced-motion path',
      'Add @media (prefers-reduced-motion: reduce) that swaps movement for a short opacity fade or a static '
      'state (keep state feedback; pause loops with animation-play-state).')
_rule('linear-easing', 'motion_interaction.0.5', 4,
      'Linear easing on UI motion',
      'Use a strong ease-out such as cubic-bezier(0.16, 1, 0.3, 1); keep linear for continuous rotation or '
      'progress.')
_rule('layout-prop-animation', 'motion_interaction.0.34', 4,
      'Animating layout properties',
      'Animate transform and opacity only (for an expanding panel, grid-template-rows 0fr -> 1fr (std) or a '
      'transform).')
_rule('cream-terracotta', 'ai_tells.0.6', 4,
      'Cream ground + terracotta accent',
      'Sample the palette from photos of the actual subject and name the tones after it; never pick from a list '
      'of safe alternatives. Cream only when the subject is made of it, then always replace the terracotta/rust '
      'accent and default to a sans display.')
_rule('headline-accent-word', 'ai_tells.0.9', 3,
      'Accent word inside a headline',
      'Set the headline in one face, one style and one colour; get emphasis from size or weight.')
_rule('side-stripe-border', 'ai_tells.0.17', 3,
      'Coloured side-stripe border',
      'Mark the card or state with a full fill change, weight, or a neutral 1px border.')
_rule('colored-glow', 'ai_tells.0.24', 3,
      'Coloured glow shadow',
      'Use neutral shadows with a real Y offset and soft blur (two layers), or none.')
_rule('ambient-glow-bg', 'ai_tells.0.23', 3,
      'Decorative glow / blob / mesh background',
      'Let photography, a lit product render or a flat tinted ground carry the atmosphere.')
_rule('ambient-animation', 'ai_tells.0.27', 3,
      'Infinite decorative animation',
      'Delete the loop; pulse only indicators tied to real live data, and give anything kept a reduced-motion pause.')
_rule('em-dash', 'ai_tells.0.33', 3,
      'Em-dashes in UI copy',
      'Replace with a period, comma, colon or parentheses; use a hyphen for ranges (2018-2026).')
_rule('vanity-metrics', 'ai_tells.0.13', 3,
      'Big-number stat strip',
      'Show real content; use metrics only where real data backs them, in context.')
_rule('stock-photo', 'ai_tells.0.19', 3,
      'Stock photography',
      'Use your own product shots, commissioned photography or brand-specific illustration.')
_rule('ai-favourite-font', 'ai_tells.0.3', 2,
      'LLM-favourite "distinctive" font',
      'Audition faces outside the current LLM rotation; pick for this brand\'s voice, not the category cliche.')
_rule('scroll-reveal-everything', 'ai_tells.0.28', 2,
      'Fade/slide-in on every section',
      'Let content be present; keep at most one deliberate entrance per page.')
_rule('gradient-text', 'ai_tells.0.22', 2,
      'Gradient-filled text',
      'Set text in a solid colour; create emphasis with size or weight.')
_rule('grey-minimal-pill', 'ai_tells.0.43', 3,
      'Grey trend-minimal page with a black pill CTA',
      'Commit harder on an existing element (bigger type scale, full-contrast primary text, a real colour or '
      'image); a black pill on a grey page is the template, not a neutral default.')
_rule('near-black-neon', 'ai_tells.0.8', 2,
      'Near-black ground with one neon accent',
      'Go dark only when the use scene argues for it; use a brand-tinted off-black and an accent from the brand '
      '(OKLCH chroma 0.15 or less), not emerald, acid green or vermilion by reflex.')
_rule('outline-removed', 'accessibility_performance.0.24', 2,
      'Focus outline removed without a replacement',
      'Keep a visible 2px :focus-visible ring (3:1 against its surroundings) on every focusable control.')
_rule('broadsheet', 'ai_tells.0.68', 1,
      'Broadsheet hairlines look (zero radius + rules + mono caps)',
      'Zero radius is a brand decision, not an anti-rounding reflex; drop the tracked mono labels and let the '
      'subject\'s world set the structure.', label='1★ Anthropic')
_rule('transition-all', 'motion_interaction.0.35', 1,
      'transition: all',
      'Name the properties: transition-property: opacity, transform (Tailwind transition-[opacity,transform] '
      'or transition-transform).', label='1★ Vercel')
_rule('zoom-disabled', 'accessibility_performance.0.26', 1,
      'Browser zoom disabled',
      'Remove user-scalable=no and maximum-scale=1; set mobile inputs to 16px+ so iOS does not auto-zoom.',
      label='1★ Vercel')
_rule('hero-h-screen', 'spacing_layout.0.22', 3,
      'Hero sized with h-screen / 100vh',
      'Use min-height: 100dvh (or calc(100svh - header height)) so content never clips on mobile browsers.')
_rule('apple-font-on-web', 'apple.1.29', 3,
      'Apple system font self-hosted on the web',
      'Never embed SF; SF Pro, New York and SF Symbols are licensed for Apple-platform UI only (std). Ship your '
      'own licensed face, or reference the platform face through system-ui without embedding it.', label='A3')
_rule('uniform-item-grid', 'ai_tells.0.14', 7,
      'Uniform grid of title + blurb items (icon optional)',
      'Moving the icon beside the title does not fix a uniform grid: show each item in context (the rule applied '
      'to a real line, the part on the drawing), vary size by importance, give each a distinct real visual, or '
      'set it as a plain list.', sev='med')
_rule('repeated-item-pattern', 'ai_tells.0.41', 14,
      'One title + blurb list pattern repeated across sections',
      'Give each section a format that fits its content (a table, a drawing with callouts, one long paragraph, a '
      'step sequence, a comparison); keep the title + blurb list for at most one section.', sev='med')
_rule('native-control-default', 'process_mindset.0.34', 5,
      'Native range control left at the browser default',
      'Restyle the track and thumb (appearance: none plus ::-webkit-slider-thumb / ::-moz-range-thumb) to the '
      'radius, colour and size tokens; accent-color alone keeps the browser default pill track and round thumb.')
_rule('design-commentary', 'copy_content.0.19', 3,
      'Design rationale shipped in the page source',
      'Keep DESIGN.md as its own file (or in the reply when only one file may be delivered); shipped markup carries '
      'no thesis, rejected directions or "values to confirm" notes.')
_rule('brief-echo', 'copy_content.0.19', 3,
      'Visible copy pasted from the brief',
      'Rewrite in words the audience uses for itself (role and context, e.g. "for site engineers on '
      'call"), never the segment or positioning phrasing of the brief.')
_rule('fixture-face', 'synthesis', 0,
      'Typeface copied from the clean fixtures of this skill',
      'The fixtures show that a direction can be clean, not which face to use: audition faces found through the '
      'reference world of this brief and leave the fixture faces out.', label='syn')
_rule('heading-cadence', 'synthesis', 0,
      'Every heading is a full-stop declarative',
      'Keep the full-stop statement for the hero and at most 2 section heads; informational modules (specs, '
      'pricing, integrations, security, care) take plain labels or questions, and adjacent heads vary in form.',
      label='syn')
_rule('apple-tokens', 'synthesis', 0,
      'Apple.com colour tokens copied as the palette',
      'Values such as #f5f5f7, #1d1d1f, #6e6e73, #0066cc, #0071e3 and #2997ff are apple.com measurements, not '
      'defaults; derive the canvas, ink and accent from this brand.', label='syn')


def rule_severity(r):
    return r.get('sev') or severity_for(r['weight'])


def severity_for(weight):
    if weight >= 7:
        return 'high'
    if weight >= 4:
        return 'med'
    return 'low'


SEV_ORDER = {'high': 0, 'med': 1, 'low': 2}

# Surface type pinned in the brief (SKILL.md section 6). Set by --surface; product, dashboard and native relax the
# rules the research scopes to brand/marketing surfaces (default font, 13-15px UI text, status badges over titles).
SURFACES = ('marketing', 'product', 'dashboard', 'native')
SURFACE = 'marketing'


def tool_surface():
    return SURFACE in ('product', 'dashboard', 'native')

# --------------------------------------------------------------------------------------
# Generic helpers
# --------------------------------------------------------------------------------------

EXTS = {'.html', '.htm', '.css', '.scss', '.sass', '.less', '.js', '.jsx', '.ts', '.tsx', '.mjs',
        '.cjs', '.vue', '.svelte', '.astro'}
SKIP_DIRS = {'node_modules', 'dist', 'build', 'out', 'coverage', 'vendor', 'venv', '__pycache__',
             'storybook-static', 'bower_components', 'target'}
MARKUP_EXTS = {'.html', '.htm', '.vue', '.svelte', '.astro'}
JSX_EXTS = {'.jsx', '.tsx'}
CSS_EXTS = {'.css', '.scss', '.sass', '.less'}
JS_EXTS = {'.js', '.mjs', '.cjs', '.ts', '.jsx', '.tsx'}

HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
CODE_TAGS = {'code', 'pre', 'kbd', 'samp', 'script', 'style', 'svg', 'math', 'textarea', 'noscript'}
VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param',
             'source', 'track', 'wbr'}
BLOCK_TAGS = {'div', 'section', 'article', 'aside', 'header', 'footer', 'nav', 'main', 'ul', 'ol',
              'table', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'figure', 'blockquote', 'pre'}


def blank_match(m):
    return re.sub(r'[^\n]', ' ', m.group(0))


def shorten(s, n=140):
    s = re.sub(r'\s+', ' ', s or '').strip()
    return s if len(s) <= n else s[:n - 3] + '...'


def match_brace(s, i, open_ch='{', close_ch='}'):
    """s[i] == open_ch. Return index just after the matching close_ch (string-aware)."""
    depth = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c in '"\'`':
            q = c
            i += 1
            while i < n and s[i] != q:
                if s[i] == '\\':
                    i += 1
                i += 1
        elif c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def match_paren(s, i):
    depth = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def split_top(s, sep=','):
    """Split on sep outside (), [] and quotes."""
    out, cur, depth, q = [], [], 0, None
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
            continue
        if ch in '"\'':
            q = ch
        elif ch in '([':
            depth += 1
        elif ch in ')]':
            depth = max(0, depth - 1)
        elif ch == sep and depth == 0:
            out.append(''.join(cur))
            cur = []
            continue
        cur.append(ch)
    out.append(''.join(cur))
    return out


def parse_len_px(tok, base=16.0):
    m = re.match(r'^\s*(-?\d*\.?\d+)\s*(px|rem|em|pt)?\s*$', tok or '')
    if not m:
        return None
    v = float(m.group(1))
    u = m.group(2) or 'px'
    if u == 'px':
        return v
    if u in ('rem', 'em'):
        return v * base
    if u == 'pt':
        return v * 4.0 / 3.0
    return None


# --------------------------------------------------------------------------------------
# Colour parsing
# --------------------------------------------------------------------------------------

NAMED = {
    'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0), 'green': (0, 128, 0),
    'blue': (0, 0, 255), 'purple': (128, 0, 128), 'violet': (238, 130, 238), 'indigo': (75, 0, 130),
    'blueviolet': (138, 43, 226), 'mediumpurple': (147, 112, 219), 'rebeccapurple': (102, 51, 153),
    'darkviolet': (148, 0, 211), 'darkorchid': (153, 50, 204), 'mediumorchid': (186, 85, 211),
    'slateblue': (106, 90, 205), 'mediumslateblue': (123, 104, 238), 'darkslateblue': (72, 61, 139),
    'fuchsia': (255, 0, 255), 'magenta': (255, 0, 255), 'orchid': (218, 112, 214), 'plum': (221, 160, 221),
    'orange': (255, 165, 0), 'gold': (255, 215, 0), 'yellow': (255, 255, 0), 'teal': (0, 128, 128),
    'cyan': (0, 255, 255), 'aqua': (0, 255, 255), 'navy': (0, 0, 128), 'pink': (255, 192, 203),
    'hotpink': (255, 105, 180), 'deeppink': (255, 20, 147), 'crimson': (220, 20, 60),
    'tomato': (255, 99, 71), 'coral': (255, 127, 80), 'lime': (0, 255, 0), 'limegreen': (50, 205, 50),
    'royalblue': (65, 105, 225), 'dodgerblue': (30, 144, 255), 'deepskyblue': (0, 191, 255),
    'gray': (128, 128, 128), 'grey': (128, 128, 128), 'silver': (192, 192, 192),
    'whitesmoke': (245, 245, 245), 'ivory': (255, 255, 240), 'beige': (245, 245, 220),
    'linen': (250, 240, 230), 'snow': (255, 250, 250), 'ghostwhite': (248, 248, 255),
    'seashell': (255, 245, 238), 'floralwhite': (255, 250, 240), 'oldlace': (253, 245, 230),
    'antiquewhite': (250, 235, 215),
}
COLOR_RE = re.compile(
    r'#[0-9a-fA-F]{3,8}(?![0-9a-zA-Z_-])|\b(?:rgba?|hsla?|oklch)\([^()]*\)|(?<![\w-])(?:'
    + '|'.join(sorted(NAMED, key=len, reverse=True)) + r')(?![\w-])', re.I)
BARE_HSL_RE = re.compile(r'^\s*(-?\d*\.?\d+)(?:deg)?\s+(\d*\.?\d+)%\s+(\d*\.?\d+)%\s*(?:/\s*(\d*\.?\d+%?))?\s*$')


def _alpha(tok):
    tok = tok.strip()
    if tok.endswith('%'):
        return float(tok[:-1]) / 100.0
    return float(tok)


def _hue(tok):
    tok = tok.strip().lower()
    if tok.endswith('deg'):
        return float(tok[:-3])
    if tok.endswith('turn'):
        return float(tok[:-4]) * 360
    if tok.endswith('grad'):
        return float(tok[:-4]) * 0.9
    if tok.endswith('rad'):
        return math.degrees(float(tok[:-3]))
    if tok == 'none':
        return 0.0
    return float(tok)


def _pct(tok, scale):
    tok = tok.strip()
    if tok == 'none':
        return 0.0
    if tok.endswith('%'):
        return float(tok[:-1]) / 100.0 * scale
    return float(tok)


def _oklch_to_rgb(L, C, H):
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    def enc(x):
        x = max(0.0, min(1.0, x))
        return 12.92 * x if x <= 0.0031308 else 1.055 * (x ** (1 / 2.4)) - 0.055
    return enc(r) * 255, enc(g) * 255, enc(bb) * 255


def parse_color(s):
    s = (s or '').strip().lower()
    if not s:
        return None
    if s.startswith('#'):
        h = s[1:]
        if len(h) in (3, 4):
            h = ''.join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        try:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            a = int(h[6:8], 16) / 255.0 if len(h) == 8 else 1.0
        except ValueError:
            return None
        return (r, g, b, a)
    m = BARE_HSL_RE.match(s)
    if m:
        r, g, b = colorsys.hls_to_rgb((float(m.group(1)) % 360) / 360.0, float(m.group(3)) / 100.0,
                                      float(m.group(2)) / 100.0)
        a = _alpha(m.group(4)) if m.group(4) else 1.0
        return (r * 255, g * 255, b * 255, a)
    m = re.match(r'^(rgba?|hsla?|oklch)\((.*)\)$', s, re.S)
    if m:
        fn, body = m.group(1), m.group(2)
        if 'var(' in body or 'from ' in body:
            return None
        body = body.replace('/', ' / ').replace(',', ' ')
        parts = body.split()
        alpha = 1.0
        try:
            if '/' in parts:
                k = parts.index('/')
                if k + 1 < len(parts):
                    alpha = _alpha(parts[k + 1])
                parts = parts[:k]
            elif len(parts) >= 4:
                alpha = _alpha(parts[3])
                parts = parts[:3]
            if len(parts) < 3:
                return None
            if fn.startswith('rgb'):
                r, g, b = [_pct(p, 255.0) for p in parts[:3]]
            elif fn.startswith('hsl'):
                hh = _hue(parts[0]) % 360
                ss = float(parts[1].rstrip('%')) / 100.0
                ll = float(parts[2].rstrip('%')) / 100.0
                r, g, b = [v * 255 for v in colorsys.hls_to_rgb(hh / 360.0, ll, ss)]
            else:
                Lt = parts[0]
                L = float(Lt[:-1]) / 100.0 if Lt.endswith('%') else float(Lt)
                if L > 1.5:
                    L = L / 100.0
                Ct = parts[1]
                C = float(Ct[:-1]) / 100.0 * 0.4 if Ct.endswith('%') else float(Ct)
                H = _hue(parts[2])
                r, g, b = _oklch_to_rgb(L, C, H)
        except (ValueError, IndexError):
            return None
        clamp = lambda v: max(0.0, min(255.0, v))
        return (clamp(r), clamp(g), clamp(b), max(0.0, min(1.0, alpha)))
    if s in NAMED:
        return NAMED[s] + (1.0,)
    return None


def rgb_to_oklab(c):
    def lin(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = lin(c[0]), lin(c[1]), lin(c[2])
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s2 = (max(0.0, l) ** (1 / 3.0), max(0.0, m) ** (1 / 3.0), max(0.0, s_) ** (1 / 3.0))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s2
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s2
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s2
    return L, a, bb


def rgb_to_oklch(c):
    L, a, b = rgb_to_oklab(c)
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def delta_ok(c1, c2):
    x, y = rgb_to_oklab(c1), rgb_to_oklab(c2)
    return math.sqrt(sum((x[i] - y[i]) ** 2 for i in range(3)))


def hls_deg(c):
    h, l, s = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
    return h * 360.0, l, s


def chroma(c):
    return (max(c[:3]) - min(c[:3])) / 255.0


def is_purple(c, min_alpha=0.3):
    if c is None or c[3] < min_alpha:
        return False
    h, l, s = hls_deg(c)
    if 250 <= h <= 300 and s > 0.25 and 0.15 <= l <= 0.85 and chroma(c) >= 0.12:
        return True
    if 238 <= h < 250 and s >= 0.6 and 0.2 <= l <= 0.75 and chroma(c) >= 0.25:
        return True
    return False


def is_saturated(c, min_s=0.3):
    if c is None:
        return False
    h, l, s = hls_deg(c)
    return chroma(c) >= 0.15 and s > min_s and 0.12 <= l <= 0.9


def hue_family(c):
    if c is None or c[3] < 0.3:
        return None
    h, l, s = hls_deg(c)
    if chroma(c) < 0.2 or s < 0.3 or not (0.2 <= l <= 0.85):
        return None
    if h < 15 or h >= 345:
        return 'red'
    if h < 40:
        return 'orange'
    if h < 65:
        return 'amber'
    if h < 165:
        return 'green'
    if h < 200:
        return 'cyan'
    if h < 238:
        return 'blue'
    if h < 290:
        return 'violet'
    return 'pink'


def is_pure(c, rgb):
    return c is not None and c[3] >= 0.999 and all(abs(c[i] - rgb[i]) < 0.6 for i in range(3))


def is_offwhite(c):
    if c is None or c[3] < 0.9:
        return False
    h, l, s = hls_deg(c)
    return 0.90 <= l <= 0.985 and chroma(c) <= 0.1


GRAD_RE = re.compile(r'(?:repeating-)?(?:linear|radial|conic)-gradient\(', re.I)


def gradients_in(value):
    out = []
    for m in GRAD_RE.finditer(value):
        j = match_paren(value, m.end() - 1)
        out.append(value[m.start():j])
    return out


# --------------------------------------------------------------------------------------
# Tailwind helpers
# --------------------------------------------------------------------------------------

TW_PALETTE = ['slate', 'gray', 'zinc', 'neutral', 'stone', 'red', 'orange', 'amber', 'yellow', 'lime',
              'green', 'emerald', 'teal', 'cyan', 'sky', 'blue', 'indigo', 'violet', 'purple', 'fuchsia',
              'pink', 'rose']
TW_NEUTRAL = {'slate', 'gray', 'zinc', 'neutral', 'stone'}
TW_PURPLE = {'violet', 'purple', 'indigo', 'fuchsia'}
TW_FAMILY = {'red': 'red', 'rose': 'red', 'orange': 'orange', 'amber': 'amber', 'yellow': 'amber',
             'lime': 'green', 'green': 'green', 'emerald': 'green', 'teal': 'cyan', 'cyan': 'cyan',
             'sky': 'cyan', 'blue': 'blue', 'indigo': 'violet', 'violet': 'violet', 'purple': 'violet',
             'fuchsia': 'pink', 'pink': 'pink'}
TW_COLOR_RE = re.compile(
    r'^(bg|text|border(?:-[xytrblse])?|from|via|to|ring|fill|stroke|decoration|outline|shadow|accent|caret|divide)-('
    + '|'.join(TW_PALETTE) + r')-(50|100|200|300|400|500|600|700|800|900|950)(?:/(\[?[\d.]+%?\]?))?$')
TW_ARB_COLOR_RE = re.compile(
    r'^(bg|text|border(?:-[xytrblse])?|from|via|to|ring|fill|stroke|decoration|outline|shadow|accent)-\[(#[0-9a-fA-F]{3,8}|(?:rgba?|hsla?|oklch)\([^\]]*\))\]$')
TW_TEXT = {'xs': 12, 'sm': 14, 'base': 16, 'lg': 18, 'xl': 20, '2xl': 24, '3xl': 30, '4xl': 36, '5xl': 48,
           '6xl': 60, '7xl': 72, '8xl': 96, '9xl': 128}
TW_TRACK = {'tighter': -0.05, 'tight': -0.025, 'normal': 0.0, 'wide': 0.025, 'wider': 0.05, 'widest': 0.1}
TW_RADIUS = {'none': 0, 'xs': 2, 'sm': 2, '': 4, 'md': 6, 'lg': 8, 'xl': 12, '2xl': 16, '3xl': 24, '4xl': 32,
             'full': 9999}
TW_HINT_RE = re.compile(r'^(flex|grid|hidden|block|inline-flex|items-\w+|justify-\w+|gap-\d+|[pm][xytrbl]?-\d+|'
                        r'text-(xs|sm|base|lg|\d?xl)|font-(bold|semibold|medium)|rounded(-\w+)?|bg-\w+-\d{2,3}|'
                        r'w-\d+|h-\d+|max-w-\w+|mx-auto|space-[xy]-\d+)$')


def tw_split(cls):
    parts, cur, depth = [], [], 0
    for ch in cls:
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
        if ch == ':' and depth == 0:
            parts.append(''.join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append(''.join(cur))
    base = parts[-1].strip('!')
    return tuple(parts[:-1]), base


def tw_font_px(base):
    m = re.match(r'^text-(xs|sm|base|lg|xl|[2-9]xl)(?:/[\w.\[\]]+)?$', base)
    if m:
        return TW_TEXT[m.group(1)]
    m = re.match(r'^text-\[(\d*\.?\d+)(px|rem|em)\]$', base)
    if m:
        v = float(m.group(1))
        return v if m.group(2) == 'px' else v * 16
    return None


def tw_tracking(base):
    """Return (value, unit) or None."""
    m = re.match(r'^tracking-(tighter|tight|normal|wide|wider|widest)$', base)
    if m:
        return TW_TRACK[m.group(1)], 'em'
    m = re.match(r'^tracking-\[(-?\d*\.?\d+)(em|px|rem)\]$', base)
    if m:
        return float(m.group(1)), m.group(2)
    return None


def tw_color(base):
    """(prefix, rgba or None, palette or None, shade or None)."""
    m = TW_COLOR_RE.match(base)
    if m:
        return m.group(1), None, m.group(2), int(m.group(3))
    m = TW_ARB_COLOR_RE.match(base)
    if m:
        return m.group(1), parse_color(m.group(2).replace('_', ' ')), None, None
    return None


# --------------------------------------------------------------------------------------
# Source files, markup tree
# --------------------------------------------------------------------------------------

class TextSeg(object):
    __slots__ = ('raw', 'off', 'parent', 'clean', '_code')

    def __init__(self, raw, off, parent, jsx):
        self.raw = raw
        self.off = off
        self.parent = parent
        t = clean_jsx_text(raw) if jsx else raw
        try:
            t = htmllib.unescape(t)
        except Exception:
            pass
        self.clean = t
        self._code = None

    def in_code(self):
        if self._code is None:
            n = self.parent
            res = False
            while n is not None:
                if n.ltag in CODE_TAGS:
                    res = True
                    break
                n = n.parent
            self._code = res
        return self._code


class Node(object):
    def __init__(self, tag, attrs, start, parent, sf, jsx):
        self.tag = tag
        self.ltag = tag.lower()
        self.attrs = attrs
        self.start = start
        self.end = start
        self.parent = parent
        self.sf = sf
        self.jsx = jsx
        self.children = []
        self.raw = None
        self.is_component = bool(jsx and tag[:1].isupper()) or ('.' in tag)
        self.classes = extract_classes(attrs)
        self.class_set = set(self.classes)
        v = attrs.get('id')
        self.id = v if isinstance(v, str) and not v.startswith('{') else None
        self.inline_decls = []
        self._text = None
        self._rules = None
        self._rules_unit = None
        self._tw = None

    def tw(self):
        if self._tw is None:
            self._tw = [tw_split(c) for c in self.classes if c and '{' not in c and '}' not in c]
        return self._tw

    def elem_children(self):
        return [c for c in self.children if isinstance(c, Node)]

    def ancestors(self, limit=50):
        out = []
        n = self.parent
        while n is not None and len(out) < limit:
            if n.tag == '#root':
                break
            out.append(n)
            n = n.parent
        return out

    def descendants(self, max_depth=8):
        out = []

        def walk(n, d):
            if d > max_depth:
                return
            for c in n.children:
                if isinstance(c, Node):
                    out.append(c)
                    walk(c, d + 1)
        walk(self, 1)
        return out

    def prev_elem_sibling(self):
        if self.parent is None:
            return None
        prev = None
        for c in self.parent.children:
            if c is self:
                return prev
            if isinstance(c, Node):
                prev = c
            elif c.clean.strip():
                prev = None  # real text between: not a sibling pair
        return None

    def text(self):
        if self._text is None:
            parts = []

            def walk(n):
                for c in n.children:
                    if isinstance(c, TextSeg):
                        parts.append(c.clean)
                    elif c.ltag not in CODE_TAGS:
                        walk(c)
            walk(self)
            self._text = re.sub(r'\s+', ' ', ' '.join(parts)).strip()
        return self._text

    def ctx(self):
        return '%s %s %s' % (self.tag, ' '.join(self.classes), self.id or '')


def clean_jsx_text(s):
    s = re.sub(r'\{\s*(["\'])([^"\'{}]*)\1\s*\}', lambda m: m.group(2), s)
    out = []
    depth = 0
    for ch in s:
        if ch == '{':
            depth += 1
            continue
        if ch == '}':
            if depth == 0:
                out = []
            else:
                depth -= 1
            continue
        if depth == 0:
            out.append(ch)
    return ''.join(out)


def parse_attrs(s):
    attrs = {}
    i, n = 0, len(s)
    name_re = re.compile(r'[^\s=/>{]+')
    while i < n:
        while i < n and (s[i].isspace() or s[i] == '/'):
            i += 1
        if i >= n:
            break
        if s[i] == '{':
            i = match_brace(s, i)
            continue
        m = name_re.match(s, i)
        if not m:
            i += 1
            continue
        name = m.group(0)
        i = m.end()
        while i < n and s[i].isspace():
            i += 1
        val = True
        if i < n and s[i] == '=':
            i += 1
            while i < n and s[i].isspace():
                i += 1
            if i < n and s[i] in '"\'':
                q = s[i]
                j = s.find(q, i + 1)
                j = n if j < 0 else j
                val = s[i + 1:j]
                i = j + 1
            elif i < n and s[i] == '{':
                j = match_brace(s, i)
                val = s[i:j]
                i = j
            else:
                m2 = re.compile(r'[^\s>]+').match(s, i)
                if m2:
                    val = m2.group(0)
                    i = m2.end()
                else:
                    i += 1
        if name not in attrs:
            attrs[name] = val
    return attrs


def extract_classes(attrs):
    out = []
    for k, v in attrs.items():
        kl = k.lower()
        if kl in ('class', 'classname', ':class', 'v-bind:class', 'class:list', 'tw', '[class]', '[ngclass]'):
            if v is True:
                continue
            if kl in ('class', 'classname') and not v.lstrip().startswith('{'):
                out.extend(t for t in v.split() if '{' not in t and '}' not in t)
            else:
                for sm in re.finditer(r'(["\'`])((?:(?!\1).)*?)\1', v, re.S):
                    out.extend(re.sub(r'\$\{[^}]*\}', ' ', sm.group(2)).split())
                for sm in re.finditer(r'\bstyles?\.([A-Za-z_][\w-]*)|\bstyles?\[\s*["\']([\w-]+)["\']\s*\]', v):
                    out.append(sm.group(1) or sm.group(2))
        elif kl.startswith('class:'):
            out.append(k[6:])
    return out


_BR = r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}'
TAG_RE = re.compile(r'<(/?)([A-Za-z][\w:.\-]*)((?:"[^"]*"|\'[^\']*\'|' + _BR + r'|[^>"\'{}/]|/(?!>))*)(/?)>', re.S)


def jsx_tag_ok(t, st):
    k = st - 1
    while k >= 0 and t[k] in ' \t\r\n':
        k -= 1
    if k < 0:
        return True
    c = t[k]
    if c in '(>{}?:&|,=;[':
        return True
    if t[max(0, k - 5):k + 1] == 'return' or t[max(0, k - 4):k + 1] == 'yield':
        return True
    return False


def implicit_close(stack, tag):
    top = stack[-1]
    if top.ltag == 'p' and tag in BLOCK_TAGS:
        stack.pop()
    elif tag == 'li' and top.ltag == 'li':
        stack.pop()
    elif tag in ('dt', 'dd') and top.ltag in ('dt', 'dd'):
        stack.pop()
    elif tag == 'option' and top.ltag == 'option':
        stack.pop()
    elif tag in ('td', 'th') and top.ltag in ('td', 'th'):
        stack.pop()
    elif tag == 'tr' and top.ltag in ('tr', 'td', 'th'):
        while len(stack) > 1 and stack[-1].ltag in ('tr', 'td', 'th'):
            stack.pop()


DOC_RE = re.compile(r'<(html|head|body)\b', re.I)
STYLE_BLOCK_RE = re.compile(r'<style\b[^>]*>(.*?)</style\s*>', re.S | re.I)
SCRIPT_BLOCK_RE = re.compile(r'<script\b([^>]*)>(.*?)</script\s*>', re.S | re.I)
CSS_IN_JS_RE = re.compile(r'(?:\bcss|\bstyled\.\w+|\bstyled\([^)\n]*\)|\bcreateGlobalStyle|\bkeyframes|\binjectGlobal)\s*`([^`]*)`', re.S)
STYLE_JSX_RE = re.compile(r'<style\b[^>]*>\s*\{\s*`([^`]*)`\s*\}', re.S)
LINK_CSS_RE = re.compile(r'<link\b[^>]*\bhref=["\']([^"\']+?\.css(?:\?[^"\']*)?)["\']', re.I)


class SourceFile(object):
    def __init__(self, path, text):
        self.path = path
        self.text = text
        self.ext = os.path.splitext(path)[1].lower()
        pp = plain_path(path)
        try:
            disp = os.path.relpath(pp)
        except ValueError:
            disp = pp
        if disp.startswith('..' + os.sep + '..'):
            disp = pp
        self.display = disp.replace('\\', '/')
        self._ls = [0]
        for m in re.finditer('\n', text):
            self._ls.append(m.end())
        self.is_doc = self.ext in ('.html', '.htm') and bool(DOC_RE.search(text))
        self.nodes = []
        self.texts = []
        self.copy = []
        self.css_regions = []
        self.js_regions = []
        self.markers = OrderedDict()
        self.has_markup = False
        self._prepared = False

    def line_of(self, off):
        return max(1, bisect.bisect_right(self._ls, max(0, off)))

    def line_text(self, ln):
        if ln < 1 or ln > len(self._ls):
            return ''
        s = self._ls[ln - 1]
        e = self.text.find('\n', s)
        return self.text[s:len(self.text) if e < 0 else e]

    def snippet(self, off):
        ln = self.line_of(off)
        lt = self.line_text(ln)
        if len(lt) > 150:
            col = max(0, off - self._ls[ln - 1])
            lt = lt[max(0, col - 30):col + 110]
        return shorten(lt, 140)

    # -- preparation -------------------------------------------------------------
    def prepare(self):
        if self._prepared:
            return
        self._prepared = True
        t = self.text
        ext = self.ext
        if ext in CSS_EXTS:
            self.css_regions.append((0, len(t)))
        elif ext in MARKUP_EXTS:
            for m in STYLE_BLOCK_RE.finditer(t):
                self.css_regions.append((m.start(1), m.end(1)))
            for m in SCRIPT_BLOCK_RE.finditer(t):
                if 'json' in m.group(1).lower() and 'ld+json' not in m.group(1).lower():
                    continue
                self.js_regions.append((m.start(2), m.end(2)))
            if ext == '.astro':
                fm = re.match(r'\A\s*---(.*?)---', t, re.S)
                if fm:
                    self.js_regions.append((fm.start(1), fm.end(1)))
            self.parse_markup(jsx=False)
        elif ext in JS_EXTS:
            self.js_regions.append((0, len(t)))
            for m in CSS_IN_JS_RE.finditer(t):
                self.css_regions.append((m.start(1), m.end(1)))
            for m in STYLE_JSX_RE.finditer(t):
                self.css_regions.append((m.start(1), m.end(1)))
            if ext in JSX_EXTS or (ext in ('.js', '.mjs', '.cjs') and re.search(
                    r'return\s*\(\s*<[A-Za-z]|=>\s*\(\s*<[A-Za-z]|=>\s*<[A-Za-z]|React', t)):
                self.parse_markup(jsx=True)
        self.collect_copy()

    def parse_markup(self, jsx):
        text = self.text
        if jsx:
            t = re.sub(r'/\*.*?\*/', blank_match, text, flags=re.S)
            t = re.sub(r'(?m)^[ \t]*//[^\n]*', blank_match, t)
        else:
            t = re.sub(r'<!--.*?-->', blank_match, text, flags=re.S)
            if self.ext == '.astro':
                t = re.sub(r'\A\s*---.*?---', blank_match, t, flags=re.S)
        root = Node('#root', {}, 0, None, self, jsx)
        root.end = len(t)
        stack = [root]
        nodes = []
        pos = i = 0
        n = len(t)
        while True:
            m = TAG_RE.search(t, i)
            if not m:
                break
            closing, name, attr_s, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
            st = m.start()
            if jsx and not closing:
                if len(stack) == 1 and not jsx_tag_ok(t, st):
                    i = st + 1
                    continue
                if re.match(r'^[A-Z]{1,2}$', name) or re.match(r'^\s*(,|extends\b)', attr_s):
                    i = st + 1
                    continue
            if st > pos and (not jsx or len(stack) > 1):
                self._add_text(stack[-1], t[pos:st], pos, jsx)
            tag = name if (jsx and (name[:1].isupper() or '.' in name)) else name.lower()
            if closing:
                for k in range(len(stack) - 1, 0, -1):
                    if stack[k].tag == tag:
                        for nd in stack[k:]:
                            nd.end = st
                        del stack[k:]
                        break
                pos = i = m.end()
                continue
            attrs = parse_attrs(attr_s)
            ltag = tag.lower()
            if not jsx:
                implicit_close(stack, ltag)
            node = Node(tag, attrs, st, stack[-1], self, jsx)
            stack[-1].children.append(node)
            nodes.append(node)
            if ltag in ('script', 'style') and not selfclose:
                close = re.compile(r'</' + ltag + r'\s*>', re.I).search(t, m.end())
                node.raw = t[m.end():close.start() if close else n]
                node.end = close.end() if close else n
                pos = i = node.end
                continue
            if selfclose or ltag in VOID_TAGS:
                node.end = m.end()
                pos = i = m.end()
                continue
            stack.append(node)
            pos = i = m.end()
        if pos < n and (not jsx or len(stack) > 1):
            self._add_text(stack[-1], t[pos:], pos, jsx)
        for nd in stack[1:]:
            nd.end = n
        self.nodes = nodes
        self.has_markup = bool(nodes)
        for nd in nodes:
            st = nd.attrs.get('style')
            if isinstance(st, str):
                nd.inline_decls = parse_inline_style(st, nd)

    def _add_text(self, parent, raw, off, jsx):
        if not raw.strip():
            return
        seg = TextSeg(raw, off, parent, jsx)
        parent.children.append(seg)
        self.texts.append(seg)

    def collect_copy(self):
        for seg in self.texts:
            if seg.in_code():
                continue
            if seg.clean.strip():
                chain = [seg.parent] + seg.parent.ancestors(3)
                prominent = any(a.ltag in HEADING_TAGS or a.ltag in ('title', 'button', 'summary') for a in chain)
                self.copy.append((seg.clean, seg.raw, seg.off, 'prominent' if prominent else 'text'))
        for (a, b) in self.js_regions:
            region = self.text[a:b]
            for m in JS_STRING_RE.finditer(region):
                s = m.group(2) if m.group(2) is not None else m.group(3)
                if s is None:
                    continue
                s = re.sub(r'\$\{[^}]*\}', ' ', s)
                if is_prose(s):
                    self.copy.append((s, s, a + m.start(), 'text'))


JS_STRING_RE = re.compile(r'(?:[:=(,\[?]|\breturn|&&|\|\|)\s*(?:(["\'])((?:\\.|(?!\1)[^\\\n])*)\1|`((?:\\.|[^\\`])*)`)')


def is_prose(s):
    s = s.strip()
    if len(s) < 8 or len(s) > 700:
        return False
    if re.search(r'[{};<>]|=>|\bfunction\b|\bimport\b|https?://|^[./#@]', s):
        return False
    toks = s.split()
    if len(toks) < 3:
        return False
    alpha = [w for w in toks if re.match(r"^[\"'(]?[A-Za-z][A-Za-z'’,.!?:;)\"-]*$", w)]
    if len(alpha) < 0.6 * len(toks):
        return False
    classy = [w for w in toks if re.match(r'^[a-z0-9!-]+(-[a-z0-9\[\]./%#_]+)+$|^[a-z0-9-]+:[\w\[\]/.-]+$', w)]
    if len(classy) >= 0.4 * len(toks):
        return False
    return True


# --------------------------------------------------------------------------------------
# CSS model
# --------------------------------------------------------------------------------------

class Decl(object):
    __slots__ = ('prop', 'value', 'off', 'selector', 'media', 'sf', 'rule', 'node')

    def __init__(self, prop, value, off, selector, media, sf, rule=None, node=None):
        self.prop = prop
        self.value = value
        self.off = off
        self.selector = selector
        self.media = media
        self.sf = sf
        self.rule = rule
        self.node = node


class CssRule(object):
    def __init__(self, selector, off, sf, media, kind):
        self.selector = selector
        self.off = off
        self.sf = sf
        self.media = media
        self.kind = kind
        self.decls = []
        self.applies = []
        self.name = ''
        self._comps = None

    def comps(self):
        if self._comps is None:
            self._comps = compounds_of(self.selector)
        return self._comps


class Compound(object):
    __slots__ = ('tag', 'classes', 'ids', 'pseudo', 'state')

    def __init__(self, tag, classes, ids, pseudo, state):
        self.tag = tag
        self.classes = classes
        self.ids = ids
        self.pseudo = pseudo
        self.state = state


def compounds_of(selector):
    out = []
    for sel in split_top(selector, ','):
        sel = sel.strip()
        if not sel or sel.startswith('@'):
            continue
        parts = [p for p in re.split(r'\s*[>+~]\s*|\s+', sel) if p]
        if not parts:
            continue
        last = parts[-1]
        pseudo = bool(re.search(r'::|:(before|after|placeholder|selection|marker)\b', last))
        state = bool(re.search(r':(hover|focus|active|visited|focus-visible|focus-within|checked|disabled|target)\b', last))
        base = re.sub(r'::?[\w-]+(\((?:[^()]|\([^()]*\))*\))?', '', last)
        base = re.sub(r'\[[^\]]*\]', '', base)
        tm = re.match(r'^[a-zA-Z][\w-]*|^\*', base)
        tag = tm.group(0).lower() if tm else None
        classes = set(c.replace('\\', '') for c in re.findall(r'\.((?:\\.|[\w-])+)', base))
        ids = set(re.findall(r'#([\w-]+)', base))
        out.append(Compound(tag, classes, ids, pseudo, state))
    return out


def combine_sel(parent, child):
    if not parent:
        return child
    out = []
    for p in split_top(parent, ','):
        for c in split_top(child, ','):
            c = c.strip()
            if '&' in c:
                out.append(c.replace('&', p.strip()))
            else:
                out.append(p.strip() + ' ' + c)
            if len(out) > 40:
                return ', '.join(out)
    return ', '.join(out)


def parse_css(sf, a, b, unit):
    css = sf.text[a:b]
    css = re.sub(r'/\*.*?\*/', blank_match, css, flags=re.S)
    if sf.ext in ('.scss', '.sass', '.less'):
        css = re.sub(r'(?m)(?:^|(?<=[\s;{}]))//[^\n]*', blank_match, css)
    n = len(css)

    def read_stmt(i):
        depth = 0
        while i < n:
            c = css[i]
            if c == '"' or c == "'":
                q = c
                i += 1
                while i < n and css[i] != q and css[i] != '\n':
                    if css[i] == '\\':
                        i += 1
                    i += 1
                i += 1
                continue
            if c == '(':
                depth += 1
            elif c == ')':
                depth = max(0, depth - 1)
            elif depth == 0 and c in ';{}':
                return i, c
            i += 1
        return n, ''

    def add_decl(rule, seg, start, media):
        st = seg.strip()
        if not st or rule is None:
            return
        off = a + start + (len(seg) - len(seg.lstrip()))
        if st.startswith('@apply'):
            rule.applies.extend(st[6:].replace('!important', '').split())
            return
        if ':' not in st:
            return
        prop, val = st.split(':', 1)
        prop = prop.strip().lower()
        if not re.match(r'^-{0,2}[a-z][\w-]*$', prop):
            return
        val = val.replace('!important', '').strip()
        d = Decl(prop, val, off, rule.selector, media, sf, rule=rule)
        rule.decls.append(d)
        if prop.startswith('--'):
            unit.custom[prop].append((val, rule.selector, d))

    def block(i, sel_ctx, media, rule, in_kf):
        while i < n:
            start = i
            j, t = read_stmt(i)
            seg = css[start:j]
            if t == '{':
                prelude = seg.strip()
                p_off = a + start + (len(seg) - len(seg.lstrip()))
                if in_kf is not None:
                    i = block(j + 1, sel_ctx, media, in_kf, in_kf)
                    continue
                if prelude.startswith('@'):
                    mm = re.match(r'@([\w-]+)\s*(.*)$', prelude, re.S)
                    name = mm.group(1).lower() if mm else ''
                    rest = mm.group(2).strip() if mm else ''
                    if name.endswith('keyframes'):
                        k = CssRule('@keyframes ' + rest, p_off, sf, media, 'keyframes')
                        k.name = rest
                        unit.keyframes.append(k)
                        i = block(j + 1, sel_ctx, media, k, k)
                        continue
                    if name == 'font-face':
                        r = CssRule('@font-face', p_off, sf, media, 'font-face')
                        unit.fontfaces.append(r)
                        i = block(j + 1, sel_ctx, media, r, None)
                        continue
                    if name in ('media', 'supports', 'layer', 'container', 'document', 'scope', 'starting-style'):
                        i = block(j + 1, sel_ctx, media + [prelude], rule, None)
                        continue
                    selector = ':root' if name == 'theme' else prelude
                    r = CssRule(selector, p_off, sf, media, 'rule')
                    unit.rules.append(r)
                    i = block(j + 1, selector, media, r, None)
                    continue
                selector = combine_sel(sel_ctx, prelude)
                r = CssRule(selector, p_off, sf, media, 'rule')
                unit.rules.append(r)
                i = block(j + 1, selector, media, r, None)
                continue
            add_decl(rule, seg, start, media)
            if t == '}':
                return j + 1
            if t == '':
                return n
            i = j + 1
        return n

    i = 0
    while i < n:
        i = block(i, None, [], None, None)


def parse_inline_style(val, node):
    out = []
    sf = node.sf
    sel = '[inline] ' + node.ctx()
    if val.lstrip().startswith('{'):
        for m in re.finditer(r'([A-Za-z]+|"[^"]+"|\'[^\']+\')\s*:\s*(?:(["\'`])((?:(?!\2).)*)\2|(-?\d*\.?\d+))', val):
            prop = m.group(1).strip('"\'')
            prop = re.sub(r'([A-Z])', lambda mm: '-' + mm.group(1).lower(), prop)
            if prop.startswith(('webkit-', 'moz-', 'ms-')):
                prop = '-' + prop
            v = m.group(3) if m.group(3) is not None else m.group(4)
            if m.group(4) is not None and prop in ('font-size', 'letter-spacing', 'border-radius', 'width', 'height'):
                v = v + 'px'
            out.append(Decl(prop, v, node.start, sel, [], sf, node=node))
    else:
        for part in split_top(val, ';'):
            if ':' in part:
                p, v = part.split(':', 1)
                p = p.strip().lower()
                if re.match(r'^-{0,2}[a-z][\w-]*$', p):
                    out.append(Decl(p, v.strip(), node.start, sel, [], sf, node=node))
    return out


# --------------------------------------------------------------------------------------
# Units (one page or one app)
# --------------------------------------------------------------------------------------

VAR_RE = re.compile(r'var\(\s*(--[\w-]+)\s*(?:,\s*((?:[^()]|\((?:[^()]|\([^()]*\))*\))*))?\)')


class Unit(object):
    def __init__(self, name):
        self.name = name
        self.files = []
        self.rules = []
        self.keyframes = []
        self.fontfaces = []
        self.custom = defaultdict(list)
        self.nodes = []
        self.extra_loaded_fonts = []
        self.tailwind = False

    def add(self, sf):
        if sf not in self.files:
            self.files.append(sf)

    def prepare(self):
        for sf in self.files:
            sf.prepare()
            for (a, b) in sf.css_regions:
                parse_css(sf, a, b, self)
            self.nodes.extend(sf.nodes)
        for nd in self.nodes:
            for d in nd.inline_decls:
                if d.prop.startswith('--'):
                    self.custom[d.prop].append((d.value, d.selector, d))
        for name in list(self.custom):
            vals = self.custom[name]
            vals.sort(key=lambda v: 0 if re.search(r':root|^html|@theme|^\s*$', v[1] or '') else 1)
        self.build_index()
        self.tailwind = self._detect_tailwind()

    def _detect_tailwind(self):
        for sf in self.files:
            if re.search(r'cdn\.tailwindcss\.com|@tailwind\b|@import\s+["\']tailwindcss|tailwind\.config|'
                         r'from\s+["\']tailwindcss', sf.text):
                return True
            if os.path.basename(sf.path).startswith('tailwind.config'):
                return True
        hits = set()
        for nd in self.nodes:
            for v, b in nd.tw():
                if TW_HINT_RE.match(b):
                    hits.add(b)
        return len(hits) >= 12

    def build_index(self):
        self.idx_class = defaultdict(list)
        self.idx_tag = defaultdict(list)
        self.idx_id = defaultdict(list)
        for r in self.rules:
            if r.kind != 'rule':
                continue
            for c in r.comps():
                if c.pseudo or c.state:
                    continue
                if c.ids:
                    self.idx_id[sorted(c.ids)[0]].append((r, c))
                elif c.classes:
                    self.idx_class[sorted(c.classes)[0]].append((r, c))
                elif c.tag and c.tag != '*':
                    self.idx_tag[c.tag].append((r, c))

    def rules_for(self, node):
        if node._rules_unit is self:
            return node._rules
        cands = []
        if node.id:
            cands += self.idx_id.get(node.id, [])
        for cl in node.class_set:
            cands += self.idx_class.get(cl, [])
        cands += self.idx_tag.get(node.ltag, [])
        seen = set()
        out = []
        for r, c in cands:
            if id(r) in seen:
                continue
            if c.tag and c.tag != '*' and c.tag != node.ltag:
                continue
            if not c.classes.issubset(node.class_set):
                continue
            if c.ids and node.id not in c.ids:
                continue
            seen.add(id(r))
            out.append(r)
        out.sort(key=lambda r: (r.sf.path, r.off))
        node._rules = out
        node._rules_unit = self
        return out

    def decls_for(self, node, rules_only=False):
        out = []
        for r in self.rules_for(node):
            out.extend(r.decls)
        if not rules_only:
            out.extend(node.inline_decls)
        return out

    def last_decl(self, node, *props):
        v = None
        for d in self.decls_for(node):
            if d.prop in props:
                v = d
        return v

    def tw(self, node):
        """(variants, base) list incl. @apply'd classes of matched rules."""
        res = list(node.tw())
        for r in self.rules_for(node):
            for c in r.applies:
                res.append(tw_split(c))
        return res

    def tw_bases(self, node, unprefixed=True):
        return set(b for v, b in self.tw(node) if not unprefixed or not v)

    def all_decls(self):
        for r in self.rules:
            for d in r.decls:
                yield d
        for nd in self.nodes:
            for d in nd.inline_decls:
                yield d

    def resolve(self, value, depth=0):
        if 'var(' not in value or depth > 6:
            return value

        def rep(m):
            vals = self.custom.get(m.group(1))
            if vals:
                return self.resolve(vals[0][0], depth + 1)
            if m.group(2) is not None:
                return self.resolve(m.group(2), depth + 1)
            return m.group(0)
        return VAR_RE.sub(rep, value)

    def colors(self, value):
        v = self.resolve(value)
        c = parse_color(v) if BARE_HSL_RE.match(v) else None
        if c:
            return [c]
        out = []
        for m in COLOR_RE.finditer(v):
            c = parse_color(m.group(0))
            if c is not None:
                out.append(c)
        return out

    def markup_files(self):
        return [sf for sf in self.files if sf.has_markup]


# --------------------------------------------------------------------------------------
# Findings
# --------------------------------------------------------------------------------------

class Findings(object):
    def __init__(self):
        self.items = OrderedDict()

    def add(self, rid, sf, off, msg, severity=None, unit_files=None):
        """severity overrides the weight-derived level (used for uncertain pooled findings); unit_files lists the
        files a pooled finding was derived from, so an ignore directive in any of them silences it."""
        r = RULES[rid]
        line = sf.line_of(off) if off is not None else 1
        k = (rid, sf.display, line)
        if k in self.items:
            prev = self.items[k]
            if msg and msg not in prev['message'] and prev['message'].count('; ') < 2:
                prev['message'] += '; ' + msg
            return
        self.items[k] = {
            'rule': rid, 'key': r['key'], 'weight': r['weight'], 'tag': r['label'],
            'severity': severity or rule_severity(r),
            'file': sf.display, 'line': line,
            'snippet': sf.snippet(off if off is not None else 0),
            'message': msg, 'fix': r['fix'],
            'unit_files': list(unit_files or ()),
        }

    def results(self, cap=5):
        items = list(self.items.values())
        if cap:
            groups = defaultdict(list)
            for it in items:
                groups[(it['rule'], it['file'])].append(it)
            keep = []
            for g in groups.values():
                g.sort(key=lambda x: x['line'])
                kept = g[:cap]
                if len(g) > cap:
                    kept[-1] = dict(kept[-1])
                    kept[-1]['message'] += ' (+%d more like this in this file)' % (len(g) - cap)
                keep.extend(kept)
            items = keep
        items.sort(key=lambda x: (SEV_ORDER[x['severity']], -x['weight'], x['file'], x['line'], x['rule']))
        return items


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------

EMOJI_RE = re.compile('[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F7E0-\U0001F7FF'
                      '\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF☀-☄☇-⛿✀-➿'
                      '⭐⭕⌚⌛⏩-⏳⏸-⏺]')


def emoji_only(s):
    if not EMOJI_RE.search(s):
        return False
    rest = EMOJI_RE.sub('', s)
    rest = re.sub('[️‍\U0001F3FB-\U0001F3FF]', '', rest)
    rest = re.sub(r'\s', '', rest)
    return rest == ''


# ---- fonts ----------------------------------------------------------------------------

GENERIC_FAMILIES = {'serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'ui-sans-serif',
                    'ui-serif', 'ui-monospace', 'ui-rounded', 'emoji', 'math', 'fangsong', '-apple-system',
                    'blinkmacsystemfont', 'apple color emoji', 'segoe ui emoji', 'segoe ui symbol',
                    'noto color emoji'}
# Helvetica / Helvetica Neue are deliberately absent: the [13] cluster does not list them and typography.0.7 [4]
# recommends Helvetica among the structurally classic faces.
DEFAULT_FONTS = {'inter', 'roboto', 'arial', 'open sans', 'lato',
                 'times new roman', 'times', 'system-ui', '-apple-system', 'blinkmacsystemfont', 'segoe ui',
                 'ui-sans-serif', 'sans-serif', 'serif', 'arial black', 'ui-serif'}
MONO_RE = re.compile(r'mono|courier|consolas|menlo|monaco|fira code|source code|jetbrains|iosevka|inconsolata|'
                     r'cascadia|ui-monospace|^monospace$|sf mono|lucida console', re.I)
AI_FAVES = ['space grotesk', 'instrument serif', 'instrument sans', 'fraunces', 'geist', 'syne',
            'bricolage grotesque', 'sora', 'young serif', 'plus jakarta sans', 'dm sans', 'dm serif display',
            'dm serif text', 'outfit', 'playfair display', 'playfair', 'cormorant garamond', 'cormorant', 'lora',
            'crimson pro', 'crimson text', 'newsreader', 'recoleta', 'ibm plex sans', 'ibm plex serif']
# The faces a01 (Anthropic cookbook "Startup" list) and a05 (Taste Skill) recommend as Inter replacements: the next
# rotation once agents follow those lists.
NEXT_ROTATION = ['satoshi', 'clash display', 'clash grotesk', 'cabinet grotesk', 'geist display']
APPLE_FONT_RE = re.compile(r'\bsf[ _-]?pro\b|\bsfpro|\bsf[ _-]?compact\b|\bnew[ _-]?york\b|\bsf[ _-]?symbols?\b|'
                           r'\bsf[ _-]?mono\b|\bsan[ _-]?francisco\b', re.I)
ICON_FONT_RE = re.compile(r'awesome|icons?\b|material symbols|glyph|fontello|icomoon|codicon|dashicons|feather|'
                          r'phosphor|remixicon|boxicons|ionicons', re.I)
FONT_SIZE_KW =r'(?:\d*\.?\d+(?:px|rem|em|%|pt|vw|vh|ch)|xx-small|x-small|small|medium|large|x-large|xx-large|smaller|larger)'


def is_default_font(f):
    return f in DEFAULT_FONTS or f.startswith('inter ') or f.startswith('roboto')


def family_list(value):
    out = []
    for tok in split_top(value, ','):
        tok = tok.strip().strip('"\'').strip()
        if tok:
            out.append(tok)
    return out


def first_family(value, unit):
    v = unit.resolve(value).strip()
    if not v or v.lower() in ('inherit', 'initial', 'unset', 'revert', 'none'):
        return None
    fams = family_list(v)
    if not fams:
        return None
    f = fams[0]
    if f.lower().startswith('var('):
        return '?var'
    return re.sub(r'\s+', ' ', f.lower())


def font_shorthand_family(value):
    m = re.search(r'(?:^|\s)' + FONT_SIZE_KW + r'(?:\s*/\s*[\w.%-]+)?\s+(.+)$', value.strip())
    return m.group(1) if m else None


def gather_fonts(u, group_loaded):
    """Return list of (family, kind, sf, off, ctx)."""
    uses = []
    for d in u.all_decls():
        ctx = d.selector or ''
        if d.prop == 'font-family':
            f = first_family(d.value, u)
            if f:
                uses.append((f, 'used', d.sf, d.off, ctx))
        elif d.prop == 'font':
            fam = font_shorthand_family(u.resolve(d.value))
            if fam:
                f = first_family(fam, u)
                if f:
                    uses.append((f, 'used', d.sf, d.off, ctx))
        elif d.prop.startswith('--') and 'font' in d.prop and not re.search(
                r'size|weight|feature|variation|optical|style|stretch|smooth|synthesis|leading|tracking|'
                r'line|spacing|scale|display-swap', d.prop):
            v = d.value
            if re.search(r'[A-Za-z]', v) and not re.match(r'^\s*-?[\d.]+', v):
                f = first_family(v, u)
                if f and f != '?var':
                    uses.append((f, 'used', d.sf, d.off, d.prop))
    for r in u.fontfaces:
        for d in r.decls:
            if d.prop == 'font-family':
                f = d.value.strip().strip('"\'').lower()
                if f:
                    uses.append((f, 'loaded', d.sf, d.off, '@font-face'))
    for sf in u.files:
        uses.extend(loaded_fonts_in(sf))
        # Tailwind fontFamily config (tailwind.config.* or inline CDN config)
        for m in re.finditer(r'fontFamily\s*:\s*\{', sf.text):
            j = match_brace(sf.text, m.end() - 1)
            body = sf.text[m.end():j]
            for km in re.finditer(r'(["\']?)([\w-]+)\1\s*:\s*\[([^\]]*)\]', body):
                items = re.findall(r'["\']([^"\']+)["\']', km.group(3))
                if items:
                    f = items[0].strip().lower()
                    if f.startswith('var('):
                        continue
                    uses.append((f, 'used', sf, m.end() + km.start(), 'tailwind fontFamily.' + km.group(2)))
    uses.extend(group_loaded)
    return uses


def loaded_fonts_in(sf):
    out = []
    t = sf.text
    for m in re.finditer(r'fonts\.(?:googleapis|bunny)\.(?:com|net)/css2?\?([^"\'\s)>]+)', t):
        q = htmllib.unescape(m.group(1))
        for fm in re.finditer(r'family=([^&]+)', q):
            for fam in fm.group(1).split('|'):
                name = re.split(r'[:@]', fam)[0].replace('+', ' ').replace('%20', ' ').strip().lower()
                if name:
                    out.append((name, 'loaded', sf, m.start(), 'font link'))
    for m in re.finditer(r'api\.fontshare\.com/v2/css\?([^"\'\s)>]+)', t):
        for fm in re.finditer(r'f\[\]=([\w-]+)', m.group(1)):
            out.append((fm.group(1).replace('-', ' ').lower(), 'loaded', sf, m.start(), 'fontshare'))
    for m in re.finditer(r'import\s*\{([^}]*)\}\s*from\s*["\']next/font/google["\']', t):
        for name in re.findall(r'\b([A-Z][A-Za-z0-9_]*)\b', m.group(1)):
            out.append((name.replace('_', ' ').lower(), 'loaded', sf, m.start(), 'next/font'))
    for m in re.finditer(r'from\s*["\']next/font/local["\']|localFont\s*\(', t):
        out.append(('(local font)', 'loaded', sf, m.start(), 'next/font/local'))
    for m in re.finditer(r'["\']@fontsource(?:-variable)?/([\w-]+)', t):
        out.append((m.group(1).replace('-', ' ').lower(), 'loaded', sf, m.start(), 'fontsource'))
    return out


def check_fonts(u, out, group_loaded, unit_files=None):
    uses = gather_fonts(u, group_loaded)
    has_unknown = any(f == '?var' for f, k, s, o, c in uses)
    real = [x for x in uses if x[0] != '?var' and not ICON_FONT_RE.search(x[0])]
    nonmono = [x for x in real if not MONO_RE.search(x[0]) and x[0] not in ('monospace', 'ui-monospace')]
    fams = OrderedDict()
    for x in nonmono:
        fams.setdefault(x[0], x)
    has_styling = any(r.decls for r in u.rules) or any(n.inline_decls for n in u.nodes) or u.tailwind
    markup = u.markup_files()
    # "nothing declared" is only knowable when the unit owns the page root (html/body or a root stylesheet);
    # a folder of components usually inherits its font from a layout outside the scan.
    has_root = any(n.ltag in ('html', 'body') for n in u.nodes) or any(
        c.tag in ('html', 'body') or ':root' in r.selector for r in u.rules if r.kind == 'rule' for c in r.comps())
    # Self-hosted Apple system fonts (licensed for Apple-platform UI only).
    for r in u.fontfaces:
        txt = ' '.join(d.value for d in r.decls if d.prop in ('font-family', 'src'))
        if APPLE_FONT_RE.search(txt):
            d0 = r.decls[0] if r.decls else None
            out.add('apple-font-on-web', d0.sf if d0 else u.files[0], d0.off if d0 else 0,
                    '@font-face embeds an Apple system face (%s)' % shorten(txt, 60))
    # Product UI, dashboards and native-feeling tools may run on one neutral sans (typography context rule 1).
    named = [f for f in fams if f not in GENERIC_FAMILIES and f not in ('sans-serif', 'serif', 'system-ui')]
    tool_ok = SURFACE == 'native' or (tool_surface() and len(named) <= 1)
    if tool_ok:
        pass
    elif not fams:
        if has_unknown or not markup or not has_styling or not has_root:
            pass
        else:
            sf = markup[0]
            anchor = None
            for n in sf.nodes:
                if n.ltag in ('body', 'html') or 'font-sans' in n.class_set:
                    anchor = n
                    break
            off = anchor.start if anchor else (sf.nodes[0].start if sf.nodes else 0)
            if u.tailwind:
                msg = 'no typeface chosen: Tailwind default font-sans (ui-sans-serif, system-ui) is the only voice'
            else:
                msg = 'no font-family anywhere: the page renders in the browser default (Times New Roman / system)'
            out.add('default-font-only', sf, off, msg, unit_files=unit_files)
    elif all(is_default_font(f) for f in fams) and not (has_unknown and not any(k == 'loaded' for f, k, s, o, c in real)):
        first = None
        for x in nonmono:
            if re.search(r'\b(body|html|h1|h2|:root)\b|font|heading|display', x[4] or ''):
                first = x
                break
        first = first or nonmono[0]
        out.add('default-font-only', first[2], first[3],
                'only default faces in use (%s); nothing gives the brand a typographic voice'
                % ', '.join(list(fams)[:5]), unit_files=unit_files)
    # AI favourites, and the next rotation that the anti-slop lists themselves recommend
    seen = set()
    for f, kind, sf, off, ctx in real:
        if 'mono' in f or f in seen:
            continue
        for fav in NEXT_ROTATION:
            if f == fav or f.startswith(fav + ' '):
                seen.add(f)
                out.add('ai-favourite-font', sf, off,
                        '"%s" is an a01/a05 Inter replacement, i.e. the next rotation; keep it only with a written '
                        'reason in DESIGN.md' % f)
                break
        if f in seen:
            continue
        for fav in AI_FAVES:
            if f == fav or f.startswith(fav + ' '):
                seen.add(f)
                out.add('ai-favourite-font', sf, off,
                        '"%s" is on the current LLM-favourite list (tension: one source still recommends Geist/'
                        'Outfit over Inter)' % f)
                break
    # Too many typefaces
    distinct = OrderedDict()
    for f, kind, sf, off, ctx in real:
        if f in GENERIC_FAMILIES or f in ('(local font)',) or f in ('system-ui', 'sans-serif', 'serif'):
            continue
        distinct.setdefault(f, (sf, off))
    if len(distinct) >= 4:
        names = list(distinct)
        sf, off = distinct[names[3]]
        out.add('too-many-typefaces', sf, off, '%d typefaces: %s' % (len(names), ', '.join(names[:6])))
    return fams


# ---- purple, gradient text --------------------------------------------------------------

CTA_CTX_RE = re.compile(r'(^|[\s._-])(btn|button|cta|primary|pill|badge|chip|tag|active|selected|current|tab-active)'
                        r'($|[\s._:-])', re.I)
BRAND_TOKEN_RE = re.compile(r'^--(?:color-)?(?:primary|accent|brand|cta|action)(?:-(?:500|600|default|base|color))?$')


def is_cta_node(u, n):
    if n.ltag == 'button' or (n.ltag == 'input' and str(n.attrs.get('type', '')).lower() in ('submit', 'button')):
        return True
    if n.attrs.get('role') == 'button':
        return True
    if n.is_component and re.search(r'button|btn|cta|badge|pill|chip', n.tag, re.I):
        return True
    if CTA_CTX_RE.search(' '.join(n.classes)):
        return True
    if any(n.attrs.get(a) for a in ('aria-selected', 'aria-current', 'aria-pressed')):
        return True
    return False


def check_purple(u, out):
    for d in u.all_decls():
        v = d.value
        lv = v.lower()
        if 'gradient(' in lv or ('var(' in lv and d.prop in ('background', 'background-image')):
            rv = u.resolve(v)
            for g in gradients_in(rv):
                cols = [parse_color(m.group(0)) for m in COLOR_RE.finditer(g)]
                if any(is_purple(c, 0.3) for c in cols if c):
                    out.add('purple-ai-colour', d.sf, d.off, 'purple/violet stop in a gradient: ' + shorten(g, 80))
                    break
        if d.prop in ('background', 'background-color') and 'gradient(' not in u.resolve(v).lower():
            ctx = d.selector or ''
            if d.node is not None:
                ctx += ' ' + d.node.ctx()
            if CTA_CTX_RE.search(ctx) or (d.node is not None and is_cta_node(u, d.node)):
                cols = u.colors(v)
                if cols and is_purple(cols[0], 0.5):
                    out.add('purple-ai-colour', d.sf, d.off, 'violet/indigo solid fill on a CTA, pill or badge (%s)'
                            % shorten(d.selector, 50))
        if d.prop.startswith('--') and BRAND_TOKEN_RE.match(d.prop):
            cols = u.colors(v)
            if cols and is_purple(cols[0], 0.5):
                out.add('purple-ai-colour', d.sf, d.off, 'brand token %s is purple/violet' % d.prop)
    for n in u.nodes:
        allb = [b for v, b in u.tw(n)]
        stops = []
        fills = []
        for b in allb:
            c = tw_color(b)
            if not c:
                continue
            prefix, rgba, pal, shade = c
            purple = (pal in TW_PURPLE) if pal else is_purple(rgba, 0.3)
            if not purple:
                continue
            if prefix in ('from', 'via', 'to') and (shade is None or shade >= 300):
                stops.append(b)
            elif prefix == 'bg' and (shade is None or shade >= 400):
                fills.append(b)
        if stops:
            out.add('purple-ai-colour', n.sf, n.start, 'Tailwind gradient stops ' + ', '.join(sorted(set(stops))[:4]))
        elif fills and is_cta_node(u, n):
            out.add('purple-ai-colour', n.sf, n.start, 'violet/indigo fill on a CTA/badge: ' + ', '.join(sorted(set(fills))[:3]))
    for sf in u.files:
        if sf.ext not in JS_EXTS and sf.ext not in MARKUP_EXTS:
            continue
        for m in re.finditer(r'\b(primary|brand|accent|cta)\s*:\s*["\'](#[0-9a-fA-F]{3,8}|(?:rgb|hsl|oklch)a?\([^"\']*\))["\']', sf.text):
            if is_purple(parse_color(m.group(2)), 0.5):
                out.add('purple-ai-colour', sf, m.start(), 'theme colour "%s" is purple/violet (%s)' % (m.group(1), m.group(2)))


def check_gradient_text(u, out):
    seen = set()
    for d in u.all_decls():
        if d.prop in ('background-clip', '-webkit-background-clip') and re.search(r'\btext\b', d.value):
            key = id(d.rule) if d.rule is not None else id(d.node)
            if key in seen:
                continue
            seen.add(key)
            out.add('gradient-text', d.sf, d.off, 'gradient-filled text via background-clip: text (%s)'
                    % shorten(d.selector, 40))
    for n in u.nodes:
        if any(b == 'bg-clip-text' for v, b in n.tw()):
            out.add('gradient-text', n.sf, n.start, 'gradient-filled text (bg-clip-text) on <%s> "%s"'
                    % (n.tag, shorten(n.text(), 40)))


# ---- emoji ------------------------------------------------------------------------------

ICONISH_CLASS_RE = re.compile(r'icon|badge|pill|chip|(^|-)tab|btn|button|nav|menu|sidebar|feature|tile|card-title',
                              re.I)
EMOJI_CTX_TAGS = HEADING_TAGS | {'button', 'nav', 'summary', 'label', 'th', 'option', 'select', 'menu', 'a',
                                 'legend', 'dt'}


def check_emoji(u, out):
    for sf in u.files:
        for seg in sf.texts:
            if seg.in_code() or not EMOJI_RE.search(seg.clean):
                continue
            p = seg.parent
            chain = [p] + p.ancestors(6)
            reason = None
            if emoji_only(seg.clean) and p.tag != '#root':
                reason = 'emoji used as an icon in <%s>' % p.tag
            else:
                for a in chain[:5]:
                    if a.ltag in EMOJI_CTX_TAGS:
                        reason = 'emoji inside <%s>' % a.ltag
                        break
                if not reason:
                    lis = [a for a in chain[:3] if a.ltag == 'li']
                    if lis and any(a.ltag in ('nav', 'aside', 'menu') or ICONISH_CLASS_RE.search(' '.join(a.classes))
                                   for a in chain):
                        reason = 'emoji in a navigation list item'
                if not reason:
                    for a in chain[:3]:
                        if ICONISH_CLASS_RE.search(' '.join(a.classes)):
                            reason = 'emoji in .%s' % next(c for c in a.classes if ICONISH_CLASS_RE.search(c))
                            break
            if reason:
                em = EMOJI_RE.search(seg.raw)
                off = seg.off + (em.start() if em else 0)
                out.add('emoji-icon', sf, off, reason + ': "%s"' % shorten(seg.clean, 40))
        for (a, b) in sf.js_regions:
            for m in re.finditer(r'\b(icon|emoji|symbol|glyph)\s*:\s*["\'`]([^"\'`\n]{1,12})["\'`]', sf.text[a:b]):
                if EMOJI_RE.search(m.group(2)):
                    out.add('emoji-icon', sf, a + m.start(), 'emoji as %s in data: %s' % (m.group(1), m.group(2).strip()))


# ---- eyebrow / pill ----------------------------------------------------------------------

EYEBROW_CLASS_RE = re.compile(r'(^|[-_])(pill|badge|eyebrow|chip|kicker|overline|tag|label|announcement|pretitle|'
                              r'preheading|tagline|supertitle|lozenge)s?($|[-_])', re.I)
EYEBROW_TEXT_RE = re.compile(r'^\W{0,3}(new\b|now\b|introducing\b|announcing\b|meet\b|powered by\b|'
                             r'just (launched|shipped|released)\b|beta\b|v\d|backed by\b)', re.I)


PILL_CLASS_RE = re.compile(r'(^|[-_])(pill|badge|chip|lozenge|announcement)s?($|[-_])', re.I)


def eyebrow_signal(u, n):
    """Return (kind, reason): kind 'pill' | 'launch' | 'label', or None."""
    t = n.text()
    if EYEBROW_TEXT_RE.search(t) or (t and EMOJI_RE.match(t)):
        return 'launch', 'launch label'
    nodes = [n] + n.descendants(2)
    for x in nodes:
        for c in x.classes:
            if PILL_CLASS_RE.search(tw_split(c)[1]):
                return 'pill', 'class "%s"' % c
        if x.is_component and re.search(r'badge|pill|chip', x.tag, re.I):
            return 'pill', '<%s>' % x.tag
    bases = set()
    for x in nodes:
        bases |= u.tw_bases(x)
    if 'rounded-full' in bases and any(b.startswith(('border', 'bg-')) for b in bases) and \
            any(re.match(r'^(text-(xs|sm|\[\d+px\])|px-[1-4](\.5)?|py-(0\.5|1|1\.5))$', b) for b in bases):
        return 'pill', 'Tailwind pill (rounded-full + border/bg + small text)'
    for x in nodes:
        decls = u.decls_for(x)
        rad = [d for d in decls if d.prop == 'border-radius']
        if rad and rad[-1].value.split():
            px = parse_len_px(rad[-1].value.split()[0])
            if (('%' in rad[-1].value and '50' in rad[-1].value) or (px is not None and px >= 100)) and \
                    any(d.prop.startswith(('border', 'background')) and d.prop != 'border-radius' for d in decls):
                return 'pill', 'CSS pill (999px radius + border/background)'
    for x in nodes:
        for c in x.classes:
            if EYEBROW_CLASS_RE.search(tw_split(c)[1]):
                return 'label', 'class "%s"' % c
        if x.is_component and re.search(r'eyebrow|tag|kicker', x.tag, re.I):
            return 'label', '<%s>' % x.tag
    if 'uppercase' in bases and any(b.startswith('tracking-') for b in bases):
        return 'label', 'uppercase tracked label'
    if 'font-mono' in bases and any(re.match(r'^text-(xs|\[\d+px\])$', b) for b in bases):
        return 'label', 'tiny mono label'
    for x in nodes:
        decls = u.decls_for(x)
        tt = any(d.prop == 'text-transform' and 'uppercase' in d.value for d in decls)
        ls = any(d.prop == 'letter-spacing' and re.match(r'^\s*0?\.\d|^\s*[1-9]', d.value) for d in decls)
        if tt and ls:
            return 'label', 'CSS uppercase + letter-spacing'
    return None


DATE_RE = re.compile(r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|'
                     r'sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b|\b(?:19|20)\d{2}\b|'
                     r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b', re.I)
NAME_STOP = {'the', 'and', 'for', 'with', 'your', 'our', 'from', 'that', 'this', 'new', 'now', 'all', 'how',
             'what', 'who', 'why', 'into', 'are', 'you', 'its', 'not'}


def brand_words(sf):
    """Distinctive words of the page's own name: the <title>, or a logo/wordmark/brand element."""
    words = set()
    for n in sf.nodes:
        if n.ltag == 'title' or (n.ltag in ('a', 'span', 'div', 'p', 'strong') and any(
                re.search(r'logo|wordmark|brand', c, re.I) for c in n.classes)):
            for w in re.findall(r'[A-Za-z][A-Za-z0-9]{2,}|\b\d+\b', n.text()):
                if w.lower() not in NAME_STOP:
                    words.add(w.lower())
    return words


def names_product_or_date(sf, text, cache):
    """The [7] rule's own exception: an eyebrow that carries the product name or a date the headline lacks."""
    if DATE_RE.search(text):
        return True
    if 'brand' not in cache:
        cache['brand'] = brand_words(sf)
    toks = set(w.lower() for w in re.findall(r'[A-Za-z][A-Za-z0-9]{2,}|\b\d+\b', text))
    return bool(toks & cache['brand'])


def check_eyebrow(u, out):
    """Pills, launch labels and anything above the h1 always count. Plain eyebrow labels above h2s are
    tolerated up to one per three sections (the research's ceiling)."""
    for sf in u.markup_files():
        found = []
        n_heads = 0
        name_cache = {}
        for h in sf.nodes:
            if h.ltag not in ('h1', 'h2'):
                continue
            n_heads += 1
            prev = h.prev_elem_sibling()
            if prev is None or prev.ltag in HEADING_TAGS or prev.ltag in ('img', 'svg', 'picture', 'video', 'nav',
                                                                        'ul', 'ol', 'form', 'br', 'hr', 'figure',
                                                                        'header', 'section', 'table'):
                continue
            t = prev.text()
            if not t or len(t) > 60 or len(t.split()) > 9:
                continue
            sig = eyebrow_signal(u, prev)
            if sig and tool_surface() and sig[0] in ('pill', 'launch') and len(t.split()) <= 2:
                continue  # product UI: a "Beta" / "New" status badge beside a page title is information
            if sig and sig[0] == 'label' and h.ltag == 'h1' and names_product_or_date(sf, t, name_cache):
                continue  # a plain label naming the product or a date above the H1 carries information
            if sig:
                found.append((h, prev, sig[0], sig[1], t))
        labels = [x for x in found if x[2] == 'label' and x[0].ltag != 'h1']
        over = len(labels) > n_heads // 3
        for h, prev, kind, why, t in found:
            if kind == 'label' and h.ltag != 'h1' and not over:
                continue
            extra = '' if kind != 'label' or h.ltag == 'h1' else ' (eyebrows: %d, headed sections: %d; ceiling 1 per 3)' % (
                len(labels), n_heads)
            out.add('eyebrow-pill', sf, prev.start, 'eyebrow above <%s> (%s): "%s"%s' % (h.ltag, why, shorten(t, 40), extra))
            sf.markers.setdefault('pill badge above a heading', prev.start)


# ---- numbering ------------------------------------------------------------------------

ZP_RE = re.compile(r'^(?:(?:step|phase|section|part|stage|chapter|no\.?)\s*)?0{1,2}([1-9])(?:\s*(?:[./)|\-–—·]|$)|\s|$)', re.I)
STEP_RE = re.compile(r'^(?:step|phase|stage)\s+([1-9])\b', re.I)


def _runs(seq):
    """Offsets where a 1 -> 2 -> 3 run starts (other numbers in between are ignored)."""
    hits = []
    expect, start = 0, None
    for v, off in seq:
        if v == 1:
            expect, start = 2, off
        elif expect and v == expect:
            expect += 1
            if expect == 4:
                hits.append(start)
    return hits


def check_numbering(u, out):
    for sf in u.files:
        seq = []
        for seg in sf.texts:
            if seg.in_code():
                continue
            s = seg.clean.strip()
            if not s or len(s) > 60:
                continue
            if any(a.ltag in ('td', 'th', 'table', 'option', 'select', 'time', 'tbody') for a in [seg.parent] + seg.parent.ancestors(3)):
                continue  # dates, calendars and data tables are real numbers, not section numbering
            m = ZP_RE.match(s) or STEP_RE.match(s)
            if m:
                seq.append((int(m.group(1)), seg.off + max(0, seg.raw.find(s[:3]))))
        hits = _runs(seq)
        for (a, b) in sf.js_regions:
            dseq = [(int(m.group(2)), a + m.start()) for m in re.finditer(
                r'\b(step|number|num|no|index|label|n|count|kicker|eyebrow)\s*:\s*["\'`]0([1-9])["\'`]', sf.text[a:b])]
            hits += _runs(dseq)
        for off in hits[:1]:
            out.add('numbered-sections', sf, off, 'sections/steps numbered 01 / 02 / 03')
            sf.markers.setdefault('numbered steps', off)


# ---- glass ------------------------------------------------------------------------------

GLASS_EXEMPT_RE = re.compile(r'nav|header|toolbar|topbar|appbar|tabbar|tab-bar|sticky|fixed|menu|dropdown|modal|'
                             r'overlay|dialog|sheet|drawer|popover|tooltip|backdrop|lightbox|command|palette', re.I)
GLASS_CARD_RE = re.compile(r'card|glass|panel|tile|feature|pricing|plan|testimonial|frost', re.I)


def check_glass(u, out):
    inst = []
    seen_rules = set()
    for d in u.all_decls():
        if d.prop in ('backdrop-filter', '-webkit-backdrop-filter') and 'blur(' in d.value:
            m = re.search(r'blur\(\s*([\d.]+)\s*(px|rem|em)?', d.value)
            px = parse_len_px(m.group(1) + (m.group(2) or 'px')) if m else 0
            if px is not None and px < 2:
                continue
            key = id(d.rule) if d.rule is not None else id(d)
            if key in seen_rules:
                continue
            seen_rules.add(key)
            ctx = (d.selector or '')
            if d.node is not None:
                ctx += ' ' + d.node.ctx() + ' ' + ' '.join(a.ctx() for a in d.node.ancestors(2))
            if GLASS_EXEMPT_RE.search(ctx):
                continue
            inst.append((d.sf, d.off, ctx))
    for n in u.nodes:
        if not any(b.startswith('backdrop-blur') and b != 'backdrop-blur-none' for v, b in n.tw()):
            continue
        ctx = n.ctx() + ' ' + ' '.join(a.ctx() for a in n.ancestors(2))
        if n.ltag in ('nav', 'header', 'dialog') or GLASS_EXEMPT_RE.search(ctx) or \
                any(a.ltag in ('nav', 'header', 'dialog') for a in n.ancestors(2)):
            continue
        inst.append((n.sf, n.start, ctx))
    if len(inst) >= 2 or any(GLASS_CARD_RE.search(c) for s, o, c in inst):
        for sf, off, ctx in inst:
            out.add('glassmorphism', sf, off, 'backdrop blur on a content surface (%d in this page/app)' % len(inst))


# ---- radius ----------------------------------------------------------------------------

def check_radius(u, out):
    vals = []
    for d in u.all_decls():
        if d.prop in ('border-radius', 'border-top-left-radius', 'border-top-right-radius',
                      'border-bottom-left-radius', 'border-bottom-right-radius'):
            v = u.resolve(d.value).strip()
            toks = v.split()
            if not toks:
                continue
            if '%' in toks[0]:
                vals.append((9999, d.sf, d.off))
                continue
            px = parse_len_px(toks[0])
            if px is None:
                continue
            vals.append((9999 if px >= 100 else round(px), d.sf, d.off))
    for n in u.nodes:
        for v, b in n.tw():
            m = re.match(r'^rounded(?:-(?:t|r|b|l|tl|tr|br|bl|s|e|ss|se|es|ee|x|y))?(?:-(none|xs|sm|md|lg|xl|2xl|3xl|4xl|full|\[[^\]]+\]))?$', b)
            if not m:
                continue
            k = m.group(1) or ''
            if k.startswith('['):
                px = parse_len_px(k[1:-1])
                if px is None:
                    continue
                vals.append((9999 if px >= 100 else round(px), n.sf, n.start))
            else:
                vals.append((TW_RADIUS.get(k, 4), n.sf, n.start))
    nonpill = [x for x in vals if x[0] < 9999]
    if len(nonpill) < 6:
        return
    cnt = Counter(x[0] for x in nonpill)
    mode, k = cnt.most_common(1)[0]
    if mode >= 12 and k >= 0.7 * len(nonpill):
        first = next(x for x in nonpill if x[0] == mode)
        out.add('uniform-radius', first[1], first[2],
                '%dpx radius on %d of %d rounded elements (no scale by role)' % (mode, k, len(nonpill)))


# ---- side stripe -----------------------------------------------------------------------

def check_side_stripe(u, out):
    for r in u.rules:
        if r.kind != 'rule' or 'blockquote' in r.selector.lower():
            continue
        all_w = None
        side = {}
        for d in r.decls:
            p = d.prop
            v = u.resolve(d.value)
            if p == 'border':
                w = re.search(r'(\d*\.?\d+)px', v)
                all_w = float(w.group(1)) if w else all_w
            m = re.match(r'^border-(left|right|top|inline-start|block-start)(-width|-color)?$', p)
            if m:
                s = m.group(1)
                ent = side.setdefault(s, {'w': None, 'c': None, 'd': d})
                if m.group(2) in (None, '-width'):
                    w = re.search(r'(\d*\.?\d+)px', v)
                    if w:
                        ent['w'] = float(w.group(1))
                if m.group(2) in (None, '-color'):
                    cols = u.colors(v)
                    if cols:
                        ent['c'] = cols[0]
        for s, ent in side.items():
            if ent['w'] and ent['w'] >= 2 and is_saturated(ent['c'], 0.25) and ent['c'][3] >= 0.5:
                if all_w is not None and all_w >= ent['w'] - 1:
                    continue
                d = ent['d']
                out.add('side-stripe-border', d.sf, d.off, '%gpx coloured border-%s on %s' % (ent['w'], s, shorten(r.selector, 50)))
    for n in u.nodes:
        if n.ltag == 'blockquote':
            continue
        bases = [b for v, b in n.tw() if not v]
        w = None
        for b in bases:
            m = re.match(r'^border-([lrts])-(\d+|\[\d+px\])$', b)
            if m:
                ww = m.group(2).strip('[]px')
                try:
                    w = float(ww)
                except ValueError:
                    w = None
        if not w or w < 2:
            continue
        chrom = False
        for b in bases:
            c = tw_color(b)
            if c and c[0].startswith('border'):
                pref, rgba, pal, shade = c
                if pal and pal not in TW_NEUTRAL and (shade or 0) >= 300:
                    chrom = True
                elif rgba is not None and is_saturated(rgba, 0.25):
                    chrom = True
        if chrom:
            out.add('side-stripe-border', n.sf, n.start, '%gpx coloured side border on <%s>' % (w, n.tag))


# ---- glows -------------------------------------------------------------------------------

def shadow_glows(u, value):
    v = u.resolve(value)
    hits = []
    for layer in split_top(v, ','):
        cols = [parse_color(m.group(0)) for m in COLOR_RE.finditer(layer)]
        cols = [c for c in cols if c]
        if not cols:
            continue
        rest = COLOR_RE.sub(' ', layer)
        lens = [parse_len_px(x[0] + (x[1] or 'px')) for x in re.findall(r'(?<![\w.#-])(-?\d*\.?\d+)(px|rem|em)?(?![\w%])', rest)]
        lens = [x for x in lens if x is not None]
        blur = lens[2] if len(lens) >= 3 else 0
        c = cols[0]
        if blur >= 15 and c[3] >= 0.1 and is_saturated(c, 0.3):
            hits.append((layer.strip(), lens[0] == 0 and lens[1] == 0 if len(lens) >= 2 else False))
    return hits


def check_glow(u, out):
    for d in u.all_decls():
        if d.prop in ('box-shadow', 'text-shadow'):
            g = shadow_glows(u, d.value)
            if g:
                out.add('colored-glow', d.sf, d.off, 'coloured %s glow: %s' % (d.prop, shorten(g[0][0], 60)))
        elif d.prop == 'filter' and 'drop-shadow(' in d.value:
            for m in re.finditer(r'drop-shadow\(((?:[^()]|\([^()]*\))*)\)', u.resolve(d.value)):
                if shadow_glows(u, '0 0 ' + m.group(1) if len(re.findall(r'-?\d*\.?\d+px', m.group(1))) == 1 else m.group(1)):
                    out.add('colored-glow', d.sf, d.off, 'coloured drop-shadow glow')
                    break
    for n in u.nodes:
        for v, b in n.tw():
            c = tw_color(b)
            if c and c[0] == 'shadow':
                pref, rgba, pal, shade = c
                op = re.search(r'/(\d+)$', b)
                if op and int(op.group(1)) < 10:
                    continue
                if (pal and pal not in TW_NEUTRAL and (shade or 0) >= 300) or (rgba is not None and is_saturated(rgba, 0.3)):
                    out.add('colored-glow', n.sf, n.start, 'coloured shadow class %s' % b)
                    break
            m = re.match(r'^(?:drop-)?shadow-\[(.+)\]$', b)
            if m and shadow_glows(u, m.group(1).replace('_', ' ')):
                out.add('colored-glow', n.sf, n.start, 'coloured glow %s' % shorten(b, 60))
                break


def check_ambient_glow(u, out):
    for d in u.all_decls():
        if d.prop not in ('background', 'background-image'):
            continue
        rv = u.resolve(d.value)
        for g in gradients_in(rv):
            if not re.match(r'(repeating-)?(radial|conic)', g, re.I):
                continue
            cols = [parse_color(m.group(0)) for m in COLOR_RE.finditer(g)]
            if any(c and c[3] >= 0.08 and is_saturated(c, 0.3) for c in cols):
                out.add('ambient-glow-bg', d.sf, d.off, 'decorative %s colour glow on %s' % (g.split('(')[0], shorten(d.selector, 40)))
                break
    for r in u.rules:
        blur = None
        bg = False
        for d in r.decls:
            if d.prop == 'filter':
                m = re.search(r'blur\(\s*([\d.]+)(px|rem)?', d.value)
                if m:
                    blur = parse_len_px(m.group(1) + (m.group(2) or 'px'))
            if d.prop in ('background', 'background-color', 'background-image'):
                if any(is_saturated(c, 0.3) for c in u.colors(d.value)):
                    bg = True
        if blur and blur >= 40 and bg:
            out.add('ambient-glow-bg', r.sf, r.off, 'blurred colour blob (%s, blur %dpx)' % (shorten(r.selector, 40), blur))
    for n in u.nodes:
        bases = set(b for v, b in n.tw())
        blurred = any(re.match(r'^blur-(2xl|3xl|\[(\d+)px\])$', b) and (b in ('blur-2xl', 'blur-3xl') or int(re.search(r'\d+', b).group(0)) >= 40) for b in bases)
        if not blurred:
            if any(b.startswith('bg-[radial-gradient') or b.startswith('bg-radial') for b in bases):
                out.add('ambient-glow-bg', n.sf, n.start, 'radial gradient glow on <%s>' % n.tag)
            continue
        colored = False
        for b in bases:
            c = tw_color(b)
            if c and c[0] in ('bg', 'from', 'via', 'to'):
                if (c[2] and c[2] not in TW_NEUTRAL) or (c[1] is not None and is_saturated(c[1], 0.3)):
                    colored = True
        if colored and ('absolute' in bases or 'fixed' in bases):
            out.add('ambient-glow-bg', n.sf, n.start, 'blurred colour blob behind content (<%s>)' % n.tag)


# ---- tracking ---------------------------------------------------------------------------

def _ls_em(value, size_px):
    m = re.match(r'^\s*(-?\d*\.?\d+)\s*(em|px|rem)?\s*$', value or '')
    if not m:
        return None
    v = float(m.group(1))
    unit = m.group(2) or 'px'
    if unit == 'em':
        return v
    px = v * 16 if unit == 'rem' else v
    return px / (size_px or 16.0)


def _tracking_eval(u, out, sf, off, size, em, where):
    if em is None or em >= 0:
        return
    # typography.0.51 [11]: nothing negative at 12px or below (13-15px may be slightly negative, as SF's own table
    # is), and never tighter than -0.04em at any size (-0.045em leaves room for rounding).
    if size is not None and size <= 12 and em < -0.001:
        out.add('neg-tracking-small', sf, off, '%+.3fem tracking at %gpx (%s)' % (em, size, where))
    elif em <= -0.045:
        out.add('tracking-too-tight', sf, off, '%+.3fem tracking%s (%s); the floor is -0.04em'
                % (em, ' at %gpx' % size if size else '', where))


def check_tracking(u, out):
    for r in u.rules:
        if r.kind != 'rule':
            continue
        size = None
        ls = None
        for d in r.decls:
            if d.prop == 'font-size':
                size = parse_len_px(u.resolve(d.value)) or size
            elif d.prop == 'font':
                m = re.search(r'(?:^|\s)(\d*\.?\d+(?:px|rem|em))(?:\s*/|\s)', u.resolve(d.value))
                if m:
                    size = parse_len_px(m.group(1))
            elif d.prop == 'letter-spacing':
                ls = d
        if ls is not None:
            raw = u.resolve(ls.value)
            if not re.search(r'(px|rem)\s*$', raw) or size is not None:
                _tracking_eval(u, out, ls.sf, ls.off, size, _ls_em(raw, size), shorten(r.selector, 40))
    for n in u.nodes:
        size, tr = None, None
        for v, b in n.tw():
            if v:
                continue
            s = tw_font_px(b)
            if s:
                size = s
            t = tw_tracking(b)
            if t:
                tr = t
        for d in n.inline_decls:
            if d.prop == 'font-size':
                size = parse_len_px(d.value) or size
            if d.prop == 'letter-spacing':
                mm = re.match(r'^\s*(-?\d*\.?\d+)\s*(em|px|rem)?', d.value)
                if mm:
                    tr = (float(mm.group(1)), mm.group(2) or 'px')
        if tr is None:
            continue
        val, unit = tr
        em = val if unit == 'em' else (val * (16 if unit == 'rem' else 1)) / (size or 16.0)
        _tracking_eval(u, out, n.sf, n.start, size, em, '<%s>' % n.tag)


def check_tracked_caps(u, out):
    items = []
    for r in u.rules:
        if r.kind != 'rule':
            continue
        tt = any(d.prop == 'text-transform' and 'uppercase' in d.value for d in r.decls)
        lsd = [d for d in r.decls if d.prop == 'letter-spacing']
        if not tt or not lsd:
            continue
        if any(c.tag in ('th', 'thead') for c in r.comps()) or re.search(r'\bth\b|thead', r.selector):
            continue  # table headers: modest caps tracking is a convention, not an eyebrow
        size = None
        for d in r.decls:
            if d.prop == 'font-size':
                size = parse_len_px(u.resolve(d.value)) or size
        em = _ls_em(u.resolve(lsd[-1].value), size or 12.0)
        if em is None or em <= 0:
            continue
        uses = 0
        for c in r.comps():
            if c.classes:
                uses += sum(1 for n in u.nodes if c.classes.issubset(n.class_set))
        items.append((em, lsd[-1].sf, lsd[-1].off, max(1, uses)))
    for n in u.nodes:
        bases = [b for v, b in n.tw() if not v]
        if 'uppercase' not in bases:
            continue
        if n.ltag == 'th' or any(a.ltag in ('thead', 'table') for a in n.ancestors(6)):
            continue
        for b in bases:
            t = tw_tracking(b)
            if t and t[0] > 0:
                em = t[0] if t[1] == 'em' else t[0] / 12.0
                items.append((em, n.sf, n.start, 1))
                break
    if not items:
        return
    # Caps tracked +0.03..+0.1em is the research band (typography.0.51 [11]); the tell is 0.18-0.22em, or wide
    # tracking used as the default label style.
    total = sum(x[3] for x in items)
    wide = [x for x in items if x[0] > 0.1]
    total_wide = sum(x[3] for x in wide)
    widest = max(items, key=lambda x: x[0])
    if widest[0] >= 0.15 or total_wide >= 4:
        first = min(wide, key=lambda x: (x[1].path, x[2]))
        anchor = widest if widest[0] >= 0.15 else first
        out.add('tracked-caps-labels', anchor[1], anchor[2],
                '%d uppercase label%s tracked past +0.1em (of %d); widest %+.2fem'
                % (total_wide, '' if total_wide == 1 else 's', total, widest[0]))


# ---- body text size -------------------------------------------------------------------

SMALL_OK_RE = re.compile(r'small|caption|legal|fine|footnote|meta|note|hint|helper|label|badge|tag|chip|disclaimer|'
                         r'copyright|footer|nav|btn|button|input|table|\bth\b|\btd\b|code|kbd|tooltip|eyebrow|'
                         r'overline|kicker|breadcrumb|cookie|toast|chart|axis|\btab', re.I)


def check_body_size(u, out):
    # Product UI and dashboards may set secondary and data text at 13-15px (typography context rule 9); there only
    # text under 13px, or running prose of 60+ words under 15px, is flagged.
    floor = 13 if tool_surface() else 15
    flagged_rules = set()
    for r in u.rules:
        if r.kind != 'rule' or SMALL_OK_RE.search(r.selector):
            continue
        if not any((c.tag in ('body', 'html', 'p', 'article', 'main') or c.classes & {'lead', 'prose', 'body-text'})
                   and not c.pseudo and not c.state for c in r.comps()):
            continue
        size = None
        for d in r.decls:
            if d.prop == 'font-size':
                size = parse_len_px(u.resolve(d.value))
                dd = d
        if size is not None and size < floor:
            flagged_rules.add(id(r))
            out.add('body-text-small', dd.sf, dd.off, 'body copy at %gpx (%s)' % (size, shorten(r.selector, 40)))
    for n in u.nodes:
        if n.ltag != 'p':
            continue
        t = n.text()
        if len(t.split()) < 24:
            continue
        chain = [n] + n.ancestors(6)
        if any(a.ltag in ('footer', 'small', 'figcaption', 'table', 'nav', 'aside') or
               SMALL_OK_RE.search(' '.join(a.classes)) for a in chain):
            continue
        size = None
        where = ''
        for v, b in n.tw():
            s = tw_font_px(b)
            if s is None:
                continue
            if not v:
                size, where = s, b
            elif v[-1] in ('sm', 'md', 'lg', 'xl') and s >= 15:
                size, where = None, ''
                break
        if size is None:
            for d in u.decls_for(n):
                if d.prop == 'font-size' and (d.rule is None or id(d.rule) not in flagged_rules):
                    s = parse_len_px(u.resolve(d.value))
                    if s is not None:
                        size, where = s, (d.selector or '')
        limit = 15 if (not tool_surface() or len(t.split()) >= 60) else floor
        if size is not None and size < limit:
            out.add('body-text-small', n.sf, n.start, '%d-word paragraph at %gpx (%s)' % (len(t.split()), size, shorten(where, 40)))


# ---- mono display -----------------------------------------------------------------------

MONO_SEL_RE = re.compile(r'(^|[\s.#_-])(hero|title|headline|heading|lead|tagline|subtitle|display|intro|body|copy|'
                         r'description)($|[\s._-])', re.I)


def check_mono(u, out):
    for r in u.rules:
        if r.kind != 'rule' or re.search(r'code|pre|kbd|samp|terminal|console|mono', r.selector, re.I):
            continue
        for d in r.decls:
            if d.prop not in ('font-family', 'font'):
                continue
            val = d.value if d.prop == 'font-family' else (font_shorthand_family(d.value) or '')
            f = first_family(val, u) if val else None
            if not f or not (MONO_RE.search(f) or f in ('monospace', 'ui-monospace')):
                continue
            comps = r.comps()
            if any(c.tag in ('body', 'html', 'h1', 'h2', 'h3', 'h4', 'p', 'blockquote') for c in comps) or MONO_SEL_RE.search(r.selector):
                out.add('mono-display', d.sf, d.off, 'monospace (%s) on %s' % (f, shorten(r.selector, 40)))
    for n in u.nodes:
        if n.ltag in CODE_TAGS or any(a.ltag in CODE_TAGS for a in n.ancestors(8)):
            continue
        mono = 'font-mono' in u.tw_bases(n)
        if not mono:
            for d in n.inline_decls:
                if d.prop == 'font-family' and MONO_RE.search(d.value):
                    mono = True
        if not mono:
            continue
        words = len(n.text().split())
        if n.ltag in ('h1', 'h2', 'h3', 'h4', 'p', 'blockquote') and words >= 2 or words >= 8:
            out.add('mono-display', n.sf, n.start, 'monospace on <%s> (%d words): "%s"' % (n.tag, words, shorten(n.text(), 40)))


# ---- icon card grid ---------------------------------------------------------------------

def is_icon_el(u, n):
    if n.ltag in ('svg', 'i'):
        return True
    if n.ltag == 'img' and re.search(r'icon|\.svg', str(n.attrs.get('src', '')) + ' ' + ' '.join(n.classes), re.I):
        return True
    if n.is_component and (n.tag.endswith('Icon') or re.match(r'^(Lucide|(Hero|Fa|Md|Io|Bi|Ri|Tb|Fi|Hi|Ph|Icon)[A-Z0-9])', n.tag)
                           or n.tag.endswith('.icon')):
        return True
    if n.is_component and not n.children and not re.search(r'avatar|image|img|logo|photo|picture|video', n.tag, re.I) and \
            (any(re.match(r'^(h|w|size)-\d', c) for c in n.classes) or 'size' in n.attrs or 'strokeWidth' in n.attrs):
        return True
    if any(re.search(r'(^|[-_])(icon|icons|lucide|feather|heroicon|material-(icons|symbols)[\w-]*|fa|fas|far|fab|fa-[\w-]+|bi|bi-[\w-]+|ti|ti-[\w-]+|ph|ph-[\w-]+|ri-[\w-]+|iconify)($|[-_])', c) for c in n.classes):
        return True
    if any(k in n.attrs for k in ('data-lucide', 'data-feather', 'data-icon')):
        return True
    t = n.text()
    if t and len(t) <= 4 and emoji_only(t):
        return True
    return False


def is_row(u, n):
    """True when n lays its children out side by side (flex row)."""
    bases = u.tw_bases(n)
    if bases & {'flex', 'inline-flex'} and not bases & {'flex-col', 'flex-col-reverse'}:
        return True
    disp = u.last_decl(n, 'display')
    if disp is not None and 'flex' in disp.value:
        fd = u.last_decl(n, 'flex-direction')
        return not (fd is not None and 'column' in fd.value)
    return False


def card_signature(u, card):
    order = []
    for i, d in enumerate(card.descendants(5)):
        if is_icon_el(u, d):
            order.append(('icon', i, d))
        elif d.ltag in ('h2', 'h3', 'h4', 'h5', 'h6') or (d.ltag in ('strong', 'b') and len(d.text().split()) <= 6) or \
                any(re.search(r'(^|-)(title|heading|headline)($|-)', c) for c in d.classes):
            order.append(('title', i, d))
        elif (d.ltag == 'p' or any(re.search(r'(^|-)(desc|description|text|body|copy|blurb|summary|excerpt)($|-)', c) for c in d.classes)) and len(d.text().split()) >= 3:
            order.append(('text', i, d))
    icon = next((x for x in order if x[0] == 'icon'), None)
    if icon is None:
        return False
    title = next((x for x in order if x[0] == 'title' and x[1] > icon[1] and icon[2] not in x[2].ancestors(6)), None)
    if title is None:
        return False
    text = next((x for x in order if x[0] == 'text' and x[1] > title[1]), None)
    if text is None:
        return False
    # Icon beside the heading (flex row shared with the title block) is the recommended pattern, not a tile.
    par = icon[2].parent
    if par is not None and par is not card and is_row(u, par) and par in title[2].ancestors(6):
        return False
    if par is card and is_row(u, card):
        return False
    return True


GRID_RE = re.compile(r'(?<![\w-])(?:[\w-]+:)?grid-cols-[2-6](?![\w-])|grid-template-columns\s*:|flex-wrap(?![\w-])|'
                     r'flexWrap\s*:\s*["\']wrap')
NAV_KEY_RE = re.compile(r'\b(href|url|path|to|route|onClick|onSelect|action|shortcut|link|slug)\s*:')
MAP_ICON_TAG_RE = re.compile(r'^[A-Za-z_]\w*\.icon$|^Icon$', re.I)
MAP_ICON_EXPR_RE = re.compile(r'\{\s*[A-Za-z_]\w*\.icon\s*\}', re.I)
TITLE_CLASS_RE = re.compile(r'(^|-)(title|heading|headline|name)($|-)')


def map_icon_nodes(sf):
    """Icons rendered from a data item inside a JSX .map(): <item.icon/>, <Icon/> or an element wrapping {item.icon}."""
    res = []
    for n in sf.nodes:
        if MAP_ICON_TAG_RE.match(n.tag):
            res.append(n)
            continue
        for c in n.children:
            if isinstance(c, TextSeg) and MAP_ICON_EXPR_RE.search(c.raw):
                res.append(n)
                break
    return res


def icon_stacked(u, icon):
    """True when the templated icon sits above its title (a tile), False when a flex row puts it beside the title."""
    for anc in icon.ancestors(3):
        title = next((d for d in anc.descendants(4) if d.start > icon.start and (
            d.ltag in ('h2', 'h3', 'h4', 'h5', 'h6') or any(TITLE_CLASS_RE.search(c) for c in d.classes))), None)
        if title is None:
            continue
        x = icon.parent
        while x is not None:
            if is_row(u, x) and x in title.ancestors(6):
                return False
            if x is anc:
                break
            x = x.parent
        return True
    return False


def check_icon_grid(u, out):
    for sf in u.markup_files():
        done = set()
        for p in sf.nodes:
            kids = p.elem_children()
            if len(kids) < 3 or id(p) in done:
                continue
            matches = [k for k in kids if card_signature(u, k)]
            if len(matches) >= 3 and len(matches) >= 0.75 * len(kids) and len(set(k.tag for k in matches)) == 1:
                out.add('icon-card-grid', sf, p.start, '%d cards shaped icon -> title -> text under <%s>' % (len(matches), p.tag))
                sf.markers.setdefault('icon + title + text feature cards', p.start)
                for d in p.descendants(10):
                    done.add(id(d))
    # JS data arrays ({icon, title, description} x3+). Nav menus, settings indexes and command palettes share this
    # shape, so only report when the same file renders a multi-column grid AND some element in it stacks an icon
    # above a title and text (an icon in a flex row beside its title is the recommended alternative).
    for sf in u.files:
        if not GRID_RE.search(sf.text):
            continue
        if not any(icon_stacked(u, n) for n in map_icon_nodes(sf)):
            continue
        for (a, b) in sf.js_regions:
            region = sf.text[a:b]
            objs = [m for m in re.finditer(r'\{[^{}]*\}', region)
                    if re.search(r'\bicon\s*:', m.group(0)) and re.search(r'\b(title|name|heading)\s*:', m.group(0))
                    and re.search(r'\b(description|desc|text|body|copy|blurb|summary|content)\s*:', m.group(0))
                    and not NAV_KEY_RE.search(m.group(0))]
            run = []
            for m in objs:
                if run and m.start() - run[-1].end() > 800:
                    run = []
                run.append(m)
                if len(run) == 3:
                    out.add('icon-card-grid', sf, a + run[0].start(), 'data array of icon + title + description cards')
                    sf.markers.setdefault('icon + title + text feature cards', a + run[0].start())
                    break


# ---- accent hues -----------------------------------------------------------------------

COLOR_PROPS = {'color', 'background', 'background-color', 'background-image', 'border', 'border-color',
               'border-top', 'border-bottom', 'border-left', 'border-right', 'border-top-color',
               'border-bottom-color', 'border-left-color', 'border-right-color', 'outline', 'outline-color',
               'fill', 'stroke', 'text-decoration-color', 'accent-color', 'caret-color', 'box-shadow',
               'text-shadow'}
DATA_TOKEN_RE = re.compile(r'chart|data|series|viz|syntax|hl|shiki|prism|token|code|terminal|graph|plot', re.I)


def check_accent_hues(u, out):
    fam = OrderedDict()

    def note(f, sf, off):
        if f is None:
            return
        if f not in fam:
            fam[f] = [0, sf, off]
        fam[f][0] += 1
    for d in u.all_decls():
        if d.prop.startswith('--'):
            if DATA_TOKEN_RE.search(d.prop):
                continue
        elif d.prop not in COLOR_PROPS:
            continue
        if DATA_TOKEN_RE.search(d.selector or '') or re.search(r'\bsvg\b|::selection', d.selector or ''):
            continue
        if d.node is not None and any(a.ltag == 'svg' for a in [d.node] + d.node.ancestors(8)):
            continue
        val = u.resolve(d.value)
        for g in gradients_in(val):  # a gradient is one decision (and purple ones are flagged elsewhere)
            val = val.replace(g, ' ')
        for c in u.colors(val):
            note(hue_family(c), d.sf, d.off)
    for n in u.nodes:
        if n.ltag == 'svg' or any(a.ltag == 'svg' for a in n.ancestors(8)):
            continue
        for v, b in n.tw():
            c = tw_color(b)
            if not c:
                continue
            pref, rgba, pal, shade = c
            if pref in ('from', 'via', 'to'):
                continue
            if pal:
                if pal in TW_NEUTRAL or (shade or 0) < 400:
                    continue
                note(TW_FAMILY.get(pal), n.sf, n.start)
            else:
                note(hue_family(rgba), n.sf, n.start)
    semantic = {'red', 'green', 'amber'}
    acc = [f for f in fam if f not in semantic]
    if len(acc) >= 3 or len(fam) >= 6:
        third = fam[acc[2]] if len(acc) >= 3 else list(fam.values())[5]
        desc = ', '.join('%s x%d' % (f, fam[f][0]) for f in fam)
        out.add('accent-hue-count', third[1], third[2], '%d hue families in use (%s); accents beyond semantic red/amber/green: %d'
                % (len(fam), desc, len(acc)))


# ---- pure black/white --------------------------------------------------------------------

PAGE_SEL = {'html', 'body', ':root', '#root', '#__next', '#app', 'main', '#__nuxt', '#svelte'}
BG_TOKEN_RE = re.compile(r'^--(?:color-)?(background|bg|canvas|page|page-bg|bg-page|surface-page|base-100|body-bg|bg-body|paper)$')
INK_TOKEN_RE = re.compile(r'^--(?:color-)?(foreground|fg|text|ink|body-text|text-primary|color-text|base-content)$')
SECTION_TAGS = {'section', 'footer', 'header', 'aside', 'article'}
SECTION_SEL_RE = re.compile(r'(^|[\s.#_-])(section|band|hero|footer|header|aside|panel|surface|card|tile|feature|cta|'
                            r'banner|stage|inverse|inverted|dark|alt|muted|statement|spotlight)($|[\s._:#-])', re.I)
SURFACE_TOKEN_RE = re.compile(r'^--(?:color-)?(surface|bg|background|canvas|band|ground|paper|card|panel|muted|'
                              r'inverse|inverted)[\w-]*$')


def check_pure_bw(u, out):
    whites, blacks, inks = [], [], []
    offwhite = False

    def is_page_sel(sel):
        for part in split_top(sel or '', ','):
            p = part.strip()
            if p in PAGE_SEL or re.match(r'^(html|body)(\s*,|$)', p):
                return True
        return False
    for d in u.all_decls():
        if any('prefers-contrast' in m for m in (d.media or [])):
            continue
        rv = u.resolve(d.value)
        cols = u.colors(d.value) if d.prop in ('background', 'background-color', 'color') or d.prop.startswith('--') else []
        surface = (d.prop in ('background', 'background-color') and 'gradient(' not in rv) or \
            (d.prop.startswith('--') and not INK_TOKEN_RE.match(d.prop) and
             not re.search(r'foreground|-fg\b|text|ink|border|ring|shadow|chart', d.prop))
        if surface and not any(s in (d.selector or '') for s in (':hover', ':focus', ':active')):
            for c in cols:
                if is_offwhite(c):
                    offwhite = True
                # Any declared non-white section or surface ground (a brand band, an inverted dark section, a tinted
                # tier) is a second tier too; only a page whose every surface is #fff is the flat-white tell.
                elif not is_pure(c, (255, 255, 255)) and c[3] >= 0.5 and \
                        not any('prefers-color-scheme' in m for m in (d.media or [])) and \
                        not re.search(r'\.dark\b|data-theme|data-mode', d.selector or '') and (
                        (SECTION_SEL_RE.search(d.selector or '') and not is_page_sel(d.selector)) or
                        (SURFACE_TOKEN_RE.match(d.prop) and not BG_TOKEN_RE.match(d.prop))):
                    offwhite = True
        if d.prop in ('background', 'background-color') and 'gradient(' not in rv and 'url(' not in rv and cols:
            page = is_page_sel(d.selector) or (d.node is not None and d.node.ltag in ('html', 'body'))
            if page:
                if is_pure(cols[0], (255, 255, 255)):
                    whites.append((d.sf, d.off, d.selector))
                elif is_pure(cols[0], (0, 0, 0)):
                    blacks.append((d.sf, d.off, d.selector))
        elif d.prop == 'color' and cols and is_pure(cols[0], (0, 0, 0)):
            if is_page_sel(d.selector) or (d.node is not None and d.node.ltag in ('html', 'body')):
                inks.append((d.sf, d.off, d.selector))
        elif d.prop.startswith('--') and cols and re.search(r':root|^html|@theme', d.selector or ''):
            if BG_TOKEN_RE.match(d.prop):
                if is_pure(cols[0], (255, 255, 255)):
                    whites.append((d.sf, d.off, d.prop))
                elif is_pure(cols[0], (0, 0, 0)):
                    blacks.append((d.sf, d.off, d.prop))
            elif INK_TOKEN_RE.match(d.prop) and is_pure(cols[0], (0, 0, 0)):
                inks.append((d.sf, d.off, d.prop))
    for n in u.nodes:
        bases = [b for v, b in n.tw()]
        for v, b in n.tw():
            if v and not set(v) <= {'sm', 'md', 'lg', 'xl', '2xl'}:
                continue  # hover:/focus:/dark: states are not a light surface tier
            if re.match(r'^bg-(gray|slate|zinc|neutral|stone)-(50|100|200)$', b):
                offwhite = True
            c = tw_color(b)
            if c and c[1] is not None and c[0] == 'bg' and is_offwhite(c[1]):
                offwhite = True
            elif (n.ltag in SECTION_TAGS or SECTION_SEL_RE.search(' '.join(n.classes))) and \
                    n.ltag not in ('html', 'body') and (b == 'bg-black' or (c and c[0] == 'bg' and (
                        c[2] is not None or (c[1] is not None and not is_pure(c[1], (255, 255, 255)) and
                                             c[1][3] >= 0.5)))):
                offwhite = True  # a non-white section band (brand colour, inverted dark) is a second tier
        page = n.ltag in ('html', 'body') or any(b in ('min-h-screen', 'min-h-dvh', 'min-h-svh', 'h-screen', 'h-dvh') for b in bases)
        if not page:
            continue
        for b in bases:
            if b in ('bg-white', 'bg-[#fff]', 'bg-[#ffffff]'):
                whites.append((n.sf, n.start, '<%s> %s' % (n.tag, b)))
            elif b in ('bg-black', 'bg-[#000]', 'bg-[#000000]'):
                blacks.append((n.sf, n.start, '<%s> %s' % (n.tag, b)))
            elif b in ('text-black', 'text-[#000]', 'text-[#000000]'):
                inks.append((n.sf, n.start, '<%s> %s' % (n.tag, b)))
    for sf, off, where in blacks[:2]:
        out.add('pure-black-white', sf, off, 'page ground is pure #000 (%s)' % shorten(where, 40))
    for sf, off, where in inks[:2]:
        out.add('pure-black-white', sf, off, 'body ink is pure #000 (%s)' % shorten(where, 40))
    if whites and not offwhite:
        sf, off, where = whites[0]
        out.add('pure-black-white', sf, off, 'flat pure #fff page with no off-white surface tier (%s)' % shorten(where, 40))


# ---- motion ----------------------------------------------------------------------------

ANIM_KEYWORDS = {'infinite', 'alternate', 'alternate-reverse', 'normal', 'reverse', 'forwards', 'backwards', 'both',
                 'none', 'running', 'paused', 'linear', 'ease', 'ease-in', 'ease-out', 'ease-in-out', 'step-start',
                 'step-end', 'initial', 'inherit'}
LOADER_RE = re.compile(r'spin|spinner|loader|loading|skeleton|progress|busy', re.I)
MARQUEE_RE = re.compile(r'marquee|ticker|scroll-x|scroll-left|infinite-scroll|slide-left|loop-x|logo-scroll', re.I)
LAYOUT_PROPS = {'width', 'height', 'max-height', 'min-height', 'max-width', 'min-width', 'top', 'left', 'right',
                'bottom', 'margin', 'margin-top', 'margin-left', 'margin-right', 'margin-bottom', 'padding',
                'padding-top', 'padding-bottom', 'padding-left', 'padding-right', 'inset'}
REVEAL_CLASS_RE = re.compile(r'^(reveal|reveal-[\w-]+|fade-up|fade-in-up|fadeInUp|slide-up|slide-in-up|animate-on-scroll|'
                             r'scroll-reveal|on-scroll|js-reveal|aos-[\w-]+)$')


SKELETON_CTX_RE = re.compile(r'skeleton|loading|placeholder|shimmer-?(row|line|block|bar)', re.I)
NEUTRAL_BG_RE = re.compile(r'^bg-(gray|slate|zinc|neutral|stone|muted|secondary|accent|border|input|black/|white/)')


def is_skeleton(n):
    """Loading UI (components-details.md section 3 asks for skeletons): an empty, neutral animate-pulse block, or
    anything under aria-busy / role=status|progressbar / a skeleton|loading|placeholder class or component."""
    if n is None:
        return False
    for a in [n] + n.ancestors(4):
        if str(a.attrs.get('aria-busy', '')).strip('{}"\' ').lower() == 'true':
            return True
        if str(a.attrs.get('role', '')).lower() in ('status', 'progressbar'):
            return True
        if SKELETON_CTX_RE.search(a.ctx()):
            return True
    bases = set(b for v, b in n.tw())
    if 'animate-pulse' in bases and not n.text() and not n.elem_children():
        if any(NEUTRAL_BG_RE.match(b) for b in bases) and not any(b.startswith('blur') for b in bases):
            return True
    return False


def anim_names(value):
    names = []
    for part in split_top(value, ','):
        toks = re.sub(r'(cubic-bezier|steps|linear)\([^)]*\)', ' ', part).split()
        name = None
        for t in toks:
            tl = t.lower()
            if tl in ANIM_KEYWORDS or re.match(r'^-?[\d.]+(m?s)?$', tl):
                continue
            name = t
            break
        names.append((name or '?', 'infinite' in part.lower(), part))
    return names


def check_motion(u, out):
    uses = []  # (name, infinite, sf, off, ctx)
    kf_names = OrderedDict((k.name, k) for k in u.keyframes)
    tw_anim_cfg = {}
    for sf in u.files:
        for m in re.finditer(r'\banimation\s*:\s*\{', sf.text):
            j = match_brace(sf.text, m.end() - 1)
            for km in re.finditer(r'(["\']?)([\w-]+)\1\s*:\s*["\'`]([^"\'`]+)["\'`]', sf.text[m.end():j]):
                tw_anim_cfg[km.group(2)] = 'infinite' in km.group(3)
    for r in u.rules:
        if r.kind != 'rule':
            continue
        iter_inf = any(d.prop == 'animation-iteration-count' and 'infinite' in d.value for d in r.decls)
        for d in r.decls:
            if d.prop in ('animation', 'animation-name'):
                if d.value.strip().lower() in ('none', 'initial', 'inherit', 'unset'):
                    continue
                for name, inf, part in anim_names(d.value):
                    uses.append((name, inf or iter_inf, d.sf, d.off, r.selector, None))
    for n in u.nodes:
        for d in n.inline_decls:
            if d.prop in ('animation', 'animation-name'):
                for name, inf, part in anim_names(d.value):
                    uses.append((name, inf, n.sf, n.start, n.ctx(), n))
    reveal = []
    motion_present = []
    for n in u.nodes:
        ctx = n.ctx()
        for v, b in n.tw():
            if b.startswith('animate-') and b != 'animate-none':
                name = b[8:]
                inf = name in ('pulse', 'ping', 'bounce', 'spin') or tw_anim_cfg.get(name, False) or 'infinite' in name
                if name.startswith('['):
                    inf = 'infinite' in name
                    name = name.strip('[]').split('_')[0] or name
                uses.append((name, inf, n.sf, n.start, ctx, n))
            if (b.startswith(('scale-', 'translate-', '-translate-', 'rotate-', '-rotate-')) and v) or b == 'transition-transform':
                motion_present.append((n.sf, n.start))
        if n.ltag.startswith('motion.') or n.tag.startswith('motion.') or n.tag in ('AnimatePresence',):
            props = [k for k in n.attrs if k in ('animate', 'initial', 'whileInView', 'whileHover', 'whileTap', 'exit', 'variants')]
            if props:
                inf = any(isinstance(n.attrs[k], str) and ('Infinity' in n.attrs[k] or re.search(r'repeat\s*:\s*-1', n.attrs[k])) for k in n.attrs)
                uses.append(('motion.' + n.tag.split('.')[-1], inf, n.sf, n.start, ctx, n))
                if 'whileInView' in n.attrs:
                    reveal.append((n.sf, n.start))
        if 'data-aos' in n.attrs or 'data-sal' in n.attrs or 'data-scroll' in n.attrs:
            reveal.append((n.sf, n.start))
            uses.append(('aos', False, n.sf, n.start, ctx, n))
        elif any(REVEAL_CLASS_RE.match(c) for c in n.classes):
            reveal.append((n.sf, n.start))
        if n.ltag == 'marquee':
            uses.append(('marquee', True, n.sf, n.start, 'marquee', n))
    for sf in u.files:
        for (a, b) in sf.js_regions:
            region = sf.text[a:b]
            for m in re.finditer(r'\bgsap\s*\.\s*(to|from|fromTo|timeline)\s*\(', region):
                seg = region[m.end():m.end() + 300]
                uses.append(('gsap.' + m.group(1), bool(re.search(r'repeat\s*:\s*-1', seg)), sf, a + m.start(), 'gsap', None))
    hover_transform = any(dd.prop == 'transform' for rr in u.rules if ':hover' in rr.selector for dd in rr.decls)
    for r in u.rules:
        if r.kind == 'rule':
            for d in r.decls:
                if d.prop == 'transition' and ('transform' in d.value or (hover_transform and re.search(r'\ball\b', d.value))):
                    motion_present.append((d.sf, d.off))
    # ambient (infinite) loops
    for name, inf, sf, off, ctx, node in uses:
        loopish = inf or MARQUEE_RE.search(name or '') or MARQUEE_RE.search(ctx or '')
        if not loopish:
            continue
        if LOADER_RE.search(name or '') or LOADER_RE.search(ctx or '') or is_skeleton(node):
            continue
        out.add('ambient-animation', sf, off, 'infinite "%s" animation (%s)' % (name, shorten(ctx, 40)))
    # overload
    real = [x for x in uses if not LOADER_RE.search(x[0] or '') and not LOADER_RE.search(x[4] or '')
            and not is_skeleton(x[5])]
    distinct = OrderedDict()
    for x in real:
        distinct.setdefault(x[0], x)
    for name, k in kf_names.items():
        if not LOADER_RE.search(name):
            distinct.setdefault(name, (name, False, k.sf, k.off, '@keyframes', None))
    if len(distinct) >= 5 or len(real) >= 12:
        first = min(list(distinct.values()), key=lambda x: (x[2].path, x[3]))
        out.add('animation-overload', first[2], first[3], '%d distinct animations, %d animated elements/rules (%s)'
                % (len(distinct), len(real), ', '.join(list(distinct)[:7])))
    # reveal on every section
    if len(reveal) >= 3:
        sf, off = reveal[0]
        out.add('scroll-reveal-everything', sf, off, '%d elements fade/slide in on scroll' % len(reveal))
    # reduced motion
    has_reduced = False
    for sf in u.files:
        if re.search(r'prefers-reduced-motion|useReducedMotion|reducedMotion|motion-reduce:|motion-safe:', sf.text):
            has_reduced = True
            break
    anim_locs = [(x[2], x[3]) for x in real] + [(k.sf, k.off) for k in u.keyframes] + motion_present
    if anim_locs and not has_reduced:
        sf, off = min(anim_locs, key=lambda x: (x[0].path, x[1]))
        out.add('reduced-motion-missing', sf, off, '%d animations/motion transforms and no prefers-reduced-motion path' % len(anim_locs))
    # linear easing
    for d in u.all_decls():
        if d.prop not in ('transition', 'transition-timing-function', 'animation-timing-function', 'animation'):
            continue
        if not re.search(r'(?<![\w-])linear(?![\w(-])', d.value):
            continue
        ctx = (d.selector or '') + ' ' + d.value
        if 'infinite' in d.value or LOADER_RE.search(ctx) or MARQUEE_RE.search(ctx):
            continue
        out.add('linear-easing', d.sf, d.off, 'linear timing: %s' % shorten(d.value, 60))
    for n in u.nodes:
        bases = set(b for v, b in n.tw())
        if 'ease-linear' in bases and not any(b.startswith('animate-') for b in bases) and not LOADER_RE.search(n.ctx()) \
                and not MARQUEE_RE.search(n.ctx()):
            out.add('linear-easing', n.sf, n.start, 'ease-linear on <%s>' % n.tag)
    # layout property animation
    for d in u.all_decls():
        if d.prop == 'transition':
            props = [p.split()[0].lower() for p in split_top(d.value, ',') if p.split()]
        elif d.prop == 'transition-property':
            props = [p.strip().lower() for p in d.value.split(',')]
        else:
            continue
        bad = [p for p in props if p in LAYOUT_PROPS]
        if bad:
            out.add('layout-prop-animation', d.sf, d.off, 'transition on %s' % ', '.join(bad))
    for k in u.keyframes:
        bad = sorted(set(d.prop for d in k.decls if d.prop in LAYOUT_PROPS))
        if bad:
            out.add('layout-prop-animation', k.sf, k.off, '@keyframes %s animates %s' % (k.name, ', '.join(bad)))
    for n in u.nodes:
        for v, b in n.tw():
            m = re.match(r'^transition-\[([^\]]+)\]$', b)
            if m:
                bad = [p for p in m.group(1).split(',') if p.strip() in LAYOUT_PROPS]
                if bad:
                    out.add('layout-prop-animation', n.sf, n.start, '%s on <%s>' % (b, n.tag))


# ---- copy -------------------------------------------------------------------------------

BUZZ = [
    (r'\bstreamlin(?:e|es|ed|ing)\b', 'streamline'), (r'\bempower(?:s|ed|ing)?\b', 'empower'),
    (r'\bsupercharg(?:e|es|ed|ing)\b', 'supercharge'), (r'\bworld[- ]class\b', 'world-class'),
    (r'\bnext[- ]gen(?:eration)?\b', 'next-gen'), (r'\belevat(?:e|es|ed|ing)\b', 'elevate'),
    (r'\bseamless(?:ly)?\b', 'seamless'), (r'\bunleash(?:es|ed|ing)?\b', 'unleash'),
    (r'\brevolutioni[sz](?:e|es|ed|ing)\b', 'revolutionize'), (r'\bgame[- ]chang(?:er|ers|ing)\b', 'game-changer'),
    (r'\bdelv(?:e|es|ing)\b', 'delve'), (r'\btapestry\b', 'tapestry'), (r'\bunlock(?:s|ed|ing)?\b', 'unlock'),
    (r'\bcutting[- ]edge\b', 'cutting-edge'), (r'\bstate[- ]of[- ]the[- ]art\b', 'state-of-the-art'),
    (r'\b(?:lightning|blazing)[- ]fast\b', 'lightning-fast'), (r'\buser[- ]friendly\b', 'user-friendly'),
    (r'\beffortless(?:ly)?\b', 'effortless'), (r'\bskyrocket(?:s|ed|ing)?\b', 'skyrocket'),
    (r'\bto the next level\b', 'to the next level'), (r'\ball[- ]in[- ]one\b', 'all-in-one'),
    (r'\breimagined\b', 'reimagined'),
    (r'\bpowered by (?:next[- ]gen(?:eration)? )?(?:ai|artificial intelligence)\b', 'powered by AI'),
    (r'\bintroducing\b', 'Introducing'), (r'\bwelcome to (?:our|the) (?:website|site|platform)\b', 'Welcome to our website'),
]
BUZZ_RE = [(re.compile(p, re.I), lbl) for p, lbl in BUZZ]
CADENCE_RE = [
    (re.compile(r'\bNot (?:just )?[^.!?\n]{1,48}[.!]\s+(?:Just|Only|Pure|Simply)\b'), '"Not X. Just Y." cadence'),
    (re.compile(r'\bNo [^.!?\n]{1,32}\.\s+No [^.!?\n]{1,32}\.'), '"No X. No Y." cadence'),
    (re.compile(r'\b[Nn]o \w+(?: \w+)?[,.]\s+[Jj]ust\b'), '"No X, just Y." cadence'),
    (re.compile(r'\bReady to (?:get started|transform|take|supercharge|level up|elevate|unlock|scale|boost|'
                r'revolutioni[sz]e|dive in|join|start)\b', re.I), '"Ready to ...?" CTA strip'),
]
PLACEHOLDER_TEXT = [
    (re.compile(r'\blorem ipsum\b|\bdolor sit amet\b', re.I), 'lorem ipsum'),
    (re.compile(r'\b(?:John|Jane) (?:Doe|Smith)\b'), 'placeholder person'),
    (re.compile(r'\bAcme(?: (?:Inc|Corp|Co|Corporation|Labs))?\b'), '"Acme" placeholder brand'),
    (re.compile(r'\b(?:Your Company|Company Name|Your Logo|Product Name|Your Brand)\b'), 'placeholder company'),
]
PLACEHOLDER_IMG_RE = re.compile(r'via\.placeholder\.com|placehold\.(?:co|it)|\bplaceholder\.com|dummyimage\.com|picsum\.photos|'
                                r'placekitten\.com|i\.pravatar\.cc|pravatar\.cc|randomuser\.me/api/portraits|ui-avatars\.com|'
                                r'loremflickr\.com|fakeimg\.pl')
STOCK_IMG_RE = re.compile(r'images\.unsplash\.com|source\.unsplash\.com|plus\.unsplash\.com|unsplash\.it|images\.pexels\.com|'
                          r'pexels\.com/photo|istockphoto\.com|shutterstock\.com|gettyimages\.com|freepik\.com')


def _copy_off(raw, raw_off, matched):
    k = raw.find(matched)
    if k < 0:
        k = raw.lower().find(matched.lower()[:12])
    return raw_off + max(0, k)


def check_copy(u, out):
    for sf in u.files:
        dash_count = 0
        dash_first = None
        buzz = []
        for clean, raw, off, ctx in sf.copy:
            for rx, lbl in BUZZ_RE:
                for m in rx.finditer(clean):
                    buzz.append((_copy_off(raw, off, m.group(0)), lbl, clean, ctx))
            for rx, lbl in CADENCE_RE:
                for m in rx.finditer(clean):
                    out.add('template-copy', sf, _copy_off(raw, off, m.group(0)[:10]), '%s: "%s"' % (lbl, shorten(m.group(0), 60)))
                    if lbl.startswith('"Ready'):
                        sf.markers.setdefault('"Ready to ...?" CTA strip', off)
            for rx, lbl in PLACEHOLDER_TEXT:
                for m in rx.finditer(clean):
                    out.add('placeholder-content', sf, _copy_off(raw, off, m.group(0)), '%s: "%s"' % (lbl, m.group(0)))
            n = clean.count('—')
            if n:
                dash_count += n
                if dash_first is None:
                    k = raw.find('—')
                    if k < 0:
                        k = raw.find('&mdash;')
                    dash_first = off + max(0, k)
        # One buzzword in long prose is ordinary English; two or more, or one in a heading/button/title, is the tell.
        for off, lbl, clean, ctx in buzz:
            if len(buzz) >= 2 or ctx == 'prominent':
                out.add('template-copy', sf, off, 'buzzword "%s": "%s"' % (lbl, shorten(clean, 60)))
        if dash_count >= 3:
            out.add('em-dash', sf, dash_first, '%d em-dashes in visible copy' % dash_count)
        for m in PLACEHOLDER_IMG_RE.finditer(sf.text):
            out.add('placeholder-content', sf, m.start(), 'placeholder image service %s' % m.group(0))
        for m in STOCK_IMG_RE.finditer(sf.text):
            out.add('stock-photo', sf, m.start(), 'stock image host %s' % m.group(0))


GENERIC_LABELS = {'submit', 'continue', 'ok', 'okay', 'yes', 'no', 'click here'}
OPTION_ROLES = {'radio', 'option', 'tab', 'switch', 'menuitemradio', 'menuitemcheckbox', 'checkbox'}
OPTION_GROUP_ROLES = {'radiogroup', 'listbox', 'tablist', 'group', 'toolbar'}


def is_option_control(n):
    """A choice inside a set (rating scale, segmented control, tab) is not a call to action."""
    if str(n.attrs.get('role', '')).lower() in OPTION_ROLES:
        return True
    if any(k in n.attrs for k in ('aria-pressed', 'aria-checked', 'aria-selected')):
        return True
    for a in n.ancestors(3):
        if str(a.attrs.get('role', '')).lower() in OPTION_GROUP_ROLES or a.ltag == 'fieldset':
            return True
    return False


def check_generic_cta(u, out):
    for n in u.nodes:
        label = None
        if is_option_control(n):
            continue
        if n.ltag == 'button' or n.attrs.get('role') == 'button' or (n.ltag == 'a' and re.search(r'btn|button|cta', ' '.join(n.classes), re.I)):
            label = n.text()
        elif n.ltag == 'input' and str(n.attrs.get('type', '')).lower() in ('submit', 'button'):
            label = n.attrs.get('value') if isinstance(n.attrs.get('value'), str) else 'Submit'
        if not label:
            continue
        clean = re.sub(r'[^\w\s]', '', EMOJI_RE.sub('', label)).strip().lower()
        if clean in GENERIC_LABELS:
            out.add('generic-cta-label', n.sf, n.start, 'button labelled "%s"' % label.strip())


# ---- headlines -------------------------------------------------------------------------

INLINE_TAGS = {'span', 'em', 'i', 'mark', 'strong', 'b', 'u', 's', 'font', 'small', 'sup'}
ACCENT_CLASS_RE = re.compile(r'gradient|accent|highlight|italic|serif|underline|text-transparent|bg-clip-text|clip-text|'
                             r'^text-(?:' + '|'.join(p for p in TW_PALETTE if p not in TW_NEUTRAL) + r')-\d|'
                             r'^text-(?:primary|brand|accent|secondary)$|^font-(?:serif|display)$|marker|squiggle|scribble',
                             re.I)


def accent_runs(u, h):
    """Inline runs inside a heading styled as a second voice: italic/serif/gradient/highlight or a saturated colour.
    Muted grey spans (version numbers, counts) are not accents."""
    ht = h.text()
    if not ht or len(ht) > 140:
        return []
    runs = []
    for d in h.descendants(4):
        if d.ltag not in INLINE_TAGS and not d.is_component:
            continue
        t = d.text()
        if not t or t == ht or not re.search(r'[A-Za-z]{2}', t):
            continue
        why = None
        if d.ltag in ('em', 'i', 'mark', 'u'):
            why = '<%s>' % d.ltag
        if not why:
            for c in d.classes:
                base = tw_split(c)[1]
                if ACCENT_CLASS_RE.search(base):
                    why = 'class "%s"' % c
                    break
                tc = tw_color(base)
                if tc and tc[0] == 'text' and tc[1] is not None and is_saturated(tc[1], 0.3):
                    why = 'class "%s"' % c
                    break
        if not why:
            for dd in d.inline_decls + u.decls_for(d, rules_only=True):
                if dd.prop in ('background-image', 'background-clip', '-webkit-background-clip',
                               '-webkit-text-fill-color', 'font-family') or \
                        (dd.prop == 'font-style' and 'italic' in dd.value) or \
                        (dd.prop == 'background' and 'gradient(' in dd.value):
                    why = 'CSS %s' % dd.prop
                    break
                if dd.prop in ('color', 'text-decoration-color', 'background', 'background-color') and \
                        any(is_saturated(c, 0.3) for c in u.colors(dd.value)):
                    why = 'CSS %s' % dd.prop
                    break
        if why:
            runs.append((d, why, t))
    return runs


def is_centered(u, node):
    for a in [node] + node.ancestors(4):
        allb = u.tw(a)
        if any(b == 'text-center' and not v for v, b in allb) and not any(
                b in ('text-left', 'text-start') and v and v[-1] in ('sm', 'md', 'lg', 'xl', '2xl') for v, b in allb):
            return True
        d = u.last_decl(a, 'text-align')
        if d is not None and 'center' in d.value:
            return True
    return False


def check_headlines(u, out):
    for sf in u.markup_files():
        first_h1 = True
        for n in sf.nodes:
            if n.ltag not in ('h1', 'h2'):
                continue
            runs = accent_runs(u, n)
            if n.ltag == 'h1' and first_h1:
                first_h1 = False
                if runs and is_centered(u, n):
                    out.add('hero-centered-two-tone', sf, n.start, 'centred h1 with an accent run (%s on "%s")'
                            % (runs[0][1], shorten(runs[0][2], 30)))
                    continue
            if runs:
                out.add('headline-accent-word', sf, runs[0][0].start, '<%s> accent run (%s): "%s"'
                        % (n.ltag, runs[0][1], shorten(runs[0][2], 40)))


# ---- vanity metrics ---------------------------------------------------------------------

METRIC_RE = re.compile(r'^[$€£¥]?\d[\d.,]*\s?(?:%|x|×|k|K|M|B|\+|K\+|M\+|B\+|k\+|ms|s|h|/5|/10|★)?\+?$|^24/7$')


def is_vanity_number(t):
    """A bare count like 01 or 7 is not a stat; 10K+, 99.9%, 4.9/5, 3x, 2,000, 650 are."""
    if re.match(r'^0\d$', t):
        return False
    digits = re.sub(r'\D', '', t)
    return bool(re.search(r'[%x×kKMB+/★]|ms$|\.\d|,\d', t)) or len(digits) >= 3


def _first_text(n):
    for c in n.children:
        if isinstance(c, TextSeg):
            if c.clean.strip() and not c.in_code():
                return c.clean.strip()
        elif c.ltag not in CODE_TAGS:
            t = _first_text(c)
            if t:
                return t
    return None


TABLE_TAGS = {'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th', 'colgroup'}


def check_vanity(u, out):
    for sf in u.markup_files():
        for p in sf.nodes:
            kids = p.elem_children()
            if len(kids) < 3:
                continue
            # rows of a data table (account codes, years, IDs) are data, not a stat strip
            if p.ltag in TABLE_TAGS or any(k.ltag in TABLE_TAGS for k in kids) or any(
                    a.ltag in TABLE_TAGS for a in p.ancestors(4)):
                continue
            vals = []
            for k in kids:
                t = _first_text(k)
                if t and len(t) <= 10 and METRIC_RE.match(t) and is_vanity_number(t):
                    vals.append(t)
            if len(vals) >= 3 and not all(re.match(r'^[$€£¥]', v) for v in vals):
                out.add('vanity-metrics', sf, p.start, 'stat strip: %s' % ', '.join(vals[:5]))
                sf.markers.setdefault('stat strip', p.start)
    for sf in u.files:
        for (a, b) in sf.js_regions:
            ms = list(re.finditer(r'\b(value|stat|number|metric|figure|count|amount)\s*:\s*["\'`]([$€£]?\d[\d.,]*\s?(?:%|x|k|K|M|B|\+|ms)\+?)["\'`]', sf.text[a:b]))
            if len(ms) >= 3:
                out.add('vanity-metrics', sf, a + ms[0].start(), 'stat data: %s' % ', '.join(m.group(2) for m in ms[:5]))
                sf.markers.setdefault('stat strip', a + ms[0].start())


# ---- cream + terracotta -----------------------------------------------------------------

SPENT_GROUNDS = ('#f4f1ea', '#f5f1ea', '#f7f5f1', '#faf7f1')
SPENT_ACCENTS = ('#d97757', '#b6553a', '#9a2436')
SEMANTIC_CTX_RE = re.compile(r'danger|error|warn|destructive|alert|negative|invalid|critical|success|positive', re.I)


def is_warm_light_ground(c):
    """Cream, ivory, greige, oatmeal: light (OKLCH L >= 0.88), barely to softly tinted, on the warm side."""
    if c is None or c[3] < 0.9:
        return False
    L, C, H = rgb_to_oklch(c)
    return L >= 0.88 and 0.004 <= C <= 0.06 and 30 <= H <= 100


def is_clay_accent(c):
    """Terracotta, rust, brick and oxblood: mid lightness, real chroma, red-orange hues."""
    if c is None or c[3] < 0.5:
        return False
    L, C, H = rgb_to_oklch(c)
    return 0.35 <= L <= 0.72 and C >= 0.08 and (10 <= H <= 52)


def _okfmt(c):
    L, C, H = rgb_to_oklch(c)
    return 'oklch(%.2f %.3f %.0f)' % (L, C, H)


def check_cream(u, out, fams):
    cream = None
    terra = None
    for d in u.all_decls():
        bgctx = d.prop in ('background', 'background-color') or (d.prop.startswith('--') and re.search(
            r'bg|background|canvas|surface|paper|cream|base|page|ground', d.prop))
        semantic = SEMANTIC_CTX_RE.search(d.prop) or SEMANTIC_CTX_RE.search(d.selector or '')
        for c in u.colors(d.value):
            if bgctx and cream is None and is_warm_light_ground(c):
                cream = (d.sf, d.off, c)
            if terra is None and not semantic and (is_clay_accent(c) or (
                    (hls_deg(c)[0] >= 340 or hls_deg(c)[0] <= 2) and 0.2 <= hls_deg(c)[1] <= 0.45 and
                    hls_deg(c)[2] >= 0.4)):
                terra = (d.sf, d.off, c)
    for n in u.nodes:
        for v, b in n.tw():
            c = tw_color(b)
            if c and c[1] is not None:
                if c[0] == 'bg' and cream is None and is_warm_light_ground(c[1]):
                    cream = (n.sf, n.start, c[1])
                if terra is None and is_clay_accent(c[1]):
                    terra = (n.sf, n.start, c[1])
    if cream and terra:
        serif = [f for f in fams if re.search(r'serif|garamond|caslon|baskerville|fraunces|playfair|newsreader|'
                                               r'instrument serif|tiempos|canela|editorial', f) and 'sans' not in f]
        dg = min((delta_ok(cream[2], parse_color(h)), h) for h in SPENT_GROUNDS)
        da = min((delta_ok(terra[2], parse_color(h)), h) for h in SPENT_ACCENTS)
        out.add('cream-terracotta', cream[0], cream[1], 'warm light ground %s + clay/brick accent %s%s; nearest '
                'spent values: ground %s (dE_ok %.2f), accent %s (dE_ok %.2f). Renaming the tones does not move them'
                % (_okfmt(cream[2]), _okfmt(terra[2]), (' + serif display (%s)' % serif[0]) if serif else '',
                   dg[1], dg[0], da[1], da[0]))


# ---- headline voice, fixture faces, native controls, item patterns, cadence, commentary, brief echo ------

SYSTEM_STACK = {'-apple-system', 'blinkmacsystemfont', 'system-ui', 'ui-sans-serif'}
TW_WEIGHT_RE = re.compile(r'^font-(thin|extralight|light|normal|medium|semibold|bold|extrabold|black|\[\d+\])$')


def resolved_family(u, node):
    """First family of the font-family that reaches this element (own rules, then ancestors); None if unknown."""
    for n in [node] + node.ancestors(30):
        if u.tailwind and any(b.startswith('font-') and not TW_WEIGHT_RE.match(b) for v, b in n.tw()):
            return None
        fam = None
        for d in u.decls_for(n):
            if d.prop == 'font-family':
                fam = first_family(d.value, u)
            elif d.prop == 'font':
                sh = font_shorthand_family(u.resolve(d.value))
                if sh:
                    fam = first_family(sh, u)
        if fam:
            return None if fam == '?var' else fam
    return None


def check_heading_voice(u, out, fams):
    """[13] names the headline voice: a loaded brand face does not help if the H1 still resolves to a default.
    A web mock of a native app (--surface native on HTML) renders its system-stack titles in whatever the
    stack falls back to off Apple devices, usually Inter or Segoe UI."""
    if SURFACE not in ('marketing', 'native'):
        return
    brand = [f for f in fams if not is_default_font(f) and f not in GENERIC_FAMILIES]
    for sf in u.markup_files():
        if SURFACE == 'native' and sf.ext not in ('.html', '.htm'):
            continue
        tags = ('h1',) if SURFACE == 'marketing' else ('h1', 'h2', 'h3')
        for tag in tags:
            h = next((n for n in sf.nodes if n.ltag == tag and n.text()), None)
            if h is None:
                continue
            fam = resolved_family(u, h)
            if not fam:
                continue
            if SURFACE == 'marketing' and brand and is_default_font(fam):
                out.add('default-font-only', sf, h.start, 'the <h1> resolves to "%s" although %s is loaded: the '
                        'headline voice is still the default' % (fam, ', '.join(brand[:2])))
                return
            if SURFACE == 'native' and fam in SYSTEM_STACK:
                out.add('default-font-only', sf, h.start, 'web mock of a native app: <%s> starts with "%s", so off '
                        'Apple devices it renders in the next family of the stack (often Inter or Segoe UI); set '
                        'titles in a loaded face, or document the stand-in' % (tag, fam))
                return


_FIXTURE_FACES = None


def fixture_faces():
    global _FIXTURE_FACES
    if _FIXTURE_FACES is None:
        _FIXTURE_FACES = {}
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
        try:
            names = sorted(fn for fn in os.listdir(d) if fn.startswith('clean') and fn.endswith('.html'))
        except OSError:
            names = []
        for fn in names:
            t = read_text(os.path.join(d, fn)) or ''
            fams = set()
            for m in re.finditer(r'family=([^&"\'\s]+)', t):
                for fam in m.group(1).split('|'):
                    fams.add(re.split(r'[:@]', fam)[0].replace('+', ' ').strip().lower())
            for m in re.finditer(r'font-family\s*:\s*([^;}]+)', t):
                f = family_list(m.group(1))
                if f:
                    fams.add(f[0].strip().lower())
            for f in fams:
                if f and f not in GENERIC_FAMILIES and not is_default_font(f) and f not in ('georgia',):
                    _FIXTURE_FACES.setdefault(f, fn)
    return _FIXTURE_FACES


def check_fixture_face(u, out):
    fx_dir = os.path.normcase(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures'))
    if any(os.path.normcase(plain_path(sf.path)).startswith(fx_dir) for sf in u.files):
        return
    faces = fixture_faces()
    seen = set()
    for f, kind, sf, off, ctx in gather_fonts(u, []):
        if f in faces and f not in seen:
            seen.add(f)
            out.add('fixture-face', sf, off, '"%s" is the face of the skill fixture %s; it shows a clean result, '
                    'not a face to reuse' % (f, faces[f]))


RANGE_STYLE_RE = re.compile(r'::-webkit-slider-thumb|::-moz-range-thumb|::-webkit-slider-runnable-track|'
                            r'::-moz-range-track|::-ms-thumb', re.I)


def check_native_controls(u, out):
    ranges = [n for n in u.nodes if n.ltag == 'input' and str(n.attrs.get('type', '')).lower() == 'range']
    if not ranges:
        return
    styled = any(RANGE_STYLE_RE.search(r.selector or '') for r in u.rules if r.kind == 'rule')
    if not styled:
        styled = any(RANGE_STYLE_RE.search(sf.text) for sf in u.files if sf.css_regions)
    if not styled:
        n = ranges[0]
        out.add('native-control-default', n.sf, n.start, '%d range input(s) with no thumb or track styling: the '
                'browser default (pill track, round thumb) ships as the control' % len(ranges))


TITLE_TAGS = {'h3', 'h4', 'h5', 'h6', 'dt', 'strong', 'b'}
ITEM_TITLE_CLASS_RE = re.compile(r'(^|[-_])(title|heading|headline|name|term)($|[-_])', re.I)


def title_blurb(item):
    """A short title (8 words or fewer) plus 6-60 words of blurb: the feature-card shape, icon or not."""
    words = len(item.text().split())
    if words < 8 or words > 70:
        return False
    for d in item.descendants(3):
        if d.ltag in TITLE_TAGS or any(ITEM_TITLE_CLASS_RE.search(c) for c in d.classes):
            t = d.text()
            if t and len(t.split()) <= 8:
                return 6 <= words - len(t.split()) <= 60
    return False


def item_list(p):
    """Number of title + blurb items directly under p (dl dt/dd pairs count as items), else 0."""
    kids = p.elem_children()
    if p.ltag == 'dl' and kids and all(k.ltag in ('dt', 'dd') for k in kids):
        pairs = 0
        for i, k in enumerate(kids[:-1]):
            if k.ltag == 'dt' and kids[i + 1].ltag == 'dd':
                tw = len(k.text().split())
                dw = len(kids[i + 1].text().split())
                if 1 <= tw <= 8 and 6 <= dw <= 60:
                    pairs += 1
        return pairs if pairs >= 3 else 0
    if len(kids) < 3:
        return 0
    hits = sum(1 for k in kids if title_blurb(k))
    return hits if hits >= 3 and hits >= 0.75 * len(kids) else 0


def is_grid_parent(u, p):
    for v, b in u.tw(p):
        m = re.match(r'^grid-cols-([2-6])$', b)
        if m:
            return True
    for d in u.decls_for(p):
        if d.prop == 'grid-template-columns':
            val = u.resolve(d.value).strip()
            if re.search(r'repeat\(\s*(auto-fit|auto-fill|[2-9])', val):
                return True
            if len([t for t in split_top(val, ' ') if t.strip()]) >= 2:
                return True
    return False


def check_item_patterns(u, out):
    if SURFACE != 'marketing':
        return  # settings rows and inspector lists repeat title + description by design
    for sf in u.markup_files():
        h2s = [n for n in sf.nodes if n.ltag == 'h2']
        sections = OrderedDict()
        for p in sf.nodes:
            if p.ltag in ('nav', 'footer', 'table', 'form', 'figure') or any(
                    a.ltag in ('nav', 'footer', 'table', 'form', 'figure') for a in p.ancestors(12)):
                continue
            n_items = item_list(p)
            if not n_items:
                continue
            if n_items >= 4 and is_grid_parent(u, p):
                out.add('uniform-item-grid', sf, p.start, 'a grid of %d title + blurb items (%s)' % (n_items, p.ctx().strip()))
            sec = next((a for a in [p] + p.ancestors(12) if a.ltag in ('section', 'article')), None)
            if sec is not None:
                key = ('sec', sec.start)
                label = sec.id or ' '.join(sec.classes[:1]) or 'section@%d' % sf.line_of(sec.start)
            else:
                prev = [h for h in h2s if h.start < p.start]
                key = ('h2', prev[-1].start if prev else -1)
                label = shorten(prev[-1].text(), 30) if prev else '(top)'
            sections.setdefault(key, (p, label))
        if len(sections) >= 3:
            first = list(sections.values())[0][0]
            out.add('repeated-item-pattern', sf, first.start, 'title + blurb lists in %d sections: %s' % (
                len(sections), ', '.join(v[1] for v in list(sections.values())[:5])))


def check_heading_cadence(u, out):
    for sf in u.markup_files():
        heads = [n for n in sf.nodes if n.ltag in ('h1', 'h2') and len(n.text().split()) >= 3]
        if len(heads) < 5:
            continue
        stops = [h for h in heads if re.search(r'\.[\u2019\u201d"\')]*$', h.text().strip())]
        if len(stops) >= 0.8 * len(heads):
            out.add('heading-cadence', sf, heads[0].start, '%d of %d headings are full-stop declaratives ("%s")'
                    % (len(stops), len(heads), shorten(stops[0].text(), 50)))


COMMENT_RE = re.compile(r'<!--(.*?)-->|/\*(.*?)\*/', re.S)
SPEC_MARKERS = [r'\bthesis\b', r'reference world', r'signature move', r'direction cards?', r'values to confirm',
                r'\brejected\b', r'\boverrides\s*:', r"\bdon'?t\s*:", r'\bdesign\.md\b']


def check_design_commentary(u, out):
    for sf in u.files:
        if not sf.is_doc and sf.ext not in MARKUP_EXTS:
            continue
        for m in COMMENT_RE.finditer(sf.text):
            body = m.group(1) or m.group(2) or ''
            if len(body) < 200:
                continue
            hits = sum(1 for rx in SPEC_MARKERS if re.search(rx, body, re.I))
            if hits >= 3:
                out.add('design-commentary', sf, m.start(), 'a %d-line comment reads like DESIGN.md (%d spec '
                        'markers) and ships to every visitor in view-source' % (body.count('\n') + 1, hits))
                break


BRIEF_TEXT = None
STOP = {'a', 'an', 'the', 'and', 'or', 'of', 'to', 'in', 'on', 'for', 'with', 'by', 'at', 'is', 'are', 'it',
        'its', 'be', 'as', 'that', 'this', 'from', 'who', 'we', 'our', 'you', 'your', 'their', 'they', 'not'}


def _words(t):
    return re.findall(r"[a-z0-9]+(?:['\u2019][a-z]+)?", t.lower().replace('\u2019', "'"))


def check_brief_echo(u, out):
    if not BRIEF_TEXT:
        return
    bw = _words(BRIEF_TEXT)
    grams = set(tuple(bw[i:i + 5]) for i in range(len(bw) - 4))
    if not grams:
        return
    for sf in u.markup_files():
        brand = brand_words(sf)
        hits = []
        for clean, raw, off, ctx in sf.copy:
            w = _words(clean)
            i = 0
            while i <= len(w) - 5:
                g = tuple(w[i:i + 5])
                content = [x for x in g if x not in STOP and x not in brand]
                if g in grams and len(content) >= 2:
                    j = i + 5
                    while j < len(w) and tuple(w[j - 4:j + 1]) in grams:
                        j += 1
                    hits.append((off, ' '.join(w[i:j])))
                    i = j
                else:
                    i += 1
        for off, phrase in hits[:3]:
            out.add('brief-echo', sf, off, 'copied from the brief: "%s"' % shorten(phrase, 70))


# ---- spent looks beyond purple and cream, and craft-floor rules ---------------------------

APPLE_HEXES = ('#f5f5f7', '#1d1d1f', '#6e6e73', '#0066cc', '#0071e3', '#2997ff')
APPLE_HEX_RE = re.compile(r'(?<![0-9a-fA-F])(' + '|'.join(h[1:] for h in APPLE_HEXES) + r')(?![0-9a-fA-F])', re.I)
NEUTRAL_DARK_TW = re.compile(r'^bg-(black|(gray|slate|zinc|neutral|stone)-950|\[#0[0-9a-f]{5}\]|\[#1[01][0-9a-f]{4}\])$', re.I)
NEON_TW = {'emerald', 'green', 'lime'}
BLACK_PILL_TW = re.compile(r'^bg-(black|(gray|slate|zinc|neutral|stone)-(800|900|950)|\[#[0-2][0-9a-f]{5}\])$', re.I)
LIGHT_GROUND_TW = re.compile(r'^bg-(white|(gray|slate|zinc|neutral|stone)-(50|100))$')
MONO_TW = 'font-mono'


def _page_node(n, bases):
    return n.ltag in ('html', 'body') or any(b in ('min-h-screen', 'min-h-dvh', 'min-h-svh', 'h-screen', 'h-dvh')
                                              for b in bases)


def _themed(d):
    return any('prefers-color-scheme' in m for m in (d.media or [])) or \
        bool(re.search(r'\.dark\b|data-theme|data-mode', d.selector or ''))


def is_near_black(c):
    if c is None or c[3] < 0.9:
        return False
    h, l, s = hls_deg(c)
    return l <= 0.09 and chroma(c) <= 0.03


def is_neon(c):
    if c is None or c[3] < 0.5:
        return False
    h, l, s = hls_deg(c)
    return s > 0.6 and chroma(c) >= 0.5 and (75 <= h <= 165 or 5 <= h <= 20)


def page_grounds(u):
    """Colours declared for the page ground: page selectors, --background-style tokens, Tailwind body classes."""
    grounds = []
    for d in u.all_decls():
        if _themed(d) or any('prefers-contrast' in m for m in (d.media or [])):
            continue
        if d.prop in ('background', 'background-color'):
            sel = d.selector or ''
            page = any(p.strip() in PAGE_SEL for p in split_top(sel, ',')) or (
                d.node is not None and d.node.ltag in ('html', 'body'))
            if page:
                cols = u.colors(d.value)
                if cols:
                    grounds.append((cols[0], d.sf, d.off))
        elif d.prop.startswith('--') and BG_TOKEN_RE.match(d.prop):
            cols = u.colors(d.value)
            if cols:
                grounds.append((cols[0], d.sf, d.off))
    for n in u.nodes:
        bases = [b for v, b in n.tw() if not v]
        if not _page_node(n, bases):
            continue
        for b in bases:
            if NEUTRAL_DARK_TW.match(b):
                grounds.append(((10, 10, 10, 1.0), n.sf, n.start))
            elif LIGHT_GROUND_TW.match(b):
                grounds.append(((250, 250, 250, 1.0), n.sf, n.start))
            else:
                c = tw_color(b)
                if c and c[0] == 'bg' and c[1] is not None:
                    grounds.append((c[1], n.sf, n.start))
    return grounds


def check_extra(u, out):
    # transition: all [1★ Vercel]
    for d in u.all_decls():
        if d.prop == 'transition' and any(p.split() and p.split()[0].lower() == 'all' for p in split_top(d.value, ',')):
            out.add('transition-all', d.sf, d.off, 'transition: %s' % shorten(d.value, 50))
        elif d.prop == 'transition-property' and re.match(r'^\s*all\b', d.value):
            out.add('transition-all', d.sf, d.off, 'transition-property: all')
    for n in u.nodes:
        if any(b == 'transition-all' for v, b in n.tw()):
            out.add('transition-all', n.sf, n.start, 'Tailwind transition-all on <%s>' % n.tag)
    # zoom disabled [1★ Vercel]
    for sf in u.files:
        for m in re.finditer(r'<meta\b[^>]*\bname=["\']viewport["\'][^>]*>', sf.text, re.I):
            if re.search(r'user-scalable\s*=\s*(no|0)\b|maximum-scale\s*=\s*1(\.0*)?(?![.\d])', m.group(0), re.I):
                out.add('zoom-disabled', sf, m.start(), 'viewport meta disables zoom')
        for m in re.finditer(r'\buserScalable\s*:\s*false\b|\bmaximumScale\s*:\s*1(?![.\d])', sf.text):
            out.add('zoom-disabled', sf, m.start(), 'viewport config disables zoom (%s)' % m.group(0))
    # outline removed with no focus-visible replacement [2]
    replacement = any(re.search(r':focus-visible|focus-visible:|focus:ring|focus:shadow|focus:border|'
                                r'focus-within:ring', sf.text) for sf in u.files)
    if not replacement:
        for d in u.all_decls():
            if d.prop in ('outline', 'outline-style') and re.match(r'^\s*(none|0)\b', d.value):
                out.add('outline-removed', d.sf, d.off, '%s: %s on %s' % (d.prop, d.value.strip(),
                                                                       shorten(d.selector or 'inline style', 40)))
        for n in u.nodes:
            if any(b in ('outline-none', 'outline-0') for v, b in n.tw()):
                out.add('outline-removed', n.sf, n.start, 'Tailwind outline-none on <%s>' % n.tag)
    # hero sized with h-screen / height: 100vh [3]
    for n in u.nodes:
        if any(b == 'h-screen' for v, b in n.tw()) and (
                n.ltag in ('section', 'header') or re.search(r'hero', n.ctx(), re.I)):
            out.add('hero-h-screen', n.sf, n.start, 'h-screen on <%s>' % n.tag)
    for r in u.rules:
        if r.kind == 'rule' and re.search(r'hero', r.selector, re.I):
            for d in r.decls:
                if d.prop == 'height' and re.match(r'^\s*100vh\s*$', d.value):
                    out.add('hero-h-screen', d.sf, d.off, 'height: 100vh on %s' % shorten(r.selector, 40))
    # apple.com tokens copied as the palette (synthesis)
    found = OrderedDict()
    for sf in u.files:
        for m in APPLE_HEX_RE.finditer(sf.text):
            found.setdefault(m.group(1).lower(), (sf, m.start()))
    if len(found) >= 3:
        sf, off = min(found.values(), key=lambda x: (x[0].path, x[1]))
        out.add('apple-tokens', sf, off, '%d apple.com values in use: %s' % (len(found), ', '.join('#' + k for k in found)))
    grounds = page_grounds(u)
    # near-black + one neon accent [2]
    dark = [g for g in grounds if is_near_black(g[0])]
    if dark:
        neon = None
        for d in u.all_decls():
            if _themed(d) or re.search(r'error|danger|destructive|success|warning|valid', d.selector or '', re.I):
                continue
            tok = d.prop.startswith('--') and BRAND_TOKEN_RE.match(d.prop)
            cta = d.prop in ('background', 'background-color', 'color', 'border-color') and (
                CTA_CTX_RE.search(d.selector or '') or (d.node is not None and is_cta_node(u, d.node)))
            if (tok or cta) and any(is_neon(c) for c in u.colors(d.value)):
                neon = (d.sf, d.off, d.prop if tok else shorten(d.selector or '', 30))
                break
        if neon is None:
            for n in u.nodes:
                if not (is_cta_node(u, n) or re.search(r'badge|pill|chip|step|numeral|highlight|featured|popular|accent',
                                                       n.ctx(), re.I)):
                    continue
                for v, b in n.tw():
                    c = tw_color(b)
                    if c and c[0] in ('bg', 'text', 'border') and ((c[2] in NEON_TW and (c[3] or 0) >= 400) or
                                                                  (c[1] is not None and is_neon(c[1]))):
                        neon = (n.sf, n.start, b)
                        break
                if neon:
                    break
        if neon:
            out.add('near-black-neon', dark[0][1], dark[0][2], 'near-black ground with a neon accent (%s)' % neon[2])
    # grey trend-minimal + black pill [3]
    light = [g for g in grounds if hls_deg(g[0])[1] >= 0.9 and chroma(g[0]) <= 0.03 and g[0][3] >= 0.9]
    if light and not dark:
        chromatic = False
        for d in u.all_decls():
            if d.prop in COLOR_PROPS or (d.prop.startswith('--') and not DATA_TOKEN_RE.search(d.prop)):
                for c in u.colors(d.value):
                    if is_saturated(c) and hue_family(c) not in ('red', 'amber', 'green'):
                        chromatic = True
                        break
            if chromatic:
                break
        if not chromatic:
            for n in u.nodes:
                for v, b in n.tw():
                    c = tw_color(b)
                    if c and ((c[2] and c[2] not in TW_NEUTRAL and TW_FAMILY.get(c[2]) not in ('red', 'amber', 'green')
                               and (c[3] or 0) >= 400) or (c[1] is not None and is_saturated(c[1]) and
                                                           hue_family(c[1]) not in ('red', 'amber', 'green'))):
                        chromatic = True
                        break
                if chromatic:
                    break
        photos = sum(1 for n in u.nodes if n.ltag in ('img', 'video', 'picture') and
                     not re.search(r'\.svg\b|logo|icon|avatar', str(n.attrs.get('src', '')) + n.ctx(), re.I))
        pill = None
        if not chromatic and photos < 2:
            for n in u.nodes:
                bases = set(b for v, b in n.tw() if not v)
                if not (is_cta_node(u, n) or (n.ltag == 'a' and (re.search(r'btn|button|cta', n.ctx(), re.I) or any(
                        re.match(r'^p[xy]-', b) for b in bases)))):
                    continue
                if 'rounded-full' in bases and any(BLACK_PILL_TW.match(b) for b in bases):
                    pill = n
                    break
                decls = u.decls_for(n)
                rad = [x for x in decls if x.prop == 'border-radius']
                bg = [x for x in decls if x.prop in ('background', 'background-color')]
                if rad and bg:
                    px = parse_len_px(rad[-1].value.split()[0]) if rad[-1].value.split() else None
                    cols = u.colors(bg[-1].value)
                    if ((px is not None and px >= 100) or '%' in rad[-1].value) and cols and hls_deg(cols[0])[1] <= 0.15:
                        pill = n
                        break
        if pill is not None:
            out.add('grey-minimal-pill', pill.sf, pill.start,
                    'light neutral canvas, no colour outside status, black pill CTA, %d photo(s)' % photos)
    # broadsheet hairlines [1★ Anthropic]
    radii = []
    for d in u.all_decls():
        if d.prop == 'border-radius' and d.value.split():
            px = parse_len_px(u.resolve(d.value).split()[0])
            if px is not None:
                radii.append(px)
    for n in u.nodes:
        for v, b in n.tw():
            m = re.match(r'^rounded(?:-(none|xs|sm|md|lg|xl|2xl|3xl|4xl|full))?$', b)
            if m:
                radii.append(TW_RADIUS[m.group(1) or ''])
    zero = not radii or sum(1 for r in radii if r < 1) >= 0.9 * len(radii)
    if zero:
        rules = 0
        for d in u.all_decls():
            if re.match(r'^border-(top|bottom|block-start|block-end|block)$', d.prop) and re.search(r'\b1px\b', d.value):
                rules += 1
        for n in u.nodes:
            if n.ltag == 'hr':
                rules += 1
            rules += sum(1 for v, b in n.tw() if not v and b in ('border-t', 'border-b', 'divide-y'))
        caps_mono = 0
        for n in u.nodes:
            bases = set(b for v, b in n.tw() if not v)
            if MONO_TW in bases and 'uppercase' in bases:
                caps_mono += 1
        for r in u.rules:
            if r.kind != 'rule':
                continue
            fam = [d for d in r.decls if d.prop in ('font-family', 'font')]
            if fam and any(MONO_RE.search(d.value) for d in fam) and \
                    any(d.prop == 'text-transform' and 'uppercase' in d.value for d in r.decls):
                caps_mono += 2
        if rules >= 6 and caps_mono >= 2:
            sf = (u.markup_files() or u.files)[0]
            out.add('broadsheet', sf, 0, 'zero radius, %d hairline rules and %d uppercase mono labels' % (rules, caps_mono))


# ---- stock section sequence -------------------------------------------------------------

LOGO_TEXT_RE = re.compile(r'\b(trusted|loved|used|backed|chosen|relied on) by\b[^.\n]{0,60}\b(teams|companies|developers|'
                          r'founders|startups|brands|businesses|customers|creators|users|organi[sz]ations|leaders|the world)\b', re.I)
STEPS_TEXT_RE = re.compile(r'\bhow it works\b|\b(3|three|4|four) (simple|easy|quick) steps\b|\bget started in (3|three)\b', re.I)
TESTI_TEXT_RE = re.compile(r'\btestimonials?\b|\bwhat (our )?(customers|users|clients|people|teams|founders) (are )?say(ing)?\b|'
                           r'\bwall of love\b|\bhear from our\b|\bloved by thousands\b', re.I)
POP_TEXT_RE = re.compile(r'\b(most popular|best value|recommended)\b', re.I)
PRICE_TEXT_RE = re.compile(r'\bpricing\b|/\s?mo(nth)?\b|\bper month\b|\bper seat\b', re.I)
FAQ_TEXT_RE = re.compile(r'\bfrequently asked questions\b|\bFAQs?\b')
CTA_TEXT_RE = re.compile(r'\bready to [^?.!\n]{3,60}\?|\bstart your free trial\b|\bget started (for free|today|now)\b', re.I)


def stock_markers(u, sf):
    mk = OrderedDict(sf.markers)

    def add(label, off):
        mk.setdefault(label, off)
    texts = [(c, o) for c, r, o, x in sf.copy]
    joined = ' '.join(c for c, o in texts)
    for c, o in texts:
        if LOGO_TEXT_RE.search(c):
            add('logo cloud', o)
        if STEPS_TEXT_RE.search(c):
            add('"How it works" steps', o)
        if TESTI_TEXT_RE.search(c):
            add('testimonials', o)
        if FAQ_TEXT_RE.search(c):
            add('FAQ', o)
        if CTA_TEXT_RE.search(c):
            add('"Ready to ...?" CTA strip', o)
        if POP_TEXT_RE.search(c) and PRICE_TEXT_RE.search(joined):
            add('pricing with a highlighted tier', o)
    for n in sf.nodes:
        ctx = ' '.join(n.classes) + ' ' + (n.id or '')
        if re.search(r'announce|promo-?bar|top-?banner|site-?banner|notice-?bar', ctx, re.I):
            add('announcement bar', n.start)
        if re.search(r'logo-?(cloud|wall|strip|grid|bar|row|marquee)|\blogos\b|client-?logos|\btrusted\b', ctx, re.I):
            add('logo cloud', n.start)
        if re.search(r'testimonial', ctx, re.I):
            add('testimonials', n.start)
        if re.search(r'chat-(widget|bubble|button|launcher)|intercom|crisp-client|floating-(chat|button|action)|\bfab\b', ctx, re.I):
            add('floating chat button', n.start)
        if n.ltag in ('section', 'header', 'div') and re.search(r'hero', ctx, re.I):
            bases = set(b for v, b in u.tw(n))
            if any(b.startswith(('bg-gradient-', 'bg-linear-', 'bg-radial')) for b in bases) or any(
                    'gradient(' in d.value for d in u.decls_for(n) if d.prop.startswith('background')):
                add('gradient hero', n.start)
        if n.ltag == 'footer':
            heads = [d for d in n.descendants(6) if d.ltag in ('h2', 'h3', 'h4', 'h5', 'h6')]
            lists = [d for d in n.descendants(4) if d.ltag == 'ul']
            if len(heads) >= 4 or len(lists) >= 4:
                add('4-column footer', n.start)
    for r in u.rules:
        if r.sf is sf and re.search(r'hero', r.selector, re.I) and any('gradient(' in d.value for d in r.decls):
            add('gradient hero', r.off)
    return mk


ROUTE_RE = re.compile(r'(^|/)app/(.+/)?page\.(tsx|jsx|ts|js|mdx)$|(^|/)pages/(?!_app\.|_document\.|api/)[^/].*\.'
                      r'(tsx|jsx|js|mdx|astro|vue)$|(^|/)src/routes/.+\.(tsx|jsx|svelte|astro)$|\+page\.svelte$', re.I)
SHARED_RE = re.compile(r'(^|/)app/(.+/)?layout\.(tsx|jsx|ts|js)$|(^|/)pages/_app\.(tsx|jsx|js)$|\+layout\.svelte$|'
                       r'(^|/)layouts?/[^/]+\.(tsx|jsx|astro|vue|svelte)$', re.I)
IMPORT_RE = re.compile(r'(?:^|[;\n])\s*(?:import|export)\b[^\'";]*?[\'"]([^\'"\n]+)[\'"]|\bimport\(\s*[\'"]([^\'"]+)[\'"]\s*\)')


def _norm(p):
    return os.path.normcase(plain_path(p)).replace('\\', '/')


def _strip_ext(p):
    root, ext = os.path.splitext(p)
    return root if ext.lower() in EXTS else p


def imported_files(sf, index):
    """Files of the unit that sf imports (relative, @/, ~/ and $lib/ specifiers)."""
    out = []
    base_dir = os.path.dirname(plain_path(sf.path))
    for m in IMPORT_RE.finditer(sf.text):
        spec = m.group(1) or m.group(2)
        if not spec:
            continue
        cands = []
        if spec.startswith('.'):
            cands.append(os.path.join(base_dir, spec))
        elif spec.startswith(('@/', '~/', '$lib/')):
            rest = spec.split('/', 1)[1]
            d = base_dir
            for _ in range(8):
                cands += [os.path.join(d, rest), os.path.join(d, 'src', rest), os.path.join(d, 'src', 'lib', rest)]
                nd = os.path.dirname(d)
                if nd == d:
                    break
                d = nd
        for c in cands:
            key = _strip_ext(_norm(os.path.normpath(c)))
            hit = index.get(key) or index.get(key + '/index')
            if hit is not None:
                out.append(hit)
                break
    return out


def check_stock_sequence(u, out, is_app):
    marks = OrderedDict((sf, stock_markers(u, sf)) for sf in u.files)
    flagged = False
    for sf, mk in marks.items():
        if len(mk) >= 5:
            flagged = True
            body = next((n for n in sf.nodes if n.ltag == 'body'), None)
            off = body.start if body is not None else min(mk.values())
            out.add('stock-section-sequence', sf, off, '%d stock blocks: %s' % (len(mk), ', '.join(mk)))
    if not is_app or flagged:
        return

    def pool(files):
        res = OrderedDict()
        for f in files:
            for k, v in marks.get(f, {}).items():
                res.setdefault(k, (f, v))
        return res
    routes = [sf for sf in u.files if ROUTE_RE.search(_norm(sf.path))]
    if routes:
        # One page = its route entry + shared layouts + the components they import (4 levels), never other routes.
        index = {}
        for sf in u.files:
            index[_strip_ext(_norm(sf.path))] = sf
        route_set = set(routes)
        shared = [sf for sf in u.files if SHARED_RE.search(_norm(sf.path))]
        for r in routes:
            seen = OrderedDict((x, True) for x in [r] + shared)
            frontier = list(seen)
            for _ in range(4):
                nxt = []
                for f in frontier:
                    for g in imported_files(f, index):
                        if g not in seen and g not in route_set:
                            seen[g] = True
                            nxt.append(g)
                frontier = nxt
            pooled = pool(seen)
            if len(pooled) >= 5:
                out.add('stock-section-sequence', r, min(v for f, v in pooled.values() if f is r) if any(
                    f is r for f, v in pooled.values()) else 0,
                        '%d stock blocks across this route and the components it imports: %s'
                        % (len(pooled), ', '.join(pooled)), unit_files=[x.display for x in seen])
        return
    pooled = pool(u.files)
    if len(pooled) >= 5:
        files = sorted(set(f for f, v in pooled.values()), key=lambda f: f.path)
        sf, off = min(pooled.values(), key=lambda x: (x[0].path, x[1]))
        out.add('stock-section-sequence', sf, off,
                'possible stock sequence across %d files (no route entry found, so they may be different pages; '
                'scan one page and its components to confirm): %s' % (len(files), ', '.join(pooled)),
                severity='med', unit_files=[x.display for x in u.files])


# --------------------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------------------

def ext_path(p):
    """Absolute path; on Windows add the \\\\?\\ prefix near MAX_PATH so deep trees still walk."""
    p = os.path.abspath(p)
    if os.name == 'nt' and not p.startswith('\\\\?\\') and len(p) >= 200:
        if p.startswith('\\\\'):
            return '\\\\?\\UNC\\' + p[2:]
        return '\\\\?\\' + p
    return p


def plain_path(p):
    if p.startswith('\\\\?\\UNC\\'):
        return '\\\\' + p[8:]
    if p.startswith('\\\\?\\'):
        return p[4:]
    return p


def read_text(path):
    try:
        if os.path.getsize(path) > 3 * 1024 * 1024:
            return None
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except (OSError, IOError):
        return None


def looks_minified(text):
    lines = text.count('\n') + 1
    return len(text) > 20000 and len(text) / lines > 400


SUPPORTED_MSG = 'html, css, scss, sass, less, js, ts, jsx, tsx, vue, svelte, astro'


def collect(args):
    groups = []
    loose = []
    for a0 in args:
        a = ext_path(a0)
        if os.path.isdir(a):
            files = []
            for dp, dns, fns in os.walk(a):
                dns[:] = sorted(d for d in dns if d not in SKIP_DIRS and not d.startswith('.'))
                for fn in sorted(fns):
                    ext = os.path.splitext(fn)[1].lower()
                    if ext in EXTS and '.min.' not in fn.lower() and not fn.endswith('.d.ts'):
                        files.append(os.path.join(dp, fn))
            groups.append((a0, files))
        elif os.path.isfile(a):
            if os.path.splitext(a)[1].lower() not in EXTS:
                raise SystemExit('slop_check: unsupported file type: %s (supported: %s). Web code only; for SwiftUI '
                                 'use the native checks in references/apple-playbook.md section 16.'
                                 % (a0, SUPPORTED_MSG))
            loose.append(a)
        else:
            raise SystemExit('slop_check: no such file or directory: %s' % a0)
    if loose:
        groups.append(('(files)', loose))
    if not any(files for label, files in groups):
        raise SystemExit('slop_check: no supported files (%s) under: %s. Nothing was checked.'
                         % (SUPPORTED_MSG, ', '.join(args)))
    return groups


def run(paths):
    cache = {}

    def get_sf(p):
        ap = ext_path(p)
        if ap in cache:
            return cache[ap]
        t = read_text(ap)
        sf = None if t is None or looks_minified(t) else SourceFile(ap, t)
        cache[ap] = sf
        return sf
    findings = Findings()
    nfiles = set()
    for label, paths_ in collect(paths):
        sfs = [s for s in (get_sf(p) for p in paths_) if s is not None]
        for s in sfs:
            nfiles.add(s.path)
        units = []
        claimed = set()
        group_loaded = []
        for d in [s for s in sfs if s.is_doc]:
            u = Unit(d.display)
            u.add(d)
            for href in LINK_CSS_RE.findall(d.text):
                if re.match(r'^([a-z]+:)?//', href, re.I):
                    continue
                p = ext_path(os.path.join(plain_path(os.path.dirname(d.path)), href.split('?')[0].split('#')[0]))
                s = get_sf(p) if os.path.isfile(p) else None
                if s is not None:
                    u.add(s)
                    claimed.add(s.path)
                    nfiles.add(s.path)
            group_loaded.extend(loaded_fonts_in(d))
            units.append((u, False))
        rest = [s for s in sfs if not s.is_doc and s.path not in claimed]
        if rest:
            u = Unit(label)
            for s in rest:
                u.add(s)
            units.append((u, True))
        for u, is_app in units:
            u.prepare()
            gl = group_loaded if is_app else []
            fams = check_fonts(u, findings, gl, unit_files=[s.display for s in u.files] if is_app else None)
            check_purple(u, findings)
            check_gradient_text(u, findings)
            check_emoji(u, findings)
            check_eyebrow(u, findings)
            check_numbering(u, findings)
            check_glass(u, findings)
            check_radius(u, findings)
            check_side_stripe(u, findings)
            check_glow(u, findings)
            check_ambient_glow(u, findings)
            check_tracking(u, findings)
            check_tracked_caps(u, findings)
            check_body_size(u, findings)
            check_mono(u, findings)
            check_icon_grid(u, findings)
            check_accent_hues(u, findings)
            check_pure_bw(u, findings)
            check_motion(u, findings)
            check_copy(u, findings)
            check_generic_cta(u, findings)
            check_headlines(u, findings)
            check_vanity(u, findings)
            check_cream(u, findings, fams)
            check_heading_voice(u, findings, fams)
            check_fixture_face(u, findings)
            check_native_controls(u, findings)
            check_item_patterns(u, findings)
            check_heading_cadence(u, findings)
            check_design_commentary(u, findings)
            check_brief_echo(u, findings)
            check_extra(u, findings)
            check_stock_sequence(u, findings, is_app)
    file_ignores = {}
    for sf in cache.values():
        if sf is None:
            continue
        ids = set()
        for m in IGNORE_DIRECTIVE_RE.finditer(sf.text):
            ids |= set(x.strip().lower() for x in re.split(r'[,\s]+', m.group(1))
                       if re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', x.strip().lower()))
        if ids:
            unknown = sorted(ids - set(RULES))
            if unknown:
                print('slop_check: warning: unknown rule id(s) in a "slop-check: ignore" directive in %s: %s '
                      '(see --list-rules); they silence nothing' % (sf.display, ', '.join(unknown)), file=sys.stderr)
            file_ignores[sf.display] = ids
    elem_ignores = []
    for sf in cache.values():
        if sf is None:
            continue
        for n in sf.nodes:
            v = n.attrs.get('data-slop-ignore')
            if isinstance(v, str) and v.strip():
                ids = set(x.strip().lower() for x in re.split(r'[,\s]+', v) if x.strip())
                unknown = sorted(ids - set(RULES))
                if unknown:
                    print('slop_check: warning: unknown rule id(s) in data-slop-ignore in %s: %s' % (
                        sf.display, ', '.join(unknown)), file=sys.stderr)
                elem_ignores.append((sf.display, sf.line_of(n.start), sf.line_of(n.end), ids))
    file_ignores['__elements__'] = elem_ignores
    return findings, len(nfiles), file_ignores


def list_rules():
    print('%-26s %-15s %-5s %-34s %s' % ('rule', 'N', 'sev', 'cluster', 'title'))
    for r in sorted(RULES.values(), key=lambda r: -r['weight']):
        print('%-26s %-15s %-5s %-34s %s' % (r['id'], '[%s]' % r['label'], rule_severity(r), r['key'],
                                             r['title']))
    print('[N] = independent creators; [1★ X] = one canonical source; [A3] = Apple-only clustering; [syn] = synthesis. '
          'python slop_check.py --explain <rule> prints a rule\'s heuristics and known false positives.')


def explain_rule(rid):
    """Print the docstring block for one rule (heuristic + known false positives) plus its fix."""
    r = RULES.get(rid)
    if r is None:
        print('slop_check: unknown rule id: %s (see --list-rules)' % rid, file=sys.stderr)
        return 2
    lines = (__doc__ or '').splitlines()
    block = []
    for i, ln in enumerate(lines):
        if ln.startswith(rid + ' '):
            block.append(ln)
            for nxt in lines[i + 1:]:
                if not nxt.startswith(' ') or not nxt.strip():
                    break
                block.append(nxt)
            break
    print('\n'.join(block) if block else '%s [%s] %s' % (rid, r['label'], r['key']))
    print('    severity: %s; title: %s' % (rule_severity(r), r['title']))
    print('    fix: %s' % r['fix'])
    return 0


def print_grouped(shown, all_items, max_items):
    """Default text output: one block per rule (most severe first) with up to 3 example locations."""
    groups = OrderedDict()
    for it in all_items:
        groups.setdefault(it['rule'], []).append(it)
    shown_rules = OrderedDict()
    for it in shown:
        shown_rules.setdefault(it['rule'], True)
    budget = max_items
    for rid in shown_rules:
        g = groups[rid]
        g.sort(key=lambda x: (x['file'], x['line']))
        it0 = g[0]
        nfiles = len(set(x['file'] for x in g))
        print('%-4s [%s] %s: %d finding(s) in %d file(s). %s' % (it0['severity'].upper(), it0['tag'], rid, len(g),
                                                                 nfiles, RULES[rid]['title']))
        print('     fix (%s): %s' % (it0['key'], it0['fix']))
        ex = g[:min(3, max(1, budget))] if budget > 0 else []
        for it in ex:
            print('     %s:%d  %s' % (it['file'], it['line'], it['message']))
            print('       > %s' % it['snippet'])
        budget -= len(ex)
        rest = g[len(ex):]
        if rest:
            print('     ...and %d more in %d file(s) (--all lists every one)'
                  % (len(rest), len(set(x['file'] for x in rest))))


IGNORE_DIRECTIVE_RE = re.compile(r'slop-check:\s*ignore\s+([a-z][a-z0-9, \t-]*)', re.I)


def main(argv=None):
    global SURFACE
    ap = argparse.ArgumentParser(
        description='Flag AI-design tells (premium-design skill). Exit 1 if any high-severity finding, 2 on usage '
                    'error or when no supported file was found.',
        epilog='Deliberate exceptions: --ignore rule-a,rule-b for the run; data-slop-ignore="rule-a rule-b" on an '
               'element for findings inside that element only; or a comment containing "slop-check: ignore rule-a, '
               'rule-b" inside a file to silence those rules for the whole file. A pooled finding '
               '(stock-section-sequence or default-font-only derived from several files) is silenced by a directive '
               'in any of the files it was derived from.')
    ap.add_argument('paths', nargs='*', help='files or directories')
    ap.add_argument('--surface', choices=SURFACES, default='marketing',
                    help='surface type pinned in the brief (SKILL.md section 6); product, dashboard and native '
                         'allow one neutral sans, 13-15px UI text and status badges over titles (default: marketing)')
    ap.add_argument('--json', action='store_true', help='machine-readable output')
    ap.add_argument('--min-severity', choices=['low', 'med', 'high'], default='low', help='hide findings below this')
    ap.add_argument('--max', type=int, default=40, metavar='N',
                    help='print at most N example locations in total, 3 per rule (default 40)')
    ap.add_argument('--all', action='store_true', help='list every finding individually, uncapped')
    ap.add_argument('--ignore', default='', help='comma-separated rule ids to skip')
    ap.add_argument('--brief', metavar='FILE', help='the brief as a text file: flags visible copy pasted from it '
                                                     '(brief-echo)')
    ap.add_argument('--list-rules', action='store_true', help='print the rule table and exit')
    ap.add_argument('--explain', metavar='RULE', help='print one rule\'s heuristics, known false positives and fix')
    a = ap.parse_args(argv)
    try:
        if sys.stdout.isatty():
            sys.stdout.reconfigure(errors='backslashreplace')
        else:
            sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    except Exception:
        pass
    if a.list_rules:
        list_rules()
        return 0
    if a.explain:
        return explain_rule(a.explain.strip())
    if not a.paths:
        ap.print_usage()
        return 2
    SURFACE = a.surface
    global BRIEF_TEXT
    if a.brief:
        BRIEF_TEXT = read_text(ext_path(a.brief))
        if BRIEF_TEXT is None:
            print('slop_check: cannot read --brief file %s' % a.brief, file=sys.stderr)
            return 2
    ignore = set(x.strip() for x in a.ignore.split(',') if x.strip())
    unknown = ignore - set(RULES)
    if unknown:
        print('slop_check: unknown rule id(s) in --ignore: %s (see --list-rules)' % ', '.join(sorted(unknown)),
              file=sys.stderr)
        return 2
    try:
        findings, nfiles, file_ignores = run(a.paths)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    elem_ignores = file_ignores.pop('__elements__', [])

    def keep(it):
        if it['rule'] in ignore or it['rule'] in file_ignores.get(it['file'], ()):
            return False
        if any(f == it['file'] and a <= it['line'] <= b and it['rule'] in ids for f, a, b, ids in elem_ignores):
            return False
        return not any(it['rule'] in file_ignores.get(f, ()) for f in it.get('unit_files') or ())
    all_items = [it for it in findings.results(cap=0) if keep(it)]
    items = [it for it in findings.results(cap=0 if a.all else 5) if keep(it)]
    counts = Counter(it['severity'] for it in all_items)
    has_high = counts['high'] > 0
    shown = [it for it in items if SEV_ORDER[it['severity']] <= SEV_ORDER[a.min_severity]]
    code = 1 if has_high else 0
    summary = ('slop_check: %d file(s), %d finding(s): %d high, %d med, %d low (surface: %s).%s [N] = independent '
               'creators behind the rule (references/evidence.md).'
               % (nfiles, len(all_items), counts['high'], counts['med'], counts['low'], SURFACE,
                  ' Exit 1: high findings present.' if has_high else ''))
    try:
        if a.json:
            for it in shown:
                it.pop('unit_files', None)
            print(json.dumps({'files_scanned': nfiles, 'surface': SURFACE,
                              'summary': {'high': counts['high'], 'med': counts['med'], 'low': counts['low']},
                              'exit': code, 'findings': shown}, indent=2, ensure_ascii=True))
            return code
        print(summary)
        if a.all:
            fixed = set()
            for it in shown:
                print('%-4s [%s] %s  %s:%d' % (it['severity'].upper(), it['tag'], it['rule'], it['file'], it['line']))
                print('     %s' % it['message'])
                print('     > %s' % it['snippet'])
                if it['rule'] not in fixed:
                    fixed.add(it['rule'])
                    print('     fix (%s): %s' % (it['key'], it['fix']))
        else:
            visible = [it for it in all_items if SEV_ORDER[it['severity']] <= SEV_ORDER[a.min_severity]]
            print_grouped(shown, visible, a.max)
        if shown:
            print(summary)
    except BrokenPipeError:
        try:
            sys.stdout = open(os.devnull, 'w')
        except Exception:
            pass
    return code


if __name__ == '__main__':
    sys.exit(main())
