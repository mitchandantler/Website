# Phase 1 — Public Website
## Integrations

---

## OpenTable (Booking)

- Purpose: allow customers to book a table
- Implementation: embedded OpenTable widget (iframe/JS snippet) on `/booking/`,
  and/or a "Book a Table" CTA linking directly to the Mitch & Antler OpenTable
  page
- Configuration: OpenTable embed/URL stored in `SiteSetting.opentable_embed_url`
  so it can be updated without a deployment
- Fallback: if the embed fails to load or is not configured, show restaurant
  phone number and a link to Contact as a manual booking fallback
- No booking data is stored in our database in Phase 1 — OpenTable is the
  system of record for reservations

---

## Uber Eats

- Purpose: link out to existing Uber Eats storefront for online ordering
- Implementation: simple outbound link/button, URL stored in
  `SiteSetting.uber_eats_url`
- No API integration, order data, or menu sync in Phase 1 — this is a
  navigation link only

---

## DoorDash

- Same pattern as Uber Eats: outbound link only, URL stored in
  `SiteSetting.doordash_url`

---

## QR Ordering Link

- Purpose: link to an in-house or third-party QR ordering system (table-side
  ordering)
- Implementation: outbound/deep link stored in `SiteSetting.qr_ordering_url`
- Full QR ordering system build-out is tracked separately under Phase 5
  (Future Expansion) — Phase 1 only needs to link to it

---

## Google Maps

- Purpose: show restaurant location
- Implementation: embedded Google Maps iframe using
  `SiteSetting.google_maps_embed_url`, plus a "Get Directions" link
- No Google Maps API key/JS SDK required for a basic iframe embed; only
  needed if richer interactivity is required later

---

## Resend (Email)

- Purpose: transactional email for the Contact form
- Trigger: on `ContactSubmission` creation, send:
  - Notification email to the site's admin contact address
  - (Optional) confirmation email to the customer acknowledging receipt
- Configuration: Resend API key stored as an environment variable per Phase 0
  (`Environment Variables`) — never hardcoded or committed to the repo
- Failure handling: if Resend fails, the `ContactSubmission` record must still
  be saved; email delivery failure should not block form submission, but
  should be logged (per Phase 0 `Logging`) so admin can follow up manually

---

## Social Links

- Purpose: outbound links to Instagram, Facebook, etc. shown in header/footer
- Implementation: URLs stored in `SiteSetting`, rendered conditionally (only
  show icons for platforms that have a URL configured)

---

## Reviews (Future Automation Note)

- Phase 1: reviews are manually curated via the admin dashboard
- Future consideration (not in scope now): pulling reviews automatically from
  Google Places API or similar — flagged for potential Phase 4/5 work if
  desired

---

## Integration Principles

- All third-party URLs/keys are configurable via `SiteSetting` or environment
  variables — never hardcoded in templates or Python code
- Prefer simple outbound links/embeds over deep API integrations in Phase 1;
  deeper integrations (order sync, live table availability, etc.) are
  explicitly deferred to later phases
- Any API keys/secrets follow Phase 0 security and environment variable
  conventions
