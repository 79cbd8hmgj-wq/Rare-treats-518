# Rare Treats 518 — Website Foundation

Astro + TypeScript website foundation for Rare Treats 518, a Troy, New York small business focused on homemade desserts, custom-order inquiries, seasonal treats, and local markets.

Savory food and catering are intentionally excluded from the public site until Misty defines and approves adding them.

## Current foundation

- Responsive homepage and six supporting pages
- Owner-editable JSON content
- Code-native pastel heart brand system
- Custom-order inquiry flow through the confirmed Instagram account
- Market announcement state for periods without confirmed dates
- Preview `noindex` protection
- Foundation and launch validation scripts
- Cloudflare Pages-compatible static output
- GitHub Actions validation

No fake food photography, copied social-media interface screenshots, live checkout, payment collection, database, account system, or unapproved business policy is included.

## Runtime

Use Node.js `22.22.2`.

```bash
nvm use
npm ci
npm run verify:content
npm run dev
```

Before merging a development patch:

```bash
npm run format:check
npm run check
npm run build
npm run verify:build
```

`npm run verify:launch` intentionally fails until the final business contact, owner-approved policies, publication-approved photography, preview setting, and production URL are ready.

## Cloudflare Pages

- Build command: `npm run build`
- Output directory: `dist`
- Node version: `22.22.2`
- Build environment variable: `PUBLIC_SITE_URL=https://approved-production-url`

## Owner-editable content

- Business identity, contact, social links, and ordering status: `content/site.json`
- Treat categories and descriptions: `content/treats.json`
- Market dates and event messaging: `content/events.json`
- Ordering and policy wording: `content/policies.json`
- Approved image registry: `content/gallery.json`

## Routes

- `/`
- `/treats`
- `/custom-orders`
- `/markets`
- `/about`
- `/faq`
- `/contact`

There is no public catering or savory-food route.

## Remaining launch inputs

- Original logo file
- Publication-approved product, market, and owner photographs
- Public business email
- Current menu and pricing language
- Lead times, deposits, payment methods, pickup and delivery rules
- Approved cancellation, refund, ingredient, and allergen wording
- Confirmed upcoming event dates
- Production URL or custom domain

See `docs/OWNER_CONTENT_INTAKE.md` and `docs/WEBSITE_DIRECTION.md` for the exact direction and content requirements.
