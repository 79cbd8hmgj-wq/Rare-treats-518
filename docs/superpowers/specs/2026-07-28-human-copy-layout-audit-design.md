# Rare Treats 518: Human Copy and Layout Audit Design

## Goal

Refine the merged Rare Treats 518 website so it feels like a real local business owned by Misty rather than a polished template. The patch will also correct visual mistakes that remain after the mobile redesign, beginning with the overlapping number and treat icon on the Treats page.

## Approved voice direction

Use a mixed voice.

- Headlines stay short, warm, and brand-focused.
- Most descriptive body copy sounds like Misty speaking naturally in first person.
- Practical details such as payment, pickup, ingredients, and cancellations stay neutral and direct.
- The writing should feel conversational without becoming overly casual or slang-heavy.

### Voice examples

Use:

> I make cookies, brownies, dessert trays, gift bags, and seasonal treats for parties, holidays, markets, or whenever you want something sweet.

Avoid:

> Something sweet for the moment you are celebrating.

Use:

> Send me the date, how many people you are ordering for, and what kind of treats you have in mind.

Avoid:

> Every order starts as a conversation so the date, quantity, flavors, payment, and handoff can be confirmed before anything is promised.

## Copy rules

1. Prefer short sentences and everyday words.
2. Use contractions where they sound natural.
3. Remove abstract phrases such as “built around,” “limited by design,” “intentionally flexible,” and “the moment you are celebrating.”
4. Do not repeat the same operational caveat in several sections.
5. Do not invent prices, lead times, menu items, policies, or personal history.
6. Keep important uncertainty clear, but phrase it simply.
7. Let Misty’s name appear where it helps the site feel personal, not in every paragraph.
8. Keep paragraphs to roughly two or three sentences on mobile.
9. Preserve the current public scope: desserts, custom orders, seasonal treats, markets, and contact. Savory food and catering remain hidden.

## Visual audit approach

The patch will review every route at mobile and desktop widths, not just the issue already reported.

### Known Treats-page defect

The mobile layout currently places the small row number and the circular treat icon inside the same compact box. The icon visually covers the number.

The corrected structure will give the number its own fixed position outside the icon’s footprint. The preferred mobile composition is:

- number in a narrow left column,
- icon beside it or above the copy,
- title and description in the main column,
- availability and action beneath the copy.

The number must remain legible at 320px, 390px, and 430px widths.

### Site-wide visual checks

Review all seven routes for:

- overlapping elements,
- clipped text or icons,
- controls that look interactive but are not,
- uneven card heights,
- accidental large empty areas,
- headings that wrap awkwardly,
- unreadable text contrast,
- repeated visual patterns that make pages feel templated,
- desktop regressions caused by mobile overrides,
- horizontal overflow,
- footer and navigation consistency.

## Page-by-page copy and layout plan

### Home

Rewrite the hero and supporting sections so they sound like Misty introducing what she makes. Keep the pastel heart artwork, but remove broad marketing phrases. Shorten the custom-order explanation and market copy. Make each section add new information rather than repeating “message Misty” in different wording.

### Treats

Fix the number/icon collision. Rewrite category descriptions in plain language. Replace “A menu built to rotate” and “Limited by design” with more natural language. Keep categories broad because current inventory and prices are not finalized.

### Custom Orders

Change the page from procedural business language to a simple explanation of what to send and what happens next. Keep first-person copy in the introduction and neutral wording for payment, pickup, and policy details.

### Markets

Use warmer language about meeting Misty and seeing what she brought that day. Avoid generic phrases such as “the table changes every time you find it.” Keep the upcoming-date state honest and direct.

### About

Make the page feel more personal without inventing Misty’s history. Use only confirmed facts: her name, Troy location, owner-led business, homemade desserts, custom orders, and local events. Remove generic brand-language filler.

### FAQ

Make answers shorter and more conversational. Keep approved policy uncertainty intact. Avoid repeated phrases such as “confirmed individually” when a simpler answer works.

### Contact

Use direct, friendly wording. Explain that Instagram is the current contact method without discussing internal decisions about whether a business email or phone number may be published later.

## Content architecture

Existing owner-editable JSON remains the source of truth.

- `content/site.json` keeps confirmed business information.
- `content/treats.json` keeps category copy.
- `content/events.json` keeps event status and categories.
- `content/policies.json` keeps unapproved policy wording.

Page-specific display copy may remain in Astro files where it is structural rather than owner-maintained. Repeated customer-facing text should be centralized only when the same sentence is intentionally reused.

## Error handling and safety

- No unapproved operational claim will be added.
- Policy language will remain conservative while becoming easier to read.
- No price, ingredient, allergy accommodation, shipping, delivery radius, or event date will be invented.
- Preview-mode indexing protection remains unchanged.
- Hidden food and catering services remain absent from public routes and navigation.

## Testing

### Automated

Run:

- `npm ci`
- `npm run verify:content`
- `npm run check`
- `npm run build`
- `npm run verify:build`

### Visual

Render all seven routes at:

- 320px mobile,
- 390px mobile,
- 430px mobile,
- 768px tablet,
- 1440px desktop.

Check:

- no horizontal overflow,
- no number/icon overlap,
- no clipped headings or buttons,
- no console errors,
- mobile menu behavior,
- FAQ disclosure behavior,
- readable line lengths and paragraph spacing,
- consistent page rhythm.

## Non-goals

This patch will not add:

- real product photography,
- prices,
- checkout,
- a website order form,
- a business email or phone number,
- new services,
- savory food or catering,
- invented founder history.

## Completion criteria

The patch is ready when:

1. Every page has been reviewed and rewritten where needed.
2. The Treats-page icon and number never overlap at supported widths.
3. The site reads naturally aloud and avoids repeated marketing-template language.
4. All automated checks pass.
5. All routes pass the visual review at the listed widths.
6. The pull request includes before-and-after notes for major copy and layout changes.
