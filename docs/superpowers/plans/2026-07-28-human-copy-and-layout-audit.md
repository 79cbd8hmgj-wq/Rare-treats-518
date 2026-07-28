# Human Copy and Layout Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the remaining visual defects across Rare Treats 518 and rewrite all customer-facing copy so the site sounds like Misty and a real local business rather than a polished template.

**Architecture:** Keep the existing Astro page structure and owner-editable JSON content model. Make focused copy and layout changes in the current pages, fix the Treats catalog markup so numbers and icons have separate layout space, and add a dependency-free voice-audit script that prevents the most robotic phrases from returning.

**Tech Stack:** Astro 7.0.9, TypeScript 5.9.3, Node 22.22.2, CSS, JSON, GitHub Actions.

## Global Constraints

- Use mixed voice: warm brand headlines, first-person descriptive copy where Misty speaks, and neutral practical wording for policies.
- Preserve the public scope: desserts, custom orders, seasonal treats, markets, About, FAQ, and Contact.
- Keep savory food and catering hidden.
- Do not invent prices, menu items, event dates, ingredients, allergy accommodations, delivery radius, founder history, email, phone number, or formal policies.
- Keep paragraphs short enough to read comfortably on mobile.
- Keep preview-mode indexing protection unchanged.
- Add no runtime dependency and no new frontend framework.
- The Treats page number and icon must remain separate and legible at 320px, 390px, and 430px.
- Every route must pass 320px, 390px, 430px, 768px, and 1440px visual review with no horizontal overflow.

---

## File Structure

**Create**

- `scripts/lib/voice-audit.mjs` — reusable text normalization and violation detection.
- `scripts/verify-voice.test.mjs` — dependency-free tests for the voice-audit functions.
- `scripts/verify-voice.mjs` — scans customer-facing source files and fails on banned template language or missing voice markers.
- `docs/qa/2026-07-28-human-copy-layout-audit.md` — records automated and visual QA results.

**Modify**

- `package.json` — adds `test:voice` and `verify:voice` scripts.
- `.github/workflows/validate.yml` — runs voice verification before build.
- `content/treats.json` — rewrites treat descriptions in plain language.
- `content/events.json` — makes the no-event state sound natural.
- `content/policies.json` — simplifies practical wording without adding promises.
- `content/site.json` — simplifies ordering labels while preserving confirmed facts.
- `src/pages/index.astro` — rewrites all homepage copy.
- `src/pages/treats.astro` — fixes catalog markup and rewrites page copy.
- `src/pages/custom-orders.astro` — rewrites the order flow in Misty’s voice.
- `src/pages/markets.astro` — rewrites market copy and empty-date state.
- `src/pages/about.astro` — makes the page personal without inventing history.
- `src/pages/faq.astro` — shortens and humanizes answers.
- `src/pages/contact.astro` — makes the contact page direct and friendly.
- `src/styles/mobile-polish.css` — removes the number/icon collision and corrects any new responsive issues found during QA.

---

### Task 1: Add a dependency-free voice audit library

**Files:**
- Create: `scripts/lib/voice-audit.mjs`
- Create: `scripts/verify-voice.test.mjs`
- Modify: `package.json`

**Interfaces:**
- Produces: `normalizeCopy(value: string): string`
- Produces: `findVoiceViolations(content: string, forbiddenPhrases: string[]): string[]`
- Consumes: Node built-ins only.

- [ ] **Step 1: Write the failing unit test**

Create `scripts/verify-voice.test.mjs`:

```js
import assert from "node:assert/strict";
import { findVoiceViolations, normalizeCopy } from "./lib/voice-audit.mjs";

assert.equal(
  normalizeCopy("Built Around Misty’s treats."),
  "built around misty's treats."
);

assert.deepEqual(
  findVoiceViolations(
    "The menu is intentionally flexible and built around the occasion.",
    ["intentionally flexible", "built around", "limited by design"]
  ),
  ["intentionally flexible", "built around"]
);

assert.deepEqual(
  findVoiceViolations(
    "I make cookies, brownies, and seasonal treats in Troy.",
    ["intentionally flexible", "built around"]
  ),
  []
);

console.log("Voice audit tests passed.");
```

