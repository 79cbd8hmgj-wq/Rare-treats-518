# Rare Treats 518 — Website Foundation

Astro + TypeScript foundation for Rare Treats 518, an owner-led homemade dessert business based in Troy, New York.

The project follows the same staged approach used for LRL Photography and Good Intentions: owner-editable content, reusable layouts, Cloudflare Pages deployment, automated validation, and customer-facing features enabled only after the business information is confirmed.

## Current public scope

- Homemade desserts and baked treats
- Custom-order inquiries
- Markets and community events
- Owner and brand story
- FAQ and working policies

Savory food and catering are intentionally disabled and hidden from all public navigation and copy.

## Runtime

Use Node.js `22.22.2`.

```bash
nvm use
npm install
npm run verify:content
npm run dev
```

Before merging a development patch:

```bash
npm run verify:content
npm run check
npm run build
```

`npm run verify:launch` is expected to fail during the foundation stage. It blocks launch until copy, photography, contact details, custom-order terms, policies, and the production URL are approved.

## Cloudflare Pages

- Build command: `npm run build`
- Output directory: `dist`
- Node version: `22.22.2`
- Build environment variable: `PUBLIC_SITE_URL=https://your-production-url`

## Owner-editable content

Business information, feature flags, navigation, treat categories, custom-order guidance, market information, policies, and launch checks are stored in `content/site.json`.

The `catering` and `savoryFood` feature flags must remain `false` until Misty explicitly approves adding those services.

## Routes

- `/`
- `/treats`
- `/custom-orders`
- `/markets`
- `/about`
- `/policies`

## Visual assets

The foundation uses a temporary code-native pastel heart and clearly labeled photo slots. No fake food photography, stock food photography, or scraped social-media images are committed. Original publication-approved logo and photography should replace temporary artwork before launch.

## Remaining launch inputs

See `docs/OWNER_CONTENT_INTAKE.md` for the complete list. The most important missing items are:

- Original logo and approved photographs
- Official contact information
- Current menu and pricing
- Order lead times and payment terms
- Pickup or delivery rules
- Allergen language and approved policies
- Confirmed market dates
- Owner-approved biography and website copy
- Production URL or custom domain
