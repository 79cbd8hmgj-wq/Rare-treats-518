from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text()


def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def replace_one(path, old, new):
    content = read(path)
    count = content.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one match, found {count}: {old[:90]!r}")
    write(path, content.replace(old, new, 1))


# Task 1: dependency-free voice audit library and tests.
write("scripts/lib/voice-audit.mjs", '''export function normalizeCopy(value) {
  return value
    .replace(/[’‘]/g, "'")
    .replace(/\\s+/g, " ")
    .trim()
    .toLowerCase();
}

export function findVoiceViolations(content, forbiddenPhrases) {
  const normalizedContent = normalizeCopy(content);

  return forbiddenPhrases.filter((phrase) =>
    normalizedContent.includes(normalizeCopy(phrase))
  );
}
''')

write("scripts/verify-voice.test.mjs", '''import assert from "node:assert/strict";
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
''')

package = json.loads(read("package.json"))
package["scripts"]["test:voice"] = "node scripts/verify-voice.test.mjs"
write("package.json", json.dumps(package, indent=2) + "\n")

# Task 2: Treats page structure and copy.
write("content/treats.json", '''{
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
''')

replace_one("src/pages/treats.astro",
'''      <p class="eyebrow">The treat table</p>
      <h1>A menu built to rotate.</h1>
      <p class="lede">{treats.intro}</p>''',
'''      <p class="eyebrow">What I make</p>
      <h1>Pick a favorite—or ask what’s new.</h1>
      <p class="lede">{treats.intro}</p>''')

replace_one("src/pages/treats.astro",
'''          <div class:list={["number", `tone-${(index % 3) + 1}`]}><span>0{index + 1}</span><TreatIcon icon={category.icon} /></div>
          <div>
            <h2>{category.name}</h2>
            <p class="lede">{category.longDescription}</p>
          </div>''',
'''          <div class:list={["catalog-mark", `tone-${(index % 3) + 1}`]}>
            <span class="catalog-number">0{index + 1}</span>
            <TreatIcon icon={category.icon} />
          </div>
          <div class="catalog-copy">
            <h2>{category.name}</h2>
            <p class="lede">{category.longDescription}</p>
          </div>''')

replace_one("src/pages/treats.astro",
'''        <p class="eyebrow">Limited by design</p>
        <h2>Seasonal treats do not stay forever.</h2>''',
'''        <p class="eyebrow">Seasonal treats</p>
        <h2>Some favorites only show up for a little while.</h2>''')

replace_one("src/pages/treats.astro",
'''        <p class="lede">Holiday boxes, themed gift bags, limited flavors, and market-day specials are announced when they are ready. Instagram is the best place to see what is current.</p>
        <a class="button" href="https://www.instagram.com/raretreats518/" target="_blank" rel="noreferrer">See current updates</a>''',
'''        <p class="lede">I share holiday boxes, themed gift bags, limited flavors, and market specials on Instagram when they’re ready.</p>
        <a class="button" href="https://www.instagram.com/raretreats518/" target="_blank" rel="noreferrer">See what’s new</a>''')

replace_one("src/pages/treats.astro",
'''  .number {
    display: flex;
    min-height: 7.5rem;
    align-items: center;
    justify-content: space-between;
    gap: 0.6rem;
    padding: 0.8rem;
    border-radius: 1.4rem;
  }

  .number > span {
    align-self: flex-start;
    color: var(--blueberry-soft);
    font-size: 0.72rem;
    font-weight: 850;
  }''',
'''  .catalog-mark {
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
  }''')

replace_one("src/pages/treats.astro",
'''    .number {
      max-width: 8rem;
    }''',
'''    .catalog-mark {
      max-width: 8rem;
    }''')