- [ ] **Step 2: Run the test and verify it fails**

Run:

```bash
node scripts/verify-voice.test.mjs
```

Expected: failure with `ERR_MODULE_NOT_FOUND` for `scripts/lib/voice-audit.mjs`.

- [ ] **Step 3: Implement the library**

Create `scripts/lib/voice-audit.mjs`:

```js
export function normalizeCopy(value) {
  return value
    .replace(/[’‘]/g, "'")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

export function findVoiceViolations(content, forbiddenPhrases) {
  const normalizedContent = normalizeCopy(content);

  return forbiddenPhrases.filter((phrase) =>
    normalizedContent.includes(normalizeCopy(phrase))
  );
}
```

- [ ] **Step 4: Add the unit-test command**

Add to `package.json` scripts:

```json
"test:voice": "node scripts/verify-voice.test.mjs"
```

Keep all existing scripts unchanged.

- [ ] **Step 5: Run the unit test**

Run:

```bash
npm run test:voice
```

Expected: `Voice audit tests passed.`

- [ ] **Step 6: Commit**

```bash
git add package.json scripts/lib/voice-audit.mjs scripts/verify-voice.test.mjs
git commit -m "test: add customer copy voice audit"
```

---

### Task 2: Fix the Treats catalog collision and rewrite treat copy

**Files:**
- Modify: `content/treats.json`
- Modify: `src/pages/treats.astro`
- Modify: `src/styles/mobile-polish.css`

**Interfaces:**
- Consumes: `treats.categories` and `TreatIcon` exactly as they exist.
- Produces: `.catalog-mark`, `.catalog-number`, and `.catalog-copy` layout hooks.

- [ ] **Step 1: Record the current failing layout condition**

In the current mobile CSS, confirm these rules exist:

```css
.catalog-row .number > span {
  position: absolute;
}

.catalog-row .number .icon {
  width: 2.65rem;
  height: 2.65rem;
}
```

Expected: the number and icon share the same 4.25rem box and can overlap.

- [ ] **Step 2: Replace the Treats catalog markup**

In `src/pages/treats.astro`, replace:

```astro
<div class:list={["number", `tone-${(index % 3) + 1}`]}><span>0{index + 1}</span><TreatIcon icon={category.icon} /></div>
<div>
  <h2>{category.name}</h2>
  <p class="lede">{category.longDescription}</p>
</div>
```

with:

```astro
<div class:list={["catalog-mark", `tone-${(index % 3) + 1}`]}>
  <span class="catalog-number">0{index + 1}</span>
  <TreatIcon icon={category.icon} />
</div>
<div class="catalog-copy">
  <h2>{category.name}</h2>
  <p class="lede">{category.longDescription}</p>
</div>
```

- [ ] **Step 3: Rewrite the Treats page introduction and seasonal section**

Use this page copy:

```astro
<p class="eyebrow">What I make</p>
<h1>Pick a favorite—or ask what’s new.</h1>
<p class="lede">{treats.intro}</p>
```

Use this seasonal section copy:

```astro
<p class="eyebrow">Seasonal treats</p>
<h2>Some favorites only show up for a little while.</h2>
```

```astro
<p class="lede">I share holiday boxes, themed gift bags, limited flavors, and market specials on Instagram when they’re ready.</p>
<a class="button" href="https://www.instagram.com/raretreats518/" target="_blank" rel="noreferrer">See what’s new</a>
```

- [ ] **Step 4: Replace `content/treats.json` with natural category copy**

Use:

