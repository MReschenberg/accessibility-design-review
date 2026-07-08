---
name: a11y-design-review
description: Performs an accessibility (a11y) design review on a Figma file on behalf of the Mozilla accessibility team. Use this skill whenever the user shares a Figma URL and asks for an accessibility review, a11y feedback, a design review, or mentions checking a design for contrast, screen reader annotations, HCM, focus order, or touch targets. Also use it proactively when the user pastes a figma.com/design URL alongside any request related to accessibility, disability inclusion, or WCAG compliance.
---

# Accessibility Design Review

You are conducting an accessibility design review on behalf of the Mozilla accessibility team. Your job is to examine a Figma design systematically and produce specific, actionable findings that the designer can act on before engineering handoff.

## Step 1: Parse the Figma URL

Extract the file key and node ID from the URL the user provided.

- URL format: `https://www.figma.com/design/:fileKey/:fileName?node-id=:nodeId`
- The `node-id` query param uses `-` as separator (e.g. `10978-9453`) — convert to `:` for API calls (e.g. `10978:9453`)

If the user didn't provide a node ID, proceed with the file key alone — you'll review comments across the whole file and take screenshots of whatever the MCP returns.

## Step 2: Get the Figma API token

Look for a Figma personal access token in this order:

1. Environment variable `FIGMA_TOKEN`
2. Memory — check MEMORY.md for a saved Figma token entry and read that file

If not found, ask the user to provide one: Figma → Settings → Account → Personal access tokens → generate a token with read access. Save it to memory (type: reference) so it's available for future reviews. The token is personal and is not bundled with this skill — each user provides their own.

The token is passed as an `X-Figma-Token` header on all REST API calls.

**On the Figma MCP:** `mcp__figma__get_design_context` requires an active selection in the Figma desktop app, which makes it unreliable for scripted reviews. Use the Figma REST API directly as the primary path. Only attempt the MCP tool if the user has Figma open and mentions they have the node selected — and treat it as a bonus, not a requirement.

## Step 3: Fetch everything in parallel

Run all of the following at the same time:

1. **Existing comments** (REST API) — *optional context, not a requirement*:
   ```
   GET https://api.figma.com/v1/files/{fileKey}/comments
   ```
   Parse the response to find threads where any of the following team members participated, or where any a11y keyword appears (`a11y`, `accessibility`, `contrast`, `screen reader`, `talkback`, `voiceover`, `aria`, `focus`, `hcm`, `wcag`, `touch target`):
   
   **Team members:** Morgan Rae Reschenberg, Anna Yeddi, Natalie Stroud, James Teh, Eitan Isaacson, Kim Bryant, Frank Griffith
   
   For each relevant thread, record the comment `id` field. When referencing the thread in your findings, link it directly using:
   `https://www.figma.com/design/{fileKey}?commentId={id}`
   rather than referring to it by number, date, or author name alone.
   
   No threads found is normal — it typically means this is the design's first accessibility review, which is exactly the scenario this skill is built for. The full review runs regardless.

2. **Design context** (REST API):
   ```
   GET https://api.figma.com/v1/files/{fileKey}/nodes?ids={nodeId}
   GET https://api.figma.com/v1/images/{fileKey}?ids={nodeId}&format=png&scale=2
   ```
   The nodes endpoint gives you the full component tree, text content, colors, and annotation properties. The images endpoint gives you a rendered PNG to view. Parse both for the review.

3. **Review checklist** — read `accessible/docs/A11yDesignReviewChecklist.md` from the Firefox repository root.
   If running outside a Firefox checkout, fetch the published version instead:
   `https://firefox-source-docs.mozilla.org/accessible/docs/A11yDesignReviewChecklist.html`

4. **Annotations guide** — read `accessible/docs/A11yAnnotationsGuide.md` from the Firefox repository root.
   If running outside a Firefox checkout, fetch the published version instead:
   `https://firefox-source-docs.mozilla.org/accessible/docs/A11yAnnotationsGuide.html`

5. **Component library reference** — read `accessible/docs/A11yDesignComponentLibraries.md` from the Firefox repository root.
   If running outside a Firefox checkout, fetch the published version instead:
   `https://firefox-source-docs.mozilla.org/accessible/docs/A11yDesignComponentLibraries.html`