replace_one("src/styles/mobile-polish.css",
'''  .catalog-row {
    grid-template-columns: 4.25rem minmax(0, 1fr) !important;
    gap: 0.8rem 1rem !important;
    align-items: start !important;
    padding: 1.15rem !important;
    border: 1px solid var(--line) !important;
    border-radius: 1.25rem;
    background: rgba(255, 255, 255, 0.76);
  }

  .catalog-row .number {
    position: relative;
    width: 4.25rem !important;
    max-width: none !important;
    min-height: 4.25rem !important;
    padding: 0.45rem !important;
    justify-content: center !important;
  }

  .catalog-row .number > span {
    position: absolute;
    top: 0.35rem;
    left: 0.45rem;
    font-size: 0.58rem !important;
  }

  .catalog-row .number .icon {
    width: 2.65rem !important;
    height: 2.65rem !important;
  }

  .catalog-row h2 {
    margin-bottom: 0.45rem !important;
    font-size: 1.75rem !important;
  }

  .catalog-row .lede {
    font-size: 0.93rem !important;
    line-height: 1.48;
  }

  .catalog-row .availability {
    grid-column: 2;
    display: flex !important;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.65rem !important;
  }''',
'''  .catalog-row {
    grid-template-columns: 4.75rem minmax(0, 1fr) !important;
    gap: 0.8rem 1rem !important;
    align-items: start !important;
    padding: 1.15rem !important;
    border: 1px solid var(--line) !important;
    border-radius: 1.25rem;
    background: rgba(255, 255, 255, 0.76);
  }

  .catalog-row .catalog-mark {
    width: 4.75rem !important;
    max-width: none !important;
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

  .catalog-row h2 {
    margin-bottom: 0.45rem !important;
    font-size: 1.75rem !important;
  }

  .catalog-row .lede {
    font-size: 0.93rem !important;
    line-height: 1.48;
  }

  .catalog-row .availability {
    grid-column: 2;
    display: flex !important;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.65rem !important;
  }''')

# Task 3: Homepage voice.
replacements = [
('''        <h1>Something sweet for the moment you are celebrating.</h1>
        <p class="lede">Cookies, brownies, dessert trays, gift bags, and seasonal treats made by Misty for parties, holidays, market days, or an ordinary craving.</p>''',
'''        <h1>Homemade treats for parties, holidays, and ordinary cravings.</h1>
        <p class="lede">I make cookies, brownies, dessert trays, gift bags, and seasonal treats in Troy, New York. If you have a date or an idea, send me a message and we’ll figure out what fits.</p>'''),
('''          <a class="button" href="/custom-orders">Request a custom order</a>
          <a class="button button-secondary" href="/treats">Explore the treats</a>''',
'''          <a class="button" href="/custom-orders">Ask about an order</a>
          <a class="button button-secondary" href="/treats">See the treats</a>'''),
('''          <h2>Favorites that change with the season.</h2>''','''          <h2>What’s on the table changes.</h2>'''),
('''        <p>The menu is intentionally flexible. Start with the category that fits your occasion, then message Misty about the date, quantity, and flavors you have in mind.</p>''',
'''        <p>I rotate flavors and seasonal treats, so the website shows the kinds of things I make instead of a fixed menu.</p>'''),
('''            <a href={`/treats#${category.slug}`}>See the details</a>''','''            <a href={`/treats#${category.slug}`}>Take a look</a>'''),
('''        <h2>Tell Misty what would make the occasion feel complete.</h2>
        <p>Every order starts as a conversation, so nothing is promised before the date, quantity, flavors, and pickup or delivery details are confirmed.</p>
        <a class="inline-link" href="/custom-orders">What to include in your message →</a>''',
'''        <h2>Tell me what you’re planning.</h2>
        <p>Send the date, how many people you’re ordering for, and what sounds good. I’ll let you know what I can make and what it will cost.</p>
        <a class="inline-link" href="/custom-orders">See what to send me →</a>'''),
('''        <li><span>01</span><div><h3>Share the idea</h3><p>Occasion, preferred date, guest count, and the treats you are considering.</p></div></li>
        <li><span>02</span><div><h3>Confirm the details</h3><p>Misty reviews availability, options, final pricing, payment, and handoff details.</p></div></li>
        <li><span>03</span><div><h3>Enjoy the treats</h3><p>Your accepted order is prepared for the date and arrangement you confirmed together.</p></div></li>''',
'''        <li><span>01</span><div><h3>Send the basics</h3><p>The date, the occasion, how many people, and what you’re thinking about.</p></div></li>
        <li><span>02</span><div><h3>We’ll figure it out</h3><p>I’ll reply with what I can make, the price, and the timing.</p></div></li>
        <li><span>03</span><div><h3>Set the details</h3><p>Payment and pickup or delivery are arranged before the order is accepted.</p></div></li>'''),
('''        <h2>Find the table, meet Misty, and see what is fresh that day.</h2>''','''        <h2>Come say hi at the next market.</h2>'''),
('''          <a class="button button-secondary" href="/markets">About market days</a>''','''          <a class="button button-secondary" href="/markets">Find me at a market</a>'''),
('''        <h2>A local business built around the joy of sharing food.</h2>''','''        <h2>Made by Misty in Troy.</h2>'''),
('''        <p class="lede">Rare Treats 518 is owned by Misty Bensalah. The brand brings homemade desserts to custom orders, community events, and local markets across the Capital Region.</p>
        <a class="inline-link" href="/about">Meet Misty and read the story →</a>''',
'''        <p class="lede">I’m Misty, the person behind Rare Treats 518. I make homemade desserts for custom orders, local markets, and community events around the Capital Region.</p>
        <a class="inline-link" href="/about">A little more about me →</a>'''),
('''      <h2>Have a date, celebration, or treat idea in mind?</h2>
      <p>Send Misty the basics and she can let you know what is possible.</p>
      <a class="button" href="/custom-orders">Plan a custom order</a>''',
'''      <h2>Have something in mind?</h2>
      <p>Send me the date and the treats you’re thinking about. I’ll take it from there.</p>
      <a class="button" href="/custom-orders">Ask about an order</a>''')
]
for old, new in replacements:
    replace_one("src/pages/index.astro", old, new)

