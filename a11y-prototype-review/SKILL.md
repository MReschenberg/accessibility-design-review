---
name: a11y-prototype-review
description: Performs an accessibility (a11y) review of a live, interactive prototype or deployed website on behalf of the Mozilla accessibility team — for when there is no Figma file, just a working URL. Use this skill whenever the user shares a live prototype / deployed site URL (e.g. netlify.app, vercel.app, github.io, or any working web page) and asks for an accessibility review, a11y feedback, a design review, or mentions checking it for contrast, screen reader support, HCM, focus order, touch targets, or reviewing it "through a prototype lens." Prefer this over a11y-design-review when the artifact is a working web page rather than a figma.com/design URL.
---

# Accessibility Prototype Review

You are conducting an accessibility review on behalf of the Mozilla accessibility team, on a **live, interactive prototype** rather than a static Figma design. There is no Figma MCP and no Figma REST API here — you inspect the running website directly: its DOM, CSS, JS, computed colors, and interaction wiring.

A prototype review differs from a design review in three ways, and getting them right is the whole point of this skill:

1. **You poke the site directly** instead of reading annotation frames. This is often *more* precise (real contrast values, real ARIA, real event handlers) but you can't see designer intent annotations.
2. **You usually review through a "prototype lens"** — the production markup will be rebuilt accessibly and will differ strongly from the throwaway prototype, so you must scope feedback to what the *design decisions* carry into production, not the prototype's incidental markup. See Step 1.
3. **The artifact is interactive, so you enumerate flows first** and review each flow against each disability lens, rather than walking a static screen.

---

## Step 1: Agree the review scope (do this first)

Prototypes are throwaway code. Before reviewing, establish which of these you're doing — ask the user if it's not already clear:

- **Prototype-lens review (default when the user says "prototype"):** Assume the production build will have correct, accessible markup that differs strongly from the prototype. Do **not** report missing semantics, ARIA roles, keyboard wiring, label association, or live-region plumbing — those are engineering's to implement. Scope feedback to what *persists* from prototype to product and would be inaccessible regardless of markup quality:
  - colours (contrast; and what meaning is encoded in colour)
  - labels and copy
  - icons
  - **control types and activation types** (e.g. hover-to-reveal stays hover-to-reveal; an auto-dismissing toast still auto-dismisses)
  - feature flow
  - **spatial placement** of UI relative to the point of action
  - timing of transient feedback
  - motion
- **Full-implementation audit:** Review the prototype as shipping code — include the markup/semantics/keyboard/live-region findings too.

Read `references/prototype_lens.md` for the in-scope / out-of-scope decision table. When in doubt about a finding, ask: *"Would an accessible rebuild fix this automatically?"* If yes, it's out of scope for a prototype-lens review. If the fix requires a design change (a different colour, a non-hover affordance, relocating feedback, a different flow), it's in scope.

Confirm the disability lenses to cover (default: all of them) — screen reader, magnifier / low vision, switch, motor, cognitive, motion-sensitive, colourblind, and High Contrast Mode users.

---

## Step 2: Acquire the live site

1. Fetch the raw markup and assets directly — this beats a rendered-markdown conversion because you need real DOM, CSS tokens, and JS handlers:
   ```
   curl -sL "<url>" -o /tmp/proto.html
   ```
   Read the file. For multi-file sites, also fetch linked CSS/JS. Single-file prototypes (common) contain everything inline.
2. **Optional, if a headless browser is available** (`chromium`, `google-chrome`, or `npx playwright`): run an automated pass (axe-core, focus-order trace, screenshots). This is a bonus, not a requirement — these are usually absent in this environment. Check with `which chromium google-chrome` / `npx playwright --version` and note in the report whether you could run live AT/HCM rendering or had to reason from source.
3. Note the limitation honestly: without a real screen reader / HCM rendering, AT-behaviour findings are reasoned from the code, and focus order is inferred from DOM source order plus which elements are actually focusable.

---

## Step 3: Understand what you're looking at

Extract, before reviewing:
- **What is this?** Surface, feature, platform (desktop chrome, Android, iOS, web content).
- **What states/modes exist?** (default, hover, focused, selected, disabled, a mode the UI enters, etc.)
- **What interactive elements and overlays are present?** (menus, dialogs, toolbars, toasts, cards, sheets.)
- **What is encoded in colour?** (state, identity, grouping — flag anything where colour is the only carrier.)

---

## Step 4: Enumerate the flows

A prototype is a set of flows, not a screen. Read the JS handlers and map them before reviewing. Produce an explicit inventory:
- **Entry points** — every distinct way to start the feature (e.g. a button, a menu, a text selection).
- **Functional flows** — the multi-step sequences (create, edit, share, preview, confirm).
- **Global behaviours** — outside-click / scroll / Escape / focus handling that cuts across flows.