## Step 4: Understand what you're looking at

Before running checks, extract:

- **What is this design?** (Surface, feature, platform — desktop chrome, Android, iOS, web content)
- **What states are shown?** Read the text label nodes on the canvas — section headings, state labels, and frame annotations (e.g. "Version 1", "HCM", "hover on menu item", "default") are the authoritative source for what each frame represents. Do NOT infer state type from visual appearance alone: a dark background does not mean dark mode, and a light background does not mean light mode — a designer may have labeled a dark frame as "HCM" and a separate dark frame as "dark mode". Always use the label. If no label is present, call it out as a question rather than assuming.
- **What interactive elements are present?** (Buttons, links, form controls, dialogs, lists, carousels, drag handles)
- **What has already been flagged?** If team members have left unresolved comments, note them — you will include them in your findings alongside any new issues you discover, attributed to the original commenter. Resolved threads can be skipped. If no team threads exist, that's expected for a first review; proceed straight to the checklist.
- **What is a component instance vs. a one-off?** When you find incomplete content, a placeholder, or an annotation gap on an element, check whether its node type is `INSTANCE` — if so, it has a `componentId` pointing to a master component. If the same issue appears across multiple instances sharing that `componentId`, the fix scope is the component library, not just this screen. Note this distinction in your findings.

  Use the component library reference (fetched in Step 3) to identify whether the component comes from Desktop Components 3, Nova, or another known library.

  **Desktop Components 3 (DC3) — Figma file key: `3WoKOSGtaSjhUHKldHCXbc`**

  DC3 components can be fetched directly to compare against their canonical definition. Use the page IDs below:

  | Page ID | Component |
  |---|---|
  | 533:7349 | Button |
  | 538:9703 | Dropdown |
  | 538:6964 | Input Text |
  | 538:6963 | Checkbox, Radio, Toggle switch |
  | 538:18542 | Input Color |
  | 5231:5818 | Visual Picker |
  | 3478:1453 | Badge |
  | 538:9121 | Label |
  | 538:20646 | Focus ring |
  | 2719:28465 | Fieldset |
  | 538:13546 | Box |
  | 538:13703 | Card |
  | 538:11014 | Panel |
  | 2500:8884 | Dialog |
  | 538:11281 | Panel list, Context menu |
  | 538:18375 | Page navigation |
  | 2006:11269 | Feature callout |
  | 538:9860 | Message bar |
  | 4429:362 | Promo |
  | 2575:18426 | Spotlight modal |
  | 4213:3149 | Five Stars |
  | 538:21167 | Browser |
  | 538:20813 | Toolbar, Tabstrip |
  | 541:8321 | Bookmarks bar, Info bar, Find bar |
  | 538:20980 | Sidebar, Side strip |

  To fetch a canonical DC3 component:
  ```
  GET https://api.figma.com/v1/files/3WoKOSGtaSjhUHKldHCXbc/nodes?ids={pageId}
  ```
  Compare the canonical component structure against what you see in the review design. Deviations (extra placeholder nodes, missing slots, overridden text) are component-level issues — flag them as needing a fix in the DC3 library, not just in this screen.

## Step 5: Run the review

Work through the checklist in `accessible/docs/A11yDesignReviewChecklist.md` in order. For each section, determine whether any issues are present in this design.

**If the check passes:** one sentence confirming why, citing the specific element or token.

**If the check fails:** describe the specific issue — name the element, the color value, the missing annotation field. Vague findings ("contrast seems low") are not useful. Cite exact values where you can see them (e.g. "the deemphasized text at `rgba(20, 9, 43, 0.7)` will lose its transparency in HCM"). If this overlaps with an unresolved team comment, include it in your findings and attribute it: *(Previously raised by @[Name])* — the designer needs one complete list of open issues, not two partial ones. If the element is an `INSTANCE` and the same issue appears in sibling instances on the same screen, state that the fix should be made in the source component — fixing only this screen leaves the problem in every other screen that uses the component.