```json
{
  "intro": "I change the menu with the season and with what I’m making for each event. These are the main kinds of treats you can ask me about.",
  "categories": [
    {
      "slug": "cookies",
      "name": "Cookies",
      "shortDescription": "Soft cookies, decorated cookies, and flavors that change through the year.",
      "longDescription": "Soft cookies, decorated cookies, treat bags, and flavors that change throughout the year.",
      "icon": "cookie",
      "availability": "rotating"
    },
    {
      "slug": "brownies-bars",
      "name": "Brownies & bars",
      "shortDescription": "Fudgy brownies, blondies, and layered bars.",
      "longDescription": "Fudgy brownies, blondies, and layered bars for sharing—or keeping to yourself.",
      "icon": "brownie",
      "availability": "rotating"
    },
    {
      "slug": "dessert-trays",
      "name": "Dessert trays",
      "shortDescription": "A mix of treats sized for your gathering.",
      "longDescription": "A mix of treats sized for your party, gathering, or work event.",
      "icon": "tray",
      "availability": "custom-order"
    },
    {
      "slug": "gift-bags",
      "name": "Gift bags",
      "shortDescription": "Small packaged treats for gifts and favors.",
      "longDescription": "Small packaged treats for birthdays, holidays, favors, thank-yous, and just-because gifts.",
      "icon": "gift",
      "availability": "custom-order"
    },
    {
      "slug": "jars-more",
      "name": "Jars & more",
      "shortDescription": "Packaged treats and fun ideas that change often.",
      "longDescription": "Cookie jars, snack mixes, and other packaged treats when I have something fun in mind.",
      "icon": "jar",
      "availability": "limited"
    },
    {
      "slug": "seasonal",
      "name": "Seasonal specialties",
      "shortDescription": "Holiday flavors and short-run treats.",
      "longDescription": "Holiday flavors, themed packages, and short-run treats that only show up for a little while.",
      "icon": "sparkle",
      "availability": "seasonal"
    }
  ]
}
```

- [ ] **Step 5: Replace desktop catalog marker styles**

In `src/pages/treats.astro`, replace `.number` and `.number > span` with:

```css
.catalog-mark {
  display: grid;
  min-height: 7.5rem;
  grid-template-columns: 1.15rem 1fr;
  gap: 0.6rem;
  align-items: start;
  padding: 0.8rem;
  border-radius: 1.4rem;
}

.catalog-number {
  color: var(--blueberry-soft);
  font-size: 0.72rem;
  font-weight: 850;
  line-height: 1;
}

.catalog-mark :global(.icon) {
  align-self: center;
  justify-self: center;
}
```

Keep the existing tone classes.

- [ ] **Step 6: Replace the mobile collision rules**

In `src/styles/mobile-polish.css`, replace the current `.catalog-row .number` block and its child rules with:

```css
.catalog-row {
  grid-template-columns: 4.75rem minmax(0, 1fr) !important;
  gap: 0.8rem 1rem !important;
}

.catalog-row .catalog-mark {
  width: 4.75rem !important;
  min-height: 5.75rem !important;
  grid-template-columns: 1fr !important;
  gap: 0.45rem !important;
  justify-items: center;
  padding: 0.55rem !important;
}

.catalog-row .catalog-number {
  position: static !important;
  justify-self: start;
  font-size: 0.6rem !important;
}

.catalog-row .catalog-mark .icon {
  width: 2.65rem !important;
  height: 2.65rem !important;
}

.catalog-row .availability {
  grid-column: 2;
}
```

Delete every remaining mobile selector that targets `.catalog-row .number`.

- [ ] **Step 7: Build and inspect the generated Treats page**

Run:

```bash
npm run verify:content
npm run check
npm run build
npm run verify:build
```

Expected: all commands pass.

Render `/treats` at 320px, 390px, and 430px. Expected: every row number is fully visible and does not touch the circular icon.

- [ ] **Step 8: Commit**

```bash
git add content/treats.json src/pages/treats.astro src/styles/mobile-polish.css
git commit -m "fix: separate treat numbers from category icons"
```

---

### Task 3: Rewrite the homepage in Misty’s voice

**Files:**
- Modify: `src/pages/index.astro`

**Interfaces:**
- Consumes: existing `events`, `site`, and `treats` content.
- Produces: no new component or data interface.

- [ ] **Step 1: Replace the hero copy**

Use:

```astro
<p class="hero-location">Troy, New York</p>
<h1>Homemade treats for parties, holidays, and ordinary cravings.</h1>
<p class="lede">I make cookies, brownies, dessert trays, gift bags, and seasonal treats in Troy, New York. If you have a date or an idea, send me a message and we’ll figure out what fits.</p>
```

Change the buttons to:

```astro
<a class="button" href="/custom-orders">Ask about an order</a>
<a class="button button-secondary" href="/treats">See the treats</a>
```

