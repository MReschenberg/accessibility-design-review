# Accessibility Annotations Guide

Accessibility annotations communicate keyboard navigation order, screen reader semantics, and interactive behavior to engineers — information that is invisible in visual designs but essential for building accessible UIs.

This guide covers why annotations are needed, how to place and number them, how to write annotation content, and how to approach custom components. It applies to Firefox Desktop, Android, and iOS designs.

For a comprehensive checklist of what reviewers look for in annotations, see [A11y Design Review Checklist](A11yDesignReviewChecklist.md).

---

## Why annotate?

Visual design communicates hierarchy and layout to sighted users through spacing, colour, and proximity. Screen reader users and keyboard-only users rely on the markup and metadata in code to understand and navigate a UI — information that cannot be inferred from visual design alone.

Accessibility annotations bridge that gap. They tell engineers:

- which elements are focusable and in what order
- how keyboard navigation works within a component (arrow keys, escape, etc.)
- the accessible name and semantic role of each element
- which elements are decorative and should be hidden from assistive technology
- where focus should move when a view opens or closes

Annotating at design time — rather than after engineering — prevents costly rework, reduces ambiguity during handoff, and accelerates the accessibility review process.

---

## Annotation types

The Acorn design system provides four annotation types. Find these components in the Figma presentation library, or use the ones already placed in the UX project template.

Each annotation is placed on top of the design; its corresponding annotation information panel is placed to the side. Annotations and information panels are linked by a shared number or letter.

| Type | Colour | Used for |
|---|---|---|
| Tab navigation | Purple | Keyboard-focusable elements (buttons, links, inputs, first item in a list) |
| Arrow key navigation | Green | Items within a list or widget navigated by arrow keys after Tab focus enters |
| Note | Orange | Non-interactive elements needing screen reader exposure: headings, icons, images, landmarks |
| Presentation | Grey | Elements that are decorative and should be hidden from assistive technology |

**Desktop uses all four types.** Mobile (Android and iOS) uses only Note and Presentation annotations, since swipe-based navigation does not distinguish Tab from arrow key movement.

---

## Placing annotations — desktop

Before annotating, duplicate the design frames into an annotation section. You don't need to copy every frame — just ensure every unique element and state is represented. Locking the design layer prevents accidentally moving elements while placing annotations.

**Tab navigation (purple)** marks every element a keyboard user reaches with the Tab key:

- Buttons, links, text inputs, checkboxes, radio buttons, dropdowns, toggles
- The *first* item in a keyboard-navigable list (subsequent items use arrow navigation)

**Arrow key navigation (green)** marks items navigated with arrow keys *within* a focused container:

- All list items after the first (the first gets a purple tab annotation)
- Individual radio buttons within a radio group (Tab reaches the group; arrows move within)
- Items in a toolbar, menubar, or tab list

There is no need to annotate established keyboard patterns for native controls — for example, dropdown option navigation with arrow keys does not need annotation because the behaviour is already well defined.

**Note (orange)** marks non-interactive elements that must be exposed to screen readers:

