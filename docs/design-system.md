# FinTrack Design System

This document is the contract between visual design and the server-rendered interface. It does not imply that the retained v1 templates already comply.

## Color tokens

| Token | Light | Dark | Purpose |
|---|---:|---:|---|
| `bg` | `#F7F8FA` | `#0D131A` | Application background |
| `panel` | `#FFFFFF` | `#151F29` | Cards and drawers |
| `panel-2` | `#F2F5F7` | `#101820` | Secondary surfaces |
| `line` | `#DCE3E8` | `#293845` | Borders and grids |
| `text` | `#17212B` | `#EAF0F4` | Primary text |
| `muted` | `#6B7785` | `#94A3AF` | Secondary text and transfers |
| `primary` | `#315A8C` | `#79A7E3` | Brand, links, selection, charts |
| `good` | `#16865C` | `#42C58A` | Positive financial state only |
| `bad` | `#D04A55` | `#FF6B76` | Negative values and overruns |
| `warning` | `#D99120` | `#F2B84B` | Approaching a threshold |
| `critical` | `#C5682C` | `#FF9566` | Critical threshold |
| `info` | `#3D73C5` | `#6EA8FE` | Informational state |

Green is reserved for positive financial states, not branding. Category colors use a separate qualitative palette and never imply status.

## Financial semantics

- Below 70% budget utilization is `good`; 70–90% is `warning`; 90–100% is `critical`; above 100% is `bad`.
- One shared helper calculates budget tone; templates do not assign thresholds independently.
- Positive and negative amounts combine semantic color with explicit plus or minus signs.
- Transfers use a neutral tone and directional label.
- Turkish amounts use `1.234,56 ₺`, tabular figures, and right alignment.

## Typography and layout

- Interface: Inter with Segoe UI and system sans-serif fallbacks.
- Financial values: `ui-monospace`, SFMono-Regular, and Consolas.
- Spacing scale: 4, 8, 12, 16, 24, and 32 pixels.
- Card radius: 12 pixels; control radius: 8–9 pixels.
- Compact table rows: 40–44 pixels.
- Shadows communicate elevation only; glow and glassmorphism are excluded.

## Accessibility

- Navigation uses links; actions use buttons.
- Every interactive element has a visible `:focus-visible` state.
- Icon-only controls have accessible names.
- Progress indicators expose minimum, maximum, and current values.
- Inputs have associated visible labels; placeholders are not labels.
- States combine text or symbols with color.
- Interactive targets are at least 38 by 38 pixels.
- Body text meets WCAG AA contrast.

## Charts and forecasting integrity

- Deterministic cash-flow projection is labelled `Planned`, not `Predicted`.
- Prediction intervals appear only after a model is evaluated and calibrated.
- Charts include units, relevant axes, real/planned distinction, and an accessible text summary.
- Visual scales must not exaggerate change.

## Responsive navigation

- Above 900 pixels: persistent sidebar.
- At or below 900 pixels: bottom navigation for Home, Transactions, Add, Reports, and More.
- More opens a complete navigation surface; hiding the sidebar must not make destinations unreachable.

## Safe frontend implementation

- Prefer `textContent`, explicit DOM construction, and server-side escaping.
- Never copy prototype `innerHTML` renderers into production.
- Do not render user or model content with Jinja `safe` without a documented sanitizer.
- Avoid inline handlers and inline styles.
- Self-host browser dependencies required by production.
- Every fetch path has loading, empty, success, and recoverable error states.
- Generated frontend work is reviewed for security and accessibility before merge.
