# Phase 1 — Public Website
## Functional Requirements

---

## 1. Home Page

- Hero section (image/video, tagline, primary CTA)
- Highlight of featured items / current promotions
- Quick links to Menu, Booking, Order Online
- Opening hours summary
- Location map preview
- Social proof (reviews snippet)

## 2. About

- Story / history of Mitch & Antler
- Team / values section (optional images)
- Location and contact summary

## 3. Food Menu

- Categorised menu items (e.g. Breakfast, Lunch, Snacks)
- Item name, description, price, dietary tags (vegan, gluten free, nut free, etc.)
- Item images (optional per item)
- Managed entirely through the admin dashboard

## 4. Drink Menu

- Categorised drink items (coffee, tea, cold drinks, alcohol if applicable)
- Same structure as Food Menu (name, description, price, tags)

## 5. Gallery

- Grid of images (food, venue, events)
- Admin-manageable (upload/remove/reorder)
- Lightbox view on click
- Lazy-loaded for performance

## 6. Functions & Events

- Static/CMS-managed content describing function/event hosting
- Enquiry form or link to Contact
- Optional gallery of past events

## 7. Special Offers / Promotions

- List of active promotions, managed via admin dashboard
- Optional start/end dates to auto-expire promotions
- Featured on Home Page when active

## 8. Booking (OpenTable Integration)

- Embedded OpenTable widget or deep link
- Fallback contact-based booking if OpenTable unavailable
- See `07-integrations.md` for integration details

## 9. Order Online

- QR Ordering link (points to external/future ordering system)
- Uber Eats link
- DoorDash link
- Clear presentation of order options on Menu and Home pages

## 10. Reviews

- Display of curated/aggregated customer reviews
- Manually curated via admin dashboard (Phase 1) — future phases may automate
  pulling from Google/third-party review APIs

## 11. FAQ

- Static list of frequently asked questions, managed via admin dashboard
- Expand/collapse (accordion) UI

## 12. Careers

- List of current openings (managed via admin dashboard)
- Application method: email link or simple application form

## 13. Contact

- Contact form (name, email, message) — submissions emailed via Resend
- Phone, email, address
- Google Maps embed
- Opening hours
- Social media links

## 14. Opening Hours

- Structured hours by day, manageable via admin dashboard
- Support for special/holiday hours override

## 15. Social Links

- Configurable links to social platforms (Instagram, Facebook, etc.), shown in
  header/footer

## 16. Admin Dashboard (Content Management)

- See `06-admin-dashboard-requirements.md` for full detail
- Staff can manage: Menu items, Categories, Promotions, Gallery, FAQ, Careers,
  Reviews, Opening Hours, Contact submissions

## 17. SEO

- See `08-seo-requirements.md`

---

## Non-Functional Requirements

- Mobile responsive across all pages
- Page load performance targets defined in `08-seo-requirements.md`
- Accessible (semantic HTML, alt text on images, keyboard navigable)
- Secure (CSRF protection, input validation, sanitised admin inputs)
- All content editable without direct code/database access
