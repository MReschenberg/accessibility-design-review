# Firefox Design System Component Libraries

This page describes the Figma component libraries used by the Firefox design team and their accessibility support status — in particular, which libraries automatically adapt to High Contrast Mode (HCM).

For background on HCM and the token system, see [Colors and High Contrast Mode](ColorsAndHighContrastMode.md).

---

## Desktop Components 3 (DC3)

Desktop Components 3 is the primary Firefox desktop component library. All components in DC3 are built on Desktop Styles tokens, which include a `tokens-forced-colors` cascade layer. This means DC3 components automatically adapt to HCM without requiring explicit `forced-colors` overrides in the component's CSS.

The [Desktop Styles tokens table](https://firefoxux.github.io/firefox-desktop-components/?path=/story/docs-tokens-table--default) is the authoritative reference for which tokens are available and what CSS system colors they resolve to in forced-colors mode.

**HCM support:** Yes — full, via the `tokens-forced-colors` cascade layer.

---

## Nova

Nova is Firefox's newer cross-platform design system, used primarily for browser UI surfaces targeting both desktop and mobile. Nova's token system does not yet include a `forced-colors` cascade layer.

This means Nova-sourced components do **not** automatically adapt to HCM. Designs using Nova components must include explicit HCM mocks, and engineering handoff should not proceed without accessibility team review. Contact the Mozilla accessibility team in **#accessibility** on Slack before engineering handoff of any Nova-based surface.

**HCM support:** Not yet — Nova tokens do not include a `forced-colors` layer as of 2026.

---

## Desktop Styles Tokens

Not a component library, but the token source for all DC3 components.

The [Desktop Styles tokens table](https://firefoxux.github.io/firefox-desktop-components/?path=/story/docs-tokens-table--default) lists all available token names and their resolved values in light mode, dark mode, Increase Contrast, and High Contrast Mode. Use this table to verify that a given token has an HCM mapping before using it in a `forced-colors` override.