# Task 4: Custom Orders, Markets, About, events.
write("content/events.json", '''{
  "upcoming": [],
  "announcement": "I don’t have a new market date posted yet. Follow me on Instagram and I’ll share the next one as soon as it’s set.",
  "pastPresence": [
    "Farmers markets",
    "Community events",
    "Seasonal pop-ups",
    "Local vendor gatherings"
  ]
}
''')

replacements = [
('''        <h1>Start with the occasion. Build the treats from there.</h1>
        <p class="lede">Misty handles custom requests through conversation so the menu, quantity, date, payment, and handoff can be confirmed before anything is promised.</p>''',
'''        <h1>Tell me what you’re celebrating—and what sounds good.</h1>
        <p class="lede">Send me the date, how many people you’re ordering for, and the treats or flavors you have in mind. I’ll get back to you with what I can make, the price, and the pickup or delivery details.</p>'''),
('''        <span>Include these five things</span>''','''        <span>What to send me</span>'''),
('''          <li>The occasion</li>
          <li>Your preferred date</li>
          <li>Estimated quantity or guest count</li>
          <li>The treats or flavors you are considering</li>
          <li>Any dietary or ingredient questions</li>''',
'''          <li>What you’re celebrating</li>
          <li>The date you need it</li>
          <li>How many people you’re ordering for</li>
          <li>The treats or flavors you have in mind</li>
          <li>Any ingredient or allergy questions</li>'''),
('''      <article><span>01</span><h2>Send the idea</h2><p>Use Instagram to introduce yourself and share the basic order details.</p></article>
      <article><span>02</span><h2>Review the options</h2><p>Misty confirms availability and discusses the exact products, quantity, final price, and timing.</p></article>
      <article><span>03</span><h2>Confirm the order</h2><p>Payment, pickup or delivery, and any change or cancellation terms are confirmed before the order is accepted.</p></article>''',
'''      <article><span>01</span><h2>Send a message</h2><p>Share the date, the occasion, the quantity, and your treat ideas.</p></article>
      <article><span>02</span><h2>We’ll figure it out</h2><p>I’ll tell you what I can make, what it will cost, and how much time I need.</p></article>
      <article><span>03</span><h2>Lock in the details</h2><p>Payment and pickup or delivery are arranged before the order is accepted.</p></article>'''),
('''        <p class="eyebrow">Ready to ask?</p>
        <h2>Message @raretreats518.</h2>
        <p class="lede">Instagram is the easiest place to start. Send the occasion, date, quantity, and treat ideas, then Misty can reply with what is available.</p>''',
'''        <p class="eyebrow">Ready when you are</p>
        <h2>Send me a message on Instagram.</h2>
        <p class="lede">The more details you include, the easier it is for me to give you a useful answer.</p>'''),
('''        <a class="button button-secondary" href="/treats">Review treat categories</a>''','''        <a class="button button-secondary" href="/treats">See what I make</a>'''),
('''      <h2>A few details to confirm together</h2>''','''      <h2>Before the order is set</h2>''')
]
for old, new in replacements:
    replace_one("src/pages/custom-orders.astro", old, new)

