---
name: premium-design
description: Presence-first rules for websites and app interfaces that read as high-end and do not look AI-generated, via confident display scale, the subject as the hero, type and colour from the brand's own world, deep real content and clean craft, ranked by how many independent creators state each decision. Includes a brief-to-ship workflow, the trope stacks and template sequences that read as generated and their fixes, context switches (marketing, product UI, dashboards, docs, venues, luxury, native iOS/macOS), slop_check.py and render_check.py. Use when building, designing or restyling a website, landing page, app screen, dashboard or component (HTML, CSS, Tailwind, React, SwiftUI), when asked to make UI premium, modern, polished, Apple-like or not AI-looking, to review UI for AI slop, or for a photo-led social sales post (product photo, name, price, order line). Not for other posters or social graphics, packaging, identity or print (blind tests showed it hurt there) or logic or data changes.
---

# Premium design

Built from 63 videos and 49 articles: about 2,650 design decisions, clustered and ranked by how many **independent creators** state each one. `[N]` = N creators; `[1★]` = one canonical source; `(synthesis)` = guidance written for this skill where the research gives no number, including lessons from its own blind A/B tests. Ranking, backers and sources: [references/evidence.md](references/evidence.md).

A clear brief always wins: a pinned font, palette or era is followed exactly [2]. An existing design system, token file or DESIGN.md counts as the brief; work in its gaps and never swap its brand font or palette unless asked. With `frontend-design` loaded, use this skill for presence, numbers and checks; load `dataviz` for charts.

## 1. What premium means here

**Premium = presence + restraint + craft.** Presence: one confident thing at display scale, the subject shown as something worth wanting, an identity drawn from the subject's own world, and content deep enough that an expert in the niche nods. Restraint: one focal point, one accent, nothing that does not earn its place [8]. Craft: spacing, type, contrast and states that hold at every width.

**What reads as AI is a stack, not a choice.** A page reads as generated when three or more moves come from one recognisable kit (italic serif tails + mono micro-labels + roman numerals + grain = "AI editorial luxury"), or when it assembles the category's stock sections in the stock order [14]. One serif, one dark band or one real numbered sequence is not a tell; the kit is. Target 0-1 default patterns per page; in a scan of 1,590 Show HN sites, 46% had 0-1 [5].

**Blandness fails too** (synthesis, blind A/B). Pages that obeyed every rule but picked a utilitarian face, a palette that fought the brief's emotion, a 4.5rem H1 and section heads at 2x body lost all three briefs to rule-free pages with giant names and coveted products, even though those pages were trope-heavy and buggy. The rules below remove defaults; they never cap ambition. If following one would make your page smaller, greyer or safer than the niche's best player, you are misreading it.

## 2. The moves that create presence

Ordered by evidence, except that display scale sits beside whitespace because space only reads as premium with it [3]. In the blind tests, display scale, the subject and depth of content decided "premium" (synthesis); give them the most effort.

**1. Whitespace, earned by strong hierarchy [16][3].** Use 2-3x the space of a standard interface on marketing, editorial and product-story pages: desktop section padding 80-160px [16], a visible gap of 96-160px between sections on one ground (synthesis of [16][14]). Space reads as premium only beside confident type, a real image or product and full-contrast primary text [3]; small grey type floating in emptiness is the grey trend-minimal look [3]. Fix emptiness with scale and contrast, never by adding elements. Whitespace surrounds groups: a column that stops 160px+ above its neighbour is a hole, not air (synthesis).

**2. Display scale [5][4][3].** Size is the strongest hierarchy lever [4]. Every marketing page gets one dramatic jump: display at least 3x body at 1440 (phones 2-2.5x, synthesis), a sentence H1 up to about 6rem [3]. When the name is the star (a house, a launch, a venue), the name itself is the hero visual at 8-15vw, beside or crossing the product, with the specific line under it as a lead at 1.25-1.6x body ([5]; ranges synthesis). Section heads run 2.5-3.5x body and at least 1.5x their lead so they never read as labels (synthesis of [3] dramatic jumps and [2] "not 5x"). H1 at most 2 lines at 1440 and 3 at 320-390 (synthesis). typography.md §3, §10.

