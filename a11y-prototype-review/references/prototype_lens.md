# The Prototype Lens — what's in scope and what isn't

A prototype is throwaway code built to communicate a design. Its markup is incidental and will be rebuilt. Reviewing the prototype's markup for accessibility defects therefore wastes the designer's time on things they don't own and engineering will replace. The value of a prototype review is catching the accessibility barriers baked into the **design decisions** — the things that survive the rebuild.

## The core test

For every candidate finding, ask:

> **"Would a clean, accessible rebuild fix this automatically?"**

- **Yes → out of scope** (it's a markup/implementation concern). Don't report it in a prototype-lens review.
- **No, the fix requires a design change → in scope.** Report it.

## What persists from prototype to production (IN SCOPE)

These are decisions the design carries forward; accessible markup alone won't fix them:

| Carried-over decision | Why markup can't fix it |
|---|---|
| **Colour values** | Contrast is a property of the chosen colours, not the markup. |
| **What meaning is encoded in colour** | If state/identity is shown only by hue, accessible markup still renders the same indistinguishable hues for colourblind users and the same fills that vanish in HCM. |
| **Labels & copy** | The words shown (and announced) are a content decision. |
| **Icons** | Which glyph means what is a design choice. |
| **Control type** | A thing designed as a button stays a button; sizes/affordances persist. |
| **Activation type** | Hover-to-reveal stays hover-to-reveal; auto-dismiss stays auto-dismiss; selection-triggered stays selection-triggered. This is the subtle one — see below. |
| **Feature flow** | The sequence of steps is the design. |
| **Spatial placement** | Where UI and feedback appear relative to the point of action. |
| **Timing** | How long transient feedback stays. |
| **Motion** | What animates and how. |

## What an accessible rebuild handles (OUT OF SCOPE for prototype-lens)

Do **not** report these as defects in a prototype-lens review:

- Non-semantic elements (`<div>`/`<span>` instead of `<button>`/`<a>`)
- Missing or wrong ARIA roles
- Keyboard operability of controls that are the right *type* (the rebuild makes the button keyboard-operable)
- Accessible name wiring (`aria-label`, `aria-labelledby`) — assuming the visible label is correct
- Programmatic label/control association (`<label for>`)
- Live-region plumbing (`aria-live`, `role="status"`) — the *existence* of an announcement is markup; see the nuance below
- Focus trap / `role="dialog"` / `aria-modal` mechanics
- Focus order, as long as it can follow the visual order the design implies

## The nuance: design requirements that look like markup

Some findings sit on the boundary. Frame them as **design requirements**, not markup defects:

- *"The copy succeeded with no visible change"* → the design must **specify that an outcome confirmation exists**, what it says, where it appears, and how long it lasts. That the announcement is implemented with `aria-live` is markup; that a perceivable confirmation must exist *and where/how long* is design.
- *"Hover reveals the only path to an action"* → activation type persists, so the design must provide a **non-hover affordance**. The rebuild can't invent an affordance the design didn't include.
- *"Escape closes some surfaces but not others"* → the **dismissal model** (what closes what, is there always a non-pointer way out) is a flow decision.
- *"Feedback appears bottom-centre while the action is top-of-window"* → **placement** is design; relocating it is a design change.

Rule of thumb: if the fix is "use the right element / add the attribute," it's markup (out). If the fix is "change the colour / move the thing / add an affordance / change the wording / lengthen the timing / provide a non-colour cue," it's design (in).

## Always confirm the scope with the user

Some users want a full-implementation audit of the prototype as-is. Ask. Default to the prototype lens when they call it a "prototype" or say the real version will be built separately. State the chosen scope in the report so the boundary of the feedback is explicit.
