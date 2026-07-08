#!/usr/bin/env python3
"""WCAG contrast helper for prototype review.

Computes WCAG 2.x contrast ratios. Handles solid hex pairs, and blends
semi-transparent foregrounds / overlays over a backing color before measuring
(forced-colors and rgba()/opacity values must be resolved to what the eye sees).

Usage:
  - As a quick check:   python3 contrast.py '#777777' '#ffffff'
  - As a batch:         edit the PAIRS list at the bottom and run `python3 contrast.py`
  - Import lin/L/ratio/blend into a one-off script.

Thresholds: 4.5:1 normal text, 3:1 large text (>=18pt or >=14pt bold) and
non-text/UI (borders, icon-affordances, focus indicators, state-vs-state).
A ratio of 4.4:1 is still a FAIL — do not pass near-misses.
"""
import sys


def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def L(hexstr):
    h = hexstr.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b):
    la, lb = L(a), L(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def blend(fg, alpha, bg):
    """Composite fg at the given alpha (0..1) over an opaque bg, return hex.

    Use for rgba() text, opacity<1 layers, and translucent overlays/scrims
    before measuring contrast.
    """
    h1, h2 = fg.lstrip('#'), bg.lstrip('#')
    out = []
    for i in (0, 2, 4):
        f = int(h1[i:i + 2], 16)
        b = int(h2[i:i + 2], 16)
        out.append(round(f * alpha + b * (1 - alpha)))
    return '#%02x%02x%02x' % tuple(out)


def report(pairs):
    """pairs: list of (label, fg_hex, bg_hex, threshold)."""
    print(f"{'PAIR':56} {'RATIO':>6}  THRESH  RESULT")
    for name, fg, bg, th in pairs:
        r = ratio(fg, bg)
        print(f"{name:56} {r:6.2f}   {th:>4}   {'PASS' if r >= th else 'FAIL'}")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(f"{ratio(sys.argv[1], sys.argv[2]):.2f}:1")
        sys.exit(0)

    # Edit this list per review. Example shape:
    PAIRS = [
        ("Body text #1c1b22 / white", "#1c1b22", "#ffffff", 4.5),
        ("Secondary text #777 / white", "#777777", "#ffffff", 4.5),
        ("Input border #cfc8dd / white (non-text 3:1)", "#cfc8dd", "#ffffff", 3.0),
        ("Primary button white / purple #9059ff", "#ffffff", "#9059ff", 4.5),
    ]
    report(PAIRS)
    # Example of resolving a translucent overlay before measuring:
    # scrim = blend('#ffffff', 0.14, '#2b2a33')
    # print('button-on-dark:', f"{ratio('#ffffff', scrim):.2f}:1")