**3. Distinctive type that fits [13][10].** Never Inter, Roboto, Arial, Open Sans, Lato, Times or a system default as the headline voice [13]. Audition 3 faces with the real headline at hero size, beside a premium player's page [10]; the most crafted face beats the most on-concept one, and a face drawn for function (cockpit, signage, terminal, forms) reads utilitarian at 70px+ (synthesis). Prefer a structurally classic face in an unexpected context over this season's novelty [4]; the LLM "distinctive" favourites need a written reason [2] (list: typography.md §1). A neutral workhorse is fine for body under a display face with character.

**4. Colour from the brand's emotional world [9][8][4].** Write 1-3 target emotions and derive face, palette, shape and motion from them [8]. Sample the palette from the real subject (its materials, place, packaging) and name tones after it [4]; then neutrals + one accent + semantic states [9], the accent only on action [8]. Temperature follows the emotion: a warm brief (food, hospitality, scent, comfort) stays warm in one specific material (olive oil, brass, smoked oak) and is never flipped cool to look different (synthesis: [8] emotions outrank [2] cross-project variety). Premium reads darker and more muted, not louder [4]; when colour is content, commit it, one hue owning 30-60% of the surface [4]. color.md §1, §9, C18.

**5. The subject is the hero [7][6][5][4].** The real product, place or UI is the biggest thing in the first viewport, about half the canvas or more, cropped or bleeding off an edge [4]. Show it as an object worth wanting, in a scene that carries its promise: smoke around the bottle, plates on the pass, a real terminal session [6]. Few art-directed images [6], graded as one set [6]; at least 2-3 real images on a landing page [5]; cut-outs on a matched sweep for catalogue views [7], one full-bleed scene for hero moments [4]. Hide the hero visual: if the first viewport still works, the visual is too weak [5]. Without photography: section 6. imagery-copy-brand.md §2-3.

**6. Depth of real content [7][5][4].** The headline is specific enough that no competitor could reuse it: put a competitor's name in it, and if it still reads true, rewrite [7]. Get real names, numbers, materials and process before judging any design [4]. Unknown brands keep the information (specs, sourcing, how it wears or performs, limits, what it costs) in scannable modules of 5-9 items [5], not sparse luxury minimalism [2]. Write to the life of owning it [2] and show how it is made [2]. Story and feature heads carry a fact only this product has, not the visitor's literal question (synthesis). Niche facts must be correct: an enthusiast who catches one wrong claim stops believing the house (synthesis). Never invent proof: ratings, logos, quotes, metrics [3].

## 3. Workflow

Scale it: a new site, page or brand runs every step; a new screen in an existing system reads its tokens, then runs 4-7; a restyle runs 1 and 3-7. Unattended (a subagent, a batch run): ask nothing, decide, and list every assumption in the reply (synthesis).

