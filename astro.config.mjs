import { defineConfig } from "astro/config";

const fallbackSite = "https://rare-treats-518.pages.dev";
const configuredSite = process.env.PUBLIC_SITE_URL?.trim();

export default defineConfig({
  site: configuredSite || fallbackSite,
  output: "static",
  build: {
    format: "directory",
  },
});
