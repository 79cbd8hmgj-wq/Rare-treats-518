import { access, readFile } from "node:fs/promises";

const requiredFiles = [
  "dist/index.html",
  "dist/treats/index.html",
  "dist/custom-orders/index.html",
  "dist/markets/index.html",
  "dist/about/index.html",
  "dist/faq/index.html",
  "dist/contact/index.html",
  "dist/robots.txt"
];

for (const path of requiredFiles) await access(path);

const home = await readFile("dist/index.html", "utf8");
if (!home.includes("Rare Treats 518")) throw new Error("Homepage build is missing the business name.");
if (!home.includes("noindex")) throw new Error("Preview build must remain noindex until launch approval.");

console.log("Production build output verified.");
