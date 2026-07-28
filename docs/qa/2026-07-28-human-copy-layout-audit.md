# Human Copy and Layout Audit

## Automated checks

- `npm ci`: pass
- `npm run verify:content`: pass
- `npm run test:voice`: pass
- `npm run verify:voice`: pass
- `npm run check`: pass
- `npm run build`: pass
- `npm run verify:build`: pass

GitHub Actions completed the full sequence and uploaded the validated production artifact.

## Viewports

- 320 × 800: pass
- 390 × 844: pass
- 430 × 932: pass
- 768 × 1024: pass
- 1440 × 1000: pass

The production artifact was rendered with Chromium at all five sizes for every public route, producing 35 full-page screenshots.

## Routes

- Home: pass
- Treats: pass; every number remains separate from its icon
- Custom Orders: pass
- Markets: pass
- About: pass
- FAQ: pass; disclosure controls work
- Contact: pass; Instagram and Facebook links are visible

## Interaction and console checks

- Mobile navigation: pass; all six links are visible inside a 390 × 844 viewport
- FAQ expansion: pass
- Horizontal overflow: none
- Treat number/icon collisions: none at any tested width
- Console errors: none
- Page errors: none
- Facebook link on Contact page: pass
- Facebook link in footer: pass

## Manual review findings

The first rendered pass found one remaining 320px issue: the longer Treats action put its arrow on a separate line. The link was shortened to “Ask about it →,” then the complete automated and visual sequence was repeated successfully.

A later copy review found stylized em dashes in two large headings and one treat description. Those sentences were rewritten with normal punctuation. The voice verifier now rejects em dashes and en dashes in customer-facing source files so the pattern cannot return.

## Copy review

The site uses brand-focused headlines, Misty’s first-person voice for descriptive sections, and neutral wording for payment, pickup, ingredients, and cancellation details. No prices, dates, policies, founder history, allergy accommodations, or services were invented.

The final read-through covered every page at mobile and desktop sizes. Repeated template phrases were removed, paragraphs remain short, and operational caveats are no longer repeated across several sections.
