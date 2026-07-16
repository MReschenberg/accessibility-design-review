# Accessibility Design Review Checklist

This checklist is used by the Mozilla accessibility team when reviewing Figma designs for accessibility compliance. It is distilled from analysis of 122 Figma design reviews (2023–2026). Work through sections relevant to what is shown in the design — not all sections will apply to every review.

For background on HCM media queries and the Firefox color token system referenced in §4–5, see [HCM Media Queries](HCMMediaQueries.md) and [Colors and High Contrast Mode](ColorsAndHighContrastMode.md).

---

## 1. Color Contrast — Text (WCAG 1.4.3, Level AA)

**Threshold:** 4.5:1 for normal text; 3:1 for large text (18pt+ or 14pt bold+).

Check:
- All text in all interactive states (default, hover, active, selected, disabled). No exemption for pressed/active states — only disabled is exempt.
- Secondary/deemphasized text, placeholder text, badge text, button labels, error messages.
- Text on image or gradient backgrounds (measure against the lightest or most variable portion).
- Text on colored container backgrounds (not just white/black).
- Link color vs. surrounding non-link text: if no underline, link must contrast at 3:1 against adjacent static text in addition to 4.5:1 against background. An underline removes this requirement.
- Mozilla purple (#7742E7 / #7743E7) consistently fails on dark/mid-tone backgrounds — flag any use on non-white backgrounds.
- 4.4:1 is still a failure. Do not pass items that are "close."

---

## 2. Color Contrast — Non-Text / UI Components (WCAG 1.4.11, Level AA)

**Threshold:** 3:1 for essential UI components and graphical elements.

Essential elements that must meet 3:1:
- Input borders (radio buttons, checkboxes, text inputs)
- Carousel/pagination dots — check all three pairings: active vs. bg, inactive vs. bg, active vs. inactive
- Toggle track and thumb (when no other state indicator exists)
- Drag handles / grab handles (when the sole affordance)
- Icon-only affordances communicating state (error icons, weather icons, status badges)
- Text selection highlight vs. unselected background
- Panel/dialog borders separating chrome from web content
- Selected state background vs. unselected state background (3:1 between the two states)

Decorative/redundant graphics (information fully conveyed by adjacent text) do not need 3:1.

Specific common failures: radio button borders (~1.9:1), grab handles (~1.7:1), text selection highlights (~1.2:1), panel borders (~1.6:1), toolbar button borders (~1.6:1).

---

## 3. Color — Not Relying on Color Alone (WCAG 1.4.1)

Any state or meaning communicated only through color change must also be communicated via shape, border, pattern, label, or icon.

Check:
- On/off toggle state (needs shape or label change, not just color)
- Error states (need text and/or icon, not just red border)
- Selected card/tab/chip (needs border, checkmark, or other non-color indicator)
- Secure vs. insecure state (needs icon shape change, not just color change)
- Sentiment/status symbols (carets, dots — need accessible names)

Adjacent state contrast: when active and inactive states appear side by side, text colors must also contrast at 4.5:1 between states, and background colors at 3:1 between states.

---

## 4. High Contrast Mode (HCM) — Forced Colors

HCM affects Windows users (and Firefox HCM users on any platform). Designs must include HCM mocks for every new UI surface before engineering handoff.

**The core principle:** Components using Firefox Desktop Styles tokens adapt to HCM automatically through the `tokens-forced-colors` cascade layer. The [Desktop Styles tokens table](https://firefoxux.github.io/firefox-desktop-components/?path=/story/docs-tokens-table--default) is the direct source from which these tokens are generated — any token name listed there is a Desktop Styles token and has a `forced-colors` mapping. Only hardcoded values (hex colors, `light-dark()` calls, `rgba()`, gradients, brand palette tokens like `--color-violet-80`) need explicit `forced-colors` overrides.

**Important for writing review feedback:** Do not use raw CSS system color keywords (`ButtonFace`, `ButtonText`, `CanvasText`, `SelectedItem`, etc.) in findings. Designers will not recognise these terms. Instead, describe the fix in terms of design system tokens (e.g. `--button-background-color`, `--button-text-color`) or in plain language (e.g. "the button background should use the button token family so it adapts automatically").

HCM mocks — check for:
- **Hardcoded hex colors** in the HCM mockup — these won't adapt to the user's theme
- **Blur effects** — must be removed; replace with a solid background using the appropriate `--background-color` token, plus a 1px solid border using the component family's border token
- **Drop shadows** — must be removed; replace with a 1px solid border using the component family's border token
- **Gradients** — must be replaced with a solid fill using the appropriate background token from the component family
- **Semi-transparent colors** (`rgba()`, `opacity < 1`) — transparency is stripped in HCM; explicit override using an opaque design system token is needed
- **Links** — must use the design system link color token that resolves to `LinkText` in forced-colors (consult the [tokens table](https://firefoxux.github.io/firefox-desktop-components/?path=/story/docs-tokens-table--default) — do not specify `LinkText` or `MozNativehyperlinkText` directly in the recommendation)
- **Token libraries without HCM mappings** — If the design uses tokens from a library that has no `forced-colors` cascade layer, flag this explicitly as a finding and direct the designer to contact the Mozilla accessibility team for guidance before engineering handoff. Do not attempt to prescribe the fix yourself — the correct override depends on the library's roadmap and may require a dedicated HCM component variant. Nova is a current example of a library in this state.
- **Ghost components** — don't override ghost tokens to default-state values in `forced-colors`; let them cascade naturally

Token family rules:
- Background, text, and border tokens must all come from the same token family and the same interaction state
- Static/non-interactive text → use the text/background token family (e.g. `--text-color`, `--background-color-canvas`)
- Interactive controls → use the button token family (e.g. `--button-background-color`, `--button-text-color`, `--button-border-color`)
- Selected items → use the selection token family, not just a different hue (e.g. `--color-accent-primary-selected`, `--text-color-accent-primary-selected`)
- Disabled → use disabled tokens (e.g. `--button-text-color-disabled`), not reduced opacity

---

## 5. Increase Contrast (IC) — macOS

IC users keep the normal Firefox color scheme — do not give them system colors or a reduced palette. IC design improvements mean increasing contrast within the existing color scheme.

IC users trigger `prefers-contrast: more` but NOT `forced-colors`. A bare `@media (prefers-contrast)` block applies to both IC and HCM users.

Check:
- IC mocks (if present) use the existing color scheme with improved contrast, not system colors
- Borders are present for IC users (using `currentColor`, not system color tokens)

---

## 6. Screen Reader Annotations — Format

Check annotation completeness and correctness:

**Annotation box types:**
- Orange box = exposed to screen readers (Name + Role + State)
- Gray box = presentational (hidden from AT, `alt=""`)
- Plain text nodes do not need annotation boxes

**Numbering:**
- Letters (A, B, C) = landmark/region annotations (non-focusable)
- Numbers (1, 2, 3) = keyboard-focusable elements
- Both interleaved in one list following visual reading order (not separated by type)

**Name field — check for:**
- Matches on-screen text verbatim
- Uses `{use on-screen string}` placeholder for dynamic content
- Does NOT include role word ("Close banner button" → should be just "Close")
- Does NOT include state ("VPN on" → should be "VPN" with state in Note)
- Does NOT use demonstrative pronouns ("this," "it," "here")
- Front-loads the unique part (e.g. "Spanish (30.2 Mb), Download" not "Download, Spanish")
- Icon-only buttons include surrounding context ("Edit New Window" not just "Edit")
- "Learn more" links use `aria-labelledby` to combine with adjacent heading
- Buttons opening new tabs include "(opens new tab)"

**Role field — check for:**
- Uses correct ARIA/semantic role, not colloquial terms
- Common errors: "Learn More" marked as Button (→ Link); "description" as role (→ "text"); gesture hints in Role field (→ Note/Hint field)
- On Android: "Menu item" role doesn't exist in Android API — use Button

**Note/State field — check for:**
- `aria-expanded` on any expandable/collapsible trigger
- `aria-pressed` on toggle buttons
- `aria-checked` on switches, checkboxes, radio buttons
- `aria-selected` on tabs, list items
- `aria-invalid` + `aria-errormessage` on invalid form inputs
- `aria-labelledby`/`aria-describedby` references where labels are separate from controls
- Focus management notes (where focus goes on open/close)
- Engineering reference links for complex patterns

---

## 7. Screen Reader Annotations — Specific Patterns

**Dialogs:**
- Orange box around full container: Name = on-screen heading (via `aria-labelledby`), Role = `dialog` or `alertdialog`
- Note must include: focus trapped inside, ESC closes

**Bottom sheets (Android/mobile):**
- Sheet itself gets NO accessible name (triggering button conveys purpose)
- Grab handle = item 1 in focus order, Role = button, Name = describes collapse/expand action
- Header row = Role: header (heading row only, not full sheet)

**Lists and groups:**
- Wrap related items in `role=group` or `role=list` with accessible name
- Example: shortcuts → `role=list, name="Shortcuts"` so group announced on first entry

**Tabs:**
- Container: `role=tablist` + name; Each tab: `role=tab` + `aria-controls` + `aria-selected`; Panel: `role=tabpanel` + `aria-labelledby`
- Navigation: arrow keys (not Tab) between tabs

**Toolbars:**
- Container: `role=toolbar`; arrow keys navigate within; ESC closes nested component first

**Landmarks:**
- `header` = `banner`; `footer` = `contentinfo`; `main` = `main`
- Names must not repeat the role word ("Website footer" is redundant)

**Images:**
- Informative: orange box, meaningful alt text
- Decorative: gray box, `alt=""` (include empty alt — do not omit attribute)
- Warning/error icons: `alt="Warning:"` or `alt="Error:"` so meaning precedes text
- "Opens new tab" icon: include "(opens new tab)" in accessible name or `title`

---

## 8. Focus Management and Keyboard Navigation

**Focus order:**
- Must follow visual reading order (left-to-right, top-to-bottom for LTR)
- Cancel/secondary actions follow their visual position; do not always place last
- Close button in banners/CFR: follows reading order (usually item 2, actions after)

**On open (dialog, panel, sheet):** focus moves inside — first focusable element or container with `tabindex="-1"`
**On close:** focus returns to the triggering element

**Hover-only controls:**
- Acceptable only with a static, always-visible affordance (persistent 3-dot icon, persistent chevron)
- Hover-only controls with no static indicator = S2 issue ("Schrödinger's icon")
- If hover-only retained, same action must be reachable through a persistent path

**Nested interactive controls:** WCAG violation — a clickable row cannot also contain a separately focusable button

**Radio groups:** Tab enters; arrow keys navigate within; `role=radiogroup` wrapper required
**Toolbars:** Tab enters; arrow keys navigate within

---

## 9. Grouping and Reducing Focus Stops

- If sub-annotations (5a, 5b, 6A–6E) exist for a component that is interactive as a whole, collapse to one focus stop
- Toggle + label: one focus stop
- Icon + adjacent label: one focus stop (icon is presentational)
- Language name + file size + download button: one focus stop (reading order: "Spanish, 30.2 Mb, Download, button")
- Cards that are interactive as a whole: annotate the card, remove sub-annotations

---

## 10. Touch Target Size

| Platform | Minimum |
|---|---|
| All (WCAG 2.5.8, AA) | 24×24 CSS px |
| All (WCAG 2.5.5, AAA) | 44×44 CSS px |
| Android (guideline) | 48×48 dp |
| Android QA threshold | < 35dp → S2 severity |

Most at-risk: close "X" buttons, kebab "..." buttons, grab handles, trashcan icons.
Icon can be smaller than the touch target — the invisible tap area must meet the minimum.

---

## 11. Dynamic Content and Live Regions

- `aria-live="polite"`: status messages, download progress, translation output, copy confirmation
- `role="alert"` (`aria-live="assertive"`): urgent errors, snackbars
- Live region container must exist in DOM before content is inserted
- Snackbars: must be announced; focus must NOT move to the snackbar
- Snackbar auto-dismiss: minimum 5 seconds standard; 20 seconds with accessibility enabled
- Progress bars: accessible name must include percentage ("Downloading (45%)")
- Error icons: must have text alternative (alt="Error:" or alt="Warning:")

---

## 12. Motion and Animation

- All animations must respect OS `prefers-reduced-motion` — provide static fallback
- Flash rate: no more than 3 times/second (333ms threshold). 350ms is dangerously close.
- Blur effects: a vestibular/motion sensitivity concern; restrict or remove
- Auto-playing animations: stop at 5 seconds OR provide visible play/pause control
- Hover-triggered animations: must stop when focus leaves
- Time limits: minimum 20 seconds, must be pauseable (WCAG 2.2.1)

---

## 13. Forms and Input Fields

- All inputs need a visible label above the field — not just placeholder text
- Placeholder text disappears on type — never use it for instructions
- Split-digit inputs (one box per digit for codes) are **S2** — direct designers to prior review doc
- Character limit counters: not live on every keystroke; surface near/at-limit warnings via `aria-describedby`
- Phone inputs: use `<input type="tel">` and input masking (no manual hyphens)
- Disabled controls: HTML `disabled` attribute, not just visual styling

---

## 14. Low Vision and Magnification

- Toggles: must be **left** of their label (not right-aligned)
- Straw test: can a magnification user see both a control and its label without panning? (Reference: https://scottvinkle.me/blogs/work/proximity-and-zoom)
- Disclosure chevrons: move to **left** of the label text, not far right
- Submenu indicators: as close to label text as possible
- Close buttons: add a second "Close" button near the bottom of tall panels for magnification users
- Chrome text: minimum 12px (browser zoom doesn't affect chrome elements)
- Text truncation: must be expandable or readable in full on focus/hover (WCAG 1.4.4)

---

## 15. Cognitive Accessibility

- Destructive actions: must have a confirmation step; CTA must name the action (e.g., "Delete group," not "Confirm")
- Binary states: use binary controls (toggle, checkbox), not labels that change
- Numeric state controls: always show the current value (e.g., "Zoom, 125%")
- No demonstrative pronouns in accessible names ("this," "it," "here")
- Instruction copy: avoid "tap," "click," "above," "below" — use "select," describe what to do
- Theme/color names: readable at a broad level, not dependent on color perception

---

## 16. Drag-and-Drop Accessibility (WCAG 2.5.7)

Every draggable element must have a non-drag alternative:
- **Android TalkBack:** Accessibility Actions menu with "Move left" / "Move right"
- **Voice Access / Single-touch:** action sheet with move up/down/left/right options
- **Keyboard:** Ctrl+Shift+Page Up/Down (Win/Linux), Cmd+Shift+Up/Down (macOS)

---

## Common Annotation Errors to Catch

Quick checklist — flag if any of these are present:

- [ ] Role word in Name field ("Close banner button," "Help Icon Button," "Downloads list")
- [ ] State word in Name field ("VPN on," "[Open or close]")
- [ ] Gesture instructions in Role field (move to Hint/Note)
- [ ] Non-ARIA terms in Role ("description," "menu item note," "Information")
- [ ] Hard-coded copy in Name when text changes (use `{use on-screen string}`)
- [ ] Missing `role=radiogroup` wrapper around radio buttons
- [ ] Missing `aria-expanded` note on expandable triggers
- [ ] Missing programmatic state notes (toggle on/off, checkbox checked/unchecked, disabled)
- [ ] Sheet grabber not annotated as item #1
- [ ] Decorative sub-elements not marked presentational when covered by parent's name
- [ ] Tab and screen reader annotations in separate lists instead of one interleaved list
- [ ] Focus order numbers don't match visual reading order
- [ ] Sub-annotations (5a, 5b) on a single-action interactive unit
