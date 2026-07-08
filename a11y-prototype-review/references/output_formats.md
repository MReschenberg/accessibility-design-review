# Output formats

Two ways to deliver a prototype review. Default to the **consolidated report**; produce **per-flow notes** when the user asks for a handoff folder, an Obsidian vault, or "a note per flow."

---

## A. Consolidated report (default)

Rendered inline. Structure in SKILL.md Step 7. Order findings by severity, then by flow. Each finding states: title, severity, affected lenses, the exact value (ratio / px / ms / colour), the WCAG criterion, and the design change needed. End with a severity table and a one-line readiness verdict.

---

## B. Per-flow notes (on request)

Create a folder (ask where, or use the path the user gives). Produce:

- **`flow.md`** — the index. Contains:
  - A **scope statement** (the prototype lens from `prototype_lens.md`, in the user's terms — what's in/out of scope, which lenses are covered).
  - The **flow inventory** from Step 4 (entry points, functional flows, global behaviours), each linking to its note.
  - A short **cross-cutting themes** section naming the recurring failure modes so the reader sees the pattern before the details.
- **One note per flow**, e.g. `01-<flow-name>.md` … `NN-<flow-name>.md`. Each note is self-contained:
  - A link back to `[[flow]]` and a one-line scope reminder.
  - **The flow** — its steps as the prototype actually runs them (traced from the JS), and links to the flows it routes into.
  - **The defining concern** — the single biggest barrier for this flow, called out first.
  - **Feedback grouped by disability lens** — screen reader, magnifier / low vision, switch, motor, cognitive, motion-sensitive, colourblind, HCM. Omit a lens only if genuinely N/A for that flow; otherwise include it.
  - **Contrast** sub-section with measured ratios for that flow's colours.

### Conventions for per-flow notes
- Use Obsidian-style `[[wikilinks]]` between notes (works in plain Markdown too).
- **Repetition is expected and good** — if the same design issue (colour-fill highlight, bottom-centre toast, purple button at 4.15:1) affects several flows, restate it in each so every note stands alone. Tell the user you've done this deliberately.
- Lead the whole set, and ideally each note, with the **magnifier lens** where the flow produces feedback — it's the most-missed.
- Keep findings scoped to the prototype lens; frame boundary items as design requirements, not markup defects.

### Number the files
Zero-pad and order by the flow inventory (entry points first, then functional flows, then global behaviours) so the folder reads top-to-bottom in flow order.
