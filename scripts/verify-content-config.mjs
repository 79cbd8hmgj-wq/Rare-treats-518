import { readFile } from "node:fs/promises";
import process from "node:process";

const isLaunchCheck = process.argv.includes("--launch");
const root = new URL("../", import.meta.url);
const readJson = async (path) => JSON.parse(await readFile(new URL(path, root), "utf8"));

const [site, treats, events, policies, gallery] = await Promise.all([
  readJson("content/site.json"),
  readJson("content/treats.json"),
  readJson("content/events.json"),
  readJson("content/policies.json"),
  readJson("content/gallery.json")
]);

const errors = [];
const warnings = [];
const requiredStrings = [
  [site.businessName, "site.businessName"],
  [site.ownerName, "site.ownerName"],
  [site.locationLabel, "site.locationLabel"],
  [site.tagline, "site.tagline"],
  [site.social?.instagram, "site.social.instagram"]
];

for (const [value, label] of requiredStrings) {
  if (typeof value !== "string" || value.trim().length === 0) errors.push(`${label} is required.`);
}

if (!Array.isArray(treats.categories) || treats.categories.length < 4) {
  errors.push("content/treats.json must define at least four treat categories.");
}

const slugs = new Set();
for (const category of treats.categories ?? []) {
  if (!category.slug || !category.name || !category.shortDescription || !category.longDescription) {
    errors.push("Every treat category requires slug, name, shortDescription, and longDescription.");
  }
  if (slugs.has(category.slug)) errors.push(`Duplicate treat slug: ${category.slug}`);
  slugs.add(category.slug);
}

if ((site.hiddenServices ?? []).some((item) => !["savory food", "catering"].includes(item))) {
  warnings.push("Unexpected hidden service found; confirm the public scope before launch.");
}

if (events.upcoming.length === 0) warnings.push("No upcoming market dates are currently published.");
if (!site.publicEmail && !site.publicPhone) warnings.push("No public business email or phone is configured; Instagram is the only contact channel.");
if (!gallery.publicationApproved || gallery.images.length === 0) warnings.push("No publication-approved gallery images are configured.");
if (!policies.approved) warnings.push("Public policies are still in draft status.");

if (isLaunchCheck) {
  if (site.previewMode) errors.push("site.previewMode must be false for launch.");
  if (!site.publicEmail) errors.push("A public business email is required for launch.");
  if (!policies.approved) errors.push("Policies must be owner-approved for launch.");
  if (!gallery.publicationApproved || gallery.images.length === 0) errors.push("Approved product or owner photography is required for launch.");
  if (events.upcoming.length === 0) warnings.push("Launch is allowed without an upcoming event, but the Markets page will show an announcement-only state.");
  if (!process.env.PUBLIC_SITE_URL || process.env.PUBLIC_SITE_URL.includes("pages.dev")) {
    errors.push("Set PUBLIC_SITE_URL to the approved production URL before launch.");
  }
}

for (const warning of warnings) console.warn(`Warning: ${warning}`);
if (errors.length > 0) {
  for (const error of errors) console.error(`Error: ${error}`);
  process.exit(1);
}

console.log(isLaunchCheck ? "Launch content validation passed." : "Foundation content validation passed.");
