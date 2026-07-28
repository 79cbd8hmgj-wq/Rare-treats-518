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
