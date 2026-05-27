# UI Design Principles  ·  Gothic II — NPC Studio (new UI)

All visual decisions for the `--new` UI follow the rules below. **Every concrete value — color, font, point size, spacing px, border width — lives in `ui_new/tokens.py`.** Nothing visual is hard-coded in QSS or in widget Python.

Aesthetic direction: **pixel-RPG**. Old-game chrome (chunky pixel bevels, bitmap typography, framed panels) plus Refactoring UI discipline (small fixed scales, limited saturated palette, hierarchy via size + weight + color, not via random chrome).

---

## 1. Token system

```
ui_new/tokens.py        ← source of truth (palette, fonts, sizes, spacing)
ui_new/theme.qss        ← template; refers to tokens via $name / ${name}
ui_new/theme.py         ← loads tokens, substitutes into QSS, applies QPalette
ui_new/widgets/*.py     ← read tokens directly for styles that can't be QSS
```

Token namespace, all flattened in `token_map()`:

| Prefix | Source | Example |
|--------|--------|---------|
| `col_*` | `COLORS` | `col_rust` → `#c44a20` |
| `font_*` | `FONTS` | `font_display` → `"Jersey 10", …` |
| `sz_*` | `SIZES` (pt) | `sz_tab` → `18` |
| `sp_*` | `SPACE` (px) | `sp_xl` → `24` |
| `bd_*` | `BORDER` (px) | `bd_width` → `2` |

Adding a new theme later: write `tokens_<name>.py` exposing the same shape, swap the import in `theme.apply()`.

---

## 2. Type system

Three voices. **One typeface per voice — no mixing within a category.**

| Voice | Family | Used for |
|-------|--------|----------|
| Display | **Jersey 10** | tabs, section titles, buttons, menu/status, viewport status |
| Body | **Pixelify Sans** | field labels, input text, list rows, checkboxes |
| Mono | **VT323** | code preview, numeric slider readouts |

All three TTFs are bundled in `ui_new/assets/fonts/` and registered at app start via `QFontDatabase`. Fallback to system serif/mono if missing.

### Size scale (pt) — small, fixed, used everywhere

| Token | pt | Where |
|-------|----|-------|
| `sz_label` / `sz_checkbox` / `sz_menu_item` / `sz_tooltip` / `sz_body` | 13 | field labels, checkbox text, menu items |
| `sz_field` / `sz_list_item` | 14 | input contents, list rows |
| `sz_status` | 15 | status bar |
| `sz_button` / `sz_menu` / `sz_viewport` / `sz_code` / `sz_section` | 16–17 | buttons, menu bar, section titles, code, viewport status |
| `sz_tab` / `sz_readout` | 18 | tab labels, slider numeric readout |

If a new element doesn't fit one of these sizes, **change the element**, don't add a new size.

---

## 3. Spacing scale (px) — multiples of 4

```
xxs=2  xs=4  sm=8  md=12  lg=16  xl=24  xxl=32  huge=48
```

Reach for the token, never type a literal px in Python or QSS. Form rows use `lg+4` vertically and `xl` horizontally — extracted in `widgets/form.py` so labels align across every tab.

---

## 4. Color contract

Two saturated colors do the talking; everything else is neutral walnut.

| Role | Token | Meaning |
|------|-------|---------|
| **Action / selection / active tab / focus fill** | `col_rust` (+ `_hi`, `_lo`) | primary attention |
| **Section titles / slider handle / numeric value / status text** | `col_gold` (+ `_hi`, `_lo`) | secondary attention, "value" indicator |
| Destructive | `col_blood` (+ `_hi`, `_lo`) | danger button only |
| Page / panel / hover / border / text | walnut ladder (`col_ink` → `col_body_hi`) | neutral structure |
| Code preview | `col_parchment` + `col_ink_dark` | the one light surface in the UI |

Refactoring UI rule applied: **don't depend on color alone**. Active tab has color *and* a brighter bevel; primary button has color *and* bigger contrast. State changes use color + bevel inversion (see §5).

---

## 5. Bevel system (pixel-RPG depth)

Every interactive element has 2px borders in one of three configurations:

| Style | Top + Left | Right + Bottom | Used by |
|-------|------------|----------------|---------|
| **Raised** | bevel highlight | ink shadow | buttons, tabs, group boxes, slider handle, scrollbar thumb, checkbox-when-checked |
| **Sunken** | ink shadow | bevel highlight | inputs, lists, code pane, slider groove, scrollbar gutter |
| **Pressed** | ink shadow | bevel highlight | buttons / handle while `:pressed` (inverts the raised state) |

Highlight color is `col_bevel` (or `col_rust_hi`, `col_gold_hi`, `col_blood_hi` for accented variants). Shadow is `col_ink` (or `_lo` cousins). Border width is always `bd_width` = 2.

No `border-radius`. No gradients. No drop-shadows.

---

## 6. Layout

- **Window:** 1600 × 1000 default; 1280 × 820 minimum (from `WINDOW` token).
- **Splitters:** main pane (form tabs ↔ viewport+preview, horizontal); right pane (viewport ↔ preview, vertical). 2px handles, hover ember.
- **View margins:** `xl` (24 px) all around; sections separated by `xxl` (32 px) top margin.
- **Form rows:** `xl` horizontal between label and field; `lg+4` vertical between rows; label column min-width 140 px so columns align across tabs.
- **Tabs:** 4px right margin between tabs (`sp_xs`); chunky bevel; uppercase letter-spaced.

---

## 7. Refactoring UI principles applied

1. **Pick a scale, stick to it.** Type and spacing are quantised to the tables above; no off-scale values.
2. **Hierarchy by size + weight + color, not by chrome.** Section titles are gold + bigger + display font; field labels are smaller + body font. No decorative dividers.
3. **One primary action stands out.** Primary buttons use `col_rust` fill + rust bevel. Everything else is ghost-walnut. Add only when the action is genuinely primary (Add Item, Load Mesh, Save).
4. **Limited palette, used saturated.** Two saturated colors (rust + gold) appear repeatedly. Neutrals are warm walnut, not gray.
5. **Avoid pure black / pure white.** Deepest shadow is `col_ink` `#0a0604`; brightest cream is `col_body_hi` `#fde9b5`; parchment is `#ece0c0`.
6. **Whitespace as a feature.** Outer view margins generous, section gaps deliberate.
7. **No useless chrome.** Status text is short. Section names are one word. Buttons say `Add`, `Remove`, `Load`, not `Add Item` / `Remove Selected` / `Load Mesh from File…`.

---

## 8. Adding a widget

1. If it can be styled in QSS → add the selector to `theme.qss` using tokens.
2. If it needs runtime values (font, color in styleSheet string, or non-QSS API like VTK background) → import `COLORS`, `FONT_FAMILY`, `SIZES`, `SPACE` from `ui_new.tokens` and pull values.
3. Never use a literal hex or px in either layer.

---

## 9. Future theme switch

When ready: build `ui_new/tokens_<name>.py` with the same dict shape. Change `theme.apply()` to accept a token-module name (or read it from `QSettings`). The QSS template, palette setup, and widget Python all read through `tokens` — no other edits needed.
