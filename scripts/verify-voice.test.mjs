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
    "Pick a favorite—or ask what is new.",
    ["—", "–"]
  ),
  ["—"]
);

assert.deepEqual(
  findVoiceViolations(
    "I make cookies, brownies, and seasonal treats in Troy.",
    ["intentionally flexible", "built around", "—", "–"]
  ),
  []
);

console.log("Voice audit tests passed.");
