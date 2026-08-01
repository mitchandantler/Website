# Phase 1 — Public Website
## UI/UX Specification

---

## Design Principles

- Mobile-first: design and build for small screens first, then scale up
- Warm, café-appropriate aesthetic — approachable, appetite-appealing imagery,
  generous whitespace
- Consistency: shared design tokens (colour, type, spacing) reused across all
  pages and future phases
- Accessibility: WCAG 2.1 AA as a baseline target

---

## Design Tokens

Colour, type scale, and spacing tokens should be defined once (Tailwind config)
and reused across the whole platform, not just Phase 1. Suggested categories:

- Brand colours (primary, secondary, accent)
- Neutral/greyscale palette (backgrounds, borders, text)
- Semantic colours (success, warning, error, info) — for forms and admin UI
- Type scale (headings h1–h6, body, small/caption)
- Spacing scale (consistent with Tailwind's default spacing scale unless
  overridden)
- Border radius and shadow scale (for cards, buttons, modals)

Exact brand colour values, fonts, and logo assets to be supplied by Mitch &
Antler or their brand guidelines. Until supplied, use neutral placeholder
values and isolate them in the Tailwind config so they're a single-point swap.

---

## Layout

- Max content width container (e.g. 1280px) with responsive gutters
- 12-column grid for desktop layouts, single column stacking on mobile
- Consistent section vertical rhythm (padding between page sections)

---

## Components (Shared / Reusable)

- Header / Navigation bar (sticky, responsive)
- Footer
- Buttons (primary, secondary, ghost/link style)
- Cards (menu item card, gallery card, offer card, review card)
- Accordion (FAQ)
- Modal / Lightbox (gallery)
- Form fields + validation states (contact form)
- Alert / toast notifications (form submission success/error)
- Badge/tag (dietary tags on menu items, "New" / "Limited Time" on offers)
- Section heading pattern (eyebrow text + heading + optional subheading)

All shared components should live in a common Django template/component layer
so later phases (Staff, Customer Platform) can reuse the same design system.

---

## Page-Level UX Notes

**Home**
- Hero with strong CTA (Book a Table / Order Online)
- Do not bury Booking/Order Online below the fold

**Menu**
- Filter/tag by dietary requirement (nice-to-have, not blocking for launch)
- Prices clearly aligned, legible at a glance
- Category tabs or anchored sections for quick navigation

**Gallery**
- Responsive grid (masonry or fixed grid), lazy-loaded images
- Lightbox for full-size viewing

**Booking**
- Minimal friction — embed OpenTable directly if possible, avoid extra clicks

**Contact**
- Form validation with inline error messages
- Clear success confirmation after submission

**Admin Dashboard**
- Prioritise clarity and speed for non-technical staff over visual polish
- Use Django Admin (customised) rather than building a bespoke admin UI in
  Phase 1, per `06-admin-dashboard-requirements.md`

---

## Responsive Breakpoints

Align with Tailwind defaults unless a specific need arises:

- sm: 640px
- md: 768px
- lg: 1024px
- xl: 1280px
- 2xl: 1536px

---

## Imagery Guidelines

- Optimise all images (WebP where possible, responsive `srcset`)
- Consistent aspect ratios per component (e.g. menu item thumbnails, gallery
  tiles)
- Alt text required for every content image (SEO + accessibility)