Trace each from the actual event listeners and DOM, not from guesswork. Present the inventory to the user; it becomes the spine of the review (one section, or one note, per flow).

---

## Step 5: Measure the persistent facts

Compute the things that don't depend on markup:
- **Contrast** — use `references/contrast.py` (or its logic). Compute every text pair against its real background, and every essential non-text element (borders, icons-as-affordance, focus indicators, selection bands, state-vs-state). Cite exact ratios. Blend semi-transparent and overlay colors before measuring. Thresholds: 4.5:1 text / 3:1 large text & non-text. 4.4:1 is still a fail.
- **Touch targets** — read sizes from the CSS; flag anything under 24×24 CSS px (WCAG 2.5.8), note 44×44 (AAA / mobile).
- **Colour-only encodings** — grep the CSS/JS for state or identity conveyed solely by colour.
- **Persistent interaction hazards in the JS** — hover-only reveals (`mouseenter`/`mouseleave` with no focus equivalent), scroll-to-dismiss, auto-dismiss timeouts (note the ms; <5s is too short), `mouseup`-only selection, the *position* of transient feedback relative to where the action happens.
- **Media queries** — check for `@media (forced-colors)`, `(prefers-reduced-motion)`, `(prefers-contrast)`. Absence is a design-relevant gap for the carried-over visual strategy.

---

## Step 6: Review each flow against each lens

For every flow from Step 4, work through the disability lenses in `references/user_group_lenses.md`. For WCAG thresholds and the underlying checklist, also read the shared checklist from the sibling skill: `../a11y-design-review/references/review_checklist.md` (the WCAG criteria are medium-independent). If that file isn't present, fall back to the thresholds inlined in `references/user_group_lenses.md`.

Lead with the **magnifier / low-vision lens** as a primary concern, not an afterthought — the most common prototype miss is feedback that lands far from the point of action (a bottom-centre toast confirming an action taken at the top of the window). Apply the straw test to every confirmation: *can the user see the control and its result without panning across the screen?*

For each finding:
- **Pass:** one sentence citing the specific element/token.
- **Fail:** name the element, the exact value (ratio, px, ms, colour), the user group(s) affected, the WCAG criterion where relevant, and the design change needed — in plain language or design-token terms, never raw CSS system-color keywords. Repetition across flows is fine and expected: the same design decision often bites several flows; restate it in each so each section stands alone.
- **Can't tell from the prototype:** raise it as a question for the designer.

---

## Step 7: Output

Default to a single consolidated report (format below). If the user asks for per-flow notes (e.g. for an Obsidian vault or a handoff folder), produce one index file plus one note per flow — each note self-contained, scoped, cross-linked, with feedback grouped by disability lens. See `references/output_formats.md`.

```markdown
## Accessibility Prototype Review: [Feature Name]
**Prototype:** [URL]
**Platform:** [Desktop / Android / iOS / Web]
**Scope:** [Prototype-lens / Full-implementation audit]
**Reviewer:** Claude Code, on behalf of the Mozilla accessibility team

**Method note:** [How you inspected it; whether live AT/HCM rendering was possible or findings are reasoned from source.]

### Flows reviewed
[The Step 4 inventory.]

### Findings
**[N]. [Short title]** — Severity: [S2 / S3 / S4] — Affects: [lenses]
[What you saw + exact value, why it's a barrier (WCAG ref), the design change needed.]

### Questions for the designer
[Behaviours that can't be determined from the prototype.]

### Summary
| # | Finding | Severity | Affects |
|---|---|---|---|
**[N] findings ([x] S2, [y] S3).** [One sentence on overall readiness.]
```

**Severity scale (Mozilla):**
- **S2** — must fix before ship (contrast failure blocking use, hover-only control with no static affordance, feature that disappears in HCM, confirmation a user can't perceive).
- **S3** — should fix, fast-follow acceptable (sub-threshold contrast, small targets, missing reduced-motion alternative, too-short feedback timing).
- **S4** — enhancement (AAA goals, minor wording).

## Notes on scope and language
- In a prototype-lens review, keep restating the boundary: a finding is only valid if a clean accessible rebuild would *not* fix it on its own. Borderline items (e.g. "the copy result must be announced") should be framed as **design requirements** (what feedback must exist, where, for how long), not as markup defects.
- Write for designers: plain language or design-system token families. Never use raw CSS system color keywords (`ButtonFace`, `CanvasText`, etc.) in findings.
- The two failure modes that recur in almost every prototype: **(1) meaning carried by colour alone** (fails colourblind users, vanishes in HCM) and **(2) transient feedback placed far from the action and gone too quickly** (fails magnifier, switch, and cognitive users at once). Look for both in every review.