- [ ] **Step 2: Replace the treat-section copy**

Use:

```astro
<p class="eyebrow">From the Rare Treats table</p>
<h2>What’s on the table changes.</h2>
```

```astro
<p>I rotate flavors and seasonal treats, so the website shows the kinds of things I make instead of a fixed menu.</p>
```

Change each card link from `See the details` to `Take a look`.

- [ ] **Step 3: Replace the custom-order copy**

Use:

```astro
<p class="eyebrow">Custom orders</p>
<h2>Tell me what you’re planning.</h2>
<p>Send the date, how many people you’re ordering for, and what sounds good. I’ll let you know what I can make and what it will cost.</p>
<a class="inline-link" href="/custom-orders">See what to send me →</a>
```

Replace the three steps with:

```astro
<li><span>01</span><div><h3>Send the basics</h3><p>The date, the occasion, how many people, and what you’re thinking about.</p></div></li>
<li><span>02</span><div><h3>We’ll figure it out</h3><p>I’ll reply with what I can make, the price, and the timing.</p></div></li>
<li><span>03</span><div><h3>Set the details</h3><p>Payment and pickup or delivery are arranged before the order is accepted.</p></div></li>
```

- [ ] **Step 4: Replace the market and founder copy**

Use:

```astro
<p class="eyebrow">Markets & pop-ups</p>
<h2>Come say hi at the next market.</h2>
<p class="lede">{events.announcement}</p>
```

Change `About market days` to `Find me at a market`.

Use this founder section:

```astro
<p class="eyebrow">Made in Troy</p>
<h2>Made by Misty in Troy.</h2>
```

```astro
<p class="lede">I’m Misty, the person behind Rare Treats 518. I make homemade desserts for custom orders, local markets, and community events around the Capital Region.</p>
<a class="inline-link" href="/about">A little more about me →</a>
```

- [ ] **Step 5: Replace the final CTA**

Use:

```astro
<p class="eyebrow">Start with a message</p>
<h2>Have something in mind?</h2>
<p>Send me the date and the treats you’re thinking about. I’ll take it from there.</p>
<a class="button" href="/custom-orders">Ask about an order</a>
```

- [ ] **Step 6: Run page checks**

Run:

```bash
npm run check
npm run build
```

Expected: both pass.

Read the homepage aloud once. Expected: no sentence uses “built around,” “intentionally flexible,” “before anything is promised,” or “the moment you are celebrating.”

- [ ] **Step 7: Commit**

```bash
git add src/pages/index.astro
git commit -m "copy: give the homepage Misty's voice"
```

---

### Task 4: Rewrite Custom Orders, Markets, and About

**Files:**
- Modify: `src/pages/custom-orders.astro`
- Modify: `src/pages/markets.astro`
- Modify: `src/pages/about.astro`
- Modify: `content/events.json`

**Interfaces:**
- Consumes: existing `site.social.instagram` and `events` data.
- Produces: no new data shape.

- [ ] **Step 1: Rewrite the Custom Orders hero and checklist**

Use:

```astro
<p class="eyebrow">Custom orders</p>
<h1>Tell me what you’re celebrating—and what sounds good.</h1>
<p class="lede">Send me the date, how many people you’re ordering for, and the treats or flavors you have in mind. I’ll get back to you with what I can make, the price, and the pickup or delivery details.</p>
```

Change the checklist label to `What to send me` and use:

```astro
<li>What you’re celebrating</li>
<li>The date you need it</li>
<li>How many people you’re ordering for</li>
<li>The treats or flavors you have in mind</li>
<li>Any ingredient or allergy questions</li>
```

- [ ] **Step 2: Rewrite the Custom Orders process and CTA**

Use:

```astro
<article><span>01</span><h2>Send a message</h2><p>Share the date, the occasion, the quantity, and your treat ideas.</p></article>
<article><span>02</span><h2>We’ll figure it out</h2><p>I’ll tell you what I can make, what it will cost, and how much time I need.</p></article>
<article><span>03</span><h2>Lock in the details</h2><p>Payment and pickup or delivery are arranged before the order is accepted.</p></article>
```