replacements = [
('''        <h1>The table changes every time you find it.</h1>
        <p class="lede">Market days are where Rare Treats 518 can bring rotating flavors, packaged treats, and limited specials directly into the community.</p>''',
'''        <h1>Find Rare Treats 518 out in the community.</h1>
        <p class="lede">I bring a changing mix of cookies, brownies, packaged treats, and seasonal specials to markets and local events around the Capital Region.</p>'''),
('''        <span>Next confirmed date</span>
        <strong>To be announced</strong>''','''        <span>Next market</span>
        <strong>Nothing posted yet</strong>'''),
('''        <h2>Come early for the widest selection.</h2>''','''        <h2>Come early if you want the most choices.</h2>'''),
('''        <p>Inventory can be different at every event and items may sell out. A social post or handwritten event menu is a snapshot of that date, not a permanent website catalog.</p>
        <p>For a specific celebration or larger quantity, use the custom-order process instead of relying on event inventory.</p>''',
'''        <p>I bring a different mix to each event, and popular treats can sell out. Check Instagram before you head over for the newest details.</p>
        <p>If you need a larger amount or something for a specific date, send a custom-order message instead.</p>''')
]
for old, new in replacements:
    replace_one("src/pages/markets.astro", old, new)

replacements = [
('''        <h1>Made by Misty. Shared across the community.</h1>
        <p class="lede">Rare Treats 518 is an owner-led Troy business centered on homemade desserts, custom requests, and the energy of local markets and events.</p>''',
'''        <h1>Hi, I’m Misty.</h1>
        <p class="lede">I’m the owner of Rare Treats 518, a small dessert business based in Troy. I make homemade treats for custom orders, markets, and community events around the Capital Region.</p>'''),
('''        <span>Made by Misty in Troy, New York</span>''','''        <span>Misty · Owner of Rare Treats 518</span>'''),
('''        <p class="eyebrow">A local, owner-led business</p>
        <h2>Homemade with love. Made for you.</h2>''',
'''        <p class="eyebrow">Made in Troy</p>
        <h2>Homemade treats, made personally.</h2>'''),
('''        <p class="lede">Misty Bensalah owns Rare Treats 518 LLC and brings the business to Troy-area markets, community events, and direct customer orders.</p>
        <p>The brand is built around a rotating dessert selection, a recognizable pastel-heart identity, and making each order feel personal.</p>
        <p>Whether someone finds the table at a community event or reaches out about a celebration, Rare Treats is meant to feel warm, approachable, and unmistakably local.</p>''',
'''        <p class="lede">Rare Treats 518 is my way of sharing the desserts I make with people around Troy and the Capital Region.</p>
        <p>The menu changes with the season, the event, and the orders I’m working on. That means there’s usually something new to see.</p>
        <p>If you have a celebration coming up, send me the details. If you spot my table at a market, come say hi and see what I brought.</p>'''),
('''      <article><span>01</span><h2>Made fresh</h2><p>The brand presents its treats as homemade and prepared with care.</p></article>
      <article><span>02</span><h2>Made personal</h2><p>Custom orders begin with a direct conversation instead of a rigid online catalog.</p></article>
      <article><span>03</span><h2>Made local</h2><p>Rare Treats 518 is proudly rooted in Troy and the greater Capital Region.</p></article>''',
'''      <article><span>01</span><h2>Homemade</h2><p>I make the treats myself and keep the menu flexible.</p></article>
      <article><span>02</span><h2>Personal</h2><p>Custom orders start with your date, your idea, and a real conversation.</p></article>
      <article><span>03</span><h2>Local</h2><p>Rare Treats 518 is based in Troy and shows up at events around the Capital Region.</p></article>'''),
('''      <div><p class="eyebrow">See what Misty is making</p><h2>Follow the newest treats and market dates.</h2></div>''',
'''      <div><p class="eyebrow">Follow along</p><h2>See what I’m making next.</h2></div>''')
]
for old, new in replacements:
    replace_one("src/pages/about.astro", old, new)

# Task 5: Policies, site labels, FAQ and Contact.
write("content/policies.json", '''{
  "approved": false,
  "allergenNotice": "Please ask about ingredients and allergens before ordering. An allergy or dietary request is not accepted until Misty has reviewed it.",
  "payment": "Misty confirms the total, payment method, and any deposit before accepting the order.",
  "changesAndCancellations": "Cancellation, change, and refund terms are explained before payment.",
  "pickupAndDelivery": "Pickup or delivery details, timing, location, and any fee are arranged for each order.",
  "shipping": "Shipping is not currently offered. Accepted orders use an arranged pickup or local delivery."
}
''')

