# Phase 1 — Public Website
## Testing Checklist

---

## Functional Testing

- [ ] Home page renders hero, featured promotions, quick links, hours summary
- [ ] About page renders correctly
- [ ] Food Menu displays all active categories/items with correct price,
      description, dietary tags
- [ ] Drink Menu displays all active categories/items correctly
- [ ] Inactive/unavailable menu items are hidden from the public site
- [ ] Gallery displays active images in correct order; lightbox opens/closes
      correctly
- [ ] Functions & Events page renders correctly
- [ ] Special Offers page displays only currently active promotions
      (respecting start/end dates)
- [ ] Booking page loads OpenTable embed; fallback shown if embed URL not
      configured
- [ ] Order Online links (Uber Eats, DoorDash, QR) open correct external URLs
- [ ] Reviews section displays featured reviews correctly
- [ ] FAQ accordion expands/collapses correctly; only active FAQs shown
- [ ] Careers page displays only active listings
- [ ] Contact form: valid submission succeeds, creates `ContactSubmission`,
      triggers Resend email
- [ ] Contact form: invalid submission shows appropriate inline validation
      errors
- [ ] Opening hours display correctly, including special/holiday overrides
- [ ] Social links only render when configured; open in new tab

## Admin Dashboard Testing

- [ ] Content Editor role can manage Menu, Gallery, Promotions, FAQ, Careers,
      Reviews, Opening Hours
- [ ] Content Editor role is blocked from `SiteSetting` and user management
- [ ] Owner/Admin role has full access
- [ ] Image upload works and displays thumbnail preview in admin
- [ ] Contact submissions are visible and can be marked as read

## Responsive / Cross-Browser Testing

- [ ] All pages verified on mobile (< 640px), tablet (768px), desktop
      (≥1280px)
- [ ] Verified in Chrome, Safari, Firefox (desktop) and Safari iOS / Chrome
      Android (mobile)
- [ ] Sticky header and mobile nav (hamburger) function correctly

## Accessibility Testing

- [ ] All images have meaningful alt text (or empty alt for decorative
      images)
- [ ] Keyboard navigation reaches all interactive elements (nav, forms,
      accordion, lightbox)
- [ ] Colour contrast meets WCAG AA
- [ ] Form fields have associated labels and accessible error messaging

## SEO Testing

- [ ] Unique title/meta description per page
- [ ] Sitemap.xml accessible and correct
- [ ] robots.txt correctly disallows `/admin/`
- [ ] Structured data validates (Google Rich Results Test) for
      Restaurant/LocalBusiness, FAQPage
- [ ] Lighthouse scores meet targets in `08-seo-requirements.md`

## Security Testing

- [ ] CSRF protection verified on Contact form and any other POST endpoints
- [ ] Admin routes require authentication
- [ ] Input sanitisation verified (no raw HTML injection via
      description/content fields rendered unsafely)
- [ ] HTTPS enforced; HTTP requests redirect to HTTPS

## Integration Testing

- [ ] OpenTable embed loads correctly with production URL
- [ ] Uber Eats / DoorDash links point to correct, live storefronts
- [ ] Google Maps embed shows correct location
- [ ] Resend email delivery confirmed in staging and production

## Performance Testing

- [ ] PageSpeed/Lighthouse run on Home, Menu, Gallery pages (heaviest pages)
- [ ] Images lazy-load below the fold
- [ ] Static assets cached/served via CDN correctly

## Pre-Launch Sign-off

- [ ] All above checks passed in staging
- [ ] Content populated (menu, hours, contact details, at least one
      promotion, reviews, FAQ) by Mitch & Antler staff
- [ ] DNS/Cloudflare cutover plan confirmed (see Phase 0 `07-deployment.md`)
- [ ] Rollback plan confirmed in case of post-launch issues