- Headings (include heading level, e.g. Heading 2)
- Standalone icons and icon-only buttons (which need a text alternative)
- Informative images
- Landmark regions (navigation, main, section/card — see [Landmark annotations](#landmark-annotations) below)

**Presentation (grey)** marks elements that are purely decorative:

- Illustrative images that add no information not already conveyed by adjacent text
- Redundant visual indicators covered entirely by a sibling element's annotation
- Partially hidden content that would be confusing if read out

---

## Placing annotations — mobile

On mobile, users navigate with swipe gestures (left/right to move between elements, double-tap to activate). The Tab/arrow key distinction does not apply.

Annotate every element the screen reader should read using Note (orange) annotations — including interactive controls, text elements needed for comprehension, and headings. Mark decorative elements with Presentation (grey).

**Reduce the number of focusable elements** where possible. Group closely related elements (a badge and a title, for example) into a single annotation so users do not have to swipe through unnecessary stops. When a card is interactive as a whole, annotate the card — not each sub-element.

---

## Focus order and numbering — desktop

On desktop, focus order (the Tab/arrow key sequence) is a subset of screen reader reading order (which also includes non-interactive text). Annotate focus order explicitly; reading order is assumed to follow English reading order (left-to-right, top-to-bottom) unless there is a specific reason to deviate.

**Tab annotations** are numbered sequentially starting at 1, following visual reading order.

**Arrow key annotations** are lettered using the number of their parent Tab annotation as a prefix. For a list reached via Tab focus stop 3, the first item is `3a`, the second `3b`, and so on. If a list is two-dimensional (e.g. a tab list with a secondary action reachable via the right arrow key), use separate letter sequences for each column: `5a` for the first column, `5b` for the second.

Do not reuse focus numbers across lists — continue incrementing to keep the overall focus order explicit.

**Note and Presentation annotations** are lettered independently (A, B, C…) without relation to the focus order numbers, since they are not part of the Tab sequence. These letters are used to reference the annotations in the annotation information panel.

---

## Focus order and numbering — mobile

On mobile, all Note annotations are numbered in the order the screen reader should read them (1, 2, 3…), left-to-right, top-to-bottom. Presentation annotations are lettered (A, B…).

If there is a reason to deviate from reading order, discuss it with the accessibility team before annotating.

---

## Writing annotation information

Each annotation has a corresponding information panel with three fields: **Name**, **Role**, and **Notes**.

### Name

The accessible name is what a screen reader reads when the element receives focus. The default placeholder is *{use on-screen string}*, meaning the visible text label is the accessible name — appropriate for most buttons, links, and form controls that have visible text.

Override the default when:

- The element has no visible text (icon-only button, image) — provide a text alternative that describes the element's purpose, not its appearance. "Back" not "Left-pointing chevron."
- The visible text is not sufficiently descriptive — a button labelled "More" should have an accessible name like "Show more results."
- The visible text includes the role word — a button labelled "Close button" should be annotated with name "Close" (the role "button" will be announced separately).

**What makes a good accessible name** ([WAI guidance](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/)):

- Convey function, not appearance — name a control by what it *does*, not what it looks like
- Lead with the distinguishing word — "Edit Jane Smith" rather than "Jane Smith, edit"
- Keep it brief — one to three words typically suffice
- Do not include the role — "Submit" not "Submit button"
- Make each name unique on the page unless elements are truly identical
- Avoid demonstrative pronouns — not "this," "it," or "here"
- Do not use instruction language ("tap here," "click to") — describe the purpose

### Role

The semantic role tells the screen reader how to interact with the element and what to announce. The role is usually the element type: `button`, `link`, `input`, `checkbox`, `radio button`, `switch`, `heading`, `image`, `list`, `list item`.

For **headings**, include the level (e.g. `heading 2`).

For **landmarks**, use the appropriate landmark type (see [Landmark annotations](#landmark-annotations) below).

For **known custom components from the design system** (e.g. toggle switch), use the component name — the accessibility team and engineers already know the expected role. For new custom components, see [Custom components](#custom-components).

Use `presentation` for elements annotated in grey — the role field is pre-filled and does not need to change.

If you are uncertain about a role, reach out to the Acorn or accessibility team.

### Notes

Notes are optional. Use them to communicate information not captured by name or role:

- **Focus management** — where focus should move when a view, sheet, or dialog opens (typically the first interactive element or the container itself)
- **Arrow key directions** — for arrow navigation annotations, specify which arrow keys move to the previous/next element
- **State announcements** — when a control has a toggled or expanded/collapsed state, note that the state should be announced (e.g. `aria-expanded` on a disclosure button, `aria-pressed` on a toggle button)
- **Shared annotations** — when two or more elements have the same name, role, and behaviour (e.g. expand buttons on identical cards), a single annotation information block can cover multiple annotations by comma-separating their reference identifiers
- **Engineering references** — for complex patterns, link to relevant ARIA Authoring Practices or prior review documents

---

## Landmark annotations

Landmarks mark distinct regions of the UI so screen reader users can understand where they are and jump directly between sections.

Annotate landmarks with an orange Note annotation. Common landmark types and when to use each ([WAI landmark guidance](https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/)):

| Landmark | Use for |
|---|---|
| `navigation` | A group of links used for navigating the site or page |
| `main` | The primary content of the page |
| `banner` | Site-level header (logo, search) — one per page |
| `contentinfo` | Footer content (copyright, legal links) — one per page |
| `complementary` | Supporting content meaningful on its own (e.g. a sidebar) |
| `search` | A search input and its controls |
| `form` | A collection of form fields with a visible label |
| `region` / `section` | A distinct, named section of the page (e.g. a card grouping open vs. closed tabs) |

**Naming landmarks:** If the same landmark type appears more than once on a page (e.g. two navigation regions), each must have a unique accessible name so users can distinguish them. Use the heading text if one is present (`aria-labelledby`), or an explicit label (`aria-label`). Do not include the landmark type word in the label — "Main navigation" is fine; "Navigation navigation" is not.

A simple, self-contained panel may not need landmarks beyond the panel itself. A complex page with multiple distinct areas (navigation sidebar, main content, collapsible card groups) benefits from explicit landmark annotations on each region.

---

## Accessible names for complex patterns

Some annotation scenarios require more care than a simple text label.

**Icon-only buttons** — Provide a name that describes the action, not the icon. "Close," "Back," "Collapse sidebar" — not "X icon" or "chevron."

**"Learn more" links** — A page with multiple "Learn more" links is ambiguous to screen reader users navigating by links. The accessible name should incorporate the topic: "Learn more about Firefox Sync." If the heading text is adjacent, it can be referenced with `aria-labelledby` — note this in the annotation.

**Buttons that open new tabs** — Append "(opens new tab)" to the accessible name so users are warned before activation.

**Grouped elements** — When a label is visually adjacent to a control but not a child of it (e.g. a toggle label to the right of the switch), note the association so engineers use `aria-labelledby` or a wrapping `<label>`.

**Placeholder text** — Never use placeholder text as the only label for a form input. Placeholder disappears on typing and is not consistently announced by screen readers. A visible label above the field is required.

For thorough guidance on naming techniques and precedence, see the [WAI accessible names and descriptions practice](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/).

---

## Common component patterns

Many standard UI patterns have well-defined ARIA roles and keyboard interactions. When annotating these components, use the corresponding role and follow the established keyboard behaviour — engineers will implement to the pattern, not invent one.

The [WAI ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/patterns/) documents keyboard interaction and role requirements for:

Accordion, Alert, Alert Dialog, Breadcrumb, Button, Carousel, Checkbox, Combobox, Dialog (Modal), Disclosure, Feed, Grid, Landmarks, Link, Listbox, Menu and Menubar, Menu Button, Meter, Radio Group, Slider, Slider (Multi-Thumb), Spinbutton, Switch, Table, Tabs, Toolbar, Tooltip, Tree View, Treegrid, Window Splitter.

When annotating any of these patterns, reference the relevant APG entry in a Note if the keyboard behaviour is non-obvious or if the component differs visually from its semantic equivalent.

---

## Custom components

Custom components — elements that don't correspond directly to a standard HTML or ARIA component — still need annotation. In most cases, a custom component has a functional equivalent from which its role and keyboard behaviour can be derived.

For example: a component where users select a quantity by clicking segments of a visual illustration functions like a slider. Annotate it as `slider` and follow the slider keyboard pattern.

When designing a custom component:

1. Identify the closest functional equivalent in the [WAI APG patterns library](https://www.w3.org/WAI/ARIA/apg/patterns/)
2. Use that pattern's role and keyboard interaction model as the annotation basis
3. Reach out to the Acorn or accessibility team early — custom components need accessibility sign-off before engineering begins

If no standard pattern fits, the accessibility team can advise on the correct role and interaction model.

---

## Desktop vs. mobile quick reference

| | Desktop | Mobile (Android/iOS) |
|---|---|---|
| Primary navigation input | Tab key + arrow keys | Swipe gestures |
| Annotation types used | All four (purple, green, orange, grey) | Note (orange) and Presentation (grey) only |
| Focus order | Annotate Tab stops with numbers; arrow nav with letter suffixes | Annotate all elements in reading order with sequential numbers |
| Presentation numbering | Letters (A, B, C…) independent of focus numbers | Letters (A, B…) |
| Screen readers | VoiceOver (macOS), NVDA/JAWS/Narrator (Windows) | TalkBack (Android), VoiceOver (iOS) |
| Key interactions to document | Arrow key directions, Escape, Enter/Space behaviour | Focus on entry, state changes, grouping decisions |