site = json.loads(read("content/site.json"))
site["ordering"] = {
    "enabled": True,
    "method": "Instagram message",
    "leadTime": "Ask early; timing depends on the date, quantity, and treats",
    "delivery": "Pickup or local delivery is arranged for each accepted order"
}
write("content/site.json", json.dumps(site, indent=2, ensure_ascii=False) + "\n")

faq_path = "src/pages/faq.astro"
faq = read(faq_path)
start = faq.index("const faqs = [")
end = faq.index("];", start) + 2
faq_block = '''const faqs = [
  { question: "How do I request an order?", answer: "Send a message on Instagram with the date, the occasion, how many people you’re ordering for, and what treats you have in mind. Misty will reply with availability and pricing." },
  { question: "Is there a permanent menu?", answer: "No. Flavors and seasonal treats change, so the Treats page shows the main categories and Instagram shows what’s current." },
  { question: "How much notice should I give?", answer: "Send your request as early as you can. The amount of time needed depends on the date, quantity, and treats." },
  { question: "Can Rare Treats accommodate allergies or dietary needs?", answer: policies.allergenNotice },
  { question: "How do payment and deposits work?", answer: policies.payment },
  { question: "Where do I pick up my order?", answer: policies.pickupAndDelivery },
  { question: "What happens if I need to change or cancel?", answer: policies.changesAndCancellations },
  { question: "Does Rare Treats ship?", answer: policies.shipping }
];'''
write(faq_path, faq[:start] + faq_block + faq[end:])
replace_one(faq_path,
'''      <h1>What to know before you order.</h1>
      <p class="lede">Start here for the basics about ordering, availability, payment, pickup, ingredients, and changes. Misty confirms the details that depend on your specific request.</p>''',
'''      <h1>A few things to know before you order.</h1>
      <p class="lede">Here are the basics. Anything that depends on your date or order will be worked out with Misty before you pay.</p>''')
replace_one(faq_path,
'''      <div><p class="eyebrow">Still deciding?</p><h2>Review the treat categories, then send Misty the idea.</h2></div>''',
'''      <div><p class="eyebrow">Still deciding?</p><h2>See what I make, then send me your idea.</h2></div>''')

replacements = [
('''        <h1>The next order starts with a direct message.</h1>
        <p class="lede">Instagram is the best place to ask about custom orders, current treats, and upcoming market dates.</p>''',
'''        <h1>Send me a message.</h1>
        <p class="lede">Use Instagram for custom orders, treat questions, and market updates. Include your date and what you have in mind so I can give you a useful answer.</p>'''),
('''        <p>Order questions, current treats, and market updates</p>
        <i>Open profile →</i>''',
'''        <p>Custom orders, treat questions, and market updates</p>
        <i>Message me →</i>'''),
('''      <article><span>01</span><h2>For custom orders</h2><p>Include the occasion, date, quantity, treat ideas, and ingredient questions.</p><a href="/custom-orders">See the full checklist →</a></article>
      <article><span>02</span><h2>For market updates</h2><p>Follow the social feed for confirmed dates, event menus, and limited seasonal announcements.</p><a href="/markets">Learn about market days →</a></article>
      <article><span>03</span><h2>For general questions</h2><p>Review the FAQ before messaging for quick answers about ordering, payment, pickup, ingredients, and changes.</p><a href="/faq">Read the FAQ →</a></article>''',
'''      <article><span>01</span><h2>Ordering treats</h2><p>Send the date, how many people, what you’re celebrating, and what sounds good.</p><a href="/custom-orders">See what to include →</a></article>
      <article><span>02</span><h2>Finding a market</h2><p>Instagram is where I post confirmed dates and what I’m bringing.</p><a href="/markets">See market information →</a></article>
      <article><span>03</span><h2>Quick questions</h2><p>The FAQ covers payment, pickup, ingredients, changes, and shipping.</p><a href="/faq">Read the FAQ →</a></article>''')
]
for old, new in replacements:
    replace_one("src/pages/contact.astro", old, new)

# Task 6: full-site voice verification.
write("scripts/verify-voice.mjs", '''import { readFile } from "node:fs/promises";
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
''')

package = json.loads(read("package.json"))
package["scripts"]["verify:voice"] = "node scripts/verify-voice.mjs"
write("package.json", json.dumps(package, indent=2) + "\n")

print("Human copy and layout patch applied.")