Use this message block:

```astro
<p class="eyebrow">Ready when you are</p>
<h2>Send me a message on Instagram.</h2>
<p class="lede">The more details you include, the easier it is for me to give you a useful answer.</p>
```

Change the secondary button to `See what I make`.

Change the note heading to `Before the order is set` and keep the practical list.

- [ ] **Step 3: Rewrite `content/events.json`**

Use:

```json
{
  "upcoming": [],
  "announcement": "I don’t have a new market date posted yet. Follow me on Instagram and I’ll share the next one as soon as it’s set.",
  "pastPresence": [
    "Farmers markets",
    "Community events",
    "Seasonal pop-ups",
    "Local vendor gatherings"
  ]
}
```

- [ ] **Step 4: Rewrite the Markets page**

Use:

```astro
<p class="eyebrow">Markets & community events</p>
<h1>Find Rare Treats 518 out in the community.</h1>
<p class="lede">I bring a changing mix of cookies, brownies, packaged treats, and seasonal specials to markets and local events around the Capital Region.</p>
```

Change the date card to:

```astro
<span>Next market</span>
<strong>Nothing posted yet</strong>
```

Use this visit section:

```astro
<p class="eyebrow">Before you visit</p>
<h2>Come early if you want the most choices.</h2>
```

```astro
<p>I bring a different mix to each event, and popular treats can sell out. Check Instagram before you head over for the newest details.</p>
<p>If you need a larger amount or something for a specific date, send a custom-order message instead.</p>
```

- [ ] **Step 5: Rewrite the About page without inventing history**

Use this hero:

```astro
<p class="eyebrow">About Rare Treats 518</p>
<h1>Hi, I’m Misty.</h1>
<p class="lede">I’m the owner of Rare Treats 518, a small dessert business based in Troy. I make homemade treats for custom orders, markets, and community events around the Capital Region.</p>
```

Change the portrait label to `Misty · Owner of Rare Treats 518`.

Use this story section:

```astro
<p class="eyebrow">Made in Troy</p>
<h2>Homemade treats, made personally.</h2>
```

```astro
<p class="lede">Rare Treats 518 is my way of sharing the desserts I make with people around Troy and the Capital Region.</p>
<p>The menu changes with the season, the event, and the orders I’m working on. That means there’s usually something new to see.</p>
<p>If you have a celebration coming up, send me the details. If you spot my table at a market, come say hi and see what I brought.</p>
```

Replace the three value cards with:

```astro
<article><span>01</span><h2>Homemade</h2><p>I make the treats myself and keep the menu flexible.</p></article>
<article><span>02</span><h2>Personal</h2><p>Custom orders start with your date, your idea, and a real conversation.</p></article>
<article><span>03</span><h2>Local</h2><p>Rare Treats 518 is based in Troy and shows up at events around the Capital Region.</p></article>
```

Change the CTA headline to `See what I’m making next.`

- [ ] **Step 6: Build and review the three pages**

Run:

```bash
npm run verify:content
npm run check
npm run build
```

Expected: all pass.

Render `/custom-orders`, `/markets`, and `/about` at 390px and 1440px. Expected: headings wrap naturally, no paragraph exceeds a comfortable mobile width, and no card contains accidental empty vertical space.

- [ ] **Step 7: Commit**

```bash
git add content/events.json src/pages/custom-orders.astro src/pages/markets.astro src/pages/about.astro
git commit -m "copy: make orders markets and about feel personal"
```

---

### Task 5: Simplify FAQ, Contact, and policy language

**Files:**
- Modify: `content/policies.json`
- Modify: `content/site.json`
- Modify: `src/pages/faq.astro`
- Modify: `src/pages/contact.astro`

**Interfaces:**
- Consumes: the current `policies` and `site` object shapes.
- Produces: no schema changes.

- [ ] **Step 1: Rewrite `content/policies.json`**

Use:

```json
{
  "approved": false,
  "allergenNotice": "Please ask about ingredients and allergens before ordering. An allergy or dietary request is not accepted until Misty has reviewed it.",
  "payment": "Misty confirms the total, payment method, and any deposit before accepting the order.",
  "changesAndCancellations": "Cancellation, change, and refund terms are explained before payment.",
  "pickupAndDelivery": "Pickup or delivery details, timing, location, and any fee are arranged for each order.",
  "shipping": "Shipping is not currently offered. Accepted orders use an arranged pickup or local delivery."
}
```

- [ ] **Step 2: Simplify ordering labels in `content/site.json`**

Keep all existing keys and confirmed values, but replace the ordering object with:

```json
"ordering": {
  "enabled": true,
  "method": "Instagram message",
  "leadTime": "Ask early; timing depends on the date, quantity, and treats",
  "delivery": "Pickup or local delivery is arranged for each accepted order"
}
```

Do not alter `previewMode`, contact fields, social URLs, or hidden services.

- [ ] **Step 3: Replace the FAQ answers with shorter wording**

Use:

```js
const faqs = [
  { question: "How do I request an order?", answer: "Send a message on Instagram with the date, the occasion, how many people you’re ordering for, and what treats you have in mind. Misty will reply with availability and pricing." },
  { question: "Is there a permanent menu?", answer: "No. Flavors and seasonal treats change, so the Treats page shows the main categories and Instagram shows what’s current." },
  { question: "How much notice should I give?", answer: "Send your request as early as you can. The amount of time needed depends on the date, quantity, and treats." },
  { question: "Can Rare Treats accommodate allergies or dietary needs?", answer: policies.allergenNotice },
  { question: "How do payment and deposits work?", answer: policies.payment },
  { question: "Where do I pick up my order?", answer: policies.pickupAndDelivery },
  { question: "What happens if I need to change or cancel?", answer: policies.changesAndCancellations },
  { question: "Does Rare Treats ship?", answer: policies.shipping }
];
```

Use this FAQ hero:

```astro
<p class="eyebrow">Frequently asked questions</p>
<h1>A few things to know before you order.</h1>
<p class="lede">Here are the basics. Anything that depends on your date or order will be worked out with Misty before you pay.</p>
```

Change the CTA headline to `See what I make, then send me your idea.`

- [ ] **Step 4: Rewrite the Contact page**

Use:

```astro
<p class="eyebrow">Contact Rare Treats 518</p>
<h1>Send me a message.</h1>
<p class="lede">Use Instagram for custom orders, treat questions, and market updates. Include your date and what you have in mind so I can give you a useful answer.</p>
```

Change the contact-card text to:

```astro
<p>Custom orders, treat questions, and market updates</p>
<i>Message me →</i>
```

Use these three cards:

```astro
<article><span>01</span><h2>Ordering treats</h2><p>Send the date, how many people, what you’re celebrating, and what sounds good.</p><a href="/custom-orders">See what to include →</a></article>
<article><span>02</span><h2>Finding a market</h2><p>Instagram is where I post confirmed dates and what I’m bringing.</p><a href="/markets">See market information →</a></article>
<article><span>03</span><h2>Quick questions</h2><p>The FAQ covers payment, pickup, ingredients, changes, and shipping.</p><a href="/faq">Read the FAQ →</a></article>
```

- [ ] **Step 5: Run content and build checks**

Run:

```bash
npm run verify:content
npm run check
npm run build
npm run verify:build
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
git add content/policies.json content/site.json src/pages/faq.astro src/pages/contact.astro
git commit -m "copy: simplify practical ordering information"
```

---

### Task 6: Add full-site voice regression checks

**Files:**
- Create: `scripts/verify-voice.mjs`
- Modify: `package.json`
- Modify: `.github/workflows/validate.yml`

**Interfaces:**
- Consumes: `findVoiceViolations` from `scripts/lib/voice-audit.mjs`.
- Produces: `npm run verify:voice` with exit code 0 on success and 1 on violations.

- [ ] **Step 1: Create the full-site verifier**

Create `scripts/verify-voice.mjs`:

```js
import { readFile } from "node:fs/promises";
import { findVoiceViolations, normalizeCopy } from "./lib/voice-audit.mjs";

const files = [
  "content/treats.json",
  "content/events.json",
  "content/policies.json",
  "content/site.json",
  "src/pages/index.astro",
  "src/pages/treats.astro",
  "src/pages/custom-orders.astro",
  "src/pages/markets.astro",
  "src/pages/about.astro",
  "src/pages/faq.astro",
  "src/pages/contact.astro"
];

const forbiddenPhrases = [
  "the moment you are celebrating",
  "intentionally flexible",
  "limited by design",
  "built around",
  "before anything is promised",
  "the table changes every time you find it",
  "owner-led",
  "final public policy is approved"
];

const requiredMarkers = new Map([
  ["src/pages/index.astro", ["i make cookies"]],
  ["src/pages/custom-orders.astro", ["send me the date"]],
  ["src/pages/about.astro", ["hi, i'm misty"]],
  ["src/pages/contact.astro", ["send me a message"]]
]);

let failed = false;

for (const path of files) {
  const content = await readFile(path, "utf8");
  const violations = findVoiceViolations(content, forbiddenPhrases);

  for (const phrase of violations) {
    console.error(`${path}: remove template phrase "${phrase}"`);
    failed = true;
  }

  const normalized = normalizeCopy(content);
  const markers = requiredMarkers.get(path) ?? [];

  for (const marker of markers) {
    if (!normalized.includes(normalizeCopy(marker))) {
      console.error(`${path}: missing approved voice marker "${marker}"`);
      failed = true;
    }
  }
}

if (failed) {
  process.exit(1);
}

console.log("Customer copy voice verification passed.");
```

- [ ] **Step 2: Add package scripts**

Add:

```json
"verify:voice": "node scripts/verify-voice.mjs"
```

Keep `test:voice` from Task 1.

- [ ] **Step 3: Run both voice checks**

Run:

```bash
npm run test:voice
npm run verify:voice
```

Expected:

```text
Voice audit tests passed.
Customer copy voice verification passed.
```

- [ ] **Step 4: Add voice verification to GitHub Actions**

In `.github/workflows/validate.yml`, insert after `npm run verify:content`:

```yaml
      - run: npm run test:voice
      - run: npm run verify:voice
```

- [ ] **Step 5: Run the full local validation sequence**

Run:

```bash
npm ci
npm run verify:content
npm run test:voice
npm run verify:voice
npm run check
npm run build
npm run verify:build
```

Expected: every command exits 0.

- [ ] **Step 6: Commit**

```bash
git add package.json scripts/verify-voice.mjs .github/workflows/validate.yml
git commit -m "ci: prevent robotic customer copy from returning"
```

---

### Task 7: Complete all-route visual QA and document the results

**Files:**
- Create: `docs/qa/2026-07-28-human-copy-layout-audit.md`
- Modify if defects are found: the affected page or `src/styles/mobile-polish.css`

**Interfaces:**
- Consumes: the built `dist` artifact.
- Produces: a written route-by-viewport QA record and final screenshots for review.

- [ ] **Step 1: Build the final artifact**

Run:

```bash
npm ci
npm run verify:content
npm run test:voice
npm run verify:voice
npm run check
npm run build
npm run verify:build
```

Expected: all pass.

- [ ] **Step 2: Serve the production output**

Run:

```bash
python3 -m http.server 4173 --directory dist
```

Expected: the site is available at `http://127.0.0.1:4173`.

- [ ] **Step 3: Render every route at every required width**

Use these routes:

```js
const routes = [
  ["home", "/"],
  ["treats", "/treats"],
  ["custom-orders", "/custom-orders"],
  ["markets", "/markets"],
  ["about", "/about"],
  ["faq", "/faq"],
  ["contact", "/contact"]
];
```

Use these viewports:

```js
const viewports = [
  ["320", 320, 800],
  ["390", 390, 844],
  ["430", 430, 932],
  ["768", 768, 1024],
  ["1440", 1440, 1000]
];
```

For every route and viewport, capture a full-page screenshot and evaluate:

```js
const metrics = await page.evaluate(() => ({
  viewportWidth: document.documentElement.clientWidth,
  scrollWidth: document.documentElement.scrollWidth,
  bodyScrollWidth: document.body.scrollWidth
}));

if (metrics.scrollWidth > metrics.viewportWidth || metrics.bodyScrollWidth > metrics.viewportWidth) {
  throw new Error(`Horizontal overflow: ${JSON.stringify(metrics)}`);
}
```

