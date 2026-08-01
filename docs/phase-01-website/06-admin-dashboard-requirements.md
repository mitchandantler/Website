# Phase 1 — Public Website
## Admin Dashboard Requirements

---

## Approach

Phase 1 uses a customised **Django Admin** as the content management interface
rather than a bespoke admin UI. This keeps development effort focused on the
public website while still giving Mitch & Antler staff full control over
content. A dedicated staff-facing dashboard (custom UI) can be considered in
Phase 2 once staff management features begin, at which point it may
supersede Django Admin for day-to-day use.

---

## Access & Permissions

- Django's built-in auth (`User`, `Group`, `Permission`) used for Phase 1
- Two initial roles:
  - **Owner/Admin** — full access to all models below
  - **Content Editor** — access to content models (Menu, Gallery, Promotions,
    FAQ, Careers, Reviews) but not `SiteSetting` or user management
- Detailed role/permission architecture matures in Phase 0 (`User Roles`,
  `Permissions`) and Phase 2 (Staff Management) — Phase 1 only needs these two
  roles to function

---

## Manageable Content

Staff must be able to, without developer involvement:

- **Menu**: create/edit/delete categories and items, set price, description,
  dietary tags, availability, image, and display order
- **Gallery**: upload/remove/reorder images, set captions and alt text
- **Promotions**: create/edit/delete, set active window (start/end date),
  toggle active flag
- **Reviews**: add/edit/delete, mark as featured
- **FAQ**: create/edit/delete, reorder
- **Careers**: post/close job listings
- **Contact Submissions**: view submitted messages, mark as read
- **Opening Hours**: edit weekly hours and add special/holiday overrides
- **Site Settings**: update phone, email, address, map embed URL, OpenTable
  embed URL, delivery links (Uber Eats/DoorDash), QR ordering URL, social
  links

---

## Admin UX Requirements

- List views for content models should show key fields (name, active status,
  order) and support search/filter (e.g. filter Menu Items by category or
  availability)
- Inline editing of `order` fields where practical (drag-and-drop reordering
  is a nice-to-have, not required for launch — numeric order field is
  sufficient for v1)
- Image fields must show a thumbnail preview in the admin list and detail view
- `SiteSetting` should be presented as a single editable object (not a list),
  using Django's admin singleton pattern
- Clear labelling and help text for non-technical users (e.g. explain what
  "Active" toggles do, explain image size/format recommendations)

---

## Notifications

- New contact form submissions should trigger a notification (email via
  Resend) to the configured admin contact email, in addition to being stored
  in `ContactSubmission`

---

## Out of Scope for Phase 1

- Custom-built (non-Django-Admin) dashboard UI
- Role-based analytics/reporting views (Phase 4)
- Staff scheduling or payroll admin (Phase 2)
- Customer account management (Phase 3)

---

## Acceptance Criteria

- A Content Editor can perform all day-to-day content updates listed above
  without needing to touch code or the database directly
- All admin-editable models are registered in Django Admin with sensible
  `list_display`, `search_fields`, and `list_filter` configured
- Admin access requires authentication; Content Editor role cannot access
  `SiteSetting` or user/group management