1. **Brief** [8][5]. Write the subject, the audience as it names itself, the page's one job, the surface (section 6) and 1-3 target emotions. Collect real copy and facts [4]; ask at most one question [6]. Commercial facts the page needs but lacks (price, size, delivery, returns) get plausible values listed "to confirm" in the reply; proof is never invented. imagery-copy-brand.md §1, §6.
2. **Direction from the desired layer of the subject's world** [6][4]. Choose the layer the audience covets (the object at its best, the place at its best hour, the craft's finest moment), not its paperwork or instruments (forms, stamps, gauges, batch cards, cockpit displays), which read as admin unless the emotion is precision; records of the craft (trial notes, sourcing, specs) are welcome as content, not as the visual identity (synthesis). Set the bar with this niche's best premium player, not Apple by default [7]. Sketch 3 directions that differ in light/dark, layout and star [6], pick one, write a one-line thesis [6], and push one dominant move through every element [4]. Every word of the product's promise ("smoky", "a way back") must be visible in the first viewport, not only written (synthesis). imagery-copy-brand.md §1, §7.
3. **Tokens** [7][5]. Write DESIGN.md (its own file, or in the reply; never a comment in shipped markup) before any markup; every later value references a token [11][6]:
   ```md
   Thesis: <page kind> for <audience>, <vibe>. Emotions: <1-3>. World: <the desired layer, as art direction>.
   Star: <product | place | name | live UI>. Hero: <scene panel | full-bleed scene | centred product | name at display scale>.
   Type: display <face> (beat <two others> at hero size because ...); text <face>; weights <..>; mono for data only.
   Scale: body 16-17px; lead 1.25-1.6x; section heads 2.5-3.5x; display >=3x body (a starring name 8-15vw).
   Colour: canvas <OKLCH> because <emotion + material>; ink; ink-muted (4.5:1); accent (action only); strategy <restrained | committed | drenched>.
   Space: 4 8 12 16 24 32 48 64 96 128. Radius <sharp | soft> from <world>. Motion <crisp | expo-out | soft>.
   Signature: <one move from the world, 3-4 placements that do a job, one in the first viewport> [4].
   Content: <the 5-8 facts only this product has>; values to confirm: <...>.
   ```
   Full token tables: typography.md §3, color.md §6, layout-spacing-hierarchy.md §4, motion.md §4, components-details.md §8, §10.
4. **Build** [7]. Greyscale structure with real content, then navigation and interaction, then style, each style solving a named problem. Build the hero first and spend the most effort on its visual: the render, the scene, the name (synthesis). Interaction stays conventional; distinctiveness lives in type, colour, imagery, composition and copy [8]. Build every state [3] and every breakpoint [5]. layout-spacing-hierarchy.md §3, §5-8; components-details.md. When it is built, record the presence baseline: display px and display/body ratio at 1440, section-head ratio, the hero visual's share of the first viewport, and the list of content modules (render_check's per-size lines give the display px, body px and hero share) (synthesis).
5. **Render and look** [4]. Run `python3 <skill-dir>/scripts/render_check.py page.html --full --surface <s>` (`python` on Windows) and open the screenshots: first viewports at 320, 390 and 1440, their greyscale blurs, and the whole page at 390 and 1440. Fix every FAIL. Then run `scripts/slop_check.py --surface <s> <files>` for code-level tells (docs, venue and editorial scan as marketing). Both exit codes are floors: pages that passed both still lost on presence (synthesis).
6. **Critique, one dimension per pass** [4]. Fix every finding with a stronger brand-specific move, never a retreat (section 5): no fix may shrink the presence baseline, remove or flatten the hero, thin the content or cool a warm identity; re-run render_check and compare (synthesis; the two-pass variant built on this rule took 4 of 8 first places in the blind test). Presence first: put your 1440 first viewport beside the niche leader's and ask which looks like the house with more taste (synthesis). Then hierarchy (blur at 5/10/20px: one focal point [8]), spacing, type, colour, motion, trope stacks (section 5), copy, and removal: would cutting this cost the user anything? Take one more thing away [8].
7. **Fix and polish** [9][7]. Any one-pass output, your own included, is a draft; budget the last 10-20% for hand polish, then run section 7.

## 4. High-weight rules not covered above