Expected: 35 screenshots and no horizontal-overflow errors.

- [ ] **Step 4: Check the specific Treats collision**

On every `/treats` viewport, evaluate each `.catalog-mark`:

```js
const collisions = await page.locator(".catalog-mark").evaluateAll((marks) =>
  marks.map((mark) => {
    const number = mark.querySelector(".catalog-number")?.getBoundingClientRect();
    const icon = mark.querySelector(".icon")?.getBoundingClientRect();

    if (!number || !icon) return false;

    return !(
      number.right <= icon.left ||
      number.left >= icon.right ||
      number.bottom <= icon.top ||
      number.top >= icon.bottom
    );
  })
);

if (collisions.some(Boolean)) {
  throw new Error(`Treat number/icon collision detected: ${collisions}`);
}
```

Expected: every value is `false`.

- [ ] **Step 5: Check interactions and console output**

At 390px:

1. Open the mobile navigation and confirm all links are visible inside the viewport.
2. Open the second FAQ item and confirm its answer becomes visible.
3. Record every `console.error`, `pageerror`, and failed request.

Expected: no console errors, page errors, failed local assets, clipped menu links, or broken FAQ behavior.

- [ ] **Step 6: Perform a human copy read-through**

Read every page at 390px and desktop. Confirm:

- body text sounds natural aloud;
- no page repeats the same order caveat more than once;
- first-person copy appears only where Misty is speaking;
- practical policy wording remains neutral;
- no unconfirmed claim was added;
- no paragraph looks like internal development documentation.

Fix any failure in the page or JSON file where it appears, then rerun Tasks 6 and 7.

- [ ] **Step 7: Write the QA record**

Create `docs/qa/2026-07-28-human-copy-layout-audit.md` with this structure and completed values:

```markdown
# Human Copy and Layout Audit

## Automated checks

- `npm ci`: pass
- `npm run verify:content`: pass
- `npm run test:voice`: pass
- `npm run verify:voice`: pass
- `npm run check`: pass
- `npm run build`: pass
- `npm run verify:build`: pass

## Viewports

- 320 × 800: pass
- 390 × 844: pass
- 430 × 932: pass
- 768 × 1024: pass
- 1440 × 1000: pass

## Routes

- Home: pass
- Treats: pass; numbers and icons do not overlap
- Custom Orders: pass
- Markets: pass
- About: pass
- FAQ: pass; disclosure controls work
- Contact: pass

## Interaction and console checks

- Mobile navigation: pass
- FAQ expansion: pass
- Horizontal overflow: none
- Console errors: none
- Failed local assets: none

## Copy review

The site uses brand-focused headlines, Misty’s first-person voice for descriptive sections, and neutral wording for payment, pickup, ingredients, and cancellation details. No prices, dates, policies, founder history, allergy accommodations, or services were invented.
```

- [ ] **Step 8: Commit**

```bash
git add docs/qa/2026-07-28-human-copy-layout-audit.md src content scripts package.json .github/workflows/validate.yml
git commit -m "docs: record full copy and responsive QA"
```

---

### Task 8: Open the review pull request

**Files:**
- No source changes expected.

**Interfaces:**
- Consumes: completed branch `refine/human-copy-and-layout-audit`.
- Produces: one reviewable pull request against `main`.

- [ ] **Step 1: Compare the branch with `main`**

Run:

```bash
git diff --check main...HEAD
git status --short
git log --oneline main..HEAD
```

Expected: no whitespace errors, clean working tree, and focused commits for tests, Treats layout, page copy, CI, and QA.

- [ ] **Step 2: Open the pull request**

Use title:

```text
Humanize site copy and complete layout audit
```

The body must state:

- Option C mixed voice was applied;
- the Treats number/icon collision was fixed structurally;
- all seven pages were rewritten where needed;
- no business facts or services were invented;
- automated validation passed;
- 35 route/viewport renders passed;
- the PR remains unmerged for user review.

- [ ] **Step 3: Leave the PR ready for review**

Expected: open, mergeable, non-draft PR against `main`. Do not merge it.
