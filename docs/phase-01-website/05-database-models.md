# Phase 1 — Public Website
## Database Models

---

## Design Notes

- All content editable via Django Admin (or a customised admin dashboard) —
  no hardcoded content in templates
- Use Django's built-in apps/migrations; PostgreSQL as the backing database
  (per Phase 0 stack)
- Images handled via Pillow + Django `ImageField`, stored per Phase 0 media
  configuration
- Models below are Phase 1 scope only; staff/customer/reporting models belong
  to later phases

---

## App: `website` (suggested app name)

### MenuCategory
- `name` (CharField)
- `menu_type` (CharField choices: `food`, `drink`)
- `order` (PositiveIntegerField) — display order
- `is_active` (BooleanField, default True)

### MenuItem
- `category` (FK → MenuCategory)
- `name` (CharField)
- `description` (TextField, blank)
- `price` (DecimalField)
- `image` (ImageField, blank/null)
- `dietary_tags` (ManyToMany → DietaryTag, blank)
- `is_available` (BooleanField, default True)
- `order` (PositiveIntegerField)
- `created_at` / `updated_at` (DateTimeField auto)

### DietaryTag
- `name` (CharField, e.g. "Vegan", "Gluten Free", "Nut Free")
- `slug` (SlugField)

### GalleryImage
- `image` (ImageField)
- `caption` (CharField, blank)
- `alt_text` (CharField) — required for accessibility/SEO
- `order` (PositiveIntegerField)
- `is_active` (BooleanField, default True)
- `uploaded_at` (DateTimeField auto)

### Promotion
- `title` (CharField)
- `description` (TextField)
- `image` (ImageField, blank/null)
- `start_date` (DateField, null/blank)
- `end_date` (DateField, null/blank)
- `is_active` (BooleanField, default True)
- `created_at` (DateTimeField auto)

### Review
- `author_name` (CharField)
- `rating` (PositiveSmallIntegerField, 1–5)
- `content` (TextField)
- `source` (CharField, e.g. "Google", "Manual")
- `is_featured` (BooleanField, default False)
- `created_at` (DateTimeField auto)

### FAQItem
- `question` (CharField)
- `answer` (TextField)
- `order` (PositiveIntegerField)
- `is_active` (BooleanField, default True)

### CareerListing
- `title` (CharField)
- `description` (TextField)
- `employment_type` (CharField, e.g. "Full-time", "Part-time", "Casual")
- `is_active` (BooleanField, default True)
- `posted_at` (DateTimeField auto)
- `application_email` (EmailField, blank — falls back to site-wide contact
  email if empty)

### ContactSubmission
- `name` (CharField)
- `email` (EmailField)
- `phone` (CharField, blank)
- `message` (TextField)
- `submitted_at` (DateTimeField auto)
- `is_read` (BooleanField, default False)
- Submission triggers an email via Resend (see `07-integrations.md`); the
  record itself is retained for admin visibility/audit

### OpeningHours
- `day_of_week` (PositiveSmallIntegerField, 0=Monday … 6=Sunday)
- `open_time` (TimeField, null/blank — null means closed)
- `close_time` (TimeField, null/blank)
- `is_closed` (BooleanField, default False)

### SpecialHoursOverride
- `date` (DateField)
- `open_time` (TimeField, null/blank)
- `close_time` (TimeField, null/blank)
- `is_closed` (BooleanField, default False)
- `note` (CharField, blank — e.g. "Public Holiday")

### SiteSetting (singleton-style config model)
- `phone_number` (CharField)
- `contact_email` (EmailField)
- `address` (TextField)
- `google_maps_embed_url` (URLField, blank)
- `opentable_embed_url` (URLField, blank)
- `uber_eats_url` (URLField, blank)
- `doordash_url` (URLField, blank)
- `qr_ordering_url` (URLField, blank)
- `instagram_url` / `facebook_url` / other social (URLField, blank)

---

## Relationships Summary

- `MenuCategory` 1—N `MenuItem`
- `MenuItem` N—N `DietaryTag`
- All other models are largely standalone/content models with no complex
  relational structure in Phase 1

---

## Migration & Seed Data

- Provide initial migration with a seed/fixture for `OpeningHours` (7 rows,
  Mon–Sun) and a default `SiteSetting` row so the site is functional
  immediately after deployment
- Menu, gallery, and other content seeded by Mitch & Antler staff via the
  admin dashboard post-launch