- [14] Space by relationship: 4-16px inside a group (label to input 4-8px), at least 2x that between groups (24-80px), the largest gaps between sections; nothing sits equidistant between two groups.
- [11] Every spacing and size value comes from one scale (4 8 12 16 24 32 48 64 96 128); no one-off values such as `p-[13px]`.
- [11] Track inversely to size: caps labels +0.03 to +0.1em, body 0, h1 -0.02em, display never tighter than -0.04em, nothing negative at 12px or below.
- [11] Animate only when the job fits one sentence (feedback, state, hierarchy, spatial context, story pacing); acknowledge every press at once [7]; ease out with something like `cubic-bezier(0.16, 1, 0.3, 1)`, never linear [4]; move only `transform` and `opacity`; give it a reduced-motion path [4].
- [8] Contrast: body and muted text 4.5:1, large text and control boundaries 3:1, in every state and every shipped appearance; near-black ink, never #000 on #fff [6].
- [8] One dominant focal point per view, at most 2 prominent elements, about 3 deliberate stops, and at most one filled primary action [4].
- [8] Every element earns its place: no decorative wordmarks, stat strips, pill clusters, icon rows, scroll cues or "Live" dots on static content [8][5].
- [8] 9-15 named text styles from one ratio (1.25 from 16px; 1.125-1.2 when dense) [8][7]; web body 16-17px, iOS 17pt; nothing rendered under 12px, SVG labels included [7].
- [8] Interaction stays conventional: logo top-left, nav top or side, sign-in or cart top-right with the primary action, a drawer on mobile, standard forms and checkout.
- [7] One design language on every section (same faces, icons, button style, image grade) [7]; one radius scale, sharp or soft as the reference world suggests, never both in one view [5].
- [7] Align every element to another on a shared axis; one text edge per section; no centred body copy.
- [6] At most two typefaces, from different classes that share a mood [6][7]; mono only for code and data [5]; neutrals tinted toward the accent or the sampled material, one temperature throughout [6][5].

## 5. Trope stacks and template sequences

One item from a row can be a deliberate choice; three from the same row is the look (synthesis). Look for them in the `--full` screenshots, not only in the code.

- **AI editorial luxury** (synthesis from the A/B; parts [4][3]): italic serif tail on every headline [3], tiny tracked mono micro-labels [4][3], roman numerals or 01-04 section numbers [4], "FIG. 1" captions, vertical letterspaced text, grain everywhere (grain alone is fine [3]; here it is costume), hairline rules with zero radius [1★].
- **AI dev-tool** (synthesis; parts [14][7][4]): announcement bar with a version pill, dot-grid hero [1★], an accent-dash eyebrow on every section [7], uppercase mono meta bullets [3], a hand-drawn swoosh under the headline, 01-04 numbered features [4], 3-tier pricing with a dark middle card and a yearly toggle [14], a "+" FAQ accordion [1★], dark closing CTA, an "All systems normal" dot [5]; often warm paper + orange-red + tight grotesk + JetBrains Mono.
- **AI warm craft** [4]: cream + terracotta or oxblood + serif or Didone display, an italic or bilingual kicker on every section, flat vector art where a photo belongs [2], whimsical over-specific copy (synthesis).
- **Purple SaaS** [11]: violet gradients, top-centre glow [3], gradient text [2], glass cards [5], three icon-on-top feature cards [7], an eyebrow pill over the H1 [7], a big-number stat strip [3].
- **Dark + neon** [2]: #0A0A0A-#111 ground, one acid accent, glows, the Linear look copied wholesale [4]. **Grey trend-minimal** [3]: light-grey canvas, small headline, tiny grey text, black pill CTA.
- **This skill's overcorrection** (synthesis): clean, tidy and timid; a cool or green canvas on a warm brief, Bootstrap-blue rectangular CTAs, a functional face as display, paperwork props, a toy-like CSS product. It reads as a booking app.

**Template sequences** [14]. SaaS: announcement bar, pill badge, gradient hero with mock, logo cloud, stat strip, 3 feature cards, "3 steps", testimonials, 3-tier pricing, CTA strip, 4-column footer, chat bubble. DTC product page (synthesis): split hero with price, craft story, feature list, care, centred closing CTA over a delivery/returns grid. Also any section pattern repeated down the page, including one head layout in 3 sections running. Derive sections from this page's content and the visitor's real questions. Refusing the sequence never drops the closing action, the answers to objections, or a buy or pricing module with a real shop's depth: variants, quantity, delivery, returns (synthesis).

