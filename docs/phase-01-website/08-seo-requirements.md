# Phase 1 — Public Website
## SEO Requirements

---

## Goals

- Rank well for local search terms (e.g. "café near me", "[suburb] café",
  "Mitch & Antler")
- Fast page loads on mobile networks
- Fully crawlable/indexable by search engines
- Rich presentation in search results (structured data, meta tags)

---

## On-Page SEO

- Unique, descriptive `<title>` and meta description per page
- Single `<h1>` per page, logical heading hierarchy (h2/h3 nested correctly)
- Descriptive, keyword-relevant URL slugs (see `03-sitemap-navigation.md`)
- Alt text required on all content images (menu items, gallery, promotions)
- Internal linking between related pages (e.g. Home → Menu, Menu → Booking)

---

## Technical SEO

- Server-rendered HTML (Django templates) — no reliance on client-side
  rendering for indexable content
- `robots.txt` configured to allow indexing of public pages, disallow `/admin/`
- XML sitemap (`django.contrib.sitemaps`) auto-generated and submitted to
  Google Search Console
- Canonical URLs set on every page to avoid duplicate content issues
- HTTPS enforced site-wide (via Cloudflare/Phase 0 deployment config)
- 301 redirects for any legacy/renamed URLs (if migrating from an existing
  site)
- Custom 404 page

---

## Structured Data (Schema.org / JSON-LD)

- `Restaurant` / `LocalBusiness` schema on Home/Contact (name, address, phone,
  opening hours, price range, cuisine)
- `Menu` schema on Menu page where practical
- `FAQPage` schema on FAQ page
- `Review`/`AggregateRating` schema on Reviews section (only if reviews are
  genuine and sourced appropriately — do not fabricate ratings)

---

## Local SEO

- Consistent NAP (Name, Address, Phone) across the website, Google Business
  Profile, and any directory listings
- Opening hours on-site kept in sync with Google Business Profile (manual
  process initially; automation is a future consideration)
- Google Maps embed on Contact/Home

---

## Performance Targets

- Lighthouse Performance score ≥ 90 (mobile)
- Lighthouse SEO score ≥ 95
- Lighthouse Accessibility score ≥ 90
- Core Web Vitals (field or lab data) within "Good" thresholds:
  - LCP < 2.5s
  - CLS < 0.1
  - INP < 200ms
- Image optimisation: responsive images, modern formats (WebP), lazy loading
  for below-the-fold images (gallery, menu images)
- Static assets served via WhiteNoise/Cloudflare CDN with appropriate cache
  headers (per Phase 0 deployment config)

---

## Social/Sharing

- Open Graph tags (title, description, image) on every page for social
  sharing previews
- Twitter Card tags (summary_large_image) as a baseline

---

## Monitoring

- Google Search Console connected post-launch to monitor indexing, coverage
  issues, and search performance
- Periodic Lighthouse/PageSpeed Insights checks as part of the testing
  checklist (`09-testing-checklist.md`)