**Every finding must include at least one Figma link** to the specific frame or element it refers to. This is not optional. Never describe a problem without linking to where it lives. Use the format:
`https://www.figma.com/design/{fileKey}?node-id={nodeId}`
where `nodeId` uses `-` as separator (e.g. `24130-52964`). If a finding spans multiple frames (e.g. the same issue in several states), link to each frame. If you only have the ID of a parent container rather than the exact element, link to the container — a link to the right region is better than no link. Apply this to findings, questions, and the summary table.

**If you can't determine from the design** (e.g. a behavior depends on a hover state not shown): flag it as a question for the designer rather than a failure.

Screenshots are valuable — use `mcp__figma__get_screenshot` to zoom into specific elements when needed. The node IDs in the design context output can be used directly. Note: instance node IDs containing semicolons (like `I10978:9454;10978:9134`) are not accepted by the screenshot tool — use only simple `number:number` node IDs.

## Step 6: Format the review

**Output discipline:** Your entire text output must be the formatted review below — nothing else. Do not narrate your progress, confirm that you have what you need, summarize what you're about to do, or add any text before or after the review block. The output is consumed programmatically; any prose outside the format will break the pipeline.

Use markdown throughout — headings, bold, tables, inline code, blockquotes. Every section uses a semantic heading level. Do not flatten the output to plain prose.

```markdown
# Accessibility Design Review: [Feature/File Name]

**Figma:** [full URL provided by user]  
**Node reviewed:** [linked node — `https://www.figma.com/design/{fileKey}?node-id={nodeId}`]  
**Platform:** [Desktop / Android / iOS / Web]  
**Reviewer:** Claude Code (Mozilla accessibility team)

---

## What's covered

[1–3 sentences: what surface/feature this is, which states and themes are shown (use the canvas label text, not color inferences), and whether this is a first review or a follow-up.]

---

## Findings

### [Finding number]. [Short title] — `S2` / `S3` / `S4`

[2–4 sentences: what you saw, why it's a problem (citing WCAG criterion or Mozilla policy where relevant), what to do about it. Include a Figma link to the specific frame or element.]  
[If this was raised in an existing team comment: *(Previously raised by [@Name](https://www.figma.com/design/{fileKey}?commentId={id}))* ]

[Repeat for each finding]

---

## Questions for the designer

1. [Question — include a Figma link to the relevant frame if applicable]

[Omit this section entirely if there are no questions.]

---

## Summary

| # | Finding | Severity | Frame |
|---|---|---|---|
| 1 | [Short title] | `S2` | [Link](https://www.figma.com/design/{fileKey}?node-id={nodeId}) |
| 2 | [Short title] | `S3` | [Link](https://www.figma.com/design/{fileKey}?node-id={nodeId}) |

**[N] new findings. [M] existing open threads.**  
[One sentence on overall a11y readiness.]
```

### Severity scale (Mozilla)

| Severity | Meaning | Examples |
|---|---|---|
| `S2` | Must fix before ship | Contrast failure blocking use, modal without focus trap, hover-only control with no static affordance |
| `S3` | Should fix; fast-follow acceptable | Incomplete annotation, missing programmatic state |
| `S4` | Enhancement; not a blocker | AAA aspirational goal, minor label improvement |

## Notes on scope

- Include ALL unresolved issues — both newly found and any still-open team comments. The designer needs one complete picture.
- Flag annotation completeness: empty Role or Note fields in accessibility annotation frames are worth calling out.
- For HCM: check that the design doesn't use hardcoded hex colors in HCM mocks, that blur/gradients/shadows are removed, and that the right design system token families are used. See `accessible/docs/A11yDesignReviewChecklist.md` §HCM for the detailed checks.
- When in doubt about an element's behavior (is it a button or a link? does it open a new tab?), ask rather than assume.
- **Language for designers:** Write findings in plain language or using design system token names (e.g. `--button-background-color`). Do not use raw CSS system color keywords (`ButtonFace`, `ButtonText`, `CanvasText`, `SelectedItem`, etc.) — designers are not expected to know these. If you need to explain the fix, describe it in terms of token families ("the button token family") or in terms of the design tool ("use the HCM-adapted component from the Desktop Components 3 library").
