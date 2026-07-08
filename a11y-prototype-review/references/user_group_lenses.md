# Disability lenses for prototype review

Review **each flow** against each of these. They're framed for a prototype-lens review (design-carried barriers), so they emphasise placement, timing, colour, activation, and motion over markup. Lead with the magnifier lens — it's the most commonly missed.

WCAG thresholds referenced here also live, in fuller form, in the sibling skill's `references/review_checklist.md`; read that for the complete WCAG criteria. The numbers are repeated below so this file stands alone.

---

## Magnifier / low vision (screen magnification: ZoomText, Windows Magnifier, macOS Zoom)

The dominant prototype failure. A magnifier user sees a small slice at 200–400%, and the magnifier pans to follow **focus, caret, or pointer** — *not* arbitrary on-screen changes.

- **Straw test (apply to every confirmation/result):** can the user see the control *and* its result without panning across the screen? A toast at bottom-centre confirming an action taken at the top of the window fails this.
- **Feedback must land near the point of action**, in the region the user is already viewing — or focus must move to it so the magnifier follows.
- **A result that appears in a different pane than the click** (e.g. sidebar click scrolls a content pane the user isn't looking at) is invisible; bring the target into the current view.
- **Transient feedback must persist long enough to pan to** — panning takes seconds; a ~2s toast is gone first.
- **Don't tie meaningful UI to scroll/hover** the user may pan away from before it renders.
- Keep related controls and their feedback in **close proximity** (don't spread a group across a wide panel that needs horizontal panning).

## Screen reader users (framed as design requirements)

- Any action with **no visible result** (copy, save, a silent state change) must have a **perceivable outcome confirmation** the design specifies — what it says, that it's announced. Don't let success be silent.
- **Live/changing values** (a count, a status) must be conveyed when they change, not only shown.
- **Meaning encoded only in visuals** (colour, position, a tint) must have a text/programmatic equivalent the design accounts for.
- **Labels/copy** must carry meaning without surrounding visual context, and must distinguish consequential variants (e.g. "link" vs "link to your *annotated* page").
- Decorative icons/emoji must not pollute names — a design note, since the glyph is a design choice.

## Switch users (sequential scanning, single activation)

- **No time limits / auto-dismiss** on anything the user needs — scanning is slow; a 2–3s auto-dismiss is gone before the scan reaches it.
- **No hover-only controls** — switch users cannot hover; every action needs an activate-able path.
- **No pointer-gesture-only dismissal** (outside-click, backdrop-click, drag) — needs an explicit, scannable control.
- **Minimise steps and scan length** — order the likely actions first; don't bury actions below long inert lists.
- **No precision-pointing prerequisites** (e.g. dragging out a text selection to start a flow) — provide a low-precision entry.

## Motor users

- **Touch/click targets ≥ 24×24 CSS px** (WCAG 2.5.8); aim 44×44 (2.5.5 / mobile). Flag tiny clustered controls (swatches, close ✕, kebabs).
- **Adequate spacing** between adjacent targets so the wrong one isn't hit (e.g. a close ✕ next to a primary action).
- **No hover-hold requirements**; no precise drag as the only path.
- **Forgiving destructive/dismiss actions** — outside-click that silently discards a draft is hostile; provide explicit Cancel and/or undo.
- **Focus returns to the trigger** on close, so the user isn't forced to re-traverse.

## Cognitive users

- **Plain, specific copy**; name actions by what they do ("Delete group", not "Confirm"). Avoid demonstrative pronouns ("this", "here") and gesture verbs ("tap", "above").
- **Make invisible outcomes explicit** (state what was copied / saved / shared, and at what scope).
- **Consistency** — the same label does the same thing across entry points; the same key (Escape) and control type dismiss every surface.
- **Predictability** — UI that changes identity by mode (one component that's both an instruction and a status bar) is hard to model; flag it.
- **Enough time to read** transient feedback; **no silent data loss**.
- **Distinguish similar options** presented together (three "share" variants at different scopes).

## Motion-sensitive / vestibular users

- Everything that animates needs a **`prefers-reduced-motion` static alternative** the design specifies: smooth-scroll → instant jump; pulse/slide → static emphasis or fade.
- **Auto-scroll** (smooth scrolling the page on a jump) is a common trigger — provide the reduced-motion path.
- Restrict/remove **blur** effects.
- Auto-playing motion stops by 5s or has a pause control; no flashing >3×/second.

## Colourblind users

- **No meaning by colour alone** (WCAG 1.4.1). State, identity, grouping, selection shown only by hue must add shape/label/pattern/icon.
- **Surface colour *names*** where the user picks or distinguishes by colour (a swatch picker needs names).
- A success colour (green check) must be paired with **text/icon**, not colour alone.
- Adjacent state-vs-state must differ by more than hue.

## High Contrast Mode / forced colors (Windows HCM; Firefox HCM on any OS)

- **Background-fill encodings disappear** — forced colors replaces background colors and drops box-shadows/gradients. Anything whose meaning is a tint or a shadow (e.g. a highlight rendered as a background fill) becomes invisible. The design needs a forced-colors-safe treatment (solid border/outline via a system-mapped token), not a fill.
- **Scrims/overlays** (semi-transparent backdrops) don't render — modals need a solid border to stay delineated.
- **Brand/hardcoded colours** don't adapt — flag colour-first features that have no HCM strategy; design the HCM variant with the accessibility team.
- Describe fixes in **design-token / plain-language** terms, never raw CSS system color keywords.

---

## Recurring cross-lens failure modes (look for these every time)

1. **Meaning carried by colour alone** → fails colourblind users *and* vanishes in HCM. (Usually two findings, same root.)
2. **Transient feedback far from the action and gone too fast** → fails magnifier (spatial), switch (timing), and cognitive (reading time) users at once.
3. **Hover-only / pointer-gesture-only interaction** → fails switch, keyboard, touch, and motor users; the design must add a persistent, non-pointer affordance.
4. **Inconsistent dismissal model** → Escape/close that works on some surfaces but not others fails cognitive and keyboard/switch users.