**Replace a trope with a brand move, never with blandness** (synthesis; swapping one default for the next fixes nothing [4][2], and slop-free is not the same as characterful [4]):
- Italic tail or accented word: emphasis from size and weight; let the name itself be the display moment.
- Mono micro-labels, eyebrows, numerals: heads that carry a fact only this product has ("Eight hours on skin, smoke last"); mono kept for real data.
- Grain, dot grids, glows: atmosphere from the subject's own material (smoke, steam, the light in the room, the product's finish).
- FIG. captions and spec callouts: captions that tell the buyer something; one drafting convention for drawings.
- Stock pricing grid, closing FAQ: pricing as the product's own spec with a worked example; objections answered beside the module they concern [1★].
- Cream-terracotta: keep the warmth, sample one specific material, change the accent and the face.
- Flat vector art: a lit render or a real photograph.
- A section-scale or display-ratio CHECK: raise the size and rewrite the head as an ownable fact, not a shorter head at the same size.
- Small-text FAIL in a drawing: fewer, larger labels on a larger drawing, never delete the drawing.
- Dead-column CHECK: give the short column its module's visual or next fact, or stack; don't shrink the other column.
- Page too long: cut repeated facts, unasked modules and padding, never modules of substance.

Then run the swap test (could a competitor's logo sit on it?) and the squint test (beside unrelated products, can you tell the domain?) [4], and the similar-prompt test: whatever you would produce for any similar prompt, change [5].

## 6. Context switches

- **Marketing or landing**: everything above at full strength; hero by the star (a product gets a centred hero or a split whose visual owns a full-height scene panel, never floating on the page ground beside a text stack; software gets a left-aligned stack beside real UI); `min-height: 100dvh`; a long page ends on its primary action (synthesis).
- **Product UI**: operational headings and no hero [2]; fixed rem scale with 16px body; motion only for state changes at 150-300ms; empty, loading and error states whose copy is true.
- **Dense dashboard**: gaps 4/8/12/16, type ratio 1.125-1.2, one neutral sans with `tabular-nums`, no 3x jump; the datum users came for is the largest text; chart colours are a separate data set.
- **Docs** (synthesis): no hero; sidebar, on-page contents and search; body 16-17px at 65-75ch; images only where they explain.
- **Local venue** (synthesis): the first viewport answers what, where and when (name, the room or the plates, hours, address, book CTA); a warm palette led by appetite; the menu as typeset HTML; hours as a short table, never a chart.
- **Editorial or luxury**: sharp or soft from the object; a serif display upright and outside the overused pool [3]; never the full category template (Didone caps wordmark + B&W chrome + square black CTA + bottle on a grey sweep): change two of them (synthesis).
- **Native iOS or macOS**: SF through text styles with Dynamic Type, semantic colours, native components, springs; the brand lives in the tint, owned artwork and a few display moments (apple-playbook.md §14-16).
- **"Make it Apple-like"**: the principles (product large on a matched field, one action colour, few words, drastic whitespace), never the costume (SF on the web, Apple blue, Apple taglines); apple-playbook.md §14.
- **No photography** (synthesis): software gets 2-4 faithful renders of its real surfaces with real commands, states and arithmetic in the platform's chrome [6]; a physical product is drawn as a coveted object with true proportions, one light source, material cues and real label type, set in a scene that carries its promise. A lit front elevation beats an isometric build from CSS boxes, which reads as a toy. Say that commissioned photography replaces it (imagery-copy-brand.md §2).
- **Dark theme**: only when the use scene argues for it [4]; a brand-tinted off-black; every ground step survives in dark (color.md §12).
- **Social sales post** (synthesis, one blind test; Instagram, WhatsApp status): one photo of the product at its best fills the canvas (owned, or a generated serving shot checked against real reference photos), and the copy sits on that photo's own empty surface. The display line is the product's name as buyers say it, with the brand's sentence and one facts line under it. A solid order bar holds the channel, the number and the price with its unit. Text 34px or more on a 1080 canvas (the 12px floor at phone size). Render the fixed canvas, not the 320-1440 sweep. Packaging, pack sizes and prices are never invented. Other posters and social graphics, packaging, identity and print stay out of scope (imagery-copy-brand.md §10).

## 7. Pre-ship checklist

- [ ] Presence: beside the niche leader's first viewport at 1440, yours has one display moment at 3x+ body (a starring name at 8-15vw) and the subject as a coveted object in a scene that shows the promise.
- [ ] Identity: from the 1440 first-viewport screenshot alone you can name the reference world; the palette's temperature fits the emotions; the display face won its audition at hero size and actually loads.
- [ ] Depth: every section answers a question the visitor really has, with facts only this product has; niche facts verified; no invented proof; assumed values listed in the reply.
- [ ] Copy: with a competitor's name in it, the H1 becomes false; buttons name their action; no buzzwords, em-dashes or phrases pasted from the brief [4][3].
- [ ] Stacks: at most one item from any row in section 5; no template sequence; the page still ends on its action and keeps a buy or pricing module with real depth.
- [ ] Hierarchy: blurred at 10px, the first fixation is the intended focal point; section heads 2.5x+ body; one filled primary action per view.
- [ ] Space: gaps by relationship and on the scale; no column ends 160px+ above its neighbour; edges sit on shared axes.
- [ ] Type: H1 at most 2 lines at 1440 and 3 at 320-390, broken on phrases (`text-wrap: balance`); body 16-17px; nothing under 12px, SVG labels included; at most 2 families plus mono for data.
- [ ] Colour: one interactive accent; body and muted text 4.5:1+, controls 3:1+, in every state and appearance; muted text is not most of the running copy.
- [ ] Components: hover, focus-visible, active, disabled, loading; 44px targets on coarse pointers; every nav link lands (no duplicate ids); no horizontal scroll at 320-1440.
- [ ] Motion: each motion has a one-sentence job, uses `transform`/`opacity` only and has a reduced-motion path; nothing loops for decoration.
- [ ] Render: `render_check.py` exits 0, every CHECK was looked at in the `--full` screenshots at 390 and 1440, `slop_check.py` reports 0 high findings, and one more thing was removed.

## 8. Reference map

| When | Read |
|---|---|
| Brief, thesis, reference world, signature, copy | [imagery-copy-brand.md](references/imagery-copy-brand.md) §1, §6-8 |
| Display scale, face audition, text styles | [typography.md](references/typography.md) §1, §3, §10, context rules |
| Palette from the world, emotion vs novelty, committed colour, dark | [color.md](references/color.md) §1, §4, §7, §9, §12, C3, C18 |
| Whitespace, hierarchy levers, layout variety, dead columns | [layout-spacing-hierarchy.md](references/layout-spacing-hierarchy.md) §1, §3, §5-6, §9 |
| Hero, imagery, products drawn in code, software renders | [imagery-copy-brand.md](references/imagery-copy-brand.md) §2-3 |
| Photo-led social sales posts (Instagram, WhatsApp) | [imagery-copy-brand.md](references/imagery-copy-brand.md) §10 |
| States, buttons, radius, elevation, forms, charts | [components-details.md](references/components-details.md) |
| Timing, easing, signature motion, scroll stories | [motion.md](references/motion.md) §1, §4, §7-8 |
| Every tell, the looks table, squint and swap tests | [ai-tells.md](references/ai-tells.md) |
| Apple-like, native iOS and macOS | [apple-playbook.md](references/apple-playbook.md) §14-16 |
| Who said what, the top 60, method | [evidence.md](references/evidence.md) |
| Scripts | `scripts/render_check.py --help` (every FAIL and CHECK); `scripts/slop_check.py --list-rules`, `--explain <rule>`; `scripts/fixtures/` shows clean pages, not faces to reuse |
