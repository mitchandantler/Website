# Phase 1 — Public Website
## Sitemap & Navigation

---

## Site Map

```
/                          Home
/about/                    About
/menu/                     Menu (Food + Drink)
/menu/food/                Food Menu (optional dedicated URL, or anchor on /menu/)
/menu/drinks/               Drink Menu (optional dedicated URL, or anchor on /menu/)
/gallery/                  Gallery
/functions-events/         Functions & Events
/offers/                   Special Offers / Promotions
/booking/                  Booking (OpenTable embed/redirect)
/order-online/             Order Online (Uber Eats / DoorDash / QR)
/reviews/                  Reviews
/faq/                      FAQ
/careers/                  Careers
/contact/                  Contact

/admin/                    Django Admin Dashboard (staff only)
```

---

## Primary Navigation (Header)

- Home
- About
- Menu
- Gallery
- Offers
- Booking (styled as primary CTA button)
- Order Online (styled as secondary CTA button)
- Contact

---

## Footer Navigation

Column 1 — Explore
- About
- Menu
- Gallery
- Functions & Events
- Careers

Column 2 — Visit
- Contact
- Opening Hours
- Booking
- FAQ

Column 3 — Connect
- Social Links (Instagram, Facebook, etc.)
- Reviews
- Newsletter (future)

Bottom Bar
- Copyright
- Privacy Policy (future)
- Terms (future)

---

## URL / Routing Conventions

- Lowercase, hyphen-separated slugs
- Trailing slash on all URLs (Django default convention)
- No query-string-based page routing for core pages
- Menu items, gallery images, offers, and FAQ entries are database-driven and do
  not require individual URLs unless a detail page is explicitly required

---

## Navigation Behaviour

- Sticky header on scroll (desktop + mobile)
- Mobile: collapsible hamburger menu
- Active page indicated in nav (aria-current="page")
- Booking and Order Online remain visible/accessible from every page (header
  and/or floating action button on mobile)

---

## Breadcrumbs

Not required for Phase 1 given shallow site depth (max 1 level). Revisit if
Menu or Gallery gain detail sub-pages.
